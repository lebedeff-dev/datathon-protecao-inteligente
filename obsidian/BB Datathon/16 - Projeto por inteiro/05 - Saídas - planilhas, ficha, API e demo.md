---
tags: [projeto, saidas, planilhas, api]
atualizado: 2026-10-28
---
# 📤 05 · Saídas: planilhas, ficha, API e demo

Tudo nasce da mesma **ficha** (um JSON por cliente-imóvel). A planilha, o app, o gerente e a API leem a ficha; ninguém recalcula nada por fora.

## 1. Planilha 1: `entrega/template_resultado_times.csv` (138 linhas)
| Coluna | De onde vem | Exemplo |
|---|---|---|
| `cliente_id`, `imovel_id` | Do template, na mesma ordem | IMO_CASO_00005_01 |
| `elegivel` | Passo 2 | SIM |
| `motivo_inelegibilidade` | Só quando NÃO | provável seguro BB neste endereço... |
| `tipo_imovel_sugerido` · `uso_imovel_sugerido` · `tipo_vinculo_sugerido` | Passo 1 | APARTAMENTO · RESIDENCIAL_HABITUAL · FINANCIADO |
| `plano_recomendado` | Passo 3 | PRATICO |
| `coberturas_recomendadas` | Fixas do plano + adicionais, separadas por ";" | ... |
| `confianca_geral` | Passo 6 | ALTA |
| `justificativa_recomendacao` | **O motivo** (`motivo.py`) | "Recomendamos o plano Prático porque você gastou R$ 11 mil com vidraçaria..." |
| `perguntas_confirmacao` | Passo 5, separadas por " \| ", opcionais com "(opcional)" | "(opcional) Seus móveis... ficam entre R$ 22 mil e R$ 60 mil?" |
| `fontes_publicas_adicionais` | Fontes usadas no caso, com data | SINAPI 2026-09 (IBGE); ... |

## 2. Planilha 2: `entrega/template_coberturas_times.csv` (1.232 linhas)
Uma linha por cobertura fixa + adicional:

| Coluna | De onde vem |
|---|---|
| `cobertura` | Nome do catálogo (assistências não entram, RN-24) |
| `faixa_valor_min` · `faixa_valor_max` | Passo 4, só números (RN-31) |
| `confianca_estimativa` | Confiança da cobertura (passo 6) |
| `dados_utilizados` · `regra_calculo_utilizada` | Os dados e a conta (ex.: "área 110 m² × R$ 2.287–2.739/m² × 25%–40% + bens") |
| `justificativa` | Texto com os números do cliente + dado da cidade |
| `informacao_a_confirmar` | O que o cliente pode confirmar |
| `observacao` | Cláusula das CG, subseguro, beneficiários (RN-27) |

**Antes de gravar**, `templates.validar_templates` confere as colunas e a ordem, os campos obrigatórios, o SIM/NÃO, o motivo de cada NÃO, os nomes do catálogo, os valores inteiros e não negativos, a confiança válida, as linhas repetidas, as fixas do plano e a **RN-33** (lista da planilha 1 = linhas da planilha 2). Com erro, `gerar.py` sai com código 1 e não copia para `entrega/`.

## 3. A ficha (JSON)
| Campo | O que tem |
|---|---|
| `campos` | tipo, vínculo, uso, área e bens, cada um com valor, natureza, confiança, fonte, idade e classe |
| `valor_imovel` | custo do m², fator e origem do padrão, reconstrução, segundo risco |
| `elegibilidade` · `pendencias` · `avisos` | Passo 2 |
| `plano` · `motivos` · `motivos_plano` · `pontos` · `alternativa` · `adicionais` | Passo 3 |
| `coberturas` | Cada uma com mín, máx, **sugerido**, confiança, regra, justificativa, observação, limitada pelo produto |
| `perguntas` | Texto, código, prioridade, **obrigatória**, quanto aperta a faixa |
| `confianca` · `confianca_score` · `confianca_motivo` · `completude` | Passo 6 |
| `jornada` · `motivo_jornada` · `canal` | Passo 7 |
| `fontes` | Fontes usadas, com data |

## 4. Outras saídas
| Saída | O que é |
|---|---|
| `entrega/metricas.json` | Todas as métricas ([[03 - Cada métrica explicada]]) |
| `entrega/casos_contrastantes.json` | Casos da demo: perfis A, B e C do slide 14 (00005, 00031, 00010), não elegível (00014), 1 toque limpo, inquilino no Total, elegibilidade a confirmar |
| `prototipos/fichas_demo.js` | As fichas desses casos para o protótipo abrir sem servidor |
| **API** (`motor/api.py`) | `GET /fichas/{id}` · `POST /recomendar` (recalcula com as respostas: bens "menos/isso/mais", área) · `GET /fontes` (data de cada fonte) · `GET /saude` |

Rodar a API: `pip install -r requirements-api.txt` e `uvicorn api:app --app-dir motor`.

Próxima: [[06 - Testes e qualidade]]
