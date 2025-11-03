# Correções Realizadas - T2 Sistemas Distribuídos

## Resumo das Correções

### Paxos - Implementações Adicionadas

1. **paxos_mmc.py** - Implementação completa do Paxos MMC com:
   - Múltiplos proposers competindo simultaneamente
   - Backoff exponencial para evitar livelock
   - Log persistente para recuperação de decisões após falhas
   - Suporte para recuperação de estado através de arquivos de log

2. **teste_backoff.py** - Script para demonstrar backoff vs sem backoff:
   - Executa sistema sem backoff (pode causar livelock)
   - Executa sistema com backoff (evita livelock)
   - Envia comandos durante a avaliação
   - Mostra prints comparando os dois comportamentos

3. **teste_falha_recuperacao.py** - Script para demonstrar falha e recuperação:
   - Cria sistema inicial com decisões
   - Simula falha de uma réplica (acceptor)
   - Continua sistema com réplicas restantes
   - Demonstra recuperação do acceptor através do log
   - Mostra sincronização do acceptor recuperado

4. **RESPOSTAS.md** - Documento com respostas às questões do Paxos:
   - Item 0: Entender, Executar, Avaliar
   - Item 1: Como o backoff evita livelock
   - Item 2: Recuperação de decisões após falha

### Raft - Melhorias Implementadas

1. **run_benchmark.py** - Ajustes realizados:
   - Duração padrão alterada para 180 segundos (3 minutos) conforme enunciado
   - Adicionada função de distribuição cumulativa (CDF) de latências
   - Geração de gráficos CDF para cada rodada de teste
   - Coleta de todas as latências de todos os clientes para análise

2. **README.md** - Documentação atualizada:
   - Instruções atualizadas para Paxos MMC
   - Documentação dos novos scripts de teste
   - Instruções para gerar gráficos CDF

### Correções Técnicas

1. **Caracteres Unicode** - Removidos caracteres especiais que causavam erro no Windows:
   - Substituído ✓ por [OK]
   - Substituído ✗ por [FALHOU]

2. **Imports** - Corrigidos imports faltantes (random em teste_backoff.py)

3. **Testes** - Scripts testados e funcionando corretamente

## O que Foi Atendido

### Paxos
- [x] Sistema com múltiplos proposers e backoff
- [x] Opção de executar sem backoff (para demonstrar livelock)
- [x] Scripts para demonstrar backoff vs sem backoff com prints
- [x] Recuperação de decisões através de log persistente
- [x] Script para demonstrar falha e reinício de réplica
- [x] Documento de respostas às questões (RESPOSTAS.md)

### Raft
- [x] Duração padrão de 180 segundos nos experimentos
- [x] Função de distribuição cumulativa (CDF) de latências
- [x] Gráficos CDF gerados para cada rodada
- [x] CSV e gráfico principal (vazão x latência)

## O que Ainda Precisa Ser Feito

### Pendências (para o grupo)

1. **Paxos/RESPOSTAS.pdf**:
   - Converter RESPOSTAS.md para PDF
   - Adicionar nomes dos membros do grupo
   - Adicionar prints/logs das execuções como evidências
   - Colocar o PDF na pasta Paxos/

2. **Execução Completa dos Testes**:
   - Executar `python teste_backoff.py` e capturar saída completa
   - Executar `python teste_falha_recuperacao.py` e capturar saída completa
   - Incluir prints nas respostas do PDF

3. **Raft - Execução Completa**:
   - Executar `python run_benchmark.py --duracao 180 --cargas 1 2 3 4 6 8 10 12`
   - Aguardar todas as rodadas completarem (180s cada)
   - Verificar CSV e gráficos gerados
   - Verificar gráficos CDF gerados em cdf_latencia/

4. **Estrutura de Entrega**:
   - Criar pasta com nomes do grupo (conforme enunciado)
   - Organizar arquivos dentro de Paxos/ e Raft/
   - Incluir todos os códigos, logs e resultados

## Observações

- Todos os scripts foram testados e estão funcionando
- A implementação está completa conforme os requisitos do enunciado
- Os testes podem ser executados localmente para gerar evidências
- O sistema é didático mas demonstra os conceitos principais

## Como Testar

### Paxos
```bash
cd T2_SD_V1/Paxos
# Teste básico
python paxos_mmc.py

# Teste backoff vs sem backoff (item 1)
python teste_backoff.py

# Teste falha e recuperação (item 2)
python teste_falha_recuperacao.py
```

### Raft
```bash
cd T2_SD_V1/Raft
# Teste rápido (10 segundos por rodada)
python run_benchmark.py --duracao 10 --cargas 1 2 3

# Execução completa (180 segundos por rodada)
python run_benchmark.py --duracao 180 --cargas 1 2 3 4 6 8 10 12
```

