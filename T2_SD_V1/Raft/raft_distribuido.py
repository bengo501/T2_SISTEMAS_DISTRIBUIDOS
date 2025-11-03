# raft_distribuido.py
# Versão distribuída do Raft usando HTTP para comunicação entre nós
# Permite executar nós em máquinas/hosts diferentes

import random
import time
import threading
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import URLError
import argparse

class Server:
    FOLLOWER = 'Follower'
    CANDIDATE = 'Candidate'
    LEADER = 'Leader'

    def __init__(self, server_id, host, port, peers):
        self.id = server_id
        self.host = host
        self.port = port
        self.peers = peers
        self.state = Server.FOLLOWER
        self.term = 0
        self.voted_for = None
        self.votes_received = 0
        self.election_timeout = random.uniform(1.0, 2.0)
        self.last_heartbeat = time.time()
        self.stop_event = threading.Event()
        self.server = None

    def start_http_server(self):
        class RaftHandler(BaseHTTPRequestHandler):
            def __init__(self, raft_server):
                self.raft_server = raft_server

            def do_GET(self):
                if self.path == '/status':
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    status = {
                        'id': self.raft_server.id,
                        'state': self.raft_server.state,
                        'term': self.raft_server.term,
                        'voted_for': self.raft_server.voted_for
                    }
                    self.wfile.write(json.dumps(status).encode())

            def do_POST(self):
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length).decode()
                data = json.loads(body)
                
                if self.path == '/request_vote':
                    result = self.raft_server.request_vote(data['term'], data['candidate_id'])
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'vote_granted': result, 'term': self.raft_server.term}).encode())
                elif self.path == '/heartbeat':
                    self.raft_server.receive_heartbeat(data['term'], data['leader_id'])
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': True, 'term': self.raft_server.term}).encode())

            def log_message(self, format, *args):
                pass

        handler = lambda *args, **kwargs: RaftHandler(self)(*args, **kwargs)
        self.server = HTTPServer((self.host, self.port), handler)
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()

    def start(self):
        self.start_http_server()
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        while not self.stop_event.is_set():
            time.sleep(0.1)
            if self.state == Server.FOLLOWER:
                if time.time() - self.last_heartbeat > self.election_timeout:
                    print(f"[server {self.id}] timeout. tornando-se candidato.")
                    self.start_election()
            elif self.state == Server.LEADER:
                self.send_heartbeats()
                time.sleep(0.3)

    def start_election(self):
        self.state = Server.CANDIDATE
        self.term += 1
        self.voted_for = self.id
        self.votes_received = 1
        print(f"[server {self.id}] inicia eleição para termo {self.term}")
        
        for peer_url in self.peers:
            try:
                request = Request(f"{peer_url}/request_vote",
                                data=json.dumps({'term': self.term, 'candidate_id': self.id}).encode(),
                                headers={'Content-Type': 'application/json'})
                with urlopen(request, timeout=0.5) as response:
                    result = json.loads(response.read().decode())
                    if result.get('vote_granted'):
                        self.votes_received += 1
                        print(f"[server {self.id}] recebeu voto de {peer_url}")
            except (URLError, Exception) as e:
                print(f"[server {self.id}] erro ao solicitar voto de {peer_url}: {e}")
        
        total_servers = len(self.peers) + 1
        if self.votes_received > total_servers // 2:
            print(f"[server {self.id}] torna-se líder para termo {self.term}")
            self.state = Server.LEADER
            self.send_heartbeats()
        else:
            print(f"[server {self.id}] falhou na eleição (recebeu {self.votes_received} votos de {total_servers})")

    def request_vote(self, term, candidate_id):
        if term > self.term and (self.voted_for is None or self.voted_for == candidate_id):
            self.term = term
            self.voted_for = candidate_id
            print(f"[server {self.id}] vota para {candidate_id} no termo {term}")
            return True
        return False

    def send_heartbeats(self):
        print(f"[líder {self.id}] enviando heartbeats...")
        self.last_heartbeat = time.time()
        for peer_url in self.peers:
            try:
                request = Request(f"{peer_url}/heartbeat",
                                data=json.dumps({'term': self.term, 'leader_id': self.id}).encode(),
                                headers={'Content-Type': 'application/json'})
                with urlopen(request, timeout=0.5) as response:
                    result = json.loads(response.read().decode())
                    if result.get('term', 0) > self.term:
                        self.term = result['term']
                        self.state = Server.FOLLOWER
            except (URLError, Exception) as e:
                print(f"[líder {self.id}] erro ao enviar heartbeat para {peer_url}: {e}")

    def receive_heartbeat(self, term, leader_id):
        if term >= self.term:
            self.term = term
            self.state = Server.FOLLOWER
            self.voted_for = leader_id
            self.last_heartbeat = time.time()
            print(f"[server {self.id}] recebeu heartbeat do líder {leader_id}")

    def stop(self):
        self.stop_event.set()
        if self.server:
            self.server.shutdown()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='servidor raft distribuído')
    parser.add_argument('--id', type=int, required=True, help='id do servidor')
    parser.add_argument('--host', type=str, default='localhost', help='host do servidor')
    parser.add_argument('--port', type=int, required=True, help='porta do servidor')
    parser.add_argument('--peers', type=str, nargs='+', default=[], help='urls dos peers (ex: http://localhost:8001 http://localhost:8002)')
    args = parser.parse_args()
    
    server = Server(args.id, args.host, args.port, args.peers)
    print(f"[server {args.id}] iniciando em {args.host}:{args.port}")
    print(f"[server {args.id}] peers: {args.peers}")
    server.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n[server {args.id}] parando...")
        server.stop()
