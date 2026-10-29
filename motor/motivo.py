"""Motivo e porquê: os textos que o cliente lê (mentoria de 28/10).

O que diferencia a recomendação é o porquê. Todo motivo segue o mesmo roteiro:
1. um fato do cliente (vem das contas e do cadastro dele);
2. quanto está em jogo (o valor em risco que o motor calculou);
3. como o plano resolve;
4. o que fica descoberto se escolher menos;
5. o que ainda falta confirmar, em linguagem simples.

Regras: só fatos do imóvel e das transações, nunca idade (RN-07); a renda só aparece
quando entrou na estimativa dos bens, e então o texto diz isso; estimativa
sempre dita como estimativa (RN-09); nada inventado, todo número tem origem (RN-53).
Este módulo só escreve texto: não decide plano, valor, canal nem confiança.
"""
import re

import parametros as P


# --- Números como gente fala ---------------------------------------------------
def _decimal(x):
    return f"{x:.1f}".replace(".", ",").replace(",0", "")


def reais(v):
    """R$ 950 · R$ 4,5 mil · R$ 49 mil · R$ 1,2 milhão (sem precisão falsa)."""
    v = float(v)
    if v >= 999_500:   # limites pelo valor já arredondado: nada de "R$ 1000 mil"
        x = round(v / 1_000_000, 1)
        return f"R$ {_decimal(x)} {'milhão' if x < 2 else 'milhões'}"
    if v >= 9_950:
        return f"R$ {round(v / 1000):.0f} mil"
    if v >= 999.5:
        return f"R$ {_decimal(round(v / 1000, 1))} mil"
    return f"R$ {round(v):.0f}"


def faixa_reais(lo, hi):
    """'de R$ 23 mil a R$ 61 mil', ou 'cerca de R$ 30 mil' quando os dois arredondam igual."""
    a, b = reais(min(lo, hi)), reais(max(lo, hi))
    return f"cerca de {a}" if a == b else f"de {a} a {b}"


NOME_PLANO = {"ESSENCIAL": "Essencial", "PRATICO": "Prático", "TOTAL": "Total"}
# Palavras do motor que não podem aparecer no texto do cliente (métrica e teste)
TERMOS_INTERNOS = ("presumido", "estimado:", "sinais ainda são fracos", "não há sinais", "o cliente ",
                   "segundo risco", "elegibilidade a confirmar", "PRESUMIDO", "INFERIDO")



# --- Motivos do Essencial (antes: "não há sinais fortes", um não-argumento) ----
def motivos_de_patrimonio(vinculo, bens):
    """Para quem não tem sinal de roubo nem de terceiros, o porquê é o próprio patrimônio
    e a cobertura mais acionada (danos elétricos). Peso 0: não muda o plano."""
    motivos = []
    if vinculo == "PROPRIETARIO":
        motivos.append(("PATRIMONIO", "não vemos aluguel nem financiamento nas suas contas, então um incêndio ou um "
                                      "temporal sairia todo do seu bolso"))
    elif vinculo == "FINANCIADO":
        motivos.append(("PATRIMONIO", "o seguro do financiamento protege a estrutura para o banco, não o que está dentro da casa"))
    e = bens["eletricos"]
    valem = "estimamos que seus eletrônicos e eletrodomésticos valem" if bens.get("regional") else \
        "seus eletrônicos e eletrodomésticos valem hoje"
    texto = f"{valem} {faixa_reais(e['min'], e['max'])}"
    pct = P.sinistros_pct("DANOS_ELETRICOS")
    if pct is not None:
        texto += f", e danos elétricos são {str(pct).replace('.', ',')}% dos acionamentos do residencial da BB"
    motivos.append(("APARELHOS", texto))
    return [{"plano": "ESSENCIAL", "peso": 0, "codigo": c, "texto": t} for c, t in motivos]


# --- Partes da justificativa ----------------------------------------------------
FALA_DOS_BENS = ("BENS_ALTOS", "APARELHOS")   # motivos que já dizem quanto valem os bens


def _em_jogo(f):
    """Quanto o cliente perderia: reconstrução (ou acabamentos) e bens, a preço de hoje.
    Se um motivo já falou dos bens, não repete o número."""
    vi, bens, vinc = f["valor_imovel"], f["campos"]["bens"], f["campos"]["vinculo"]["valor"]
    rec = (vi["reconstrucao_min"] + vi["reconstrucao_max"]) / 2
    ja_falou = any(m["codigo"] in FALA_DOS_BENS for m in f["motivos_plano"])
    seus = "os seus bens" if ja_falou else f"os seus bens, {faixa_reais(bens['min'], bens['max'])}"
    if vi["segundo_risco"]:
        a, b = P.FRACAO_ACABAMENTOS
        quem = "do condomínio" if f["campos"]["tipo"]["valor"] != "CASA" else "do financiamento"
        return f"A estrutura tem o seguro {quem}; o seu protege os acabamentos, cerca de {reais(rec * (a + b) / 2)}, e {seus}."
    if vi.get("estrutura_do_locador"):
        return (f"O imóvel é do proprietário, e o seu seguro protege {seus}; "
                f"se o contrato pedir, inclua a reconstrução, cerca de {reais(rec)}.")
    dono = ", que é do proprietário," if vinc == "INQUILINO" else ""
    return f"Reconstruir o imóvel{dono} custaria cerca de {reais(rec)} pelo custo oficial do IBGE, fora {seus}."


