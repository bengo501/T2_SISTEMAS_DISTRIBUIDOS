# Implementação Raft em Go usando etcd-io/raft

Esta implementação usa o código original do repositório [etcd-io/raft](https://github.com/etcd-io/raft) para criar um sistema Raft distribuído com medição de desempenho.

## Estrutura do Projeto

- `main.go` - Inicia um nó Raft individual
- `raft_node.go` - Implementação do nó Raft usando etcd-io/raft
- `storage.go` - Implementação da interface Storage do etcd-io/raft
- `transport.go` - Transport para comunicação entre nós
- `client.go` - Cliente para gerar carga
- `benchmark.go` - Script de benchmark para medição de desempenho
- `run_benchmark.go` - Executável para rodar benchmark
- `go.mod` - Dependências do projeto

## Pré-requisitos

- Go 1.21 ou superior
- Python 3 (para gerar gráficos)
- matplotlib (para gráficos)

## Instalação

```bash
cd T2_SD_V1/Raft
go mod download
```

## Uso

### 1. Iniciar cluster Raft (3 réplicas)

Em 3 terminais diferentes:

**Terminal 1:**
```bash
go run . --id 1 --port 8000
```

**Terminal 2:**
```bash
go run . --id 2 --port 8001
```

**Terminal 3:**
```bash
go run . --id 3 --port 8002
```

### 2. Executar benchmark

```bash
go run run_benchmark.go --duracao 180 --cargas 1,2,3,4,6,8,10,12
```

Parâmetros:
- `--duracao`: Duração de cada execução em segundos (padrão: 180 = 3 minutos)
- `--cargas`: Lista de números de clientes separados por vírgula (padrão: 1,2,3,4,6,8,10,12)

### 3. Resultados

O benchmark gera:
- `resultados_desempenho.csv` - Resultados em CSV
- `grafico_vazao_latencia.png` - Gráfico principal (vazão x latência)
- `cdf_latencia/` - Diretório com gráficos CDF de latência para cada rodada

## Características

### Usa código original do etcd-io/raft

- **raft.StartNode()**: Inicia nó Raft usando etcd-io/raft
- **raft.MemoryStorage**: Usa storage do etcd-io/raft
- **raft.Node.Ready()**: Processa atualizações do etcd-io/raft
- **raft.Node.Propose()**: Propõe comandos usando etcd-io/raft

### Sistema Distribuído

- 3 réplicas mínimas
- Comunicação via HTTP/RPC
- Execução distribuída em múltiplas máquinas

### Medição de Desempenho

- **Vazão**: Operações por segundo (ops/s)
- **Latência**: Latência média de resposta
- **CDF**: Função de distribuição cumulativa de latência

### Módulo Cliente

- Aguarda sistema estar no ar
- Timestamp_inicio
- Loop por tempo programado
- Cria pedido, manda para cluster, aguarda resposta
- Calcula amostra de latência
- Grava em array
- Calcula métricas: vazão, latência média, CDF

### Experimentos

- Para cada nível de carga:
  - Subir réplicas
  - Esperar estarem ativas
  - Subir número de clientes
  - Aguardar término
  - Colher dados
  - Obter desempenho geral
  - Plotar ponto no gráfico (X=vazão, Y=latência)

## Arquitetura

### Nó Raft

- Usa `go.etcd.io/raft/v3` diretamente
- Implementa interface Storage do etcd-io/raft
- Processa Ready() do etcd-io/raft
- Envia mensagens via Transport
- Expõe API HTTP para propostas

### Transport

- Comunicação HTTP entre nós
- Serializa/deserializa mensagens do etcd-io/raft
- Envia mensagens para peers

### Cliente

- Gera carga incremental
- Mede latência por requisição
- Calcula métricas agregadas

### Benchmark

- Executa múltiplas rodadas com diferentes cargas
- Reinicia cluster a cada rodada
- Coleta dados de todos os clientes
- Gera gráficos e CSV

## Referências

- [etcd-io/raft](https://github.com/etcd-io/raft) - Biblioteca Raft em Go
- [Documentação etcd-io/raft](https://pkg.go.dev/go.etcd.io/raft/v3)

