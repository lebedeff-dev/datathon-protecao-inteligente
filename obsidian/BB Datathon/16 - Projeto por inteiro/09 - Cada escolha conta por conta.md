---
tags: [projeto, motor, exemplo, conta]
atualizado: 2026-10-29
---
# 🧮 09 · Cada escolha, conta por conta (dois casos reais)

Aqui o motor é seguido **passo a passo em dois clientes reais da base de teste**, com os números que entram, a regra aplicada e a conta que dá o resultado. O objetivo é poder conferir se cada escolha faz sentido. Os números saem do próprio código (versão de 29/10).

> [!tip] Como ler
> Cada passo tem: **o dado** (o que está na base) → **a regra** (o que o motor faz) → **a conta** → **o resultado**. Ao final de cada caso, o texto que o cliente lê.

---

# Caso 1 · `IMO_CASO_00005_01`, apartamento financiado em Curitiba (1 toque)

## 1. Que imóvel é esse?
| Escolha | Dado | Regra | Resultado |
|---|---|---|---|
| **Tipo** | Endereço com "apartamento"; complemento "BLOCO B APTO 305" | "Apartamento" no endereço → apartamento. O complemento traz APTO/BLOCO, então **confirma** | Apartamento, observado (alta) |
| **Vínculo** | Aluguel pago: não. Parcela de financiamento: R$ 950/mês | A ordem é aluguel → financiamento → recebe aluguel → proprietário. Há parcela | **Financiado**, observado (transação) |
| **Uso** | Endereço bate com o principal do cliente | Endereço principal → moradia | Moradia habitual, observado |
| **Área** | Área cadastrada: 110 m² (cadastro do IPTU) | Área cadastrada **sempre vence** a estimativa | 110 m², observado |

> [!info] Por que a área cadastrada vence
> Se o motor estimasse: IPTU R$ 1.800 ÷ R$ 13,75/m² (mediana de Curitiba) = 130,9 m²; luz R$ 500 ÷ R$ 3,60/m² = 138,9 m²; 0,6 × 130,9 + 0,4 × 138,9 = **134 m²**, 22% acima do real. Por isso a estimativa só entra quando falta o cadastro.

## 2. Quanto custa reconstruir?
| Escolha | Conta | Resultado |
|---|---|---|
| **Padrão** (vazio no cadastro) | IPTU por m² = R$ 1.800 ÷ 110 = R$ 16,36. Comparado ao de Curitiba: 16,36 ÷ 13,75 = **1,19**. Acima de 1,15 → descarta o econômico | Fator de 1,00 (normal) a 1,30 (superior) |
| **Custo do m²** | Mínimo: SINAPI do Paraná R$ 2.287,43 × 1,00. Máximo: CUB oficial do Paraná R$ 2.738,93 × 1,30 | R$ 2.287 a R$ 3.561 por m² |
| **Reconstrução** | 110 × 2.287 = R$ 251,6 mil · 110 × 3.561 = R$ 391,7 mil | R$ 252 mil a R$ 392 mil |
| **Segundo risco** | Apartamento: a estrutura tem o seguro do condomínio (CG cl. 15.2). O residencial cobre só os acabamentos, 25% a 40% | Acabamentos: R$ 62,9 mil a R$ 156,7 mil |

## 3. Quanto valem os bens?
| Escolha | Conta | Resultado |
|---|---|---|
| **Compras de 36 meses** | Eletrônicos 8.800 + eletrodomésticos 2.850 + móveis 9.100 | R$ 20.750 |
| **Bens ligados ao imóvel** | 3 bens, ponderados pela chance de estarem lá | R$ 2.500 |
| **Mínimo comprovado** | maior(20.750; 2.500) × 1,0694 (IPCA de 12 meses trazido ao meio da janela) | **R$ 22.190** |
| **Máximo de estoque** | 2,7 × 20.750 × 1,0694 (cerca de 8 anos de compras acumuladas) | **R$ 59.914** |
| **Confiança dos bens** | Há compras, mas nenhum bem com vínculo forte (0% do valor) | Média |
| Só eletrônicos (base do roubo) | 8.800 × 1,0694 → 2,7 × 8.800 × 1,0694 | R$ 9.411 a R$ 25.409 |
| Eletrônicos + eletrodomésticos (danos elétricos) | 11.650 × 1,0694 → 2,7 × 11.650 × 1,0694 | R$ 12.459 a R$ 33.639 |

