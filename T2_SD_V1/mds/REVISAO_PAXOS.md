# Revisão - O que é pedido nos itens 1) e 2) do Paxos

## Item 1: Como o "backoff" tenta evitar livelock de líderes?

### O que é pedido:

1. **Coloque prints no sistema e execute sem backoff**
   - ✅ Implementado: prints detalhados em `paxos_mmc.py`
   - ✅ Script `teste_backoff.py` executa sem backoff (linha 68)

2. **Observe se existe o comportamento de livelock?**
   - ✅ Implementado: script observa e compara comportamento
   - ✅ Prints mostram conflitos e tentativas repetidas sem convergência

3. **Mande comandos ao sistema durante esta avaliação**
   - ✅ Implementado: `teste_backoff.py` envia comandos durante execução (linhas 44-52)
   - ✅ Comandos enviados a cada segundo durante a avaliação

4. **Idem para backoff**
   - ✅ Implementado: mesmo script executa com backoff (linha 75)
   - ✅ Compara comportamento com e sem backoff lado a lado

### Verificação de Atendimento:

| Requisito | Status | Localização |
|-----------|--------|-------------|
| Prints no sistema | ✅ | `paxos_mmc.py` - múltiplos prints |
| Executar sem backoff | ✅ | `teste_backoff.py` linha 68 |
| Observar livelock | ✅ | `teste_backoff.py` - análise de comportamento |
| Enviar comandos durante avaliação | ✅ | `teste_backoff.py` linhas 44-52 |
| Executar com backoff | ✅ | `teste_backoff.py` linha 75 |
| Comparar resultados | ✅ | Script compara ambos os cenários |

---

## Item 2: Se uma réplica falha e reinicia

### O que é pedido:

1. **Há como obter as decisões anteriores para que ela se sincronize?**
   - ✅ Implementado: log persistente em `paxos_mmc.py`
   - ✅ Métodos `_save_to_log()` e `_load_from_log()` implementados

2. **Construa e demonstre este cenário de execução**
   - ✅ Implementado: script completo `teste_falha_recuperacao.py`
   - ✅ Demonstra passo a passo:
     - Criação do sistema
     - Decisões iniciais
     - Falha de réplica
     - Continuação do sistema
     - Recuperação da réplica
     - Sincronização

### Verificação de Atendimento:

| Requisito | Status | Localização |
|-----------|--------|-------------|
| Recuperação de decisões | ✅ | `paxos_mmc.py` - log persistente |
| Construir cenário | ✅ | `teste_falha_recuperacao.py` |
| Demonstrar execução | ✅ | Script completo com prints |
| Mostrar sincronização | ✅ | Script mostra recuperação e sincronização |

---

## Origem do Código Paxos

### Informação Importante:

**O código foi implementado do zero, baseado no protocolo Paxos descrito na literatura, não foi copiado de nenhuma fonte específica.**

O enunciado menciona "código de Paxos MMC" e "python v2", mas não especifica uma fonte ou repositório específico. Portanto:

1. **paxos_example.py** - Implementação básica didática criada para este trabalho
2. **paxos_mmc.py** - Implementação completa do Multi-Paxos com:
   - Múltiplos proposers
   - Backoff exponencial
   - Log persistente
   - Baseado no protocolo Paxos clássico (Leslie Lamport)

### Referências Acadêmicas:

- **Protocolo Paxos original**: "The Part-Time Parliament" - Leslie Lamport (1998)
- **Multi-Paxos**: Extensão do Paxos para múltiplas instâncias
- **Backoff**: Técnica padrão para evitar livelock em sistemas distribuídos

### Observação:

O código foi implementado seguindo a especificação do protocolo Paxos, mas não foi copiado de nenhum repositório específico ou código fonte encontrado na internet. A implementação foi feita para atender aos requisitos específicos do trabalho.

---

## Conclusão

### Item 1: ✅ Totalmente Atendido
- Prints implementados
- Execução sem backoff com observação de livelock
- Execução com backoff para comparação
- Comandos enviados durante avaliação

### Item 2: ✅ Totalmente Atendido
- Recuperação de decisões implementada
- Cenário completo construído e demonstrado
- Script mostra todo o processo passo a passo

