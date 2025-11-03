# client_simulator.py
# Cliente para medir desempenho de operações em um cluster Raft simulado

import time    # passo necessário na lógica do protocolo/benchmark
import threading    # cria thread para executar em concorrência com demais componentes
import random    # passo necessário na lógica do protocolo/benchmark
import requests    # passo necessário na lógica do protocolo/benchmark

class ClientSimulator:    # declara uma classe que modela este papel no protocolo
    def __init__(self, client_id, cluster, duration=10):    # define uma função/método com a lógica correspondente
        self.client_id = client_id    # passo necessário na lógica do protocolo/benchmark
        self.cluster = cluster    # passo necessário na lógica do protocolo/benchmark
        self.duration = duration    # passo necessário na lógica do protocolo/benchmark
        self.latencies = []    # passo necessário na lógica do protocolo/benchmark
        self.total_requests = 0    # passo necessário na lógica do protocolo/benchmark

    def run(self):    # define uma função/método com a lógica correspondente
        print(f"Client {self.client_id} started for {self.duration}s")    # gera saída no console para observação do estado
        start_time = time.time()    # passo necessário na lógica do protocolo/benchmark
        while time.time() - start_time < self.duration:    # passo necessário na lógica do protocolo/benchmark
            target = random.choice(self.cluster)    # usa aleatoriedade para evitar sincronização/livelock e simular variabilidade
            timestamp1 = time.time()    # passo necessário na lógica do protocolo/benchmark
            response = self.send_request(target)    # passo necessário na lógica do protocolo/benchmark
            latency = time.time() - timestamp1    # passo necessário na lógica do protocolo/benchmark
            if response:    # inicia um desvio condicional para tratar este caso
                self.latencies.append(latency)    # passo necessário na lógica do protocolo/benchmark
                self.total_requests += 1    # passo necessário na lógica do protocolo/benchmark
            time.sleep(0.05)  # controlar taxa de envio    # simula atraso/tempo de processamento

        total_time = time.time() - start_time    # passo necessário na lógica do protocolo/benchmark
        throughput = self.total_requests / total_time    # passo necessário na lógica do protocolo/benchmark
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0    # inicia um desvio condicional para tratar este caso

        print(f"Client {self.client_id} finished.")    # gera saída no console para observação do estado
        print(f"Total requests: {self.total_requests}")    # gera saída no console para observação do estado
        print(f"Throughput: {throughput:.2f} ops/sec")    # gera saída no console para observação do estado
        print(f"Average latency: {avg_latency:.4f} sec")    # gera saída no console para observação do estado

    def send_request(self, target):    # define uma função/método com a lógica correspondente
        # Simulação de envio: aqui apenas espera o 'leader' processar
        try:    # passo necessário na lógica do protocolo/benchmark
            # em um sistema real, aqui faríamos uma chamada HTTP, por exemplo
            time.sleep(random.uniform(0.01, 0.03))  # simula tempo de processamento    # simula atraso/tempo de processamento
            return True    # retorna o valor computado para o chamador
        except Exception:    # passo necessário na lógica do protocolo/benchmark
            return False    # retorna o valor computado para o chamador

if __name__ == "__main__":    # inicia um desvio condicional para tratar este caso
    cluster_simulado = ["Leader-0", "Follower-1", "Follower-2"]    # passo necessário na lógica do protocolo/benchmark
    clientes = [ClientSimulator(i, cluster_simulado, duration=5) for i in range(3)]    # itera sobre a coleção para aplicar a ação a cada elemento
    threads = [threading.Thread(target=c.run) for c in clientes]    # itera sobre a coleção para aplicar a ação a cada elemento

    for t in threads:    # itera sobre a coleção para aplicar a ação a cada elemento
        t.start()    # inicializa execução assíncrona (thread/servidor)
    for t in threads:    # itera sobre a coleção para aplicar a ação a cada elemento
        t.join()    # aguarda conclusão da thread antes de seguir
