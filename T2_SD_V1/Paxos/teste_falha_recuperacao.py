# teste_falha_recuperacao.py
# Script para demonstrar recuperação de decisões anteriores quando uma réplica reinicia

import time    # passo necessário na lógica do protocolo/benchmark
from pathlib import Path    # passo necessário na lógica do protocolo/benchmark
import shutil    # passo necessário na lógica do protocolo/benchmark
from paxos_mmc import criar_sistema_paxos, Acceptor    # passo necessário na lógica do protocolo/benchmark

def demonstrar_falha_e_recuperacao():    # define uma função/método com a lógica correspondente
    print("\n" + "="*60)    # gera saída no console para observação do estado
    print("demonstração: falha e reinício de réplica (acceptor)")    # gera saída no console para observação do estado
    print("="*60 + "\n")    # gera saída no console para observação do estado
    
    log_dir = "logs_falha_recuperacao"    # passo necessário na lógica do protocolo/benchmark
    if Path(log_dir).exists():    # inicia um desvio condicional para tratar este caso
        shutil.rmtree(log_dir)    # passo necessário na lógica do protocolo/benchmark
    
    # passo 1: cria sistema inicial e faz algumas decisões
    print("[passo 1] criando sistema inicial com 5 acceptors...")    # gera saída no console para observação do estado
    acceptors, proposers = criar_sistema_paxos(n_acceptors=5, n_proposers=1, use_backoff=True, log_dir=log_dir)    # passo necessário na lógica do protocolo/benchmark
    
    print("[passo 2] fazendo algumas propostas para gerar decisões...")    # gera saída no console para observação do estado
    proposers[0].propose("valor_inicial_1")    # propõe um valor a ser decidido (Paxos)
    time.sleep(0.5)    # simula atraso/tempo de processamento
    
    proposers[0].propose("valor_inicial_2")    # propõe um valor a ser decidido (Paxos)
    time.sleep(0.5)    # simula atraso/tempo de processamento
    
    proposers[0].propose("valor_inicial_3")    # propõe um valor a ser decidido (Paxos)
    time.sleep(0.5)    # simula atraso/tempo de processamento
    
    # verifica decisões aceitas
    print("\n[passo 3] verificando decisões antes da falha:")    # gera saída no console para observação do estado
    for acceptor in acceptors:    # itera sobre a coleção para aplicar a ação a cada elemento
        if acceptor.accepted_value is not None:    # inicia um desvio condicional para tratar este caso
            print(f"  acceptor {acceptor.acceptor_id}: aceitou '{acceptor.accepted_value}' (proposta #{acceptor.accepted_number})")    # gera saída no console para observação do estado
            print(f"    log: {len(acceptor.decisions_log)} decisões registradas")    # gera saída no console para observação do estado
    
    # passo 4: simula falha do acceptor 2 (remove da lista mas mantém log)
    print("\n[passo 4] simulando falha do acceptor 2...")    # gera saída no console para observação do estado
    acceptor_falha = acceptors[2]    # passo necessário na lógica do protocolo/benchmark
    log_file_falha = acceptor_falha.log_file    # passo necessário na lógica do protocolo/benchmark
    
    print(f"  acceptor {acceptor_falha.acceptor_id} falhou (log salvo em: {log_file_falha})")    # gera saída no console para observação do estado
    
    # remove acceptor falho do sistema
    acceptors.remove(acceptor_falha)    # passo necessário na lógica do protocolo/benchmark
    for proposer in proposers:    # itera sobre a coleção para aplicar a ação a cada elemento
        proposer.acceptors = acceptors    # passo necessário na lógica do protocolo/benchmark
    
    print(f"  sistema continua com {len(acceptors)} acceptors")    # gera saída no console para observação do estado
    
    # passo 5: sistema continua funcionando e faz mais decisões
    print("\n[passo 5] sistema continua funcionando e faz mais decisões...")    # gera saída no console para observação do estado
    proposers[0].propose("valor_apos_falha_1")    # propõe um valor a ser decidido (Paxos)
    time.sleep(0.5)    # simula atraso/tempo de processamento
    
    proposers[0].propose("valor_apos_falha_2")    # propõe um valor a ser decidido (Paxos)
    time.sleep(0.5)    # simula atraso/tempo de processamento
    
    # passo 6: acceptor 2 reinicia e recupera decisões anteriores do log
    print("\n[passo 6] acceptor 2 reinicia e recupera decisões do log...")    # gera saída no console para observação do estado
    acceptor_recuperado = Acceptor(2, log_file=log_file_falha)    # passo necessário na lógica do protocolo/benchmark
    
    print(f"  acceptor {acceptor_recuperado.acceptor_id} recuperado:")    # gera saída no console para observação do estado
    print(f"    últimas decisões no log: {len(acceptor_recuperado.decisions_log)}")    # gera saída no console para observação do estado
    if acceptor_recuperado.accepted_value is not None:    # inicia um desvio condicional para tratar este caso
        print(f"    último valor aceito: '{acceptor_recuperado.accepted_value}' (proposta #{acceptor_recuperado.accepted_number})")    # gera saída no console para observação do estado
        print(f"    promised_number: {acceptor_recuperado.promised_number}")    # gera saída no console para observação do estado
    
    # mostra algumas decisões recuperadas
    if acceptor_recuperado.decisions_log:    # inicia um desvio condicional para tratar este caso
        print(f"  decisões recuperadas do log:")    # gera saída no console para observação do estado
        for i, dec in enumerate(list(acceptor_recuperado.decisions_log)[-5:], 1):  # mostra últimas 5    # itera sobre a coleção para aplicar a ação a cada elemento
            print(f"    {i}. proposta #{dec['proposal_number']}: '{dec['value']}'")    # gera saída no console para observação do estado
    
    # passo 7: adiciona acceptor recuperado de volta ao sistema
    print("\n[passo 7] adicionando acceptor recuperado de volta ao sistema...")    # gera saída no console para observação do estado
    acceptors.append(acceptor_recuperado)    # passo necessário na lógica do protocolo/benchmark
    for proposer in proposers:    # itera sobre a coleção para aplicar a ação a cada elemento
        proposer.acceptors = acceptors    # passo necessário na lógica do protocolo/benchmark
    
    print(f"  sistema agora tem {len(acceptors)} acceptors novamente")    # gera saída no console para observação do estado
    
    # passo 8: sistema continua funcionando normalmente
    print("\n[passo 8] sistema continua funcionando normalmente...")    # gera saída no console para observação do estado
    proposers[0].propose("valor_apos_recuperacao")    # propõe um valor a ser decidido (Paxos)
    time.sleep(0.5)    # simula atraso/tempo de processamento
    
    # verificação final
    print("\n[verificação final] estado de todos os acceptors:")    # gera saída no console para observação do estado
    for acceptor in acceptors:    # itera sobre a coleção para aplicar a ação a cada elemento
        status = f"valor: '{acceptor.accepted_value}'" if acceptor.accepted_value else "sem valor aceito"    # passo necessário na lógica do protocolo/benchmark
        print(f"  acceptor {acceptor.acceptor_id}: {status} | log: {len(acceptor.decisions_log)} decisões")    # gera saída no console para observação do estado
    
    print("\n[conclusão] o acceptor recuperado conseguiu obter as decisões anteriores do log e")    # gera saída no console para observação do estado
    print("            sincronizou-se com o sistema, continuando a funcionar normalmente.")    # gera saída no console para observação do estado

if __name__ == "__main__":    # inicia um desvio condicional para tratar este caso
    demonstrar_falha_e_recuperacao()    # passo necessário na lógica do protocolo/benchmark

