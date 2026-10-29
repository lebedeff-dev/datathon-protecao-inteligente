"""O motivo "feito para você" (plano de 28/10): o fato que diferencia o cliente dos vizinhos,
a casa e a cidade dele, o risco do lugar, o que fica descoberto em reais e a confiança em números."""
import copy

import pytest

import motivo
import motor


@pytest.fixture(scope="session")
def fichas(teste, cal):
    return motor.processar(teste, cal)


def _viz(valor, p10=1000, p25=2000, p75=8000, p90=12000, nivel="município e tipo", n=40):
    return {"valor": valor, "p10": p10, "p25": p25, "p75": p75, "p90": p90, "nivel": nivel, "n": n}


def _ficha(fichas, plano="PRATICO", **viz):
    f = copy.deepcopy(next(x for x in fichas if x["plano"] == plano and x["campos"]["tipo"]["valor"] == "APARTAMENTO"))
    f["vizinhos"] = viz
    return f


# --- Tarefa 3 · fato distintivo -------------------------------------------------
def test_vizinhos_na_ficha(fichas):
    v = fichas[0]["vizinhos"]
    assert {"compras", "eletronicos"} <= set(v)
    assert v["compras"]["p25"] <= v["compras"]["p75"] and v["compras"]["n"] >= 20


def test_aluguel_so_para_quem_paga(fichas):
    for f in fichas:
        paga = f["campos"]["vinculo"]["valor"] == "INQUILINO"
        assert ("aluguel" in f["vizinhos"]) == paga


def test_fato_distintivo_acima(fichas):
    f = _ficha(fichas, eletronicos=_viz(13000))
    f["necessidades"] = []   # o porquê não falou dos eletrônicos: o fato traz o valor
    texto = motivo.fato_distintivo(f)
    assert "mais do que 9 em cada 10" in texto and f"clientes com apartamento {motivo.na_cidade(f)}" in texto
    assert "R$ 13 mil" in texto


def test_fato_distintivo_3_em_4(fichas):
    f = _ficha(fichas, eletronicos=_viz(9000))
    f["necessidades"] = []
    assert "mais do que 3 em cada 4" in motivo.fato_distintivo(f)


def test_fato_sem_repetir_o_valor_do_porque(fichas):
    # o porquê já disse "pelo menos R$ 13 mil em eletrônicos" (valor de hoje): o fato não repete outro número
    f = _ficha(fichas, eletronicos=_viz(13000))
    f["necessidades"] = [{"codigo": "ROUBO", "provas": [{"codigo": "ELETRONICOS"}]}]
    texto = motivo.fato_distintivo(f)
    assert texto.startswith("Em eletrônicos, você está acima de 9 em cada 10") and "R$" not in texto


def test_fato_distintivo_no_meio_some(fichas):
    f = _ficha(fichas, eletronicos=_viz(5000), compras=_viz(5000))
    assert motivo.fato_distintivo(f) is None


def test_degrau_estado_nao_inventa_cidade(fichas):
    f = _ficha(fichas, eletronicos=_viz(13000, nivel="estado"))
    f["necessidades"] = []
    texto = motivo.fato_distintivo(f)
    assert motivo.nome_cidade(f) not in texto and f"clientes de {f['local'].split('/')[1]}" in texto


def test_cidade_com_acento_e_preposicao():
    assert motivo.na_cidade({"local": "Sao Paulo/SP"}) == "em São Paulo"
    assert motivo.na_cidade({"local": "Rio de Janeiro/RJ"}) == "no Rio de Janeiro"
    assert motivo.da_cidade({"local": "Goiania/GO"}) == "de Goiânia"


def test_essencial_com_poucos_eletronicos_explica_por_que_basta(fichas):
    f = _ficha(fichas, plano="ESSENCIAL", eletronicos=_viz(1500))
    f["campos"]["tipo"]["valor"] = "APARTAMENTO"
    texto = motivo.fato_distintivo(f)
    assert "menos do que 3 em cada 4" in texto and "roubo" in texto


def test_fato_nunca_usa_idade(ficha):
    a = ficha("IMO_CASO_00004_01", idade=25)
    b = ficha("IMO_CASO_00004_01", idade=80)
    assert motor.justificativa(a) == motor.justificativa(b)


