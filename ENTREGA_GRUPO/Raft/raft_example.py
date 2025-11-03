# raft_example.py
# Simulação educacional simples do algoritmo Raft

import random
import time
from threading import Thread, Event

class Server:
    FOLLOWER = 'Follower'
    CANDIDATE = 'Candidate'
    LEADER = 'Leader'

    def __init__(self, server_id, cluster):
        self.id = server_id
        self.cluster = cluster
        self.state = Server.FOLLOWER
        self.term = 0
        self.voted_for = None
        self.votes_received = 0
        self.election_timeout = random.uniform(1.0, 2.0)
        self.last_heartbeat = time.time()
        self.stop_event = Event()

    def start(self):
        Thread(target=self.run, daemon=True).start()

    def run(self):
        while not self.stop_event.is_set():
            time.sleep(0.1)
            if self.state == Server.FOLLOWER:
                if time.time() - self.last_heartbeat > self.election_timeout:
                    print(f"Server {self.id} timeout. Becoming candidate.")
                    self.start_election()
            elif self.state == Server.CANDIDATE:
                pass
            elif self.state == Server.LEADER:
                self.send_heartbeats()
                time.sleep(0.3)

    def start_election(self):
        self.state = Server.CANDIDATE
        self.term += 1
        self.voted_for = self.id
        self.votes_received = 1
        print(f"Server {self.id} starts election for term {self.term}")
        for peer in self.cluster:
            if peer.id != self.id:
                if peer.request_vote(self.term, self.id):
                    self.votes_received += 1
        if self.votes_received > len(self.cluster) // 2:
            print(f"Server {self.id} becomes leader for term {self.term}")
            self.state = Server.LEADER
            self.send_heartbeats()
        else:
            print(f"Server {self.id} failed to win election")

    def request_vote(self, term, candidate_id):
        if term > self.term and (self.voted_for is None or self.voted_for == candidate_id):
            self.term = term
            self.voted_for = candidate_id
            print(f"Server {self.id} votes for {candidate_id} in term {term}")
            return True
        return False

    def send_heartbeats(self):
        print(f"Leader {self.id} sending heartbeats...")
        self.last_heartbeat = time.time()
        for peer in self.cluster:
            if peer.id != self.id:
                peer.receive_heartbeat(self.term, self.id)

    def receive_heartbeat(self, term, leader_id):
        if term >= self.term:
            self.term = term
            self.state = Server.FOLLOWER
            self.voted_for = leader_id
            self.last_heartbeat = time.time()
            print(f"Server {self.id} received heartbeat from leader {leader_id}")

if __name__ == "__main__":
    servers = [Server(i, []) for i in range(3)]
    for s in servers:
        s.cluster = servers
        s.start()

    time.sleep(10)
    for s in servers:
        s.stop_event.set()
