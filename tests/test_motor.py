"""Testes do motor. Cada bloco corresponde a uma tarefa do PLANO_UNIFICADO.md."""
import parametros as P


# --- T1: parâmetros e fontes ----------------------------------------------------
def test_custo_m2_rj_sem_cub_oficial_usa_razao():
    # CUB-RJ veio de agregador: o máximo é SINAPI-RJ × mediana CUB/SINAPI das UFs com CUB oficial
    sinapi = P._tabela_custo()[0]["RJ"]
    lo, hi = P.custo_m2("RJ")
    assert lo == sinapi and hi == round(sinapi * P._tabela_custo()[2], 2)
    assert 1.0 < P._tabela_custo()[2] < 1.3 and "razão" in P.fonte_custo("RJ")


def test_cub_oficial_de_sete_ufs():
    oficiais = P._tabela_custo()[1]
    assert set(oficiais) == {"SP", "DF", "GO", "BA", "MG", "RS", "PR"}
    assert P.custo_m2("PR")[1] == 2738.93 and "oficial" in P.fonte_custo("PR")


def test_custo_m2_sp_usa_cub_oficial():
    assert P.custo_m2("SP") == (P._tabela_custo()[0]["SP"], 2238.58) and P.fonte_custo("SP") == "CUB SP oficial"


def test_custo_m2_uf_desconhecida_usa_neutro():
    assert P.custo_m2("XX") == P.CUSTO_M2_NEUTRO


def test_fator_ipca():
    assert 1.06 < P.FATOR_IPCA < 1.08


def test_aluguel_m2_curitiba():
    assert P.aluguel_m2("PR") == 49.44


def test_renda_so_tem_um_parametro():
    # Mentoria BB 28/10: renda não é dado sensível. Entra num único ponto (bens sem compras),
    # ligado por um parâmetro; nenhum outro parâmetro de decisão usa renda.
    assert [n for n in dir(P) if "RENDA" in n.upper()] == ["RENDA_NOS_BENS_SEM_COMPRAS"]


# --- T2: tipo, área e bens -------------------------------------------------------
import json  # noqa: E402
from types import SimpleNamespace  # noqa: E402

import pandas as pd  # noqa: E402

import motor  # noqa: E402


def test_bens_caso_00005(caso):
    r, b = caso("IMO_CASO_00005_01")
    est = motor.estimar_bens(r, b)
    assert round(est["min"]) == round(20750 * P.FATOR_IPCA)
    assert round(est["max"]) == round(2.7 * 20750 * P.FATOR_IPCA)


def test_bens_sem_compras_nem_bens_usa_piso(linha, vazio):
    r = linha(compras_moveis_36m=0, compras_eletrodomesticos_36m=0, compras_eletronicos_36m=0)
    est = motor.estimar_bens(r, vazio)
    assert est["min"] == P.BENS_PISO and est["confianca"] == "BAIXA"


def test_bens_com_compras_ignoram_renda_e_idade(linha, vazio, cal):
    # Quem tem compras tem prova: a renda não substitui nem mexe na evidência
    a = motor.estimar_bens(linha(renda_mensal=1800, idade=20, quantidade_dependentes=0), vazio, cal)
    b = motor.estimar_bens(linha(renda_mensal=34000, idade=80, quantidade_dependentes=3), vazio, cal)
    assert a == b


SEM_COMPRAS = dict(compras_moveis_36m=0, compras_eletrodomesticos_36m=0, compras_eletronicos_36m=0)


def test_bens_sem_compras_combinam_regiao_e_renda(linha, vazio, cal):
    baixa = motor.estimar_bens(linha(renda_mensal=2000, **SEM_COMPRAS), vazio, cal)
    alta = motor.estimar_bens(linha(renda_mensal=30000, **SEM_COMPRAS), vazio, cal)
    assert alta["min"] > baixa["min"] and alta["max"] > baixa["max"]
    assert "renda" in alta["fonte"] and alta["usou_renda"] and alta["confianca"] == "BAIXA"


def test_bens_sem_compras_nem_renda_ficam_na_regiao(linha, vazio, cal, monkeypatch):
    sem_renda = motor.estimar_bens(linha(renda_mensal=0, **SEM_COMPRAS), vazio, cal)
    monkeypatch.setattr(P, "RENDA_NOS_BENS_SEM_COMPRAS", False)
    desligada = motor.estimar_bens(linha(renda_mensal=30000, **SEM_COMPRAS), vazio, cal)
    assert sem_renda == desligada and not sem_renda["usou_renda"] and "renda" not in sem_renda["fonte"]


def test_renda_com_idade_nao_mexe_nos_bens(linha, vazio, cal):
    a = motor.estimar_bens(linha(renda_mensal=9000, idade=19, **SEM_COMPRAS), vazio, cal)
    b = motor.estimar_bens(linha(renda_mensal=9000, idade=85, **SEM_COMPRAS), vazio, cal)
    assert a == b


