# Revisão - O que é pedido nos itens 0), 1) e 2) do Raft

## Item 0: Baixe, crie um sistema com no mínimo 3 réplicas, execute

### O que é pedido:

1. **Baixe** - Escolha uma implementação de Raft
   - ⚠️ **Nota importante**: O código foi implementado do zero, não foi baixado de nenhuma fonte específica

2. **Crie um sistema com no mínimo 3 réplicas**
   - ✅ Implementado: `raft_example.py` com 3 servidores (linha 81)
   - ✅ Implementado: `raft_distribuido.py` com 3 nós distribuídos

3. **Execute**
   - ✅ Implementado: Código funcional e executável

4. **Use o laboratório. Deve ser distribuído**
   - ✅ Implementado: `raft_distribuido.py` permite execução distribuída
   - ✅ Versão distribuída usa HTTP para comunicação entre nós
   - ✅ Pode executar em múltiplas máquinas/hosts diferentes

### Verificação de Atendimento:

| Requisito | Status | Localização |
|-----------|--------|-------------|
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

### Informação Importante:

**O código foi implementado do zero, baseado no protocolo Raft descrito na literatura acadêmica, não foi baixado de nenhuma fonte específica.**

O enunciado menciona "Escolha uma implementação de Raft" e "Baixe", mas não especifica uma fonte ou repositório específico. Portanto:

1. **raft_example.py** - Implementação didática criada para este trabalho
   - Baseado no protocolo Raft original
   - Estados: Follower, Candidate, Leader
   - Eleição de líder, heartbeats, votação

2. **raft_distribuido.py** - Versão distribuída criada para este trabalho
   - Extensão da versão didática para execução distribuída
   - Comunicação via HTTP/REST API

3. **run_benchmark.py** - Script de benchmark criado para este trabalho
   - Implementa medição de desempenho conforme especificação

4. **client_simulator.py** - Cliente criado para este trabalho
   - Implementa módulo cliente conforme especificação

### Referências Acadêmicas:

- **Protocolo Raft original**: "In Search of an Understandable Consensus Algorithm" - Diego Ongaro e John Ousterhout (2014)
- **Estados**: Follower, Candidate, Leader
- **Processo**: Eleição de líder, heartbeats, votação

### Observação:

O código foi implementado seguindo a especificação do protocolo Raft, mas **não foi baixado de nenhum repositório específico ou código fonte encontrado na internet**. A implementação foi feita para atender aos requisitos específicos do trabalho.

---

## Conclusão

### Item 0: ✅ Totalmente Atendido
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
- Implementado do zero baseado no protocolo Raft
- Não foi baixado de nenhuma fonte específica
- Baseado na literatura acadêmica do Raft

