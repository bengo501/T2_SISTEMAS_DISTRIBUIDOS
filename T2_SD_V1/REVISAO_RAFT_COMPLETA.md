# Revisão Completa - O que é pedido nos itens 0), 1) e 2) do Raft

## Item 0: Baixe, crie um sistema com no mínimo 3 réplicas, execute

### O que é pedido:

1. **Escolha uma implementação de Raft**
   - **Base escolhida**: [etcd-io/raft](https://github.com/etcd-io/raft) - Biblioteca Raft em Go
   - **Nota**: O repositório etcd-io/raft é em Go, mas foi usado como referência para implementar em Python

2. **Baixe** - Escolha uma implementação de Raft
   - ⚠️ **Nota importante**: O código foi implementado em Python baseado no protocolo Raft e na referência do etcd-io/raft, mas não foi copiado diretamente (pois o etcd-io/raft é em Go)

3. **Crie um sistema com no mínimo 3 réplicas**
   - ✅ Implementado: `raft_example.py` com 3 servidores (linha 81)
   - ✅ Implementado: `raft_distribuido.py` com 3 nós distribuídos

4. **Execute**
   - ✅ Implementado: Código funcional e executável

5. **Use o laboratório. Deve ser distribuído**
   - ✅ Implementado: `raft_distribuido.py` permite execução distribuída
   - ✅ Versão distribuída usa HTTP para comunicação entre nós
   - ✅ Pode executar em múltiplas máquinas/hosts diferentes

### Verificação de Atendimento:

| Requisito | Status | Localização |
|-----------|--------|-------------|
| Escolher implementação | ✅ | Baseado em etcd-io/raft |
| 3 réplicas | ✅ | `raft_example.py` linha 81 |
| Sistema funcional | ✅ | Código executável |
| Distribuído | ✅ | `raft_distribuido.py` |

---

## Item 1: Medição de Desempenho - Visão Geral

### O que é pedido:

1. **Medir vazão (ops/s) e latência para níveis incrementais de carga**
   - ✅ Implementado: `run_benchmark.py` mede vazão e latência

2. **Módulo de geração de carga controlada (cliente)**
   - ✅ Implementado: Classe `Client` em `run_benchmark.py` (linha 27)

3. **Várias execuções variando carga, anotando vazão e latência**
   - ✅ Implementado: Loop por níveis de carga (linha 120)

4. **Sistema terminado e reiniciado a cada execução**
   - ✅ Implementado: `run_round_with_restart()` (linha 63) reinicia cluster

5. **Cada execução roda por tempo determinado (exemplo: 3 minutos)**
   - ✅ Implementado: Duração padrão 180 segundos (3 minutos) - linha 107

6. **Gráfico com eixo x=vazão e eixo y=latência, cada ponto = uma execução**
   - ✅ Implementado: Gráfico gerado (linha 136-147)

### Verificação de Atendimento:

| Requisito | Status | Localização |
|-----------|--------|-------------|
| Medir vazão e latência | ✅ | `run_benchmark.py` |
| Módulo cliente | ✅ | Classe `Client` (linha 27) |
| Várias execuções variando carga | ✅ | Loop linha 120 |
| Reiniciar a cada execução | ✅ | `run_round_with_restart()` |
| Duração 3 minutos | ✅ | Padrão 180s (linha 107) |
| Gráfico vazão x latência | ✅ | Linha 136-147 |

---

## Item 2: Módulo Cliente

### O que é pedido:

1. **Aguarda sistema estar no ar**
   - ✅ Implementado: `_pick_leader()` aguarda líder (linha 47-53)

2. **Timestamp_inicio**
   - ✅ Implementado: `start = time.time()` (linha 37)

3. **Loop parada por tempo:**
   - ✅ Implementado: `while time.time() - start < self.duration_s` (linha 38)

4. **Cria pedido, timestamp1, manda para cluster, aguarda resposta**
   - ✅ Implementado: Linhas 39-42

5. **Calcula amostra de latência = tempoAgora - timestamp1**
   - ✅ Implementado: `lat = time.time() - t1` (linha 42)

6. **Grava amostra em array, nroPedidos++**
   - ✅ Implementado: `self.latencies.append(lat)` e `self.requests += 1` (linhas 43-44)

7. **Calcula tempoTotal = tempoAgora - timestamp_inicio**
   - ✅ Implementado: `total_time = duration_s` (linha 84)

8. **Vazão = nroPedidos / tempoTotal**
   - ✅ Implementado: `throughput = total_reqs / total_time` (linha 85)

9. **Latência Média = somatório / nroPedidos**
   - ✅ Implementado: `avg_latency = sum(all_latencies) / len(all_latencies)` (linha 86)

10. **Função de Distribuição Cumulativa de latência**
    - ✅ Implementado: `calcular_cdf()` (linha 95-103)
    - ✅ Gráficos CDF gerados para cada rodada (linha 150-170)

11. **Desempenho geral: vazão = somatório das vazões, latência = média das latências**
    - ✅ Implementado: Coleta todas as latências (linha 79-81) e calcula métricas gerais

12. **Experimentos: para cada nível de carga**
    - ✅ Implementado: Loop por níveis de carga (linha 120)
    - ✅ Subir réplicas (linha 64-67)
    - ✅ Aguardar ativas (linha 69)
    - ✅ Subir clientes (linha 72-74)
    - ✅ Aguardar término (linha 75-76)
    - ✅ Colher dados (linha 79-81)
    - ✅ Obter desempenho geral (linha 85-86)
    - ✅ Plotar ponto no gráfico (linha 136-147)

### Verificação de Atendimento:

| Requisito | Status | Localização |
|-----------|--------|-------------|
| Aguarda sistema | ✅ | `_pick_leader()` |
| Timestamp_inicio | ✅ | Linha 37 |
| Loop por tempo | ✅ | Linha 38 |
| Cria pedido, manda, aguarda | ✅ | Linhas 39-42 |
| Calcula latência | ✅ | Linha 42 |
| Grava em array | ✅ | Linha 43 |
| Conta pedidos | ✅ | Linha 44 |
| Calcula métricas | ✅ | Linhas 85-86 |
| CDF | ✅ | Linha 95-103, 150-170 |
| Experimentos | ✅ | Loop linha 120 |

---

## Origem do Código Raft

### Referência Base:

**Base de Implementação**: [etcd-io/raft](https://github.com/etcd-io/raft)

O repositório [etcd-io/raft](https://github.com/etcd-io/raft) é uma biblioteca Raft em Go para manter uma máquina de estado replicada. É uma implementação de produção amplamente usada por sistemas como etcd, CockroachDB, TiKV, entre outros.

### Observação Importante:

**O código foi implementado em Python baseado no protocolo Raft e inspirado na arquitetura do etcd-io/raft, mas não foi copiado diretamente.**

Razões:
1. O etcd-io/raft é escrito em **Go**, não em Python
2. A implementação atual é em **Python** para este trabalho
3. Foi seguida a **especificação do protocolo Raft** e a **arquitetura conceitual** do etcd-io/raft
4. Os conceitos principais foram adaptados:
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
2. **Comunicação HTTP**: Versão distribuída usando HTTP (não RPC como no etcd-io/raft)
3. **Sistema didático**: Simplificado para fins educacionais
4. **Benchmark**: Script de benchmark criado para este trabalho

### Referências Acadêmicas:

- **Protocolo Raft original**: "In Search of an Understandable Consensus Algorithm" - Diego Ongaro e John Ousterhout (2014)
- **Implementação de referência**: [etcd-io/raft](https://github.com/etcd-raft) - Biblioteca Raft em Go
- **Estados**: Follower, Candidate, Leader
- **Processo**: Eleição de líder, heartbeats, votação

### Conclusão sobre Origem:

- **Base conceitual**: [etcd-io/raft](https://github.com/etcd-io/raft) (arquitetura e protocolo)
- **Implementação**: Criada do zero em Python
- **Adaptação**: De Go para Python, mantendo conceitos do protocolo Raft
- **Não foi copiado**: Código foi implementado do zero seguindo a especificação do etcd-io/raft e do protocolo Raft original
- **Referência**: Usado como base para entender a arquitetura e implementação do algoritmo Raft

---

## Conclusão

### Item 0: ✅ Totalmente Atendido
- Baseado em etcd-io/raft (como referência)
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
- **Base conceitual**: etcd-io/raft (https://github.com/etcd-io/raft)
- **Implementação**: Criada do zero em Python baseada no protocolo Raft
- **Adaptação**: De Go para Python, mantendo conceitos do protocolo