def test_motivo_avisa_quando_usou_a_renda(teste, cal, caso, vazio):
    # Transparência (LGPD art. 20): se a renda entrou na estimativa, o cliente lê isso
    catalogo = teste["catalogo"].groupby("plano").cobertura_fixa.apply(list).to_dict()
    r, _ = caso("IMO_CASO_00005_01")
    r = SimpleNamespace(**{**vars(r), **SEM_COMPRAS})
    f = motor.processar_caso(r, vazio, cal, catalogo)
    assert f["campos"]["bens"]["usou_renda"] and "sua renda" in motor.justificativa(f)


def test_sem_compras_renda_nao_muda_plano_nem_jornada(teste, cal, caso, vazio):
    # Revisão: a renda chegava ao plano pelos limiares de bens. Bens presumidos não somam pontos.
    catalogo = teste["catalogo"].groupby("plano").cobertura_fixa.apply(list).to_dict()
    for imovel_id in ("IMO_CASO_00001_01", "IMO_CASO_00005_01", "IMO_CASO_00031_01"):
        r, _ = caso(imovel_id)
        fs = [motor.processar_caso(SimpleNamespace(**{**vars(r), **SEM_COMPRAS, "renda_mensal": renda}), vazio, cal, catalogo)
              for renda in (0, 1500, 8000, 40000, 150000)]
        for k in ("plano", "elegibilidade", "jornada", "confianca", "adicionais"):
            assert len({json.dumps(f[k], sort_keys=True) for f in fs}) == 1, (imovel_id, k)
        for f in fs:   # sem compras, o texto não pode dizer que ele comprou nem dar a estimativa como fato
            textos = [motor.justificativa(f)] + [c["justificativa"] for c in f["coberturas"]]
            assert not any("suas compras" in t or "você comprou" in t for t in textos), imovel_id
            assert "média de casas parecidas na sua região" in motor.justificativa(f), imovel_id


def test_renda_em_texto_ou_invalida_nao_quebra(linha, vazio, cal):
    texto = motor.estimar_bens(linha(renda_mensal="5000", **SEM_COMPRAS), vazio, cal)
    ruim = motor.estimar_bens(linha(renda_mensal="abc", **SEM_COMPRAS), vazio, cal)
    assert texto["usou_renda"] and not ruim["usou_renda"]


def test_renda_nao_passa_de_2x_a_regiao(linha, vazio, cal, monkeypatch):
    rica = motor.estimar_bens(linha(renda_mensal=500000, **SEM_COMPRAS), vazio, cal)
    monkeypatch.setattr(P, "RENDA_NOS_BENS_SEM_COMPRAS", False)
    so_regiao = motor.estimar_bens(linha(renda_mensal=500000, **SEM_COMPRAS), vazio, cal)
    assert rica["max"] <= 2 * so_regiao["max"] + 1


def test_razao_compras_renda_exige_amostra_minima():
    df = pd.DataFrame({"codigo_ibge_municipio": [1] * 3 + [2] * P.REGIONAL_MIN_IMOVEIS,
                       "compras": [100.0] * (3 + P.REGIONAL_MIN_IMOVEIS),
                       "renda_mensal": [10.0] * (3 + P.REGIONAL_MIN_IMOVEIS)})
    t = motor._compras_por_renda(df)
    assert "1" not in t["municipio"] and "2" in t["municipio"]


def test_backtest_regiao_com_renda_erra_menos(cal):
    bt = cal["backtest_bens_sem_compras"]
    assert bt["erro_mediano_regiao_e_renda_pct"] < bt["erro_mediano_so_regiao_pct"]


def test_area_sem_iptu_nem_energia(linha, cal):
    d = motor.inferir_area(linha(area_cadastrada_m2=0, pagamento_iptu_anual=0, energia_media_mensal_6m=0), cal)
    assert 30 <= d["valor"] <= 400 and d["confianca"] == "BAIXA"


def test_tipo_complemento_diverge(linha):
    d = motor.inferir_tipo(linha(possui_termo_apartamento="SIM", complemento="CASA FUNDOS"))
    assert d["valor"] == "APARTAMENTO" and d["confianca"] == "MEDIA" and d["diverge"]


def test_tipo_complemento_confirma(linha):
    d = motor.inferir_tipo(linha(possui_termo_apartamento="SIM", complemento="BLOCO B APTO 305"))
    assert d["confianca"] == "ALTA" and not d["diverge"]


# --- T3: elegibilidade, plano e coberturas ---------------------------------------
APTO_CURITIBA = "IMO_CASO_00005_01"   # apartamento financiado, 110 m², Curitiba


def _cob(f, nome):
    return next(c for c in f["coberturas"] if c["cobertura"] == nome)


def test_obra_vira_sim_com_pergunta(ficha):
    f = ficha(APTO_CURITIBA, gastos_material_construcao_24m=40000)
    assert f["elegibilidade"] == "SIM"
    assert f["perguntas"][0]["prioridade"] == 100 and "reforma" in f["perguntas"][0]["texto"]
    assert f["canal"] == "GERENTE"


def test_situacao_irregular_vira_nao(ficha):
    f = ficha(APTO_CURITIBA, situacao_imovel_cadastral="TOMBADO")
    assert f["elegibilidade"] == "NAO"


