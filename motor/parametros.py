"""Parâmetros do motor.

Toda premissa numérica fica aqui, separada da lógica, com a origem escrita ao
lado: cláusula das Condições Gerais (CG v1.4), print do app atual, fonte externa
(motor/externos/FONTES.md) ou "premissa do time".

Regra do projeto: idade NÃO entra em nenhum parâmetro de decisão (guardrail do
guia; RN-07). A renda deixou de ser tratada como dado sensível (mentoria BB de
28/10) e entra num ponto só: RENDA_NOS_BENS_SEM_COMPRAS. Dependentes e pet só
entram como necessidade de RC informada pelo cliente, nunca em valor, risco,
canal ou confiança.
"""
import csv
import statistics
from functools import lru_cache
from pathlib import Path

EXTERNOS = Path(__file__).resolve().parent / "externos"


def _ler_csv(nome):
    caminho = EXTERNOS / nome
    if not caminho.exists():
        return []
    with open(caminho, encoding="utf-8") as f:
        return list(csv.DictReader(f))


# --- Custo de reconstrução (R$/m²) --------------------------------------------
# Mínimo: SINAPI ago/2026 sem desoneração (IBGE). Máximo: CUB R8-N, só quando veio
# do site ou PDF oficial do Sinduscon. CUB de agregador (status "validar") não entra:
# nesse caso o máximo é SINAPI × razão CUB/SINAPI medida nas UFs com CUB oficial.
CUSTO_M2_NEUTRO = (2100.0, 2500.0)  # usado se a UF não estiver nas tabelas


def referencia(nome_csv, coluna):
    """Último valor de `coluna` no CSV (ex.: mês de referência), para citar a fonte com a data certa."""
    linhas = _ler_csv(nome_csv)
    return linhas[-1].get(coluna, "") if linhas else ""


@lru_cache(maxsize=None)
def _tabela_custo():
    sinapi = {l["uf"]: float(l["sinapi_m2_sem_desoneracao"]) for l in _ler_csv("sinapi_uf.csv")}
    cub = {l["uf"]: float(l["cub_r8n_m2"]) for l in _ler_csv("cub_uf.csv") if l.get("status") == "oficial"}
    razoes = [cub[uf] / sinapi[uf] for uf in cub if uf in sinapi]
    razao = statistics.median(razoes) if razoes else 1.15
    return sinapi, cub, razao


def custo_m2(uf):
    """(mínimo SINAPI, máximo CUB oficial ou SINAPI × razão) em R$/m²; neutro sem SINAPI."""
    sinapi, cub, razao = _tabela_custo()
    lo = sinapi.get(uf)
    if lo is None:
        return CUSTO_M2_NEUTRO
    hi = cub.get(uf, round(lo * razao, 2))
    return (min(lo, hi), max(lo, hi))


def fonte_custo(uf):
    """Texto da fonte do máximo, para a regra de cálculo."""
    sinapi, cub, razao = _tabela_custo()
    if uf not in sinapi:
        return "valor neutro (sem SINAPI da UF)"
    return f"CUB {uf} oficial" if uf in cub else f"SINAPI {uf} × {razao:.3f} (razão CUB/SINAPI das UFs com CUB oficial)"


def fonte_disponivel(uf):
    sinapi, _, _ = _tabela_custo()
    return uf in sinapi


# Ajuste pelo padrão construtivo cadastrado (premissa do time).
FATOR_PADRAO = {"ECONOMICO": 0.85, "NORMAL": 1.0, "SUPERIOR": 1.30}
# Padrão não cadastrado (98 dos 138 casos de teste): em vez de supor "normal", a faixa vai do
# econômico ao superior. A incerteza do dado aparece no valor, e a pergunta do padrão ganha prioridade.
FATOR_PADRAO_DESCONHECIDO = (0.85, 1.30)


def fator_padrao(padrao):
    """(fator mínimo, fator máximo) do padrão construtivo cadastrado."""
    f = FATOR_PADRAO.get(str(padrao).upper())
    return (f, f) if f else FATOR_PADRAO_DESCONHECIDO


# Padrão vazio, mas área cadastrada: o IPTU por m² comparado à mediana do município indica o padrão,
# porque a planta genérica de valores do IPTU considera o padrão de acabamento. Na base de
# desenvolvimento (273 imóveis com área e padrão), a mediana dessa razão é 0,82 no econômico,
# 0,98 no normal e 1,32 no superior. Abaixo de 0,90 o superior é descartado; acima de 1,15, o
# econômico. Estreita 178 dos 273 e o padrão real fica dentro do intervalo em 98,5% (metricas.py).
IPTU_REL_SEM_SUPERIOR = 0.90
IPTU_REL_SEM_ECONOMICO = 1.15


