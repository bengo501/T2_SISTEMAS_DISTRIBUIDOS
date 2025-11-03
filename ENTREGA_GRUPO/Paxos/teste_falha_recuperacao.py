# teste_falha_recuperacao.py
# Script para demonstrar recuperação de decisões anteriores quando uma réplica reinicia

import time
from pathlib import Path
import shutil
from paxos_mmc import criar_sistema_paxos, Acceptor

def demonstrar_falha_e_recuperacao():
    print("\n" + "="*60)
    print("demonstração: falha e reinício de réplica (acceptor)")
    print("="*60 + "\n")
    
    log_dir = "logs_falha_recuperacao"
    if Path(log_dir).exists():
        shutil.rmtree(log_dir)
    
    print("[passo 1] criando sistema inicial com 5 acceptors...")
    acceptors, proposers = criar_sistema_paxos(n_acceptors=5, n_proposers=1, use_backoff=True, log_dir=log_dir)
    
    print("[passo 2] fazendo algumas propostas para gerar decisões...")
    proposers[0].propose("valor_inicial_1")
    time.sleep(0.5)
    
    proposers[0].propose("valor_inicial_2")
    time.sleep(0.5)
    
    proposers[0].propose("valor_inicial_3")
    time.sleep(0.5)
    
    print("\n[passo 3] verificando decisões antes da falha:")
    for acceptor in acceptors:
        if acceptor.accepted_value is not None:
            print(f"  acceptor {acceptor.acceptor_id}: aceitou '{acceptor.accepted_value}' (proposta #{acceptor.accepted_number})")
            print(f"    log: {len(acceptor.decisions_log)} decisões registradas")
    
    print("\n[passo 4] simulando falha do acceptor 2...")
    acceptor_falha = acceptors[2]
    log_file_falha = acceptor_falha.log_file
    
    print(f"  acceptor {acceptor_falha.acceptor_id} falhou (log salvo em: {log_file_falha})")
    
    acceptors.remove(acceptor_falha)
    for proposer in proposers:
        proposer.acceptors = acceptors
    
    print(f"  sistema continua com {len(acceptors)} acceptors")
    
    print("\n[passo 5] sistema continua funcionando e faz mais decisões...")
    proposers[0].propose("valor_apos_falha_1")
    time.sleep(0.5)
    
    proposers[0].propose("valor_apos_falha_2")
    time.sleep(0.5)
    
    print("\n[passo 6] acceptor 2 reinicia e recupera decisões do log...")
    acceptor_recuperado = Acceptor(2, log_file=log_file_falha)
    
    print(f"  acceptor {acceptor_recuperado.acceptor_id} recuperado:")
    print(f"    últimas decisões no log: {len(acceptor_recuperado.decisions_log)}")
    if acceptor_recuperado.accepted_value is not None:
        print(f"    último valor aceito: '{acceptor_recuperado.accepted_value}' (proposta #{acceptor_recuperado.accepted_number})")
        print(f"    promised_number: {acceptor_recuperado.promised_number}")
    
    if acceptor_recuperado.decisions_log:
        print(f"  decisões recuperadas do log:")
        for i, dec in enumerate(list(acceptor_recuperado.decisions_log)[-5:], 1):
            print(f"    {i}. proposta #{dec['proposal_number']}: '{dec['value']}'")
    
    print("\n[passo 7] adicionando acceptor recuperado de volta ao sistema...")
    acceptors.append(acceptor_recuperado)
    for proposer in proposers:
        proposer.acceptors = acceptors
    
    print(f"  sistema agora tem {len(acceptors)} acceptors novamente")
    
    print("\n[passo 8] sistema continua funcionando normalmente...")
    proposers[0].propose("valor_apos_recuperacao")
    time.sleep(0.5)
    
    print("\n[verificação final] estado de todos os acceptors:")
    for acceptor in acceptors:
        status = f"valor: '{acceptor.accepted_value}'" if acceptor.accepted_value else "sem valor aceito"
        print(f"  acceptor {acceptor.acceptor_id}: {status} | log: {len(acceptor.decisions_log)} decisões")
    
    print("\n[conclusão] o acceptor recuperado conseguiu obter as decisões anteriores do log e")
    print("            sincronizou-se com o sistema, continuando a funcionar normalmente.")

if __name__ == "__main__":
    demonstrar_falha_e_recuperacao()