def test_incendio_apto_financiado_segundo_risco(ficha):
    inc = _cob(ficha(APTO_CURITIBA, padrao_construtivo_cadastrado="NORMAL"), "INCENDIO_RAIO_EXPLOSAO_FUMACA")
    assert 100000 <= inc["min"] and inc["max"] <= 200000
    assert "15.2" in inc["observacao"]


def test_casa_quitada_soma_reconstrucao(ficha):
    f = ficha(APTO_CURITIBA, possui_termo_apartamento="NAO", possui_termo_casa="SIM", possui_termo_condominio="NAO",
              complemento="CASA", parcela_financiamento_imobiliario=0, padrao_construtivo_cadastrado="NORMAL")
    inc = _cob(f, "INCENDIO_RAIO_EXPLOSAO_FUMACA")
    assert inc["min"] >= 110 * 2287.42 and "5.5" in inc["observacao"]


def test_plano_e_coberturas_ignoram_renda_e_idade(ficha):
    a = ficha(APTO_CURITIBA, renda_mensal=1800, idade=19)
    b = ficha(APTO_CURITIBA, renda_mensal=34000, idade=85)
    assert a["plano"] == b["plano"]
    assert [(c["min"], c["max"]) for c in a["coberturas"]] == [(c["min"], c["max"]) for c in b["coberturas"]]


def test_criancas_e_pet_pesam_so_no_plano(ficha):
    sem = ficha(APTO_CURITIBA, quantidade_dependentes=0, possui_pet_informado="NAO")
    com = ficha(APTO_CURITIBA, quantidade_dependentes=2, possui_pet_informado="SIM")
    assert any(m["codigo"] == "FAMILIA_DECLARADA" for m in com["motivos"])
    assert not any(m["codigo"] == "FAMILIA_DECLARADA" for m in sem["motivos"])
    assert com["pontos"]["total"] == sem["pontos"]["total"] + 1
    faixa = lambda f: {c["cobertura"]: (c["min"], c["max"]) for c in f["coberturas"]}
    fs, fc = faixa(sem), faixa(com)
    assert all(fs[k] == fc[k] for k in fs.keys() & fc.keys())
    for k in ("elegibilidade", "confianca", "confianca_score", "canal", "campos"):
        assert sem[k] == com[k]


def test_crianca_em_apartamento_ganha_rc_adicional(ficha):
    f = ficha(APTO_CURITIBA, quantidade_dependentes=1, possui_pet_informado="NAO", gastos_vidracaria_24m=0,
              compras_eletronicos_36m=0)
    assert not any(m["codigo"] == "FAMILIA_DECLARADA" for m in f["motivos"])
    assert f["plano"] != "TOTAL"
    rc = [c for c in f["coberturas"] if c["cobertura"] == "RESPONSABILIDADE_CIVIL_FAMILIAR"]
    assert len(rc) == 1 and rc[0]["tipo"] == "ADICIONAL" and "adicional" in rc[0]["observacao"].lower()


def test_casa_com_pet_recebe_pergunta_e_nao_adicional(ficha):
    f = ficha(APTO_CURITIBA, possui_termo_apartamento="NAO", possui_termo_condominio="NAO", complemento="CASA",
              quantidade_dependentes=0, possui_pet_informado="SIM", pagamento_aluguel_recorrente="NAO")
    if f["plano"] != "TOTAL":
        assert not f["adicionais"] and f["perguntas_candidatas"] >= 1


def test_veraneio_nao_puxa_o_pratico(linha, cal, vazio):
    r = linha(possui_termo_apartamento="SIM", possui_termo_condominio="NAO", complemento="APTO 12",
              pagamento_aluguel_recorrente="NAO", parcela_financiamento_imobiliario=0, credito_recorrente_compativel_aluguel="NAO",
              endereco_principal_compativel="NAO", gastos_vidracaria_24m=0, compras_eletronicos_36m=0,
              compras_eletrodomesticos_36m=0, compras_moveis_36m=0, quantidade_dependentes=0, possui_pet_informado="NAO")
    uso = motor.inferir_uso(r, True)
    rec = motor.escolher_plano(r, motor.inferir_tipo(r), motor.inferir_vinculo(r), uso, motor.estimar_bens(r, vazio))
    assert uso["valor"] == "LAZER_VERANEIO" and rec["plano"] == "ESSENCIAL"
    assert "desocupada" in rec["motivos_plano"][0]["texto"]


def test_familia_nao_empurra_para_o_pratico(linha, cal, vazio):
    # casa sem sinais de roubo além de ser casa: a família pede RC (Total), não o Prático
    r = linha(possui_termo_apartamento="NAO", possui_termo_condominio="NAO", pagamento_aluguel_recorrente="NAO",
              parcela_financiamento_imobiliario=0, credito_recorrente_compativel_aluguel="NAO", gastos_vidracaria_24m=0,
              compras_eletronicos_36m=0, compras_eletrodomesticos_36m=0, compras_moveis_36m=0,
              quantidade_dependentes=2, possui_pet_informado="SIM", endereco_principal_compativel="SIM", complemento="CASA")
    tipo, vinc = motor.inferir_tipo(r), motor.inferir_vinculo(r)
    rec = motor.escolher_plano(r, tipo, vinc, motor.inferir_uso(r, False), motor.estimar_bens(r, vazio))
    assert rec["pontos"] == {"pratico": 1, "total": 1} and rec["plano"] == "ESSENCIAL"


