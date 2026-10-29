"""Assertividade: quanto acerta cada cálculo que completa um dado faltante.

Como medimos (a "prova com gabarito escondido"): na base de desenvolvimento, pegamos os imóveis
que TÊM o dado (ex.: área cadastrada), escondemos o dado, deixamos o motor estimar e comparamos
com a verdade. Em 5 rodadas (validação cruzada em 5 dobras): em cada uma o motor aprende com 4/5
dos imóveis e é testado no 1/5 que não viu. Todo cálculo é comparado com o "chute" (dar a todo
mundo o valor do meio da base): um cálculo bom erra muito menos que o chute.

Onde não existe gabarito (bens, uso, vínculo, tipo), o boletim diz isso (`tem_gabarito: False`)
e mede a concordância entre fontes independentes, sem fingir acurácia (RN-47).
Este módulo só mede: não muda plano, faixa nem texto. Quem lê os números é calibrar() e o motivo.
"""
import math

import numpy as np

import motor as M
import parametros as P

DOBRAS = 5
SEMENTE = 0
METODO_CV = "validação cruzada em 5 dobras na base de desenvolvimento (aprende em 4/5, mede no 1/5 que não viu)"
METODO_CONCORDANCIA = "sem gabarito: concordância entre fontes independentes da base de desenvolvimento"
ORIGEM_CALIBRADA = "faixa calibrada de área × padrão"


def _pct(x):
    return round(100 * float(x), 1)


def dobras(n):
    """Número da dobra (0 a 4) de cada linha, sorteado com semente fixa: o resultado se repete."""
    return np.random.default_rng(SEMENTE).permutation(n) % DOBRAS


def boletim(o_que_estima, como, tem_gabarito, metodo, veredito, erro_mediano_pct=None, ate_20pct_pct=None,
            na_faixa_pct=None, chute_erro_mediano_pct=None, **extra):
    """O mesmo formato para todo cálculo, para a tabela do README e o texto do motivo."""
    return {"o_que_estima": o_que_estima, "como": como, "tem_gabarito": tem_gabarito, "metodo": metodo,
            "erro_mediano_pct": erro_mediano_pct, "ate_20pct_pct": ate_20pct_pct, "na_faixa_pct": na_faixa_pct,
            "chute_erro_mediano_pct": chute_erro_mediano_pct, "veredito": veredito, **extra}


