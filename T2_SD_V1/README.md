# Entrega – Sistemas Distribuídos (Paxos e Raft)

## Estrutura
```
entrega_sd/
├── Paxos/
│   └── paxos_example.py          # Exemplo didático de Paxos (linha a linha comentado)
├── Raft/
│   ├── raft_example.py           # Cluster Raft didático (Follower/Candidate/Leader) – comentado
│   ├── run_benchmark.py          # Benchmark de vazão x latência (reinicia cluster a cada rodada) – comentado
│   └── client_simulator.py       # Cliente gerador de carga – comentado
└── docs/
    ├── resultados_desempenho.csv # Resultados das execuções
    ├── grafico_vazao_latencia.png# Gráfico de desempenho (X=vazão, Y=latência)
    └── Relatorio_Raft_Benchmark.pdf
```

## Requisitos
- Python 3.9+
- `matplotlib` (para gráficos do benchmark): `pip install matplotlib`
- `reportlab` (para gerar o PDF do relatório): `pip install reportlab`

## Como executar (Raft)
1. Terminal na pasta `entrega_sd/Raft`.
2. Execute o benchmark (execução curta de exemplo):
   ```bash
   python run_benchmark.py --duracao 3 --cargas 1 2 3 4 6 8 10 12
   ```
   Saídas:
   - `resultados_desempenho.csv`
   - `grafico_vazao_latencia.png`

> **Conforme enunciado:** use **180 s** por carga e **reinicie o cluster a cada rodada** (o script já faz). Exemplo:
```bash
python run_benchmark.py --duracao 180 --cargas 1 2 3 4 6 8 10 12
```

## Metodologia (resumo)
- Cluster Raft didático com 3 nós.
- Para cada rodada (carga de N clientes concorrentes):
  - Reinicia o cluster.
  - Aguarda eleição do líder.
  - Executa por `--duracao` segundos.
  - Mede **vazão agregada** e **latência média**.
- Gera o gráfico com **eixo X = vazão (ops/s)** e **eixo Y = latência média (s)**.

## Como executar (Paxos – didático)
- Em `entrega_sd/Paxos/paxos_example.py`:
  ```bash
  python paxos_example.py
  ```
- Demonstra a dinâmica **prepare/promise** e **accept/accepted** com 5 acceptors.

## Observações
- Os códigos estão **comentados linha a linha** com marcadores `TODO` para que o grupo personalize as explicações das linhas mais relevantes.
- Para experimentos mais realistas, integrar I/O real (RPC/HTTP), logs persistentes e cenários de falha.
