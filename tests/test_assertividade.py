"""Assertividade de cada cálculo que completa um dado faltante (plano de 28/10).
Validação cruzada em 5 dobras na base de desenvolvimento: o motor nunca é testado num imóvel que já viu."""
import math
from types import SimpleNamespace

import pytest

import assertividade as A
import motor


@pytest.fixture(scope="session")
def fichas_teste(teste, cal):
    return motor.processar(teste, cal)


CHAVES = {"o_que_estima", "como", "tem_gabarito", "metodo", "erro_mediano_pct", "ate_20pct_pct",
          "na_faixa_pct", "chute_erro_mediano_pct", "veredito"}


def test_todo_calculo_tem_boletim_com_as_mesmas_chaves(cal):
    b = cal["assertividade"]
    assert set(b) == {"area", "area_regional", "padrao_iptu", "area_x_padrao", "tipo", "vinculo", "uso",
                      "bens", "bens_sem_compras", "cep"}
    assert all(CHAVES <= set(x) for x in b.values())


def test_boletim_da_area(cal):
    a = cal["assertividade"]["area"]
    assert 13 <= a["erro_mediano_pct"] <= 17
    assert 77 <= a["na_faixa_pct"] <= 86
    assert a["chute_erro_mediano_pct"] > 2 * a["erro_mediano_pct"]
    assert a["tem_gabarito"] and a["metodo"].startswith("validação cruzada em 5 dobras")


def test_regiao_e_pior_que_os_sinais_e_melhor_que_o_chute(cal):
    b = cal["assertividade"]
    assert b["area"]["erro_mediano_pct"] < b["area_regional"]["erro_mediano_pct"] < b["area"]["chute_erro_mediano_pct"]


def test_padrao_exato_pelo_iptu_perde_do_chute_e_por_isso_vira_intervalo(cal):
    p = cal["assertividade"]["padrao_iptu"]
    assert p["classe_exata_pct"] < p["chute_classe_exata_pct"]   # o IPTU não diz o padrão exato
    assert p["na_faixa_pct"] >= 95                                # mas o intervalo de 2 classes acerta


def test_sem_gabarito_e_dito(cal):
    for nome in ("bens", "uso", "vinculo", "tipo"):
        b = cal["assertividade"][nome]
        assert b["tem_gabarito"] is False and b["erro_mediano_pct"] is None
    assert cal["assertividade"]["tipo"]["concordancia_pct"] == 100.0
    assert 0.5 < cal["assertividade"]["bens"]["correlacao_compras_bens"] < 0.8


def test_luz_nao_indica_casa_vazia(cal):
    u = cal["assertividade"]["uso"]
    assert abs(u["luz_principal"] - u["luz_nao_principal"]) < 0.1


def test_cep_e_ruido(cal):
    c = cal["assertividade"]["cep"]
    assert c["r2_cep"] <= c["r2_cep_embaralhado"] + 0.02 and "descartado" in c["veredito"]


def test_dobras_reprodutiveis(dev, cal):
    assert motor.calibrar(dev)["assertividade"] == cal["assertividade"]


def test_motor_funciona_sem_assertividade(teste, cal):
    # RN-12: a medição é para explicar; sem ela o motor ainda responde os 138 casos
    sem = {k: v for k, v in cal.items() if k not in ("assertividade", "area_padrao_q")}
    fichas = motor.processar(teste, sem)
    assert len(fichas) == 138 and all(f["plano"] in ("ESSENCIAL", "PRATICO", "TOTAL") for f in fichas)
    assert all(motor.justificativa(f) for f in fichas)


# --- Área pela média geométrica e faixa calibrada de área × padrão ---------------
def test_media_geometrica():
    cal = {"iptu_m2": {"1": 10.0}, "energia_m2": {"1": 2.0}, "iptu_m2_geral": 10.0, "energia_m2_geral": 2.0}
    r = SimpleNamespace(codigo_ibge_municipio=1, pagamento_iptu_anual=1000.0, energia_media_mensal_6m=400.0)
    # IPTU diz 100 m², luz diz 200 m²: 100^0,6 × 200^0,4 = 131,95 m² (a média comum daria 140)
    assert motor._area_estimada(r, cal) == pytest.approx(131.95, abs=0.01)


def test_media_geometrica_com_um_sinal_so():
    cal = {"iptu_m2": {}, "energia_m2": {}, "iptu_m2_geral": 10.0, "energia_m2_geral": 2.0}
    r = SimpleNamespace(codigo_ibge_municipio=1, pagamento_iptu_anual=0.0, energia_media_mensal_6m=400.0)
    assert motor._area_estimada(r, cal) == pytest.approx(200.0)


