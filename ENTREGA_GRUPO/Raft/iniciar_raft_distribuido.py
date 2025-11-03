# iniciar_raft_distribuido.py
# Script para iniciar múltiplos nós Raft distribuídos
# Exemplo de uso para demonstrar execução distribuída

import subprocess
import time
import sys

def iniciar_cluster_raft_distribuido():
    processos = []
    
    print("=== iniciando cluster raft distribuído ===")
    print("")
    print("para execução verdadeiramente distribuída:")
    print("1. execute cada nó em uma máquina/terminal diferente")
    print("2. configure as urls dos peers corretamente (hosts/ips reais)")
    print("")
    
    configuracoes = [
        {
            'id': 0,
            'host': 'localhost',
            'port': 8000,
            'peers': ['http://localhost:8001', 'http://localhost:8002']
        },
        {
            'id': 1,
            'host': 'localhost',
            'port': 8001,
            'peers': ['http://localhost:8000', 'http://localhost:8002']
        },
        {
            'id': 2,
            'host': 'localhost',
            'port': 8002,
            'peers': ['http://localhost:8000', 'http://localhost:8001']
        }
    ]
    
    for config in configuracoes:
        cmd = [
            sys.executable,
            'raft_distribuido.py',
            '--id', str(config['id']),
            '--host', config['host'],
            '--port', str(config['port']),
            '--peers'] + config['peers']
        
        print(f"iniciando nó {config['id']} em {config['host']}:{config['port']}...")
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processos.append(proc)
    
    print("")
    print("cluster iniciado. aguardando eleição...")
    print("pressione ctrl+c para parar todos os nós")
    print("")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nparando todos os nós...")
        for proc in processos:
            proc.terminate()
            proc.wait()
        print("todos os nós parados.")

if __name__ == "__main__":
    iniciar_cluster_raft_distribuido()
