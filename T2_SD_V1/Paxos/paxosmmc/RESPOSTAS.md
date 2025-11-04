# Respostas - Estudo de Caso com Paxos MMC

## Base de Implementação

**Base:** [paxosmmc](https://github.com/denizalti/paxosmmc) - Paxos Made Moderately Complex

O código foi baseado no repositório [paxosmmc](https://github.com/denizalti/paxosmmc) e adaptado para os requisitos do enunciado.

## Item 0: Entender, Executar, Avaliar

**Resposta:**
A implementação do Paxos MMC foi baseada no código do repositório [paxosmmc](https://github.com/denizalti/paxosmmc) e adaptada para incluir:
- Suporte a backoff no Leader para evitar livelock
- Log persistente em Replica e Acceptor para recuperação após falhas
- Scripts de demonstração para os itens 1 e 2

O sistema implementa:
- Replica: recebe requests e decisions, propõe comandos para leaders
- Acceptor: processa P1a/P1b e P2a/P2b messages, mantém log de decisões
- Leader: coordena propostas, usa backoff quando preemptado
- Scout: fase 1 do Paxos (prepare/promise)
- Commander: fase 2 do Paxos (accept/accepted)

## Item 1: Como o "backoff" tenta evitar livelock de líderes?

**Resposta:**
O backoff exponencial evita livelock fazendo com que leaders que foram preemptados aguardem um tempo crescente antes de tentar novamente. Isso reduz a probabilidade de múltiplos leaders competindo simultaneamente e conflitando constantemente.

**Implementação:**
- O `Leader` tem parâmetro `use_backoff` (True/False)
- Quando preemptado, o leader incrementa `failed_attempts`
- O tempo de backoff = `backoff_time * (2 ^ failed_attempts)`
- O backoff é limitado a um máximo (ex: 2 segundos)
- Quando um leader é adotado, o contador é resetado

**Evidências:**

1. **Execução sem backoff:**
   - Execute `python teste_backoff.py`
   - Observe que sem backoff, os leaders tentam imediatamente após serem preemptados
   - Isso pode causar livelock onde múltiplos leaders competem continuamente
   - As prints mostram múltiplas tentativas conflitantes
   - Prints mostram: `[leader X] sem backoff - tentando novamente imediatamente...`

2. **Execução com backoff:**
   - O mesmo script executa com backoff habilitado
   - Os leaders que são preemptados aguardam um tempo crescente (backoff exponencial)
   - Isso permite que um leader obtenha maioria enquanto outros aguardam
   - As prints mostram menos conflitos e mais sucessos
   - Prints mostram: `[leader X] aguardando backoff de Y.XXs antes de tentar novamente...`

**Comandos executados durante a avaliação:**
O script `teste_backoff.py` envia comandos automaticamente durante a execução (a cada 1 segundo) para observar o comportamento do sistema com e sem backoff.

## Item 2: Se uma réplica falha e reinicia, há como obter as decisões anteriores para que ela se sincronize?

**Resposta:**
Sim, há como obter as decisões anteriores. Tanto `Replica` quanto `Acceptor` salvam decisões em log persistente (arquivo JSON). Quando uma réplica ou acceptor reinicia, o log é carregado e as decisões são recuperadas.

**Implementação:**
- `Replica` salva decisões em `log_file` (formato JSON)
- `Acceptor` salva pvalues aceitos em `log_file` (formato JSON)
- Ao reiniciar, o log é carregado e as decisões são recuperadas
- A réplica pode sincronizar com outras réplicas usando decisões do log

**Demonstração:**
Execute `python teste_falha_recuperacao.py`

O script demonstra:
1. **Fase 1:** Envio de comandos iniciais
2. **Fase 2:** Simulação de falha da réplica (réplica para de processar)
3. **Fase 3:** Envio de comandos durante a falha (outras réplicas continuam)
4. **Fase 4:** Recuperação da réplica (criando nova instância com log)
   - A réplica carrega decisões do log
   - Prints mostram: `[replica X] recuperou Y decisões do log, slot_out=Z`
5. **Fase 5:** Envio de novos comandos após recuperação
   - A réplica recuperada pode processar novos comandos

**Evidências:**
- Logs são salvos em arquivos JSON (`logs_falha_recuperacao/replica_X.log`)
- Ao reiniciar, o log é carregado e as decisões são recuperadas
- A réplica recuperada pode sincronizar com outras réplicas

## Referências

- [paxosmmc](https://github.com/denizalti/paxosmmc) - Repositório original
- [paxos.systems](https://paxos.systems) - Documentação do protocolo

