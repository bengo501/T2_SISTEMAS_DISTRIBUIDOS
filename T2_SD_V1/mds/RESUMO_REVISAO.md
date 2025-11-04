# Resumo da Revisão - Paxos

## Revisão dos Itens 1) e 2)

### Item 1: Como o "backoff" tenta evitar livelock de líderes?

**O que é pedido:**
1. ✅ Coloque prints no sistema e execute sem backoff
2. ✅ Observe se existe o comportamento de livelock?
3. ✅ Mande comandos ao sistema durante esta avaliação
4. ✅ Idem para backoff

**Status:** ✅ **TOTALMENTE ATENDIDO**

- Prints implementados em `paxos_mmc.py`
- Script `teste_backoff.py` executa sem backoff (linha 68) e com backoff (linha 75)
- Script observa e compara comportamento de livelock
- Comandos enviados durante avaliação (linhas 44-52)

---

### Item 2: Se uma réplica falha e reinicia

**O que é pedido:**
1. ✅ Há como obter as decisões anteriores para que ela se sincronize?
2. ✅ Construa e demonstre este cenário de execução

**Status:** ✅ **TOTALMENTE ATENDIDO**

- Log persistente implementado em `paxos_mmc.py`
- Métodos `_save_to_log()` e `_load_from_log()` implementados
- Script completo `teste_falha_recuperacao.py` demonstra o cenário passo a passo

---

## Origem do Código Paxos

### Informação Importante:

**O código foi implementado do zero, baseado no protocolo Paxos descrito na literatura acadêmica.**

- **paxos_example.py** - Implementação básica didática criada para este trabalho
- **paxos_mmc.py** - Implementação completa do Multi-Paxos criada para este trabalho

### Referências Acadêmicas:

- **Protocolo Paxos original**: "The Part-Time Parliament" - Leslie Lamport (1998)
- **Multi-Paxos**: Extensão do Paxos para múltiplas instâncias
- **Backoff**: Técnica padrão para evitar livelock em sistemas distribuídos

### Observação:

O código foi implementado seguindo a especificação do protocolo Paxos, mas **não foi copiado de nenhum repositório específico ou código fonte encontrado na internet**. A implementação foi feita para atender aos requisitos específicos do trabalho.

O enunciado menciona "código de Paxos MMC" e "python v2", mas não especifica uma fonte ou repositório específico. Portanto, o código foi desenvolvido do zero baseado no protocolo.

---

## Limpeza de Comentários

### Ação Realizada:

✅ **Removidos todos os comentários adicionados durante o desenvolvimento**

Os arquivos foram limpos removendo:
- Comentários descritivos adicionados (ex: "passo necessário na lógica do protocolo/benchmark")
- Comentários explicativos não originais
- Mantidos apenas comentários de cabeçalho dos arquivos (originais)

### Arquivos Limpos:

1. ✅ `paxos_mmc.py` - Limpo, sem comentários desnecessários
2. ✅ `paxos_example.py` - Limpo, sem comentários desnecessários
3. ✅ `teste_backoff.py` - Limpo, sem comentários desnecessários
4. ✅ `teste_falha_recuperacao.py` - Limpo, sem comentários desnecessários

Todos os arquivos foram copiados para a pasta de entrega (`ENTREGA_GRUPO/Paxos/`).

---

## Conclusão

✅ **Revisão Completa:**
- Item 1: Totalmente atendido
- Item 2: Totalmente atendido
- Origem do código: Implementado do zero baseado no protocolo Paxos
- Limpeza de comentários: Completa

Tudo pronto para entrega!

