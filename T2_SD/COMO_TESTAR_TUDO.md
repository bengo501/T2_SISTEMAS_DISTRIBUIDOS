# Como Testar Tudo - Paxos e Raft

## Guia Rápido de Testes

### PAXOS - Testes (5 minutos)

#### 1. Teste Rápido (30 segundos)

```bash
cd T2_SD/Paxos/paxosmmc
python teste_rapido.py
```

**O que verificar:**
- ✅ Imports bem-sucedidos
- ✅ Componentes criados
- ✅ Comandos enviados

#### 2. Teste de Backoff (30 segundos)

```bash
cd T2_SD/Paxos/paxosmmc
python teste_backoff.py
```

**O que verificar:**
- ✅ Execução sem backoff (pode mostrar livelock)
- ✅ Execução com backoff (evita livelock)
- ✅ Comandos enviados durante ambos os testes
- ✅ Prints mostram comportamento diferente

#### 3. Teste de Falha e Recuperação (30 segundos)

```bash
cd T2_SD/Paxos/paxosmmc
python teste_falha_recuperacao.py
```

**O que verificar:**
- ✅ Réplica falha e reinicia
- ✅ Prints mostram: `[replica X] recuperou Y decisões do log`
- ✅ Réplica processa novos comandos após recuperação

---

### RAFT - Testes (10 minutos)

#### 1. Teste Básico - Cluster (5 minutos)

**Passo 1: Iniciar 3 réplicas**

Abra 3 terminais diferentes:

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

**Passo 2: Aguardar 5 segundos** para eleição de líder

**Passo 3: Verificar status**

Em outro terminal:
```bash
curl http://localhost:8000/status
curl http://localhost:8001/status
curl http://localhost:8002/status
```

**O que verificar:**
- ✅ Um nó deve ter `"state": "StateLeader"`
- ✅ Outros devem ter `"state": "StateFollower"`

**Passo 4: Enviar proposta**

```bash
curl -X POST http://localhost:8000/propose -H "Content-Type: application/json" -d "{\"data\":\"teste\"}"
```

**O que verificar:**
- ✅ Resposta: `{"success": true, "index": 1}`

**Passo 5: Parar nós**
- Pressione Ctrl+C em cada terminal

---

#### 2. Teste Rápido - Verificação Automática (1 minuto)

**IMPORTANTE:** Inicie o cluster primeiro (3 terminais acima), depois:

```bash
cd T2_SD/Raft
go run -tags teste_rapido teste_rapido.go
```

**O que verificar:**
- ✅ Cluster encontrado
- ✅ Proposta enviada com sucesso
- ✅ Status de todos os nós

---

#### 3. Teste de Benchmark Rápido (2 minutos)

```bash
cd T2_SD/Raft
go run -tags benchmark benchmark_main.go --duracao 30 --cargas 1,2
```

**O que verificar:**
- ✅ Sistema reinicia cluster para cada carga
- ✅ CSV gerado: `resultados_desempenho.csv`
- ✅ Gráfico gerado: `grafico_vazao_latencia.png`

---

#### 4. Teste de Benchmark Completo (10-15 minutos)

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

## Checklist Completo

### PAXOS
- [ ] `teste_rapido.py` executa sem erros
- [ ] `teste_backoff.py` executa sem erros
  - [ ] Prints mostram comportamento sem backoff
  - [ ] Prints mostram comportamento com backoff
  - [ ] Comandos são enviados durante avaliação
- [ ] `teste_falha_recuperacao.py` executa sem erros
  - [ ] Réplica recupera decisões do log
  - [ ] Prints mostram recuperação

### RAFT
- [ ] 3 réplicas iniciam sem erros
- [ ] Um líder é eleito
- [ ] Propostas são aceitas
- [ ] `teste_rapido.go` executa sem erros
- [ ] Benchmark executa sem erros
- [ ] CSV é gerado
- [ ] Gráfico é gerado

---

## Solução de Problemas

### PAXOS

**Erro: "ModuleNotFoundError"**
```bash
cd T2_SD/Paxos/paxosmmc
python teste_rapido.py
```

**Erro: "ImportError"**
- Certifique-se de estar na pasta `paxosmmc/`

---

### RAFT

**Erro: "port already in use"**
```bash
# Windows PowerShell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Erro: "could not import go.etcd.io/raft/v3"**
```bash
cd T2_SD/Raft
go mod download
go mod tidy
```

**Erro ao compilar: "main redeclared"**
```bash
# Para nó Raft
go run main.go --id 1 --port 8000

# Para benchmark
go run -tags benchmark benchmark_main.go --duracao 180
```

**Clientes não encontram líder**
- Aguarde mais tempo para eleição (5-10 segundos)
- Verifique se há 3 réplicas rodando
- Verifique se há um líder: `curl http://localhost:8000/status`

---

## Resultados Esperados

### PAXOS

**Teste de Backoff:**
- Sem backoff: mais conflitos, possível livelock
- Com backoff: menos conflitos, convergência melhor

**Teste de Falha e Recuperação:**
- Réplica recupera decisões do log
- Prints mostram: `[replica X] recuperou Y decisões do log`

---

### RAFT

**Teste Básico:**
- 3 réplicas iniciam
- Um líder é eleito
- Propostas são aceitas

**Benchmark:**
- CSV gerado com resultados
- Gráfico vazão x latência gerado
- Gráficos CDF gerados
- Cada ponto no gráfico = uma execução

---

## Próximos Passos

Depois de testar tudo:

1. **PAXOS:** Converter `RESPOSTAS.md` para PDF
2. **RAFT:** Verificar resultados do benchmark
3. **Estrutura de Entrega:** Criar pasta com nomes dos componentes

---

## Documentação Completa

- `T2_SD/Paxos/COMO_TESTAR.md` - Guia completo de testes do Paxos
- `T2_SD/Raft/COMO_TESTAR.md` - Guia completo de testes do Raft
- `T2_SD/TESTE_RAPIDO.md` - Testes rápidos de ambos

