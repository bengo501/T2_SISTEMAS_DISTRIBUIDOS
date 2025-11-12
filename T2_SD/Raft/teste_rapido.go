//go:build teste_rapido

package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"
	"time"
)

func main() {
	fmt.Println(strings.Repeat("=", 80))
	fmt.Println("teste rapido - raft")
	fmt.Println(strings.Repeat("=", 80))

	fmt.Println("\n[1/3] verificando se o cluster esta rodando...")

	urls := []string{
		"http://localhost:8000",
		"http://localhost:8001",
		"http://localhost:8002",
	}

	var leaderURL string
	for i := 0; i < 30; i++ {
		for _, url := range urls {
			resp, err := http.Get(url + "/status")
			if err == nil {
				var status struct {
					State string `json:"state"`
				}
				if err := json.NewDecoder(resp.Body).Decode(&status); err == nil {
					if status.State == "StateLeader" {
						leaderURL = url
						resp.Body.Close()
						break
					}
				}
				resp.Body.Close()
			}
		}
		if leaderURL != "" {
			break
		}
		time.Sleep(1 * time.Second)
	}

	if leaderURL == "" {
		log.Fatal("[ERRO] cluster nao encontrado. inicie 3 replicas primeiro:\n  Terminal 1: go run main.go --id 1 --port 8000\n  Terminal 2: go run main.go --id 2 --port 8001\n  Terminal 3: go run main.go --id 3 --port 8002")
	}

	fmt.Printf("[OK] cluster encontrado (lider: %s)\n", leaderURL)

	fmt.Println("\n[2/3] testando envio de proposta...")

	client := &http.Client{Timeout: 5 * time.Second}
	req, err := http.NewRequest("POST", leaderURL+"/propose", strings.NewReader(`{"data":"teste_rapido"}`))
	if err != nil {
		log.Fatalf("[ERRO] erro ao criar request: %v", err)
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		log.Fatalf("[ERRO] erro ao enviar proposta: %v", err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	if resp.StatusCode != http.StatusOK {
		log.Fatalf("[ERRO] proposta falhou (status: %d, body: %s)", resp.StatusCode, string(body))
	}

	fmt.Println("[OK] proposta enviada com sucesso")

	fmt.Println("\n[3/3] verificando status do cluster...")

	for i, url := range urls {
		resp, err := http.Get(url + "/status")
		if err != nil {
			fmt.Printf("[AVISO] no %d nao acessivel\n", i+1)
			continue
		}

		var status struct {
			ID     uint64 `json:"id"`
			Term   uint64 `json:"term"`
			Leader uint64 `json:"leader"`
			State  string `json:"state"`
		}
		if err := json.NewDecoder(resp.Body).Decode(&status); err == nil {
			fmt.Printf("[OK] no %d: term=%d, leader=%d, state=%s\n",
				status.ID, status.Term, status.Leader, status.State)
		}
		resp.Body.Close()
	}

	fmt.Println("\n" + strings.Repeat("=", 80))
	fmt.Println("teste rapido concluido com sucesso!")
	fmt.Println(strings.Repeat("=", 80))
	fmt.Println("\npronto para executar benchmark completo:")
	fmt.Println("  go run -tags benchmark . --duracao 180 --cargas 1,2,3,4")
}
