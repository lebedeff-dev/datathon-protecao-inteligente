"""Motor de recomendação do Seguro Residencial.

Regras explicáveis, sem ML. Para cada cliente-imóvel gera uma "ficha" com:
dados inferidos (com natureza e confiança), elegibilidade, plano, motivos,
alternativa, coberturas com faixa mín/máx, perguntas e canal sugerido.
A mesma ficha alimenta os CSVs da entrega, a tela do cliente e a do gerente.
Plano de implementação: documentos/PLANO_UNIFICADO.md.
"""
import json
import math
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

import motivo as M
import parametros as P

TABELAS = ["clientes", "enderecos_imoveis", "sinais_imobiliarios", "bens_compras", "territorio"]


def carregar(origem):
    """Lê as tabelas de uma pasta ou direto de um .zip do pacote."""
    origem = Path(origem)
    if origem.suffix == ".zip":
        with zipfile.ZipFile(origem) as z:
            dados = {t: pd.read_csv(z.open(f"{t}.csv"), encoding="utf-8-sig") for t in TABELAS}
            dados["template"] = pd.read_csv(z.open("template_resultado_times.csv"), encoding="utf-8-sig")
            dados["template_coberturas"] = pd.read_csv(z.open("template_coberturas_times.csv"), encoding="utf-8-sig")
            dados["catalogo"] = pd.read_csv(z.open("catalogo_coberturas_fixas_planos.csv"), encoding="utf-8-sig")
        return dados
    dados = {t: pd.read_csv(origem / f"{t}.csv", encoding="utf-8-sig") for t in TABELAS}
    dados["template"] = pd.read_csv(origem / "template_resultado_times.csv", encoding="utf-8-sig")
    dados["template_coberturas"] = pd.read_csv(origem / "template_coberturas_times.csv", encoding="utf-8-sig")
    dados["catalogo"] = pd.read_csv(origem / "catalogo_coberturas_fixas_planos.csv", encoding="utf-8-sig")
    return dados


# --- Calibração (roda na base de desenvolvimento) -----------------------------

def calibrar(dados):
    """Aprende R$ de IPTU e de energia por m² por município, nos imóveis com área
    cadastrada, e o erro típico da estimativa para montar a faixa. Também guarda o
    backtest fora da amostra da área e do padrão pelo IPTU (ver backtest())."""
    m = dados["enderecos_imoveis"].merge(dados["sinais_imobiliarios"], on=["imovel_id", "cliente_id"])
    m = m.merge(dados["clientes"][["cliente_id", "renda_mensal"]], on="cliente_id", how="left", validate="many_to_one")
    a = m[m.area_cadastrada_m2 > 0].copy()
    cal = _calibrar_area(a)
    cal["backtest"] = backtest(a)
    # Média da região em degraus para o que faltar (área sem IPTU nem energia; imóvel sem compras)
    compras = m.compras_moveis_36m + m.compras_eletrodomesticos_36m + m.compras_eletronicos_36m
    com_compras = m.assign(compras=compras)[compras > 0]
    cal["regional"] = {"area": _degraus(a, "area_cadastrada_m2"), "compras": _degraus(com_compras, "compras")}
    cal["compras_por_renda"] = _compras_por_renda(com_compras)
    cal["backtest_bens_sem_compras"] = backtest_bens_sem_compras(com_compras)
    tot = com_compras.compras.sum()
    cal["fracao_compras"] = {"eletronicos": float(com_compras.compras_eletronicos_36m.sum() / tot),
                             "eletricos": float((com_compras.compras_eletronicos_36m + com_compras.compras_eletrodomesticos_36m).sum() / tot)}
    cal["teste_cep"] = teste_cep(a)
    return cal


def _tipo_simples(df):
    return df.possui_termo_apartamento.map({"SIM": "APTO"}).fillna("CASA")


DEGRAUS = [("município e tipo", "municipio_tipo", ["codigo_ibge_municipio", "tipo_simples"]),
           ("município", "municipio", ["codigo_ibge_municipio"]),
           ("estado", "uf", ["uf_real"])]


def _degraus(df, coluna):
    """Mediana de `coluna` em cada degrau regional, só nos grupos com pelo menos
    P.REGIONAL_MIN_IMOVEIS imóveis. Chave: 'nivel|valores' → (mediana, n)."""
    df = df.assign(tipo_simples=_tipo_simples(df))
    niveis = ([("cep", "cep", ["cep_agregado"])] if P.USAR_CEP else []) + DEGRAUS
    tabela = {}
    for _, nivel, cols in niveis:
        g = df.groupby(cols)[coluna].agg(["median", "size"])
        for chave, linha in g.iterrows():
            if linha["size"] >= P.REGIONAL_MIN_IMOVEIS:
                partes = chave if isinstance(chave, tuple) else (chave,)
                tabela["|".join([nivel, *map(str, partes)])] = (float(linha["median"]), int(linha["size"]))
    tabela["geral"] = (float(df[coluna].median()), int(df[coluna].notna().sum()))
    return tabela


def regional(cal, campo, r):
    """(mediana, nome do degrau, nº de imóveis) do degrau mais próximo que tem dados:
    município + tipo → município → estado → geral (e CEP antes, se P.USAR_CEP)."""
    t = cal["regional"][campo]
    tipo = "APTO" if r.possui_termo_apartamento == "SIM" else "CASA"
    chaves = ([("CEP", f"cep|{r.cep_agregado}")] if P.USAR_CEP else []) + [
        ("município e tipo", f"municipio_tipo|{r.codigo_ibge_municipio}|{tipo}"),
        ("município", f"municipio|{r.codigo_ibge_municipio}"), ("estado", f"uf|{r.uf_real}"), ("geral", "geral")]
    for nome, chave in chaves:
        if chave in t:
            return t[chave][0], nome, t[chave][1]


def _compras_por_renda(com_compras):
    """Compras de 36 meses ÷ renda mensal: mediana por município (só com P.REGIONAL_MIN_IMOVEIS
    imóveis ou mais, como os degraus regionais) e geral. Só renda > 0."""
    x = com_compras[com_compras.renda_mensal > 0]
    razao = x.compras / x.renda_mensal
    g = razao.groupby(x.codigo_ibge_municipio).agg(["median", "size"])
    return {"municipio": {str(k): float(l["median"]) for k, l in g.iterrows() if l["size"] >= P.REGIONAL_MIN_IMOVEIS},
            "geral": float(razao.median())}


def _renda(r):
    """Renda mensal como número, ou None se faltar, for zero, negativa ou não for número."""
    try:
        renda = float(getattr(r, "renda_mensal", 0))
    except (TypeError, ValueError):
        return None
    return renda if _positivo(renda) else None


def compras_pela_renda(r, cal):
    """Compras de 36 meses esperadas pela renda (renda × razão do município), ou None se a
    renda estiver desligada (P.RENDA_NOS_BENS_SEM_COMPRAS) ou vazia."""
    renda = _renda(r)
    if not (P.RENDA_NOS_BENS_SEM_COMPRAS and "compras_por_renda" in cal and renda):
        return None
    t = cal["compras_por_renda"]
    return renda * t["municipio"].get(str(r.codigo_ibge_municipio), t["geral"])


def _regiao_e_renda(med, pela_renda):
    """Média geométrica da região e da renda, presa entre 0,5 × e 2 × a região:
    a renda puxa a estimativa, mas nunca decide sozinha (RN-08)."""
    return min(max(math.sqrt(med * pela_renda), 0.5 * med), 2 * med)


def _compras_sem_prova(r, cal):
    """(compras estimadas, texto da fonte, degrau regional, usou renda) para quem não tem compras nem bens:
    média da região, combinada com a renda quando houver renda."""
    med, nivel, n = regional(cal, "compras", r)
    fonte = f"sem compras nem bens ligados ao imóvel: média de compras de {n} imóveis da região ({nivel})"
    pela_renda = compras_pela_renda(r, cal)
    if pela_renda is None:
        return med, fonte, nivel, False
    return _regiao_e_renda(med, pela_renda), f"{fonte} combinada com a renda mensal ({brl(_renda(r))})", nivel, True


def backtest_bens_sem_compras(com_compras):
    """Fora da amostra: finge que quem tem compras não tem e estima as compras (2 metades da base
    de desenvolvimento). Compara só a média da região com a região combinada com a renda."""
    c = com_compras.reset_index(drop=True)
    erros = {"regiao": [], "regiao_e_renda": []}
    for metade in (0, 1):
        treino, prova = c[c.index % 2 != metade], c[c.index % 2 == metade]
        mini = {"regional": {"compras": _degraus(treino, "compras")}, "compras_por_renda": _compras_por_renda(treino)}
        for r in prova.itertuples(index=False):
            med = regional(mini, "compras", r)[0]
            pela_renda = compras_pela_renda(r, mini)
            erros["regiao"].append(abs(med - r.compras) / r.compras)
            erros["regiao_e_renda"].append(abs(_regiao_e_renda(med, pela_renda) - r.compras) / r.compras
                                           if pela_renda else erros["regiao"][-1])
    return {"metodo": "2 metades da base de desenvolvimento, imóveis com compras tratados como se não tivessem",
            "casos": len(erros["regiao"]),
            "erro_mediano_so_regiao_pct": round(100 * float(np.median(erros["regiao"])), 1),
            "erro_mediano_regiao_e_renda_pct": round(100 * float(np.median(erros["regiao_e_renda"])), 1)}


def teste_cep(a):
    """O CEP agregado explica a variação do IPTU/m² melhor que um CEP sorteado? (R² entre grupos
    com 3+ imóveis.) Se não, ele é ruído e não entra como degrau regional (RN-10)."""
    a = a.assign(rel=(a.pagamento_iptu_anual / a.area_cadastrada_m2))
    a = a.assign(rel=a.rel / a.groupby("codigo_ibge_municipio").rel.transform("median"))

    def r2(col):
        x = a[a[col].map(a[col].value_counts()) >= 3]
        media = x.groupby(col).rel.transform("mean")
        return float(1 - ((x.rel - media) ** 2).sum() / ((x.rel - x.rel.mean()) ** 2).sum())
    embaralhado = a.cep_agregado.sample(frac=1, random_state=0).to_numpy()
    a = a.assign(cep_embaralhado=embaralhado)
    return {"r2_cep": round(r2("cep_agregado"), 3), "r2_cep_embaralhado": round(r2("cep_embaralhado"), 3)}


