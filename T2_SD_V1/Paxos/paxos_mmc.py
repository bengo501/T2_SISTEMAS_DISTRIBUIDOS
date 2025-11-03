# paxos_mmc.py
# Implementação do Paxos MMC (Multi-Paxos com múltiplos proposers)
# Com suporte a backoff para evitar livelock e recuperação de decisões

import random
import time
import threading
import json
from pathlib import Path
from collections import deque

class Acceptor:
    def __init__(self, acceptor_id, log_file=None):
        self.acceptor_id = acceptor_id
        self.promised_number = 0
        self.accepted_number = None
        self.accepted_value = None
        self.log_file = log_file
        self.decisions_log = deque()
        
        if log_file and Path(log_file).exists():
            self._load_from_log()
    
    def _save_to_log(self, proposal_number, value):
        if self.log_file:
            decision = {"proposal_number": proposal_number, "value": value, "acceptor_id": self.acceptor_id, "timestamp": time.time()}
            self.decisions_log.append(decision)
            try:
                with open(self.log_file, 'a') as f:
                    f.write(json.dumps(decision) + "\n")
            except Exception as e:
                print(f"erro ao salvar log: {e}")
    
    def _load_from_log(self):
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    decision = json.loads(line.strip())
                    self.decisions_log.append(decision)
                    if self.accepted_number is None or decision["proposal_number"] > self.accepted_number:
                        self.accepted_number = decision["proposal_number"]
                        self.accepted_value = decision["value"]
                        self.promised_number = decision["proposal_number"]
            print(f"acceptor {self.acceptor_id} recuperou {len(self.decisions_log)} decisões do log")
        except Exception as e:
            print(f"erro ao carregar log: {e}")
    
    def receive_prepare(self, proposal_number):
        if proposal_number > self.promised_number:
            self.promised_number = proposal_number
            print(f"[acceptor {self.acceptor_id}] promete para proposta #{proposal_number}")
            return (self.accepted_number, self.accepted_value)
        else:
            print(f"[acceptor {self.acceptor_id}] rejeita proposta #{proposal_number} (já prometeu #{self.promised_number})")
            return None
    
    def receive_accept(self, proposal_number, value):
        if proposal_number >= self.promised_number:
            self.accepted_number = proposal_number
            self.accepted_value = value
            self._save_to_log(proposal_number, value)
            print(f"[acceptor {self.acceptor_id}] aceita proposta #{proposal_number} com valor '{value}'")
            return True
        return False
    
    def get_decisions(self):
        return list(self.decisions_log)

class Proposer:
    def __init__(self, proposer_id, acceptors, use_backoff=True):
        self.proposer_id = proposer_id
        self.acceptors = acceptors
        self.proposal_number_base = proposer_id * 1000
        self.proposal_number = self.proposal_number_base
        self.use_backoff = use_backoff
        self.backoff_time = 0.1
        self.failed_attempts = 0
    
    def propose(self, value):
        max_attempts = 10
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            self.proposal_number += 1
            
            print(f"[proposer {self.proposer_id}] tentando proposta #{self.proposal_number} com valor '{value}' (tentativa {attempt})")
            
            promises = []
            for acceptor in self.acceptors:
                response = acceptor.receive_prepare(self.proposal_number)
                if response is not None:
                    promises.append(response)
                    time.sleep(0.01)
            
            if len(promises) >= len(self.acceptors) // 2 + 1:
                accepted_value = value
                for accepted_n, accepted_v in promises:
                    if accepted_v is not None and accepted_n is not None:
                        accepted_value = accepted_v
                        print(f"[proposer {self.proposer_id}] encontrou valor já aceito '{accepted_value}' na proposta #{accepted_n}, usando este valor")
                        break
                
                accepts = 0
                for acceptor in self.acceptors:
                    if acceptor.receive_accept(self.proposal_number, accepted_value):
                        accepts += 1
                    time.sleep(0.01)
                
                if accepts >= len(self.acceptors) // 2 + 1:
                    print(f"[proposer {self.proposer_id}] [OK] proposta #{self.proposal_number} aceita com valor '{accepted_value}'")
                    self.failed_attempts = 0
                    self.backoff_time = 0.1
                    return True
                else:
                    print(f"[proposer {self.proposer_id}] [FALHOU] não obteve maioria na fase accept ({accepts}/{len(self.acceptors)})")
            else:
                print(f"[proposer {self.proposer_id}] [FALHOU] não obteve maioria na fase prepare ({len(promises)}/{len(self.acceptors)})")
            
            if self.use_backoff:
                self.failed_attempts += 1
                backoff = self.backoff_time * (2 ** self.failed_attempts)
                backoff = min(backoff, 2.0)
                print(f"[proposer {self.proposer_id}] aguardando backoff de {backoff:.2f}s antes de tentar novamente...")
                time.sleep(backoff)
            else:
                print(f"[proposer {self.proposer_id}] sem backoff - tentando novamente imediatamente...")
                time.sleep(0.05)
        
        print(f"[proposer {self.proposer_id}] [FALHOU] falhou após {max_attempts} tentativas")
        return False

def criar_sistema_paxos(n_acceptors=5, n_proposers=3, use_backoff=True, log_dir="logs"):
    Path(log_dir).mkdir(exist_ok=True)
    
    acceptors = [Acceptor(i, log_file=f"{log_dir}/acceptor_{i}.log") for i in range(n_acceptors)]
    proposers = [Proposer(i, acceptors, use_backoff=use_backoff) for i in range(n_proposers)]
    
    return acceptors, proposers

if __name__ == "__main__":
    print("=== teste básico do paxos mmc ===")
    acceptors, proposers = criar_sistema_paxos(n_acceptors=5, n_proposers=2, use_backoff=True)
    
    proposers[0].propose("valor_a")
    
    time.sleep(0.5)
    
    proposers[1].propose("valor_b")
