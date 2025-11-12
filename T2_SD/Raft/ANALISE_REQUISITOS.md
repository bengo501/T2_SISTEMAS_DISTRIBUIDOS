# análise de requisitos - implementação raft

## resumo executivo

esta análise verifica se a implementação atual atende todos os requisitos do enunciado do trabalho de sistemas distribuídos (t2).

---

## requisitos do enunciado

### item 0: sistema básico
- [x] **mínimo 3 réplicas**: implementado ✅
- [x] **sistema distribuído**: implementado ✅ (comunicação via http entre nós)
- [x] **execução**: implementado ✅

### item 1: medição de desempenho

#### 1.1 requisitos gerais
- [x] **medir vazão (ops/s)**: implementado ✅
- [x] **medir latência de resposta**: implementado ✅
- [x] **níveis incrementais de carga**: implementado ✅
- [x] **módulo de geração de carga controlada**: implementado ✅
- [x] **múltiplas execuções variando carga**: implementado ✅
- [x] **sistema terminado e reiniciado a cada execução**: implementado ✅
- [x] **execução por tempo determinado (ex: 3 minutos)**: implementado ✅
- [x] **gráfico x=vazão, y=latência com vários pontos**: implementado ✅

### item 2: módulo cliente

#### 2.1 fluxo do cliente (conforme enunciado)
- [x] **aguarda sistema estar no ar**: parcialmente implementado ⚠️
  - problema: cliente tenta encontrar líder mas não espera explicitamente cluster estar pronto
  - impacto: o `timestamp_inicio` pode ser contado antes do cluster estar totalmente operacional
- [x] **timestamp_inicio**: implementado ✅ (`startTime`)
- [x] **loop por tempo programado**: implementado ✅
- [x] **cria pedido**: implementado ✅
- [x] **timestamp1 antes de enviar**: implementado ✅ (`t1 := time.Now()`)
- [x] **manda para cluster raft**: implementado ✅
- [x] **aguarda resposta**: implementado ✅
- [x] **calcula amostra de latência = tempoagora - timestamp1**: implementado ✅
- [x] **grava amostra em array**: implementado ✅ (`latencies` array)
- [x] **nropedidos++**: implementado ✅ (`requests++`)
- [x] **calcula tempoTotal**: implementado ✅
- [x] **vazão = nropedidos / tempoTotal**: implementado ✅
- [x] **latência média = somatório / nropedidos**: implementado ✅
- [x] **função de distribuição cumulativa de latência**: implementado ✅ (cdf)

#### 2.2 desempenho geral do sistema
- [x] **vazão = somatório das vazões de cada cliente**: implementado ✅
- [x] **latência = média da latência média entre clientes**: implementado ✅

### item 3: experimentos

- [x] **para cada nível de carga**: implementado ✅
- [x] **subir réplicas**: implementado ✅
- [x] **esperar estarem ativas**: parcialmente implementado ⚠️
  - problema: espera apenas 2 segundos fixos, não verifica se cluster está realmente pronto
- [x] **subir número de clientes**: implementado ✅
- [x] **aguardar término conforme tempo calculado**: implementado ✅
- [x] **colher dados de cada cliente**: implementado ✅
- [x] **obter desempenho geral do sistema**: implementado ✅
- [x] **plotar ponto no gráfico (x=vazão, y=latência)**: implementado ✅

---

## métricas e resultados esperados

### métricas por cliente
1. **vazão individual** (ops/s): `nroPedidos / tempoTotal` ✅
2. **latência média individual** (s): `somatório latências / nroPedidos` ✅
3. **array de amostras de latência**: ✅
4. **função de distribuição cumulativa (cdf)**: ✅

### métricas do sistema (agregadas)
1. **vazão total do sistema** (ops/s): `somatório vazões de todos clientes` ✅
2. **latência média do sistema** (s): `média das latências médias dos clientes` ✅
3. **cdf agregada**: ✅

### resultados gerados
1. **csv com resultados**: `resultados_desempenho.csv` ✅
   - colunas: `nro_clientes`, `vazao`, `latencia_media`
2. **gráfico vazão x latência**: `grafico_vazao_latencia.png` ✅
   - eixo x: vazão (ops/s)
   - eixo y: latência média (s)
   - vários pontos (um por execução)
3. **gráficos cdf**: `cdf_latencia/cdf_latencia_*_clientes.png` ✅
4. **arquivos json com latências**: `cdf_latencia/latencias_*_clientes.json` ✅

---

## problemas identificados

### problema 1: cliente não espera cluster estar pronto ⚠️

**localização**: `client.go:34-42`

**problema atual**:
```go
func (c *Client) Run() {
    c.startTime = time.Now()  // inicia imediatamente
    
    for time.Since(c.startTime) < c.duration {
        leaderURL := c.pickLeader()
        if leaderURL == "" {
            time.Sleep(100 * time.Millisecond)
            continue  // continua tentando mas já está contando o tempo
        }
        // ...
    }
}
```

**impacto**: 
- o `timestamp_inicio` é contado mesmo quando o cluster ainda não está pronto
- isso pode reduzir a vazão medida (tempo total maior sem requisições efetivas)
- não atende completamente ao requisito "aguarda sistema estar no ar"

