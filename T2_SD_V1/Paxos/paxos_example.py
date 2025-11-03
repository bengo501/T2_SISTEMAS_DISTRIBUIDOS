# paxos_example.py
# Simulação didática de proposta Paxos

import random
import time

class Proposer:
    def __init__(self, proposer_id):
        self.proposer_id = proposer_id
        self.proposal_number = 0

    def propose(self, value, acceptors):
        self.proposal_number += 1
        print(f"Proposer {self.proposer_id} proposing value {value} with proposal #{self.proposal_number}")
        promises = []
        for acceptor in acceptors:
            response = acceptor.receive_prepare(self.proposal_number)
            if response is not None:
                promises.append(response)

        if len(promises) >= len(acceptors) // 2 + 1:
            print(f"Proposer {self.proposer_id} received majority promises.")
            for acceptor in acceptors:
                acceptor.receive_accept(self.proposal_number, value)
        else:
            print(f"Proposer {self.proposer_id} failed to get majority promises.")

class Acceptor:
    def __init__(self, acceptor_id):
        self.acceptor_id = acceptor_id
        self.promised_number = 0
        self.accepted_number = None
        self.accepted_value = None

    def receive_prepare(self, proposal_number):
        if proposal_number > self.promised_number:
            self.promised_number = proposal_number
            print(f"Acceptor {self.acceptor_id} promises for proposal #{proposal_number}")
            return (self.accepted_number, self.accepted_value)
        else:
            print(f"Acceptor {self.acceptor_id} rejects proposal #{proposal_number}")
            return None

    def receive_accept(self, proposal_number, value):
        if proposal_number >= self.promised_number:
            self.accepted_number = proposal_number
            self.accepted_value = value
            print(f"Acceptor {self.acceptor_id} accepts proposal #{proposal_number} with value '{value}'")

if __name__ == "__main__":
    acceptors = [Acceptor(i) for i in range(5)]
    proposer = Proposer(1)
    proposer.propose("valor_consenso", acceptors)