def fator_padrao_pelo_iptu(iptu_rel):
    """(fator mínimo, fator máximo) pelo IPTU/m² relativo ao município; None se não estreitar."""
    if iptu_rel is None or not iptu_rel > 0:
        return None
    if iptu_rel < IPTU_REL_SEM_SUPERIOR:
        return (FATOR_PADRAO["ECONOMICO"], FATOR_PADRAO["NORMAL"])
    if iptu_rel > IPTU_REL_SEM_ECONOMICO:
        return (FATOR_PADRAO["NORMAL"], FATOR_PADRAO["SUPERIOR"])
    return None

# Segundo risco (CG cl. 15.2): apartamento, casa em condomínio ou imóvel financiado.
# A estrutura é paga primeiro pelo seguro do condomínio/financiamento; o residencial
# cobre acabamentos e benfeitorias. Para desligar a regra, use (1.0, 1.0).
FRACAO_ACABAMENTOS = (0.25, 0.40)


# --- IPCA: compras de 36 meses a preço de hoje ---------------------------------
@lru_cache(maxsize=None)
def _ipca_12m():
    linhas = _ler_csv("ipca_mensal.csv")
    if not linhas:
        return 0.0
    fator = 1.0
    for l in linhas[-12:]:
        fator *= 1 + float(l["variacao_mensal_pct"]) / 100
    return fator - 1


IPCA_12M = _ipca_12m()
FATOR_IPCA = (1 + IPCA_12M) ** 1.5  # meio da janela de 36 meses = 18 meses


# --- Aluguel de mercado (FipeZAP set/2026) -------------------------------------
@lru_cache(maxsize=None)
def _tabela_aluguel():
    return {l["uf"]: float(l["aluguel_m2"]) for l in _ler_csv("fipezap_aluguel.csv")}


def aluguel_m2(uf):
    """R$/m² de aluguel na capital da UF (as 10 cidades da base são capitais); None se faltar."""
    return _tabela_aluguel().get(uf)


# --- Acionamentos reais do Seguro Residencial BB (jan/2023 a mai/2026) ---------
# Só entra no TEXTO do motivo (por que a cobertura importa), nunca no valor. Sem o arquivo,
# o motor roda igual e o texto sai sem a frase.
@lru_cache(maxsize=None)
def _tabela_sinistros():
    return {l["cobertura"]: l for l in _ler_csv("sinistros_residencial_bb.csv")}


def sinistros_pct(cobertura):
    """% dos acionamentos do Seguro Residencial BB nessa cobertura, ou None."""
    l = _tabela_sinistros().get(cobertura)
    return float(l["pct_acionamentos"]) if l else None


# Fonte SECUNDÁRIA (dado da BB Seguros divulgado à imprensa, sem API nem relatório oficial): só contexto no texto.
FONTE_SINISTROS = "BB Seguros, dado divulgado à imprensa (Monitor Mercantil, 22/07/2026): acionamentos jan/2023 a mai/2026 [fonte secundária]"


# --- Território: desastres (Atlas/S2iD) e quedas de energia (ANEEL), por município ---
# Mesma regra dos sinistros: só reforçam o TEXTO do motivo; sem o arquivo, a frase some.
@lru_cache(maxsize=None)
def _tabela_desastres():
    return {l["codigo_ibge_municipio"]: l for l in _ler_csv("desastres_municipio.csv")}


def desastres(codigo_ibge):
    """Registros oficiais de chuva/alagamento/enxurrada e de vendaval/granizo no município, ou None."""
    return _tabela_desastres().get(str(codigo_ibge))


@lru_cache(maxsize=None)
def _tabela_energia():
    return {l["codigo_ibge_municipio"]: l for l in _ler_csv("aneel_continuidade.csv")}


def continuidade_energia(codigo_ibge):
    """Distribuidora do município e posição no ranking de continuidade da ANEEL 2025, ou None."""
    return _tabela_energia().get(str(codigo_ibge))


FONTE_DESASTRES = "Atlas Digital de Desastres no Brasil / S2iD (Sedec/MIDR), registros de 1991 a 2025"
FONTE_ANEEL = "Ranking de Continuidade do Fornecimento 2025 (ANEEL)"


# --- Bens (três âncoras) -------------------------------------------------------
FATOR_ESTOQUE = 2.7   # estoque ≈ compras/ano × vida útil (~8 anos) = 2,7 × compras de 36 meses (premissa)
BENS_PISO = 15000     # cesta mínima de uma casa quando não há compras nem bens (premissa)
# Renda (mentoria BB de 28/10: renda não é dado sensível). Entra só nos bens de quem não tem
# compras nem bens ligados ao imóvel, combinada com a média da região por média geométrica,
# para nenhum dos dois decidir sozinho (RN-08). Fora da amostra, o erro mediano das compras
# cai de ~40% (só região) para ~23% (região e renda): ver calibrar(). Quem tem compras segue
# pelas compras (a prova vence a estimativa), e a renda não entra em plano, elegibilidade,
# canal nem confiança. False volta ao comportamento anterior (só a média da região).
RENDA_NOS_BENS_SEM_COMPRAS = True

