import argparse
import json
import statistics
from pathlib import Path
from typing import List


def percentis(valores: List[float], marcas):
    if not valores:
        raise ValueError("lista de latências vazia")
    ordenados = sorted(valores)
    resultados = {}
    n = len(ordenados)
    for marca in marcas:
        if not 0 < marca <= 100:
            raise ValueError(f"percentil inválido: {marca}")
        k = (marca / 100) * (n - 1)
        base = int(k)
        resto = k - base
        if base + 1 < n:
            valor = ordenados[base] + (ordenados[base + 1] - ordenados[base]) * resto
        else:
            valor = ordenados[base]
        resultados[marca] = valor
    return resultados


def carregar_latencias(caminho_json: Path):
    with caminho_json.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    latencias = payload.get("latencias", [])
    if not latencias:
        raise ValueError(f"nenhuma latência encontrada em {caminho_json}")
    return {
        "nro_clientes": payload.get("nro_clientes"),
        "duracao_seg": payload.get("duracao_seg"),
        "latencias": [float(x) for x in latencias],
    }


def imprimir_metricas(lat_info, marcas):
    latencias = lat_info["latencias"]
    print(f"==== métricas para {lat_info['nro_clientes']} clientes ====")
    print(f"amostras coletadas : {len(latencias)}")
    print(f"media              : {statistics.mean(latencias):.6f} s")
    print(f"mediana            : {statistics.median(latencias):.6f} s")
    print(f"desvio padrão      : {statistics.pstdev(latencias):.6f} s")
    print(f"mínimo             : {min(latencias):.6f} s")
    print(f"máximo             : {max(latencias):.6f} s")

    pcs = percentis(latencias, marcas)
    print("percentis:")
    for marca in sorted(pcs):
        print(f"  p{int(marca):>2}: {pcs[marca]:.6f} s")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="calcula percentis de latência a partir dos arquivos latencias_*_clientes.json."
    )
    parser.add_argument(
        "--diretorio",
        type=Path,
        default=Path("cdf_latencia"),
        help="diretório que contém os arquivos latencias_*.json (padrão: cdf_latencia).",
    )
    parser.add_argument(
        "--percentis",
        type=str,
        default="50,90,95,99",
        help="lista de percentis separados por vírgula (padrão: 50,90,95,99).",
    )
    parser.add_argument(
        "--clientes",
        type=int,
        nargs="*",
        help="filtra por número de clientes específico (opcional).",
    )
    args = parser.parse_args()

    marcas = [float(x.strip()) for x in args.percentis.split(",") if x.strip()]
    arquivos = sorted(args.diretorio.glob("latencias_*_clientes.json"))
    if not arquivos:
        raise FileNotFoundError("nenhum arquivo de latência encontrado. execute o benchmark primeiro.")

    for arquivo in arquivos:
        info = carregar_latencias(arquivo)
        if args.clientes and info["nro_clientes"] not in args.clientes:
            continue
        imprimir_metricas(info, marcas)


if __name__ == "__main__":
    main()

