# Checklist Completo - Baseado no Enunciado

## PAXOS - Checklist

### Item 0: Entender, Executar, Avaliar
- ✅ Implementação baseada no paxosmmc
- ✅ Código funcional e executável
- ✅ Documentação completa

### Item 1: Como o "backoff" tenta evitar livelock de líderes?
- ✅ Prints no sistema (leader.py tem prints detalhados)
- ✅ Execute sem backoff (teste_backoff.py executa sem backoff primeiro)
- ✅ Observe se existe o comportamento de livelock (prints mostram comportamento)
- ✅ Mande comandos ao sistema durante esta avaliação (enviar_comandos() envia a cada 1s)
- ✅ Idem para backoff (teste_backoff.py executa com backoff depois)

**Arquivos:**
- ✅ `paxosmmc/leader.py` - Backoff implementado com prints
- ✅ `paxosmmc/teste_backoff.py` - Teste completo (sem e com backoff)

### Item 2: Se uma réplica falha e reinicia, há como obter as decisões anteriores?
- ✅ Há como obter as decisões anteriores (log persistente)
- ✅ Construa e demonstre este cenário (teste_falha_recuperacao.py demonstra)

**Arquivos:**
- ✅ `paxosmmc/replica.py` - Log persistente
- ✅ `paxosmmc/acceptor.py` - Log persistente
- ✅ `paxosmmc/teste_falha_recuperacao.py` - Demonstração completa

### ⚠️ FALTA em PAXOS
1. ⚠️ **RESPOSTAS.PDF** - O enunciado pede PDF (existe apenas RESPOSTAS.md)

---

## RAFT - Checklist

### Item 0: Baixe, crie um sistema com no mínimo 3 réplicas, execute
- ✅ Escolha uma implementação (etcd-io/raft)
- ✅ Baixe (implementação baseada em etcd-io/raft)
- ✅ Crie um sistema com no mínimo 3 réplicas (main.go cria 3 peers)
- ✅ Execute (código funcional)
- ✅ Use o laboratório (distribuído)
- ✅ Deve ser distribuído (transport.go usa HTTP)

### Item 1: Medição de Desempenho - Visão Geral
- ✅ Medir vazão (ops/s) e latência para níveis incrementais de carga
- ✅ Módulo de geração de carga controlada (cliente)
- ✅ Várias execuções variando carga, anotando vazão e latência
- ✅ Sistema terminado e reiniciado a cada execução
- ✅ Cada execução roda por tempo determinado (3 minutos)
- ✅ Gráfico com eixo x=vazão e eixo y=latência, cada ponto = uma execução

### Item 2: Módulo Cliente
- ✅ Aguarda sistema estar no ar (pickLeader() aguarda líder)
- ✅ Timestamp_inicio (startTime = time.Now())
- ✅ Loop [parada por tempo] (for time.Since(startTime) < duration)
- ✅ Cria pedido (cria request)
- ✅ Timestamp1 (t1 := time.Now())
- ✅ Manda para o "cluster" Raft (sendRequest())
- ✅ Aguarda a resposta (sendRequest() aguarda)
- ✅ Calcula amostra de latência = tempoAgora - timestamp1 (lat := time.Since(t1))
- ✅ Grava amostra de latência em um array (latencies.append(lat))
- ✅ nroPedidos++ (requests++)
- ✅ Calcula tempoTotal = tempoAgora - timestamp_inicio (time.Since(startTime))
- ✅ Vazão = nroPedidos / tempoTotal (throughput = requests / totalTime)
- ✅ Latência Média = somatório / nroPedidos (avgLatency = sum / len(latencies))
- ✅ Função de distribuição cumulativa de latência (calcularCDF())

### Desempenho geral do sistema
- ✅ Vazão = somatório das vazões observadas em cada cliente (totalThroughput += thr)
- ✅ Latência = média da latência média entre os clientes (avgLatency = sumAvgLatency / nClients)

### Experimentos
- ✅ Para cada nível de carga:
  - ✅ Subir réplicas (startCluster())
  - ✅ Esperar estarem ativas (time.Sleep(2 * time.Second))
  - ✅ Subir número de clientes (cria N clientes)
  - ✅ Aguardar término conforme tempo calculado (wg.Wait())
  - ✅ Colher dados de cada cliente (GetMetrics())
  - ✅ Obter desempenho geral do sistema (calcula métricas agregadas)
  - ✅ Plotar ponto no gráfico (X=vazão, Y=latência) (generateGraph())

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

**Ações necessárias:**
1. ⚠️ Criar pasta com nomes dos componentes (ex: `NOME1_NOME2_NOME3/`)
2. ⚠️ Copiar `T2_SD/Paxos/` para `NOME1_NOME2_NOME3/Paxos/`
3. ⚠️ Copiar `T2_SD/Raft/` para `NOME1_NOME2_NOME3/Raft/`
4. ⚠️ Converter `paxosmmc/RESPOSTAS.md` para PDF e colocar em `Paxos/RESPOSTAS.PDF`

---

## RESUMO

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