def test_seguro_existente_um_imovel_nao_elegivel(caso, cal, teste):
    import motor
    r, b = caso(APTO_CURITIBA)
    r.possui_seguro_residencial, r.qtd_produtos_seguridade = "SIM", 1   # tem produto de seguridade BB
    catalogo = teste["catalogo"].groupby("plano").cobertura_fixa.apply(list).to_dict()
    f = motor.processar_caso(r, b, cal, catalogo, n_imoveis=1)
    assert f["elegibilidade"] == "NAO" and f["pendencias"][0]["codigo"] == "SEGURO_EXISTENTE"
    assert motor.justificativa(f).startswith("Não podemos fazer uma nova proposta")


def test_seguro_existente_sem_produto_bb_vira_pergunta(caso, cal, teste):
    # A vedação do guia é só para seguro BB; sem produto de seguridade BB, pode ser outra seguradora.
    import motor
    r, b = caso(APTO_CURITIBA)
    r.possui_seguro_residencial, r.qtd_produtos_seguridade = "SIM", 0
    catalogo = teste["catalogo"].groupby("plano").cobertura_fixa.apply(list).to_dict()
    f = motor.processar_caso(r, b, cal, catalogo, n_imoveis=1)
    assert f["elegibilidade"] == "SIM" and f["jornada"] == "APP_COM_PERGUNTAS"   # o app resolve; gerente é último recurso
    assert f["perguntas"][0]["prioridade"] == 100 and "BB Seguros" in f["perguntas"][0]["texto"]


def test_dado_observado_antigo_conta_como_estimado():
    # "Dados antigos valem menos": observado mais velho que a meia-vida do campo vira ESTIMADO.
    import motor
    recente = {"natureza": "OBSERVADO", "fonte_tipo": "TRANSACAO", "idade_meses": 3}
    antigo = {"natureza": "OBSERVADO", "fonte_tipo": "TRANSACAO", "idade_meses": 30}
    assert motor.classe_dado(recente, "vinculo") == "OBSERVADO"
    assert motor.classe_dado(antigo, "vinculo") == "ESTIMADO" and antigo["antigo"]


def test_seguro_existente_dois_imoveis_pergunta_qual(caso, cal, teste):
    import motor
    r, b = caso(APTO_CURITIBA)
    r.possui_seguro_residencial = "SIM"
    catalogo = teste["catalogo"].groupby("plano").cobertura_fixa.apply(list).to_dict()
    f = motor.processar_caso(r, b, cal, catalogo, n_imoveis=2)
    assert f["elegibilidade"] == "SIM" and f["confianca"] != "ALTA"
    assert any("Qual dos seus imóveis" in p["texto"] for p in f["perguntas"])


def test_padrao_desconhecido_abre_a_faixa(ficha):
    # sem área cadastrada, o IPTU não serve para o padrão (seria circular): a faixa abre inteira
    normal = ficha(APTO_CURITIBA, padrao_construtivo_cadastrado="NORMAL", area_cadastrada_m2=0)
    nao_sei = ficha(APTO_CURITIBA, padrao_construtivo_cadastrado="NAO_DISPONIVEL", area_cadastrada_m2=0)
    a, b = _cob(normal, "INCENDIO_RAIO_EXPLOSAO_FUMACA"), _cob(nao_sei, "INCENDIO_RAIO_EXPLOSAO_FUMACA")
    assert b["min"] <= a["min"] and b["max"] >= a["max"] and nao_sei["valor_imovel"]["fator_padrao"] == [0.85, 1.3]
    assert any(p["codigo"] == "PADRAO" for p in nao_sei["perguntas"]) or nao_sei["perguntas_candidatas"] > 3


def test_padrao_pelo_iptu_estreita_a_faixa(ficha, caso, cal):
    # área cadastrada + IPTU/m² acima de 1,15 × a mediana do município: descarta o econômico
    r, _ = caso(APTO_CURITIBA)
    rel = motor.iptu_relativo(r, cal)
    alto = ficha(APTO_CURITIBA, padrao_construtivo_cadastrado="NAO_DISPONIVEL",
                 pagamento_iptu_anual=r.pagamento_iptu_anual * 1.3 / rel)
    baixo = ficha(APTO_CURITIBA, padrao_construtivo_cadastrado="NAO_DISPONIVEL",
                  pagamento_iptu_anual=r.pagamento_iptu_anual * 0.7 / rel)
    assert alto["valor_imovel"]["fator_padrao"] == [1.0, 1.3] and alto["valor_imovel"]["origem_padrao"] == "estimado pelo IPTU/m²"
    assert baixo["valor_imovel"]["fator_padrao"] == [0.85, 1.0]
    assert "estimado pelo IPTU" in _cob(alto, "INCENDIO_RAIO_EXPLOSAO_FUMACA")["regra"]


