# Como Testar o Raft

## Pré-requisitos

- Go 1.21 ou superior
- Python 3 (para gerar gráficos)
- matplotlib (para gráficos): `pip install matplotlib`

## Instalação

```bash
cd T2_SD/Raft
go mod download
```

---

## Testes Disponíveis

### 1. Teste Básico - Iniciar Cluster (3 Réplicas)

**Teste 1: Iniciar um nó Raft**

Abra 3 terminais diferentes e execute:

**Terminal 1:**

```bash
cd T2_SD/Raft
go run main.go --id 1 --port 8000
```

**Terminal 2:**

```bash
cd T2_SD/Raft
go run main.go --id 2 --port 8001
```

**Terminal 3:**

```bash
cd T2_SD/Raft
go run main.go --id 3 --port 8002
```

**O que esperar:**

- Cada terminal mostra: `nó raft X iniciado na porta Y`
- Sistema elege um líder automaticamente
- Pressione Ctrl+C em cada terminal para parar

**Verificação:**

- Verificar se há um líder: `curl http://localhost:8000/status`
- Deve retornar JSON com `"state": "StateLeader"` para um dos nós

---

### 2. Teste de Proposta (Enviar Comando)

Com o cluster rodando (3 terminais), em outro terminal:

```bash
curl -X POST http://localhost:8000/propose -H "Content-Type: application/json" -d "{\"data\":\"teste_comando_1\"}"
```

**O que esperar:**

- Resposta JSON: `{"success": true, "index": 1}`
- Comando é proposto e commitado

**Testar em diferentes nós:**

```bash
# Enviar para nó 1
curl -X POST http://localhost:8000/propose -H "Content-Type: application/json" -d "{\"data\":\"cmd1\"}"

# Enviar para nó 2
curl -X POST http://localhost:8001/propose -H "Content-Type: application/json" -d "{\"data\":\"cmd2\"}"

# Enviar para nó 3
curl -X POST http://localhost:8002/propose -H "Content-Type: application/json" -d "{\"data\":\"cmd3\"}"
```

---

### 3. Teste de Benchmark Completo (Item 1 e 2 do enunciado)

**IMPORTANTE:** Antes de executar o benchmark, certifique-se de que não há processos Raft rodando:

```bash
# Windows PowerShell
Get-Process | Where-Object {$_.ProcessName -like "*go*"} | Stop-Process -Force
```

**Executar benchmark:**

```bash
cd T2_SD/Raft
go run -tags benchmark benchmark_main.go --duracao 60 --cargas 1,2,3
```

**Parâmetros:**

- `--duracao`: Duração de cada execução em segundos (padrão: 180 = 3 minutos)
- `--cargas`: Lista de números de clientes (padrão: 1,2,3,4,6,8,10,12)

**O que esperar:**

**Para cada nível de carga:**

1. Sistema reinicia o cluster (3 réplicas)
2. Aguarda réplicas estarem ativas
3. Inicia N clientes
4. Clientes enviam requisições por tempo determinado
5. Coleta dados de todos os clientes
6. Calcula métricas:
   - Vazão (ops/s)
   - Latência média
   - CDF de latência

**Resultados gerados:**

- `resultados_desempenho.csv` - Resultados em CSV
- `grafico_vazao_latencia.png` - Gráfico principal (vazão x latência)
- `cdf_latencia/` - Gráficos CDF de latência para cada rodada

**Duração:** ~5-10 minutos (dependendo do número de cargas e duração)

---

## Verificação de Funcionamento

### 1. Verificar se o cluster está funcionando

**Verificar status de cada nó:**

```bash
curl http://localhost:8000/status
curl http://localhost:8001/status
curl http://localhost:8002/status
```

**Resposta esperada:**

```json
{
  "id": 1,
  "term": 1,
  "leader": 1,
  "state": "StateLeader"
}
```

### 2. Verificar se há líder

Apenas um nó deve ter `"state": "StateLeader"`, os outros devem ter `"StateFollower"`.

### 3. Verificar comunicação entre nós

**Enviar proposta para líder:**

```bash
curl -X POST http://localhost:8000/propose -H "Content-Type: application/json" -d "{\"data\":\"teste\"}"
```

**Resposta esperada:**

```json
{
  "success": true,
  "index": 1
}
```

### 4. Verificar resultados do benchmark

**Verificar CSV:**

```bash
cat resultados_desempenho.csv
```

**Deve conter:**

```csv
nro_clientes,vazao,latencia_media
1,10.5,0.095
2,20.3,0.098
3,30.1,0.101
```

