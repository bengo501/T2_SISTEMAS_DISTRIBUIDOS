package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"sync"

	"go.etcd.io/raft/v3"
	"go.etcd.io/raft/v3/raftpb"
)

type Transport struct {
	id        uint64
	port      int
	peerPorts []int
	node      raft.Node
	mu        sync.Mutex
}

func NewTransport(id uint64, port int, peerPorts []int) *Transport {
	return &Transport{
		id:        id,
		port:      port,
		peerPorts: peerPorts,
	}
}

func (t *Transport) SetNode(node raft.Node) {
	t.mu.Lock()
	defer t.mu.Unlock()
	t.node = node
}

func (t *Transport) Start() {
	http.HandleFunc("/raft/message", t.handleMessage)
	go func() {
		addr := fmt.Sprintf(":%d", t.port+1000)
		log.Printf("transport %d: servindo em %s", t.id, addr)
		if err := http.ListenAndServe(addr, nil); err != nil {
			log.Fatalf("transport %d: erro ao iniciar: %v", t.id, err)
		}
	}()
}

func (t *Transport) Stop() {
}

func (t *Transport) Send(messages []raftpb.Message) {
	t.mu.Lock()
	defer t.mu.Unlock()

	for _, msg := range messages {
		if msg.To == 0 {
			continue
		}

		peerPort := t.peerPorts[msg.To-1]
		if peerPort == 0 {
			continue
		}

		data, err := msg.Marshal()
		if err != nil {
			log.Printf("transport %d: erro ao marshal: %v", t.id, err)
			continue
		}

		url := fmt.Sprintf("http://localhost:%d/raft/message", peerPort+1000)
		resp, err := http.Post(url, "application/x-protobuf", bytes.NewReader(data))
		if err != nil {
			continue
		}
		resp.Body.Close()
	}
}

func (t *Transport) handleMessage(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "método não permitido", http.StatusMethodNotAllowed)
		return
	}

	data, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, fmt.Sprintf("erro ao ler: %v", err), http.StatusBadRequest)
		return
	}

	var msg raftpb.Message
	if err := msg.Unmarshal(data); err != nil {
		http.Error(w, fmt.Sprintf("erro ao unmarshal: %v", err), http.StatusBadRequest)
		return
	}

	t.mu.Lock()
	node := t.node
	t.mu.Unlock()

	if node != nil {
		node.Step(context.Background(), msg)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}
