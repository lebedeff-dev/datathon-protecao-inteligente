---
tags: [projeto, fontes, apis]
atualizado: 2026-10-28
---
# 🌐 04 · Fontes externas e APIs

> [!fonte] A regra
> O motor **não chama a internet enquanto roda**. Ele lê os arquivos de `motor/externos/`. As fontes com API oficial são renovadas por `python motor/externos/coletar.py --ao-vivo`, que **valida a resposta antes de gravar** e, se a API falhar, mantém o último valor salvo, com a data. Sem nenhum arquivo, o motor usa valores neutros e baixa a confiança (RN-12). Fonte externa só reforça: nunca decide sozinha (RN-08).

| Fonte | Arquivo | Para quê no motor | Como chega | Data | Sem ela |
|---|---|---|---|---|---|
| **SINAPI** (IBGE) | `sinapi_uf.csv` | Mínimo do custo do m² → incêndio, água, vendaval, RC | ✅ **API SIDRA** (tabelas 6586 e 2296) | set/2026 | Custo neutro (R$ 2.100–2.500/m²) e confiança baixa |
| **IPCA** (Banco Central) | `ipca_mensal.csv` | Compras a preço de hoje (fator 1,069) | ✅ **API SGS** (série 433) | out/2025–set/2026 | Fator 1,0 |
| **CUB R8-N** (Sinduscons) | `cub_uf.csv` | Máximo do custo do m² | Site ou PDF oficial (7 estados); RJ, PE e CE pela razão 1,14 | set/2026 | Razão sobre o SINAPI |
| **FipeZAP Locação** (Fipe) | `fipezap_aluguel.csv` | Perda de aluguel de quem mora no próprio imóvel | PDF | set/2026 | 0,4%–0,5% do valor do imóvel |
| **Sinistros BB** | `sinistros_residencial_bb.csv` | "Danos elétricos são 53,3% dos acionamentos" (só texto) | Matéria com dado da BB | jan/2023–mai/2026 | A frase some |
| **Atlas de Desastres / S2iD** (MIDR) | `desastres_municipio.csv` | Chuvas e vendavais na cidade (só texto) | Arquivo oficial (sem API); `coletar.py --atlas` | 1991–2025 | A frase some |
| **ANEEL** | `aneel_continuidade.csv` | Quedas de energia da distribuidora (só texto) | Ranking oficial | 2025 | A frase some |
| **Condições Gerais BB v1.4** | (regras no código) | Segundo risco, limite único, bens não cobertos | PDF lido | v1.4 | — |

Detalhe de licença, transformação e limitação de cada uma: `motor/externos/FONTES.md`. As notas [[Atlas Digital de Desastres]] e [[ANEEL continuidade]] trazem as tabelas por cidade.

## Como uma fonte nova entra
1. CSV em `motor/externos/` + linha no `FONTES.md` (fonte, data de acesso, licença, nível, transformação, limitação).
2. Leitura em `parametros.py` que devolve `None` quando o arquivo falta.
3. Um teste mostrando que o motor roda sem ela.
4. Se tiver API: uma função em `coletar.py` que valida antes de gravar.

## O que pesquisamos e ainda não entrou
| Fonte | Traria | Por que ainda não |
|---|---|---|
| SUSEP SES | Sinistros e prêmios do residencial por estado | Base grande; contexto, não decisão |
| ANEEL DEC/FEC por conjunto | Quedas de energia por bairro | Arquivo de 30 MB; o ranking da distribuidora já serve ao motivo |
| CUB oficial de RJ, PE e CE | Máximo oficial do m² | Sites dos Sinduscons fora do ar ou sem o valor |
| ViaCEP / BrasilAPI | — | **Não usar:** o CEP da base é fictício e não é fonte do governo |

Próxima: [[05 - Saídas - planilhas, ficha, API e demo]]
