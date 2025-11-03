# iniciar_raft_distribuido.py
# Script para iniciar múltiplos nós Raft distribuídos
# Exemplo de uso para demonstrar execução distribuída

import subprocess    # passo necessário na lógica do protocolo/benchmark
import time    # passo necessário na lógica do protocolo/benchmark
import sys    # passo necessário na lógica do protocolo/benchmark
import signal    # passo necessário na lógica do protocolo/benchmark

def iniciar_cluster_raft_distribuido():    # define uma função/método com a lógica correspondente
    """inicia um cluster raft com 3 nós em portas diferentes"""    # passo necessário na lógica do protocolo/benchmark
    
    # configuração dos nós
    # cada nó precisa saber sobre os outros peers
    # para simular distribuição real, execute cada nó em uma máquina/terminal diferente
    
    processos = []    # passo necessário na lógica do protocolo/benchmark
    
    print("=== iniciando cluster raft distribuído ===")    # gera saída no console para observação do estado
    print("")    # gera saída no console para observação do estado
    print("para execução verdadeiramente distribuída:")    # gera saída no console para observação do estado
    print("1. execute cada nó em uma máquina/terminal diferente")    # gera saída no console para observação do estado
    print("2. configure as urls dos peers corretamente (hosts/ips reais)")    # gera saída no console para observação do estado
    print("")    # gera saída no console para observação do estado
    
    # exemplo: iniciar 3 nós localmente (para teste)
    # em produção, cada nó rodaria em uma máquina diferente
    
    configuracoes = [    # passo necessário na lógica do protocolo/benchmark
        {    # passo necessário na lógica do protocolo/benchmark
            'id': 0,    # passo necessário na lógica do protocolo/benchmark
            'host': 'localhost',    # passo necessário na lógica do protocolo/benchmark
            'port': 8000,    # passo necessário na lógica do protocolo/benchmark
            'peers': ['http://localhost:8001', 'http://localhost:8002']    # passo necessário na lógica do protocolo/benchmark
        },    # passo necessário na lógica do protocolo/benchmark
        {    # passo necessário na lógica do protocolo/benchmark
            'id': 1,    # passo necessário na lógica do protocolo/benchmark
            'host': 'localhost',    # passo necessário na lógica do protocolo/benchmark
            'port': 8001,    # passo necessário na lógica do protocolo/benchmark
            'peers': ['http://localhost:8000', 'http://localhost:8002']    # passo necessário na lógica do protocolo/benchmark
        },    # passo necessário na lógica do protocolo/benchmark
        {    # passo necessário na lógica do protocolo/benchmark
            'id': 2,    # passo necessário na lógica do protocolo/benchmark
            'host': 'localhost',    # passo necessário na lógica do protocolo/benchmark
            'port': 8002,    # passo necessário na lógica do protocolo/benchmark
            'peers': ['http://localhost:8000', 'http://localhost:8001']    # passo necessário na lógica do protocolo/benchmark
        }    # passo necessário na lógica do protocolo/benchmark
    ]    # passo necessário na lógica do protocolo/benchmark
    
    # inicia cada nó em um processo separado
    for config in configuracoes:    # itera sobre a coleção para aplicar a ação a cada elemento
        cmd = [    # passo necessário na lógica do protocolo/benchmark
            sys.executable,    # passo necessário na lógica do protocolo/benchmark
            'raft_distribuido.py',    # passo necessário na lógica do protocolo/benchmark
            '--id', str(config['id']),    # passo necessário na lógica do protocolo/benchmark
            '--host', config['host'],    # passo necessário na lógica do protocolo/benchmark
            '--port', str(config['port']),    # passo necessário na lógica do protocolo/benchmark
            '--peers'] + config['peers']    # passo necessário na lógica do protocolo/benchmark
        
        print(f"iniciando nó {config['id']} em {config['host']}:{config['port']}...")    # gera saída no console para observação do estado
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    # passo necessário na lógica do protocolo/benchmark
        processos.append(proc)    # passo necessário na lógica do protocolo/benchmark
    
    print("")    # gera saída no console para observação do estado
    print("cluster iniciado. aguardando eleição...")    # gera saída no console para observação do estado
    print("pressione ctrl+c para parar todos os nós")    # gera saída no console para observação do estado
    print("")    # gera saída no console para observação do estado
    
    # aguarda
    try:    # passo necessário na lógica do protocolo/benchmark
        while True:    # passo necessário na lógica do protocolo/benchmark
            time.sleep(1)    # simula atraso/tempo de processamento
    except KeyboardInterrupt:    # passo necessário na lógica do protocolo/benchmark
        print("\nparando todos os nós...")    # gera saída no console para observação do estado
        for proc in processos:    # itera sobre a coleção para aplicar a ação a cada elemento
            proc.terminate()    # passo necessário na lógica do protocolo/benchmark
            proc.wait()    # passo necessário na lógica do protocolo/benchmark
        print("todos os nós parados.")    # gera saída no console para observação do estado

if __name__ == "__main__":    # inicia um desvio condicional para tratar este caso
    iniciar_cluster_raft_distribuido()    # passo necessário na lógica do protocolo/benchmark

