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
> Se o motor estimasse: IPTU R$ 1.800 ÷ R$ 13,75/m² (mediana de Curitiba) = 130,9 m²; luz R$ 500 ÷ R$ 3,60/m² = 138,9 m²; 130,9^0,6 × 138,9^0,4 = **134 m²** (média geométrica; ver [[11 - Assertividade de cada cálculo (do zero)]]), 22% acima do real. Por isso a estimativa só entra quando falta o cadastro.

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

## 5. Qual plano? (as três necessidades)
| Necessidade | Pergunta | Resposta e prova | Força |
|---|---|---|---|
| **A · Aluguel em jogo** | Paga ou recebe aluguel deste imóvel? | **Não** (paga parcela de financiamento, não aluguel) | — |
| **B · Roubo e vidros** | Bens ≥ R$ 36 mil? Eletrônicos ≥ R$ 10 mil? Gastou com vidros? | Bens R$ 22.190 (não); eletrônicos R$ 9.411 (não, mas perto); **vidraçaria R$ 11.000 (sim)** | **Clara**: a vidraçaria é uma prova direta, não depende de limite |
| **C · Danos a terceiros** | Prédio ou condomínio? Dependentes ou pet? | **Sim**: apartamento (o vizinho está colado) e 1 dependente | Clara |

**Decisão:** não tem A → não é Total. Tem B → **Prático**. Tem C e o plano não é o Total → **RC familiar como adicional**.
**Motivo do plano:** a prova que acendeu B (a vidraçaria).
**Por que a força é "clara" mesmo com eletrônicos perto do limite:** a necessidade B já está provada pela vidraçaria. O valor dos eletrônicos não muda o plano, então não há pergunta decisiva.

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
| Pergunta decisiva | Não entra: a recomendação é clara | — | — |

→ **2 perguntas, as duas opcionais.** Desde 28/10 elas dizem o porquê em reais: *"Seus móveis, eletrodomésticos e eletrônicos valem entre R$ 22 mil e R$ 60 mil? A resposta pode mudar a proteção dos seus bens em até R$ 38 mil."* e *"O acabamento do imóvel é simples, normal ou de alto padrão? A resposta pode mudar o valor do incêndio em até R$ 36 mil."*

## 8. Confiança e jornada
- **Confiança:** tipo, vínculo, uso e área observados; bens por transação com idade de 18 meses, abaixo da meia-vida de 36 → observado. Os 5 observados, elegível e sem pendência → **ALTA**.
- **Jornada:** elegível · sem obra · usa o app · nenhuma pergunta obrigatória · maturidade 62 (≥ 40) → **1 toque**.

## 9. O que o cliente lê (motivo feito para você, desde 28/10)
> Para o seu apartamento de 110 m² em Curitiba, recomendamos o plano Prático com a responsabilidade civil familiar. Isso porque você gastou R$ 11 mil com vidraçaria nos últimos 2 anos, e vidro quebrado custa caro para repor; e, no prédio e com dependentes ou pet, um acidente seu pode atingir outras pessoas. Em Curitiba, a distribuidora de luz ficou entre as piores no ranking de quedas de energia da ANEEL (27º de 33, 2025); o plano cobre danos elétricos. Se você escolher menos, R$ 22 mil em bens no seu apartamento ficam descobertos contra roubo e quebra de vidros. Confiança alta: os dados vêm do seu cadastro e das suas contas.

**Por que cada frase está ali** (ver [[12 - O motivo feito para você]]):
- **Sem fato dos vizinhos:** compras de R$ 20.750 e eletrônicos de R$ 8.800 ficam entre os percentis 25 e 75 dos apartamentos de Curitiba (113 imóveis). Ele está no meio, então não há o que diferenciar.
- **Risco da cidade:** a COPEL ficou em 27º de 33 (≥ 75% de 33 = 24,75) → frase da ANEEL. Curitiba também teve 10 registros de chuva forte, mas a ANEEL vem primeiro na ordem.
- **Saiu para caber em 140 palavras:** o valor em jogo e a opção acima ("O Total acrescenta…"), as de menor prioridade.

