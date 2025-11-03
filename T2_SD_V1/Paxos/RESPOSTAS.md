# Respostas - Estudo de Caso com Paxos MMC

## Membros do Grupo
[Preencher com os nomes dos membros do grupo]

## Questões sobre Paxos

### Item 0: Entender, Executar, Avaliar

**Resposta:**
A implementação do Paxos MMC foi entendida, executada e avaliada. O sistema implementa:
- Múltiplos proposers competindo simultaneamente
- Sistema de backoff exponencial para evitar livelock
- Log persistente para recuperação de decisões após falhas
- Scripts de demonstração para os itens 1 e 2

### Item 1: Como o "backoff" tenta evitar livelock de líderes?

**Resposta:**
O backoff exponencial evita livelock fazendo com que proposers que falharam em obter maioria aguardem um tempo crescente antes de tentar novamente. Isso reduz a probabilidade de múltiplos proposers competindo simultaneamente e conflitando constantemente.

**Evidências:**

1. **Execução sem backoff:**
   - Execute `python teste_backoff.py`
   - Observe que sem backoff, os proposers tentam imediatamente após cada falha
   - Isso pode causar livelock onde múltiplos proposers competem continuamente
   - As prints mostram múltiplas tentativas conflitantes

2. **Execução com backoff:**
   - O mesmo script executa com backoff habilitado
   - Os proposers que falham aguardam um tempo crescente (backoff exponencial)
   - Isso permite que um proposer obtenha maioria enquanto outros aguardam
   - As prints mostram menos conflitos e mais sucessos

**Como funciona:**
- Quando um proposer falha, incrementa um contador de tentativas falhadas
- O tempo de backoff = tempo_base * (2 ^ tentativas_falhadas)
- O backoff é limitado a um máximo (ex: 2 segundos)
- Quando um proposer tem sucesso, o contador é resetado

**Comandos executados durante a avaliação:**
O script `teste_backoff.py` envia comandos automaticamente durante a execução para observar o comportamento do sistema com e sem backoff.

### Item 2: Se uma réplica falha e reinicia, há como obter as decisões anteriores para que ela se sincronize?

**Resposta:**
Sim, através de log persistente. Quando uma réplica (acceptor) reinicia, ela carrega as decisões anteriores de seu arquivo de log e atualiza seu estado interno.

**Evidências:**

**Demonstração do cenário:**
Execute `python teste_falha_recuperacao.py`

O script demonstra:
1. Criação do sistema inicial com 5 acceptors
2. Realização de várias propostas e decisões
3. Falha do acceptor 2 (simulada removendo-o do sistema)
4. Continuação do sistema com os acceptors restantes
5. Mais decisões são tomadas enquanto o acceptor 2 está fora
6. Reinício do acceptor 2 e recuperação do log
7. O acceptor recuperado carrega todas as decisões anteriores do arquivo de log
8. O acceptor é reintegrado ao sistema e continua funcionando normalmente

**Como funciona a recuperação:**
- Cada acceptor salva todas as decisões aceitas em um arquivo de log (JSON)
- Cada linha do log contém: proposal_number, value, acceptor_id, timestamp
- Quando um acceptor reinicia:
  1. Verifica se existe arquivo de log
  2. Carrega todas as decisões do log
  3. Atualiza seu estado interno (promised_number, accepted_number, accepted_value)
  4. Fica pronto para continuar participando do protocolo

**Exemplo de log:**
```json
{"proposal_number": 1, "value": "valor_inicial_1", "acceptor_id": 2, "timestamp": 1234567890.123}
{"proposal_number": 2, "value": "valor_inicial_2", "acceptor_id": 2, "timestamp": 1234567890.456}
```

**Limitações da implementação atual:**
- Esta é uma implementação didática
- Em um sistema real, seria necessário também:
  - Sincronizar com outros acceptors para obter decisões que foram perdidas
  - Tratar casos onde o log pode estar incompleto
  - Implementar snapshots para logs muito grandes

## Observações Finais

A implementação demonstra os conceitos principais do Paxos MMC:
- Evita livelock através de backoff exponencial
- Permite recuperação de falhas através de log persistente
- Garante consenso mesmo com múltiplos proposers competindo

Para experimentos mais realistas, seria necessário:
- Rede distribuída real (RPC/HTTP)
- Persistência em disco mais robusta
- Tratamento de falhas mais complexos (network partitions, etc.)