# --- Limites do produto (prints do app atual; máximos sem print são premissa) ---
LIMITES_PRODUTO = {
    "INCENDIO_RAIO_EXPLOSAO_FUMACA": (100000, 600000),
    "DANOS_POR_AGUA": (3000, 50000),
    "VENDAVAL_GRANIZO": (1000, 60000),
    "IMPACTO_VEICULOS_TERRESTRES": (1000, 20000),
    "QUEDA_AERONAVE": (1000, 20000),
    "DANOS_ELETRICOS": (5000, 30000),
    "ROUBO_FURTO_ARROMBAMENTO": (1000, 45000),
    "QUEBRA_DE_VIDROS": (1000, 25000),
    "RESPONSABILIDADE_CIVIL_FAMILIAR": (10000, 200000),
    "PERDA_PAGAMENTO_ALUGUEL": (5000, 30000),
    "DESPESAS_EMERGENCIAIS": (2000, 15000),
}
MESES_PERDA_ALUGUEL = (6, 12)

# --- Elegibilidade, plano e canal ----------------------------------------------
OBRA_LIMIAR_CONFIRMAR = 15000   # gasto em material de construção (24 meses) que pede confirmação
BENS_RELEVANTES = 36000         # bens comprovados acima da mediana da base de desenvolvimento (acende ROUBO)
PORTATEIS_RELEVANTES = 10000    # eletrônicos comprovados acima da mediana da base de desenvolvimento (acende ROUBO)
# Recomendação "no limite": o valor que decide está a menos de 15% do limite (para cima ou para baixo).
# Os limites são medianas, não um corte atuarial; a faixa assume essa incerteza e gera a pergunta que decide.
FAIXA_NO_LIMITE = 0.15
MATURIDADE_MIN_ONE_CLICK = 40   # comportamento digital, não atributo pessoal

# --- Confiança e perguntas ------------------------------------------------------
# Três dimensões de qualidade do dado, como na BCBS 239 (bancos) e nas notas por campo
# do prefill de seguradoras: precisão (peso da fonte), atualidade (meia-vida) e
# completude (campos do imóvel que vieram vazios).
# DERIVADO = calculado a partir de outros sinais (ex.: área pelo IPTU e pela energia).
PESO_FONTE = {"CONFIRMADO": 1.0, "DOCUMENTO": 0.9, "TRANSACAO": 0.8, "DERIVADO": 0.7, "INFERIDO": 0.6, "PRESUMIDO": 0.5}
MEIA_VIDA_MESES = {"vinculo": 12, "area": 120, "bens": 36, "uso": 12, "tipo": 120}
# O NÍVEL de confiança sai de regra sobre a classe de cada dado crítico (motor.confianca_geral),
# não de um corte na nota: com corte, 101 dos 138 casos ficavam a 3 pontos de mudar de nível.
CLASSE_FONTE = {"CONFIRMADO": "OBSERVADO", "DOCUMENTO": "OBSERVADO", "TRANSACAO": "OBSERVADO",
                "DERIVADO": "ESTIMADO", "INFERIDO": "ESTIMADO", "PRESUMIDO": "PRESUMIDO"}
# Completude: quanto a nota (só detalhe) cai quando o campo do imóvel veio vazio (premissa do time).
PENALIDADE_COMPLETUDE = {"area_cadastrada_m2": 0.15, "padrao_construtivo_cadastrado": 0.01,
                         "material_parede_externa_cadastrado": 0.01}
CAMPOS_COMPLETUDE = tuple(PENALIDADE_COMPLETUDE)
MAX_PERGUNTAS = 3
# Faixa da área estimada: percentis da razão área real ÷ estimada na base de desenvolvimento.
# Com 10% e 90%, a faixa continha a área real em 78,3% fora da amostra; com 9% e 91%, em 80,9%
# (meta: 80%). Sugestão P1 do relatório de validação (PR #14).
AREA_QUANTIS = (0.09, 0.91)
# Média da região em degraus (mentoria de 28/10): município + tipo → município → estado → geral.
# Um degrau só vale com pelo menos este número de imóveis na base de desenvolvimento.
REGIONAL_MIN_IMOVEIS = 20
# O CEP agregado da base é fictício (guia; RN-10) e não tem sinal: explica a variação do IPTU/m²
# tanto quanto um CEP embaralhado (calibrar() refaz esse teste). Ligar só com CEP real.
USAR_CEP = False
# Pergunta de valor que aperta a faixa em menos que isto não vale o esforço do cliente (premissa do time;
# RN-36 "poucas e priorizadas" e RN-51 "equilíbrio"). Cerca de 1% de um incêndio típico.
VALOR_MINIMO_PERGUNTA = 5000

# faixa() usa este nome
LIMITES_COBERTURA = LIMITES_PRODUTO
