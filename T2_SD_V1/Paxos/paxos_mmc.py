# paxos_mmc.py
# Implementação do Paxos MMC (Multi-Paxos com múltiplos proposers)
# Com suporte a backoff para evitar livelock e recuperação de decisões

import random    # passo necessário na lógica do protocolo/benchmark
import time    # passo necessário na lógica do protocolo/benchmark
import threading    # cria thread para executar em concorrência com demais componentes
import json    # passo necessário na lógica do protocolo/benchmark
from pathlib import Path    # passo necessário na lógica do protocolo/benchmark
from collections import deque    # passo necessário na lógica do protocolo/benchmark

class Acceptor:    # declara uma classe que modela este papel no protocolo
    def __init__(self, acceptor_id, log_file=None):    # define uma função/método com a lógica correspondente
        self.acceptor_id = acceptor_id    # passo necessário na lógica do protocolo/benchmark
        self.promised_number = 0    # passo necessário na lógica do protocolo/benchmark
        self.accepted_number = None    # passo necessário na lógica do protocolo/benchmark
        self.accepted_value = None    # passo necessário na lógica do protocolo/benchmark
        self.log_file = log_file    # passo necessário na lógica do protocolo/benchmark
        self.decisions_log = deque()    # passo necessário na lógica do protocolo/benchmark
        
        # recupera decisões anteriores do log se existir
        if log_file and Path(log_file).exists():    # inicia um desvio condicional para tratar este caso
            self._load_from_log()    # passo necessário na lógica do protocolo/benchmark
    
    def _save_to_log(self, proposal_number, value):    # define uma função/método com a lógica correspondente
        if self.log_file:    # inicia um desvio condicional para tratar este caso
            decision = {"proposal_number": proposal_number, "value": value, "acceptor_id": self.acceptor_id, "timestamp": time.time()}    # passo necessário na lógica do protocolo/benchmark
            self.decisions_log.append(decision)    # passo necessário na lógica do protocolo/benchmark
            try:    # passo necessário na lógica do protocolo/benchmark
                with open(self.log_file, 'a') as f:    # passo necessário na lógica do protocolo/benchmark
                    f.write(json.dumps(decision) + "\n")    # passo necessário na lógica do protocolo/benchmark
            except Exception as e:    # passo necessário na lógica do protocolo/benchmark
                print(f"erro ao salvar log: {e}")    # gera saída no console para observação do estado
    
    def _load_from_log(self):    # define uma função/método com a lógica correspondente
        try:    # passo necessário na lógica do protocolo/benchmark
            with open(self.log_file, 'r') as f:    # passo necessário na lógica do protocolo/benchmark
                for line in f:    # itera sobre a coleção para aplicar a ação a cada elemento
                    decision = json.loads(line.strip())    # passo necessário na lógica do protocolo/benchmark
                    self.decisions_log.append(decision)    # passo necessário na lógica do protocolo/benchmark
                    # atualiza estado com última decisão
                    if self.accepted_number is None or decision["proposal_number"] > self.accepted_number:    # inicia um desvio condicional para tratar este caso
                        self.accepted_number = decision["proposal_number"]    # passo necessário na lógica do protocolo/benchmark
                        self.accepted_value = decision["value"]    # passo necessário na lógica do protocolo/benchmark
                        self.promised_number = decision["proposal_number"]    # passo necessário na lógica do protocolo/benchmark
            print(f"acceptor {self.acceptor_id} recuperou {len(self.decisions_log)} decisões do log")    # gera saída no console para observação do estado
        except Exception as e:    # passo necessário na lógica do protocolo/benchmark
            print(f"erro ao carregar log: {e}")    # gera saída no console para observação do estado
    
    def receive_prepare(self, proposal_number):    # define uma função/método com a lógica correspondente
        if proposal_number > self.promised_number:    # inicia um desvio condicional para tratar este caso
            self.promised_number = proposal_number    # passo necessário na lógica do protocolo/benchmark
            print(f"[acceptor {self.acceptor_id}] promete para proposta #{proposal_number}")    # gera saída no console para observação do estado
            return (self.accepted_number, self.accepted_value)    # retorna o valor computado para o chamador
        else:    # trata casos alternativos do fluxo condicional
            print(f"[acceptor {self.acceptor_id}] rejeita proposta #{proposal_number} (já prometeu #{self.promised_number})")    # gera saída no console para observação do estado
            return None    # retorna o valor computado para o chamador
    
    def receive_accept(self, proposal_number, value):    # define uma função/método com a lógica correspondente
        if proposal_number >= self.promised_number:    # inicia um desvio condicional para tratar este caso
            self.accepted_number = proposal_number    # passo necessário na lógica do protocolo/benchmark
            self.accepted_value = value    # passo necessário na lógica do protocolo/benchmark
            self._save_to_log(proposal_number, value)    # passo necessário na lógica do protocolo/benchmark
            print(f"[acceptor {self.acceptor_id}] aceita proposta #{proposal_number} com valor '{value}'")    # gera saída no console para observação do estado
            return True    # retorna o valor computado para o chamador
        return False    # retorna o valor computado para o chamador
    
    def get_decisions(self):    # define uma função/método com a lógica correspondente
        return list(self.decisions_log)    # retorna o valor computado para o chamador