def test_faixa_calibrada_nos_64_casos(fichas_teste):
    calibrados = [f for f in fichas_teste if f["valor_imovel"]["origem_padrao"] == A.ORIGEM_CALIBRADA]
    assert len(calibrados) == 64
    assert all(f["campos"]["area"]["natureza"] == "ESTIMADO" for f in calibrados)
    larg = sorted(f["valor_imovel"]["reconstrucao_max"] / f["valor_imovel"]["reconstrucao_min"] for f in calibrados)
    assert larg[len(larg) // 2] <= 2.2   # antes: 3,1


def test_faixa_calibrada_contem_80(cal):
    # percentis 9%–91% (~80%), alargados até a faixa de quem tem padrão normal (revisão de código): ~88%
    b = cal["assertividade"]["area_x_padrao"]
    assert 80 <= b["na_faixa_pct"] <= 92
    assert b["largura_calibrada"] < b["largura_pior_caso"]
    lo, hi = cal["area_padrao_q"]
    assert 0.5 < lo < 1 < hi < 1.6


def test_quantis_calibrados_sao_fora_da_amostra(dev, cal):
    # os percentis vêm dos erros das 5 dobras (o motor não "cola" do imóvel que mede)
    assert cal["area_padrao_q"] == tuple(cal["assertividade"]["area_x_padrao"]["quantis"])


def test_casos_no_teste_contados(fichas_teste, cal):
    b = A.com_casos_no_teste(cal["assertividade"], fichas_teste)
    assert b["area"]["casos_no_teste"] == 92 and b["area_regional"]["casos_no_teste"] == 0
    assert b["area_x_padrao"]["casos_no_teste"] == 64 and b["bens_sem_compras"]["casos_no_teste"] == 0
    assert b["uso"]["casos_no_teste"] == 31 and b["tipo"]["casos_no_teste"] == 138
    assert math.isclose(sum(1 for f in fichas_teste if f["campos"]["area"]["natureza"] == "ESTIMADO"), 92)


def test_regra_do_incendio_explica_a_faixa_calibrada(fichas_teste):
    f = next(f for f in fichas_teste if f["valor_imovel"]["origem_padrao"] == A.ORIGEM_CALIBRADA)
    regra = next(c["regra"] for c in f["coberturas"] if c["cobertura"] == "INCENDIO_RAIO_EXPLOSAO_FUMACA")
    assert "faixa calibrada de área × padrão" in regra and "m² de padrão normal" in regra


def test_gerar_grava_assertividade_com_casos_do_teste(tmp_path):
    import json

    import gerar
    gerar.gerar(tmp_path)
    b = json.loads((tmp_path / "assertividade.json").read_text(encoding="utf-8"))
    assert b["area"]["casos_no_teste"] == 92 and b["area"]["erro_mediano_pct"] < 17
    met = json.loads((tmp_path / "metricas.json").read_text(encoding="utf-8"))
    assert met["assertividade"]["area_x_padrao"]["casos_no_teste"] == 64


def test_padrao_desconhecido_nunca_tem_teto_menor_que_o_normal(ficha):
    normal = ficha("IMO_CASO_00005_01", padrao_construtivo_cadastrado="NORMAL", area_cadastrada_m2=0)
    nao_sei = ficha("IMO_CASO_00005_01", padrao_construtivo_cadastrado="NAO_DISPONIVEL", area_cadastrada_m2=0)
    assert nao_sei["valor_imovel"]["origem_padrao"] == A.ORIGEM_CALIBRADA
    assert nao_sei["valor_imovel"]["reconstrucao_min"] <= normal["valor_imovel"]["reconstrucao_min"]
    assert nao_sei["valor_imovel"]["reconstrucao_max"] >= normal["valor_imovel"]["reconstrucao_max"]


def test_backtest_ignora_area_que_nao_deu_para_estimar(dev):
    m = dev["enderecos_imoveis"].merge(dev["sinais_imobiliarios"], on=["imovel_id", "cliente_id"])
    a = m[m.area_cadastrada_m2 > 0].copy()
    i = a[a.padrao_construtivo_cadastrado == "NORMAL"].index[0]
    a.loc[i, ["pagamento_iptu_anual", "energia_media_mensal_6m"]] = 0
    q = A.backtest(a)["area_padrao_quantis"]
    assert all(math.isfinite(x) for x in q)


def test_pergunta_nao_promete_mais_que_a_faixa_calibrada(fichas_teste):
    for f in fichas_teste:
        if f["valor_imovel"]["origem_padrao"] != A.ORIGEM_CALIBRADA:
            continue
        largura = f["valor_imovel"]["reconstrucao_max"] - f["valor_imovel"]["reconstrucao_min"]
        for p in f["perguntas"]:
            if p["codigo"] in ("AREA", "PADRAO"):
                assert p["reduz_faixa_ate"] <= largura + 1000


def test_regra_calibrada_nao_conta_o_padrao_duas_vezes(fichas_teste):
    import parametros as P
    for f in fichas_teste:
        vi = f["valor_imovel"]
        if vi["origem_padrao"] == A.ORIGEM_CALIBRADA:
            # a reconstrução é área × padrão × custo SEM fator: o custo mostrado é o SINAPI/CUB de base
            uf = f["local"].split("/")[1]
            assert tuple(vi["custo_m2"]) == tuple(round(x, 2) for x in P.custo_m2(uf))
            regra = next(c["regra"] for c in f["coberturas"] if c["cobertura"] == "INCENDIO_RAIO_EXPLOSAO_FUMACA")
            if not vi["estrutura_do_locador"]:
                assert f"{vi['custo_m2'][0]:,.0f}".replace(",", ".") in regra