def _calibrar_area(a):
    """A parte da calibração que aprende com imóveis de área conhecida (`a`)."""
    a = a.copy()
    # IPTU ou energia zerados (isenção, imóvel vazio) não entram na mediana do R$/m²
    a["iptu_m2"] = a.pagamento_iptu_anual.where(a.pagamento_iptu_anual > 0) / a.area_cadastrada_m2
    a["energia_m2"] = a.energia_media_mensal_6m.where(a.energia_media_mensal_6m > 0) / a.area_cadastrada_m2
    por_mun = a.groupby("codigo_ibge_municipio")[["iptu_m2", "energia_m2"]].median()
    geral = a[["iptu_m2", "energia_m2"]].median()
    cal = {
        "iptu_m2": {str(k): v for k, v in por_mun.iptu_m2.items()},
        "energia_m2": {str(k): v for k, v in por_mun.energia_m2.items()},
        "iptu_m2_geral": geral.iptu_m2,
        "energia_m2_geral": geral.energia_m2,
    }
    est = a.apply(lambda r: _area_estimada(r, cal), axis=1)
    razao = a.area_cadastrada_m2 / est
    # nomes históricos: hoje são os percentis de P.AREA_QUANTIS (9% e 91%)
    cal["razao_q10"], cal["razao_q90"] = (float(razao.quantile(q)) for q in P.AREA_QUANTIS)
    cal["erro_mediano_m2"] = float((a.area_cadastrada_m2 - est).abs().median())
    cal["n_calibracao"] = int(len(a))
    # reserva para imóvel sem área, IPTU e energia: mediana por município e tipo
    a["tipo_simples"] = a.possui_termo_apartamento.map({"SIM": "APTO"}).fillna("CASA")
    med = a.groupby(["codigo_ibge_municipio", "tipo_simples"]).area_cadastrada_m2.median()
    cal["area_mediana"] = {f"{k[0]}|{k[1]}": float(v) for k, v in med.items()}
    cal["area_mediana_geral"] = float(a.area_cadastrada_m2.median())
    return cal


def backtest(a):
    """Validação fora da amostra, como os bancos fazem com modelos de estimativa: divide os
    imóveis de área conhecida em 2 metades, calibra numa e mede na outra (e vice-versa).
    Área: erro percentual (MAPE e mediana) e % da área real dentro da faixa q10–q90 (meta: ~80%).
    Padrão: nos imóveis com padrão cadastrado, % em que o intervalo pelo IPTU contém o padrão real."""
    a = a.reset_index(drop=True)
    erros, dentro = [], []
    estreitou = acertou = com_padrao = 0
    for metade in (0, 1):
        treino, prova = a[a.index % 2 != metade], a[a.index % 2 == metade]
        c = _calibrar_area(treino)
        for r in prova.itertuples(index=False):
            est = _area_estimada(r, c)
            if math.isfinite(est) and est > 0:
                erros.append(abs(est - r.area_cadastrada_m2) / r.area_cadastrada_m2)
                dentro.append(est * c["razao_q10"] <= r.area_cadastrada_m2 <= est * c["razao_q90"])
            fator = P.FATOR_PADRAO.get(str(r.padrao_construtivo_cadastrado).upper())
            if fator:
                com_padrao += 1
                intervalo = P.fator_padrao_pelo_iptu(iptu_relativo(r, c))
                if intervalo:
                    estreitou += 1
                    acertou += intervalo[0] <= fator <= intervalo[1]
    return {
        "metodo": "2 metades da base de desenvolvimento (calibra numa, mede na outra)",
        "area_casos": len(erros),
        "area_mape_pct": round(100 * float(np.mean(erros)), 1),
        "area_erro_mediano_pct": round(100 * float(np.median(erros)), 1),
        "area_dentro_da_faixa_pct": round(100 * float(np.mean(dentro)), 1),
        "padrao_casos": com_padrao,
        "padrao_estreitados": estreitou,
        "padrao_intervalo_correto_pct": round(100 * acertou / estreitou, 1) if estreitou else None,
    }


def _positivo(v):
    return v is not None and math.isfinite(float(v)) and float(v) > 0


def _area_estimada(r, cal):
    """Área pelo IPTU (peso 0,6) e pela energia (0,4). Se um dos dois vier zerado ou vazio,
    usa só o outro com o peso inteiro: um IPTU isento não pode encolher a área em 60%.
    Sem nenhum dos dois, devolve NaN (inferir_area usa a mediana de imóveis parecidos)."""
    k = str(r.codigo_ibge_municipio)
    partes = []
    if _positivo(r.pagamento_iptu_anual):
        partes.append((0.6, r.pagamento_iptu_anual / cal["iptu_m2"].get(k, cal["iptu_m2_geral"])))
    if _positivo(r.energia_media_mensal_6m):
        partes.append((0.4, r.energia_media_mensal_6m / cal["energia_m2"].get(k, cal["energia_m2_geral"])))
    if not partes:
        return float("nan")
    return sum(p * v for p, v in partes) / sum(p for p, _ in partes)


def iptu_relativo(r, cal):
    """IPTU por m² do imóvel ÷ mediana do município. Só com área cadastrada: quando a área
    é estimada pelo próprio IPTU, a razão seria circular. None se não der para calcular."""
    if not (_positivo(r.area_cadastrada_m2) and _positivo(r.pagamento_iptu_anual)):
        return None
    ref = cal["iptu_m2"].get(str(r.codigo_ibge_municipio), cal["iptu_m2_geral"])
    return (r.pagamento_iptu_anual / r.area_cadastrada_m2) / ref if ref else None


# --- Utilidades ----------------------------------------------------------------

def dado(valor, natureza, confianca, fonte, fonte_tipo="INFERIDO", idade_meses=0):
    """Um dado inferido: valor + natureza (observado/estimado/inferido/confirmado),
    confiança, fonte legível e, para a T5, o tipo de fonte e a idade do sinal."""
    return {"valor": valor, "natureza": natureza, "confianca": confianca, "fonte": fonte,
            "fonte_tipo": fonte_tipo, "idade_meses": idade_meses}


def arred(v):
    passo = 500 if v < 20000 else 1000
    return int(round(v / passo) * passo)


def faixa(lo, hi, cob):
    piso, teto = P.LIMITES_COBERTURA.get(cob, (0, float("inf")))
    lo, hi = max(piso, min(lo, teto)), max(piso, min(hi, teto))
    lo, hi = arred(min(lo, hi)), arred(max(lo, hi))
    return lo, max(hi, lo)


def pior(*confs):
    ordem = ["BAIXA", "MEDIA", "ALTA"]
    return min(confs, key=ordem.index)


def brl(v):
    return f"R$ {v:,.0f}".replace(",", ".")


# --- Inferências sobre o imóvel ------------------------------------------------

_APTO_COMPLEMENTO = re.compile(r"\b(AP|APTO|APARTAMENTO|BLOCO|BL|TORRE)\b")
_CASA_COMPLEMENTO = re.compile(r"\b(CASA|LOTE|QUADRA|SOBRADO|FUNDOS)\b")


def tipo_pelo_complemento(complemento):
    c = str(complemento or "").upper()
    if _APTO_COMPLEMENTO.search(c):
        return "APARTAMENTO"
    if _CASA_COMPLEMENTO.search(c):
        return "CASA"
    return None


def inferir_tipo(r):
    if r.possui_termo_apartamento == "SIM":
        d = dado("APARTAMENTO", "INFERIDO", "ALTA", "termo 'apartamento' no endereço")
    elif r.possui_termo_condominio == "SIM":
        conf = "ALTA" if r.pagamento_condominio_mensal > 0 else "MEDIA"
        d = dado("CASA_EM_CONDOMINIO", "INFERIDO", conf, "termos 'casa' + 'condomínio' no endereço e pagamento de condomínio")
    else:
        d = dado("CASA", "INFERIDO", "ALTA", "termo 'casa' no endereço, sem condomínio")
    # conferência com o complemento (AP/APTO/BLOCO/TORRE × CASA/LOTE/QUADRA)
    pelo_compl = tipo_pelo_complemento(r.complemento)
    d["diverge"] = pelo_compl is not None and (pelo_compl == "APARTAMENTO") != (d["valor"] == "APARTAMENTO")
    d["fonte_tipo"] = "DOCUMENTO"
    if d["diverge"]:
        d["confianca"], d["fonte_tipo"] = "MEDIA", "INFERIDO"
        d["fonte"] += f"; o complemento sugere {pelo_compl.lower()}"
    elif pelo_compl:
        d["fonte"] += "; confirmado pelo complemento"
    return d


def inferir_vinculo(r):
    if r.pagamento_aluguel_recorrente == "SIM":
        return dado("INQUILINO", "OBSERVADO", "ALTA", f"aluguel recorrente de {brl(r.valor_aluguel_recorrente)}/mês", "TRANSACAO", 3)
    if r.parcela_financiamento_imobiliario > 0:
        return dado("FINANCIADO", "OBSERVADO", "ALTA", f"parcela de financiamento de {brl(r.parcela_financiamento_imobiliario)}/mês", "TRANSACAO", 3)
    if r.credito_recorrente_compativel_aluguel == "SIM" and r.endereco_principal_compativel == "NAO":
        return dado("PROPRIETARIO_LOCADOR", "INFERIDO", "MEDIA",
                    f"recebe crédito recorrente compatível com aluguel ({brl(r.valor_medio_credito_recorrente)}/mês)", "TRANSACAO", 3)
    return dado("PROPRIETARIO", "INFERIDO", "MEDIA", "sem aluguel pago nem financiamento: provável imóvel quitado", "INFERIDO", 3)


def inferir_uso(r, outro_principal):
    if r.endereco_principal_compativel == "SIM":
        return dado("RESIDENCIAL_HABITUAL", "OBSERVADO", "ALTA", "endereço compatível com o endereço principal do cliente", "DOCUMENTO", 0)
    if r.credito_recorrente_compativel_aluguel == "SIM":
        return dado("RESIDENCIAL_LOCADO_A_TERCEIROS", "INFERIDO", "MEDIA", "não é o endereço principal e há crédito de aluguel", "TRANSACAO", 3)
    if outro_principal:
        return dado("LAZER_VERANEIO", "INFERIDO", "BAIXA", "cliente mora em outro imóvel cadastrado", "PRESUMIDO", 0)
    return dado("RESIDENCIAL_HABITUAL", "INFERIDO", "BAIXA",
                "único imóvel, mas o endereço não bate com o principal (cadastro desatualizado?)", "PRESUMIDO", 0)


