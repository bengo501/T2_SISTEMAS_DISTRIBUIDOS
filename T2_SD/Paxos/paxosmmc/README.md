# Paxos Made Moderately Complex (PaxosMMC)

Implementação baseada no repositório [paxosmmc](https://github.com/denizalti/paxosmmc) adaptada para os requisitos do enunciado.

## Estrutura

- `utils.py` - Utilitários (BallotNumber, PValue, Command, etc.)
- `message.py` - Tipos de mensagens do Paxos
- `process.py` - Classe base Process
- `acceptor.py` - Implementação do Acceptor com log persistente
- `replica.py` - Implementação do Replica com log persistente
- `leader.py` - Implementação do Leader com suporte a backoff
- `scout.py` - Implementação do Scout
- `commander.py` - Implementação do Commander
- `env.py` - Environment para criar e executar o sistema
- `teste_backoff.py` - Script para testar backoff (com e sem)
- `teste_falha_recuperacao.py` - Script para demonstrar falha e recuperação

## Requisitos do Enunciado

### Item 0: Entender, Executar, Avaliar

A implementação segue o protocolo Paxos MMC conforme descrito em [paxos.systems](https://paxos.systems).

### Item 1: Como o "backoff" tenta evitar livelock de líderes?

**Implementação:** O `Leader` tem suporte a backoff exponencial quando preemptado.

**Como funciona:**
- Quando um leader é preemptado, ele incrementa `failed_attempts`
- O tempo de backoff = `backoff_time * (2 ^ failed_attempts)`
- O backoff é limitado a um máximo (ex: 2 segundos)
- Quando um leader é adotado, o contador é resetado

**Teste:**
```bash
python teste_backoff.py
```

O script executa:
1. Teste sem backoff (pode causar livelock)
2. Teste com backoff (evita livelock)

Durante a execução, comandos são enviados automaticamente para observar o comportamento.

### Item 2: Se uma réplica falha e reinicia, há como obter as decisões anteriores?

**Implementação:** `Replica` e `Acceptor` salvam decisões em log persistente.

**Como funciona:**
- Cada réplica e acceptor salva decisões em arquivo de log
- Ao reiniciar, o log é carregado e as decisões são recuperadas
- A réplica pode sincronizar com outras réplicas usando decisões do log

**Teste:**
```bash
python teste_falha_recuperacao.py
```

O script demonstra:
1. Envio de comandos iniciais
2. Simulação de falha da réplica
3. Envio de comandos durante a falha
4. Recuperação da réplica com log
5. Envio de novos comandos após recuperação

## Execução

### Executar sistema básico

```bash
python env.py
```

### Executar teste de backoff

```bash
python teste_backoff.py
```

### Executar teste de falha e recuperação

```bash
python teste_falha_recuperacao.py
```

## Referências

- [paxosmmc](https://github.com/denizalti/paxosmmc) - Repositório original
- [paxos.systems](https://paxos.systems) - Documentação do protocolo