# --- Área, padrão e área × padrão (com gabarito) ---------------------------------
def backtest(a):
    """Fora da amostra, em 5 dobras, nos imóveis de área cadastrada `a`:
    área (sinais, região e chute), padrão pelo IPTU/m² e a faixa de área × padrão.
    Devolve o dicionário de calibracao['backtest'] (as chaves antigas continuam)."""
    a = a.reset_index(drop=True)
    d = dobras(len(a))
    real = a.area_cadastrada_m2.to_numpy(dtype=float)
    est, lo, hi, chute, regiao = (np.full(len(a), np.nan) for _ in range(5))
    q_area = {}
    padrao = []   # (padrão real, IPTU relativo)
    for k in range(DOBRAS):
        treino, prova = a[d != k], a[d == k]
        c = M._calibrar_area(treino)
        q_area[k] = (c["razao_q10"], c["razao_q90"])
        mini = {"regional": {"area": M._degraus(treino, "area_cadastrada_m2")}}
        idx = np.where(d == k)[0]
        for i, r in zip(idx, prova.itertuples(index=False)):
            est[i] = M._area_estimada(r, c)
            regiao[i] = M.regional(mini, "area", r)[0]
            if str(r.padrao_construtivo_cadastrado).upper() in P.FATOR_PADRAO:
                padrao.append((i, str(r.padrao_construtivo_cadastrado).upper(), M.iptu_relativo(r, c)))
        lo[idx], hi[idx] = est[idx] * c["razao_q10"], est[idx] * c["razao_q90"]
        chute[idx] = float(treino.area_cadastrada_m2.median())
    ok = np.isfinite(est) & (est > 0)
    erro = np.abs(est[ok] - real[ok]) / real[ok]
    erro_chute = np.abs(chute - real) / real
    erro_regiao = np.abs(regiao - real) / real

    # Padrão pelo IPTU/m²: classe exata (cortes 0,90 e 1,15) e o intervalo de 2 classes que o motor usa
    classe = lambda rel: ("ECONOMICO" if rel < P.IPTU_REL_SEM_SUPERIOR else
                          "SUPERIOR" if rel > P.IPTU_REL_SEM_ECONOMICO else "NORMAL")
    com_rel = [(i, p, rel) for i, p, rel in padrao if rel is not None]
    intervalos = [(p, P.fator_padrao_pelo_iptu(rel)) for _, p, rel in com_rel]
    estreitados = [(p, iv) for p, iv in intervalos if iv]
    acertos = sum(iv[0] <= P.FATOR_PADRAO[p] <= iv[1] for p, iv in estreitados)

    # Área × padrão (o que multiplica o custo do m²) nos imóveis sem padrão e sem área do teste:
    # pior caso (área q10–q90 × padrão 0,85–1,30) contra a faixa calibrada pelos erros fora da amostra
    ip = np.array([i for i, _, _ in padrao], dtype=int)
    fator = np.array([P.FATOR_PADRAO[p] for _, p, _ in padrao])
    boa = np.isfinite(est[ip]) & (est[ip] > 0)   # sem IPTU nem luz não há estimativa para medir
    ip, fator = ip[boa], fator[boa]
    alvo, centro = real[ip] * fator, est[ip] * P.FATOR_PADRAO_MEIO
    razao = alvo / centro
    f_lo, f_hi = P.FATOR_PADRAO_DESCONHECIDO
    dentro_pior, larg_pior, dentro_cal, larg_cal = [], [], [], []
    for k in range(DOBRAS):
        nesta = d[ip] == k
        q1, q9 = np.quantile(razao[~nesta], P.AREA_QUANTIS)
        ql, qh = q_area[k]
        e = est[ip][nesta]
        pl, ph = e * ql * f_lo, e * qh * f_hi
        dentro_pior += list((alvo[nesta] >= pl) & (alvo[nesta] <= ph))
        larg_pior += list(ph / pl)
        cl, ch = faixa_area_x_padrao(e, e * ql, e * qh, (q1, q9))
        dentro_cal += list((alvo[nesta] >= cl) & (alvo[nesta] <= ch))
        larg_cal += list(ch / cl)
    quantis = tuple(round(float(q), 4) for q in np.quantile(razao, P.AREA_QUANTIS))

    return {
        "metodo": METODO_CV,
        "area_casos": int(ok.sum()),
        "area_mape_pct": _pct(np.mean(erro)),
        "area_erro_mediano_pct": _pct(np.median(erro)),
        "area_ate_20pct_pct": _pct(np.mean(erro <= 0.2)),
        "area_dentro_da_faixa_pct": _pct(np.mean((real[ok] >= lo[ok]) & (real[ok] <= hi[ok]))),
        "area_chute_erro_mediano_pct": _pct(np.median(erro_chute)),
        "area_chute_ate_20pct_pct": _pct(np.mean(erro_chute <= 0.2)),
        "area_regiao_erro_mediano_pct": _pct(np.median(erro_regiao)),
        "area_regiao_ate_20pct_pct": _pct(np.mean(erro_regiao <= 0.2)),
        "padrao_casos": len(padrao),
        "padrao_estreitados": len(estreitados),
        "padrao_intervalo_correto_pct": _pct(acertos / len(estreitados)) if estreitados else None,
        "padrao_classe_exata_pct": _pct(np.mean([classe(rel) == p for _, p, rel in com_rel])) if com_rel else None,
        "padrao_chute_normal_pct": _pct(np.mean([p == "NORMAL" for _, p, _ in com_rel])) if com_rel else None,
        "area_padrao_casos": len(padrao),
        "area_padrao_erro_mediano_pct": _pct(np.median(np.abs(razao - 1))),
        "area_padrao_dentro_pior_caso_pct": _pct(np.mean(dentro_pior)),
        "area_padrao_largura_pior_caso": round(float(np.median(larg_pior)), 2),
        "area_padrao_dentro_calibrada_pct": _pct(np.mean(dentro_cal)),
        "area_padrao_largura_calibrada": round(float(np.median(larg_cal)), 2),
        "area_padrao_quantis": quantis,
    }


