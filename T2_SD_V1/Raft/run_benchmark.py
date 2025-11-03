# run_benchmark.py
"""
Benchmark automatizado (latência x vazão) para o cluster Raft didático,    # passo necessário na lógica do protocolo/benchmark
reiniciando o cluster a cada rodada (conforme enunciado).    # passo necessário na lógica do protocolo/benchmark

Uso:    # passo necessário na lógica do protocolo/benchmark
    python run_benchmark.py --duracao 3 --cargas 1 2 3 4 6 8 10 12    # passo necessário na lógica do protocolo/benchmark

Saídas:    # passo necessário na lógica do protocolo/benchmark
    - resultados_desempenho.csv    # passo necessário na lógica do protocolo/benchmark
    - grafico_vazao_latencia.png    # passo necessário na lógica do protocolo/benchmark
"""

import argparse    # passo necessário na lógica do protocolo/benchmark
import csv    # passo necessário na lógica do protocolo/benchmark
import time    # passo necessário na lógica do protocolo/benchmark
import random    # passo necessário na lógica do protocolo/benchmark
import threading    # cria thread para executar em concorrência com demais componentes
from pathlib import Path    # passo necessário na lógica do protocolo/benchmark

# Importa a classe Server do exemplo didático
from raft_example import Server    # passo necessário na lógica do protocolo/benchmark

# ----------------------------
# Cliente gerador de carga
# ----------------------------
class Client(threading.Thread):    # declara uma classe que modela este papel no protocolo
    def __init__(self, client_id, servers, duration_s=3):    # define uma função/método com a lógica correspondente
        super().__init__(daemon=True)    # passo necessário na lógica do protocolo/benchmark
        self.client_id = client_id    # passo necessário na lógica do protocolo/benchmark
        self.servers = servers    # passo necessário na lógica do protocolo/benchmark
        self.duration_s = duration_s    # passo necessário na lógica do protocolo/benchmark
        self.latencies = []    # passo necessário na lógica do protocolo/benchmark
        self.requests = 0    # passo necessário na lógica do protocolo/benchmark

    def run(self):    # define uma função/método com a lógica correspondente
        start = time.time()    # passo necessário na lógica do protocolo/benchmark
        while time.time() - start < self.duration_s:    # passo necessário na lógica do protocolo/benchmark
            leader = self._pick_leader()    # passo necessário na lógica do protocolo/benchmark
            t1 = time.time()    # passo necessário na lógica do protocolo/benchmark
            self._simulate_request(leader)    # passo necessário na lógica do protocolo/benchmark
            lat = time.time() - t1    # passo necessário na lógica do protocolo/benchmark
            self.latencies.append(lat)    # passo necessário na lógica do protocolo/benchmark
            self.requests += 1    # passo necessário na lógica do protocolo/benchmark
            time.sleep(0.01)    # simula atraso/tempo de processamento

    def _pick_leader(self):    # define uma função/método com a lógica correspondente
        # Escolhe o líder atual; se não houver (eleição), aguarda
        while True:    # passo necessário na lógica do protocolo/benchmark
            leaders = [s for s in self.servers if s.state == Server.LEADER]    # inicia um desvio condicional para tratar este caso
            if leaders:    # inicia um desvio condicional para tratar este caso
                return random.choice(leaders)    # retorna o valor computado para o chamador
            time.sleep(0.01)    # simula atraso/tempo de processamento

    def _simulate_request(self, leader):    # define uma função/método com a lógica correspondente
        # Simula processamento didático (em um Raft real seria RPC ao líder)
        time.sleep(random.uniform(0.003, 0.01))    # simula atraso/tempo de processamento


