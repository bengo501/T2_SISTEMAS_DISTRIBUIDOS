# teste_backoff.py
# Script para demonstrar o efeito do backoff no Paxos MMC
# Compara execução sem backoff (pode causar livelock) vs com backoff

import time
import threading
import random
from paxos_mmc import criar_sistema_paxos

def executar_competicao_proposers(use_backoff, duracao_segundos=10):
    print(f"\n{'='*60}")
    print(f"teste com {'backoff' if use_backoff else 'sem backoff'}")
    print(f"{'='*60}\n")
    
    import shutil
    from pathlib import Path
    log_dir = f"logs_backoff_{'on' if use_backoff else 'off'}"
    if Path(log_dir).exists():
        shutil.rmtree(log_dir)
    
    acceptors, proposers = criar_sistema_paxos(n_acceptors=5, n_proposers=3, use_backoff=use_backoff, log_dir=log_dir)
    
    def proposer_thread(proposer, value):
        time.sleep(random.uniform(0.1, 0.3))
        success = proposer.propose(value)
        if success:
            print(f"[proposer {proposer.proposer_id}] [OK] sucesso ao propor '{value}'")
        else:
            print(f"[proposer {proposer.proposer_id}] [FALHOU] falhou ao propor '{value}'")
    
    threads = []
    
    start_time = time.time()
    
    for i, proposer in enumerate(proposers):
        value = f"valor_proposer_{i}_{time.time()}"
        t = threading.Thread(target=proposer_thread, args=(proposer, value), daemon=True)
        threads.append(t)
        t.start()
    
    comando_count = 0
    while time.time() - start_time < duracao_segundos:
        time.sleep(1.0)
        comando_count += 1
        proposer_idx = random.randint(0, len(proposers) - 1)
        valor_cmd = f"comando_{comando_count}"
        print(f"[comando externo {comando_count}] enviando '{valor_cmd}' via proposer {proposer_idx}")
        proposers[proposer_idx].propose(valor_cmd)
    
    time.sleep(2.0)
    
    decisoes_sucesso = sum(1 for a in acceptors if a.accepted_value is not None)
    print(f"\n[resultado] {decisoes_sucesso}/{len(acceptors)} acceptors aceitaram valores")
    
    print(f"[observacao] {'sem backoff pode mostrar mais conflitos/livelock' if not use_backoff else 'com backoff tende a convergir melhor'}")

if __name__ == "__main__":
    print("="*60)
    print("teste 1: execução sem backoff (pode causar livelock)")
    print("="*60)
    executar_competicao_proposers(use_backoff=False, duracao_segundos=15)
    
    time.sleep(2)
    
    print("\n" + "="*60)
    print("teste 2: execução com backoff (evita livelock)")
    print("="*60)
    executar_competicao_proposers(use_backoff=True, duracao_segundos=15)
    
    print("\n" + "="*60)
    print("comparação concluída")
    print("="*60)
