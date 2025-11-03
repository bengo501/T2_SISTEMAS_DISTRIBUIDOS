# Entrega – Sistemas Distribuídos (Paxos e Raft)

## Estrutura
```
T2_SD_V1/
├── Paxos/
│   ├── paxos_example.py          # Exemplo didático básico de Paxos (linha a linha comentado)
│   ├── paxos_mmc.py              # Implementação Paxos MMC com backoff e recuperação
│   ├── teste_backoff.py          # Script para demonstrar backoff vs sem backoff (item 1)
│   ├── teste_falha_recuperacao.py # Script para demonstrar falha e recuperação (item 2)
│   └── RESPOSTAS.pdf             # Respostas às questões do Paxos
├── Raft/
│   ├── raft_example.py           # Cluster Raft didático (Follower/Candidate/Leader) – comentado
│   ├── run_benchmark.py          # Benchmark de vazão x latência (reinicia cluster a cada rodada) – comentado
│   └── client_simulator.py       # Cliente gerador de carga – comentado
└── docs/
    ├── resultados_desempenho.csv # Resultados das execuções
    ├── grafico_vazao_latencia.png# Gráfico de desempenho (X=vazão, Y=latência)
    ├── cdf_latencia/             # Gráficos CDF de latência por rodada
    └── Relatorio_Raft_Benchmark.pdf
```

## Requisitos
- Python 3.9+
- `matplotlib` (para gráficos do benchmark): `pip install matplotlib`
- `reportlab` (para gerar o PDF do relatório): `pip install reportlab`

## Como executar (Raft)
1. Terminal na pasta `T2_SD_V1/Raft`.
2. Execute o benchmark (duração padrão: 180s = 3min conforme enunciado):
   ```bash
   python run_benchmark.py --duracao 180 --cargas 1 2 3 4 6 8 10 12
   ```
   Saídas:
   - `resultados_desempenho.csv`
   - `grafico_vazao_latencia.png`
   - `cdf_latencia/cdf_latencia_N_clientes.png` (gráficos CDF por rodada)

Para execuções mais rápidas de teste:
```bash
python run_benchmark.py --duracao 10 --cargas 1 2 3
```

## Metodologia (resumo) - Raft
- Cluster Raft didático com 3 nós.
- Para cada rodada (carga de N clientes concorrentes):
  - Reinicia o cluster.
  - Aguarda eleição do líder.
  - Executa por `--duracao` segundos (padrão: 180s).
  - Mede **vazão agregada** e **latência média**.
  - Calcula **função de distribuição cumulativa (CDF)** de latências.
- Gera o gráfico com **eixo X = vazão (ops/s)** e **eixo Y = latência média (s)**.
- Gera gráficos CDF separados para cada nível de carga.

## Como executar (Paxos MMC)

### Item 1: Backoff e Livelock
Execute o script que compara execução sem backoff vs com backoff:
```bash
cd T2_SD_V1/Paxos
python teste_backoff.py
```
Este script demonstra:
- Execução sem backoff (pode causar livelock com múltiplos proposers competindo)
- Execução com backoff (evita livelock através de backoff exponencial)
- Envia comandos durante a avaliação para observar o comportamento

### Item 2: Falha e Recuperação
Execute o script que demonstra falha e reinício de réplica:
```bash
cd T2_SD_V1/Paxos
python teste_falha_recuperacao.py
```
Este script demonstra:
- Criação do sistema inicial e algumas decisões
- Falha de uma réplica (acceptor)
- Continuação do sistema com as réplicas restantes
- Recuperação do acceptor falho através do log persistente
- Sincronização do acceptor recuperado com o sistema

### Exemplo básico
Para executar o exemplo didático básico:
```bash
cd T2_SD_V1/Paxos
python paxos_example.py
```
Demonstra a dinâmica **prepare/promise** e **accept/accepted** com 5 acceptors.

### Implementação completa
Para usar o Paxos MMC completo com backoff e recuperação:
```bash
cd T2_SD_V1/Paxos
python paxos_mmc.py
```

## Observações
- Os códigos estão **comentados linha a linha** com comentários descritivos.
- **Paxos MMC**: Implementa sistema com múltiplos proposers, backoff exponencial para evitar livelock, e log persistente para recuperação de decisões após falhas.
- **Raft**: Cluster didático com eleição de líder, heartbeats, e medição de desempenho com CDF de latências.
- Para experimentos mais realistas, integrar I/O real (RPC/HTTP), rede distribuída, e cenários de falha mais complexos.
