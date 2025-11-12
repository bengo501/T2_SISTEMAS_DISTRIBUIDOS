import argparse
import csv
import statistics
from pathlib import Path


def carregar_resultados(caminho_csv: Path):
    result = []
    with caminho_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                result.append(
                    {
                        "nro_clientes": int(row["nro_clientes"]),
                        "vazao": float(row["vazao"]),
                        "latencia_media": float(row["latencia_media"]),
                    }
                )
            except (KeyError, ValueError) as exc:
                raise ValueError(f"linha inválida no csv: {row}") from exc
    if not result:
        raise ValueError("arquivo csv vazio")
    return result


def imprimir_resumo(dados):
    total = len(dados)
    vazoes = [item["vazao"] for item in dados]
    latencias = [item["latencia_media"] for item in dados]

    print("==== resumo geral ====")
    print(f"rodadas analisadas : {total}")
    print(f"vazao media        : {statistics.mean(vazoes):.2f} ops/s")
    print(f"vazao maxima       : {max(vazoes):.2f} ops/s")
    print(f"vazao minima       : {min(vazoes):.2f} ops/s")
    print(f"latencia media     : {statistics.mean(latencias):.4f} s")
    print(f"latencia mediana   : {statistics.median(latencias):.4f} s")
    print(f"latencia maxima    : {max(latencias):.4f} s")
    print(f"latencia minima    : {min(latencias):.4f} s")
    print()

    print("==== detalhes por carga ====")
    print(f"{'clientes':>10} | {'vazao (ops/s)':>15} | {'latencia media (s)':>20}")
    print("-" * 52)
    for item in sorted(dados, key=lambda x: x["nro_clientes"]):
        print(
            f"{item['nro_clientes']:>10} | {item['vazao']:>15.2f} | {item['latencia_media']:>20.4f}"
        )


def main():
    parser = argparse.ArgumentParser(
        description="extrai métricas básicas de vazão e latência do resultados_desempenho.csv."
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("resultados_desempenho.csv"),
        help="caminho para o arquivo resultados_desempenho.csv (padrão: resultados_desempenho.csv).",
    )
    args = parser.parse_args()

    dados = carregar_resultados(args.csv)
    imprimir_resumo(dados)


if __name__ == "__main__":
    main()