def faixa_area_x_padrao(area, area_min, area_max, quantis):
    """(mín, máx) de área × padrão quando os dois faltam: o centro (área × 1,05, o padrão do meio)
    vezes os percentis 9% e 91% do erro real, nunca mais estreita que a faixa da área com padrão
    normal (quem sabe menos não pode ter um teto menor que quem sabe que o padrão é normal)."""
    q_lo, q_hi = quantis
    centro = area * P.FATOR_PADRAO_MEIO
    return np.minimum(centro * q_lo, area_min), np.maximum(centro * q_hi, area_max)


# --- Bens sem compras e CEP (movidos de motor.py) --------------------------------
def backtest_bens_sem_compras(com_compras):
    """Fora da amostra, em 5 dobras: finge que quem tem compras não tem e estima as compras.
    Compara só a média da região com a região combinada com a renda."""
    c = com_compras.reset_index(drop=True)
    d = dobras(len(c))
    erros = {"regiao": [], "regiao_e_renda": []}
    for k in range(DOBRAS):
        treino, prova = c[d != k], c[d == k]
        mini = {"regional": {"compras": M._degraus(treino, "compras")}, "compras_por_renda": M._compras_por_renda(treino)}
        for r in prova.itertuples(index=False):
            med = M.regional(mini, "compras", r)[0]
            pela_renda = M.compras_pela_renda(r, mini)
            erros["regiao"].append(abs(med - r.compras) / r.compras)
            erros["regiao_e_renda"].append(abs(M._regiao_e_renda(med, pela_renda) - r.compras) / r.compras
                                           if pela_renda else erros["regiao"][-1])
    return {"metodo": METODO_CV + "; imóveis com compras tratados como se não tivessem",
            "casos": len(erros["regiao"]),
            "erro_mediano_so_regiao_pct": _pct(np.median(erros["regiao"])),
            "erro_mediano_regiao_e_renda_pct": _pct(np.median(erros["regiao_e_renda"])),
            "ate_20pct_regiao_e_renda_pct": _pct(np.mean(np.array(erros["regiao_e_renda"]) <= 0.2))}


def teste_cep(a):
    """O CEP agregado explica a variação do IPTU/m² melhor que um CEP sorteado? (R² entre grupos
    com 3+ imóveis.) Se não, ele é ruído e não entra como degrau regional (RN-10)."""
    a = a.assign(rel=(a.pagamento_iptu_anual / a.area_cadastrada_m2))
    a = a.assign(rel=a.rel / a.groupby("codigo_ibge_municipio").rel.transform("median"))

    def r2(col):
        x = a[a[col].map(a[col].value_counts()) >= 3]
        media = x.groupby(col).rel.transform("mean")
        return float(1 - ((x.rel - media) ** 2).sum() / ((x.rel - x.rel.mean()) ** 2).sum())
    embaralhado = a.cep_agregado.sample(frac=1, random_state=SEMENTE).to_numpy()
    a = a.assign(cep_embaralhado=embaralhado)
    return {"r2_cep": round(r2("cep_agregado"), 3), "r2_cep_embaralhado": round(r2("cep_embaralhado"), 3)}


# --- Sem gabarito: concordância entre fontes -------------------------------------
def concordancias(m, bens):
    """Tipo, vínculo, uso e bens não têm valor real para comparar. Medimos se fontes
    independentes concordam (e dizemos que é isso, não acurácia)."""
    termo = np.where(m.possui_termo_apartamento == "SIM", "APARTAMENTO", "CASA")
    compl = m.complemento.map(M.tipo_pelo_complemento)
    tem = compl.notna().to_numpy()
    alug = (m.pagamento_aluguel_recorrente == "SIM").to_numpy()
    fin = (m.parcela_financiamento_imobiliario > 0).to_numpy()
    cred = (m.credito_recorrente_compativel_aluguel == "SIM").to_numpy()
    princ = (m.endereco_principal_compativel == "SIM").to_numpy()
    luz = (m.energia_media_mensal_6m / m.groupby("codigo_ibge_municipio").energia_media_mensal_6m.transform("median")).to_numpy()
    compras = (m.compras_moveis_36m + m.compras_eletrodomesticos_36m + m.compras_eletronicos_36m)
    pond = m.imovel_id.map(bens.groupby("imovel_id_referencia").valor_bem_ponderado_referencia.sum()).fillna(0)
    com = (pond > 0).to_numpy()
    return {
        "tipo_com_complemento": int(tem.sum()), "imoveis": len(m),
        "tipo_concordancia_pct": _pct(np.mean(compl[tem].to_numpy() == termo[tem])) if tem.any() else None,
        "vinculo_observado_pct": _pct(np.mean(alug | fin)),
        "vinculo_aluguel_e_financiamento": int((alug & fin).sum()),
        "vinculo_sem_sinal_pct": _pct(np.mean(~alug & ~fin & ~cred)),
        "uso_nao_principal": int((~princ).sum()),
        "uso_luz_principal": round(float(np.median(luz[princ])), 2),
        "uso_luz_nao_principal": round(float(np.median(luz[~princ])), 2),
        "bens_correlacao_compras_bens": round(float(compras[com].rank().corr(pond[com].rank())), 2),
    }