class Proposer:    # declara uma classe que modela este papel no protocolo
    def __init__(self, proposer_id, acceptors, use_backoff=True):    # define uma função/método com a lógica correspondente
        self.proposer_id = proposer_id    # passo necessário na lógica do protocolo/benchmark
        self.acceptors = acceptors    # passo necessário na lógica do protocolo/benchmark
        self.proposal_number_base = proposer_id * 1000    # passo necessário na lógica do protocolo/benchmark
        self.proposal_number = self.proposal_number_base    # passo necessário na lógica do protocolo/benchmark
        self.use_backoff = use_backoff    # passo necessário na lógica do protocolo/benchmark
        self.backoff_time = 0.1    # passo necessário na lógica do protocolo/benchmark
        self.failed_attempts = 0    # passo necessário na lógica do protocolo/benchmark
    
    def propose(self, value):    # define uma função/método com a lógica correspondente
        max_attempts = 10    # passo necessário na lógica do protocolo/benchmark
        attempt = 0    # passo necessário na lógica do protocolo/benchmark
        
        while attempt < max_attempts:    # passo necessário na lógica do protocolo/benchmark
            attempt += 1    # passo necessário na lógica do protocolo/benchmark
            self.proposal_number += 1    # passo necessário na lógica do protocolo/benchmark
            
            print(f"[proposer {self.proposer_id}] tentando proposta #{self.proposal_number} com valor '{value}' (tentativa {attempt})")    # gera saída no console para observação do estado
            
            # fase 1: prepare
            promises = []    # passo necessário na lógica do protocolo/benchmark
            for acceptor in self.acceptors:    # itera sobre a coleção para aplicar a ação a cada elemento
                response = acceptor.receive_prepare(self.proposal_number)    # implementa a fase de prepare/accept do Paxos no acceptor
                if response is not None:    # inicia um desvio condicional para tratar este caso
                    promises.append(response)    # passo necessário na lógica do protocolo/benchmark
                    time.sleep(0.01)  # simula delay de rede    # simula atraso/tempo de processamento
            
            # verifica se obteve maioria
            if len(promises) >= len(self.acceptors) // 2 + 1:    # inicia um desvio condicional para tratar este caso
                # verifica se alguma proposta já foi aceita
                accepted_value = value    # passo necessário na lógica do protocolo/benchmark
                for accepted_n, accepted_v in promises:    # itera sobre a coleção para aplicar a ação a cada elemento
                    if accepted_v is not None and accepted_n is not None:    # inicia um desvio condicional para tratar este caso
                        accepted_value = accepted_v    # passo necessário na lógica do protocolo/benchmark
                        print(f"[proposer {self.proposer_id}] encontrou valor já aceito '{accepted_value}' na proposta #{accepted_n}, usando este valor")    # gera saída no console para observação do estado
                        break    # passo necessário na lógica do protocolo/benchmark
                
                # fase 2: accept
                accepts = 0    # passo necessário na lógica do protocolo/benchmark
                for acceptor in self.acceptors:    # itera sobre a coleção para aplicar a ação a cada elemento
                    if acceptor.receive_accept(self.proposal_number, accepted_value):    # inicia um desvio condicional para tratar este caso
                        accepts += 1    # passo necessário na lógica do protocolo/benchmark
                    time.sleep(0.01)  # simula delay de rede    # simula atraso/tempo de processamento
                
                if accepts >= len(self.acceptors) // 2 + 1:    # inicia um desvio condicional para tratar este caso
                    print(f"[proposer {self.proposer_id}] [OK] proposta #{self.proposal_number} aceita com valor '{accepted_value}'")    # gera saída no console para observação do estado
                    self.failed_attempts = 0    # passo necessário na lógica do protocolo/benchmark
                    self.backoff_time = 0.1    # passo necessário na lógica do protocolo/benchmark
                    return True    # retorna o valor computado para o chamador
                else:    # trata casos alternativos do fluxo condicional
                    print(f"[proposer {self.proposer_id}] [FALHOU] não obteve maioria na fase accept ({accepts}/{len(self.acceptors)})")    # gera saída no console para observação do estado
            else:    # trata casos alternativos do fluxo condicional
                print(f"[proposer {self.proposer_id}] [FALHOU] não obteve maioria na fase prepare ({len(promises)}/{len(self.acceptors)})")    # gera saída no console para observação do estado
            
            # backoff exponencial para evitar livelock
            if self.use_backoff:    # inicia um desvio condicional para tratar este caso
                self.failed_attempts += 1    # passo necessário na lógica do protocolo/benchmark
                backoff = self.backoff_time * (2 ** self.failed_attempts)    # passo necessário na lógica do protocolo/benchmark
                backoff = min(backoff, 2.0)  # limita backoff máximo    # passo necessário na lógica do protocolo/benchmark
                print(f"[proposer {self.proposer_id}] aguardando backoff de {backoff:.2f}s antes de tentar novamente...")    # gera saída no console para observação do estado
                time.sleep(backoff)    # simula atraso/tempo de processamento
            else:    # trata casos alternativos do fluxo condicional
                # sem backoff: tenta imediatamente (pode causar livelock)
                print(f"[proposer {self.proposer_id}] sem backoff - tentando novamente imediatamente...")    # gera saída no console para observação do estado
                time.sleep(0.05)  # pequeno delay mínimo    # simula atraso/tempo de processamento
        
        print(f"[proposer {self.proposer_id}] [FALHOU] falhou após {max_attempts} tentativas")    # gera saída no console para observação do estado
        return False    # retorna o valor computado para o chamador

