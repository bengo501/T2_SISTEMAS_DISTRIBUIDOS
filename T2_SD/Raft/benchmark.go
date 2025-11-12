package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
	"sort"
	"strconv"
	"sync"
	"time"
)

type Benchmark struct {
	raftURLs     []string
	duracao      time.Duration
	cargas       []int
	outputCSV    string
	outputPNG    string
	outputCDFDir string

	procs []*exec.Cmd
}

func NewBenchmark(raftURLs []string, duracao time.Duration, cargas []int) *Benchmark {
	return &Benchmark{
		raftURLs:     raftURLs,
		duracao:      duracao,
		cargas:       cargas,
		outputCSV:    "resultados_desempenho.csv",
		outputPNG:    "grafico_vazao_latencia.png",
		outputCDFDir: "cdf_latencia",
		procs:        make([]*exec.Cmd, 0, 3),
	}
}

type Resultado struct {
	nroClientes int
	vazao       float64
	latencia    float64
	latencies   []float64
}

func (b *Benchmark) Run() error {
	os.MkdirAll(b.outputCDFDir, 0755)

	resultados := make([]Resultado, 0)

	for _, nClients := range b.cargas {
		fmt.Printf("[rodada] reiniciando cluster | %d clientes por %s\n", nClients, b.duracao)

		thr, lat, latencies := b.runRoundWithRestart(nClients)

		resultados = append(resultados, Resultado{
			nroClientes: nClients,
			vazao:       thr,
			latencia:    lat,
			latencies:   latencies,
		})

		fmt.Printf(" -> vazão=%.2f ops/s | latência média=%.4fs | amostras=%d\n", thr, lat, len(latencies))
	}

	if err := b.saveCSV(resultados); err != nil {
		return err
	}

	if err := b.generateGraph(resultados); err != nil {
		return err
	}

	if err := b.generateCDFGraphs(resultados); err != nil {
		return err
	}

	return nil
}

func (b *Benchmark) runRoundWithRestart(nClients int) (throughput float64, avgLatency float64, latencies []float64) {
	// conforme enunciado: "subir replicas"
	b.startCluster()

	// conforme enunciado: "esperar estarem ativas"
	// aguarda cluster estar pronto antes de iniciar clientes
	if !b.waitForClusterReady(30 * time.Second) {
		log.Printf("aviso: cluster pode nao estar totalmente pronto, continuando mesmo assim")
	}

	// conforme enunciado: "subir nro de clientes [cliente]"
	clients := make([]*Client, nClients)
	var wg sync.WaitGroup

	for i := 0; i < nClients; i++ {
		client := NewClient(i, b.raftURLs, b.duracao)
		clients[i] = client
		wg.Add(1)
		go func(c *Client) {
			defer wg.Done()
			c.Run()
		}(client)
	}

	wg.Wait()

	allLatencies := make([]float64, 0)
	totalThroughput := 0.0
	sumAvgLatency := 0.0

	for _, client := range clients {
		thr, avgLat, lats := client.GetMetrics()
		totalThroughput += thr
		sumAvgLatency += avgLat
		allLatencies = append(allLatencies, lats...)
	}

	avgLatency = sumAvgLatency / float64(nClients)
	throughput = totalThroughput

	b.stopCluster()
	time.Sleep(500 * time.Millisecond)

	return throughput, avgLatency, allLatencies
}

func (b *Benchmark) startCluster() {
	// tenta parar cluster anterior
	b.stopCluster()
	time.Sleep(300 * time.Millisecond)

	b.procs = b.procs[:0]
	for i := 0; i < 3; i++ {
		port := 8000 + i
		cmd := exec.Command("go", "run", ".", "--id", strconv.Itoa(i+1), "--port", strconv.Itoa(port))
		cmd.Dir = "."
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		if err := cmd.Start(); err == nil {
			b.procs = append(b.procs, cmd)
		}
	}
}

func (b *Benchmark) stopCluster() {
	for _, p := range b.procs {
		if p != nil && p.Process != nil {
			_ = p.Process.Kill()
			_, _ = p.Process.Wait()
		}
	}
	b.procs = b.procs[:0]
}

// waitForClusterReady aguarda o cluster estar pronto antes de iniciar clientes
// conforme requisito do enunciado: "esperar estarem ativas"
func (b *Benchmark) waitForClusterReady(timeout time.Duration) bool {
	deadline := time.Now().Add(timeout)

	for time.Now().Before(deadline) {
		// verifica se há um líder eleito
		leader := b.findLeader()
		if leader == "" {
			time.Sleep(1 * time.Second)
			continue
		}

		// verifica se pelo menos 2 nós estão respondendo (cluster mínimo funcional)
		activeNodes := b.countActiveNodes()
		if activeNodes >= 2 {
			// aguarda mais um pouco para garantir estabilidade
			time.Sleep(2 * time.Second)
			return true
		}

		time.Sleep(1 * time.Second)
	}

	return false
}