---

# Caso 2 · `IMO_CASO_00015_01`, casa quitada em Porto Alegre, sem área cadastrada (Essencial)

## 1. Que imóvel é esse?
| Escolha | Dado | Regra | Resultado |
|---|---|---|---|
| **Tipo** | "Casa" no endereço, sem condomínio; complemento "QUADRA 8 CASA 15" | Confirma casa | Casa, observado |
| **Vínculo** | Sem aluguel, sem parcela, sem crédito de aluguel | Nenhum sinal → **proprietário (deduzido)** | Proprietário, **estimado** |
| **Uso** | Endereço bate com o principal | Moradia | Moradia habitual, observado |
| **Área** | Sem área cadastrada. IPTU R$ 1.650/ano; luz R$ 500/mês | IPTU: 1.650 ÷ 14,08 (Porto Alegre) = 117,2 m². Luz: 500 ÷ 3,52 = 142,0 m². **117,2^0,6 × 142,0^0,4 = 126,6 m²** (média geométrica). Faixa: 126,6 × 0,75 = 95 m² a 126,6 × 1,32 = 166 m² | 127 m² (95–166), **estimado** |

## 2. Reconstrução
- **Padrão:** vazio. Sem área cadastrada, o IPTU/m² **não pode** ser usado, porque a área já saiu do IPTU (seria circular). Faltam a área **e** o padrão → **faixa calibrada de área × padrão** (ver [[11 - Assertividade de cada cálculo (do zero)]], seção 4), mais a pergunta do acabamento.
- **Área × padrão:** de **95 a 166 m² de padrão normal**. É a faixa da área com o padrão normal: o erro real de área × padrão, medido fora da amostra, cabe nela em 88% dos testes.
- **Custo do m²:** SINAPI RS R$ 2.065,95 até CUB RS oficial R$ 2.943,73 (sem fator, porque o padrão já está em área × padrão).
- **Reconstrução:** 95 × 2.066 = **R$ 196 mil** a 166 × 2.944 = **R$ 490 mil**.
- **Antes (pior caso de cada um):** 92 × 2.066 × 0,85 = R$ 162 mil a 165 × 2.944 × 1,30 = R$ 632 mil: 3,9 vezes de largura. **Agora: 2,5 vezes.**
- **Sem segundo risco:** casa quitada, então o residencial paga a estrutura inteira.

## 3. Bens
Compras 8.400 + 8.050 + 4.700 = R$ 21.150; bens ligados R$ 9.650. Mínimo 21.150 × 1,0694 = **R$ 22.618**; máximo 2,7 × 21.150 × 1,0694 = **R$ 61.069**. Bens com vínculo forte: 10.450 de 13.850 (75%, acima de 60%) e há compras → confiança dos bens **ALTA**.

## 4. Plano (as três necessidades)
| Necessidade | Resposta e prova | Força |
|---|---|---|
| **A · Aluguel em jogo** | **Não**: sem aluguel pago nem recebido | — |
| **B · Roubo e vidros** | **Não**: bens R$ 22.618 (< 36 mil); eletrônicos **R$ 8.983** (< 10 mil); sem vidraçaria. A casa fora de condomínio é só agravante | **No limite**: 8.983 ÷ 10.000 = 0,90, a menos de 15% do limite |
| **C · Danos a terceiros** | **Sim**: 1 dependente | Clara |

**Decisão:** sem A e sem B → **Essencial**, + **RC familiar como adicional** (por causa de C).
**Como a recomendação "no limite" aparece:**
1. a pergunta decisiva entra em primeiro: "Seus eletrônicos (TV, notebook, celulares, videogame) valem mais de R$ 10 mil?";
2. o motivo avisa: "Você está perto de precisar do Prático, que cobre roubo e vidros";
3. se o cliente responder "sim", a necessidade B acende e o plano sobe para o Prático.

