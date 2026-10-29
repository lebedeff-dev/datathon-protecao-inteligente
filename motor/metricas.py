"""Evidências para a banca (guia §8): métricas da base de teste e casos contrastantes."""
import statistics
from collections import Counter
from types import SimpleNamespace

import pandas as pd

import assertividade as A
import motivo
import motor
import parametros as P


def _incendio_meio(f):
    c = next(c for c in f["coberturas"] if c["cobertura"] == "INCENDIO_RAIO_EXPLOSAO_FUMACA")
    return (c["min"] + c["max"]) / 2


def calcular_metricas(dados, cal, fichas, resultado, coberturas, segundos):
    n = len(fichas)
    m = (dados["enderecos_imoveis"].merge(dados["sinais_imobiliarios"], on=["imovel_id", "cliente_id"])
         .merge(dados["clientes"], on="cliente_id"))
    bens = dict(tuple(dados["bens_compras"].groupby("imovel_id_referencia")))
    vazio = dados["bens_compras"].iloc[0:0]
    catalogo = dados["catalogo"].groupby("plano").cobertura_fixa.apply(list).to_dict()
    por_id = {f["imovel_id"]: f for f in fichas}

    # Justiça: trocar renda e idade não pode mudar nada em quem tem compras ou bens (a renda só
    # entra nos bens de quem não tem nenhum dos dois; na base comum, nenhum caso).
    # Necessidade declarada: trocar dependentes e pet pode mudar só o plano, os motivos e as
    # perguntas; nunca a faixa de uma cobertura em comum, a elegibilidade, o canal ou a confiança.
    # Sensibilidade: área 10% maior deve aumentar (ou manter) o incêndio.
    mudou_justica, familia_fora_do_lugar, familia_muda_plano, variacoes, quedas = 0, 0, 0, [], 0
    fora_do_teste_justica = 0
    base_nivel, base_nivel_plano = {}, {}
    for r in m.itertuples(index=False):
        b = bens.get(r.imovel_id, vazio)
        base = motor.processar_caso(r, b, cal, catalogo)
        base_nivel[r.imovel_id] = base["confianca"]
        base_nivel_plano[r.imovel_id] = base["plano"]
        trocado = SimpleNamespace(**{**r._asdict(), "renda_mensal": 99999, "idade": 99,
                                     "origem_renda": "PRESUMIDA", "confianca_renda": "BAIXA"})
        trocada = motor.processar_caso(trocado, b, cal, catalogo)
        if base["campos"]["bens"].get("usou_renda"):   # sem compras a renda entra de propósito nos bens:
            fora_do_teste_justica += 1                  # o que não pode mudar é plano, elegibilidade, jornada e confiança
            mudou_justica += any(trocada[k] != base[k] for k in ("plano", "elegibilidade", "jornada", "confianca"))
        elif trocada != base:
            mudou_justica += 1
        sem_familia = 0 if (r.quantidade_dependentes or 0) > 0 or r.possui_pet_informado == "SIM" else 2
        outra = motor.processar_caso(SimpleNamespace(**{**r._asdict(), "quantidade_dependentes": sem_familia,
                                                        "possui_pet_informado": "SIM" if sem_familia else "NAO"}),
                                     b, cal, catalogo)
        familia_muda_plano += outra["plano"] != base["plano"]
        faixa = lambda f: {c["cobertura"]: (c["min"], c["max"]) for c in f["coberturas"]}
        fa, fo = faixa(base), faixa(outra)
        if any(fa[k] != fo[k] for k in fa.keys() & fo.keys()) or any(
                base[k] != outra[k] for k in ("elegibilidade", "canal", "confianca", "confianca_score", "campos")):
            familia_fora_do_lugar += 1
        maior = SimpleNamespace(**{**r._asdict(),
                                   "area_cadastrada_m2": r.area_cadastrada_m2 * 1.1,
                                   "pagamento_iptu_anual": r.pagamento_iptu_anual * 1.1,
                                   "energia_media_mensal_6m": r.energia_media_mensal_6m * 1.1})
        a, z = _incendio_meio(motor.processar_caso(r, b, cal, catalogo)), _incendio_meio(motor.processar_caso(maior, b, cal, catalogo))
        variacoes.append((z - a) / a * 100)
        quedas += z < a

    conf = Counter(f["confianca"] for f in fichas)

    # Estabilidade: mexer 20% nos pesos das fontes e no desconto de completude não pode mudar
    # o nível de nenhum caso (o nível vem de regra, não de corte na nota).
    peso_orig, pen_orig = dict(P.PESO_FONTE), dict(P.PENALIDADE_COMPLETUDE)
    mudou_nivel = 0
    try:
        for fator in (0.8, 1.2):
            P.PESO_FONTE.update({k: min(1.0, v * fator) for k, v in peso_orig.items()})
            P.PENALIDADE_COMPLETUDE.update({k: v * fator for k, v in pen_orig.items()})
            for r in m.itertuples(index=False):
                novo = motor.processar_caso(r, bens.get(r.imovel_id, vazio), cal, catalogo)
                mudou_nivel += novo["confianca"] != base_nivel[r.imovel_id]
    finally:
        P.PESO_FONTE.update(peso_orig)
        P.PENALIDADE_COMPLETUDE.update(pen_orig)

    # Estabilidade do plano (guia §8): ±5% nos valores (compras, bens, IPTU, energia, vidraçaria)
    # não deveria trocar o plano; quem troca está perto de um limiar e é listado.
    colunas = ["compras_moveis_36m", "compras_eletrodomesticos_36m", "compras_eletronicos_36m",
               "pagamento_iptu_anual", "energia_media_mensal_6m", "gastos_vidracaria_24m"]
    instaveis = []
    for r in m.itertuples(index=False):
        b = bens.get(r.imovel_id, vazio)
        for fator in (0.95, 1.05):
            x = SimpleNamespace(**{**r._asdict(), **{c: getattr(r, c) * fator for c in colunas}})
            b2 = b.assign(valor_bem_ponderado_referencia=b.valor_bem_ponderado_referencia * fator)
            if motor.processar_caso(x, b2, cal, catalogo)["plano"] != base_nivel_plano[r.imovel_id]:
                instaveis.append(r.imovel_id)
                break

    # Cumprimento da elegibilidade: cada regra do guia 9.1 e quantos casos ela pegou.
    regras_eleg = Counter(p["codigo"] for f in fichas for p in f["pendencias"])
    regras_eleg["NAO_ELEGIVEL"] = sum(f["elegibilidade"] == "NAO" for f in fichas)

    # Justiça por faixa de renda (como os testes de "impacto desigual" de crédito): a renda só entra nos
    # bens de quem não tem compras, mas pode chegar por tabela via bens (correlação 0,88 na base). A tabela
    # mostra, por quinto de renda, o plano e os bens comprovados, para provar que o plano segue os bens.
    por_renda = renda_por_quinto(m, por_id)

    # Ordenação: quanto menor a confiança, mais larga a faixa de incêndio (máx ÷ mín).
    largura = {}
    for nivel in ("ALTA", "MEDIA", "BAIXA"):
        xs = [c["max"] / c["min"] for f in fichas if f["confianca"] == nivel
              for c in f["coberturas"] if c["cobertura"] == "INCENDIO_RAIO_EXPLOSAO_FUMACA"]
        if xs:
            largura[nivel] = round(statistics.median(xs), 2)
    fixas_ok = sum(set(catalogo[f["plano"]]) <= {c["cobertura"] for c in f["coberturas"]} for f in fichas)
    esperados = set(dados["template"].imovel_id)
    return {
        "casos_processados": n,
        "processados_pct": round(100 * len(esperados & set(por_id)) / len(esperados), 1),
        "com_justificativa_pct": round(100 * (resultado.justificativa_recomendacao.str.len() > 0).mean(), 1),
        "completude_coberturas_fixas_pct": round(100 * fixas_ok / n, 1),
        "linhas_de_cobertura": len(coberturas),
        "faixas_vazias": int(coberturas.faixa_valor_min.isna().sum() + coberturas.faixa_valor_max.isna().sum()),
        "faixas_invertidas": int((coberturas.faixa_valor_min > coberturas.faixa_valor_max).sum()),
        "planos": dict(Counter(f["plano"] for f in fichas)),
        "elegibilidade": dict(Counter(f["elegibilidade"] for f in fichas)),
        "casos_com_confirmacao_de_elegibilidade": sum(bool(f["pendencias"]) for f in fichas),
        "elegibilidade_por_regra": dict(regras_eleg),
        "coberturas_adicionais": dict(Counter(a["cobertura"] for f in fichas for a in f.get("adicionais", []))),
        "estabilidade_plano_casos_que_mudam_com_valores_5pct": len(instaveis),
        "estabilidade_plano_casos_instaveis": instaveis,
        "casos_com_falha": n - len({f["imovel_id"] for f in fichas}),
        "confianca": dict(conf),
        "confianca_baixa_pct": round(100 * conf.get("BAIXA", 0) / n, 1),
        "confianca_estabilidade_casos_que_mudam_com_pesos_20pct": int(mudou_nivel),
        "confianca_largura_incendio_mediana": largura,
        "confianca_por_cobertura": {cob: dict(Counter(c["confianca"] for f in fichas for c in f["coberturas"]
                                                      if c["cobertura"] == cob))
                                    for cob in sorted({c["cobertura"] for f in fichas for c in f["coberturas"]})},
        "canal": dict(Counter(f["canal"] for f in fichas)),
        "jornada": dict(Counter(f["jornada"] for f in fichas)),
        # Recomendação por necessidades: quantos têm cada necessidade e quantos foram decididos por pouco
        "necessidades": {cod: sum(any(n["codigo"] == cod and n["sim"] for n in f["necessidades"]) for f in fichas)
                         for cod in ("ALUGUEL", "ROUBO", "TERCEIROS")},
        "forca_da_recomendacao": dict(Counter(f["forca"] for f in fichas)),
        "instaveis_marcados_no_limite_pct": round(100 * sum(por_id[i]["forca"] == "no_limite" for i in instaveis)
                                                  / len(instaveis), 1) if instaveis else 100.0,
        "gerente_pct_dos_elegiveis": round(100 * sum(f["jornada"] == "GERENTE" for f in fichas)
                                           / max(1, sum(f["elegibilidade"] == "SIM" for f in fichas)), 1),
        "gerente_motivos": dict(Counter(r for f in fichas if f["jornada"] == "GERENTE"
                                        for r in f["motivo_jornada"].split("; "))),
        "perguntas_media": round(sum(len(f["perguntas"]) for f in fichas) / n, 2),
        "perguntas_candidatas_media": round(sum(f["perguntas_candidatas"] for f in fichas) / n, 2),
        "perguntas_obrigatorias_media": round(sum(p.get("obrigatoria", False) for f in fichas for p in f["perguntas"]) / n, 2),
        "casos_sem_pergunta_obrigatoria": sum(not any(p.get("obrigatoria") for p in f["perguntas"]) for f in fichas),
        "teste_justica_casos_alterados": mudou_justica,
        "teste_justica_casos_sem_compras_so_decisoes": fora_do_teste_justica,
        "justica_por_quinto_de_renda": por_renda,
        "familia_declarada_muda_plano": int(familia_muda_plano),
        "familia_declarada_muda_valor_ou_confianca": int(familia_fora_do_lugar),
        "sensibilidade_area_10pct_incendio_media_pct": round(sum(variacoes) / n, 2),
        "sensibilidade_area_casos_com_queda": int(quedas),
        "tempo_segundos": round(segundos, 2),
        "backtest_fora_da_amostra": cal.get("backtest", {}),
        "mercado": metricas_de_mercado(fichas),
        "qualidade_do_motivo": qualidade_do_motivo(fichas),
        "dados_faltantes": dados_faltantes(fichas, cal),
        # o acerto de cada cálculo de dado faltante, com quantos casos da base usam cada um (assertividade.py)
        "assertividade": A.com_casos_no_teste(cal["assertividade"], fichas) if "assertividade" in cal else {},
    }


