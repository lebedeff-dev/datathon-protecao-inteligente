# Proteção Inteligente · Seguro Residencial

Projeto para o **Datathon Proteção Inteligente** (IBMEC + BB Seguros / Brasilseg).

## Equipe
- **Nome da equipe:** _(preencher)_
- **Integrantes:** _(preencher com nome completo de cada um)_
- **Desafio:** Seguro Residencial
- **Instituição / turma:** _(preencher)_

## Objetivo
Responder, para cada cliente e imóvel, "quanto proteger esta casa e com qual plano?" usando só o que o banco já sabe: é elegível? qual plano? quais coberturas e com que faixa de valor? o que foi observado, o que foi estimado e o que precisa ser confirmado? por que esse plano e não outro?

A solução é um **motor de regras explicável**, sem machine learning. Cada decisão tem uma regra escrita, uma fonte e um teste. A mesma saída (a "ficha" do caso) alimenta as duas planilhas, o app do cliente (1 toque), o painel do gerente e uma API para agentes.

## Como rodar
Python 3.11 (registrado em `.python-version`).

```bash
pip install -r requirements.txt
python -m pytest -q                 # 105 testes
python motor/gerar.py --entrega     # gera, valida e copia as planilhas para entrega/
```

- **Demo:** abra `prototipos/indexprototipo_gerente.html` com dois cliques. Os botões A, B e C mostram os perfis do slide 14 com a ficha real do motor.
- **API (opcional):** `pip install -r requirements-api.txt` e `uvicorn api:app --app-dir motor --port 8000`. Documentação em `/docs`.
- Os testes também rodam sozinhos no GitHub a cada envio (`.github/workflows/testes.yml`).

## Arquitetura

```
dados/desenvolvimento ──► calibrar()  (R$ de IPTU e de energia por m², por município)
                                │
dados/teste_comum ──► processar_caso() para cada cliente-imóvel
   1. inferir tipo, vínculo, uso, área e bens  → cada dado com natureza, fonte e confiança
   2. elegibilidade (guia 9.1)                 → SIM / NAO / SIM + pergunta
   3. plano por pontos de sinais               → Essencial, Prático ou Total (+ adicionais)
   4. faixa mín/máx de cada cobertura          → SINAPI, CUB, IPCA, FipeZAP, condições gerais
   5. até 3 perguntas, pelo valor da informação
   6. confiança por regra + jornada (1 toque, app com perguntas, gerente só em último caso)
   7. motivo para o cliente: fato dele, valor em risco, o que fica descoberto (motor/motivo.py)
                                │
                     ficha (JSON) ──► 2 planilhas · métricas · demo · API
```

| Arquivo | O que faz |
|---|---|
| `motor/motor.py` | Toda a lógica: inferências, elegibilidade, plano, coberturas, perguntas, confiança, planilhas |
| `motor/parametros.py` | Todas as premissas numéricas, com a origem escrita ao lado |
| `motor/metricas.py` | Métricas do guia §8 e casos contrastantes |
| `motor/templates.py` | Valida as planilhas contra as regras do guia antes de gravar |
| `motor/gerar.py` | Roda tudo de ponta a ponta |
| `motor/api.py` | API de demonstração (ficha e recálculo com as respostas do cliente) |
| `motor/externos/` | Fontes externas salvas + `FONTES.md` (fonte, data, licença, método, limitações) |
| `entrega/` | As 2 planilhas, `metricas.json` e `casos_contrastantes.json` |
| `tests/` | Testes automáticos |
| `documentos/contexto/` | Um documento curto por etapa (comece pelo `00-mapa.md`) |

## Premissas principais
- **Faixa = importância segurada** (quanto segurar), não valor de sinistro.
- **Casa:** reconstrução = área × custo do m² (mínimo SINAPI/IBGE, máximo CUB oficial) × padrão construtivo. Terreno não entra.
- **Apartamento, casa em condomínio ou financiado:** segundo risco (CG cl. 15.2). A estrutura tem seguro próprio; segura-se 25% a 40% (acabamentos) + bens.
- **Bens:** compras de 36 meses e bens vinculados, corrigidos pelo IPCA (Banco Central), até 2,7 × as compras (estoque). Sem compras nem bens ligados ao imóvel: média da região combinada com a renda (média geométrica; erro mediano fora da amostra de 40,5% só com a região para 22,7%).
- **Área sem cadastro (67% dos casos):** estimada pelo IPTU e pela energia, comparados aos imóveis do mesmo município com área conhecida. A renda não ajuda aqui (correlação 0,01 com a área).
- **Padrão construtivo vazio:** faixa do econômico ao superior (0,85 a 1,30) e pergunta do acabamento.
- **Plano:** pontos por sinal (aluguel, vizinhos, bens, eletrônicos, vidros, dependentes e pet, só como necessidade de RC). Tabela completa em `documentos/contexto/17-revisao-qa.md`.
- **Idade não entra em nenhuma decisão** (guia: "não utilize dados sensíveis ou atributos pessoais como atalho para risco ou patrimônio"). Dependentes e pet só como necessidade de RC familiar, nunca em valor, risco, canal ou confiança.
- **Renda:** na mentoria de 28/10, o Banco do Brasil confirmou que renda não é dado sensível (a LGPD, art. 5º, II, também não a lista). Ela entra num ponto só: os bens de quem não tem compras nem bens ligados ao imóvel, sempre combinada com a média da região, e o cliente lê no motivo que a renda foi usada. Quem tem compras segue pelas compras. Elegibilidade, canal e confiança não usam renda. Desligável em `parametros.RENDA_NOS_BENS_SEM_COMPRAS`.