// findLeader encontra o líder do cluster
func (b *Benchmark) findLeader() string {
	for _, url := range b.raftURLs {
		resp, err := http.Get(url + "/status")
		if err != nil {
			continue
		}
		defer resp.Body.Close()

		var status struct {
			State string `json:"state"`
		}
		if err := json.NewDecoder(resp.Body).Decode(&status); err != nil {
			continue
		}

		if status.State == "StateLeader" {
			return url
		}
	}
	return ""
}

// countActiveNodes conta quantos nós estão respondendo
func (b *Benchmark) countActiveNodes() int {
	count := 0
	for _, url := range b.raftURLs {
		resp, err := http.Get(url + "/health")
		if err == nil {
			resp.Body.Close()
			if resp.StatusCode == http.StatusOK {
				count++
			}
		}
	}
	return count
}

func (b *Benchmark) saveCSV(resultados []Resultado) error {
	file, err := os.Create(b.outputCSV)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	writer.Write([]string{"nro_clientes", "vazao", "latencia_media"})
	for _, r := range resultados {
		writer.Write([]string{
			strconv.Itoa(r.nroClientes),
			fmt.Sprintf("%.2f", r.vazao),
			fmt.Sprintf("%.4f", r.latencia),
		})
	}

	return nil
}

func (b *Benchmark) generateGraph(resultados []Resultado) error {
	script := `
import matplotlib.pyplot as plt
import csv

xs = []
ys = []

with open('` + b.outputCSV + `', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        xs.append(float(row['vazao']))
        ys.append(float(row['latencia_media']))

plt.figure(figsize=(10, 6))
plt.scatter(xs, ys, s=100, alpha=0.6)
plt.plot(xs, ys, 'b-', alpha=0.3)
plt.xlabel('Vazão (ops/s)')
plt.ylabel('Latência média (s)')
plt.title('Desempenho Raft (etcd-io/raft): Vazão x Latência')
plt.grid(True, alpha=0.3)
plt.savefig('` + b.outputPNG + `', dpi=140, bbox_inches='tight')
plt.close()
`

	cmd := exec.Command("python", "-c", script)
	return cmd.Run()
}

func (b *Benchmark) calcularCDF(latencies []float64) ([]float64, []float64) {
	if len(latencies) == 0 {
		return []float64{}, []float64{}
	}

	sorted := make([]float64, len(latencies))
	copy(sorted, latencies)
	sort.Float64s(sorted)

	n := len(sorted)
	cumulative := make([]float64, n)
	for i := range sorted {
		cumulative[i] = float64(i+1) / float64(n)
	}

	return sorted, cumulative
}

func (b *Benchmark) generateCDFGraphs(resultados []Resultado) error {
	for _, r := range resultados {
		if len(r.latencies) == 0 {
			continue
		}

		sorted, cumulative := b.calcularCDF(r.latencies)
		sortedJSON, err := json.Marshal(sorted)
		if err != nil {
			log.Printf("erro ao serializar latencias ordenadas para %d clientes: %v", r.nroClientes, err)
			continue
		}
		cumulativeJSON, err := json.Marshal(cumulative)
		if err != nil {
			log.Printf("erro ao serializar cdf para %d clientes: %v", r.nroClientes, err)
			continue
		}

		if err := b.writeLatenciesJSON(r); err != nil {
			log.Printf("erro ao salvar latencias para %d clientes: %v", r.nroClientes, err)
		}

		script := fmt.Sprintf(`
import matplotlib.pyplot as plt

sorted_lat = %s
cumulative = %s

plt.figure(figsize=(10, 6))
plt.plot(sorted_lat, cumulative, 'b-', linewidth=2)
plt.xlabel('Latência (s)')
plt.ylabel('Probabilidade cumulativa')
plt.title('CDF de Latência - %d clientes (duração: %s)')
plt.grid(True, alpha=0.3)
plt.xlim(0, max(sorted_lat) * 1.1 if sorted_lat else 1)
plt.ylim(0, 1)
plt.savefig('%s/cdf_latencia_%d_clientes.png', dpi=140, bbox_inches='tight')
plt.close()
`, sortedJSON, cumulativeJSON, r.nroClientes, b.duracao, b.outputCDFDir, r.nroClientes)

		cmd := exec.Command("python", "-c", script)
		if err := cmd.Run(); err != nil {
			log.Printf("erro ao gerar cdf para %d clientes: %v", r.nroClientes, err)
		}
	}

	return nil
}

func (b *Benchmark) writeLatenciesJSON(r Resultado) error {
	if len(r.latencies) == 0 {
		return nil
	}

	payload := map[string]interface{}{
		"nro_clientes": r.nroClientes,
		"duracao_seg":  b.duracao.Seconds(),
		"latencias":    r.latencies,
	}

	filePath := fmt.Sprintf("%s/latencias_%d_clientes.json", b.outputCDFDir, r.nroClientes)
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	return encoder.Encode(payload)
}
