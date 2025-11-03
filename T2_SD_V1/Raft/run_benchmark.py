# run_benchmark.py
"""
Benchmark automatizado (latência x vazão) para o cluster Raft didático,
reiniciando o cluster a cada rodada (conforme enunciado).

Uso:
    python run_benchmark.py --duracao 180 --cargas 1 2 3 4 6 8 10 12

Saídas:
    - resultados_desempenho.csv
    - grafico_vazao_latencia.png
    - cdf_latencia/cdf_latencia_N_clientes.png
"""

import argparse
import csv
import time
import random
import threading
from pathlib import Path

from raft_example import Server

class Client(threading.Thread):
    def __init__(self, client_id, servers, duration_s=3):
        super().__init__(daemon=True)
        self.client_id = client_id
        self.servers = servers
        self.duration_s = duration_s
        self.latencies = []
        self.requests = 0

    def run(self):
        start = time.time()
        while time.time() - start < self.duration_s:
            leader = self._pick_leader()
            t1 = time.time()
            self._simulate_request(leader)
            lat = time.time() - t1
            self.latencies.append(lat)
            self.requests += 1
            time.sleep(0.01)

    def _pick_leader(self):
        while True:
            leaders = [s for s in self.servers if s.state == Server.LEADER]
            if leaders:
                return random.choice(leaders)
            time.sleep(0.01)

    def _simulate_request(self, leader):
        time.sleep(random.uniform(0.003, 0.01))

def run_round_with_restart(n_clients, duration_s, n_servers=3):
    servers = [Server(i, []) for i in range(n_servers)]
    for s in servers:
        s.cluster = servers
        s.start()
    time.sleep(1.0)

    try:
        clients = [Client(i, servers, duration_s) for i in range(n_clients)]
        for c in clients:
            c.start()
        for c in clients:
            c.join()

        all_latencies = []
        for c in clients:
            all_latencies.extend(c.latencies)
        
        total_reqs = sum(c.requests for c in clients)
        total_time = duration_s
        throughput = total_reqs / total_time
        avg_latency = sum(all_latencies) / len(all_latencies) if all_latencies else 0.0
        return throughput, avg_latency, all_latencies
    finally:
        for s in servers:
            s.stop_event.set()
        time.sleep(0.2)

def calcular_cdf(latencies):
    """calcula função de distribuição cumulativa (cdf) de latências"""
    if not latencies:
        return [], []
    
    sorted_latencies = sorted(latencies)
    n = len(sorted_latencies)
    cumulative = [(i + 1) / n for i in range(n)]
    return sorted_latencies, cumulative

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--duracao", type=int, default=180, help="Duração (s) de cada execução/rodada (padrão: 180s = 3min)")
    parser.add_argument("--cargas", type=int, nargs="+", default=[1,2,3,4,6,8,10,12], help="Lista de números de clientes")
    parser.add_argument("--out_csv", type=Path, default=Path("resultados_desempenho.csv"))
    parser.add_argument("--out_png", type=Path, default=Path("grafico_vazao_latencia.png"))
    parser.add_argument("--out_cdf_dir", type=Path, default=Path("cdf_latencia"), help="Diretório para salvar gráficos CDF")
    args = parser.parse_args()

    args.out_cdf_dir.mkdir(exist_ok=True)

    resultados = []
    all_latencies_per_round = []
    
    for n in args.cargas:
        print(f"[rodada] reiniciando cluster | {n} clientes por {args.duracao}s")
        thr, lat, latencies = run_round_with_restart(n, args.duracao, n_servers=3)
        resultados.append((n, thr, lat))
        all_latencies_per_round.append((n, latencies))
        print(f" -> vazão={thr:.2f} ops/s | latência média={lat:.4f}s | amostras={len(latencies)}")

    with args.out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["nro_clientes", "vazao", "latencia_media"])
        for n, thr, lat in resultados:
            w.writerow([n, thr, lat])

    try:
        import matplotlib.pyplot as plt
        xs = [thr for _, thr, _ in resultados]
        ys = [lat for _, _, lat in resultados]
        plt.figure(figsize=(10, 6))
        plt.scatter(xs, ys, s=100, alpha=0.6)
        plt.plot(xs, ys, 'b-', alpha=0.3)
        plt.xlabel("Vazão (ops/s)")
        plt.ylabel("Latência média (s)")
        plt.title("Desempenho Raft (didático): Vazão x Latência (cluster reiniciado por rodada)")
        plt.grid(True, alpha=0.3)
        plt.savefig(args.out_png, dpi=140, bbox_inches="tight")
        print(f"gráfico principal salvo em: {args.out_png}")
        plt.close()
        
        print(f"gerando gráficos CDF de latência para cada rodada...")
        for n, latencies in all_latencies_per_round:
            if not latencies:
                continue
            
            sorted_lat, cumulative = calcular_cdf(latencies)
            
            plt.figure(figsize=(10, 6))
            plt.plot(sorted_lat, cumulative, 'b-', linewidth=2)
            plt.xlabel("Latência (s)")
            plt.ylabel("Probabilidade cumulativa")
            plt.title(f"CDF de Latência - {n} clientes (duração: {args.duracao}s)")
            plt.grid(True, alpha=0.3)
            plt.xlim(0, max(sorted_lat) * 1.1 if sorted_lat else 1)
            plt.ylim(0, 1)
            
            cdf_file = args.out_cdf_dir / f"cdf_latencia_{n}_clientes.png"
            plt.savefig(cdf_file, dpi=140, bbox_inches="tight")
            plt.close()
            print(f"  cdf salvo: {cdf_file}")
        
    except Exception as e:
        print("falha ao gerar gráfico:", e)

if __name__ == "__main__":
    main()
