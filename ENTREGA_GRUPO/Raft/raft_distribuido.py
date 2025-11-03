# raft_distribuido.py
# Versão distribuída do Raft usando HTTP para comunicação entre nós
# Permite executar nós em máquinas/hosts diferentes

import random    # passo necessário na lógica do protocolo/benchmark
import time    # passo necessário na lógica do protocolo/benchmark
import threading    # cria thread para executar em concorrência com demais componentes
import json    # passo necessário na lógica do protocolo/benchmark
from http.server import HTTPServer, BaseHTTPRequestHandler    # passo necessário na lógica do protocolo/benchmark
from urllib.parse import urlparse, parse_qs    # passo necessário na lógica do protocolo/benchmark
from urllib.request import urlopen, Request    # passo necessário na lógica do protocolo/benchmark
from urllib.error import URLError    # passo necessário na lógica do protocolo/benchmark
import argparse    # passo necessário na lógica do protocolo/benchmark

class Server:    # declara uma classe que modela este papel no protocolo
    FOLLOWER = 'Follower'    # passo necessário na lógica do protocolo/benchmark
    CANDIDATE = 'Candidate'    # passo necessário na lógica do protocolo/benchmark
    LEADER = 'Leader'    # passo necessário na lógica do protocolo/benchmark

    def __init__(self, server_id, host, port, peers):    # define uma função/método com a lógica correspondente
        self.id = server_id    # passo necessário na lógica do protocolo/benchmark
        self.host = host    # passo necessário na lógica do protocolo/benchmark
        self.port = port    # passo necessário na lógica do protocolo/benchmark
        self.peers = peers    # passo necessário na lógica do protocolo/benchmark
        self.state = Server.FOLLOWER    # atualiza o estado do servidor conforme o papel atual no Raft
        self.term = 0    # atualiza o termo (era) do Raft para refletir nova eleição/heartbeat
        self.voted_for = None    # passo necessário na lógica do protocolo/benchmark
        self.votes_received = 0    # verifica maioria/quórum para prosseguir na decisão
        self.election_timeout = random.uniform(1.0, 2.0)    # usa aleatoriedade para evitar sincronização/livelock e simular variabilidade
        self.last_heartbeat = time.time()    # passo necessário na lógica do protocolo/benchmark
        self.stop_event = threading.Event()    # sinaliza término ordenado do componente
        self.server = None    # passo necessário na lógica do protocolo/benchmark

    def start_http_server(self):    # define uma função/método com a lógica correspondente
        class RaftHandler(BaseHTTPRequestHandler):    # declara uma classe que modela este papel no protocolo
            def __init__(self, raft_server):    # define uma função/método com a lógica correspondente
                self.raft_server = raft_server    # passo necessário na lógica do protocolo/benchmark

            def do_GET(self):    # define uma função/método com a lógica correspondente
                if self.path == '/status':    # inicia um desvio condicional para tratar este caso
                    self.send_response(200)    # passo necessário na lógica do protocolo/benchmark
                    self.send_header('Content-Type', 'application/json')    # passo necessário na lógica do protocolo/benchmark
                    self.end_headers()    # passo necessário na lógica do protocolo/benchmark
                    status = {    # passo necessário na lógica do protocolo/benchmark
                        'id': self.raft_server.id,    # passo necessário na lógica do protocolo/benchmark
                        'state': self.raft_server.state,    # passo necessário na lógica do protocolo/benchmark
                        'term': self.raft_server.term,    # passo necessário na lógica do protocolo/benchmark
                        'voted_for': self.raft_server.voted_for    # passo necessário na lógica do protocolo/benchmark
                    }    # passo necessário na lógica do protocolo/benchmark
                    self.wfile.write(json.dumps(status).encode())    # passo necessário na lógica do protocolo/benchmark

            def do_POST(self):    # define uma função/método com a lógica correspondente
                content_length = int(self.headers['Content-Length'])    # passo necessário na lógica do protocolo/benchmark
                body = self.rfile.read(content_length).decode()    # passo necessário na lógica do protocolo/benchmark
                data = json.loads(body)    # passo necessário na lógica do protocolo/benchmark
                
                if self.path == '/request_vote':    # inicia um desvio condicional para tratar este caso
                    result = self.raft_server.request_vote(data['term'], data['candidate_id'])    # passo necessário na lógica do protocolo/benchmark
                    self.send_response(200)    # passo necessário na lógica do protocolo/benchmark
                    self.send_header('Content-Type', 'application/json')    # passo necessário na lógica do protocolo/benchmark
                    self.end_headers()    # passo necessário na lógica do protocolo/benchmark
                    self.wfile.write(json.dumps({'vote_granted': result, 'term': self.raft_server.term}).encode())    # passo necessário na lógica do protocolo/benchmark
                elif self.path == '/heartbeat':    # inicia um desvio condicional para tratar este caso
                    self.raft_server.receive_heartbeat(data['term'], data['leader_id'])    # passo necessário na lógica do protocolo/benchmark
                    self.send_response(200)    # passo necessário na lógica do protocolo/benchmark
                    self.send_header('Content-Type', 'application/json')    # passo necessário na lógica do protocolo/benchmark
                    self.end_headers()    # passo necessário na lógica do protocolo/benchmark
                    self.wfile.write(json.dumps({'success': True, 'term': self.raft_server.term}).encode())    # passo necessário na lógica do protocolo/benchmark

            def log_message(self, format, *args):    # define uma função/método com a lógica correspondente
                pass    # suprime logs do http server    # passo necessário na lógica do protocolo/benchmark

        handler = lambda *args, **kwargs: RaftHandler(self)(*args, **kwargs)    # passo necessário na lógica do protocolo/benchmark
        self.server = HTTPServer((self.host, self.port), handler)    # passo necessário na lógica do protocolo/benchmark
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)    # cria thread para executar em concorrência com demais componentes
        thread.start()    # inicializa execução assíncrona (thread/servidor)

    def start(self):    # define uma função/método com a lógica correspondente
        self.start_http_server()    # passo necessário na lógica do protocolo/benchmark
        threading.Thread(target=self.run, daemon=True).start()    # cria thread para executar em concorrência com demais componentes

    def run(self):    # define uma função/método com a lógica correspondente
        while not self.stop_event.is_set():    # sinaliza término ordenado do componente
            time.sleep(0.1)    # simula atraso/tempo de processamento
            if self.state == Server.FOLLOWER:    # inicia um desvio condicional para tratar este caso
                if time.time() - self.last_heartbeat > self.election_timeout:    # inicia um desvio condicional para tratar este caso
                    print(f"[server {self.id}] timeout. tornando-se candidato.")    # gera saída no console para observação do estado
                    self.start_election()    # passo necessário na lógica do protocolo/benchmark
            elif self.state == Server.LEADER:    # inicia um desvio condicional para tratar este caso
                self.send_heartbeats()    # envia/recebe heartbeats para manter liderança e resetar timeout
                time.sleep(0.3)    # simula atraso/tempo de processamento

    def start_election(self):    # define uma função/método com a lógica correspondente
        self.state = Server.CANDIDATE    # atualiza o estado do servidor conforme o papel atual no Raft
        self.term += 1    # atualiza o termo (era) do Raft para refletir nova eleição/heartbeat
        self.voted_for = self.id    # passo necessário na lógica do protocolo/benchmark
        self.votes_received = 1    # verifica maioria/quórum para prosseguir na decisão
        print(f"[server {self.id}] inicia eleição para termo {self.term}")    # gera saída no console para observação do estado
        
        # solicita votos dos peers via http
        for peer_url in self.peers:    # itera sobre a coleção para aplicar a ação a cada elemento
            try:    # passo necessário na lógica do protocolo/benchmark
                request = Request(f"{peer_url}/request_vote",    # passo necessário na lógica do protocolo/benchmark
                                data=json.dumps({'term': self.term, 'candidate_id': self.id}).encode(),    # passo necessário na lógica do protocolo/benchmark
                                headers={'Content-Type': 'application/json'})    # passo necessário na lógica do protocolo/benchmark
                with urlopen(request, timeout=0.5) as response:    # passo necessário na lógica do protocolo/benchmark
                    result = json.loads(response.read().decode())    # passo necessário na lógica do protocolo/benchmark
                    if result.get('vote_granted'):    # inicia um desvio condicional para tratar este caso
                        self.votes_received += 1    # verifica maioria/quórum para prosseguir na decisão
                        print(f"[server {self.id}] recebeu voto de {peer_url}")    # gera saída no console para observação do estado
            except (URLError, Exception) as e:    # passo necessário na lógica do protocolo/benchmark
                print(f"[server {self.id}] erro ao solicitar voto de {peer_url}: {e}")    # gera saída no console para observação do estado
        
        total_servers = len(self.peers) + 1    # inclui este servidor    # passo necessário na lógica do protocolo/benchmark
        if self.votes_received > total_servers // 2:    # inicia um desvio condicional para tratar este caso
            print(f"[server {self.id}] torna-se líder para termo {self.term}")    # gera saída no console para observação do estado
            self.state = Server.LEADER    # atualiza o estado do servidor conforme o papel atual no Raft
            self.send_heartbeats()    # envia/recebe heartbeats para manter liderança e resetar timeout
        else:    # trata casos alternativos do fluxo condicional
            print(f"[server {self.id}] falhou na eleição (recebeu {self.votes_received} votos de {total_servers})")    # gera saída no console para observação do estado

    def request_vote(self, term, candidate_id):    # define uma função/método com a lógica correspondente
        if term > self.term and (self.voted_for is None or self.voted_for == candidate_id):    # inicia um desvio condicional para tratar este caso
            self.term = term    # atualiza o termo (era) do Raft para refletir nova eleição/heartbeat
            self.voted_for = candidate_id    # passo necessário na lógica do protocolo/benchmark
            print(f"[server {self.id}] vota para {candidate_id} no termo {term}")    # gera saída no console para observação do estado
            return True    # retorna o valor computado para o chamador
        return False    # retorna o valor computado para o chamador

    def send_heartbeats(self):    # define uma função/método com a lógica correspondente
        print(f"[líder {self.id}] enviando heartbeats...")    # gera saída no console para observação do estado
        self.last_heartbeat = time.time()    # passo necessário na lógica do protocolo/benchmark
        for peer_url in self.peers:    # itera sobre a coleção para aplicar a ação a cada elemento
            try:    # passo necessário na lógica do protocolo/benchmark
                request = Request(f"{peer_url}/heartbeat",    # passo necessário na lógica do protocolo/benchmark
                                data=json.dumps({'term': self.term, 'leader_id': self.id}).encode(),    # passo necessário na lógica do protocolo/benchmark
                                headers={'Content-Type': 'application/json'})    # passo necessário na lógica do protocolo/benchmark
                with urlopen(request, timeout=0.5) as response:    # passo necessário na lógica do protocolo/benchmark
                    result = json.loads(response.read().decode())    # passo necessário na lógica do protocolo/benchmark
                    # atualiza termo se necessário
                    if result.get('term', 0) > self.term:    # inicia um desvio condicional para tratar este caso
                        self.term = result['term']    # passo necessário na lógica do protocolo/benchmark
                        self.state = Server.FOLLOWER    # atualiza o estado do servidor conforme o papel atual no Raft
            except (URLError, Exception) as e:    # passo necessário na lógica do protocolo/benchmark
                print(f"[líder {self.id}] erro ao enviar heartbeat para {peer_url}: {e}")    # gera saída no console para observação do estado

    def receive_heartbeat(self, term, leader_id):    # define uma função/método com a lógica correspondente
        if term >= self.term:    # inicia um desvio condicional para tratar este caso
            self.term = term    # atualiza o termo (era) do Raft para refletir nova eleição/heartbeat
            self.state = Server.FOLLOWER    # atualiza o estado do servidor conforme o papel atual no Raft
            self.voted_for = leader_id    # passo necessário na lógica do protocolo/benchmark
            self.last_heartbeat = time.time()    # passo necessário na lógica do protocolo/benchmark
            print(f"[server {self.id}] recebeu heartbeat do líder {leader_id}")    # gera saída no console para observação do estado

    def stop(self):    # define uma função/método com a lógica correspondente
        self.stop_event.set()    # sinaliza término ordenado do componente
        if self.server:    # inicia um desvio condicional para tratar este caso
            self.server.shutdown()    # passo necessário na lógica do protocolo/benchmark