**Verificar gráfico:**

```bash
# Abrir grafico_vazao_latencia.png
```

**Verificar CDF:**

```bash
# Verificar arquivos em cdf_latencia/
ls cdf_latencia/
```

---

## Teste Completo Passo a Passo

### Teste 1: Cluster Básico (5 minutos)

1. **Iniciar 3 réplicas:**

   ```bash
   # Terminal 1
   cd T2_SD/Raft
   go run main.go --id 1 --port 8000

   # Terminal 2
   cd T2_SD/Raft
   go run main.go --id 2 --port 8001

   # Terminal 3
   cd T2_SD/Raft
   go run main.go --id 3 --port 8002
   ```
2. **Aguardar 5 segundos** para eleição de líder
3. **Verificar status:**

   ```bash
   curl http://localhost:8000/status
   curl http://localhost:8001/status
   curl http://localhost:8002/status
   ```
4. **Enviar proposta:**

   ```bash
   curl -X POST http://localhost:8000/propose -H "Content-Type: application/json" -d "{\"data\":\"teste1\"}"
   ```
5. **Parar nós:** Pressione Ctrl+C em cada terminal

---

### Teste 2: Benchmark Rápido (2 minutos)

```bash
cd T2_SD/Raft
go run -tags benchmark benchmark_main.go --duracao 30 --cargas 1,2
```

**O que verificar:**

- ✅ Sistema reinicia cluster para cada carga
- ✅ Clientes enviam requisições
- ✅ CSV é gerado
- ✅ Gráfico é gerado

---

### Teste 3: Benchmark Completo (10-15 minutos)

```bash
cd T2_SD/Raft
go run -tags benchmark benchmark_main.go --duracao 180 --cargas 1,2,3,4,6,8
```

**O que verificar:**

- ✅ Para cada carga: reinicia cluster, inicia clientes, coleta dados
- ✅ CSV com resultados
- ✅ Gráfico vazão x latência
- ✅ Gráficos CDF para cada rodada

---

## Solução de Problemas

### Erro: "port already in use"

**Solução:**

```bash
# Windows PowerShell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Erro: "could not import go.etcd.io/raft/v3"

**Solução:**

```bash
cd T2_SD/Raft
go mod download
go mod tidy
```

### Erro ao compilar: "main redeclared"

**Solução:**

```bash
# Para nó Raft
go run main.go --id 1 --port 8000

# Para benchmark
go run -tags benchmark benchmark_main.go --duracao 180
```

### Clientes não encontram líder

**Solução:**

1. Aguarde mais tempo para eleição (5-10 segundos)
2. Verifique se há 3 réplicas rodando
3. Verifique se há um líder: `curl http://localhost:8000/status`

### Erro ao gerar gráfico: "matplotlib not found"

**Solução:**

```bash
pip install matplotlib
```

---

## Verificação de Requisitos do Enunciado

### Item 0: Sistema com 3 réplicas, distribuído

- ✅ Teste 1: Iniciar 3 réplicas
- ✅ Verificar comunicação entre nós
- ✅ Sistema distribuído (HTTP)

### Item 1: Medição de Desempenho

- ✅ Teste 3: Benchmark completo
- ✅ Gera CSV com resultados
- ✅ Gera gráfico vazão x latência
- ✅ Gera gráficos CDF

### Item 2: Módulo Cliente

- ✅ Teste 3: Benchmark usa módulo cliente
- ✅ Cliente aguarda sistema estar no ar
- ✅ Cliente mede latência
- ✅ Cliente calcula métricas

---

## Exemplo de Saída Esperada

### Cluster Iniciado:

```
nó raft 1 iniciado na porta 8000
aguardando sinal para parar...
```

### Status:

```json
{
  "id": 1,
  "term": 1,
  "leader": 1,
  "state": "StateLeader"
}
```

### Benchmark:

```
[rodada] reiniciando cluster | 1 clientes por 180s
 -> vazão=10.50 ops/s | latência média=0.0950s | amostras=1890
[rodada] reiniciando cluster | 2 clientes por 180s
 -> vazão=20.30 ops/s | latência média=0.0980s | amostras=3654
...
gráfico principal salvo em: grafico_vazao_latencia.png
```

---

## Resultados Esperados

### Teste Básico:

- ✅ 3 réplicas iniciam
- ✅ Um líder é eleito
- ✅ Propostas são aceitas

### Benchmark:

- ✅ CSV gerado com resultados
- ✅ Gráfico vazão x latência gerado
- ✅ Gráficos CDF gerados
- ✅ Cada ponto no gráfico = uma execução
