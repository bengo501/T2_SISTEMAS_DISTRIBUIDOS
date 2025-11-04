import sys
import os
import time
import threading
import random
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from env import Env
from utils import *
from message import RequestMessage

def executar_test_backoff(use_backoff=True, duracao_segundos=15):
    print(f"\n{'='*80}")
    print(f"teste com {'backoff' if use_backoff else 'sem backoff'}")
    print(f"{'='*80}\n")
    
    log_dir = f"logs_backoff_{'on' if use_backoff else 'off'}"
    if Path(log_dir).exists():
        import shutil
        shutil.rmtree(log_dir)
    
    env = Env(log_dir=log_dir)
    
    initialconfig = Config([], [], [])
    
    from replica import Replica
    from acceptor import Acceptor
    from leader import Leader
    
    for i in range(2):
        pid = "replica: %d" % i
        log_file = f"{log_dir}/replica_{i}.log"
        Replica(env, pid, initialconfig, log_file=log_file)
        initialconfig.replicas.append(pid)
    
    for i in range(3):
        pid = "acceptor: %d.%d" % (0, i)
        log_file = f"{log_dir}/acceptor_0_{i}.log"
        Acceptor(env, pid, log_file=log_file)
        initialconfig.acceptors.append(pid)
    
    for i in range(2):
        pid = "leader: %d.%d" % (0, i)
        Leader(env, pid, initialconfig, use_backoff=use_backoff)
        initialconfig.leaders.append(pid)
    
    time.sleep(2)
    
    comando_count = 0
    start_time = time.time()
    
    def enviar_comandos():
        nonlocal comando_count
        while time.time() - start_time < duracao_segundos:
            time.sleep(1.0)
            comando_count += 1
            proposer_idx = random.randint(0, len(initialconfig.replicas) - 1)
            replica_id = initialconfig.replicas[proposer_idx]
            valor_cmd = f"comando_{comando_count}"
            cmd = Command(f"client_{comando_count}", 0, valor_cmd)
            print(f"[comando externo {comando_count}] enviando '{valor_cmd}' via replica {replica_id}")
            env.sendMessage(replica_id, RequestMessage(f"client_{comando_count}", cmd))
    
    thread_comandos = threading.Thread(target=enviar_comandos, daemon=True)
    thread_comandos.start()
    
    try:
        while time.time() - start_time < duracao_segundos:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    time.sleep(2)
    
    print(f"\n[resultado] teste concluído após {comando_count} comandos enviados")
    print(f"[observacao] {'sem backoff pode mostrar mais conflitos/livelock' if not use_backoff else 'com backoff tende a convergir melhor'}")

if __name__ == "__main__":
    print("="*80)
    print("teste 1: execução sem backoff (pode causar livelock)")
    print("="*80)
    executar_test_backoff(use_backoff=False, duracao_segundos=15)
    
    time.sleep(2)
    
    print("\n" + "="*80)
    print("teste 2: execução com backoff (evita livelock)")
    print("="*80)
    executar_test_backoff(use_backoff=True, duracao_segundos=15)
    
    print("\n" + "="*80)
    print("comparação concluída")
    print("="*80)