## Elegibilidade (guia 9.1)
| Regra | Como o motor trata |
|---|---|
| Situação cadastral tombado, desapropriado ou condenado | `NAO` |
| Endereço que já tem seguro BB | Um imóvel só → `NAO`. Dois imóveis → `SIM` + "qual já tem seguro?" |
| Construção ou reforma | Gasto alto com material de construção → `SIM` + pergunta (o gasto sugere, mas não prova) |
| Parede de material combustível | `SIM` + pergunta sobre madeira pré-fabricada ABNT |
| Comunidade, favela, atividade rural, MEI fora da lista | A base não tem esses dados: confirmação na contratação (ver limitações) |

## Limitações
- Não há sinistros nem rótulos na base, então não há acurácia a medir. A qualidade é mostrada por testes de coerência, estabilidade, justiça e sensibilidade.
- Favela/comunidade, atividade rural e MEI não aparecem nos dados. Precisam de declaração do cliente na contratação.
- O CUB de RJ, PE e CE não foi conferido em fonte oficial. Nessas UFs o máximo é SINAPI × razão CUB/SINAPI das 7 UFs oficiais (≈ 1,14).
- Custos e aluguel são médias do estado ou da capital, não do bairro.
- O catálogo do datathon não tem "instalações e pequenos reparos", que o guia lista no Essencial. Seguimos o catálogo, que é a nomenclatura de conferência.
- Os valores de vendaval, danos por água, RC e despesas emergenciais são proporções premissa do time (em `parametros.py` e `motor.dimensionar()`), sem dado de sinistro para calibrar.
- A base não traz risco de território. Usamos registros oficiais da Defesa Civil (Atlas/S2iD) e o ranking de energia da ANEEL por município, só no texto do motivo; o risco de furto segue sem fonte.

## Métricas (base comum, 138 casos)
| Métrica | Resultado |
|---|---|
| Casos processados / com justificativa / coberturas fixas completas | 100% · 100% · 100% |
| Falhas na execução | 0 |
| Planos | Prático 68 · Total 38 · Essencial 32 (dependentes e pet não mudam o plano) |
| Coberturas adicionais | 52 (RC familiar em prédio ou condomínio com dependentes ou pet; em casa, vira pergunta) |
| Elegibilidade | SIM 138 · NÃO só com prova (situação cadastral irregular; nenhum na base) · 37 com confirmação pendente, 16 deles "provável seguro BB" (o app pergunta; RN-19) |
| Confiança | ALTA 17 · MÉDIA 101 · BAIXA 20 (14%) |
| Jornada | 1 toque 63 (nenhuma pergunta obrigatória) · app com perguntas 49 (elegibilidade, uso duvidoso, confiança baixa, modo simples) · gerente 26 (19%: obra 10, sem app 16) |
| Qualidade do motivo | 0 motivos genéricos · 100% com fato do próprio cliente e valor em risco · 0 termos internos · mediana de 100 palavras |
| Perguntas por caso | 2,78 (0,46 obrigatória; as demais só ajustam o valor e vêm marcadas "(opcional)"); 80 casos sem pergunta que trave |
| Teste de justiça (troca renda e idade) | 0 casos mudam (todos os 138 têm compras ou bens; a renda só entra sem eles) |
| Bens sem compras: só região × região + renda (fora da amostra, 2.578 imóveis) | erro mediano 40,5% → 22,7% |
| Dependentes e pet mudando plano, valor ou confiança | 0 casos (só pedem a RC familiar como adicional ou pergunta) |
| Estabilidade do plano (valores ±5%) | 1 caso muda (perto do limiar de eletrônicos) |
| Estabilidade da confiança (pesos ±20%) | 0 casos mudam |
| Faixa de incêndio por confiança (máx ÷ mín) | ALTA 1,89 · MÉDIA 2,33 · BAIXA 2,56 |
| Sensibilidade (área +10%) | incêndio +4,6% em média, 0 quedas |
| Regra dos 80% na elegibilidade por faixa de renda | 1,00 |
| Reprodutibilidade | duas rodadas geram arquivos idênticos |
| Tempo | ~0,5 s para os 138 casos |