# --- Os boletins -----------------------------------------------------------------
def boletins(cal):
    """Um boletim por cálculo, a partir do que calibrar() mediu. Sem `casos_no_teste`:
    esse número depende da base processada (ver com_casos_no_teste)."""
    b, bs, cep, c = cal["backtest"], cal["backtest_bens_sem_compras"], cal["teste_cep"], cal["concordancias"]
    return {
        "area": boletim(
            "área do imóvel (m²)", "IPTU (peso 0,6) e conta de luz (0,4) divididos pelo R$/m² da cidade, em média geométrica",
            True, METODO_CV, "3 vezes melhor que o chute; usado quando não há área cadastrada",
            b["area_erro_mediano_pct"], b["area_ate_20pct_pct"], b["area_dentro_da_faixa_pct"],
            b["area_chute_erro_mediano_pct"], casos_medidos=b["area_casos"], chute_ate_20pct_pct=b["area_chute_ate_20pct_pct"]),
        "area_regional": boletim(
            "área do imóvel sem IPTU nem luz", "mediana da região: cidade + tipo → cidade → estado → geral (mínimo de 20 imóveis)",
            True, METODO_CV, "reserva: melhor que o chute, pior que os sinais",
            b["area_regiao_erro_mediano_pct"], b["area_regiao_ate_20pct_pct"], None, b["area_chute_erro_mediano_pct"],
            casos_medidos=b["area_casos"]),
        "padrao_iptu": boletim(
            "padrão construtivo (econômico, normal, superior)", "IPTU por m² ÷ mediana da cidade: abaixo de 0,90 tira o superior; "
            "acima de 1,15 tira o econômico", True, METODO_CV,
            "o IPTU não diz o padrão exato (perde do chute), mas descarta um extremo com segurança: por isso o motor usa intervalo",
            na_faixa_pct=b["padrao_intervalo_correto_pct"], casos_medidos=b["padrao_casos"],
            casos_estreitados=b["padrao_estreitados"], classe_exata_pct=b["padrao_classe_exata_pct"],
            chute_classe_exata_pct=b["padrao_chute_normal_pct"]),
        "area_x_padrao": boletim(
            "área × padrão (o que multiplica o custo do m² na reconstrução)",
            f"área estimada × {P.FATOR_PADRAO_MEIO:.2f} (padrão do meio) × percentis 9% e 91% do erro real, "
            "nunca mais estreita que a faixa da área com padrão normal".replace(".", ","),
            True, METODO_CV, "faixa bem mais estreita que o pior caso e ainda contendo o valor real em quase 9 de cada 10 casos",
            b["area_padrao_erro_mediano_pct"], None, b["area_padrao_dentro_calibrada_pct"], None,
            casos_medidos=b["area_padrao_casos"], largura_calibrada=b["area_padrao_largura_calibrada"],
            largura_pior_caso=b["area_padrao_largura_pior_caso"], na_faixa_pior_caso_pct=b["area_padrao_dentro_pior_caso_pct"],
            quantis=list(b["area_padrao_quantis"])),
        "tipo": boletim(
            "tipo do imóvel (casa, casa em condomínio, apartamento)", "termo do endereço conferido com o complemento (AP, BLOCO × CASA, LOTE)",
            False, METODO_CONCORDANCIA, "duas fontes independentes concordam",
            concordancia_pct=c["tipo_concordancia_pct"], casos_medidos=c["tipo_com_complemento"]),
        "vinculo": boletim(
            "vínculo (inquilino, financiado, dono, dono que aluga)", "aluguel pago, parcela de financiamento e crédito de aluguel nas contas",
            False, METODO_CONCORDANCIA, "observado nas transações quando há aluguel ou financiamento; 'provável quitado' é só ausência de sinal",
            observado_pct=c["vinculo_observado_pct"], conflitos=c["vinculo_aluguel_e_financiamento"],
            sem_sinal_pct=c["vinculo_sem_sinal_pct"], casos_medidos=c["imoveis"]),
        "uso": boletim(
            "uso (mora, veraneio, alugado a terceiros)", "endereço principal; crédito de aluguel; outro imóvel principal; senão, pergunta",
            False, METODO_CONCORDANCIA, "sem como medir: a conta de luz não separa casa habitada de casa vazia; vira pergunta (RN-19)",
            luz_principal=c["uso_luz_principal"], luz_nao_principal=c["uso_luz_nao_principal"], casos_medidos=c["uso_nao_principal"]),
        "bens": boletim(
            "valor dos bens (móveis, eletrodomésticos, eletrônicos)", "compras de 36 meses corrigidas pelo IPCA (mínimo) até "
            f"{P.FATOR_ESTOQUE:.1f} × compras (máximo, premissa de vida útil)".replace(".", ","),
            False, METODO_CONCORDANCIA, "o mínimo é comprovado pelas compras; o máximo é premissa; compras e bens cadastrados concordam",
            correlacao_compras_bens=c["bens_correlacao_compras_bens"], casos_medidos=c["imoveis"]),
        "bens_sem_compras": boletim(
            "compras de quem não tem compras nem bens", "mediana da região combinada com a renda (média geométrica, presa entre 0,5× e 2× a região)",
            True, bs["metodo"], "reserva: a renda corta o erro quase pela metade",
            bs["erro_mediano_regiao_e_renda_pct"], bs["ate_20pct_regiao_e_renda_pct"], None, bs["erro_mediano_so_regiao_pct"],
            casos_medidos=bs["casos"]),
        "cep": boletim(
            "degrau regional por CEP agregado", "R² do IPTU/m² por CEP contra um CEP sorteado", True,
            "comparação com um CEP sorteado (semente fixa)", "descartado: explica tanto quanto um CEP sorteado (ruído, RN-10)",
            r2_cep=cep["r2_cep"], r2_cep_embaralhado=cep["r2_cep_embaralhado"]),
    }