def inferir_area(r, cal):
    if r.area_cadastrada_m2 > 0:
        a = float(r.area_cadastrada_m2)
        d = dado(round(a), "OBSERVADO", "ALTA", f"área cadastrada ({r.origem_area})", "DOCUMENTO", 0)
        d["min"], d["max"] = a, a
        return d
    a = _area_estimada(r, cal)
    if not math.isfinite(a) or a <= 0:  # sem área, IPTU nem energia: mediana de imóveis parecidos
        a, nivel, n = regional(cal, "area", r)
        d = dado(round(a), "ESTIMADO", "BAIXA", f"sem IPTU nem energia: mediana de {n} imóveis da região ({nivel})", "PRESUMIDO", 0)
        d["min"], d["max"], d["regional"] = a * 0.7, a * 1.3, nivel
        return d
    sinais = [f"IPTU ({brl(r.pagamento_iptu_anual)}/ano)" if _positivo(r.pagamento_iptu_anual) else "",
              f"energia ({brl(r.energia_media_mensal_6m)}/mês)" if _positivo(r.energia_media_mensal_6m) else ""]
    d = dado(round(a), "ESTIMADO", "MEDIA",
             f"estimada pelo {' e '.join(s for s in sinais if s)} comparados a imóveis de {r.municipio_real}", "DERIVADO", 3)
    d["min"], d["max"] = a * cal["razao_q10"], a * cal["razao_q90"]
    return d


def _ancoras(compras, bens_ponderados):
    """Três âncoras: mínimo comprovado (o maior entre compras e bens, a preço de hoje)
    e máximo de estoque (2,7 × compras de 36 meses, a preço de hoje)."""
    lo = max(compras, bens_ponderados) * P.FATOR_IPCA
    hi = max(lo, P.FATOR_ESTOQUE * compras * P.FATOR_IPCA)
    return lo, hi


def estimar_bens(r, bens, cal=None):
    """Faixa de valor dos bens do imóvel, por categoria. Sem arredondar: quem
    arredonda é faixa(). Nunca lê idade, dependentes ou pet. A renda só entra quando
    não há compras nem bens vinculados, junto com a média da região (com `cal`);
    sem `cal`, o piso."""
    soma = lambda tipos: float(bens.loc[bens.tipo_bem.isin(tipos), "valor_bem_ponderado_referencia"].sum())
    ele, dom, mov = float(r.compras_eletronicos_36m), float(r.compras_eletrodomesticos_36m), float(r.compras_moveis_36m)
    compras = ele + dom + mov
    pond = float(bens.valor_bem_ponderado_referencia.sum())

    if compras <= 0 and pond <= 0 and cal is not None:   # região (e renda), como se fossem as compras dele
        estimadas, fonte, nivel, usou_renda = _compras_sem_prova(r, cal)
        lo, hi = _ancoras(estimadas, 0)
        lo, hi = max(lo, P.BENS_PISO), max(hi, P.BENS_PISO)
        d = dado(int(round((lo + hi) / 2)), "ESTIMADO", "BAIXA", fonte, "PRESUMIDO", 0)
        fr = cal["fracao_compras"]
        d.update({"min": lo, "max": hi, "regional": nivel, "usou_renda": usou_renda, "categorias": {},
                  "portateis": {"min": lo * fr["eletronicos"], "max": hi * fr["eletronicos"]},
                  "eletricos": {"min": lo * fr["eletricos"], "max": hi * fr["eletricos"]},
                  "molhaveis": {"min": lo, "max": hi}})
        return d
    if compras <= 0 and pond <= 0:
        d = dado(int(P.BENS_PISO * 1.5), "ESTIMADO", "BAIXA", "sem compras nem bens vinculados: piso de uma casa mobiliada", "PRESUMIDO", 0)
        d["min"], d["max"] = float(P.BENS_PISO), float(2 * P.BENS_PISO)
        piso = {"min": P.BENS_PISO * 0.3, "max": P.BENS_PISO * 0.6}
        d.update(portateis=piso, eletricos=piso, molhaveis={"min": d["min"], "max": d["max"]}, categorias={})
        return d

    lo, hi = _ancoras(compras, pond)
    lo, hi = max(lo, P.BENS_PISO), max(hi, P.BENS_PISO)
    total_cad = float(bens.valor_cadastrado.sum())
    alta = float(bens.loc[bens.nivel_confianca_vinculo == "ALTA", "valor_cadastrado"].sum())
    # Duas provas que concordam (compras + bens ligados ao imóvel com vínculo forte) = ALTA
    vinculo_forte = bool(total_cad) and alta / total_cad >= 0.6
    conf = "ALTA" if compras > 0 and vinculo_forte else "MEDIA" if compras > 0 or vinculo_forte else "BAIXA"
    d = dado(int(round((lo + hi) / 2)), "ESTIMADO", conf,
             f"compras de {brl(compras)} nos últimos 36 meses (corrigidas pelo IPCA) e {len(bens)} bens vinculados "
             f"({brl(pond)} ponderado pela chance de estarem no imóvel)", "TRANSACAO", 18)
    d["min"], d["max"] = lo, hi
    faixa_de = lambda c, b: dict(zip(("min", "max"), _ancoras(c, b)))
    d["categorias"] = {
        "eletronicos": faixa_de(ele, soma(["ELETRONICO"])),
        "eletrodomesticos": faixa_de(dom, soma(["ELETRODOMESTICO"])),
        "moveis": faixa_de(mov, soma(["MOVEL"])),
    }
    d["portateis"] = faixa_de(ele, soma(["ELETRONICO"]))                                   # base do roubo
    d["eletricos"] = faixa_de(ele + dom, soma(["ELETRONICO", "ELETRODOMESTICO"]))          # base de danos elétricos
    d["molhaveis"] = faixa_de(compras, soma(["MOVEL", "ELETRODOMESTICO", "ELETRONICO"]))   # base de danos por água
    return d


def valor_imovel(r, tipo, vinculo, area, cal=None):
    """Custo de reconstruir o imóvel: área × [SINAPI, CUB] da UF × padrão construtivo.
    Padrão vazio com área cadastrada: o IPTU/m² do município estreita o fator (parametros.py).
    Segundo risco (CG cl. 15.2): apartamento, casa em condomínio ou imóvel financiado."""
    lo_m2, hi_m2 = P.custo_m2(r.uf_real)
    f_lo, f_hi = P.fator_padrao(r.padrao_construtivo_cadastrado)
    origem_padrao = "cadastrado" if f_lo == f_hi else "não cadastrado"
    if f_lo != f_hi and cal is not None:
        pelo_iptu = P.fator_padrao_pelo_iptu(iptu_relativo(r, cal))
        if pelo_iptu:
            f_lo, f_hi = pelo_iptu
            origem_padrao = "estimado pelo IPTU/m²"
    return {
        "custo_m2": (lo_m2 * f_lo, hi_m2 * f_hi),
        "custo_m2_base": (lo_m2, hi_m2),
        "fator_padrao": (f_lo, f_hi),
        "origem_padrao": origem_padrao,
        "reconstrucao": (area["min"] * lo_m2 * f_lo, area["max"] * hi_m2 * f_hi),
        "segundo_risco": tipo["valor"] in ("APARTAMENTO", "CASA_EM_CONDOMINIO") or vinculo["valor"] == "FINANCIADO",
        # Inquilino de casa: o seguro contra fogo do imóvel é do locador (Lei do Inquilinato, art. 22, VIII),
        # salvo contrato em contrário. Por padrão, só os bens; a pergunta do contrato inclui a estrutura (D-07).
        "estrutura_do_locador": vinculo["valor"] == "INQUILINO" and not (
            tipo["valor"] in ("APARTAMENTO", "CASA_EM_CONDOMINIO") or vinculo["valor"] == "FINANCIADO"),
        "fonte_disponivel": P.fonte_disponivel(r.uf_real),
    }


# --- Elegibilidade -------------------------------------------------------------

def avaliar_elegibilidade(r, uso, n_imoveis=None):
    """SIM ou NAO. NAO só com prova: situação cadastral não regular, ou cliente com
    seguro residencial, produto de seguridade BB e um imóvel só (provável seguro BB neste endereço). Sinal fraco vira SIM +
    pergunta de confirmação (guia §9.1). `n_imoveis`: imóveis do cliente na base."""
    pendencias, avisos = [], []
    situacao = str(r.situacao_imovel_cadastral).upper()
    if situacao not in ("REGULAR", "NAN", ""):
        return "NAO", [{"codigo": "SITUACAO_CADASTRAL", "prioridade": 100, "pergunta": "",
                        "texto": f"situação cadastral '{r.situacao_imovel_cadastral}': imóvel tombado, desapropriado ou condenado não é aceito"}], avisos
    material = str(r.material_parede_externa_cadastrado).upper()
    if material not in ("ALVENARIA", "NAO_DISPONIVEL", "NAN", ""):
        pendencias.append({"codigo": "MATERIAL", "prioridade": 98,
                           "texto": f"parede externa cadastrada como {material.lower()}: só é aceita casa de madeira pré-fabricada conforme ABNT",
                           "pergunta": "A casa é de madeira pré-fabricada certificada (ABNT)?"})
    if r.gastos_material_construcao_24m >= P.OBRA_LIMIAR_CONFIRMAR:
        pendencias.append({"codigo": "POSSIVEL_REFORMA", "prioridade": 100,
                           "texto": f"gastos de {brl(r.gastos_material_construcao_24m)} em material de construção em 24 meses podem indicar reforma, que impede a contratação",
                           "pergunta": f"Notamos {M.reais(r.gastos_material_construcao_24m)} em material de construção nos últimos 2 anos. O imóvel está em obra ou reforma agora?"})
    if r.possui_seguro_residencial == "SIM":
        # A vedação do guia vale só para seguro da BB no mesmo endereço. O campo da base não diz
        # a seguradora: só tratamos como seguro BB quando o cliente já tem produto de seguridade do BB.
        # "Produto de seguridade" pode ser vida ou previdência: é indício, não prova. Pela RN-19, vira
        # pergunta obrigatória (crítica da banca, 29/10); se a resposta for "sim", o app não faz nova proposta.
        produtos_bb = (getattr(r, "qtd_produtos_seguridade", 0) or 0) >= 1
        if n_imoveis == 1 and produtos_bb:
            pendencias.append({"codigo": "SEGURO_EXISTENTE", "prioridade": 100, "provavel_bb": True,
                               "texto": "provável seguro BB neste endereço: há seguro residencial e produto de seguridade do BB; "
                                        "se o seguro for da BB, não pode haver nova proposta para o mesmo endereço",
                               "pergunta": "O seu seguro residencial atual é da BB Seguros?"})
        elif n_imoveis == 1:
            pendencias.append({"codigo": "SEGURO_EXISTENTE", "prioridade": 100,
                               "texto": "há seguro residencial, mas nenhum produto de seguridade do BB; se o seguro atual "
                                        "for de outra seguradora, a proposta é permitida",
                               "pergunta": "O seu seguro residencial atual é da BB Seguros?"})
        else:
            pendencias.append({"codigo": "SEGURO_EXISTENTE", "prioridade": 95,
                               "texto": "há seguro residencial em um dos imóveis, e não pode haver duas propostas BB para o mesmo endereço",
                               "pergunta": ("Qual dos seus imóveis já tem o seguro residencial da BB Seguros?" if n_imoveis
                                            else "Você já tem seguro residencial da BB Seguros para este endereço?")})
    if uso["valor"] == "LAZER_VERANEIO":
        avisos.append("como o imóvel é de veraneio, o roubo não cobre os períodos em que ele fica desocupado (CG, Roubo 2.1 c)")
    return "SIM", pendencias, avisos