def dados_faltantes(fichas, cal):
    """Como cada lacuna foi tratada: quem tem tudo é fácil; a personalização vale para quem não tem."""
    area = [f["campos"]["area"] for f in fichas]
    origem = Counter(f["valor_imovel"]["origem_padrao"] for f in fichas)
    return {
        "area_cadastrada": sum(a["natureza"] == "OBSERVADO" for a in area),
        "area_estimada_por_iptu_e_energia": sum(a["natureza"] == "ESTIMADO" and not a.get("regional") for a in area),
        "area_pela_media_da_regiao": sum(bool(a.get("regional")) for a in area),
        "padrao_cadastrado": origem.get("cadastrado", 0),
        "padrao_estimado_pelo_iptu": origem.get("estimado pelo IPTU/m²", 0),
        "padrao_faixa_aberta_com_pergunta": origem.get("não cadastrado", 0),
        "padrao_faixa_calibrada_de_area_x_padrao": origem.get("faixa calibrada de área × padrão", 0),
        "bens_pela_media_da_regiao": sum(bool(f["campos"]["bens"].get("regional")) and not f["campos"]["bens"].get("usou_renda")
                                         for f in fichas),
        "bens_pela_regiao_e_renda": sum(bool(f["campos"]["bens"].get("usou_renda")) for f in fichas),
        "backtest_bens_sem_compras": cal.get("backtest_bens_sem_compras", {}),
        "teste_cep_da_base": cal.get("teste_cep", {}),
    }