def _se_escolher_menos(f):
    """A frase do slide 23 da Brasilseg, com a consequência concreta para este cliente."""
    plano, cods = f["plano"], {m["codigo"] for m in f["motivos"]}
    if plano == "PRATICO":
        return "Se você escolher menos, roubo e vidros ficarão descobertos: um arrombamento sairia do seu bolso."
    if plano == "TOTAL":
        if "INQUILINO" in cods:
            return "Se você escolher menos, a perda de aluguel ficará descoberta."
        if "RECEBE_ALUGUEL" in cods:
            return "Se você escolher menos, a renda do aluguel ficará descoberta enquanto o imóvel é reparado."
        return "Se você escolher menos, danos a terceiros ficarão descobertos e sairiam do seu bolso."
    return ""


def _opcao_acima(f):
    acima = {"ESSENCIAL": "PRATICO", "PRATICO": "TOTAL"}.get(f["plano"])
    if not acima:
        return ""
    oque = {"PRATICO": "roubo e vidros", "TOTAL": "danos a terceiros e perda de aluguel"}[acima]
    if acima == "TOTAL" and any(a["cobertura"] == "RESPONSABILIDADE_CIVIL_FAMILIAR" for a in f.get("adicionais", [])):
        oque = "perda de aluguel e despesas emergenciais"
    return f"O {NOME_PLANO[acima]} acrescenta {oque}."


EXPLICA_CAMPO = {
    ("uso", "PRESUMIDO"): "falta confirmar se você mora no imóvel",
    ("area", "PRESUMIDO"): "a área veio da média de imóveis parecidos na sua região",
    ("bens", "PRESUMIDO"): "sem compras ligadas ao imóvel, usamos a média de casas parecidas na sua região",
    ("area", "ESTIMADO"): "a área foi estimada pelo IPTU e pela conta de luz",
    ("tipo", "ESTIMADO"): "o endereço não deixa claro se é casa ou apartamento",
    ("vinculo", "ESTIMADO"): "a sua relação com o imóvel foi deduzida das suas contas",
    ("uso", "ESTIMADO"): "o uso do imóvel foi deduzido das suas contas",
    ("bens", "ESTIMADO"): "o valor dos bens foi estimado pelas compras",
}
NIVEL = {"ALTA": "alta", "MEDIA": "média", "BAIXA": "baixa"}


def _confianca(f):
    """Uma frase: o nível e a principal razão, na ordem do que mais pesa (presumido antes de estimado)."""
    if f["confianca"] == "ALTA":
        return "Confiança alta: os dados vêm do seu cadastro e das suas contas."
    for chave in [(k, c) for c in ("PRESUMIDO", "ESTIMADO") for k in ("uso", "area", "bens", "tipo", "vinculo")]:
        if f["campos"][chave[0]].get("classe") == chave[1] and chave in EXPLICA_CAMPO:
            texto = EXPLICA_CAMPO[chave]
            if chave == ("bens", "PRESUMIDO") and f["campos"]["bens"].get("usou_renda"):
                texto += " e a sua renda"
            return f"Confiança {NIVEL[f['confianca']]}: {texto}."
    return f"Confiança {NIVEL[f['confianca']]} até a sua resposta."


def _nao_elegivel(f):
    if "SITUACAO_CADASTRAL" in {p["codigo"] for p in f["pendencias"]}:
        return "Não podemos fazer uma nova proposta: o cadastro indica imóvel tombado, desapropriado ou condenado."
    return ("Não podemos fazer uma nova proposta: este endereço já deve ter o seguro residencial da BB, e só pode haver "
            "um por endereço. Use a recomendação abaixo para revisar a apólice atual.")


def justificativa(f):
    """O texto da coluna justificativa_recomendacao e do app: fato, valor em risco,
    o que fica descoberto (ou a opção acima), o que confirmar e a confiança."""
    partes = [_nao_elegivel(f)] if f["elegibilidade"] == "NAO" else []
    motivos = [m["texto"] for m in f["motivos_plano"]]
    partes.append(f"Recomendamos o plano {NOME_PLANO[f['plano']]} porque {'; '.join(motivos)}.")
    partes.append(_em_jogo(f))
    if f.get("adicionais"):
        partes.append("Incluímos a responsabilidade civil familiar, que paga danos que dependentes ou pet causem a vizinhos.")
    if f["elegibilidade"] == "SIM":   # alternativas só fazem sentido para uma proposta nova (RN-37)
        partes.append(_se_escolher_menos(f))
        partes.append(_opcao_acima(f))
    if f["pendencias"] and f["elegibilidade"] == "SIM":
        perguntas = [p["pergunta"] for p in f["pendencias"] if p.get("pergunta")]
        if perguntas:
            partes.append("Antes de contratar: " + " ".join(perguntas))
    if f["avisos"]:   # a cláusula fica nas colunas técnicas; o cliente lê só o efeito
        partes.append("Atenção: " + "; ".join(re.sub(r" \(CG[^)]*\)", "", a) for a in f["avisos"]) + ".")
    partes.append(_confianca(f))
    return " ".join(p for p in partes if p)