# --- Plano ---------------------------------------------------------------------

def familia_declarada(r):
    """Composição da casa: (tem dependentes no cadastro, informou pet).
    Uso único: necessidade de RC familiar. Nunca entra em valor, risco, canal ou confiança."""
    return (getattr(r, "quantidade_dependentes", 0) or 0) > 0, getattr(r, "possui_pet_informado", "") == "SIM"


ORDEM_PLANO = {"ESSENCIAL": 0, "PRATICO": 1, "TOTAL": 2}
NOME_PLANO = {"ESSENCIAL": "Essencial", "PRATICO": "Prático", "TOTAL": "Total"}
O_QUE_ACRESCENTA = {"PRATICO": "roubo com arrombamento e quebra de vidros",
                    "TOTAL": "o conserto de danos a terceiros, a perda de aluguel e as despesas emergenciais"}


COBRE = {"ALUGUEL": "a perda de aluguel", "ROUBO": "o roubo e a quebra de vidros", "TERCEIROS": "os danos a terceiros"}
PLANO_DA_NECESSIDADE = {"ALUGUEL": "TOTAL", "ROUBO": "PRATICO", "TERCEIROS": "RC"}


def _forca_por_limite(valor, limite):
    """'clara' se o valor está a mais de P.FAIXA_NO_LIMITE do limite (para cima ou para baixo);
    senão, 'no_limite'. É o quanto a decisão depende de um número estimado."""
    razao = valor / limite
    return "no_limite" if (1 - P.FAIXA_NO_LIMITE) <= razao < (1 + P.FAIXA_NO_LIMITE) else "clara"


def avaliar_necessidades(r, tipo, vinculo, uso, bens):
    """As três perguntas que decidem a proteção (recomendação por necessidades, 29/10).
    A · ALUGUEL: paga ou recebe aluguel deste imóvel → perda de aluguel (só no Total).
    B · ROUBO: bens comprovados ≥ R$ 36 mil, eletrônicos ≥ R$ 10 mil ou gasto com vidraçaria
        → roubo e vidros (Prático). Não conta em veraneio (o roubo não cobre casa desocupada,
        CG Roubo 2.1 c) nem com bens presumidos (não são prova).
    C · TERCEIROS: prédio ou condomínio (vizinho colado) ou dependentes/pet → RC familiar.
    Cada uma devolve: codigo, sim, forca ('clara' ou 'no_limite'), provas (texto com o número do
    cliente), cobertura que resolve e, se estiver no limite, a pergunta que decide.
    Renda, idade, dependentes e pet nunca acendem A nem B."""
    def prova(codigo, texto):
        return {"codigo": codigo, "texto": texto}

    # A · aluguel em jogo (prova de transação: sempre clara)
    a = []
    if vinculo["valor"] == "INQUILINO":
        a.append(prova("INQUILINO", f"você paga {M.reais(r.valor_aluguel_recorrente)} de aluguel por mês e, se o imóvel ficar "
                                    f"inabitável, precisaria pagar outra moradia"))
    if vinculo["valor"] == "PROPRIETARIO_LOCADOR":
        a.append(prova("RECEBE_ALUGUEL", f"este imóvel rende cerca de {M.reais(r.valor_medio_credito_recorrente)} de aluguel "
                                         f"por mês, que para de entrar se ele precisar de reparo"))
    nec_a = {"codigo": "ALUGUEL", "sim": bool(a), "forca": "clara", "provas": a, "cobertura": COBRE["ALUGUEL"], "pergunta": None}

    # B · roubo e vidros
    b, perto = [], []
    comprovados = not bens.get("regional")
    veraneio = uso["valor"] == "LAZER_VERANEIO"
    limites = [("BENS_ALTOS", bens["min"], P.BENS_RELEVANTES,
                lambda v: f"suas compras para a casa nos últimos 3 anos valem hoje pelo menos {M.reais(v)}",
                f"Somando móveis, eletrodomésticos e eletrônicos, sua casa tem mais de {M.reais(P.BENS_RELEVANTES)} em bens?"),
               ("ELETRONICOS", bens["portateis"]["min"], P.PORTATEIS_RELEVANTES,
                lambda v: f"você tem pelo menos {M.reais(v)} em eletrônicos, os itens mais levados num arrombamento",
                f"Seus eletrônicos (TV, notebook, celulares, videogame) valem mais de {M.reais(P.PORTATEIS_RELEVANTES)}?")]
    forcas = []
    if comprovados and not veraneio:
        for codigo, valor, limite, texto, pergunta in limites:
            forca = _forca_por_limite(valor, limite)
            if valor >= limite:
                b.append(prova(codigo, texto(valor)))
                forcas.append(forca)
            if forca == "no_limite":
                perto.append((abs(valor / limite - 1), codigo, pergunta))
        if r.gastos_vidracaria_24m > 0:
            b.append(prova("VIDROS", f"você gastou {M.reais(r.gastos_vidracaria_24m)} com vidraçaria nos últimos 2 anos, "
                                     f"e vidro quebrado custa caro para repor"))
            forcas.append("clara")
    if b and tipo["valor"] == "CASA":
        b.append(prova("CASA_SEM_CONDOMINIO", "a casa fica fora de condomínio, mais exposta a arrombamento"))
    # clara se alguma prova é clara; no limite se a decisão (sim ou não) depende de um valor a menos de 15% do limite
    forca_b = "clara" if "clara" in forcas else "no_limite" if (forcas or perto) else "clara"
    pergunta_b = min(perto)[2] if forca_b == "no_limite" and perto else None
    nec_b = {"codigo": "ROUBO", "sim": bool(b), "forca": forca_b, "provas": b, "cobertura": COBRE["ROUBO"],
             "pergunta": pergunta_b}

    # C · danos a terceiros
    c = []
    if tipo["valor"] in ("APARTAMENTO", "CASA_EM_CONDOMINIO"):
        c.append(prova("VIZINHOS", "em prédio ou condomínio, um vazamento ou incêndio no seu imóvel pode atingir o vizinho"))
    if any(familia_declarada(r)):
        c.append(prova("FAMILIA", "há dependentes ou pet na casa, e um acidente com eles pode atingir terceiros"))
    nec_c = {"codigo": "TERCEIROS", "sim": bool(c), "forca": "clara", "provas": c, "cobertura": COBRE["TERCEIROS"], "pergunta": None}
    return [nec_a, nec_b, nec_c]


def escolher_plano(r, tipo, vinculo, uso, bens):
    """O menor plano que cobre as necessidades: aluguel em jogo → Total; senão, roubo e vidros →
    Prático; senão → Essencial. Danos a terceiros entram como RC adicional (coberturas_adicionais)
    quando o plano não é o Total. A força da recomendação é a da necessidade que decidiu (ou,
    no Essencial e no Prático, a da necessidade logo acima, que pode mudar o plano)."""
    nec = {n["codigo"]: n for n in avaliar_necessidades(r, tipo, vinculo, uso, bens)}
    a, b = nec["ALUGUEL"], nec["ROUBO"]
    plano = "TOTAL" if a["sim"] else "PRATICO" if b["sim"] else "ESSENCIAL"
    forca = a["forca"] if plano == "TOTAL" else b["forca"]
    motivos = [{"plano": PLANO_DA_NECESSIDADE[n["codigo"]], "peso": 0, **p} for n in nec.values() if n["sim"] for p in n["provas"]]

    decisiva = a if plano == "TOTAL" else b if plano == "PRATICO" else None
    a_favor = [{"plano": plano, "peso": 0, **p} for p in decisiva["provas"][:2]] if decisiva else []
    patrimonio = M.motivos_de_patrimonio(vinculo["valor"], bens)
    if not a_favor and uso["valor"] == "LAZER_VERANEIO":
        a_favor = [{"plano": "ESSENCIAL", "peso": 0, "codigo": "VERANEIO",
                    "texto": "o imóvel é de lazer e fica vazio parte do tempo, quando fogo, água, vento e danos elétricos "
                             "seguem cobertos, mas o roubo do Prático não cobre residência desocupada"}, patrimonio[-1]]
    if not a_favor:   # sem aluguel nem roubo: o porquê é o patrimônio (antes, um "não há sinais")
        a_favor = patrimonio[:2]
    if not any("R$" in m["texto"] for m in a_favor):   # todo motivo leva pelo menos um número do próprio cliente
        a_favor = a_favor + [patrimonio[-1]]

    abaixo = {"ESSENCIAL": None, "PRATICO": "ESSENCIAL", "TOTAL": "PRATICO"}[plano]
    acima = {"ESSENCIAL": "PRATICO", "PRATICO": "TOTAL", "TOTAL": None}[plano]
    por_que_nao_abaixo = f"o {NOME_PLANO[abaixo]} não cobre {O_QUE_ACRESCENTA[plano]}" if abaixo else ""
    por_que_nao_acima = ""
    if acima:
        falta = {"PRATICO": "bens, eletrônicos ou gasto com vidros que peçam isso", "TOTAL": "aluguel em jogo"}[acima]
        por_que_nao_acima = (f"o {NOME_PLANO[acima]} acrescenta {O_QUE_ACRESCENTA[acima]}, e você está perto de precisar dele"
                             if acima == "PRATICO" and b["forca"] == "no_limite" else
                             f"o {NOME_PLANO[acima]} acrescenta {O_QUE_ACRESCENTA[acima]}, mas hoje não vemos {falta}")
    alt = acima if (acima == "PRATICO" and b["forca"] == "no_limite") else (abaixo or acima)
    texto_alt = (f"{NOME_PLANO[alt]}: acrescenta {O_QUE_ACRESCENTA[alt]}" if ORDEM_PLANO[alt] > ORDEM_PLANO[plano]
                 else f"{NOME_PLANO[alt]}: mais barato, sem {O_QUE_ACRESCENTA[plano]}")
    return {"plano": plano, "forca": forca, "necessidades": list(nec.values()), "motivos": motivos,
            "motivos_plano": a_favor, "alternativa": {"plano": alt, "texto": texto_alt},
            "pergunta_decisiva": b["pergunta"] if plano != "TOTAL" else None,
            "por_que_nao_abaixo": por_que_nao_abaixo, "por_que_nao_acima": por_que_nao_acima}