# ----------------------------
# Execução de uma rodada (cluster reiniciado)
# ----------------------------
def run_round_with_restart(n_clients, duration_s, n_servers=3):    # define uma função/método com a lógica correspondente
    servers = [Server(i, []) for i in range(n_servers)]    # itera sobre a coleção para aplicar a ação a cada elemento
    for s in servers:    # itera sobre a coleção para aplicar a ação a cada elemento
        s.cluster = servers    # passo necessário na lógica do protocolo/benchmark
        s.start()    # inicializa execução assíncrona (thread/servidor)
    # Aguarda eleição inicial
    time.sleep(1.0)    # simula atraso/tempo de processamento

    try:    # passo necessário na lógica do protocolo/benchmark
        clients = [Client(i, servers, duration_s) for i in range(n_clients)]    # itera sobre a coleção para aplicar a ação a cada elemento
        for c in clients:    # itera sobre a coleção para aplicar a ação a cada elemento
            c.start()    # inicializa execução assíncrona (thread/servidor)
        for c in clients:    # itera sobre a coleção para aplicar a ação a cada elemento
            c.join()    # aguarda conclusão da thread antes de seguir

        # coleta todas as latências de todos os clientes
        all_latencies = []    # passo necessário na lógica do protocolo/benchmark
        for c in clients:    # itera sobre a coleção para aplicar a ação a cada elemento
            all_latencies.extend(c.latencies)    # passo necessário na lógica do protocolo/benchmark
        
        total_reqs = sum(c.requests for c in clients)    # itera sobre a coleção para aplicar a ação a cada elemento
        total_time = duration_s    # passo necessário na lógica do protocolo/benchmark
        throughput = total_reqs / total_time    # passo necessário na lógica do protocolo/benchmark
        avg_latency = sum(all_latencies) / len(all_latencies) if all_latencies else 0.0    # inicia um desvio condicional para tratar este caso
        return throughput, avg_latency, all_latencies    # retorna o valor computado para o chamador
    finally:    # passo necessário na lógica do protocolo/benchmark
        # Encerra cluster desta rodada
        for s in servers:    # itera sobre a coleção para aplicar a ação a cada elemento
            s.stop_event.set()    # sinaliza término ordenado do componente
        time.sleep(0.2)    # simula atraso/tempo de processamento


def calcular_cdf(latencies):    # define uma função/método com a lógica correspondente
    """calcula função de distribuição cumulativa (cdf) de latências"""    # passo necessário na lógica do protocolo/benchmark
    if not latencies:    # inicia um desvio condicional para tratar este caso
        return [], []    # retorna o valor computado para o chamador
    
    sorted_latencies = sorted(latencies)    # passo necessário na lógica do protocolo/benchmark
    n = len(sorted_latencies)    # passo necessário na lógica do protocolo/benchmark
    cumulative = [(i + 1) / n for i in range(n)]    # passo necessário na lógica do protocolo/benchmark
    return sorted_latencies, cumulative    # retorna o valor computado para o chamador