def qualidade_do_motivo(fichas):
    """O porquê é o que a banca mais olha (mentoria de 28/10). Mede o texto que o cliente lê:
    nenhum motivo genérico, fato do próprio cliente, valor em risco, alternativas, sem
    jargão interno, tamanho de leitura e coberturas com texto personalizado."""
    import re
    textos = {f["imovel_id"]: motor.justificativa(f) for f in fichas}
    n, eleg = len(fichas), [f for f in fichas if f["elegibilidade"] == "SIM"]
    palavras = [len(t.split()) for t in textos.values()]
    por_cob = {}
    for f in fichas:
        for c in f["coberturas"]:
            por_cob.setdefault(c["cobertura"], []).append(c["justificativa"])
    pct = lambda k, tot: round(100 * k / tot, 1) if tot else 0.0
    return {
        "motivos_genericos": sum(any(m["codigo"] == "BASE" for m in f["motivos_plano"]) for f in fichas),
        "motivo_com_fato_do_cliente_pct": pct(sum(any("R$" in m["texto"] for m in f["motivos_plano"]) for f in fichas), n),
        "justificativa_com_valor_em_risco_pct": pct(sum(len(re.findall(r"R\$ \d", t)) >= 2 for t in textos.values()), n),
        "alternativas_mostradas_pct": pct(sum("acrescenta" in textos[f["imovel_id"]] or "Se você escolher menos" in textos[f["imovel_id"]]
                                              for f in eleg), len(eleg)),
        "justificativas_com_termo_interno": sum(any(x in t for x in motivo.TERMOS_INTERNOS) for t in textos.values()),
        "palavras_mediana": statistics.median(palavras),
        "palavras_max": max(palavras),
        "palavras_entre_60_e_120_pct": pct(sum(60 <= w <= 120 for w in palavras), n),
        "coberturas_texto_distinto_pct": {k: pct(len(set(v)), len(v)) for k, v in sorted(por_cob.items())},
        **personalizacao_do_motivo(fichas, textos),
    }


