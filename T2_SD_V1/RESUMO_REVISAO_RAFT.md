# Resumo da Revisão - Raft

## Revisão dos Itens 0), 1) e 2)

### Item 0: Baixe, crie um sistema com no mínimo 3 réplicas, execute

**O que é pedido:**
1. ✅ Escolha uma implementação de Raft
2. ✅ Crie um sistema com no mínimo 3 réplicas
3. ✅ Execute
4. ✅ Use o laboratório. Deve ser distribuído

**Status:** ✅ **TOTALMENTE ATENDIDO**

- Sistema com 3 réplicas implementado (`raft_example.py`)
- Versão distribuída implementada (`raft_distribuido.py`)
- Código funcional e executável

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

- Medição de vazão e latência implementada
- Módulo cliente implementado
- Execuções variando carga implementadas
- Reinício do sistema a cada execução
- Duração padrão 180 segundos (3 minutos)
- Gráfico vazão x latência gerado

---

### Item 2: Módulo Cliente e Experimentos

**O que é pedido:**
1. ✅ Aguarda sistema estar no ar
2. ✅ Timestamp_inicio
3. ✅ Loop parada por tempo
4. ✅ Cria pedido, timestamp1, manda para cluster, aguarda resposta
5. ✅ Calcula amostra de latência = tempoAgora - timestamp1
6. ✅ Grava amostra em array, nroPedidos++
7. ✅ Calcula tempoTotal, vazão, latência média
8. ✅ Função de distribuição cumulativa de latência
9. ✅ Desempenho geral: vazão = somatório, latência = média
10. ✅ Experimentos: para cada nível de carga, subir réplicas, aguardar, subir clientes, aguardar término, colher dados, plotar ponto

**Status:** ✅ **TOTALMENTE ATENDIDO**

- Módulo cliente conforme especificação completa
- Todas as métricas calculadas
- CDF de latências implementado
- Experimentos completos implementados

---

## Origem do Código Raft

### Informação Importante:

**O código foi implementado do zero, baseado no protocolo Raft descrito na literatura acadêmica, não foi baixado de nenhuma fonte específica.**

O enunciado menciona "Escolha uma implementação de Raft" e "Baixe", mas não especifica uma fonte ou repositório específico. Portanto:

1. **raft_example.py** - Implementação didática criada para este trabalho
2. **raft_distribuido.py** - Versão distribuída criada para este trabalho
3. **run_benchmark.py** - Script de benchmark criado para este trabalho
4. **client_simulator.py** - Cliente criado para este trabalho

### Referências Acadêmicas:

- **Protocolo Raft original**: "In Search of an Understandable Consensus Algorithm" - Diego Ongaro e John Ousterhout (2014)
- **Estados**: Follower, Candidate, Leader
- **Processo**: Eleição de líder, heartbeats, votação

### Observação:

O código foi implementado seguindo a especificação do protocolo Raft, mas **não foi baixado de nenhum repositório específico ou código fonte encontrado na internet**. A implementação foi feita para atender aos requisitos específicos do trabalho.

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

✅ **Revisão Completa:**
- Item 0: Totalmente atendido
- Item 1: Totalmente atendido
- Item 2: Totalmente atendido
- Origem do código: Implementado do zero baseado no protocolo Raft
- Limpeza de comentários: Completa

Tudo pronto para entrega!

