# teste_backoff.py
# Script para demonstrar o efeito do backoff no Paxos MMC
# Compara execução sem backoff (pode causar livelock) vs com backoff

import time    # passo necessário na lógica do protocolo/benchmark
import threading    # cria thread para executar em concorrência com demais componentes
import random    # passo necessário na lógica do protocolo/benchmark
from paxos_mmc import criar_sistema_paxos    # passo necessário na lógica do protocolo/benchmark

def executar_competicao_proposers(use_backoff, duracao_segundos=10):    # define uma função/método com a lógica correspondente
    print(f"\n{'='*60}")    # gera saída no console para observação do estado
    print(f"teste com {'backoff' if use_backoff else 'sem backoff'}")
    print(f"{'='*60}\n")    # gera saída no console para observação do estado
    
    # limpa logs anteriores se existirem
    import shutil    # passo necessário na lógica do protocolo/benchmark
    from pathlib import Path    # passo necessário na lógica do protocolo/benchmark
    log_dir = f"logs_backoff_{'on' if use_backoff else 'off'}"    # passo necessário na lógica do protocolo/benchmark
    if Path(log_dir).exists():    # inicia um desvio condicional para tratar este caso
        shutil.rmtree(log_dir)    # passo necessário na lógica do protocolo/benchmark
    
    acceptors, proposers = criar_sistema_paxos(n_acceptors=5, n_proposers=3, use_backoff=use_backoff, log_dir=log_dir)    # passo necessário na lógica do protocolo/benchmark
    
    # cria threads para múltiplos proposers competindo simultaneamente
    def proposer_thread(proposer, value):    # define uma função/método com a lógica correspondente
        time.sleep(random.uniform(0.1, 0.3))  # pequeno delay inicial aleatório    # simula atraso/tempo de processamento
        success = proposer.propose(value)    # passo necessário na lógica do protocolo/benchmark
        if success:    # inicia um desvio condicional para tratar este caso
            print(f"[proposer {proposer.proposer_id}] [OK] sucesso ao propor '{value}'")    # gera saída no console para observação do estado
        else:    # trata casos alternativos do fluxo condicional
            print(f"[proposer {proposer.proposer_id}] [FALHOU] falhou ao propor '{value}'")    # gera saída no console para observação do estado
    
    threads = []    # passo necessário na lógica do protocolo/benchmark
    
    # inicia proposers competindo
    start_time = time.time()    # passo necessário na lógica do protocolo/benchmark
    
    for i, proposer in enumerate(proposers):    # itera sobre a coleção para aplicar a ação a cada elemento
        value = f"valor_proposer_{i}_{time.time()}"    # passo necessário na lógica do protocolo/benchmark
        t = threading.Thread(target=proposer_thread, args=(proposer, value), daemon=True)    # cria thread para executar em concorrência com demais componentes
        threads.append(t)    # passo necessário na lógica do protocolo/benchmark
        t.start()    # inicializa execução assíncrona (thread/servidor)
    
    # continua enviando comandos durante a avaliação
    comando_count = 0    # passo necessário na lógica do protocolo/benchmark
    while time.time() - start_time < duracao_segundos:    # passo necessário na lógica do protocolo/benchmark
        time.sleep(1.0)    # simula atraso/tempo de processamento
        comando_count += 1    # passo necessário na lógica do protocolo/benchmark
        proposer_idx = random.randint(0, len(proposers) - 1)    # usa aleatoriedade para evitar sincronização/livelock e simular variabilidade
        valor_cmd = f"comando_{comando_count}"    # passo necessário na lógica do protocolo/benchmark
        print(f"[comando externo {comando_count}] enviando '{valor_cmd}' via proposer {proposer_idx}")    # gera saída no console para observação do estado
        proposers[proposer_idx].propose(valor_cmd)    # propõe um valor a ser decidido (Paxos)
    
    # aguarda threads terminarem
    time.sleep(2.0)    # simula atraso/tempo de processamento
    
    # conta decisões bem-sucedidas
    decisoes_sucesso = sum(1 for a in acceptors if a.accepted_value is not None)    # itera sobre a coleção para aplicar a ação a cada elemento
    print(f"\n[resultado] {decisoes_sucesso}/{len(acceptors)} acceptors aceitaram valores")    # gera saída no console para observação do estado
    
    # verifica se houve livelock (muitas tentativas mas poucas decisões)
    print(f"[observacao] {'sem backoff pode mostrar mais conflitos/livelock' if not use_backoff else 'com backoff tende a convergir melhor'}")    # gera saída no console para observação do estado

if __name__ == "__main__":    # inicia um desvio condicional para tratar este caso
    print("="*60)    # gera saída no console para observação do estado
    print("teste 1: execução sem backoff (pode causar livelock)")    # gera saída no console para observação do estado
    print("="*60)    # gera saída no console para observação do estado
    executar_competicao_proposers(use_backoff=False, duracao_segundos=15)    # passo necessário na lógica do protocolo/benchmark
    
    time.sleep(2)    # simula atraso/tempo de processamento
    
    print("\n" + "="*60)    # gera saída no console para observação do estado
    print("teste 2: execução com backoff (evita livelock)")    # gera saída no console para observação do estado
    print("="*60)    # gera saída no console para observação do estado
    executar_competicao_proposers(use_backoff=True, duracao_segundos=15)    # passo necessário na lógica do protocolo/benchmark
    
    print("\n" + "="*60)    # gera saída no console para observação do estado
    print("comparação concluída")    # gera saída no console para observação do estado
    print("="*60)    # gera saída no console para observação do estado