def test_padrao_cadastrado_nao_e_trocado_pelo_iptu(ficha):
    f = ficha(APTO_CURITIBA, padrao_construtivo_cadastrado="ECONOMICO", pagamento_iptu_anual=999999)
    assert f["valor_imovel"]["fator_padrao"] == [0.85, 0.85]


def test_backtest_fora_da_amostra(cal):
    b = cal["backtest"]
    assert 70 <= b["area_dentro_da_faixa_pct"] <= 90          # faixa q10–q90 calibrada (~80%)
    assert b["padrao_intervalo_correto_pct"] >= 95 and b["padrao_estreitados"] > 100


def test_area_com_iptu_zerado_usa_so_a_energia(linha, cal):
    com = motor.inferir_area(linha(area_cadastrada_m2=0), cal)
    sem_iptu = motor.inferir_area(linha(area_cadastrada_m2=0, pagamento_iptu_anual=0), cal)
    # antes: 0,4 × área pela energia (encolhia 60%); agora a energia sozinha, com peso inteiro
    assert sem_iptu["valor"] > 0.6 * com["valor"] and "IPTU" not in sem_iptu["fonte"]


def test_estimativa_acima_do_limite_avisa_subseguro(ficha):
    f = ficha(APTO_CURITIBA, compras_eletronicos_36m=400000, compras_eletrodomesticos_36m=200000)
    c = _cob(f, "DANOS_ELETRICOS")
    assert c["max"] == 30000 and c["limitada_pelo_produto"] and "fica descoberto" in c["observacao"]


def test_despesas_emergenciais_sobre_a_faixa_de_incendio(ficha):
    f = ficha("IMO_CASO_00008_01")
    inc, desp = _cob(f, "INCENDIO_RAIO_EXPLOSAO_FUMACA"), _cob(f, "DESPESAS_EMERGENCIAIS")
    assert desp["max"] <= max(motor.arred(inc["max"] * 0.05), 2000)


def test_locador_avisa_que_conteudo_e_do_inquilino(ficha):
    f = ficha("IMO_CASO_00003_01")
    assert f["campos"]["vinculo"]["valor"] == "PROPRIETARIO_LOCADOR"
    assert "locatário" in _cob(f, "INCENDIO_RAIO_EXPLOSAO_FUMACA")["observacao"]


def test_motivo_cita_sinistros_reais_sem_mudar_valor(ficha, monkeypatch):
    com = ficha(APTO_CURITIBA)
    assert "53,3%" in _cob(com, "DANOS_ELETRICOS")["justificativa"]
    monkeypatch.setattr(motor.P, "sinistros_pct", lambda cob: None)   # sem o arquivo externo
    sem = ficha(APTO_CURITIBA)
    assert [(c["min"], c["max"]) for c in com["coberturas"]] == [(c["min"], c["max"]) for c in sem["coberturas"]]
    assert "acionamentos" not in _cob(sem, "DANOS_ELETRICOS")["justificativa"]


def test_territorio_entra_so_no_texto(ficha, monkeypatch):
    # Curitiba: registros da Defesa Civil (Atlas/S2iD) e ranking da ANEEL citados no motivo
    com = ficha(APTO_CURITIBA)
    assert "Defesa Civil registrou" in _cob(com, "VENDAVAL_GRANIZO")["justificativa"]
    assert "ranking de continuidade da ANEEL" in _cob(com, "DANOS_ELETRICOS")["justificativa"]
    assert any("S2iD" in f for f in com["fontes"]) and any("ANEEL" in f for f in com["fontes"])
    monkeypatch.setattr(motor.P, "desastres", lambda cod: None)              # sem os arquivos externos
    monkeypatch.setattr(motor.P, "continuidade_energia", lambda cod: None)
    sem = ficha(APTO_CURITIBA)
    assert [(c["min"], c["max"]) for c in com["coberturas"]] == [(c["min"], c["max"]) for c in sem["coberturas"]]
    assert com["plano"] == sem["plano"] and com["confianca"] == sem["confianca"]
    assert "Defesa Civil" not in _cob(sem, "VENDAVAL_GRANIZO")["justificativa"]


def test_municipio_sem_registro_nao_ganha_frase(linha):
    r = linha(codigo_ibge_municipio=2304400, municipio_real="Fortaleza")   # 0 registros de vento
    assert motor.contexto_territorio("VENDAVAL_GRANIZO", r) == ""
    assert "Fortaleza" in motor.contexto_territorio("DANOS_POR_AGUA", r)


def test_perguntas_de_valor_seguem_o_valor_da_informacao(ficha):
    f = ficha(APTO_CURITIBA, area_cadastrada_m2=0, padrao_construtivo_cadastrado="NAO_DISPONIVEL")
    valor = [p["reduz_faixa_ate"] for p in f["perguntas"] if "reduz_faixa_ate" in p]
    assert len(valor) >= 2 and valor == sorted(valor, reverse=True)


