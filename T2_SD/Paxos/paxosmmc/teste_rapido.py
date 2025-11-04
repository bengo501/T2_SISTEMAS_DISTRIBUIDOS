#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))

print("="*80)
print("teste rapido - paxos")
print("="*80)

print("\n[1/3] testando importacoes...")
try:
    from env import Env
    from utils import *
    from message import RequestMessage
    from replica import Replica
    from acceptor import Acceptor
    from leader import Leader
    print("[OK] importacoes bem-sucedidas")
except Exception as e:
    print(f"[ERRO] erro ao importar: {e}")
    sys.exit(1)

print("\n[2/3] testando criacao de componentes...")
try:
    log_dir = "logs_teste_rapido"
    if os.path.exists(log_dir):
        import shutil
        shutil.rmtree(log_dir)
    
    env = Env(log_dir=log_dir)
    initialconfig = Config([], [], [])
    
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
        Leader(env, pid, initialconfig, use_backoff=True)
        initialconfig.leaders.append(pid)
    
    print("[OK] componentes criados com sucesso")
except Exception as e:
    print(f"[ERRO] erro ao criar componentes: {e}")
    sys.exit(1)

print("\n[3/3] testando envio de comandos...")
try:
    time.sleep(2)
    
    for i in range(3):
        cmd = Command(f"client_{i}", 0, f"teste_{i}")
        env.sendMessage(initialconfig.replicas[0], RequestMessage(f"client_{i}", cmd))
        time.sleep(0.5)
    
    time.sleep(2)
    print("[OK] comandos enviados com sucesso")
except Exception as e:
    print(f"[ERRO] erro ao enviar comandos: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("teste rapido concluido com sucesso!")
print("="*80)
print("\npronto para executar testes completos:")
print("  - python teste_backoff.py")
print("  - python teste_falha_recuperacao.py")