def _esqueleto(texto):
    """O texto sem os números: dois motivos com o mesmo esqueleto são o mesmo modelo com valores trocados."""
    import re
    return re.sub(r"R\$ ?[\d.,]+( mil| milhão| milhões)?|\d+[.,]?\d*%?º?", "#", texto)


def personalizacao_do_motivo(fichas, textos):
    """O motivo é feito para a pessoa ou é um modelo com números trocados? (plano de 28/10)
    - esqueletos_unicos: motivos cujo texto sem números é diferente de todos os outros;
    - semelhanca_media: quanto dois motivos têm em comum (sequências de 3 palavras, 0 = nada, 1 = iguais);
    - frase_mais_repetida_n: em quantos motivos aparece a frase (sem números) mais repetida;
    - cita_cidade_pct, com_fato_dos_vizinhos_pct, com_risco_da_cidade_pct."""
    import itertools
    import re
    esq = [_esqueleto(textos[f["imovel_id"]]) for f in fichas]
    tri = [set(zip(*(e.split()[i:] for i in range(3)))) for e in esq]
    pares = [len(a & b) / len(a | b) for a, b in itertools.combinations(tri, 2) if a | b]
    frases = Counter(fr.strip() for e in esq for fr in set(re.split(r"(?<=\.)\s", e)))
    contagem = Counter(esq)
    n = len(fichas)
    tem = lambda cond: round(100 * sum(cond(f, textos[f["imovel_id"]]) for f in fichas) / n, 1) if n else 0.0
    usa = lambda frase, t: bool(frase) and frase in t
    return {
        "esqueletos_unicos": sum(contagem[e] == 1 for e in esq),
        "semelhanca_media": round(statistics.mean(pares), 3) if pares else 0.0,
        "frase_mais_repetida_n": frases.most_common(1)[0][1] if frases else 0,
        "frase_mais_repetida": frases.most_common(1)[0][0] if frases else "",
        "cita_cidade_pct": tem(lambda f, t: motivo.na_cidade(f) in t),
        "com_fato_dos_vizinhos_pct": tem(lambda f, t: usa(motivo.fato_distintivo(f), t)),
        "com_risco_da_cidade_pct": tem(lambda f, t: usa(motivo.risco_do_lugar(f), t)),
    }


