package main

import (
	"flag"
	"fmt"
	"log"
	"strconv"
	"strings"
	"time"
)

func main() {
	var duracao = flag.Int("duracao", 180, "duração de cada execução em segundos (padrão: 180 = 3min)")
	var cargasStr = flag.String("cargas", "1,2,3,4,6,8,10,12", "lista de números de clientes separados por vírgula")
	flag.Parse()

	cargas := make([]int, 0)
	for _, s := range strings.Split(*cargasStr, ",") {
		n, err := strconv.Atoi(strings.TrimSpace(s))
		if err != nil {
			log.Fatalf("erro ao parsear carga: %v", err)
		}
		cargas = append(cargas, n)
	}

	raftURLs := []string{
		"http://localhost:8000",
		"http://localhost:8001",
		"http://localhost:8002",
	}

	benchmark := NewBenchmark(
		raftURLs,
		time.Duration(*duracao)*time.Second,
		cargas,
	)

	fmt.Printf("iniciando benchmark com duração de %d segundos por rodada\n", *duracao)
	fmt.Printf("cargas: %v\n", cargas)

	if err := benchmark.Run(); err != nil {
		log.Fatalf("erro ao executar benchmark: %v", err)
	}

	fmt.Printf("benchmark concluído!\n")
	fmt.Printf("resultados salvos em: resultados_desempenho.csv\n")
	fmt.Printf("gráfico principal salvo em: grafico_vazao_latencia.png\n")
	fmt.Printf("gráficos cdf salvos em: cdf_latencia/\n")
}