**Motivo sem necessidade A ou B = patrimônio:** não há aluguel nem financiamento (o prejuízo seria todo dele), quanto valem os aparelhos e o fato de danos elétricos serem a cobertura mais acionada.

## 5. Faixas (as principais)
| Cobertura | Conta | Faixa |
|---|---|---|
| Incêndio | 196 mil + 22,6 mil = 218,6 mil → 490 mil + 61,1 mil = 551 mil | **R$ 219 mil – 551 mil** (sugerido 385 mil; antes R$ 185 mil – 600 mil, preso no teto) |
| Vendaval | casa: 10% × 196 mil = 19,6 mil → 20% × 490 mil = 98 mil (teto 60 mil) | **R$ 19,5 mil – 60 mil** |
| Danos elétricos | 17,6 mil → 47,5 mil (teto 30 mil) | **R$ 17,5 mil – 30 mil**, confiança **ALTA** (bens com duas provas) |

## 6. Perguntas
| Candidata | Quanto aperta | Prioridade | Tipo |
|---|---|---|---|
| **Pergunta decisiva** (eletrônicos > R$ 10 mil?) | decide entre Essencial e Prático | 65 | opcional |
| Área | (166 − 95) × 2.944 × 1,30 = **R$ 274 mil** do incêndio. Texto: "Qual a área do seu imóvel? Estimamos de 95 a 166 m². A resposta pode mudar o valor do incêndio em até R$ 274 mil." | 58 | opcional |
| Acabamento | 166 × 2.944 × (1,30 − 0,85) = **R$ 220 mil** | 56 | opcional |
| Bens (R$ 38 mil) e "o imóvel é seu e quitado?" | Ficam de fora (só 3 vagas; a RC agora entra como adicional, sem pergunta) | 54 · 30 | — |

## 7. Confiança e jornada
Área e vínculo **estimados** (nenhum presumido) → **MÉDIA**. Nenhuma pergunta obrigatória, usa o app, maturidade 55 → **1 toque**: contrata com a faixa sugerida, e as 3 perguntas só ajustam.

## 8. O que o cliente lê
> Para a sua casa de cerca de 127 m² em Porto Alegre, recomendamos o plano Essencial com a responsabilidade civil familiar. Isso porque não há aluguel nem financiamento nas suas contas, então um incêndio sairia todo do seu bolso; seus eletrônicos e eletrodomésticos valem hoje de R$ 18 mil a R$ 47 mil, e um pico de energia pode queimar vários de uma vez; e, com dependentes ou pet em casa, um acidente pode atingir outras pessoas. Você está perto de precisar do Prático, que cobre roubo e vidros: a pergunta sobre os seus bens decide. Confiança média: a área veio do seu IPTU e da sua conta de luz, comparados aos de Porto Alegre (erro abaixo de 20% em 2 de cada 3 testes).

**Por que cada frase está ali** (ver [[12 - O motivo feito para você]]):
- **"cerca de 127 m²":** a área foi estimada, então o texto diz "cerca de" (RN-09).
- **A confiança com número:** os 2 de cada 3 vêm do boletim da área (65,4% dos imóveis a menos de 20% da área real), não de um texto escrito à mão.
- **Saíram para caber em 140 palavras:** o fato dos vizinhos (compras de R$ 21.150, abaixo do percentil 25 das casas de Porto Alegre, R$ 26.350: "o roubo pesa menos para você"), o risco da cidade (a distribuidora em último lugar na ANEEL) e o valor em jogo. A frase "perto do limite" tem prioridade, porque a pergunta decide o plano.

---