def main():    # define uma função/método com a lógica correspondente
    parser = argparse.ArgumentParser()    # passo necessário na lógica do protocolo/benchmark
    parser.add_argument("--duracao", type=int, default=180, help="Duração (s) de cada execução/rodada (padrão: 180s = 3min)")    # passo necessário na lógica do protocolo/benchmark
    parser.add_argument("--cargas", type=int, nargs="+", default=[1,2,3,4,6,8,10,12], help="Lista de números de clientes")    # passo necessário na lógica do protocolo/benchmark
    parser.add_argument("--out_csv", type=Path, default=Path("resultados_desempenho.csv"))    # passo necessário na lógica do protocolo/benchmark
    parser.add_argument("--out_png", type=Path, default=Path("grafico_vazao_latencia.png"))    # passo necessário na lógica do protocolo/benchmark
    parser.add_argument("--out_cdf_dir", type=Path, default=Path("cdf_latencia"), help="Diretório para salvar gráficos CDF")    # passo necessário na lógica do protocolo/benchmark
    args = parser.parse_args()    # passo necessário na lógica do protocolo/benchmark

    # cria diretório para CDFs se não existir
    args.out_cdf_dir.mkdir(exist_ok=True)    # passo necessário na lógica do protocolo/benchmark

    resultados = []    # passo necessário na lógica do protocolo/benchmark
    all_latencies_per_round = []    # passo necessário na lógica do protocolo/benchmark
    
    for n in args.cargas:    # itera sobre a coleção para aplicar a ação a cada elemento
        print(f"[rodada] reiniciando cluster | {n} clientes por {args.duracao}s")    # gera saída no console para observação do estado
        thr, lat, latencies = run_round_with_restart(n, args.duracao, n_servers=3)    # passo necessário na lógica do protocolo/benchmark
        resultados.append((n, thr, lat))    # passo necessário na lógica do protocolo/benchmark
        all_latencies_per_round.append((n, latencies))    # passo necessário na lógica do protocolo/benchmark
        print(f" -> vazão={thr:.2f} ops/s | latência média={lat:.4f}s | amostras={len(latencies)}")    # gera saída no console para observação do estado

    # salva csv
    with args.out_csv.open("w", newline="") as f:    # passo necessário na lógica do protocolo/benchmark
        w = csv.writer(f)    # registra métricas em CSV para posterior análise
        w.writerow(["nro_clientes", "vazao", "latencia_media"])    # registra métricas em CSV para posterior análise
        for n, thr, lat in resultados:    # itera sobre a coleção para aplicar a ação a cada elemento
            w.writerow([n, thr, lat])    # registra métricas em CSV para posterior análise

    # gera gráfico principal (x=vazão, y=latência)
    try:    # passo necessário na lógica do protocolo/benchmark
        import matplotlib.pyplot as plt    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
        xs = [thr for _, thr, _ in resultados]    # itera sobre a coleção para aplicar a ação a cada elemento
        ys = [lat for _, _, lat in resultados]    # itera sobre a coleção para aplicar a ação a cada elemento
        plt.figure(figsize=(10, 6))    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
        plt.scatter(xs, ys, s=100, alpha=0.6)    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
        plt.plot(xs, ys, 'b-', alpha=0.3)    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
        plt.xlabel("Vazão (ops/s)")    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
        plt.ylabel("Latência média (s)")    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
        plt.title("Desempenho Raft (didático): Vazão x Latência (cluster reiniciado por rodada)")    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
        plt.grid(True, alpha=0.3)    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
        plt.savefig(args.out_png, dpi=140, bbox_inches="tight")    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
        print(f"gráfico principal salvo em: {args.out_png}")    # gera saída no console para observação do estado
        plt.close()    # passo necessário na lógica do protocolo/benchmark
        
        # gera gráficos CDF para cada rodada
        print(f"gerando gráficos CDF de latência para cada rodada...")    # gera saída no console para observação do estado
        for n, latencies in all_latencies_per_round:    # itera sobre a coleção para aplicar a ação a cada elemento
            if not latencies:    # inicia um desvio condicional para tratar este caso
                continue    # passo necessário na lógica do protocolo/benchmark
            
            sorted_lat, cumulative = calcular_cdf(latencies)    # passo necessário na lógica do protocolo/benchmark
            
            plt.figure(figsize=(10, 6))    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
            plt.plot(sorted_lat, cumulative, 'b-', linewidth=2)    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
            plt.xlabel("Latência (s)")    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
            plt.ylabel("Probabilidade cumulativa")    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
            plt.title(f"CDF de Latência - {n} clientes (duração: {args.duracao}s)")    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
            plt.grid(True, alpha=0.3)    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
            plt.xlim(0, max(sorted_lat) * 1.1 if sorted_lat else 1)    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
            plt.ylim(0, 1)    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
            
            cdf_file = args.out_cdf_dir / f"cdf_latencia_{n}_clientes.png"    # passo necessário na lógica do protocolo/benchmark
            plt.savefig(cdf_file, dpi=140, bbox_inches="tight")    # gera o gráfico X=Vazão, Y=Latência conforme o enunciado
            plt.close()    # passo necessário na lógica do protocolo/benchmark
            print(f"  cdf salvo: {cdf_file}")    # gera saída no console para observação do estado
        
    except Exception as e:    # passo necessário na lógica do protocolo/benchmark
        print("falha ao gerar gráfico:", e)    # gera saída no console para observação do estado

if __name__ == "__main__":    # inicia um desvio condicional para tratar este caso
    main()    # passo necessário na lógica do protocolo/benchmark