def test_confianca_area_presumida_e_baixa(ficha):
    f = ficha(APTO_CURITIBA, area_cadastrada_m2=0, pagamento_iptu_anual=0, energia_media_mensal_6m=0)
    assert f["confianca"] == "BAIXA" and "presumido: área" in f["confianca_motivo"]


def test_confianca_dado_estimado_nao_e_alta(ficha):
    f = ficha(APTO_CURITIBA, area_cadastrada_m2=0)
    assert f["confianca"] == "MEDIA" and "estimado: área" in f["confianca_motivo"]


def test_confianca_motivo_na_justificativa(ficha):
    import motor
    f = ficha(APTO_CURITIBA)
    assert f"Confiança {motor.NIVEL_TEXTO[f['confianca']]}:" in motor.justificativa(f)


def test_campo_vazio_baixa_a_confianca(ficha):
    cheio = ficha(APTO_CURITIBA, area_cadastrada_m2=110, padrao_construtivo_cadastrado="NORMAL",
                  material_parede_externa_cadastrado="ALVENARIA")
    vazio_ = ficha(APTO_CURITIBA, area_cadastrada_m2=110, padrao_construtivo_cadastrado="NAO_DISPONIVEL",
                   material_parede_externa_cadastrado="NAO_DISPONIVEL")
    assert cheio["completude"]["pct"] == 100 and vazio_["completude"]["pct"] < 100
    assert vazio_["confianca_score"] < cheio["confianca_score"]


def test_inquilino_vai_para_total_com_aluguel(ficha):
    f = ficha(APTO_CURITIBA, pagamento_aluguel_recorrente="SIM", valor_aluguel_recorrente=2000, parcela_financiamento_imobiliario=0)
    assert f["plano"] == "TOTAL"
    alug = _cob(f, "PERDA_PAGAMENTO_ALUGUEL")
    assert (alug["min"], alug["max"]) == (12000, 24000)


def test_justificativa_tem_alternativas(ficha):
    import motor
    f = ficha(APTO_CURITIBA)
    texto = motor.justificativa(f)
    assert texto.startswith("Recomendamos o plano")
    if f["plano"] != "ESSENCIAL":   # frase do slide 23 da Brasilseg
        assert "Se você escolher menos" in texto and "descobert" in texto
    if f["plano"] != "TOTAL":       # alternativa mais completa (RN-37)
        assert "acrescenta" in texto


# --- T4: validação e planilhas ----------------------------------------------------
import pytest  # noqa: E402
from templates import validar_templates  # noqa: E402


@pytest.fixture(scope="session")
def planilhas(teste, cal):
    fichas = motor.processar(teste, cal)
    return motor.para_templates(fichas, teste["template"])


def test_planilhas_validas(planilhas, teste):
    res, cob = planilhas
    assert validar_templates(res, cob, teste["template"], teste["template_coberturas"], teste["catalogo"]) == []


def test_138_casos_na_ordem_do_template(planilhas, teste):
    res, _ = planilhas
    assert len(res) == 138 and list(res.imovel_id) == list(teste["template"].imovel_id)


def test_validador_pega_erros(planilhas, teste):
    res, cob = planilhas
    cob = cob.copy()
    cob.loc[0, ["faixa_valor_min", "faixa_valor_max"]] = [50000, 1000]   # faixa invertida
    cob = cob[cob.cobertura != "QUEDA_AERONAVE"]                          # cobertura fixa faltando
    erros = validar_templates(res, cob, teste["template"], teste["template_coberturas"], teste["catalogo"])
    assert any("mínimo maior" in e for e in erros) and any("sem as fixas" in e for e in erros)


def test_validador_pega_plano_e_coberturas_inconsistentes(planilhas, teste):
    res, cob = planilhas
    res = res.copy()
    res.loc[0, "coberturas_recomendadas"] += "; QUEBRA_DE_VIDROS_EXTRA"      # RN-33: lista ≠ linhas
    cob = pd.concat([cob, cob.iloc[[0]]])                                        # linha duplicada
    cob.loc[cob.index[1], "confianca_estimativa"] = "ALTISSIMA"
    erros = validar_templates(res, cob, teste["template"], teste["template_coberturas"], teste["catalogo"])
    assert any("coberturas_recomendadas diferente" in e for e in erros)
    assert any("repetida" in e for e in erros) and any("fora de ALTA/MEDIA/BAIXA" in e for e in erros)


# --- T5: confiança, perguntas, justiça e coerência ------------------------------
import json  # noqa: E402


def test_dado_antigo_pesa_menos():
    novo = motor.peso_dado({"fonte_tipo": "TRANSACAO", "idade_meses": 3}, "bens")
    velho = motor.peso_dado({"fonte_tipo": "TRANSACAO", "idade_meses": 30}, "bens")
    assert velho < novo


def test_dado_confirmado_vale_o_maximo():
    assert motor.peso_dado({"natureza": "CONFIRMADO", "fonte_tipo": "PRESUMIDO", "idade_meses": 99}, "bens") == 1.0


