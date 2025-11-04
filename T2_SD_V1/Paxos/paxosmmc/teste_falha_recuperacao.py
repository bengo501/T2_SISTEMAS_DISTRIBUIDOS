import sys
import os
import time
import threading
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from env import Env
from utils import *
from message import RequestMessage

def demonstrar_falha_e_recuperacao():
    print("\n" + "="*80)
    print("demonstração: falha e recuperação de réplica")
    print("="*80 + "\n")
    
    log_dir = "logs_falha_recuperacao"
    if Path(log_dir).exists():
        import shutil
        shutil.rmtree(log_dir)
    
    env = Env(log_dir=log_dir)
    
    initialconfig = Config([], [], [])
    
    from replica import Replica
    from acceptor import Acceptor
    from leader import Leader
    
    replicas = []
    for i in range(2):
        pid = "replica: %d" % i
        log_file = f"{log_dir}/replica_{i}.log"
        replica = Replica(env, pid, initialconfig, log_file=log_file)
        replicas.append((pid, log_file))
        initialconfig.replicas.append(pid)
    
    for i in range(3):
        pid = "acceptor: %d.%d" % (0, i)
        log_file = f"{log_dir}/acceptor_0_{i}.log"
        Acceptor(env, pid, log_file=log_file)
        initialconfig.acceptors.append(pid)
    
    for i in range(2):
        pid = "leader: %d.%d" % (0, i)
        Leader(env, pid, initialconfig, use_backoff=True)
        initialconfig.leaders.append(pid)
    
    time.sleep(2)
    
    print("[fase 1] enviando comandos iniciais...")
    for i in range(5):
        cmd = Command(f"client_{i}", 0, f"comando_inicial_{i}")
        for replica_id in initialconfig.replicas:
            env.sendMessage(replica_id, RequestMessage(f"client_{i}", cmd))
        time.sleep(1)
    
    time.sleep(3)
    
    print("\n[fase 2] simulando falha da réplica 0...")
    replica_falhou_id = initialconfig.replicas[0]
    print(f"[fase 2] réplica {replica_falhou_id} falhou")
    
    print("\n[fase 3] enviando mais comandos enquanto réplica está falha...")
    for i in range(5, 10):
        cmd = Command(f"client_{i}", 0, f"comando_durante_falha_{i}")
        for replica_id in initialconfig.replicas[1:]:
            env.sendMessage(replica_id, RequestMessage(f"client_{i}", cmd))
        time.sleep(1)
    
    time.sleep(3)
    
    print("\n[fase 4] recuperando réplica (criando nova instância com log)...")
    replica_id, log_file = replicas[0]
    nova_replica = Replica(env, replica_id, initialconfig, log_file=log_file)
    initialconfig.replicas[0] = replica_id
    
    print(f"[fase 4] réplica {replica_id} recuperada com decisões do log")
    
    time.sleep(3)
    
    print("\n[fase 5] enviando novos comandos após recuperação...")
    for i in range(10, 15):
        cmd = Command(f"client_{i}", 0, f"comando_pos_recuperacao_{i}")
        for replica_id in initialconfig.replicas:
            env.sendMessage(replica_id, RequestMessage(f"client_{i}", cmd))
        time.sleep(1)
    
    time.sleep(3)
    
    print("\n[resultado] demonstração concluída")
    print(f"[resultado] réplica recuperou decisões anteriores do log em {log_file}")
    print("[resultado] réplica pode sincronizar com outras réplicas usando decisões do log")

if __name__ == "__main__":
    demonstrar_falha_e_recuperacao()

