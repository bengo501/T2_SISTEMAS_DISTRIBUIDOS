import argparse
import subprocess
import sys
from pathlib import Path

PORTAS_PADRAO = [8000, 8001, 8002, 9000, 9001, 9002]


def executar_powershell(comando: str) -> subprocess.CompletedProcess:
    resultado = subprocess.run(
        ["powershell", "-Command", comando],
        capture_output=True,
        text=True,
    )
    return resultado


def matar_processos_go():
    consulta = executar_powershell(
        "Get-Process go -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id"
    )
    if consulta.returncode != 0:
        if consulta.stderr.strip():
            print(f"nao foi possivel listar processos go: {consulta.stderr.strip()}", file=sys.stderr)
        return

    pids = {linha.strip() for linha in consulta.stdout.splitlines() if linha.strip().isdigit()}
    if not pids:
        print("nenhum processo go encontrado.")
        return

    print(f"finalizando processos go: {', '.join(sorted(pids))}")
    for pid in pids:
        resposta = executar_powershell(f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue")
        if resposta.returncode != 0 and resposta.stderr.strip():
            print(f"falha ao finalizar pid {pid}: {resposta.stderr.strip()}", file=sys.stderr)


def obter_pids_por_porta(porta: int) -> set[str]:
    comando = f'netstat -ano | findstr ":{porta}"'
    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        shell=True,
    )
    if resultado.returncode not in (0, 1):
        print(f"falha ao consultar netstat para porta {porta}: {resultado.stderr.strip()}", file=sys.stderr)
        return set()

    pids = set()
    for linha in resultado.stdout.splitlines():
        partes = linha.split()
        if partes:
            pid = partes[-1]
            if pid.isdigit():
                pids.add(pid)
    return pids


def liberar_portas(portas: list[int]):
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
        resposta = executar_powershell(f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue")
        if resposta.returncode != 0 and resposta.stderr.strip():
            print(f"falha ao finalizar pid {pid}: {resposta.stderr.strip()}", file=sys.stderr)


def confirmar_portas_livres(portas: list[int]):
    ocupadas = []
    for porta in portas:
        if obter_pids_por_porta(porta):
            ocupadas.append(str(porta))

    if ocupadas:
        print(f"alerta: portas ainda ocupadas: {', '.join(ocupadas)}")
    else:
        print("todas as portas alvo estao livres.")


def executar_benchmark(duracao: int, cargas: str, raiz_projeto: Path):
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