# --- Coberturas: maior perda provável (CG cl. 15.1, primeiro risco absoluto) ---

NOME_SINISTRO = {"DANOS_ELETRICOS": "danos elétricos", "DANOS_POR_AGUA": "danos por água",
                 "VENDAVAL_GRANIZO": "vendaval e granizo", "ROUBO_FURTO_ARROMBAMENTO": "roubo ou furto com arrombamento"}


GRUPO_DESASTRE = {"DANOS_POR_AGUA": ("agua", "chuvas intensas, alagamentos ou enxurradas"),
                  "VENDAVAL_GRANIZO": ("vento", "vendaval, ciclone ou granizo")}


def contexto_territorio(cob, r):
    """Frase com dado oficial do município para o motivo da cobertura, ou "" sem dado.
    Água e vento: registros da Defesa Civil (Atlas/S2iD). Danos elétricos: ranking da ANEEL.
    Ausência de registro não prova ausência de risco, por isso zero registros não gera frase."""
    mun = r.municipio_real
    if cob in GRUPO_DESASTRE:
        d = P.desastres(r.codigo_ibge_municipio)
        g, nome = GRUPO_DESASTRE[cob]
        if not d or int(d[f"{g}_registros_1991_2025"] or 0) == 0:
            return ""
        return (f"Em {mun}, a Defesa Civil registrou {d[f'{g}_registros_1991_2025']} ocorrências de {nome} desde 1991 "
                f"({d[f'{g}_registros_2016_2025']} nos últimos 10 anos; a última em {d[f'{g}_ultimo_ano']}).")
    if cob == "DANOS_ELETRICOS":
        e = P.continuidade_energia(r.codigo_ibge_municipio)
        if not e:
            return ""
        return (f"A distribuidora de {mun} ({e['distribuidora']}) ficou em {e['posicao_2025']}º de {e['total_grandes_2025']} "
                f"no ranking de continuidade da ANEEL de 2025 (1º = menos quedas de energia).")
    return ""


def faixa_bruta_incendio(ctx):
    rec, bens, im = ctx["imovel"]["reconstrucao"], ctx["bens"], ctx["imovel"]
    if im.get("estrutura_do_locador"):
        return bens["min"], bens["max"]
    if im["segundo_risco"]:
        a, b = P.FRACAO_ACABAMENTOS
        return rec[0] * a + bens["min"], rec[1] * b + bens["max"]
    return rec[0] + bens["min"], rec[1] + bens["max"]


