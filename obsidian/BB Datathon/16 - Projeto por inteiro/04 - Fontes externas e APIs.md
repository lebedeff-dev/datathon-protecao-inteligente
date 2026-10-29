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
| **Atlas de Desastres / S2iD** (MIDR) | `desastres_municipio.csv` | Chuvas e vendavais na cidade (só texto) | Arquivo oficial (sem API); `coletar.py --atlas` | 1991–2025 | A frase some |
| **ANEEL** | `aneel_continuidade.csv` | Quedas de energia da distribuidora (só texto) | Ranking oficial | 2025 | A frase some |
| **Condições Gerais BB v1.4** | (regras no código) | Segundo risco, limite único, bens não cobertos | PDF lido | v1.4 | — |

> [!info] Retirado em 29/10: os sinistros da BB
> O dado de acionamentos do Seguro Residencial BB ("danos elétricos são 53,3% dos acionamentos") vinha de uma **matéria de imprensa**, sem API nem relatório oficial. Não tinha como a banca auditar. Ele só aparecia no texto, então tirá-lo não mudou nenhum plano nem faixa.

## O motor sem internet e sem os arquivos externos (testado em 29/10)
**O motor nunca acessa a internet.** Só o `coletar.py --ao-vivo` busca as APIs, e ele **salva** o resultado em CSV. O motor só lê os CSVs. Rodamos o motor com a rede bloqueada no próprio Python: 138 casos, 0 erros.

E se os arquivos sumirem? Rodamos sem **nenhum** arquivo externo:
| O que | Igual? | Por quê |
|---|---|---|
| Elegibilidade, jornada, nível de confiança, pendências, adicionais | **138 de 138** | Nenhuma decisão usa fonte externa |
| Plano | **137 de 138** | Sem o IPCA, um cliente tem R$ 9.450 em eletrônicos em vez de R$ 10.106 e fica abaixo do limite de R$ 10 mil. Ele já estava marcado "no limite", com a pergunta que decide |
| Faixa do incêndio | mudou em 122, mas pouco: o meio da faixa muda **0% na mediana** (de −10,5% a +8,9%) | Sem SINAPI e CUB, o custo do m² vira o neutro (R$ 2.100 a R$ 2.500), perto dos valores reais (R$ 1.888 a R$ 2.944) |
| Confiança das coberturas | cai para **baixa** | O motor avisa que está sem o custo oficial |
| Motivo | perde as frases da ANEEL e da Defesa Civil | Elas só existem com o dado |

**Leitura:** dependemos de um **custo de construção** para dizer quanto vale reconstruir uma casa, porque a base não traz esse dado. Isso é dependência do **dado**, não da internet: o dado está salvo no repositório com data e fonte. Sem ele, o motor ainda entrega as 138 respostas, com valores próximos e confiança baixa (RN-12).

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
