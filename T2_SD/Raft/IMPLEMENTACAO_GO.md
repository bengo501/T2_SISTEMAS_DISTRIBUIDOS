# Implementação Raft em Go usando etcd-io/raft

## Resumo

Foi criada uma implementação completa do estudo de caso Raft em **Go** usando o código original do repositório [etcd-io/raft](https://github.com/etcd-io/raft).

## Arquivos Criados

### Estrutura Principal

1. **`go.mod`** - Módulo Go com dependência do etcd-io/raft v3
2. **`main.go`** - Executável para iniciar um nó Raft individual
3. **`benchmark_main.go`** - Executável para rodar benchmark

### Implementação Core

4. **`raft_node.go`** - Implementação do nó Raft usando etcd-io/raft diretamente
   - Usa `raft.StartNode()` do etcd-io/raft
   - Processa `node.Ready()` do etcd-io/raft
   - Usa `node.Propose()` do etcd-io/raft
   - Implementa ciclo completo do etcd-io/raft

5. **`storage.go`** - Implementação da interface Storage do etcd-io/raft
   - Usa `raft.MemoryStorage` do etcd-io/raft
   - Implementa métodos necessários para o etcd-io/raft

6. **`transport.go`** - Transport para comunicação entre nós
   - Serializa/deserializa mensagens do etcd-io/raft
   - Comunicação HTTP entre nós

### Cliente e Benchmark

7. **`client.go`** - Cliente para gerar carga
   - Aguarda sistema estar no ar
   - Timestamp_inicio
   - Loop por tempo programado
   - Cria pedido, manda para cluster, aguarda resposta
   - Calcula amostra de latência
   - Grava em array
   - Calcula métricas: vazão, latência média

8. **`benchmark.go`** - Script de benchmark
   - Executa múltiplas rodadas com diferentes cargas
   - Reinicia cluster a cada rodada
   - Coleta dados de todos os clientes
   - Gera gráficos e CSV
   - Calcula CDF de latência

### Documentação

9. **`README_GO.md`** - Documentação completa da implementação
10. **`IMPLEMENTACAO_GO.md`** - Este arquivo

## Características da Implementação

### Usa código original do etcd-io/raft

- ✅ **`raft.StartNode()`**: Inicia nó Raft usando etcd-io/raft
- ✅ **`raft.MemoryStorage`**: Usa storage do etcd-io/raft
- ✅ **`raft.Node.Ready()`**: Processa atualizações do etcd-io/raft
- ✅ **`raft.Node.Propose()`**: Propõe comandos usando etcd-io/raft
- ✅ **`raft.Node.Tick()`**: Tick do etcd-io/raft
- ✅ **`raft.Node.Advance()`**: Advance do etcd-io/raft
- ✅ **`raftpb.Message`**: Mensagens do etcd-io/raft
- ✅ **`raftpb.Entry`**: Entradas do etcd-io/raft

### Sistema Distribuído

- ✅ 3 réplicas mínimas
- ✅ Comunicação via HTTP/RPC
- ✅ Execução distribuída em múltiplas máquinas

### Medição de Desempenho

- ✅ **Vazão**: Operações por segundo (ops/s)
- ✅ **Latência**: Latência média de resposta
- ✅ **CDF**: Função de distribuição cumulativa de latência

### Módulo Cliente (conforme especificação)

- ✅ Aguarda sistema estar no ar
- ✅ Timestamp_inicio
- ✅ Loop por tempo programado
- ✅ Cria pedido, manda para cluster, aguarda resposta
- ✅ Calcula amostra de latência = tempoAgora - timestamp1
- ✅ Grava amostra em array
- ✅ nroPedidos++
- ✅ Calcula tempoTotal = tempoAgora - timestamp_inicio
- ✅ Vazão = nroPedidos / tempoTotal
- ✅ Latência Média = somatório / nroPedidos
- ✅ Função de distribuição cumulativa de latência

### Experimentos (conforme especificação)

- ✅ Para cada nível de carga:
  - ✅ Subir réplicas
  - ✅ Esperar estarem ativas
  - ✅ Subir número de clientes
  - ✅ Aguardar término conforme tempo calculado
  - ✅ Colher dados de cada cliente
  - ✅ Obter desempenho geral do sistema
  - ✅ Plotar ponto no gráfico (X=vazão, Y=latência)

## Como Usar

### 1. Instalar dependências

```bash
cd T2_SD_V1/Raft
go mod download
```

### 2. Iniciar cluster Raft (3 réplicas)

Em 3 terminais diferentes:

**Terminal 1:**
```bash
go run main.go --id 1 --port 8000
```

**Terminal 2:**
```bash
go run main.go --id 2 --port 8001
```

**Terminal 3:**
```bash
go run main.go --id 3 --port 8002
```

### 3. Executar benchmark

```bash
go run benchmark_main.go --duracao 180 --cargas 1,2,3,4,6,8,10,12
```

### 4. Resultados

- `resultados_desempenho.csv` - Resultados em CSV
- `grafico_vazao_latencia.png` - Gráfico principal (vazão x latência)
- `cdf_latencia/` - Diretório com gráficos CDF de latência

## Dependências

- Go 1.21 ou superior
- `go.etcd.io/raft/v3 v3.6.0` - Biblioteca Raft original do etcd-io
- Python 3 (para gerar gráficos)
- matplotlib (para gráficos)

## Referências

- [etcd-io/raft](https://github.com/etcd-io/raft) - Biblioteca Raft em Go
- [Documentação etcd-io/raft](https://pkg.go.dev/go.etcd.io/raft/v3)

## Conclusão

A implementação usa o código original do etcd-io/raft diretamente, sem adaptações para outras linguagens. Todo o código está em Go, conforme solicitado.