def test_no_maximo_tres_perguntas_por_impacto(ficha):
    f = ficha("IMO_CASO_00001_01", gastos_material_construcao_24m=40000)
    assert len(f["perguntas"]) == 3 and f["perguntas_candidatas"] > 3
    assert [p["prioridade"] for p in f["perguntas"]] == sorted((p["prioridade"] for p in f["perguntas"]), reverse=True)


def test_pendencia_impede_confianca_alta(ficha):
    assert ficha(APTO_CURITIBA, gastos_material_construcao_24m=40000)["confianca"] != "ALTA"


def test_justica_ficha_inteira_igual(ficha):
    a = ficha(APTO_CURITIBA, renda_mensal=1800, idade=19, origem_renda="INFORMADA")
    b = ficha(APTO_CURITIBA, renda_mensal=34000, idade=85, origem_renda="PRESUMIDA")
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    texto = json.dumps(a)
    for chave in ['"renda', '"origem_renda"', '"idade"', '"quantidade_dependentes"', '"possui_pet', '"dependentes"']:
        assert chave not in texto


def test_area_maior_nunca_reduz_incendio(ficha):
    p = ficha(APTO_CURITIBA, area_cadastrada_m2=100)
    g = ficha(APTO_CURITIBA, area_cadastrada_m2=110)
    assert _cob(g, "INCENDIO_RAIO_EXPLOSAO_FUMACA")["max"] >= _cob(p, "INCENDIO_RAIO_EXPLOSAO_FUMACA")["max"]


def test_extremos_respeitam_limites(ficha):
    import parametros
    f = ficha(APTO_CURITIBA, compras_eletronicos_36m=900000, compras_moveis_36m=900000, compras_eletrodomesticos_36m=900000,
              gastos_vidracaria_24m=500000, area_cadastrada_m2=5000)
    for c in f["coberturas"]:
        lo, hi = parametros.LIMITES_PRODUTO[c["cobertura"]]
        assert isinstance(c["min"], int) and lo <= c["min"] <= c["max"] <= hi


def test_bens_de_outro_imovel_nao_entram(caso):
    _, b1 = caso("IMO_CASO_00005_01")
    _, b2 = caso("IMO_CASO_00005_02")
    assert set(b1.imovel_id_referencia) <= {"IMO_CASO_00005_01"} and set(b2.imovel_id_referencia) <= {"IMO_CASO_00005_02"}


def test_reprodutivel(tmp_path):
    import gerar
    gerar.gerar(tmp_path / "a")
    gerar.gerar(tmp_path / "b")
    for nome in ["template_resultado_times.csv", "template_coberturas_times.csv", "fichas.json"]:
        assert (tmp_path / "a" / nome).read_bytes() == (tmp_path / "b" / nome).read_bytes()


# --- T6: métricas e casos contrastantes ----------------------------------------
def test_metricas_e_casos(tmp_path):
    import gerar
    info = gerar.gerar(tmp_path)
    met = json.loads((tmp_path / "metricas.json").read_text(encoding="utf-8"))
    assert met["teste_justica_casos_alterados"] == 0
    assert met["familia_declarada_muda_valor_ou_confianca"] == 0
    assert met["elegibilidade"].get("NAO", 0) > 0 and met["confianca"].get("BAIXA", 0) > 0
    assert met["confianca_estabilidade_casos_que_mudam_com_pesos_20pct"] == 0
    assert met["casos_com_falha"] == 0 and met["estabilidade_plano_casos_que_mudam_com_valores_5pct"] <= 5
    assert met["elegibilidade_por_regra"]["NAO_ELEGIVEL"] == met["elegibilidade"]["NAO"]
    assert met["justica_por_quinto_de_renda"]["razao_elegibilidade_menor_maior"] >= 0.8
    larg = met["confianca_largura_incendio_mediana"]
    assert larg["ALTA"] <= larg["MEDIA"] <= larg["BAIXA"]
    assert met["completude_coberturas_fixas_pct"] == 100.0 and met["sensibilidade_area_casos_com_queda"] == 0
    assert "bens_pela_regiao_e_renda" in met["dados_faltantes"]
    assert met["dados_faltantes"]["backtest_bens_sem_compras"]["erro_mediano_regiao_e_renda_pct"] > 0
    assert all(info["casos_contrastantes"].values())


# --- Motivo 2.0 (mentoria 28/10: o porquê é o que diferencia) -------------------
import re  # noqa: E402

import motivo  # noqa: E402

TERMOS_INTERNOS = ("presumido", "estimado:", "sinais ainda são fracos", "não há sinais", "o cliente ",
                   "segundo risco", "elegibilidade a confirmar", "PRESUMIDO", "INFERIDO")


@pytest.fixture(scope="session")
def todas(teste, cal):
    return motor.processar(teste, cal)


def test_reais_arredonda_como_gente_fala():
    assert motivo.reais(48552) == "R$ 49 mil"
    assert motivo.reais(1_234_567) == "R$ 1,2 milhão"
    assert motivo.reais(950) == "R$ 950"
    assert motivo.reais(4_480) == "R$ 4,5 mil"
    assert motivo.reais(999_800) == "R$ 1 milhão" and motivo.reais(999.7) == "R$ 1 mil" and motivo.reais(9_980) == "R$ 10 mil"


