# Teste Rápido - Paxos e Raft

## PAXOS - Teste Rápido (2 minutos)

### 1. Teste de Backoff

```bash
cd T2_SD/Paxos/paxosmmc
python teste_backoff.py
```

**O que verificar:**
- ✅ Script executa sem backoff (pode mostrar livelock)
- ✅ Script executa com backoff (evita livelock)
- ✅ Comandos são enviados durante ambos os testes
- ✅ Prints mostram comportamento diferente entre sem e com backoff

**Duração:** ~30 segundos

---

### 2. Teste de Falha e Recuperação

```bash
cd T2_SD/Paxos/paxosmmc
python teste_falha_recuperacao.py
```

**O que verificar:**
- ✅ Réplica falha e reinicia
- ✅ Prints mostram: `[replica X] recuperou Y decisões do log`
- ✅ Réplica pode processar novos comandos após recuperação

**Duração:** ~30 segundos

---

## RAFT - Teste Rápido (5 minutos)

### 1. Teste Básico (3 réplicas)

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

**Aguardar 5 segundos**, depois verificar:

```bash
curl http://localhost:8000/status
curl http://localhost:8001/status
curl http://localhost:8002/status
```

**O que verificar:**
- ✅ Um nó deve ter `"state": "StateLeader"`
- ✅ Outros devem ter `"state": "StateFollower"`

**Enviar proposta:**
```bash
curl -X POST http://localhost:8000/propose -H "Content-Type: application/json" -d "{\"data\":\"teste\"}"
```

**O que verificar:**
- ✅ Resposta: `{"success": true, "index": 1}`

**Parar:** Pressione Ctrl+C em cada terminal

---

### 2. Teste de Benchmark Rápido

```bash
cd T2_SD/Raft
go run -tags benchmark benchmark_main.go --duracao 30 --cargas 1,2
```

**O que verificar:**
- ✅ Sistema reinicia cluster para cada carga
- ✅ CSV gerado: `resultados_desempenho.csv`
- ✅ Gráfico gerado: `grafico_vazao_latencia.png`

**Duração:** ~2 minutos

---

## Checklist de Verificação

### PAXOS
- [ ] `teste_backoff.py` executa sem erros
- [ ] Prints mostram comportamento sem backoff
- [ ] Prints mostram comportamento com backoff
- [ ] Comandos são enviados durante avaliação
- [ ] `teste_falha_recuperacao.py` executa sem erros
- [ ] Réplica recupera decisões do log

### RAFT
- [ ] 3 réplicas iniciam sem erros
- [ ] Um líder é eleito
- [ ] Propostas são aceitas
- [ ] Benchmark executa sem erros
- [ ] CSV é gerado
- [ ] Gráfico é gerado

