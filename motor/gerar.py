"""Roda o motor de ponta a ponta.

1. Calibra a estimativa de área na base de desenvolvimento (dados/desenvolvimento).
2. Processa a base Teste Comum (dados/teste_comum).
3. Valida e grava as 2 planilhas, as fichas (JSON para as telas), as métricas e o acerto de cada
   cálculo de dado faltante (assertividade.json).

Uso:
    python motor/gerar.py                  grava em motor/saida/
    python motor/gerar.py --saida PASTA    grava em outra pasta
    python motor/gerar.py --entrega        também copia as 2 planilhas para entrega/
Sai com código 1 se a validação encontrar algum problema.
"""
import argparse
import json
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

import motor
from metricas import calcular_metricas, casos_contrastantes
from templates import validar_templates

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"
PLANILHAS = ["template_resultado_times.csv", "template_coberturas_times.csv"]


def resumo(fichas, segundos):
    n = len(fichas)
    return {
        "casos": n,
        "planos": dict(Counter(f["plano"] for f in fichas)),
        "elegibilidade": dict(Counter(f["elegibilidade"] for f in fichas)),
        "confianca": dict(Counter(f["confianca"] for f in fichas)),
        "canal": dict(Counter(f["canal"] for f in fichas)),
        "perguntas_media": round(sum(len(f["perguntas"]) for f in fichas) / n, 2),
        "tempo_segundos": round(segundos, 2),
    }


def escrever_fichas_demo(teste, fichas, casos):
    """prototipos/fichas_demo.js: as fichas dos casos contrastantes para o protótipo com gerente.
    É um .js (e não .json) para o protótipo funcionar aberto com dois cliques, sem servidor."""
    m = teste["enderecos_imoveis"].merge(teste["sinais_imobiliarios"], on=["imovel_id", "cliente_id"])
    sinais = m.set_index("imovel_id")
    por_id = {f["imovel_id"]: f for f in fichas}
    demo = {"casos": casos, "fichas": {}}
    for imovel_id in filter(None, casos.values()):
        s = sinais.loc[imovel_id]
        demo["fichas"][imovel_id] = {**por_id[imovel_id], "sinais": {
            "parcela": float(s.parcela_financiamento_imobiliario), "aluguel": float(s.valor_aluguel_recorrente),
            "vidracaria": float(s.gastos_vidracaria_24m), "obra": float(s.gastos_material_construcao_24m)}}
    texto = ("// Gerado por motor/gerar.py. Não edite à mão.\n"
             "window.FICHAS_DEMO = " + json.dumps(demo, ensure_ascii=False, indent=1) + ";\n")
    (RAIZ / "prototipos" / "fichas_demo.js").write_text(texto, encoding="utf-8")


def gerar(saida, entrega=False):
    inicio = time.time()
    cal = motor.calibrar(motor.carregar(DADOS / "desenvolvimento"))
    teste = motor.carregar(DADOS / "teste_comum")
    fichas = motor.processar(teste, cal)
    resultado, cob = motor.para_templates(fichas, teste["template"])
    erros = validar_templates(resultado, cob, teste["template"], teste["template_coberturas"], teste["catalogo"])

    saida.mkdir(parents=True, exist_ok=True)
    resultado.to_csv(saida / PLANILHAS[0], index=False, encoding="utf-8-sig", lineterminator="\n")
    cob.to_csv(saida / PLANILHAS[1], index=False, encoding="utf-8-sig", lineterminator="\n")
    (saida / "fichas.json").write_text(json.dumps(fichas, ensure_ascii=False, indent=1), encoding="utf-8")
    (saida / "calibracao.json").write_text(json.dumps(cal, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    met = calcular_metricas(teste, cal, fichas, resultado, cob, time.time() - inicio)
    casos = casos_contrastantes(fichas)
    (saida / "metricas.json").write_text(json.dumps(met, ensure_ascii=False, indent=1), encoding="utf-8")
    (saida / "assertividade.json").write_text(json.dumps(met["assertividade"], ensure_ascii=False, indent=1), encoding="utf-8")
    (saida / "casos_contrastantes.json").write_text(json.dumps(casos, ensure_ascii=False, indent=1), encoding="utf-8")
    info = {**resumo(fichas, time.time() - inicio), "erros_validacao": len(erros), "erros": erros,
            "teste_justica_casos_alterados": met["teste_justica_casos_alterados"], "casos_contrastantes": casos}
    if entrega and not erros:
        escrever_fichas_demo(teste, fichas, casos)
        destino = RAIZ / "entrega"
        destino.mkdir(exist_ok=True)
        for nome in PLANILHAS + ["metricas.json", "casos_contrastantes.json", "assertividade.json"]:
            shutil.copy(saida / nome, destino / nome)
    return info


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", type=Path, default=Path(__file__).resolve().parent / "saida")
    ap.add_argument("--entrega", action="store_true")
    args = ap.parse_args()
    info = gerar(args.saida, args.entrega)
    print(json.dumps({k: v for k, v in info.items() if k != "tempo_segundos"}, ensure_ascii=False, indent=1))
    sys.exit(1 if info["erros_validacao"] else 0)