### Métricas de mercado e validação
| Métrica | Resultado | Como |
|---|---|---|
| 1 toque puro · sem pessoa no meio | 45,7% · 81,2% dos elegíveis | Sem pergunta obrigatória · 1 toque + app com perguntas de sim/não |
| Esforço | 2,7 perguntas × 19,9 campos de uma cotação tradicional (86,4% menos) | 5 dados do imóvel + 6 declarações de elegibilidade + 1 valor por cobertura |
| Aderência aos sinistros reais | 100% das recomendações têm danos elétricos, água e vendaval, que somam 79,4% dos acionamentos do residencial BB | `motor/externos/sinistros_residencial_bb.csv` |
| ITV do incêndio (segurado ÷ valor em risco) | máximo 1,48 · mínimo 0,62 · sugerido ÷ cenário pessimista 0,67 | O valor sugerido evita o mínimo; contra o pior cenário ele cobre 67% (medida sem circularidade) |
| Backtest fora da amostra: área | erro mediano 15%; a faixa contém a área real em 78% (meta 80%) | Calibra em metade da base de desenvolvimento, mede na outra |
| Backtest fora da amostra: padrão pelo IPTU/m² | intervalo certo em 97,8% dos 180 estreitados | Mesmo método |

Tudo em `entrega/metricas.json`.

**Reprodutibilidade:** as planilhas entregues usam os dados externos salvos no repositório (SINAPI set/2026, IPCA até set/2026). Rodar `python motor/externos/coletar.py --ao-vivo` renova essas fontes pelas APIs e, de propósito, muda as faixas; sem o coletor, duas gerações dão arquivos idênticos.

## Resultados: casos contrastantes (slide 14)
| Perfil | Caso | Plano | Por quê |
|---|---|---|---|
| A · Apartamento urbano | `IMO_CASO_00004_01` | Prático + RC | Bens e eletrônicos comprovados altos; dependentes ou pet → RC adicional |
| B · Casa familiar | `IMO_CASO_00001_01` | Prático + RC | Casa em condomínio com bens e eletrônicos altos; a família pede a RC familiar como adicional, sem mudar o plano |
| C · Imóvel de lazer | `IMO_CASO_00010_01` | Essencial + RC | Apartamento de veraneio que fica vazio: o roubo do Prático não cobre residência desocupada |
| Já segurado? | `IMO_CASO_00014_01` | Prático + RC | Provável seguro BB no endereço: vira pergunta obrigatória ("O seu seguro atual é da BB?"); se sim, não há nova proposta |

## Fontes externas
SINAPI (IBGE, pela API SIDRA, set/2026), CUB oficial (Sinduscons de SP, DF, GO, BA, MG, RS e PR), IPCA (Banco Central, API SGS 433; `coletar.py --ao-vivo` renova os dois), FipeZAP Locação (Fipe), acionamentos do Seguro Residencial BB jan/2023–mai/2026, Atlas Digital de Desastres / S2iD (Sedec/MIDR, 1991–2025) e Ranking de Continuidade 2025 da ANEEL (os três só no texto do motivo) e Condições Gerais BB Seguro Residencial v1.4. Detalhes, licença e limitações em `motor/externos/FONTES.md`.

## Privacidade e responsabilidade
- Só dados do pacote e fontes públicas. Os dados do pacote são fictícios.
- Minimização: idade e origem da renda não são lidas por nenhuma regra (teste automático). A renda é lida num ponto só (bens sem compras), ligado por um parâmetro, e o texto do cliente avisa quando ela foi usada.
- Controle humano: toda estimativa vira pergunta ou vai para o gerente; nada é contratado sem confirmação.
- Nenhuma credencial ou dado restrito no repositório.

## Uso de IA
Usamos assistentes de IA como apoio para revisar código, pesquisar fontes públicas e revisar textos. As regras, os parâmetros e os resultados foram decididos, executados e conferidos pela equipe, que entende e defende a solução.

## Relato
Caminhos testados e descartados estão em `documentos/contexto/` (seção "Decisões e o que descartamos" de cada etapa). Exemplos: confiança por corte numa nota (descartada por instabilidade), qualquer criança ou pet levando ao Total (inflava o Total para 65%), CUB de agregador (fonte não oficial).
