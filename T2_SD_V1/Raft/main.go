package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"

	"go.etcd.io/raft/v3"
)

func main() {
	var id = flag.Int("id", 1, "id do nó raft")
	var port = flag.Int("port", 8000, "porta do nó raft")
	flag.Parse()

	if *id < 1 || *id > 3 {
		log.Fatalf("id deve estar entre 1 e 3")
	}

	peers := []raft.Peer{
		{ID: 1},
		{ID: 2},
		{ID: 3},
	}

	peerPorts := []int{8000, 8001, 8002}

	node, err := NewRaftNode(uint64(*id), peers, *port, peerPorts)
	if err != nil {
		log.Fatalf("erro ao criar nó raft: %v", err)
	}

	fmt.Printf("nó raft %d iniciado na porta %d\n", *id, *port)
	fmt.Printf("aguardando sinal para parar...\n")

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	<-sigChan

	fmt.Printf("\nparando nó raft %d...\n", *id)
	node.Stop()
	fmt.Printf("nó raft %d parado\n", *id)
}