if __name__ == "__main__":    # inicia um desvio condicional para tratar este caso
    parser = argparse.ArgumentParser(description='servidor raft distribuído')    # passo necessário na lógica do protocolo/benchmark
    parser.add_argument('--id', type=int, required=True, help='id do servidor')    # passo necessário na lógica do protocolo/benchmark
    parser.add_argument('--host', type=str, default='localhost', help='host do servidor')    # passo necessário na lógica do protocolo/benchmark
    parser.add_argument('--port', type=int, required=True, help='porta do servidor')    # passo necessário na lógica do protocolo/benchmark
    parser.add_argument('--peers', type=str, nargs='+', default=[], help='urls dos peers (ex: http://localhost:8001 http://localhost:8002)')    # passo necessário na lógica do protocolo/benchmark
    args = parser.parse_args()    # passo necessário na lógica do protocolo/benchmark
    
    server = Server(args.id, args.host, args.port, args.peers)    # passo necessário na lógica do protocolo/benchmark
    print(f"[server {args.id}] iniciando em {args.host}:{args.port}")    # gera saída no console para observação do estado
    print(f"[server {args.id}] peers: {args.peers}")    # gera saída no console para observação do estado
    server.start()    # inicializa execução assíncrona (thread/servidor)
    
    try:    # passo necessário na lógica do protocolo/benchmark
        while True:    # passo necessário na lógica do protocolo/benchmark
            time.sleep(1)    # simula atraso/tempo de processamento
    except KeyboardInterrupt:    # passo necessário na lógica do protocolo/benchmark
        print(f"\n[server {args.id}] parando...")    # gera saída no console para observação do estado
        server.stop()    # passo necessário na lógica do protocolo/benchmark

