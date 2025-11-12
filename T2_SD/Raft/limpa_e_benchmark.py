import argparse
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Set, List

PORTAS_PADRAO = [8000, 8001, 8002, 9000, 9001, 9002]
IS_WINDOWS = platform.system() == "Windows"


def executar_comando(comando: List[str], shell: bool = False) -> subprocess.CompletedProcess:
    """executa um comando e retorna o resultado."""
    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        shell=shell,
    )
    return resultado


def matar_processos_go():
    """mata todos os processos go em execucao."""
    if IS_WINDOWS:
        consulta = executar_comando(
            ["powershell", "-Command", "Get-Process go -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id"]
        )
        if consulta.returncode != 0:
            if consulta.stderr.strip():
                print(f"nao foi possivel listar processos go: {consulta.stderr.strip()}", file=sys.stderr)
            return

        pids = {linha.strip() for linha in consulta.stdout.splitlines() if linha.strip().isdigit()}
        if not pids:
            print("nenhum processo go encontrado.")
            return

        pids_str = ', '.join(sorted(pids))
        print(f"finalizando processos go: {pids_str}")
        for pid in pids:
            resposta = executar_comando(
                ["powershell", "-Command", f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue"]
            )
            if resposta.returncode != 0 and resposta.stderr.strip():
                print(f"falha ao finalizar pid {pid}: {resposta.stderr.strip()}", file=sys.stderr)
    else:
        # linux/unix
        consulta = executar_comando(["pgrep", "-f", "go run"])
        if consulta.returncode == 1:
            print("nenhum processo go encontrado.")
            return

        pids = {linha.strip() for linha in consulta.stdout.splitlines() if linha.strip().isdigit()}
        if not pids:
            print("nenhum processo go encontrado.")
            return

        print(f"finalizando processos go: {', '.join(sorted(pids))}")
        for pid in pids:
            resposta = executar_comando(["kill", "-9", pid])
            if resposta.returncode != 0 and resposta.stderr.strip():
                print(f"falha ao finalizar pid {pid}: {resposta.stderr.strip()}", file=sys.stderr)


def obter_pids_por_porta(porta: int) -> Set[str]:
    """obtem os pids dos processos que estao usando a porta especificada."""
    pids = set()
    
    if IS_WINDOWS:
        comando = f'netstat -ano | findstr ":{porta}"'
        resultado = executar_comando(comando.split(), shell=True)
        if resultado.returncode not in (0, 1):
            if resultado.stderr.strip():
                print(f"falha ao consultar netstat para porta {porta}: {resultado.stderr.strip()}", file=sys.stderr)
            return pids

        for linha in resultado.stdout.splitlines():
            partes = linha.split()
            if partes:
                pid = partes[-1]
                if pid.isdigit():
                    pids.add(pid)
    else:
        # linux/unix - tenta varios comandos disponiveis
        # tenta lsof primeiro (mais comum e confiavel)
        resultado = executar_comando(["lsof", "-ti", f":{porta}"])
        if resultado.returncode == 0 and resultado.stdout.strip():
            for linha in resultado.stdout.splitlines():
                pid = linha.strip()
                if pid.isdigit():
                    pids.add(pid)
        else:
            # tenta ss (socket statistics) - mais moderno
            resultado = executar_comando(["ss", "-ltnp", "sport", f":{porta}"])
            if resultado.returncode == 0 and resultado.stdout.strip():
                for linha in resultado.stdout.splitlines()[1:]:  # pula o cabecalho
                    # procura por "pid=1234," na linha
                    if "pid=" in linha:
                        for parte in linha.split():
                            if parte.startswith("pid="):
                                pid = parte.split("=")[1].split(",")[0]
                                if pid.isdigit():
                                    pids.add(pid)
            else:
                # tenta netstat como ultimo recurso
                resultado = executar_comando(["netstat", "-tlnp"])
                if resultado.returncode == 0:
                    for linha in resultado.stdout.splitlines():
                        if f":{porta}" in linha:
                            partes = linha.split()
                            for parte in reversed(partes):
                                if "/" in parte:
                                    pid = parte.split("/")[0]
                                    if pid.isdigit():
                                        pids.add(pid)
                                    break
    
    return pids


def liberar_portas(portas: List[int]):
    """libera todas as portas especificadas, matando os processos que as estao usando."""
    todos_pids = set()
    for porta in portas:
        pids = obter_pids_por_porta(porta)
        if pids:
            print(f"porta {porta} em uso por: {', '.join(sorted(pids))}")
            todos_pids.update(pids)

    if not todos_pids:
        print("nenhuma porta alvo esta em uso.")
        return

    print(f"finalizando pids restantes: {', '.join(sorted(todos_pids))}")
    for pid in todos_pids:
        if IS_WINDOWS:
            resposta = executar_comando(
                ["powershell", "-Command", f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue"]
            )
            if resposta.returncode != 0 and resposta.stderr.strip():
                print(f"falha ao finalizar pid {pid}: {resposta.stderr.strip()}", file=sys.stderr)
        else:
            # linux/unix - usa kill -9 para forcar encerramento
            resposta = executar_comando(["kill", "-9", pid])
            if resposta.returncode != 0 and resposta.stderr.strip():
                print(f"falha ao finalizar pid {pid}: {resposta.stderr.strip()}", file=sys.stderr)


def confirmar_portas_livres(portas: List[int]):
    """verifica se todas as portas estao livres."""
    ocupadas = []
    for porta in portas:
        if obter_pids_por_porta(porta):
            ocupadas.append(str(porta))

    if ocupadas:
        print(f"alerta: portas ainda ocupadas: {', '.join(ocupadas)}")
    else:
        print("todas as portas alvo estao livres.")


def verificar_versao_go() -> bool:
    """verifica se a versao do go e compativel (>= 1.21)."""
    resultado = executar_comando(["go", "version"])
    if resultado.returncode != 0:
        print("erro: nao foi possivel verificar a versao do go.", file=sys.stderr)
        return False
    
    versao_str = resultado.stdout.strip()
    print(f"versao do go: {versao_str}")
    
    # extrai a versao (ex: "go1.21.5" ou "go version go1.21.5 linux/amd64")
    match = re.search(r'go(\d+)\.(\d+)', versao_str)
    if match:
        maior, menor = int(match.group(1)), int(match.group(2))
        if maior > 1 or (maior == 1 and menor >= 21):
            return True
        else:
            print(f"erro: go {maior}.{menor} detectado, mas e necessario go 1.21 ou superior.", file=sys.stderr)
            print("por favor, atualize o go: https://go.dev/doc/install", file=sys.stderr)
            return False
    else:
        print("aviso: nao foi possivel determinar a versao do go.", file=sys.stderr)
        return True  # assume que esta ok se nao conseguir verificar


def preparar_go_modules(raiz_projeto: Path):
    """prepara os modulos go executando go mod tidy."""
    print("preparando modulos go...")
    resultado = executar_comando(["go", "mod", "tidy"], cwd=raiz_projeto)
    if resultado.returncode != 0:
        print(f"aviso: go mod tidy falhou: {resultado.stderr.strip()}", file=sys.stderr)
    else:
        print("modulos go preparados com sucesso.")


def executar_benchmark(duracao: int, cargas: str, raiz_projeto: Path):
    """executa o benchmark go."""
    # verifica versao do go primeiro
    if not verificar_versao_go():
        print("benchmark cancelado devido a incompatibilidade de versao do go.", file=sys.stderr)
        sys.exit(1)
    
    # prepara modulos go
    preparar_go_modules(raiz_projeto)
    
    comando = [
        "go",
        "run",
        "-tags",
        "benchmark",
        ".",
        "--duracao",
        str(duracao),
        "--cargas",
        cargas,
    ]
    print("executando benchmark:", " ".join(comando))
    resultado = subprocess.run(comando, cwd=raiz_projeto)
    if resultado.returncode != 0:
        print("benchmark terminou com codigo de erro:", resultado.returncode, file=sys.stderr)
    else:
        print("benchmark concluido com sucesso.")


def main():
    parser = argparse.ArgumentParser(
        description="limpa processos e portas usados pelo cluster raft antes de executar o benchmark."
    )
    parser.add_argument(
        "--duracao",
        type=int,
        default=180,
        help="duracao de cada rodada do benchmark em segundos (padrao: 180).",
    )
    parser.add_argument(
        "--cargas",
        type=str,
        default="1,2,3,4,6,8,10,12",
        help="lista de cargas separadas por virgula (padrao: 1,2,3,4,6,8,10,12).",
    )
    parser.add_argument(
        "--porta",
        type=int,
        nargs="*",
        default=PORTAS_PADRAO,
        help="lista de portas a liberar (padrao: 8000 8001 8002 9000 9001 9002).",
    )
    parser.add_argument(
        "--somente-limpeza",
        action="store_true",
        help="apenas limpa processos e portas sem executar o benchmark.",
    )
    args = parser.parse_args()

    raiz_projeto = Path(__file__).resolve().parent

    print("interrompendo processos go em execucao...")
    matar_processos_go()

    print("liberando portas alvo...")
    liberar_portas(args.porta)

    print("verificando situacao das portas...")
    confirmar_portas_livres(args.porta)

    if args.somente_limpeza:
        print("limpeza concluida. benchmark nao foi executado por opcao do usuario.")
        return

    executar_benchmark(args.duracao, args.cargas, raiz_projeto)


if __name__ == "__main__":
    main()