def dimensionar(cob, ctx):
    """Faixa mín/máx de uma cobertura + dados, regra, justificativa, o que confirmar e observação."""
    r, tipo, vinculo, uso, area, bens, im = (ctx[k] for k in ("r", "tipo", "vinculo", "uso", "area", "bens", "imovel"))
    casa = tipo["valor"] in ("CASA", "CASA_EM_CONDOMINIO")
    rec = im["reconstrucao"]
    # Confiança de cada cobertura: o pior dos dados que ela usa (sugestão P1 do relatório de validação).
    # Área: cadastrada ALTA, estimada MÉDIA, da região BAIXA. Padrão: cadastrado ALTA, senão MÉDIA.
    # Bens: compras + vínculo forte ALTA, um dos dois MÉDIA, nenhum BAIXA. Sem SINAPI da UF: BAIXA.
    conf_fonte = "ALTA" if im["fonte_disponivel"] else "BAIXA"
    conf_padrao = "ALTA" if im["origem_padrao"] == "cadastrado" else "MEDIA"
    conf_estrutura = pior(area["confianca"], conf_padrao, conf_fonte)
    conf_base = pior(conf_estrutura, bens["confianca"])
    # RN-27: em imóvel alugado, o imóvel é do locador e o conteúdo é do locatário
    obs_aluguel = {"INQUILINO": "Imóvel alugado: beneficiários distintos (locador para o imóvel, locatário para o conteúdo).",
                   "PROPRIETARIO_LOCADOR": "Imóvel alugado a terceiros: os bens do inquilino são dele (locatário); "
                                           "confirme se o imóvel é alugado mobiliado com bens seus."}.get(vinculo["valor"], "")

    def saida(lo, hi, conf, dados_u, regra, just, confirmar="", obs=""):
        teto = P.LIMITES_COBERTURA.get(cob, (0, float("inf")))[1]
        bruto_lo, bruto_hi = min(lo, hi), max(lo, hi)
        lo, hi = faixa(lo, hi, cob)
        # Transparência sobre subseguro (Código Civil art. 778; D-07): a estimativa passa do limite do produto
        acima = "Toda a estimativa" if bruto_lo > teto else "O máximo estimado" if bruto_hi > teto else ""
        if acima:
            obs = (f"{obs} {acima} ({brl(arred(bruto_hi))}) passa do limite do produto "
                   f"({brl(teto)}): o valor acima do limite fica descoberto.").strip()
        pct = P.sinistros_pct(cob)
        if pct is not None:   # frequência real na carteira BB: só reforça o motivo, não muda o valor
            just = (f"{just} Na BB Seguros, {str(pct).replace('.', ',')}% dos acionamentos do residencial "
                    f"são de {NOME_SINISTRO[cob]} (jan/2023 a mai/2026).")
            ctx["fontes"].add(P.FONTE_SINISTROS)
        frase = contexto_territorio(cob, r)
        if frase:   # território: também só no texto
            just = f"{just} {frase}"
            ctx["fontes"].add(P.FONTE_ANEEL if cob == "DANOS_ELETRICOS" else P.FONTE_DESASTRES)
        return {"min": lo, "max": hi, "confianca": conf, "dados_utilizados": dados_u, "regra": regra,
                "justificativa": just, "confirmar": confirmar, "observacao": obs,
                "limitada_pelo_produto": bool(acima),
                # valor sugerido para o app: o meio da faixa (escolher o mínimo deixa subseguro: ITV 0,60)
                "sugerido": min(max(arred((lo + hi) / 2), lo), hi)}

    seus_bens = M.faixa_reais(bens["min"], bens["max"])
    # Bens presumidos (sem compras) são estimativa, não compra: o texto não pode dizer "você comprou" (RN-09)
    estimados = bool(bens.get("regional"))
    repor = "repor os seus bens, que estimamos" if estimados else "repor o que você comprou para a casa,"
    repoe = "repõe os seus bens, que estimamos" if estimados else "repõe o que você comprou para a casa,"
    custo = f"{brl(im['custo_m2'][0])}–{brl(im['custo_m2'][1])}/m² (SINAPI {r.uf_real} até {P.fonte_custo(r.uf_real)}"
    f_lo, f_hi = im["fator_padrao"]
    if f_lo != f_hi:
        custo += f", padrão {im['origem_padrao']}: fator {f_lo:.2f} a {f_hi:.2f}".replace(".", ",")
    custo += ")"
    if cob == "INCENDIO_RAIO_EXPLOSAO_FUMACA":
        lo, hi = faixa_bruta_incendio(ctx)
        if im.get("estrutura_do_locador"):
            regra = "bens do inquilino (a estrutura é do locador; entra se o contrato pedir)"
            obs = obs_aluguel
            just = (f"O imóvel é do proprietário, e o seguro contra fogo da estrutura é dele (Lei do Inquilinato, art. 22, VIII): "
                    f"a faixa protege o que é seu, {seus_bens}. Se o seu contrato pedir que você segure o imóvel, inclua a "
                    f"reconstrução, cerca de {M.reais((rec[0] + rec[1]) / 2)}.")
        elif im["segundo_risco"]:
            regra = f"área {area['min']:.0f}–{area['max']:.0f} m² × {custo} × 25%–40% (acabamentos) + bens"
            obs = "Segundo risco (CG cl. 15.2): a estrutura é paga primeiro pelo seguro do condomínio ou do financiamento. " + obs_aluguel
            a, b = P.FRACAO_ACABAMENTOS
            just = (f"A estrutura tem seguro próprio (condomínio ou financiamento); o seu paga os acabamentos, estimados em "
                    f"{M.faixa_reais(rec[0] * a, rec[1] * b)}, e {repoe} {seus_bens}.")
        else:
            regra = f"área {area['min']:.0f}–{area['max']:.0f} m² × {custo} + bens"
            obs = "Limite único prédio + conteúdo, com prioridade do prédio (CG cl. 5.5–5.6). " + obs_aluguel
            just = (f"Se um incêndio atingir o imóvel, reconstruir custaria {M.faixa_reais(rec[0], rec[1])} pelo custo oficial "
                    f"de construção, e {repor} {seus_bens}. Com limite único, a reconstrução é paga primeiro.")
        c = saida(lo, hi, conf_base, "área, tipo, vínculo, UF, padrão, compras 36m, bens; SINAPI, CUB, IPCA", regra, just,
                  "Área do imóvel e valor dos bens", obs.strip())
        c["valor_em_risco"] = arred((lo + hi) / 2)   # meio da estimativa, antes dos limites (para o ITV)
        c["valor_em_risco_max"] = arred(hi)            # cenário pessimista, para medir o sugerido sem circularidade
        c["sugerido"] = min(max(c["valor_em_risco"], c["min"]), c["max"])   # o valor em risco, dentro da faixa
        return c
    if cob == "DANOS_POR_AGUA":
        m = bens["molhaveis"]
        rec_a = (0, 0) if im.get("estrutura_do_locador") else rec   # piso e paredes são do locador
        return saida(0.5 * m["min"] + 0.03 * rec_a[0], m["max"] + 0.08 * rec_a[1], conf_base, "bens molháveis, reconstrução",
                     "50%–100% dos bens molháveis + 3%–8% da reconstrução (pisos e acabamentos)",
                     f"Um cano rompido ou uma chuva forte estraga móveis e eletrodomésticos, e os seus valem hoje "
                     f"{M.faixa_reais(m['min'], m['max'])}. A faixa cobre esses bens e parte de pisos e paredes.")
    if cob == "VENDAVAL_GRANIZO":
        a, b = (0.10, 0.20) if casa else (0.02, 0.05)
        if im.get("estrutura_do_locador"):   # telhado é do locador: o inquilino protege os bens que a chuva alcança
            m = bens["molhaveis"]
            return saida(m["min"] * a, m["max"] * b, conf_base, "bens molháveis",
                         f"{a:.0%}–{b:.0%} dos bens molháveis (o telhado é do locador)",
                         f"O telhado é do proprietário; se o vento abrir o telhado ou uma janela, a chuva estraga os seus bens: "
                         f"{M.faixa_reais(m['min'] * a, m['max'] * b)}.")
        onde = ("Vento e granizo atingem primeiro o telhado: refazer de 10% a 20% de uma casa como a sua custa" if casa else
                "Em apartamento, vento e granizo atingem sobretudo janelas e esquadrias: repor de 2% a 5% do imóvel custa")
        return saida(rec[0] * a, rec[1] * b, conf_estrutura, "tipo, reconstrução",
                     f"{a:.0%}–{b:.0%} da reconstrução", f"{onde} {M.faixa_reais(rec[0] * a, rec[1] * b)}.")
    if cob == "IMPACTO_VEICULOS_TERRESTRES":
        return saida(10000, 20000 if casa else 10000, "MEDIA", "tipo do imóvel",
                     "padrão do produto (casa até R$ 20 mil)",
                     "Um carro desgovernado atinge primeiro muro, portão e fachada; por isso a casa vai até R$ 20 mil." if casa else
                     "Em apartamento, um carro raramente atinge a sua unidade; fica no valor padrão de R$ 10 mil.")
    if cob == "QUEDA_AERONAVE":
        return saida(10000, 10000, "MEDIA", "padrão do produto", "padrão do produto",
                     "Evento raro: fica no valor padrão do produto, R$ 10 mil, sem precisar de pergunta.")
    if cob == "DANOS_ELETRICOS":
        e = bens["eletricos"]
        return saida(e["min"], e["max"], bens["confianca"], "compras de eletrônicos e eletrodomésticos (36m), bens vinculados; IPCA",
                     "eletrônicos + eletrodomésticos: comprovado → estoque, a preço de hoje",
                     f"Seus eletrônicos e eletrodomésticos valem hoje {M.faixa_reais(e['min'], e['max'])}, e um pico de energia "
                     f"pode queimar vários de uma vez. Desgaste e mau uso não são cobertos.", "Principais aparelhos da casa")
    if cob == "ROUBO_FURTO_ARROMBAMENTO":
        p = bens["portateis"]
        obs = "Não cobre joias, relógios, dinheiro, drones nem bicicleta fora de casa (CG cl. 6; Roubo 2.1)."
        if uso["valor"] == "LAZER_VERANEIO":
            obs += " Residência desocupada não é coberta."
        return saida(p["min"], p["max"], bens["confianca"], "compras de eletrônicos (36m), bens vinculados; IPCA",
                     "eletrônicos e portáteis: comprovado → estoque, a preço de hoje",
                     f"Seus eletrônicos, os itens mais levados num arrombamento, valem hoje {M.faixa_reais(p['min'], p['max'])}; "
                     f"a faixa repõe esses bens a preço de hoje.", "Bens portáteis de maior valor", obs)
    if cob == "QUEBRA_DE_VIDROS":
        base = (3000, 8000) if casa else (2000, 5000)
        return saida(base[0], max(base[1], r.gastos_vidracaria_24m * 1.2), "MEDIA" if r.gastos_vidracaria_24m > 0 else "BAIXA",
                     "tipo do imóvel, gastos com vidraçaria 24m", "faixa por tipo, ampliada para 1,2 × o gasto com vidraçaria",
                     (f"Você gastou {M.reais(r.gastos_vidracaria_24m)} com vidraçaria nos últimos 2 anos; a faixa cobre janelas, "
                      f"box e tampos de vidro." if r.gastos_vidracaria_24m > 0 else
                      f"Num{'a casa' if casa else ' apartamento'} de cerca de {area['valor']} m², repor box, janelas e "
                      f"tampos de vidro costuma custar {M.faixa_reais(*base)}."), "Há vidros grandes (sacada, box, fachada)?")
    if cob == "RESPONSABILIDADE_CIVIL_FAMILIAR":
        if tipo["valor"] in ("APARTAMENTO", "CASA_EM_CONDOMINIO"):
            # a unidade vizinha tem tamanho parecido com a do cliente (mesmo prédio ou condomínio)
            viz = area["valor"]
            lo, hi = viz * im["custo_m2"][0] * 0.30, viz * im["custo_m2"][1] * 0.60
            regra = f"reparo de uma unidade vizinha do mesmo tamanho: {viz} m² × {custo} × 30%–60%"
        else:
            lo, hi, regra = 30000, 60000, "casa: faixa de referência de danos a terceiros"
        just = (f"Um vazamento ou incêndio no seu imóvel pode atingir a unidade vizinha, de tamanho parecido com a sua "
                f"(cerca de {area['valor']} m²): repará-la custa {M.faixa_reais(lo, hi)}, e a cobertura paga isso no seu lugar."
                if tipo["valor"] in ("APARTAMENTO", "CASA_EM_CONDOMINIO") else
                f"Numa casa de cerca de {area['valor']} m², o risco a terceiros vem de muro, telhado ou árvore que atinge o "
                f"vizinho, ou de um acidente com dependentes ou pet; a faixa de referência vai de R$ 30 mil a R$ 60 mil.")
        return saida(lo, hi, "MEDIA", "tipo do imóvel; SINAPI, CUB", regra, just)
    if cob == "PERDA_PAGAMENTO_ALUGUEL":
        m_lo, m_hi = P.MESES_PERDA_ALUGUEL
        aluguel_m2 = P.aluguel_m2(r.uf_real)
        if vinculo["valor"] == "INQUILINO":
            mensal, conf, fonte = (r.valor_aluguel_recorrente,) * 2, "ALTA", "aluguel pago (transações)"
        elif vinculo["valor"] == "PROPRIETARIO_LOCADOR":
            mensal, conf, fonte = (r.valor_medio_credito_recorrente,) * 2, "MEDIA", "aluguel recebido (transações)"
        elif aluguel_m2:
            mensal = (aluguel_m2 * area["min"], aluguel_m2 * area["max"])
            conf, fonte = "MEDIA", f"FipeZAP set/2026: {brl(aluguel_m2)}/m² × área"
            ctx["fontes"].add("FipeZAP Locação set/2026 (Fipe)")
        else:
            mensal, conf, fonte = (rec[0] * 0.004, rec[1] * 0.005), "BAIXA", "0,4%–0,5% do valor do imóvel"
        just = {"INQUILINO": f"Você paga {M.reais(mensal[0])} de aluguel por mês; se o imóvel ficar inabitável, a faixa paga "
                             f"outra moradia por {m_lo} a {m_hi} meses.",
                "PROPRIETARIO_LOCADOR": f"Você recebe cerca de {M.reais(mensal[0])} de aluguel por mês; se o imóvel precisar de "
                                        f"reparo, a faixa repõe de {m_lo} a {m_hi} meses."}.get(
            vinculo["valor"], f"Enquanto o imóvel é reparado, você precisaria morar em outro lugar: um imóvel parecido custa "
                              f"{M.faixa_reais(*mensal)} por mês, e a faixa cobre de {m_lo} a {m_hi} meses.")
        return saida(mensal[0] * m_lo, mensal[1] * m_hi, conf, fonte, f"aluguel mensal × {m_lo} a {m_hi} meses", just,
                     "" if conf == "ALTA" else "Valor de aluguel de um imóvel equivalente")
    if cob == "DESPESAS_EMERGENCIAIS":
        # sobre a faixa de incêndio já ajustada aos limites do produto, como diz a regra
        lo, hi = faixa(*faixa_bruta_incendio(ctx), "INCENDIO_RAIO_EXPLOSAO_FUMACA")
        return saida(lo * 0.02, hi * 0.05, conf_base, "faixa de incêndio", "2%–5% da faixa de incêndio",
                     f"Lona no telhado, retirada de entulho e outras medidas urgentes para o dano não aumentar: de 2% a 5% "
                     f"da faixa de incêndio, ou {M.faixa_reais(lo * 0.02, hi * 0.05)}.")
    raise ValueError(cob)


# --- Perguntas e confiança -----------------------------------------------------

def valor_da_informacao(area, bens, imovel, largura_incendio=None):
    """Quanto da faixa de incêndio (R$ entre mínimo e máximo) cada resposta pode eliminar.
    É a mesma ideia das seguradoras digitais: perguntar primeiro o que mais aperta a faixa.
    `largura_incendio`: largura da faixa entregue, já nos limites do produto. Área e padrão só
    mexem no incêndio, então não podem prometer apertar mais do que essa largura. Os bens
    mexem também em danos elétricos, água e roubo, e ficam sem esse teto."""
    frac = P.FRACAO_ACABAMENTOS[1] if imovel["segundo_risco"] else 1.0
    lo_m2, hi_m2 = imovel["custo_m2_base"]
    f_lo, f_hi = imovel["fator_padrao"]
    valor = {"BENS": bens["max"] - bens["min"]}
    if area["natureza"] == "ESTIMADO":
        valor["AREA"] = (area["max"] - area["min"]) * hi_m2 * f_hi * frac
    if f_hi > f_lo:
        valor["PADRAO"] = area["max"] * hi_m2 * (f_hi - f_lo) * frac
    if largura_incendio is not None:
        for k in ("AREA", "PADRAO"):
            if k in valor:
                valor[k] = min(valor[k], largura_incendio)
    return valor