# Campos que uma cotação tradicional pede ao cliente: os 5 dados críticos do imóvel (tipo, uso,
# vínculo, área, valor dos bens), as 6 declarações de elegibilidade do guia §9.1 (comunidade,
# rural, tombado/condenado, obra, material combustível, seguro BB no endereço) e 1 valor por
# cobertura do plano (o app atual pede para digitar cada valor).
CAMPOS_DO_IMOVEL, DECLARACOES_ELEGIBILIDADE = 5, 6


def metricas_de_mercado(fichas):
    """Métricas que bancos e seguradoras acompanham, calculadas na base de teste:
    - STP (straight-through processing): % que pode ir direto ao One Click, sem pessoa no meio;
    - esforço: campos de uma cotação tradicional × perguntas da nossa jornada;
    - ITV (insurance-to-value): importância segurada de incêndio ÷ valor em risco estimado (meio da
      estimativa), no máximo e no mínimo da faixa. O mercado usa 80% como piso (cláusula de
      ITV/rateio); abaixo disso, há subseguro. Mostra o risco de o cliente escolher o mínimo;
    - faixas limitadas pelo produto: a estimativa passa do limite da cobertura;
    - aderência aos sinistros reais: % das recomendações com as coberturas que mais
      geram acionamentos na carteira residencial da BB Seguros."""
    n = len(fichas)
    eleg = sum(f["elegibilidade"] == "SIM" for f in fichas)
    pess = [c["sugerido"] / c["valor_em_risco_max"] for f in fichas for c in f["coberturas"]
            if c["cobertura"] == "INCENDIO_RAIO_EXPLOSAO_FUMACA" and c.get("valor_em_risco_max")]
    tradicional = [CAMPOS_DO_IMOVEL + DECLARACOES_ELEGIBILIDADE + len(f["coberturas"]) for f in fichas]
    nossas = [len(f["perguntas"]) for f in fichas]
    itv_max, itv_min = [], []
    for f in fichas:
        c = next(c for c in f["coberturas"] if c["cobertura"] == "INCENDIO_RAIO_EXPLOSAO_FUMACA")
        if c.get("valor_em_risco"):
            itv_max.append(c["max"] / c["valor_em_risco"])
            itv_min.append(c["min"] / c["valor_em_risco"])
    limitadas = Counter(c["cobertura"] for f in fichas for c in f["coberturas"] if c.get("limitada_pelo_produto"))
    mais_acionadas = [c for c in ("DANOS_ELETRICOS", "DANOS_POR_AGUA", "VENDAVAL_GRANIZO") if P.sinistros_pct(c) is not None]
    return {
        # STP honesto (crítica da banca): 1 toque = nenhuma pergunta obrigatória; "sem pessoa" inclui o app com perguntas
        "um_toque_pct_dos_elegiveis": round(100 * sum(f["jornada"] == "UM_TOQUE" for f in fichas) / max(1, eleg), 1),
        "sem_pessoa_pct_dos_elegiveis": round(100 * sum(f["jornada"] in ("UM_TOQUE", "APP_COM_PERGUNTAS") for f in fichas)
                                              / max(1, eleg), 1),
        "esforco_campos_cotacao_tradicional_media": round(statistics.mean(tradicional), 2),
        "esforco_perguntas_nossa_jornada_media": round(statistics.mean(nossas), 2),
        "esforco_reducao_pct": round(100 * (1 - sum(nossas) / sum(tradicional)), 1),
        "itv_incendio_no_maximo_mediana": round(statistics.median(itv_max), 2) if itv_max else None,
        "itv_incendio_no_maximo_abaixo_de_80pct_casos": sum(v < 0.8 for v in itv_max),
        "itv_incendio_no_minimo_mediana": round(statistics.median(itv_min), 2) if itv_min else None,
        "itv_incendio_no_minimo_abaixo_de_80pct_casos": sum(v < 0.8 for v in itv_min),
        # Sem circularidade: o sugerido contra o cenário pessimista (o máximo da estimativa, antes dos limites)
        "itv_sugerido_sobre_pessimista_mediana": round(statistics.median(pess), 2) if pess else None,
        "sugerido_cobre_80pct_do_pessimista_casos": sum(v >= 0.8 for v in pess),
        "faixas_limitadas_pelo_produto": dict(limitadas),
        "recomendacoes_com_coberturas_mais_acionadas_pct": round(100 * sum(
            set(mais_acionadas) <= {c["cobertura"] for c in f["coberturas"]} for f in fichas) / n, 1),
        "acionamentos_bb_cobertos_por_elas_pct": round(sum(P.sinistros_pct(c) for c in mais_acionadas), 1),
    }