# Cada número fixo: de onde veio e se é coerente
| Número | Onde | Origem | Coerente? |
|---|---|---|---|
| Peso 0,6 do IPTU e 0,4 da luz, em média geométrica | Área | Premissa (o IPTU acompanha mais a área: 0,86 contra 0,80), **confirmada por regressão** (0,59 e 0,42) | Erro mediano 14,1% fora da amostra (chute: 44,4%) · 17,3% nos 46 do teste com área |
| Faixa 0,75–1,32 da área | Área | Percentis de 9% e 91% da razão real ÷ estimada | 81,0% (desenvolvimento, 5 dobras) · 71,7% (teste, só 46 casos) |
| Cortes 0,90 e 1,15 do IPTU/m² | Padrão | Medianas por padrão na base (0,81 · 0,98 · 1,35) e onde as faixas quase não se cruzam | Intervalo certo em 97,8% (182 estreitados); o padrão exato acertaria só 51% |
| Faixa calibrada de área × padrão | Reconstrução sem área e sem padrão | Percentis 9% e 91% do erro real de área × padrão, nunca abaixo da faixa de padrão normal | Contém o real em 88% (pior caso: 98%, mas 2,7× mais largo) |
| Percentis 25 e 75 ("3 em cada 4") · 10 e 90 ("9 em cada 10") | Fato dos vizinhos | Só quem está fora do meio é diferente | O meio não vira frase |
| ≥ 75% do ranking da ANEEL | Risco da cidade | "Entre as piores" só no último quarto | Recife (21º) fica sem a frase da ANEEL e recebe a da Defesa Civil |
| 140 palavras | Motivo | Com 130, o fato e o risco cabiam em menos de 30% | ~1 minuto de leitura |
| Fator 0,85 / 1,00 / 1,30 | Padrão | Premissa (proporção entre padrões do CUB) | Defensável; confirmar com a tabela do CUB |
| 25%–40% de acabamentos | Segundo risco | Condições Gerais cl. 15.2 + premissa do percentual | Premissa: citar como tal |
| IPCA^1,5 (1,0694) | Bens | Banco Central (API); 1,5 ano = meio da janela de 36 meses | Coerente |
| 2,7 × compras | Bens | Premissa: ~8 anos de vida útil ÷ 3 anos de compras | Premissa: citar como tal |
| R$ 36 mil · R$ 10 mil | Necessidade B (roubo) | Medianas da base de desenvolvimento | Escolha de produto, não risco atuarial. Por isso existe a faixa "no limite" (±15%) com pergunta decisiva; o único caso que muda com ±5% está marcado "no limite" |
| ±15% ("no limite") | Força da recomendação | Premissa: a margem de erro típica das estimativas da base (15% a 17%) | Coerente com o backtest |
| 10–20% (casa) · 2–5% (apartamento) | Vendaval | Premissa: telhado e esquadrias | Premissa: citar como tal |
| 50–100% bens + 3–8% reconstrução | Água | Premissa | Premissa; o teto de R$ 50 mil prende 134 casos |
| R$ 5 mil | Perguntas | Corte mínimo de valor de uma pergunta (RN-36) | Coerente com "poucas perguntas" |
| RC familiar como adicional | Necessidade C | Prédio, condomínio ou família | Desde 29/10, 93 imóveis com RC (antes, 52); todo prédio tem a proteção do vizinho |

## O que esta conta revelou (e foi corrigido)
- **(28/10) A faixa do incêndio no caso 2 ia até o teto do produto** porque somava o pior caso da área com o pior caso do padrão. Com a faixa calibrada, vai de R$ 219 mil a R$ 551 mil, abaixo do teto.
- **A oferta da RC sumia:** em 23 de 34 casas com família, a pergunta da RC (prioridade 45) ficava de fora atrás das 3 perguntas de valor. Subiu para 59.
- **Ponto de atenção:** a RC do apartamento de 110 m² sai com mínimo de R$ 75 mil, porque considera o vizinho do mesmo tamanho e 30% a 60% da reconstrução dele. É conservador; os 30% são premissa.

Ligações: [[02 - O motor passo a passo]] · [[01 - Os dados e como tratamos]] · [[08 - Perguntas da banca e respostas]] · [[00 - Índice (leia nesta ordem)]]