def coberturas_adicionais(r, tipo, plano):
    """Coberturas de planos acima que entram como adicional (guia 9.2: as coberturas do Prático
    e do Total podem ser incluídas ou excluídas). Hoje uma regra: dependentes ou pet informados +
    imóvel em prédio ou condomínio → RC familiar, sem levar o cliente ao Total inteiro."""
    adicionais = []
    predio = tipo["valor"] in ("APARTAMENTO", "CASA_EM_CONDOMINIO")
    familia = any(familia_declarada(r))
    if plano != "TOTAL" and (predio or familia):   # necessidade C · danos a terceiros
        motivo = ("o vizinho está colado e há dependentes ou pet na casa" if predio and familia else
                  "o vizinho está colado: um vazamento ou incêndio no seu imóvel pode atingi-lo" if predio else
                  "há dependentes ou pet na casa, e um acidente com eles pode atingir terceiros")
        adicionais.append(("RESPONSABILIDADE_CIVIL_FAMILIAR", f"{motivo}; a RC familiar paga esse dano no seu lugar"))
    return adicionais


def montar_perguntas(r, pendencias, tipo, uso, vinculo, area, bens, plano=None, imovel=None, largura_incendio=None,
                     decisiva=None):
    """Até 3 perguntas, das que mais mudam o resultado (PLANO_UNIFICADO §7).
    Ordem: elegibilidade (95-100), as que mudam o plano (60-70) e depois as que mudam o
    valor, ordenadas pelo valor da informação (58, 56, 54: quem mais aperta a faixa vem antes).
    Pergunta de valor que aperta a faixa em menos de P.VALOR_MINIMO_PERGUNTA não é feita.
    Cada pergunta diz se é **obrigatória** (trava a contratação: elegibilidade, uso duvidoso,
    tipo duvidoso) ou **opcional** (só ajusta o valor: bens, área, acabamento...). Sem
    obrigatória, o cliente contrata direto com a faixa sugerida (1 toque de verdade)."""
    cand = [(p["prioridade"], p["pergunta"], p["codigo"]) for p in pendencias if p.get("pergunta")]
    if uso["confianca"] == "BAIXA":
        cand.append((70, "Este imóvel é onde você mora, uma casa de veraneio ou está alugado para outra pessoa?", "USO"))
    if decisiva:   # recomendação no limite: a resposta decide o plano (opcional; acima das de valor)
        cand.append((65, decisiva, "DECIDE_PLANO"))
    if r.credito_recorrente_compativel_aluguel == "SIM" and vinculo["valor"] != "PROPRIETARIO_LOCADOR":
        cand.append((60, "Você recebe aluguel referente a este imóvel?", "RECEBE_ALUGUEL"))
    textos = {
        "BENS": f"Seus móveis, eletrodomésticos e eletrônicos ficam entre {M.reais(bens['min'])} e {M.reais(bens['max'])}?",
        "AREA": f"Estimamos que o imóvel tem cerca de {area['valor']} m². Confere?",
        "PADRAO": "O acabamento do imóvel é simples, normal ou de alto padrão?",
    }
    if imovel:
        vdi = valor_da_informacao(area, bens, imovel, largura_incendio)
        vdi = {k: v for k, v in vdi.items() if v >= P.VALOR_MINIMO_PERGUNTA}
    else:
        vdi = {"BENS": 1, **({"AREA": 0} if area["natureza"] == "ESTIMADO" else {})}
    for i, cod in enumerate(sorted(vdi, key=lambda c: -vdi[c])):
        cand.append((58 - 2 * i, textos[cod], cod))
    if tipo.get("diverge"):
        cand.append((40, "O imóvel é um apartamento ou uma casa?", "TIPO"))
    if vinculo["valor"] == "INQUILINO" and imovel and not imovel["segundo_risco"]:
        # Lei do Inquilinato, art. 22, VIII: o seguro contra fogo é do locador, salvo contrato em contrário.
        # A resposta decide se o incêndio inclui a reconstrução ou só os bens (opcional; não trava).
        cand.append((59, "O seu contrato de aluguel pede que você faça o seguro do imóvel, e não só dos seus bens?",
                     "SEGURO_DO_IMOVEL"))
    if vinculo["valor"] == "PROPRIETARIO":
        cand.append((30, "O imóvel é seu e já está quitado?", "VINCULO"))
    cand.sort(key=lambda x: -x[0])
    vdi = vdi if imovel else {}
    obrigatorias = {p["codigo"] for p in pendencias} | PERGUNTAS_QUE_TRAVAM
    return [{"prioridade": p, "texto": t, "codigo": c, "obrigatoria": c in obrigatorias,
             **({"reduz_faixa_ate": arred(vdi[c])} if c in vdi else {})}
            for p, t, c in cand[:P.MAX_PERGUNTAS]], len(cand)


# Perguntas que travam a contratação além das de elegibilidade: sem saber se a pessoa mora no
# imóvel ou se ele é casa ou apartamento, a própria recomendação pode mudar.
PERGUNTAS_QUE_TRAVAM = {"USO", "TIPO"}


def peso_dado(d, campo):
    """Quanto um dado vale (0 a 1) = peso da fonte × frescor.
    Frescor = 0,5 ** (idade do sinal / meia-vida do campo): dado antigo vale menos."""
    if d.get("natureza") == "CONFIRMADO":
        return 1.0
    fonte = P.PESO_FONTE.get(d.get("fonte_tipo", "INFERIDO"), 0.6)
    return fonte * 0.5 ** (d.get("idade_meses", 0) / P.MEIA_VIDA_MESES.get(campo, 12))


def campos_faltantes(r):
    """Campos do imóvel que vieram vazios no cadastro (dimensão completude)."""
    faltam = []
    for c in P.CAMPOS_COMPLETUDE:
        v = getattr(r, c, None)
        if c == "area_cadastrada_m2":
            vazio = not (v is not None and v > 0)
        else:
            vazio = str(v).upper() in ("NAO_DISPONIVEL", "NAN", "", "NONE")
        if vazio:
            faltam.append(c)
    return faltam


NOME_CAMPO = {"area": "área", "bens": "valor dos bens", "uso": "uso do imóvel", "vinculo": "vínculo", "tipo": "tipo do imóvel"}


def classe_dado(d, campo=None):
    """OBSERVADO (documento, transação ou confirmado), ESTIMADO (derivado ou inferido) ou PRESUMIDO.
    Dado antigo vale menos: observado com idade maior que a meia-vida do campo conta como ESTIMADO."""
    if d.get("natureza") == "CONFIRMADO":
        return "OBSERVADO"
    classe = P.CLASSE_FONTE.get(d.get("fonte_tipo", "INFERIDO"), "ESTIMADO")
    if classe == "OBSERVADO" and campo and d.get("idade_meses", 0) > P.MEIA_VIDA_MESES.get(campo, 12):
        d["antigo"] = True
        return "ESTIMADO"
    return classe


def confianca_geral(campos, elegibilidade, pendencias, faltantes=()):
    """Nível por regra sobre os 5 dados críticos (sem nota de corte):
    BAIXA: área ou bens presumidos, ou um dado presumido junto com outro estimado;
    ALTA: os 5 observados, elegível e sem pendência; MÉDIA: o resto.
    A nota de 0 a 100 (peso da fonte × frescor, com desconto por campo vazio) fica
    só como detalhe para ordenar casos; ela não decide o nível."""
    pesos = {"tipo": 1, "vinculo": 1, "uso": 1, "area": 2, "bens": 2}
    for k in pesos:
        campos[k]["peso"] = round(peso_dado(campos[k], k), 3)
        campos[k]["classe"] = classe_dado(campos[k], k)
    score = sum(pesos[k] * campos[k]["peso"] for k in pesos) / sum(pesos.values())
    score *= 1 - sum(P.PENALIDADE_COMPLETUDE[c] for c in faltantes)

    ordem = ("area", "bens", "uso", "vinculo", "tipo")   # do que mais pesa no valor ao que menos pesa
    presumidos = [k for k in ordem if campos[k]["classe"] == "PRESUMIDO"]
    estimados = [k for k in ordem if campos[k]["classe"] == "ESTIMADO"]
    if {"area", "bens"} & set(presumidos) or (presumidos and estimados):
        nivel = "BAIXA"
    elif not presumidos and not estimados and elegibilidade == "SIM" and not pendencias:
        nivel = "ALTA"
    else:
        nivel = "MEDIA"
    partes = []
    if presumidos:
        partes.append("presumido: " + ", ".join(NOME_CAMPO[k] for k in presumidos))
    if estimados:
        partes.append("estimado: " + ", ".join(NOME_CAMPO[k] + (" (dado antigo)" if campos[k].get("antigo") else "") for k in estimados))
    if pendencias and elegibilidade == "SIM":
        partes.append("elegibilidade a confirmar")
    motivo = "; ".join(partes) or "todos os dados críticos observados"
    return nivel, round(score * 100), motivo


# --- Orquestração --------------------------------------------------------------

FONTES_SEMPRE = [f"SINAPI {P.referencia('sinapi_uf.csv', 'mes_referencia') or '(valor neutro)'} (IBGE)",
                 "CUB R8-N oficial dos Sinduscons",
                 f"IPCA 12m até {P.referencia('ipca_mensal.csv', 'data')[3:] or '(sem dado)'}, série 433 (Banco Central)",
                 "Condições Gerais BB Seguro Residencial v1.4"]


