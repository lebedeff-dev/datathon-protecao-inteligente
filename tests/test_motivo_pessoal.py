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
    texto = motivo.fato_distintivo(f)
    assert "mais do que 9 em cada 10" in texto and f"clientes com apartamento {motivo.na_cidade(f)}" in texto
    assert "R$ 13 mil" in texto


def test_fato_distintivo_3_em_4(fichas):
    f = _ficha(fichas, eletronicos=_viz(9000))
    assert "mais do que 3 em cada 4" in motivo.fato_distintivo(f)


def test_fato_distintivo_no_meio_some(fichas):
    f = _ficha(fichas, eletronicos=_viz(5000), compras=_viz(5000))
    assert motivo.fato_distintivo(f) is None


def test_degrau_estado_nao_inventa_cidade(fichas):
    f = _ficha(fichas, eletronicos=_viz(13000, nivel="estado"))
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