## 4. Pode contratar?
Situação cadastral regular; material vazio (não pergunta, porque só pergunta quando o cadastro diz outro material); material de construção R$ 0 (abaixo de R$ 15 mil); sem seguro residencial. → **Elegível, sem pendência.**

## 5. Qual plano?
| Sinal | Tem? | Pontos |
|---|---|---|
| Paga aluguel | não | — |
| Recebe aluguel | não | — |
| Prédio ou condomínio | **sim** | Total +1 |
| Bens comprovados ≥ R$ 36 mil | não (R$ 22.190) | — |
| Eletrônicos comprovados ≥ R$ 10 mil | não (R$ 9.411, por pouco) | — |
| Casa fora de condomínio | não | — |
| Gasto com vidraçaria em 24 meses | **sim** (R$ 11.000) | Prático +1 |

**Regra:** Total exige 2 pontos de Total (tem 1). Prático exige 2 de Prático **ou** 1 de Prático + 1 de Total → tem (1 + 1). → **Prático.**
**Adicional:** 1 dependente + apartamento + plano abaixo do Total → **RC familiar** como adicional.
**Motivo do plano:** o sinal que deu o ponto ao Prático (vidraçaria).

## 6. As faixas
Cada faixa: a conta → os limites do produto → o arredondamento (de 500 em 500 até R$ 20 mil, de 1.000 em 1.000 acima).

| Cobertura | Conta | Limite | Faixa | Sugerido |
|---|---|---|---|---|
| Incêndio | 25% × 251,6 mil + 22,2 mil = 85,1 mil → 40% × 391,7 mil + 59,9 mil = 216,6 mil | mín. 100 mil | **R$ 100 mil – 217 mil** | 151 mil (meio da estimativa) |
| Danos por água | 50% × 22,2 mil + 3% × 251,6 mil = 18,6 mil → 59,9 mil + 8% × 391,7 mil = 91,2 mil | máx. 50 mil | **R$ 18,5 mil – 50 mil** | 34 mil |
| Vendaval | apartamento: 2% × 251,6 mil = 5,0 mil → 5% × 391,7 mil = 19,6 mil | — | **R$ 5 mil – 19,5 mil** | 12 mil |
| Impacto de veículos | apartamento: valor padrão | — | R$ 10 mil | — |
| Queda de aeronave | valor padrão | — | R$ 10 mil | — |
| Danos elétricos | 12,5 mil → 33,6 mil | máx. 30 mil | **R$ 12,5 mil – 30 mil** | 21 mil |
| Roubo | 9,4 mil → 25,4 mil | — | **R$ 9,5 mil – 25 mil** | 17 mil |
| Quebra de vidros | apartamento R$ 2–5 mil; o máximo sobe para 1,2 × 11 mil = 13,2 mil | — | **R$ 2 mil – 13 mil** | 7,5 mil |
| RC familiar | vizinho do mesmo tamanho: 110 × 2.287 × 30% = 75,5 mil → 110 × 3.561 × 60% = 235 mil | máx. 200 mil | **R$ 75 mil – 200 mil** | 138 mil |

## 7. Que perguntas?
| Candidata | Por quê | Prioridade | Tipo |
|---|---|---|---|
| Bens | A faixa dos bens tem 59,9 − 22,2 = R$ 37,7 mil de largura | 58 | opcional |
| Acabamento | 110 × 2.739 × (1,30 − 1,00) × 40% = R$ 36,2 mil do incêndio | 56 | opcional |
| Área | Não entra: a área é cadastrada | — | — |
| RC da família | Não entra: a RC já veio como adicional | — | — |

→ **2 perguntas, as duas opcionais.**

## 8. Confiança e jornada
- **Confiança:** tipo, vínculo, uso e área observados; bens por transação com idade de 18 meses, abaixo da meia-vida de 36 → observado. Os 5 observados, elegível e sem pendência → **ALTA**.
- **Jornada:** elegível · sem obra · usa o app · nenhuma pergunta obrigatória · maturidade 62 (≥ 40) → **1 toque**.