def _limpo(v):
    """Converte tipos do numpy para tipos nativos (para o JSON)."""
    if isinstance(v, (np.floating, np.integer)):
        return float(v)
    if isinstance(v, np.bool_):
        return bool(v)
    if isinstance(v, dict):
        return {k: _limpo(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_limpo(x) for x in v]
    return v


def processar_caso(r, bens_imovel, cal, catalogo, outro_principal=False, confirmados=(), n_imoveis=None):
    """A ficha de um cliente-imóvel. Usada pelo processar(), pelos testes e pela API.
    `confirmados`: campos que o cliente confirmou (passam a valer o máximo na confiança).
    `n_imoveis`: quantos imóveis o cliente tem na base (para o seguro já existente)."""
    tipo, vinculo = inferir_tipo(r), inferir_vinculo(r)
    uso, area = inferir_uso(r, outro_principal), inferir_area(r, cal)
    bens = estimar_bens(r, bens_imovel, cal)
    imovel = valor_imovel(r, tipo, vinculo, area, cal)
    eleg, pendencias, avisos = avaliar_elegibilidade(r, uso, n_imoveis)
    rec = escolher_plano(r, tipo, vinculo, uso, bens)
    ctx = {"r": r, "tipo": tipo, "vinculo": vinculo, "uso": uso, "area": area, "bens": bens,
           "imovel": imovel, "fontes": set()}
    coberturas = [{"cobertura": cob, "tipo": "FIXA", **dimensionar(cob, ctx)} for cob in catalogo[rec["plano"]]]
    rec["adicionais"] = []
    for cob, motivo in coberturas_adicionais(r, tipo, rec["plano"]):
        c = {"cobertura": cob, "tipo": "ADICIONAL", **dimensionar(cob, ctx)}
        c["observacao"] = (f"Cobertura adicional ao plano {NOME_PLANO[rec['plano']]} (guia 9.2): {motivo}. " + c["observacao"]).strip()
        coberturas.append(c)
        rec["adicionais"].append({"cobertura": cob, "motivo": motivo})
    if any(a["cobertura"] == "RESPONSABILIDADE_CIVIL_FAMILIAR" for a in rec["adicionais"]) and rec["por_que_nao_acima"]:
        rec["por_que_nao_acima"] = rec["por_que_nao_acima"].replace(
            "o conserto de danos a terceiros, a perda de aluguel e as despesas emergenciais",
            "a perda de aluguel e as despesas emergenciais (a RC familiar já entra como adicional)")
    if rec["plano"] == "ESSENCIAL":   # sem roubo no plano, o aviso sobre roubo não se aplica
        avisos = [a for a in avisos if "roubo" not in a]
    inc = next(c for c in coberturas if c["cobertura"] == "INCENDIO_RAIO_EXPLOSAO_FUMACA")
    perguntas, n_cand = montar_perguntas(r, pendencias, tipo, uso, vinculo, area, bens, rec["plano"], imovel,
                                         inc["max"] - inc["min"], rec["pergunta_decisiva"])
    campos = {"tipo": tipo, "vinculo": vinculo, "uso": uso, "area": area, "bens": bens}
    for k in confirmados:
        campos[k]["natureza"] = "CONFIRMADO"
    faltantes = [c for c in campos_faltantes(r) if not (c == "area_cadastrada_m2" and "area" in confirmados)]
    nivel, score, motivo_conf = confianca_geral(campos, eleg, pendencias, faltantes)
    jornada, motivo_jornada = escolher_jornada(r, eleg, pendencias, nivel, uso, perguntas)
    return _limpo({
        "cliente_id": r.cliente_id, "imovel_id": r.imovel_id,
        "local": f"{r.municipio_real}/{r.uf_real}", "complemento": r.complemento,
        "canal_digital": {"usuario_app": r.usuario_app, "maturidade_digital": int(r.indice_maturidade_digital)},
        "campos": campos,
        "valor_imovel": {"custo_m2": [round(x, 2) for x in imovel["custo_m2"]],
                         "fator_padrao": list(imovel["fator_padrao"]),
                         "origem_padrao": imovel["origem_padrao"],
                         "reconstrucao_min": arred(imovel["reconstrucao"][0]), "reconstrucao_max": arred(imovel["reconstrucao"][1]),
                         "segundo_risco": imovel["segundo_risco"], "estrutura_do_locador": imovel["estrutura_do_locador"]},
        "elegibilidade": eleg, "pendencias": pendencias, "avisos": avisos,
        **rec,
        "coberturas": coberturas, "perguntas": perguntas, "perguntas_candidatas": n_cand,
        "confianca": nivel, "confianca_score": score, "confianca_motivo": motivo_conf,
        "completude": {"faltantes": faltantes, "pct": round(100 * (1 - len(faltantes) / len(P.CAMPOS_COMPLETUDE)))},
        # canal: o que o protótipo lê (1 toque × gerente); jornada: o caminho detalhado
        "canal": "ONE_CLICK" if jornada in ("UM_TOQUE", "APP_COM_PERGUNTAS") else "GERENTE",
        "jornada": jornada, "motivo_jornada": motivo_jornada,
        "fontes": FONTES_SEMPRE + sorted(ctx["fontes"]),
    })


def escolher_jornada(r, eleg, pendencias, nivel, uso, perguntas=()):
    """Gerente é o último recurso, porque custa caro (mentoria de 28/10). Ordem:
    - SEM_NOVA_PROPOSTA: não elegível; o app só informa e a ficha serve para revisar a apólice;
    - GERENTE: o app não resolve: sinal de obra (pede conversa) ou cliente sem o app;
    - APP_COM_PERGUNTAS: há pergunta obrigatória (elegibilidade, "você mora no imóvel?") ou pouca
      familiaridade com o app (modo simples, D-03). Na confiança baixa, o app pergunta primeiro;
      o gerente só entra se a resposta mudar o caso ou não vier;
    - UM_TOQUE: nenhuma pergunta trava; contrata com a faixa sugerida e as perguntas só ajustam
      o valor. O relatório do gerente (a ficha) existe para todos os casos."""
    if eleg != "SIM":
        return "SEM_NOVA_PROPOSTA", "não elegível para nova proposta: o app informa e a ficha serve para revisar a apólice atual"
    razoes = []
    if any(p["codigo"] == "POSSIVEL_REFORMA" for p in pendencias):
        razoes.append("sinal de obra ou reforma, que impede a contratação e pede conversa")
    if r.usuario_app != "SIM":
        razoes.append("o cliente não usa o app")
    if razoes:
        return "GERENTE", "; ".join(razoes)
    obrigatorias = [p["codigo"] for p in perguntas if p.get("obrigatoria")]
    if nivel == "BAIXA":
        return "APP_COM_PERGUNTAS", ("confiança baixa: o app pergunta primeiro se o cliente mora no imóvel; "
                                     "o gerente entra se a resposta mudar o caso ou não vier")
    if obrigatorias or pendencias:
        return "APP_COM_PERGUNTAS", "o app confirma " + ", ".join(c.lower().replace("_", " ") for c in obrigatorias or
                                                                   [p["codigo"] for p in pendencias])
    if r.indice_maturidade_digital < P.MATURIDADE_MIN_ONE_CLICK:
        return "APP_COM_PERGUNTAS", "pouca familiaridade com o app: modo simples e ajuda contextual"
    return "UM_TOQUE", "nenhuma pergunta trava a contratação: contrata com a faixa sugerida e as perguntas só ajustam o valor"


def processar(dados, cal):
    c, e, s, b = dados["clientes"], dados["enderecos_imoveis"], dados["sinais_imobiliarios"], dados["bens_compras"]
    m = e.merge(s, on=["imovel_id", "cliente_id"]).merge(c, on="cliente_id")
    principais = m[m.endereco_principal_compativel == "SIM"].groupby("cliente_id").imovel_id.apply(set).to_dict()
    n_imoveis = m.groupby("cliente_id").imovel_id.nunique().to_dict()
    bens_por_imovel = dict(tuple(b.groupby("imovel_id_referencia")))
    catalogo = dados["catalogo"].groupby("plano").cobertura_fixa.apply(list).to_dict()
    vazio = b.iloc[0:0]

    fichas = []
    for r in m.itertuples(index=False):
        outro_principal = bool(principais.get(r.cliente_id, set()) - {r.imovel_id})
        fichas.append(processar_caso(r, bens_por_imovel.get(r.imovel_id, vazio), cal, catalogo, outro_principal,
                                     n_imoveis=n_imoveis.get(r.cliente_id)))
    return fichas


NIVEL_TEXTO = {"ALTA": "alta", "MEDIA": "média", "BAIXA": "baixa"}


def justificativa(f):
    """O porquê para o cliente (texto em motivo.py): fato, valor em risco, o que fica
    descoberto, o que confirmar e a confiança, em linguagem simples."""
    return M.justificativa(f)


def para_templates(fichas, template):
    idx = {(f["cliente_id"], f["imovel_id"]): f for f in fichas}
    linhas = []
    for t in template.itertuples(index=False):
        f = idx[(t.cliente_id, t.imovel_id)]
        linhas.append({
            "cliente_id": f["cliente_id"], "imovel_id": f["imovel_id"],
            "elegivel": f["elegibilidade"],
            "motivo_inelegibilidade": "; ".join(p["texto"] for p in f["pendencias"]) if f["elegibilidade"] == "NAO" else "",
            "tipo_imovel_sugerido": f["campos"]["tipo"]["valor"],
            "uso_imovel_sugerido": f["campos"]["uso"]["valor"],
            "tipo_vinculo_sugerido": f["campos"]["vinculo"]["valor"],
            "plano_recomendado": f["plano"],
            "coberturas_recomendadas": "; ".join(c["cobertura"] for c in f["coberturas"]),
            "confianca_geral": f["confianca"],
            "justificativa_recomendacao": justificativa(f),
            "perguntas_confirmacao": " | ".join(("" if p.get("obrigatoria") else "(opcional) ") + p["texto"]
                                                for p in f["perguntas"]),
            "fontes_publicas_adicionais": "; ".join(f["fontes"]),
        })
    resultado = pd.DataFrame(linhas, columns=template.columns)
    cob = pd.DataFrame([{
        "cliente_id": f["cliente_id"], "imovel_id": f["imovel_id"], "cobertura": c["cobertura"],
        "faixa_valor_min": c["min"], "faixa_valor_max": c["max"], "confianca_estimativa": c["confianca"],
        "dados_utilizados": c["dados_utilizados"], "regra_calculo_utilizada": c["regra"],
        "justificativa": c["justificativa"], "informacao_a_confirmar": c["confirmar"],
        "observacao": (("Não elegível para nova proposta; valores só de referência. "
                        if f["elegibilidade"] == "NAO" else "") + c["observacao"]).strip(),
    } for f in fichas for c in f["coberturas"]])
    return resultado, cob
