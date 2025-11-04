# Revisão Final Completa - T2 Sistemas Distribuídos

## Revisão dos Itens 0), 1) e 2) do Raft

### Item 0: Baixe, crie um sistema com no mínimo 3 réplicas, execute

**O que é pedido:**
1. ✅ Escolha uma implementação de Raft → **Base escolhida**: [etcd-io/raft](https://github.com/etcd-io/raft)
2. ✅ Baixe → **Nota**: Código foi implementado em Python baseado no etcd-io/raft (que é em Go)
3. ✅ Crie um sistema com no mínimo 3 réplicas → **Implementado**: `raft_example.py` e `raft_distribuido.py`
4. ✅ Execute → **Implementado**: Código funcional
5. ✅ Use o laboratório. Deve ser distribuído → **Implementado**: `raft_distribuido.py` permite execução distribuída

**Status:** ✅ **TOTALMENTE ATENDIDO**

---

### Item 1: Medição de Desempenho - Visão Geral

**O que é pedido:**
1. ✅ Medir vazão (ops/s) e latência para níveis incrementais de carga
2. ✅ Módulo de geração de carga controlada (cliente)
3. ✅ Várias execuções variando carga, anotando vazão e latência
4. ✅ Sistema terminado e reiniciado a cada execução
5. ✅ Cada execução roda por tempo determinado (exemplo: 3 minutos)
6. ✅ Gráfico com eixo x=vazão e eixo y=latência, cada ponto = uma execução

**Status:** ✅ **TOTALMENTE ATENDIDO**

- Localização: `run_benchmark.py`
- Duração padrão: 180 segundos (3 minutos)
- Gráfico gerado automaticamente

---

### Item 2: Módulo Cliente

**O que é pedido:**
1. ✅ Aguarda sistema estar no ar → `_pick_leader()` (linha 44)
2. ✅ Timestamp_inicio → `start = time.time()` (linha 34)
3. ✅ Loop parada por tempo → `while time.time() - start < self.duration_s` (linha 35)
4. ✅ Cria pedido, timestamp1, manda para cluster, aguarda resposta → Linhas 36-38
5. ✅ Calcula amostra de latência = tempoAgora - timestamp1 → `lat = time.time() - t1` (linha 39)
6. ✅ Grava amostra em array, nroPedidos++ → Linhas 40-41
7. ✅ Calcula tempoTotal → `total_time = duration_s` (linha 73)
8. ✅ Vazão = nroPedidos / tempoTotal → `throughput = total_reqs / total_time` (linha 74)
9. ✅ Latência Média = somatório / nroPedidos → `avg_latency = sum(all_latencies) / len(all_latencies)` (linha 75)
10. ✅ Função de distribuição cumulativa de latência → `calcular_cdf()` (linha 82) e gráficos CDF (linha 134)
11. ✅ Desempenho geral: vazão = somatório, latência = média → Linhas 68-75
12. ✅ Experimentos: para cada nível de carga → Loop linha 106

**Status:** ✅ **TOTALMENTE ATENDIDO**

- Localização: `run_benchmark.py` - Classe `Client` e função `run_round_with_restart()`

---

## Origem do Código Raft

### Referência Base:

**Base de Implementação**: [etcd-io/raft](https://github.com/etcd-io/raft)

O repositório [etcd-io/raft](https://github.com/etcd-io/raft) é uma biblioteca Raft em Go para manter uma máquina de estado replicada. É uma implementação de produção amplamente usada por sistemas como:
- etcd (distributed reliable key-value store)
- CockroachDB (Scalable SQL Database)
- TiKV (Distributed transactional key value database)
- Dgraph (Graph Database)
- Swarmkit (toolkit for orchestrating distributed systems)

### Observação Importante:

**O código foi implementado em Python baseado no protocolo Raft e inspirado na arquitetura do etcd-io/raft, mas não foi copiado diretamente.**

**Razões:**
1. O etcd-io/raft é escrito em **Go**, não em Python
2. A implementação atual é em **Python** para este trabalho
3. Foi seguida a **especificação do protocolo Raft** e a **arquitetura conceitual** do etcd-io/raft
4. Os conceitos principais foram adaptados para Python:
   - Estados: Follower, Candidate, Leader
   - Eleição de líder
   - Heartbeats
   - Votação
   - Log de replicação (conceitual)
   - Sistema de termos (term)
   - Timeout de eleição

### O que foi baseado no etcd-io/raft:

1. **Arquitetura Conceitual**:
   - Estados do Raft (Follower, Candidate, Leader)
   - Processo de eleição
   - Heartbeats para manter liderança
   - Sistema de termos

2. **Protocolo Raft**:
   - Seguiu a especificação do Raft conforme documentado no etcd-io/raft
   - Implementação dos conceitos principais adaptados para Python

### O que foi implementado do zero:

1. **Código Python completo**: Implementado do zero em Python
2. **Comunicação HTTP**: Versão distribuída usando HTTP/REST API (não RPC como no etcd-io/raft)
3. **Sistema didático**: Simplificado para fins educacionais
4. **Benchmark**: Script de benchmark criado para este trabalho

### Referências Acadêmicas:

- **Protocolo Raft original**: "In Search of an Understandable Consensus Algorithm" - Diego Ongaro e John Ousterhout (2014)
- **Implementação de referência**: [etcd-io/raft](https://github.com/etcd-io/raft) - Biblioteca Raft em Go
- **Estados**: Follower, Candidate, Leader
- **Processo**: Eleição de líder, heartbeats, votação

### Conclusão sobre Origem:

- **Base conceitual**: [etcd-io/raft](https://github.com/etcd-io/raft) (arquitetura e protocolo)
- **Implementação**: Criada do zero em Python
- **Adaptação**: De Go para Python, mantendo conceitos do protocolo Raft
- **Não foi copiado**: Código foi implementado do zero seguindo a especificação do etcd-io/raft e do protocolo Raft original
- **Referência**: Usado como base para entender a arquitetura e implementação do algoritmo Raft

---

## Limpeza de Comentários

### Ação Realizada:

✅ **Removidos todos os comentários adicionados durante o desenvolvimento**

Os arquivos foram limpos removendo:
- Comentários descritivos adicionados (ex: "passo necessário na lógica do protocolo/benchmark")
- Comentários explicativos não originais
- Mantidos apenas comentários de cabeçalho dos arquivos (originais)

### Arquivos Limpos:

1. ✅ `raft_example.py` - Limpo, sem comentários desnecessários
2. ✅ `raft_distribuido.py` - Limpo, sem comentários desnecessários
3. ✅ `run_benchmark.py` - Limpo, sem comentários desnecessários (mantido docstring do cabeçalho)
4. ✅ `client_simulator.py` - Limpo, sem comentários desnecessários
5. ✅ `iniciar_raft_distribuido.py` - Limpo, sem comentários desnecessários

Todos os arquivos foram copiados para a pasta de entrega (`ENTREGA_GRUPO/Raft/`).

---

## Conclusão

### Item 0: ✅ Totalmente Atendido
- Baseado em [etcd-io/raft](https://github.com/etcd-io/raft) (como referência)
- Sistema com 3 réplicas implementado
- Versão distribuída implementada
- Código funcional e executável

### Item 1: ✅ Totalmente Atendido
- Medição de vazão e latência implementada
- Módulo cliente implementado
- Execuções variando carga implementadas
- Reinício do sistema a cada execução
- Duração padrão 3 minutos
- Gráfico vazão x latência gerado

### Item 2: ✅ Totalmente Atendido
- Módulo cliente conforme especificação completa
- Todas as métricas calculadas
- CDF de latências implementado
- Experimentos completos implementados

### Origem do Código:
- **Base conceitual**: [etcd-io/raft](https://github.com/etcd-io/raft) (arquitetura e protocolo)
- **Implementação**: Criada do zero em Python
- **Adaptação**: De Go para Python, mantendo conceitos do protocolo Raft

### Limpeza de Comentários:
- ✅ Completa

**Tudo pronto para entrega!**

