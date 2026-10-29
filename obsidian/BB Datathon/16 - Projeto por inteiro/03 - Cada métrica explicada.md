---
tags: [projeto, metricas]
atualizado: 2026-10-28
---
# 📊 03 · Cada métrica explicada

Todas saem de `motor/metricas.py` para `entrega/metricas.json` a cada `python motor/gerar.py --entrega`. Valores da base Teste Comum (138 casos).

## 1. As que a banca pediu (guia §8)
| Métrica (`metricas.json`) | Valor | Como é calculada | Por que importa |
|---|---|---|---|
| `casos_processados` · `processados_pct` | 138 · 100% | Imóveis do template que ganharam ficha | Nenhum caso esquecido |
| `com_justificativa_pct` | 100% | Linhas com motivo preenchido | O motivo é o principal (mentoria) |
| `completude_coberturas_fixas_pct` | 100% | Casos com todas as coberturas fixas do plano | RN-21, RN-22 |
| `linhas_de_cobertura` · `faixas_vazias` · `faixas_invertidas` | 1.232 · 0 · 0 | Linhas da planilha 2; faixas sem valor; mínimo maior que o máximo | RN-30, RN-32 |
| `planos` | Prático 66 · Total 38 · Essencial 34 | Contagem | Distribuição coerente (nem todo mundo no Total) |
| `elegibilidade` · `elegibilidade_por_regra` | SIM 138 · seguro existente 30 (16 "provável BB", com pergunta) · reforma 10 | Cada regra do guia 9.1 e quantos casos pegou | Elegibilidade antes de recomendar |
| `casos_com_confirmacao_de_elegibilidade` | 37 | Casos com pendência que vira pergunta | Sinal fraco vira pergunta, não recusa |
| `coberturas_adicionais` | RC familiar 93 | Adicionais fora do plano (todo prédio ou família abaixo do Total) | Slide 23: plano + **adicionais** |
| `perguntas_media` · `perguntas_candidatas_media` | 2,75 · 3,5 | Perguntas feitas e possíveis | Poucas e priorizadas (RN-36) |
| `perguntas_obrigatorias_media` · `casos_sem_pergunta_obrigatoria` | 0,34 · 94 | Perguntas que travam a contratação | Quanto dá para contratar direto |
| `confianca` · `confianca_baixa_pct` | alta 17 · média 101 · baixa 20 (14,5%) | Nível por regra | O guia pede o % de confiança baixa |
| `confianca_por_cobertura` | ex.: danos elétricos ALTA 69 · MÉDIA 69 | O pior dos dados que a cobertura usa | A coluna de confiança da planilha 2 informa algo |
| `estabilidade_plano_casos_que_mudam_com_valores_5pct` | 1 | Muda compras, bens, IPTU e energia em ±5% | Estabilidade (o caso que muda está no limiar) |
| `confianca_estabilidade_casos_que_mudam_com_pesos_20pct` | 0 | Muda os pesos das fontes em ±20% | O nível não depende de um número mágico |
| `confianca_largura_incendio_mediana` | alta 1,89 · média 2,33 · baixa 2,56 | Máximo ÷ mínimo do incêndio por nível | Menos confiança = faixa mais larga (honesto) |
| `sensibilidade_area_10pct_incendio_media_pct` · `..._casos_com_queda` | +4,65% · 0 | Área 10% maior: quanto sobe o incêndio | Coerência: área maior nunca reduz |
| `casos_com_falha` · `tempo_segundos` | 0 · ~1 s | Falhas e tempo dos 138 casos | Viabilidade |

| `necessidades` | aluguel 38 · roubo 84 · terceiros 126 | Quantos clientes têm cada necessidade (a base do plano) | A recomendação se explica pelas necessidades |
| `forca_da_recomendacao` | clara 124 · no limite 14 | Recomendações decididas com folga × por menos de 15% do limite | Dizer quando a decisão foi por pouco |
| `instaveis_marcados_no_limite_pct` | 100% | Dos casos que mudam de plano com ±5% nos valores, quantos estão marcados "no limite" | A instabilidade está avisada, não escondida |