**solução recomendada**: 
- adicionar fase de espera inicial antes de `startTime`
- aguardar cluster estar pronto (líder eleito + cluster estável)
- só então iniciar `startTime` e começar a medir

### problema 2: benchmark não verifica se cluster está pronto ⚠️

**localização**: `benchmark.go:81-83`

**problema atual**:
```go
func (b *Benchmark) runRoundWithRestart(nClients int) {
    b.startCluster()
    time.Sleep(2 * time.Second)  // espera fixa, não verifica
    
    // inicia clientes imediatamente
    clients := make([]*Client, nClients)
    // ...
}
```

**impacto**:
- espera fixa de 2 segundos pode não ser suficiente
- cluster pode não estar totalmente estável quando clientes iniciam
- pode afetar resultados da primeira execução

**solução recomendada**:
- adicionar verificação explícita de que cluster está pronto
- verificar se há líder eleito
- verificar se pelo menos 2 dos 3 nós estão respondendo
- aguardar cluster estar estável antes de iniciar clientes

### problema 3: resultados zerados no csv ⚠️

**evidência**: `resultados_desempenho.csv` mostra vazão e latência = 0.00

**possíveis causas**:
1. benchmark foi interrompido antes de completar
2. clientes não conseguiram encontrar líder
3. requisições falharam silenciosamente
4. cluster não estava pronto quando clientes iniciaram

**solução recomendada**:
- implementar espera explícita por cluster pronto
- adicionar logs detalhados de requisições
- verificar se requisições estão sendo bem-sucedidas
- adicionar timeout maior para eleição de líder

---

## correções necessárias

### correção 1: adicionar espera explícita por cluster pronto no cliente

**arquivo**: `client.go`

**mudança necessária**:
```go
func (c *Client) Run() {
    // fase 1: aguardar cluster estar pronto
    c.waitForClusterReady()
    
    // fase 2: iniciar medição
    c.startTime = time.Now()
    
    // fase 3: loop de requisições
    for time.Since(c.startTime) < c.duration {
        // ...
    }
}

func (c *Client) waitForClusterReady() {
    maxWait := 30 * time.Second
    deadline := time.Now().Add(maxWait)
    
    for time.Now().Before(deadline) {
        leaderURL := c.pickLeader()
        if leaderURL != "" {
            // verifica se líder está realmente operacional
            if c.testLeader(leaderURL) {
                return
            }
        }
        time.Sleep(500 * time.Millisecond)
    }
    
    // se não encontrou, continua mesmo assim (com warning)
}

func (c *Client) testLeader(url string) bool {
    // tenta uma requisição de teste
    // verifica se responde corretamente
}
```

### correção 2: adicionar verificação de cluster pronto no benchmark

**arquivo**: `benchmark.go`

**mudança necessária**:
```go
func (b *Benchmark) runRoundWithRestart(nClients int) {
    b.startCluster()
    
    // aguarda cluster estar pronto (com timeout)
    if !b.waitForClusterReady(30 * time.Second) {
        log.Printf("aviso: cluster pode não estar totalmente pronto")
    }
    
    // agora inicia clientes
    clients := make([]*Client, nClients)
    // ...
}

func (b *Benchmark) waitForClusterReady(timeout time.Duration) bool {
    deadline := time.Now().Add(timeout)
    
    for time.Now().Before(deadline) {
        // verifica se há líder
        leader := b.findLeader()
        if leader == "" {
            time.Sleep(1 * time.Second)
            continue
        }
        
        // verifica se pelo menos 2 nós estão respondendo
        activeNodes := b.countActiveNodes()
        if activeNodes >= 2 {
            // aguarda mais um pouco para estabilizar
            time.Sleep(2 * time.Second)
            return true
        }
        
        time.Sleep(1 * time.Second)
    }
    
    return false
}
```

---

## conclusão

### atendimento aos requisitos

- **requisitos básicos**: 100% ✅
- **módulo cliente**: 95% ⚠️ (falta espera explícita por cluster)
- **experimentos**: 90% ⚠️ (falta verificação de cluster pronto)
- **métricas e resultados**: 100% ✅

### status geral

a implementação atende a **maioria dos requisitos** do enunciado, mas há **2 problemas importantes**:

1. **cliente não espera explicitamente cluster estar pronto** antes de iniciar medição
2. **benchmark não verifica se cluster está realmente operacional** antes de iniciar clientes

esses problemas podem explicar os **resultados zerados** no csv, indicando que os clientes podem estar iniciando antes do cluster estar totalmente operacional.

### recomendação

implementar as correções sugeridas antes de executar benchmarks completos para garantir resultados válidos e reprodutíveis.

---

## próximos passos

1. [ ] implementar `waitForClusterReady()` no cliente
2. [ ] implementar `waitForClusterReady()` no benchmark
3. [ ] adicionar logs detalhados de requisições
4. [ ] executar benchmark completo e verificar resultados
5. [ ] validar que gráficos estão sendo gerados corretamente
6. [ ] validar que cdf está sendo calculada corretamente

