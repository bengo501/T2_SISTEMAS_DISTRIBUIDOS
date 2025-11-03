# paxos_example.py
# Simulação didática de proposta Paxos

import random    # passo necessário na lógica do protocolo/benchmark
import time    # passo necessário na lógica do protocolo/benchmark

class Proposer:    # declara uma classe que modela este papel no protocolo
    def __init__(self, proposer_id):    # define uma função/método com a lógica correspondente
        self.proposer_id = proposer_id    # passo necessário na lógica do protocolo/benchmark
        self.proposal_number = 0    # passo necessário na lógica do protocolo/benchmark

    def propose(self, value, acceptors):    # define uma função/método com a lógica correspondente
        self.proposal_number += 1    # passo necessário na lógica do protocolo/benchmark
        print(f"Proposer {self.proposer_id} proposing value {value} with proposal #{self.proposal_number}")    # gera saída no console para observação do estado
        promises = []    # passo necessário na lógica do protocolo/benchmark
        for acceptor in acceptors:    # itera sobre a coleção para aplicar a ação a cada elemento
            response = acceptor.receive_prepare(self.proposal_number)    # implementa a fase de prepare/accept do Paxos no acceptor
            if response is not None:    # inicia um desvio condicional para tratar este caso
                promises.append(response)    # passo necessário na lógica do protocolo/benchmark

        if len(promises) >= len(acceptors) // 2 + 1:    # inicia um desvio condicional para tratar este caso
            print(f"Proposer {self.proposer_id} received majority promises.")    # gera saída no console para observação do estado
            for acceptor in acceptors:    # itera sobre a coleção para aplicar a ação a cada elemento
                acceptor.receive_accept(self.proposal_number, value)    # implementa a fase de prepare/accept do Paxos no acceptor
        else:    # trata casos alternativos do fluxo condicional
            print(f"Proposer {self.proposer_id} failed to get majority promises.")    # gera saída no console para observação do estado

class Acceptor:    # declara uma classe que modela este papel no protocolo
    def __init__(self, acceptor_id):    # define uma função/método com a lógica correspondente
        self.acceptor_id = acceptor_id    # passo necessário na lógica do protocolo/benchmark
        self.promised_number = 0    # passo necessário na lógica do protocolo/benchmark
        self.accepted_number = None    # passo necessário na lógica do protocolo/benchmark
        self.accepted_value = None    # passo necessário na lógica do protocolo/benchmark

    def receive_prepare(self, proposal_number):    # define uma função/método com a lógica correspondente
        if proposal_number > self.promised_number:    # inicia um desvio condicional para tratar este caso
            self.promised_number = proposal_number    # passo necessário na lógica do protocolo/benchmark
            print(f"Acceptor {self.acceptor_id} promises for proposal #{proposal_number}")    # gera saída no console para observação do estado
            return (self.accepted_number, self.accepted_value)    # retorna o valor computado para o chamador
        else:    # trata casos alternativos do fluxo condicional
            print(f"Acceptor {self.acceptor_id} rejects proposal #{proposal_number}")    # gera saída no console para observação do estado
            return None    # retorna o valor computado para o chamador

    def receive_accept(self, proposal_number, value):    # define uma função/método com a lógica correspondente
        if proposal_number >= self.promised_number:    # inicia um desvio condicional para tratar este caso
            self.accepted_number = proposal_number    # passo necessário na lógica do protocolo/benchmark
            self.accepted_value = value    # passo necessário na lógica do protocolo/benchmark
            print(f"Acceptor {self.acceptor_id} accepts proposal #{proposal_number} with value '{value}'")    # gera saída no console para observação do estado

if __name__ == "__main__":    # inicia um desvio condicional para tratar este caso
    acceptors = [Acceptor(i) for i in range(5)]    # itera sobre a coleção para aplicar a ação a cada elemento
    proposer = Proposer(1)    # passo necessário na lógica do protocolo/benchmark
    proposer.propose("valor_consenso", acceptors)    # propõe um valor a ser decidido (Paxos)