## 2. Responsabilidade (justiça)
| Métrica | Valor | Como | Por que |
|---|---|---|---|
| `teste_justica_casos_alterados` | **0** | Troca renda e idade de todos e roda de novo; nada muda | Renda e idade não decidem |
| `teste_justica_casos_sem_compras_so_decisoes` | 0 | Nos casos sem compras (a renda entra nos bens), confere que plano, elegibilidade, jornada e confiança não mudam | D-08 |
| `justica_por_quinto_de_renda` | razão de elegibilidade 0,85 | % elegível por quinto de renda; menor ÷ maior ≥ 0,8 (regra dos 80% do crédito) | Sem impacto desigual |
| `familia_declarada_muda_plano` · `..._muda_valor_ou_confianca` | 18 · 0 | Troca dependentes e pet | Família pesa só no plano, pela RC (decisão aberta) |

## 3. O motivo (o que a mentoria disse que diferencia)
| Métrica (`qualidade_do_motivo`) | Valor | O que é |
|---|---|---|
| `motivos_genericos` | **0** | Ninguém recebe "não há sinais" |
| `motivo_com_fato_do_cliente_pct` | **100%** | O motivo traz um número do próprio cliente |
| `justificativa_com_valor_em_risco_pct` | **100%** | Diz quanto ele perderia |
| `alternativas_mostradas_pct` | **100%** | Mostra a opção mais barata e a mais completa (RN-37) |
| `justificativas_com_termo_interno` | **0** | Sem "presumido", "estimado:"... |
| `palavras_mediana` · `palavras_max` · `palavras_entre_60_e_120_pct` | 100 · 130 · 92% | Tamanho de leitura (RN-51) |
| `coberturas_texto_distinto_pct` | incêndio 100% · danos elétricos 98% | Texto personalizado por cliente |

## 4. Jornada
| Métrica | Valor | O que é |
|---|---|---|
| `jornada` | 1 toque 63 · app com perguntas 49 · gerente 26 | Para onde cada caso vai |
| `gerente_pct_dos_elegiveis` · `gerente_motivos` | 18% · obra 9 · sem app 13 | Gerente só em último caso |
| `canal` | 1 toque 100 · gerente 38 | O campo que o protótipo lê |

## 5. Mercado (`mercado`) — ver [[Métricas do mercado x as nossas]]
| Métrica | Valor | O que é |
|---|---|---|
| `um_toque_pct_dos_elegiveis` · `sem_pessoa_pct_dos_elegiveis` | 45,7% · 81,2% | 1 toque puro (sem pergunta obrigatória) e contratação sem pessoa no meio (inclui o app com perguntas). Antes, um único 72,5% sobre os 138 misturava os dois |
| `esforco_*` | 2,77 perguntas × 19,9 campos (86% menos) | Esforço contra uma cotação comum (5 dados + 6 declarações + 1 valor por cobertura) |
| `itv_incendio_no_maximo` · `no_minimo` · `itv_sugerido_sobre_pessimista` | 1,48 · 0,62 · **0,67** | Segurado ÷ valor em risco (abaixo de 0,8 = subseguro). O sugerido é comparado ao **cenário pessimista** (sem circularidade): cobre 67% do pior caso; 15 casos chegam a 80% |
| `faixas_limitadas_pelo_produto` | água 134 · danos elétricos 122 | Estimativa acima do limite (limites de água e elétricos são premissa) |
| `recomendacoes_com_coberturas_mais_acionadas_pct` | 100% (79,4% dos acionamentos da BB) | Todas têm as coberturas que mais dão sinistro na BB |

## 6. Validação fora da amostra (`backtest_fora_da_amostra` e `dados_faltantes`)
| Métrica | Valor | O que é |
|---|---|---|
| `area_erro_mediano_pct` · `area_mape_pct` | 15% · 18,7% | Erro da área estimada contra a cadastrada |
| `area_dentro_da_faixa_pct` | 80,9% | A faixa contém a área real (meta: 80%) |
| `padrao_intervalo_correto_pct` | 97,8% (180 estreitados) | Padrão pelo IPTU/m² acerta |
| `backtest_bens_sem_compras` | região 40,5% → região + renda 22,7% | Erro das compras estimadas |
| `teste_cep_da_base` | 0,215 contra 0,223 sorteado | O CEP é ruído (RN-10) |
| `dados_faltantes` | área: 46 cadastradas · 92 pelo IPTU e energia · padrão: 40 · 25 pelo IPTU · 73 com pergunta | Como cada lacuna foi tratada |

Próxima: [[04 - Fontes externas e APIs]]