## 9. O que o cliente lê
> Recomendamos o plano Prático porque você gastou R$ 11 mil com vidraçaria nos últimos 2 anos, e vidro quebrado custa caro para repor. A estrutura tem o seguro do condomínio; o seu protege os acabamentos, cerca de R$ 105 mil, e os seus bens, de R$ 22 mil a R$ 60 mil. Incluímos a responsabilidade civil familiar, que paga danos que dependentes ou pet causem a vizinhos. Se você escolher menos, roubo e vidros ficarão descobertos: um arrombamento sairia do seu bolso. O Total acrescenta perda de aluguel e despesas emergenciais. Confiança alta: os dados vêm do seu cadastro e das suas contas.

---

# Caso 2 · `IMO_CASO_00015_01`, casa quitada em Porto Alegre, sem área cadastrada (Essencial)

## 1. Que imóvel é esse?
| Escolha | Dado | Regra | Resultado |
|---|---|---|---|
| **Tipo** | "Casa" no endereço, sem condomínio; complemento "QUADRA 8 CASA 15" | Confirma casa | Casa, observado |
| **Vínculo** | Sem aluguel, sem parcela, sem crédito de aluguel | Nenhum sinal → **proprietário (deduzido)** | Proprietário, **estimado** |
| **Uso** | Endereço bate com o principal | Moradia | Moradia habitual, observado |
| **Área** | Sem área cadastrada. IPTU R$ 1.650/ano; luz R$ 500/mês | IPTU: 1.650 ÷ 14,08 (Porto Alegre) = 117,2 m². Luz: 500 ÷ 3,52 = 141,9 m². **0,6 × 117,2 + 0,4 × 141,9 = 127 m²**. Faixa: 127 × 0,728 = 92 m² a 127 × 1,299 = 165 m² | 127 m² (92–165), **estimado** |

## 2. Reconstrução
- **Padrão:** vazio. Sem área cadastrada, o IPTU/m² **não pode** ser usado, porque a área já saiu do IPTU (seria circular) → fator de **0,85 a 1,30**, mais a pergunta do acabamento.
- **Custo do m²:** SINAPI RS R$ 2.065,95 × 0,85 = R$ 1.756 · CUB RS oficial R$ 2.943,73 × 1,30 = R$ 3.827.
- **Reconstrução:** 92 × 1.756 = **R$ 162 mil** a 165 × 3.827 = **R$ 632 mil**. A faixa é larga porque a área **e** o padrão são incertos.
- **Sem segundo risco:** casa quitada, então o residencial paga a estrutura inteira.

## 3. Bens
Compras 8.400 + 8.050 + 4.700 = R$ 21.150; bens ligados R$ 9.650. Mínimo 21.150 × 1,0694 = **R$ 22.618**; máximo 2,7 × 21.150 × 1,0694 = **R$ 61.069**. Bens com vínculo forte: 10.450 de 13.850 (75%, acima de 60%) e há compras → confiança dos bens **ALTA**.

## 4. Plano
Só um sinal: casa fora de condomínio (Prático +1). Bens R$ 22.618 (< 36 mil); eletrônicos R$ 8.983 (< 10 mil); sem vidraçaria. Prático 1, Total 0 → **Essencial**.
**Motivo sem sinal = patrimônio:** não há aluguel nem financiamento (o prejuízo seria todo dele) + quanto valem os aparelhos + danos elétricos são a cobertura mais acionada.
**Família:** 1 dependente, numa casa e abaixo do Total → **pergunta** da RC (casa não ganha a RC automaticamente).

## 5. Faixas (as principais)
| Cobertura | Conta | Faixa |
|---|---|---|
| Incêndio | 162 mil + 22,6 mil = 184,6 mil → 632 mil + 61,1 mil = 693 mil (teto 600 mil) | **R$ 185 mil – 600 mil** (sugerido 439 mil) |
| Vendaval | casa: 10% × 162 mil = 16,2 mil → 20% × 632 mil = 126 mil (teto 60 mil) | **R$ 16 mil – 60 mil** |
| Danos elétricos | 17,6 mil → 47,5 mil (teto 30 mil) | **R$ 17,5 mil – 30 mil**, confiança **ALTA** (bens com duas provas) |

