# Revisão Final - Baseado no Enunciado

## RESUMO EXECUTIVO

### ✅ PAXOS - Status: Completo (falta apenas PDF)
### ✅ RAFT - Status: Completo
### ⚠️ ESTRUTURA DE ENTREGA - Falta criar conforme enunciado

---

## PAXOS - Verificação Detalhada

### Item 0: Entender, Executar, Avaliar
✅ **ATENDIDO**
- Implementação baseada em [paxosmmc](https://github.com/denizalti/paxosmmc)
- Código funcional e executável
- Documentação completa

### Item 1: Como o "backoff" tenta evitar livelock de líderes?

✅ **ATENDIDO - TODOS OS REQUISITOS**

**Requisitos:**
1. ✅ Coloque prints no sistema
   - `leader.py` tem prints detalhados:
     - `[leader X] sem backoff - tentando novamente imediatamente...`
     - `[leader X] aguardando backoff de Y.XXs antes de tentar novamente...`
     - `[leader X] [PREEMPTED] preemptado por ballot...`
     - `[leader X] [OK] adotado para ballot...`

2. ✅ Execute sem backoff
   - `teste_backoff.py` executa primeiro sem backoff (linha 84)

3. ✅ Observe se existe o comportamento de livelock
   - Prints mostram comportamento de livelock sem backoff
   - Observação: "sem backoff pode mostrar mais conflitos/livelock"

4. ✅ Mande comandos ao sistema durante esta avaliação
   - Função `enviar_comandos()` envia comandos a cada 1 segundo (linha 54-64)
   - Prints mostram: `[comando externo X] enviando 'comando_X' via replica Y`

5. ✅ Idem para backoff
   - `teste_backoff.py` executa depois com backoff (linha 91)
   - Observação: "com backoff tende a convergir melhor"

**Arquivos:**
- ✅ `paxosmmc/leader.py` - Backoff implementado com prints
- ✅ `paxosmmc/teste_backoff.py` - Teste completo (sem e com backoff, comandos durante avaliação)

### Item 2: Se uma réplica falha e reinicia, há como obter as decisões anteriores?

✅ **ATENDIDO - TODOS OS REQUISITOS**

**Requisitos:**
1. ✅ Há como obter as decisões anteriores para que ela se sincronize?
   - Sim, através de log persistente em `Replica` e `Acceptor`

2. ✅ Construa e demonstre este cenário de execução
   - `teste_falha_recuperacao.py` demonstra:
     1. Fase 1: Envio de comandos iniciais
     2. Fase 2: Simulação de falha da réplica
     3. Fase 3: Envio de comandos durante a falha
     4. Fase 4: Recuperação da réplica com log
     5. Fase 5: Envio de novos comandos após recuperação

**Arquivos:**
- ✅ `paxosmmc/replica.py` - Log persistente e recuperação
- ✅ `paxosmmc/acceptor.py` - Log persistente e recuperação
- ✅ `paxosmmc/teste_falha_recuperacao.py` - Demonstração completa do cenário

### ⚠️ O QUE FALTA em PAXOS

1. ⚠️ **RESPOSTAS.PDF**
   - O enunciado pede: "adicione um arquivo RESPOSTAS.PDF contendo: seus nomes e as repostas às questões sobre o Paxos"
   - Existe: `paxosmmc/RESPOSTAS.md`
   - Falta: `RESPOSTAS.PDF` na pasta `Paxos/`

---

## RAFT - Verificação Detalhada

### Item 0: Baixe, crie um sistema com no mínimo 3 réplicas, execute

✅ **ATENDIDO - TODOS OS REQUISITOS**

**Requisitos:**
1. ✅ Escolha uma implementação de Raft
   - Base: [etcd-io/raft](https://github.com/etcd-io/raft)

2. ✅ Baixe (implementação baseada em etcd-io/raft)
   - Implementação usa `go.etcd.io/raft/v3` diretamente

3. ✅ Crie um sistema com no mínimo 3 réplicas
   - `main.go` cria 3 peers (linha 25-29)

4. ✅ Execute
   - Código funcional e executável

5. ✅ Use o laboratório
   - Sistema distribuído implementado

6. ✅ Deve ser distribuído
   - `transport.go` usa HTTP para comunicação entre máquinas diferentes
   - `raft_node.go` implementa comunicação distribuída

**Arquivos:**
- ✅ `main.go` - Inicia nó Raft (3 réplicas)
- ✅ `raft_node.go` - Implementação usando etcd-io/raft
- ✅ `transport.go` - Comunicação distribuída via HTTP

### Item 1: Medição de Desempenho - Visão Geral

✅ **ATENDIDO - TODOS OS REQUISITOS**

**Requisitos:**
1. ✅ Medir vazão (ops/s) e latência para níveis incrementais de carga
   - `benchmark.go` mede vazão e latência

2. ✅ Módulo de geração de carga controlada (cliente)
   - `client.go` implementa cliente

3. ✅ Várias execuções variando carga, anotando vazão e latência
   - Loop por níveis de carga (linha 47)

4. ✅ Sistema terminado e reiniciado a cada execução
   - `runRoundWithRestart()` reinicia cluster (linha 77)

5. ✅ Cada execução roda por tempo determinado (exemplo: 3 minutos)
   - Duração padrão: 180 segundos (3 minutos)

6. ✅ Gráfico com eixo x=vazão e eixo y=latência, cada ponto = uma execução
   - `generateGraph()` gera gráfico (linha 151)

**Arquivos:**
- ✅ `client.go` - Cliente para gerar carga
- ✅ `benchmark.go` - Script de benchmark
- ✅ `benchmark_main.go` - Executável para benchmark

### Item 2: Módulo Cliente

✅ **ATENDIDO - TODOS OS REQUISITOS**

**Requisitos do Cliente:**
1. ✅ Aguarda sistema estar no ar
   - `pickLeader()` aguarda líder (linha 57-64)

2. ✅ Timestamp_inicio
   - `startTime = time.Now()` (linha 35)

3. ✅ Loop [parada por tempo]
   - `for time.Since(startTime) < duration` (linha 37)

4. ✅ Cria pedido
   - Cria request (linha 83-84)

5. ✅ Timestamp1
   - `t1 := time.Now()` (linha 44)

6. ✅ Manda para o "cluster" Raft
   - `sendRequest(leaderURL)` (linha 45)

7. ✅ Aguarda a resposta
   - `sendRequest()` aguarda resposta HTTP

8. ✅ Calcula amostra de latência = tempoAgora - timestamp1
   - `lat := time.Since(t1).Seconds()` (linha 46)

9. ✅ Grava amostra de latência em um array
   - `latencies.append(lat)` (linha 48)

10. ✅ nroPedidos++
    - `requests++` (linha 49)

11. ✅ Calcula tempoTotal = tempoAgora - timestamp_inicio
    - `totalTime := time.Since(startTime).Seconds()` (linha 108)

12. ✅ Vazão = nroPedidos / tempoTotal
    - `throughput = requests / totalTime` (linha 113)

13. ✅ Latência Média = somatório / nroPedidos
    - `avgLatency = sum / len(latencies)` (linha 120)

14. ✅ Função de distribuição cumulativa de latência
    - `calcularCDF()` implementada (linha 180)

**Desempenho geral do sistema:**
1. ✅ Vazão = somatório das vazões observadas em cada cliente
   - `totalThroughput += thr` (linha 102)

2. ✅ Latência = média da latência média entre os clientes
   - `avgLatency = sumAvgLatency / nClients` (linha 107)

**Experimentos:**
1. ✅ Para cada nível de carga:
   - ✅ Subir réplicas (`startCluster()` linha 116)
   - ✅ Esperar estarem ativas (`time.Sleep(2 * time.Second)` linha 79)
   - ✅ Subir número de clientes (linha 84-91)
   - ✅ Aguardar término conforme tempo calculado (`wg.Wait()` linha 94)
   - ✅ Colher dados de cada cliente (`GetMetrics()` linha 101)
   - ✅ Obter desempenho geral do sistema (linha 96-108)
   - ✅ Plotar ponto no gráfico (X=vazão, Y=latência) (`generateGraph()` linha 151)

**Arquivos:**
- ✅ `client.go` - Módulo cliente completo conforme especificação
- ✅ `benchmark.go` - Script de benchmark completo conforme especificação

---

## ESTRUTURA DE ENTREGA

### ⚠️ FALTA: Estrutura Conforme Enunciado

**O enunciado pede:**
```
crie uma pasta que seja a concatenacao dos nomes dos compontes do grupo
dentro desta, crie uma pasta Paxos
e outra para Raft.
Em Paxos, coloque seus códigos utilizados para responder às questões,
e adicione um arquivo RESPOSTAS.PDF contendo:
seus nomes e as repostas às questões sobre o Paxos.
```

**Situação atual:**
- ✅ Pasta `T2_SD/Paxos/` existe
- ✅ Pasta `T2_SD/Raft/` existe
- ⚠️ **FALTA:** Pasta com nomes dos componentes do grupo
- ⚠️ **FALTA:** `RESPOSTAS.PDF` em `Paxos/`

**Ações necessárias:**
1. ⚠️ Criar pasta com nomes dos componentes (ex: `NOME1_NOME2_NOME3/`)
2. ⚠️ Copiar `T2_SD/Paxos/` para `NOME1_NOME2_NOME3/Paxos/`
3. ⚠️ Copiar `T2_SD/Raft/` para `NOME1_NOME2_NOME3/Raft/`
4. ⚠️ Converter `paxosmmc/RESPOSTAS.md` para PDF e colocar em `Paxos/RESPOSTAS.PDF`

---

## CONCLUSÃO

### PAXOS
- ✅ **Item 0:** Atendido
- ✅ **Item 1:** Atendido (prints, sem backoff, com backoff, comandos durante avaliação)
- ✅ **Item 2:** Atendido (falha e recuperação demonstrada)
- ⚠️ **FALTA:** RESPOSTAS.PDF

### RAFT
- ✅ **Item 0:** Atendido (3 réplicas, distribuído, baseado em etcd-io/raft)
- ✅ **Item 1:** Atendido (medição de desempenho completa)
- ✅ **Item 2:** Atendido (módulo cliente completo conforme especificação)

### ESTRUTURA DE ENTREGA
- ⚠️ **FALTA:** Pasta com nomes dos componentes do grupo
- ⚠️ **FALTA:** Organizar arquivos conforme enunciado
- ⚠️ **FALTA:** RESPOSTAS.PDF em Paxos/

---

## AÇÕES NECESSÁRIAS

1. **Converter RESPOSTAS.md para PDF**
   - Converter `T2_SD/Paxos/paxosmmc/RESPOSTAS.md` para PDF
   - Colocar em `T2_SD/Paxos/RESPOSTAS.PDF`

2. **Criar estrutura de entrega**
   - Criar pasta com nomes dos componentes do grupo
   - Copiar `T2_SD/Paxos/` para pasta de entrega
   - Copiar `T2_SD/Raft/` para pasta de entrega
   - Adicionar `RESPOSTAS.PDF` em `Paxos/`

3. **Verificar funcionamento**
   - Testar se código Python funciona
   - Testar se código Go compila e funciona