def com_casos_no_teste(bols, fichas):
    """Os boletins com quantos casos da base processada usam cada cálculo."""
    area = [f["campos"]["area"] for f in fichas]
    bens = [f["campos"]["bens"] for f in fichas]
    origem = [f["valor_imovel"]["origem_padrao"] for f in fichas]
    n = {
        "area": sum(a["natureza"] == "ESTIMADO" and not a.get("regional") for a in area),
        "area_regional": sum(bool(a.get("regional")) for a in area),
        "padrao_iptu": origem.count("estimado pelo IPTU/m²"),
        "area_x_padrao": origem.count(ORIGEM_CALIBRADA),
        "tipo": len(fichas),
        "vinculo": len(fichas),
        "uso": sum(f["campos"]["uso"]["natureza"] != "OBSERVADO" for f in fichas),
        "bens": len(fichas),
        "bens_sem_compras": sum(bool(b.get("regional")) for b in bens),
        "cep": 0,
    }
    return {k: {**v, "casos_no_teste": n[k]} for k, v in bols.items()}


def frase_de_acerto(campo, cal):
    """A confiança em números, em português simples, ou '' sem a medição (RN-12).
    Ex.: 'erro abaixo de 20% em 2 de cada 3 testes' (nos imóveis de área conhecida da base de desenvolvimento)."""
    b = (cal or {}).get("assertividade", {}).get(campo)
    if campo != "area" or not b or b.get("ate_20pct_pct") is None:
        return ""
    pct = b["ate_20pct_pct"]
    fracao = next((f for limite, f in ((75, "3 de cada 4"), (65, "2 de cada 3"), (58, "6 de cada 10"),
                                        (48, "metade dos")) if pct >= limite), None)
    return f"erro abaixo de 20% em {fracao} testes" if fracao else ""