def criar_sistema_paxos(n_acceptors=5, n_proposers=3, use_backoff=True, log_dir="logs"):    # define uma função/método com a lógica correspondente
    Path(log_dir).mkdir(exist_ok=True)    # passo necessário na lógica do protocolo/benchmark
    
    acceptors = [Acceptor(i, log_file=f"{log_dir}/acceptor_{i}.log") for i in range(n_acceptors)]    # itera sobre a coleção para aplicar a ação a cada elemento
    proposers = [Proposer(i, acceptors, use_backoff=use_backoff) for i in range(n_proposers)]    # itera sobre a coleção para aplicar a ação a cada elemento
    
    return acceptors, proposers    # retorna o valor computado para o chamador

if __name__ == "__main__":    # inicia um desvio condicional para tratar este caso
    print("=== teste básico do paxos mmc ===")    # gera saída no console para observação do estado
    acceptors, proposers = criar_sistema_paxos(n_acceptors=5, n_proposers=2, use_backoff=True)    # passo necessário na lógica do protocolo/benchmark
    
    # proposer 0 tenta propor valor
    proposers[0].propose("valor_a")    # propõe um valor a ser decidido (Paxos)
    
    time.sleep(0.5)    # simula atraso/tempo de processamento
    
    # proposer 1 tenta propor valor diferente
    proposers[1].propose("valor_b")    # propõe um valor a ser decidido (Paxos)