def renda_por_quinto(m, por_id):
    """Por quinto de renda (Q1 = 20% de menor renda): casos, % de cada plano, % elegível e
    mediana dos bens comprovados. A regra dos 80% do crédito vale para a decisão que nega algo,
    aqui a elegibilidade: o menor % de elegíveis dividido pelo maior tem de ficar em 0,8 ou mais.
    O plano não é negativa; a tabela mostra que ele acompanha os bens comprovados e o vínculo."""
    q = m[["imovel_id", "renda_mensal"]].copy()
    q["quinto"] = pd.qcut(q.renda_mensal.rank(method="first"), 5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"])
    tabela = {}
    for nome, g in q.groupby("quinto", observed=True):
        fs = [por_id[i] for i in g.imovel_id]
        n = len(fs)
        pct = lambda cond: round(100 * sum(cond(f) for f in fs) / n, 1)
        tabela[str(nome)] = {
            "casos": n,
            "essencial_pct": pct(lambda f: f["plano"] == "ESSENCIAL"),
            "pratico_pct": pct(lambda f: f["plano"] == "PRATICO"),
            "total_pct": pct(lambda f: f["plano"] == "TOTAL"),
            "elegivel_pct": pct(lambda f: f["elegibilidade"] == "SIM"),
            "inquilino_pct": pct(lambda f: f["campos"]["vinculo"]["valor"] == "INQUILINO"),
            "bens_comprovados_mediana": int(statistics.median(f["campos"]["bens"]["min"] for f in fs)),
        }
    eleg = [v["elegivel_pct"] for v in tabela.values()]
    return {"quintos": tabela,
            "razao_elegibilidade_menor_maior": round(min(eleg) / max(eleg), 2) if max(eleg) else 1.0}


def casos_contrastantes(fichas):
    """Casos para a demo e o vídeo. Os três primeiros são os perfis do slide 14
    (apartamento urbano, casa familiar, casa de lazer); depois, casos de canal e elegibilidade."""
    def primeiro(*conds):
        ordem = sorted(fichas, key=lambda f: f["imovel_id"])
        return next((f["imovel_id"] for cond in conds for f in ordem if cond(f)), None)
    tipo = lambda f: f["campos"]["tipo"]["valor"]
    uso = lambda f: f["campos"]["uso"]["valor"]
    motivo = lambda f, cod: any(m["codigo"] == cod for m in f["motivos"])
    eleg = lambda f: f["elegibilidade"] == "SIM"
    return {
        "perfil_A_apto_urbano": primeiro(
            lambda f: eleg(f) and tipo(f) == "APARTAMENTO" and uso(f) == "RESIDENCIAL_HABITUAL" and f["plano"] == "PRATICO"
            and (motivo(f, "ELETRONICOS") or motivo(f, "VIDROS")),
            lambda f: eleg(f) and tipo(f) == "APARTAMENTO" and f["plano"] == "PRATICO"),
        "perfil_B_casa_familiar": primeiro(
            # casa com família: RC familiar como adicional (condomínio) ou oferecida na pergunta (casa)
            lambda f: eleg(f) and tipo(f).startswith("CASA") and uso(f) == "RESIDENCIAL_HABITUAL"
            and any(a["cobertura"] == "RESPONSABILIDADE_CIVIL_FAMILIAR" for a in f.get("adicionais", [])),
            lambda f: eleg(f) and tipo(f).startswith("CASA") and uso(f) == "RESIDENCIAL_HABITUAL"
            and any(p["codigo"] == "RC_FAMILIA" for p in f["perguntas"]),
            lambda f: eleg(f) and tipo(f).startswith("CASA") and f["plano"] == "TOTAL"),
        "perfil_C_casa_lazer": primeiro(
            lambda f: eleg(f) and uso(f) == "LAZER_VERANEIO" and f["plano"] == "ESSENCIAL",
            lambda f: eleg(f) and uso(f) == "LAZER_VERANEIO",
            lambda f: eleg(f) and uso(f) == "RESIDENCIAL_LOCADO_A_TERCEIROS"),
        # chave mantida para o protótipo ("Já segurado"): agora é o provável seguro BB a confirmar no app (RN-19)
        "nao_elegivel_seguro_existente": primeiro(lambda f: any(p.get("provavel_bb") for p in f["pendencias"]),
                                                  lambda f: not eleg(f)),
        "one_click_limpo": primeiro(lambda f: f["canal"] == "ONE_CLICK" and f["confianca"] == "ALTA" and not f["pendencias"]),
        "inquilino_total": primeiro(lambda f: f["campos"]["vinculo"]["valor"] == "INQUILINO" and f["plano"] == "TOTAL"),
        "elegibilidade_a_confirmar": primeiro(lambda f: any(p["codigo"] == "POSSIVEL_REFORMA" for p in f["pendencias"]))
                                     or primeiro(lambda f: bool(f["pendencias"])),
    }