## 6. Perguntas
| Candidata | Quanto aperta | Prioridade | Tipo |
|---|---|---|---|
| RC da família | muda o que está coberto | 59 | opcional |
| Área | (165 − 92) × 2.944 × 1,30 = **R$ 278 mil** do incêndio | 58 | opcional |
| Acabamento | 165 × 2.944 × (1,30 − 0,85) = **R$ 219 mil** | 56 | opcional |
| Bens (R$ 38 mil) e "o imóvel é seu e quitado?" | Ficam de fora (só 3 vagas) | 54 · 30 | — |

## 7. Confiança e jornada
Área e vínculo **estimados** (nenhum presumido) → **MÉDIA**. Nenhuma pergunta obrigatória, usa o app, maturidade 55 → **1 toque**: contrata com a faixa sugerida, e as 3 perguntas só ajustam.

## 8. O que o cliente lê
> Recomendamos o plano Essencial porque não vemos aluguel nem financiamento nas suas contas, então um incêndio ou um temporal sairia todo do seu bolso; seus eletrônicos e eletrodomésticos valem hoje de R$ 18 mil a R$ 47 mil, e danos elétricos são 53,3% dos acionamentos do residencial da BB. Reconstruir o imóvel custaria cerca de R$ 397 mil pelo custo oficial do IBGE, fora os seus bens. O Prático acrescenta roubo e vidros. Confiança média: a área foi estimada pelo IPTU e pela conta de luz.

---

# Cada número fixo: de onde veio e se é coerente
| Número | Onde | Origem | Coerente? |
|---|---|---|---|
| Peso 0,6 do IPTU e 0,4 da luz | Área | Premissa: o IPTU é calculado sobre a área; a luz varia com hábitos | Validado: erro de 15% (desenvolvimento) e 17% (teste) |
| Faixa 0,728–1,299 da área | Área | Percentis de 9% e 91% do erro na base de desenvolvimento | 80,9% (desenvolvimento) · 73,9% (teste, 46 casos) |
| Cortes 0,90 e 1,15 do IPTU/m² | Padrão | Medianas por padrão na base (0,82 · 0,98 · 1,32) | 97,8% e 7 de 7 no teste |
| Fator 0,85 / 1,00 / 1,30 | Padrão | Premissa (proporção entre padrões do CUB) | Defensável; confirmar com a tabela do CUB |
| 25%–40% de acabamentos | Segundo risco | Condições Gerais cl. 15.2 + premissa do percentual | Premissa: citar como tal |
| IPCA^1,5 (1,0694) | Bens | Banco Central (API); 1,5 ano = meio da janela de 36 meses | Coerente |
| 2,7 × compras | Bens | Premissa: ~8 anos de vida útil ÷ 3 anos de compras | Premissa: citar como tal |
| R$ 36 mil · R$ 10 mil | Plano | Medianas da base de desenvolvimento | Escolha de produto, não risco atuarial (1 caso muda com ±5%) |
| 10–20% (casa) · 2–5% (apartamento) | Vendaval | Premissa: telhado e esquadrias | Premissa: citar como tal |
| 50–100% bens + 3–8% reconstrução | Água | Premissa | Premissa; o teto de R$ 50 mil prende 134 casos |
| R$ 5 mil | Perguntas | Corte mínimo de valor de uma pergunta (RN-36) | Coerente com "poucas perguntas" |
| Prioridade 59 da RC da família | Perguntas | Muda o que está coberto, então vem antes das perguntas de valor | Corrigido em 29/10: 33 de 34 casas com família recebem a oferta (antes, 11) |

## O que esta conta revelou (e foi corrigido em 29/10)
- **A oferta da RC sumia:** em 23 de 34 casas com família, a pergunta da RC (prioridade 45) ficava de fora atrás das 3 perguntas de valor. Subiu para 59.
- **Ponto de atenção:** a RC do apartamento de 110 m² sai com mínimo de R$ 75 mil, porque considera o vizinho do mesmo tamanho e 30% a 60% da reconstrução dele. É conservador; os 30% são premissa.

Ligações: [[02 - O motor passo a passo]] · [[01 - Os dados e como tratamos]] · [[08 - Perguntas da banca e respostas]] · [[00 - Índice (leia nesta ordem)]]