# --- Tarefa 4 · o motivo novo -----------------------------------------------------
import metricas  # noqa: E402

TIPO_NO_TEXTO = {"APARTAMENTO": "apartamento", "CASA": "casa", "CASA_EM_CONDOMINIO": "casa em condomínio"}


def test_motivo_cita_casa_e_cidade(fichas):
    for f in fichas:
        t = motor.justificativa(f)
        assert motivo.na_cidade(f) in t and f"seu {TIPO_NO_TEXTO[f['campos']['tipo']['valor']]}" in t.replace("sua casa", "seu casa")


def test_motivos_diferentes(fichas):
    q = metricas.qualidade_do_motivo(fichas)
    # antes (27/10): 83 esqueletos únicos, semelhança 0,29, frase mais repetida em 93 motivos, cidade em 0
    assert q["esqueletos_unicos"] >= 120 and q["semelhanca_media"] < 0.22
    assert q["cita_cidade_pct"] == 100.0 and q["frase_mais_repetida_n"] <= 40


def test_confianca_com_numero(fichas):
    f = next(f for f in fichas if f["confianca"] != "ALTA" and f["campos"]["area"].get("classe") == "ESTIMADO"
             and f["campos"]["uso"].get("classe") != "PRESUMIDO" and f["campos"]["bens"].get("classe") != "PRESUMIDO")
    t = motor.justificativa(f)
    assert "2 de cada 3" in t and "IPTU" in t


def test_lacuna_em_reais(fichas):
    for f in fichas:
        t = motor.justificativa(f)
        if f["plano"] == "PRATICO" and not f["pendencias"]:
            frase = next(s for s in t.split(". ") if "Se você escolher menos" in s)
            assert "R$" in frase and "roubo" in frase
        if f["plano"] == "TOTAL" and f["campos"]["vinculo"]["valor"] == "INQUILINO":
            assert "de aluguel por mês" in t


def test_risco_do_lugar(fichas):
    poa = next(f for f in fichas if f["local"].startswith("Porto Alegre"))
    assert "33º de 33" in motivo.risco_do_lugar(poa) and "em último lugar" in motivo.risco_do_lugar(poa)
    fortaleza = next(f for f in fichas if f["local"].startswith("Fortaleza"))
    assert motivo.risco_do_lugar(fortaleza) == ""   # 23º de 33 e nada da Defesa Civil desde 2016: sem frase
    salvador = next(f for f in fichas if f["local"].startswith("Salvador"))
    assert "Defesa Civil registrou 2 ocorrências" in motivo.risco_do_lugar(salvador)


def test_maioria_dos_motivos_tem_fato_ou_risco_da_cidade(fichas):
    q = metricas.qualidade_do_motivo(fichas)
    assert q["com_risco_da_cidade_pct"] >= 45 and q["com_fato_dos_vizinhos_pct"] >= 35


def test_tamanho_e_termos(fichas):
    for f in fichas:
        t = motor.justificativa(f)
        assert len(t.split()) <= motivo.MAX_PALAVRAS == 140, (f["imovel_id"], len(t.split()), t)
        assert not any(x in t for x in motivo.TERMOS_INTERNOS)


# --- Tarefa 5 · perguntas com o porquê ------------------------------------------------
def test_pergunta_da_area_diz_a_faixa_e_quanto_muda(fichas):
    com = [(f, p) for f in fichas for p in f["perguntas"] if p["codigo"] == "AREA"]
    assert com
    for f, p in com:
        a = f["campos"]["area"]
        assert f"de {round(a['min'])} a {round(a['max'])} m²" in p["texto"]
        assert "R$" in p["texto"] and "incêndio" in p["texto"]


def test_perguntas_de_valor_dizem_por_que(fichas):
    for f in fichas:
        for p in f["perguntas"]:
            if p["codigo"] in ("BENS", "PADRAO"):
                assert "R$" in p["texto"], p["texto"]


def test_maximo_3_perguntas_continua(fichas):
    assert max(len(f["perguntas"]) for f in fichas) <= 3
