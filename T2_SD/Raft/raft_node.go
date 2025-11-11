package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"

	"go.etcd.io/raft/v3"
	"go.etcd.io/raft/v3/raftpb"
)

type RaftNode struct {
	id            uint64
	port          int
	node          raft.Node
	storage       *memoryStorage
	transport     *Transport
	proposeC      chan []byte
	confChangeC   chan raftpb.ConfChange
	commitC       chan *commit
	done          chan struct{}
	mu            sync.Mutex
	lastIndex     uint64
	commits       map[uint64]bool
	committedData map[string]bool
}

type commit struct {
	data      []byte
	index     uint64
	term      uint64
	committed chan bool
}

func NewRaftNode(id uint64, peers []raft.Peer, port int, peerPorts []int) (*RaftNode, error) {
	storage := newMemoryStorage()
	cfg := &raft.Config{
		ID:              id,
		ElectionTick:    10,
		HeartbeatTick:   1,
		Storage:         storage,
		MaxSizePerMsg:   4096,
		MaxInflightMsgs: 256,
	}

	node := raft.StartNode(cfg, peers)

	transport := NewTransport(id, port, peerPorts)

	rn := &RaftNode{
		id:            id,
		port:          port,
		node:          node,
		storage:       storage,
		transport:     transport,
		proposeC:      make(chan []byte, 1000),
		confChangeC:   make(chan raftpb.ConfChange, 100),
		commitC:       make(chan *commit, 1000),
		done:          make(chan struct{}),
		commits:       make(map[uint64]bool),
		committedData: make(map[string]bool),
	}

	transport.SetNode(node)
	transport.Start()

	go rn.serveRaft()
	go rn.serveHTTP()
	go rn.processCommits()

	// força início de eleição no nó 1 para evitar cluster sem líder
	if id == 1 {
		go func() {
			time.Sleep(500 * time.Millisecond)
			_ = node.Campaign(context.Background())
		}()
	}

	return rn, nil
}

func (rn *RaftNode) serveRaft() {
	ticker := time.NewTicker(100 * time.Millisecond)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			rn.node.Tick()
		case rd := <-rn.node.Ready():
			rn.storage.Lock()
			if err := rn.storage.Append(rd.Entries); err != nil {
				log.Fatalf("raft %d: append entries error: %v", rn.id, err)
			}
			if !raft.IsEmptyHardState(rd.HardState) {
				if err := rn.storage.SetHardState(rd.HardState); err != nil {
					log.Fatalf("raft %d: set hardstate error: %v", rn.id, err)
				}
			}
			if !raft.IsEmptySnap(rd.Snapshot) {
				if err := rn.storage.ApplySnapshot(rd.Snapshot); err != nil {
					log.Fatalf("raft %d: apply snapshot error: %v", rn.id, err)
				}
			}
			rn.storage.Unlock()

			rn.transport.Send(rd.Messages)

			for _, entry := range rd.CommittedEntries {
				if entry.Type == raftpb.EntryConfChange {
					var cc raftpb.ConfChange
					cc.Unmarshal(entry.Data)
					rn.node.ApplyConfChange(cc)
				} else if entry.Type == raftpb.EntryNormal {
					if len(entry.Data) > 0 {
						rn.commitC <- &commit{
							data:      entry.Data,
							index:     entry.Index,
							term:      entry.Term,
							committed: make(chan bool, 1),
						}
					}
				}
			}

			rn.node.Advance()
		case <-rn.done:
			return
		}
	}
}

func (rn *RaftNode) processCommits() {
	for commit := range rn.commitC {
		rn.mu.Lock()
		rn.commits[commit.index] = true
		rn.lastIndex = commit.index
		rn.committedData[string(commit.data)] = true
		rn.mu.Unlock()
		commit.committed <- true
	}
}

func (rn *RaftNode) Propose(data []byte) error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	return rn.node.Propose(ctx, data)
}

func (rn *RaftNode) WaitForDataCommit(data []byte, timeout time.Duration) bool {
	deadline := time.Now().Add(timeout)
	key := string(data)
	for time.Now().Before(deadline) {
		rn.mu.Lock()
		ok := rn.committedData[key]
		rn.mu.Unlock()
		if ok {
			return true
		}
		time.Sleep(10 * time.Millisecond)
	}
	return false
}

func (rn *RaftNode) WaitForCommit(index uint64, timeout time.Duration) bool {
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		rn.mu.Lock()
		if rn.commits[index] {
			rn.mu.Unlock()
			return true
		}
		rn.mu.Unlock()
		time.Sleep(10 * time.Millisecond)
	}
	return false
}

func (rn *RaftNode) serveHTTP() {
	mux := http.NewServeMux()
	mux.HandleFunc("/propose", rn.handlePropose)
	mux.HandleFunc("/status", rn.handleStatus)
	mux.HandleFunc("/health", rn.handleHealth)
	mux.HandleFunc("/campaign", rn.handleCampaign)

	addr := fmt.Sprintf(":%d", rn.port)
	log.Printf("raft %d: servindo http em %s", rn.id, addr)
	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatalf("raft %d: erro ao iniciar http server: %v", rn.id, err)
	}
}

func (rn *RaftNode) handleCampaign(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "método não permitido", http.StatusMethodNotAllowed)
		return
	}
	go func() {
		_ = rn.node.Campaign(context.Background())
	}()
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"ok":  true,
		"id":  rn.id,
		"msg": "campaign solicitado",
	})
}

func (rn *RaftNode) handlePropose(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "método não permitido", http.StatusMethodNotAllowed)
		return
	}

	var req struct {
		Data string `json:"data"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, fmt.Sprintf("erro ao decodificar: %v", err), http.StatusBadRequest)
		return
	}

	if err := rn.Propose([]byte(req.Data)); err != nil {
		http.Error(w, fmt.Sprintf("erro ao propor: %v", err), http.StatusInternalServerError)
		return
	}

	timeout := 5 * time.Second
	if !rn.WaitForDataCommit([]byte(req.Data), timeout) {
		http.Error(w, "timeout aguardando commit", http.StatusRequestTimeout)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"success": true,
		"data":    req.Data,
	})
}

func (rn *RaftNode) handleStatus(w http.ResponseWriter, r *http.Request) {
	status := rn.node.Status()
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"id":     rn.id,
		"term":   status.Term,
		"leader": status.Lead,
		"state":  status.RaftState.String(),
	})
}

func (rn *RaftNode) handleHealth(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("ok"))
}

func (rn *RaftNode) Stop() {
	close(rn.done)
	rn.node.Stop()
	rn.transport.Stop()
}