def test_nenhum_motivo_generico(todas):
    for f in todas:
        assert all(m["codigo"] != "BASE" for m in f["motivos_plano"]), f["imovel_id"]
        assert any("R$" in m["texto"] for m in f["motivos_plano"]), f["imovel_id"]


def test_justificativa_sem_jargao_e_no_tamanho(todas):
    for f in todas:
        t = motor.justificativa(f)
        assert not any(x in t for x in TERMOS_INTERNOS), (f["imovel_id"], t)
        assert len(t.split()) <= (150 if f["elegibilidade"] == "NAO" else 130), (f["imovel_id"], len(t.split()))


def test_justificativa_diz_quanto_esta_em_jogo(todas):
    for f in todas:
        t = motor.justificativa(f)
        assert len(re.findall(r"R\$ \d", t)) >= 2, (f["imovel_id"], t)
        assert "Se você escolher" in t or f["plano"] == "ESSENCIAL" or f["elegibilidade"] == "NAO"


def test_coberturas_com_texto_personalizado(todas):
    for cob in ("INCENDIO_RAIO_EXPLOSAO_FUMACA", "DANOS_ELETRICOS", "DANOS_POR_AGUA", "VENDAVAL_GRANIZO"):
        textos = [c["justificativa"] for f in todas for c in f["coberturas"] if c["cobertura"] == cob]
        assert len(set(textos)) > len(textos) * 0.5, cob
        assert all("R$" in t for t in textos), cob


# --- F2: média da região em degraus (mentoria 28/10) ----------------------------
def test_area_sem_sinais_usa_municipio_e_tipo(linha, cal, dev):
    r = linha(area_cadastrada_m2=0, pagamento_iptu_anual=0, energia_media_mensal_6m=0,
              codigo_ibge_municipio=4106902, municipio_real="Curitiba", uf_real="PR", possui_termo_apartamento="SIM")
    d = motor.inferir_area(r, cal)
    e = dev["enderecos_imoveis"]
    alvo = e[(e.codigo_ibge_municipio == 4106902) & (e.possui_termo_apartamento == "SIM") & (e.area_cadastrada_m2 > 0)]
    assert d["valor"] == round(alvo.area_cadastrada_m2.median()) and d["regional"] == "município e tipo"
    assert "imóveis" in d["fonte"] and d["confianca"] == "BAIXA"


def test_municipio_fora_da_base_sobe_para_o_estado(linha, cal):
    r = linha(area_cadastrada_m2=0, pagamento_iptu_anual=0, energia_media_mensal_6m=0,
              codigo_ibge_municipio=4113700, municipio_real="Londrina", uf_real="PR")
    assert motor.inferir_area(r, cal)["regional"] == "estado"


def test_bens_sem_compras_usam_a_media_da_regiao(linha, cal, vazio):
    r = linha(compras_moveis_36m=0, compras_eletrodomesticos_36m=0, compras_eletronicos_36m=0)
    d = motor.estimar_bens(r, vazio, cal)
    assert d["regional"] and d["min"] > P.BENS_PISO and "região" in d["fonte"]
    assert d["eletricos"]["max"] < d["max"] and d["confianca"] == "BAIXA"


def test_cep_da_base_nao_tem_sinal(cal):
    t = cal["teste_cep"]   # RN-10: CEP agregado fictício; o degrau de CEP fica desligado
    assert abs(t["r2_cep"] - t["r2_cep_embaralhado"]) < 0.05 and not P.USAR_CEP


# --- F3: gerente como último recurso (mentoria 28/10) ---------------------------
def test_gerente_so_no_ultimo_caso(todas):
    for f in todas:
        if f["jornada"] == "GERENTE":
            obra = any(p["codigo"] == "POSSIVEL_REFORMA" for p in f["pendencias"])
            assert f["confianca"] == "BAIXA" or obra or f["canal_digital"]["usuario_app"] != "SIM", f["imovel_id"]
            assert f["motivo_jornada"]
    gerente = sum(f["jornada"] == "GERENTE" for f in todas)
    assert gerente <= 0.3 * sum(f["elegibilidade"] == "SIM" for f in todas)


def test_pergunta_simples_fica_no_app(ficha):
    f = ficha(APTO_CURITIBA, possui_seguro_residencial="SIM", qtd_produtos_seguridade=0)
    assert f["pendencias"] and f["jornada"] == "APP_COM_PERGUNTAS" and f["canal"] == "ONE_CLICK"


def test_sinal_de_obra_vai_ao_gerente(ficha):
    f = ficha(APTO_CURITIBA, gastos_material_construcao_24m=40000)
    assert f["jornada"] == "GERENTE" and "obra" in f["motivo_jornada"]


def test_nao_elegivel_nao_conta_como_venda(todas):
    for f in todas:
        if f["elegibilidade"] == "NAO":
            assert f["jornada"] == "SEM_NOVA_PROPOSTA"
