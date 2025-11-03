# raft_example.py
# Simulação educacional simples do algoritmo Raft

import random    # passo necessário na lógica do protocolo/benchmark
import time    # passo necessário na lógica do protocolo/benchmark
from threading import Thread, Event    # cria thread para executar em concorrência com demais componentes

class Server:    # declara uma classe que modela este papel no protocolo
    FOLLOWER = 'Follower'    # passo necessário na lógica do protocolo/benchmark
    CANDIDATE = 'Candidate'    # passo necessário na lógica do protocolo/benchmark
    LEADER = 'Leader'    # passo necessário na lógica do protocolo/benchmark

    def __init__(self, server_id, cluster):    # define uma função/método com a lógica correspondente
        self.id = server_id    # passo necessário na lógica do protocolo/benchmark
        self.cluster = cluster    # passo necessário na lógica do protocolo/benchmark
        self.state = Server.FOLLOWER    # atualiza o estado do servidor conforme o papel atual no Raft
        self.term = 0    # atualiza o termo (era) do Raft para refletir nova eleição/heartbeat
        self.voted_for = None    # passo necessário na lógica do protocolo/benchmark
        self.votes_received = 0    # verifica maioria/quórum para prosseguir na decisão
        self.election_timeout = random.uniform(1.0, 2.0)    # usa aleatoriedade para evitar sincronização/livelock e simular variabilidade
        self.last_heartbeat = time.time()    # passo necessário na lógica do protocolo/benchmark
        self.stop_event = Event()    # sinaliza término ordenado do componente

    def start(self):    # define uma função/método com a lógica correspondente
        Thread(target=self.run, daemon=True).start()    # cria thread para executar em concorrência com demais componentes

    def run(self):    # define uma função/método com a lógica correspondente
        while not self.stop_event.is_set():    # sinaliza término ordenado do componente
            time.sleep(0.1)    # simula atraso/tempo de processamento
            if self.state == Server.FOLLOWER:    # inicia um desvio condicional para tratar este caso
                if time.time() - self.last_heartbeat > self.election_timeout:    # inicia um desvio condicional para tratar este caso
                    print(f"Server {self.id} timeout. Becoming candidate.")    # gera saída no console para observação do estado
                    self.start_election()    # passo necessário na lógica do protocolo/benchmark
            elif self.state == Server.CANDIDATE:    # inicia um desvio condicional para tratar este caso
                pass  # election handled in start_election    # passo necessário na lógica do protocolo/benchmark
            elif self.state == Server.LEADER:    # inicia um desvio condicional para tratar este caso
                self.send_heartbeats()    # envia/recebe heartbeats para manter liderança e resetar timeout
                time.sleep(0.3)    # simula atraso/tempo de processamento

    def start_election(self):    # define uma função/método com a lógica correspondente
        self.state = Server.CANDIDATE    # atualiza o estado do servidor conforme o papel atual no Raft
        self.term += 1    # atualiza o termo (era) do Raft para refletir nova eleição/heartbeat
        self.voted_for = self.id    # passo necessário na lógica do protocolo/benchmark
        self.votes_received = 1    # verifica maioria/quórum para prosseguir na decisão
        print(f"Server {self.id} starts election for term {self.term}")    # gera saída no console para observação do estado
        for peer in self.cluster:    # itera sobre a coleção para aplicar a ação a cada elemento
            if peer.id != self.id:    # inicia um desvio condicional para tratar este caso
                if peer.request_vote(self.term, self.id):    # inicia um desvio condicional para tratar este caso
                    self.votes_received += 1    # verifica maioria/quórum para prosseguir na decisão
        if self.votes_received > len(self.cluster) // 2:    # inicia um desvio condicional para tratar este caso
            print(f"Server {self.id} becomes leader for term {self.term}")    # gera saída no console para observação do estado
            self.state = Server.LEADER    # atualiza o estado do servidor conforme o papel atual no Raft
            self.send_heartbeats()    # envia/recebe heartbeats para manter liderança e resetar timeout
        else:    # trata casos alternativos do fluxo condicional
            print(f"Server {self.id} failed to win election")    # gera saída no console para observação do estado

    def request_vote(self, term, candidate_id):    # define uma função/método com a lógica correspondente
        if term > self.term and (self.voted_for is None or self.voted_for == candidate_id):    # inicia um desvio condicional para tratar este caso
            self.term = term    # atualiza o termo (era) do Raft para refletir nova eleição/heartbeat
            self.voted_for = candidate_id    # passo necessário na lógica do protocolo/benchmark
            print(f"Server {self.id} votes for {candidate_id} in term {term}")    # itera sobre a coleção para aplicar a ação a cada elemento
            return True    # retorna o valor computado para o chamador
        return False    # retorna o valor computado para o chamador

    def send_heartbeats(self):    # define uma função/método com a lógica correspondente
        print(f"Leader {self.id} sending heartbeats...")    # gera saída no console para observação do estado
        self.last_heartbeat = time.time()    # passo necessário na lógica do protocolo/benchmark
        for peer in self.cluster:    # itera sobre a coleção para aplicar a ação a cada elemento
            if peer.id != self.id:    # inicia um desvio condicional para tratar este caso
                peer.receive_heartbeat(self.term, self.id)    # envia/recebe heartbeats para manter liderança e resetar timeout

    def receive_heartbeat(self, term, leader_id):    # define uma função/método com a lógica correspondente
        if term >= self.term:    # inicia um desvio condicional para tratar este caso
            self.term = term    # atualiza o termo (era) do Raft para refletir nova eleição/heartbeat
            self.state = Server.FOLLOWER    # atualiza o estado do servidor conforme o papel atual no Raft
            self.voted_for = leader_id    # passo necessário na lógica do protocolo/benchmark
            self.last_heartbeat = time.time()    # passo necessário na lógica do protocolo/benchmark
            print(f"Server {self.id} received heartbeat from leader {leader_id}")    # gera saída no console para observação do estado

if __name__ == "__main__":    # inicia um desvio condicional para tratar este caso
    servers = [Server(i, []) for i in range(3)]    # itera sobre a coleção para aplicar a ação a cada elemento
    for s in servers:    # itera sobre a coleção para aplicar a ação a cada elemento
        s.cluster = servers    # passo necessário na lógica do protocolo/benchmark
        s.start()    # inicializa execução assíncrona (thread/servidor)

    time.sleep(10)    # simula atraso/tempo de processamento
    for s in servers:    # itera sobre a coleção para aplicar a ação a cada elemento
        s.stop_event.set()    # sinaliza término ordenado do componente
