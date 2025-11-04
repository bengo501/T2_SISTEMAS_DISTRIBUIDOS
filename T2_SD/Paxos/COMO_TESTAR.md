# Como Testar o Paxos

## Pré-requisitos

- Python 2.7 ou Python 3
- Dependências: nenhuma especial (usa apenas bibliotecas padrão)

## Testes Disponíveis

### 1. Teste Básico do Sistema

Teste rápido para verificar se o sistema está funcionando:

```bash
cd T2_SD/Paxos/paxosmmc
python env.py
```

**O que esperar:**
- Sistema cria réplicas, acceptors e leaders
- Envia comandos
- Imprime mensagens do sistema
- Pressione Ctrl+C para parar

---

### 2. Teste de Backoff (Item 1 do enunciado)

Este teste demonstra o efeito do backoff para evitar livelock:

```bash
cd T2_SD/Paxos/paxosmmc
python teste_backoff.py
```

**O que esperar:**

**Teste 1: Sem Backoff (pode causar livelock)**
- Leaders tentam imediatamente após serem preemptados
- Prints mostram: `[leader X] sem backoff - tentando novamente imediatamente...`
- Pode haver muitos conflitos entre leaders
- Prints mostram: `[comando externo X] enviando 'comando_X' via replica Y`

**Teste 2: Com Backoff (evita livelock)**
- Leaders aguardam tempo crescente após serem preemptados
- Prints mostram: `[leader X] aguardando backoff de Y.XXs antes de tentar novamente...`
- Menos conflitos, mais sucessos
- Prints mostram líder sendo adotado: `[leader X] [OK] adotado para ballot...`

**Duração:** ~30 segundos (15s sem backoff + 15s com backoff)

**Resultado esperado:**
- Sem backoff: mais conflitos, possível livelock
- Com backoff: menos conflitos, convergência melhor

---

### 3. Teste de Falha e Recuperação (Item 2 do enunciado)

Este teste demonstra como uma réplica recupera decisões após falha:

```bash
cd T2_SD/Paxos/paxosmmc
python teste_falha_recuperacao.py
```

**O que esperar:**

**Fase 1: Envio de comandos iniciais**
- Réplicas processam comandos
- Prints mostram: `[replica X] perform Y : Command(...)`

**Fase 2: Simulação de falha da réplica**
- Prints mostram: `[fase 2] réplica replica: 0 falhou`

**Fase 3: Envio de comandos durante falha**
- Outras réplicas continuam funcionando
- Prints mostram: `[replica 1] perform ...`

**Fase 4: Recuperação da réplica**
- Prints mostram: `[replica 0] recuperou X decisões do log, slot_out=Y`
- Réplica carrega decisões do arquivo de log

**Fase 5: Envio de novos comandos após recuperação**
- Réplica recuperada processa novos comandos normalmente

**Duração:** ~30 segundos

**Resultado esperado:**
- Réplica recupera decisões anteriores do log
- Réplica pode sincronizar com outras réplicas

**Logs gerados:**
- `logs_falha_recuperacao/replica_0.log` - Log da réplica que falhou
- `logs_falha_recuperacao/replica_1.log` - Log da outra réplica
- `logs_falha_recuperacao/acceptor_0_X.log` - Logs dos acceptors

---

## Verificação de Funcionamento

### Verificar se o sistema está funcionando corretamente:

1. **Verificar prints:**
   - ✅ Réplicas devem imprimir: `[replica X] aqui estou`
   - ✅ Acceptors devem imprimir: `[acceptor X] aqui estou`
   - ✅ Leaders devem imprimir: `[leader X] aqui estou`

2. **Verificar processamento de comandos:**
   - ✅ Réplicas devem imprimir: `[replica X] perform Y : Command(...)`
   - ✅ Acceptors devem imprimir: `[acceptor X] aceita pvalue ...`
   - ✅ Leaders devem imprimir: `[leader X] criando commander para slot ...`

3. **Verificar backoff:**
   - ✅ Sem backoff: `[leader X] sem backoff - tentando novamente imediatamente...`
   - ✅ Com backoff: `[leader X] aguardando backoff de Y.XXs antes de tentar novamente...`

4. **Verificar recuperação:**
   - ✅ Ao reiniciar: `[replica X] recuperou Y decisões do log, slot_out=Z`
   - ✅ Logs devem existir em `logs_falha_recuperacao/`

---

## Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'env'"

**Solução:**
```bash
cd T2_SD/Paxos/paxosmmc
python teste_backoff.py
```

### Erro: "ImportError"

**Solução:**
Certifique-se de estar na pasta `paxosmmc/`:
```bash
cd T2_SD/Paxos/paxosmmc
```

### Sistema não processa comandos

**Verificação:**
- Verifique se há líder ativo (prints mostram `[leader X] [OK] adotado`)
- Aguarde alguns segundos para eleição de líder
- Verifique se há acceptors suficientes (mínimo 3)

---

## Exemplo de Execução

### Teste de Backoff:

```bash
$ cd T2_SD/Paxos/paxosmmc
$ python teste_backoff.py

================================================================================
teste 1: execução sem backoff (pode causar livelock)
================================================================================

================================================================================
teste com sem backoff
================================================================================

[replica 0] aqui estou
[acceptor 0] aqui estou
[leader 0] aqui estou
...
[comando externo 1] enviando 'comando_1' via replica 0
[leader 0] sem backoff - tentando novamente imediatamente...
...

================================================================================
teste 2: execução com backoff (evita livelock)
================================================================================

[leader 0] aguardando backoff de 0.20s antes de tentar novamente...
[leader 0] [OK] adotado para ballot ...
...
```

---

## Resultados Esperados

### Teste de Backoff:
- ✅ Execução sem backoff mostra mais conflitos
- ✅ Execução com backoff mostra menos conflitos
- ✅ Comandos são enviados durante ambos os testes

### Teste de Falha e Recuperação:
- ✅ Réplica recupera decisões do log
- ✅ Prints mostram: `[replica X] recuperou Y decisões do log`
- ✅ Réplica pode processar novos comandos após recuperação

---

## Arquivos de Log

Os testes geram logs em:
- `logs_backoff_on/` - Logs do teste com backoff
- `logs_backoff_off/` - Logs do teste sem backoff
- `logs_falha_recuperacao/` - Logs do teste de falha e recuperação

Estes logs podem ser usados como evidência do funcionamento.

