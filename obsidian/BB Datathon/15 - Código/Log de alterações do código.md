---
tags: [codigo, log, git]
atualizado: 2026-10-29
---
# 📝 Log de alterações do código

Toda mudança no motor, do mais novo para o mais antigo. Repositório: [pedroiaan/datathon-protecao-inteligente](https://github.com/pedroiaan/datathon-protecao-inteligente) · histórico completo: `git log --oneline`.

> [!info] Como registrar
> A cada commit que mexe em `motor/`, `tests/` ou `entrega/`, acrescente uma linha aqui: **o que mudou, por quê e qual regra atende**. Os detalhes ficam no commit e na nota da etapa em `documentos/contexto/`.

## 29/10 · madrugada: sinistros BB fora · assertividade e motivo feito para você
| Onde | O que mudou | Por quê |
|---|---|---|
| `parametros.py` · `motor.py` · `motivo.py` · `metricas.py` | **Sinistros da BB retirados** (arquivo, função, frase das coberturas, frase do Essencial e a métrica de aderência) | Fonte secundária (imprensa), sem como auditar (RN-11); não mudava plano nem faixa |
| `assertividade.py` (novo) | Acerto de cada cálculo de dado faltante em 5 dobras, contra o chute | Saber e mostrar quanto cada conta acerta (RN-35, RN-47) |
| `motor.py` · `_area_estimada` · `valor_imovel` | Área pela média geométrica; faixa calibrada de área × padrão nos 64 casos sem os dois | Erro 15,0% → 14,1%; faixa 2,7× → 1,76× contendo o real em 88% |
| `motivo.py` · `justificativa` | Motivo feito para você: casa e cidade, fato dos vizinhos, risco da cidade, lacuna em reais, confiança com o acerto | O motivo é o diferencial (RN-49) |
| `motor.py` · `montar_perguntas` | Perguntas dizem o porquê em reais | O cliente entende por que responder |

## 28/10 · noite: pós-mentoria ([[Plano - motivo, dados faltantes e gerente]])
| Arquivo | O que mudou | Por quê |
|---|---|---|
| `motivo.py` (novo) | Todo texto ao cliente: fato dele → valor em risco → o que fica descoberto (frase do slide 23) → opção acima → o que confirmar → confiança em linguagem simples. `reais()` arredonda como gente fala | Mentoria: o porquê é o que diferencia; RN-09, RN-37, RN-53 |
| `motor.py` · `escolher_plano` | Motivos com número do cliente; o Essencial genérico ("não há sinais") virou patrimônio + aparelhos (danos elétricos = 53% dos acionamentos da BB) | 29 casos tinham motivo vazio |
| `motor.py` · `dimensionar` | Justificativa de cada cobertura com os valores do cliente (antes, o mesmo texto para os 138) | Personalização |
| `motor.py` · `_degraus`, `regional`, `teste_cep` | Média da região em degraus (município + tipo → município → estado → geral, mínimo de 20 imóveis); CEP desligado porque é ruído (R² 0,215 contra 0,223 embaralhado) | Mentoria (média regional) + RN-10 |
| `motor.py` · `escolher_jornada` | UM_TOQUE · APP_COM_PERGUNTAS · GERENTE (só confiança baixa, obra ou sem app) · SEM_NOVA_PROPOSTA. O `canal` continua 1 toque × gerente para o protótipo | Mentoria: gerente é o último recurso (71 → 35) |
| `externos/coletar.py --ao-vivo` | SINAPI pela API SIDRA do IBGE (tabelas 6586 e 2296) e IPCA pela API do BC; valida antes de gravar; se falhar, mantém o salvo | Dado sempre atualizado sem depender da internet para rodar (RN-12) |
| `metricas.py` | `qualidade_do_motivo`, `dados_faltantes`, `jornada` e `gerente_motivos` | Medir o que a banca vai olhar |
| `api.py` | Rota `/fontes` com a data de cada fonte | Transparência |
| `tests/` | +18 testes (82 no total) | Cada regra com prova |

## 28/10 · noite: fontes territoriais ([[Atlas Digital de Desastres]], [[ANEEL continuidade]])
| Arquivo | O que mudou | Por quê |
|---|---|---|
| `externos/desastres_municipio.csv` | Registros de água e vento por capital (Atlas/S2iD 1991–2025) | Motivo de danos por água e vendaval com dado oficial |
| `externos/aneel_continuidade.csv` | Posição da distribuidora no ranking da ANEEL 2025 | Motivo de danos elétricos |
| `externos/cub_uf.csv` | CUB oficial de MG, RS e PR (7 de 10 UFs) | Issue #11; a razão CUB/SINAPI passou de 1,09 para 1,14 |
| `externos/coletar.py` | `--atlas` resume a base do Atlas (reprodutível) | RN-11 |
| `parametros.py` | `desastres()`, `continuidade_energia()` | Leitura que devolve `None` sem o arquivo |
| `motor.py` · `contexto_territorio` | Frase com o dado do município na justificativa; zero registros não gera frase | RN-12, RN-49 |
| `tests/` | +3 testes (64 no total) | Motor igual sem os arquivos |

## 28/10 · noite: auditoria do código ([[Auditoria do código - 28-10]])
| Arquivo | O que mudou | Por quê |
|---|---|---|
| `motor.py` · `_area_estimada` | Usa só os sinais que existem (IPTU ou energia zerados não encolhem a área) | RN-14, valores extremos |
| `motor.py` · `calibrar`, `_calibrar_area`, `backtest` | Calibração separada + **backtest fora da amostra** (área e padrão) | Validação de modelo, RN-47 |
| `motor.py` · `iptu_relativo`, `valor_imovel` | Padrão vazio + área cadastrada → IPTU/m² estreita o fator do padrão | Precisão das faixas, RN-08 |
| `motor.py` · `dimensionar` | Aviso de **subseguro** quando a estimativa passa do limite; RN-27 para o locador; despesas emergenciais sobre a faixa de incêndio já limitada; motivo cita os **sinistros reais da BB** | D-07, RN-27, RN-49 |
| `motor.py` · `valor_da_informacao`, `montar_perguntas` | A pergunta não promete mais que a faixa entregue; corta as que mudam menos de R$ 5 mil | RN-36, RN-51 |
| `parametros.py` | `fator_padrao_pelo_iptu`, `sinistros_pct`, `VALOR_MINIMO_PERGUNTA` | Premissas com origem |
| `externos/sinistros_residencial_bb.csv` + `FONTES.md` | Mix de acionamentos do residencial BB (jan/2023–mai/2026) | Dado real da própria BB, só no texto |
| `metricas.py` | `processados_pct` calculado de verdade; `metricas_de_mercado` (STP, esforço, ITV, faixas no limite, aderência aos sinistros); backtest | Guia §8 + mercado |
| `templates.py` | Confere RN-33, confiança válida, linhas repetidas e valores negativos | RN-33 |
| `api.py` | Área 0, negativa ou acima de 10.000 m² é recusada | Robustez da API |
| `tests/` | +10 testes (61 no total) | Cada correção com prova |

## 28/10 · tarde
| Hora | Quem | Commit | O que mudou |
|---|---|---|---|
| 15:20 | Pedro | `5bac480` | Seguro BB só com produto de seguridade; frescor de volta na confiança; "dependentes" em vez de "crianças" |
| 15:13 | Pedro | `3830400` | Merge do PR #13 (revisão QA + vault) |
| 15:07 | Matheus | `3ee7095` | Vault do Obsidian no repositório |
| 14:09 | Matheus | `03c4e67` | Veraneio não puxa o Prático; RC familiar como adicional; métricas de estabilidade, falhas e elegibilidade |
| 13:59 | Matheus | `9404798` | Faixa aberta sem padrão construtivo; perguntas pelo valor da informação; justiça por quinto de renda |
| 13:53 | Matheus | `66e3326` | Perfis do slide 14; confiança por regra; CUB só oficial |

## 28/10 · madrugada (primeira versão)
| Hora | Commit | Tarefa |
|---|---|---|
| 00:59 | `69378a9` | T9 · API de demonstração |
| 00:57 | `53eeeca` | T7 · protótipo do gerente lê as fichas do motor |
| 00:53 | `2a0311d` | T5, T6 · confiança, justiça, métricas, casos contrastantes |
| 00:50 | `d6e3c77` | T4 · validação das planilhas |
| 00:49 | `33fb8ea` | T3 · elegibilidade, plano e coberturas |
| 00:44 | `ab211aa` | T2 · bens pelas três âncoras com IPCA |
| 00:42 | `f87a8a0` | T1 · parâmetros com fontes oficiais |
| 00:39 | `752993d` | Estrutura inicial |

Ligações: [[Mapa do código]] · [[Log de commits]] · [[Correções P1-P5 no motor]]
