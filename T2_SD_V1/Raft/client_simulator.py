# client_simulator.py
# Cliente para medir desempenho de operações em um cluster Raft simulado

import time
import threading
import random

class ClientSimulator:
    def __init__(self, client_id, cluster, duration=10):
        self.client_id = client_id
        self.cluster = cluster
        self.duration = duration
        self.latencies = []
        self.total_requests = 0

    def run(self):
        print(f"Client {self.client_id} started for {self.duration}s")
        start_time = time.time()
        while time.time() - start_time < self.duration:
            target = random.choice(self.cluster)
            timestamp1 = time.time()
            response = self.send_request(target)
            latency = time.time() - timestamp1
            if response:
                self.latencies.append(latency)
                self.total_requests += 1
            time.sleep(0.05)

        total_time = time.time() - start_time
        throughput = self.total_requests / total_time
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0

        print(f"Client {self.client_id} finished.")
        print(f"Total requests: {self.total_requests}")
        print(f"Throughput: {throughput:.2f} ops/sec")
        print(f"Average latency: {avg_latency:.4f} sec")

    def send_request(self, target):
        try:
            time.sleep(random.uniform(0.01, 0.03))
            return True
        except Exception:
            return False

if __name__ == "__main__":
    cluster_simulado = ["Leader-0", "Follower-1", "Follower-2"]
    clientes = [ClientSimulator(i, cluster_simulado, duration=5) for i in range(3)]
    threads = [threading.Thread(target=c.run) for c in clientes]

    for t in threads:
        t.start()
    for t in threads:
        t.join()
