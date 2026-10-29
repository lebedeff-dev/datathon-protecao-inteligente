---
tags: [projeto, motor, regras, formulas]
atualizado: 2026-10-28
---
# ⚙️ 02 · O motor passo a passo

Para cada cliente-imóvel, `motor.processar_caso` faz 8 passos e devolve a **ficha**. Tudo são regras escritas (sem caixa-preta), e toda premissa numérica está em `motor/parametros.py`.

```mermaid
flowchart LR
  A[1 · Entender<br>o imóvel] --> B[2 · Elegibilidade] --> C[3 · Plano] --> D[4 · Faixas] --> E[5 · Perguntas] --> F[6 · Confiança] --> G[7 · Jornada] --> H[8 · Motivo]
```

## 1 · Entender o imóvel
| Dado | Regra | Exemplo |
|---|---|---|
| **Tipo** | Termo "apartamento" no endereço → apartamento; "condomínio" → casa em condomínio; senão, casa. O complemento (AP, BLOCO, CASA, LOTE) confirma ou levanta dúvida | "BLOCO B APTO 305" confirma apartamento |
| **Vínculo** | Paga aluguel → inquilino; paga parcela → financiado; recebe aluguel e não mora → locador; senão → proprietário (inferido) | Parcela de R$ 950 → financiado |
| **Uso** | Endereço principal → moradia; recebe aluguel → alugado a terceiros; mora em outro imóvel → veraneio; senão, dúvida (cadastro desatualizado?) | — |
| **Área** e **bens** | Ver [[01 - Os dados e como tratamos]] | 110 m² (IPTU) · bens de R$ 22 mil a R$ 60 mil |
| **Valor da casa** | Área × custo do m² (SINAPI a CUB) × padrão; segundo risco = 25% a 40% | — |

## 2 · Elegibilidade (antes de tudo; RN-15)
| Situação | Resultado |
|---|---|
| Situação cadastral não regular (tombado, desapropriado, condenado) | **NÃO** |
| Seguro residencial + produto de seguridade BB + um único imóvel | **NÃO** (provável seguro BB no endereço) |
| Seguro residencial sem produto BB | SIM + pergunta obrigatória "O seu seguro atual é da BB Seguros?" |
| Seguro residencial e mais de um imóvel | SIM + pergunta "Qual dos seus imóveis já tem o seguro da BB?" |
| R$ 15 mil ou mais em material de construção em 24 meses | SIM + pergunta "Está em obra ou reforma?" (obra impede) |
| Parede de outro material que não alvenaria | SIM + pergunta "É madeira pré-fabricada certificada?" |

**Regra de ouro (RN-19):** sinal fraco nunca vira NÃO; vira pergunta. Resultado: SIM 122 · NÃO 16.

## 3 · Plano (pontos por sinais)
| Sinal | Pontos | Para |
|---|---|---|
| Paga aluguel (inquilino) | 2 | Total |
| Recebe aluguel do imóvel | 2 | Total |
| Prédio ou condomínio (vizinhos) | 1 | Total |
| Dependentes **e** pet | 1 | Total |
| Bens comprovados ≥ R$ 36 mil | 2 | Prático |
| Eletrônicos comprovados ≥ R$ 10 mil | 1 | Prático |
| Casa fora de condomínio | 1 | Prático |
| Gasto com vidraçaria em 24 meses | 1 | Prático |

**Decisão:** Total com 2 pontos ou mais de Total; Prático com 2 de Prático (ou 1 de Prático + 1 de Total do imóvel); senão, Essencial. Veraneio não soma para o Prático (o roubo não cobre casa desocupada). Bens presumidos não somam pontos. **Adicional:** RC familiar para prédio ou condomínio com dependentes ou pet, quando o plano não é o Total.
Resultado: Prático 59 · Total 49 · Essencial 30 · RC adicional 41.

## 4 · Faixas de cada cobertura
| Cobertura | Mínimo → máximo | Limite do produto |
|---|---|---|
| Incêndio | reconstrução + bens (segundo risco: 25%–40% da reconstrução + bens) | R$ 100 mil a R$ 600 mil |
| Danos por água | 50%–100% dos bens molháveis + 3%–8% da reconstrução | R$ 3 mil a R$ 50 mil |
| Vendaval e granizo | casa 10%–20% da reconstrução · apartamento 2%–5% | R$ 1 mil a R$ 60 mil |
| Impacto de veículos | casa R$ 10–20 mil · apartamento R$ 10 mil | até R$ 20 mil |
| Queda de aeronave | R$ 10 mil (padrão) | até R$ 20 mil |
| Danos elétricos | eletrônicos + eletrodomésticos: comprovado → estoque | R$ 5 mil a R$ 30 mil |
| Roubo | eletrônicos: comprovado → estoque | R$ 1 mil a R$ 45 mil |
| Quebra de vidros | casa R$ 3–8 mil · apartamento R$ 2–5 mil; ampliada para 1,2 × o gasto com vidraçaria | R$ 1 mil a R$ 25 mil |
| RC familiar | prédio: 70 m² × custo do m² × 30%–60% · casa: R$ 30–60 mil | R$ 10 mil a R$ 200 mil |
| Perda de aluguel | aluguel pago ou recebido × 6 a 12 meses; senão FipeZAP × área × 6 a 12 | R$ 5 mil a R$ 30 mil |
| Despesas emergenciais | 2%–5% da faixa de incêndio | R$ 2 mil a R$ 15 mil |

Depois, cada faixa vai para dentro do limite do produto e é arredondada (de 500 em 500 até R$ 20 mil, de 1.000 em 1.000 acima). Se a estimativa passa do limite, a observação avisa que o excedente fica descoberto. Cada cobertura também traz um **valor sugerido** (meio da faixa; no incêndio, o valor em risco), para o app não puxar o mínimo e gerar subseguro.

## 5 · Perguntas (até 3)
| Prioridade | Pergunta | Tipo |
|---|---|---|
| 95–100 | Elegibilidade (seguro BB? obra? material?) | **obrigatória** |
| 70 | "É onde você mora, veraneio ou alugado?" (uso duvidoso) | **obrigatória** |
| 60 | "Você recebe aluguel deste imóvel?" | opcional |
| 59 | Inquilino de casa: "O contrato pede que você segure o imóvel?" | opcional |
| 58 · 56 · 54 | Bens, área, acabamento, **na ordem de quanto cada resposta aperta a faixa** | opcional |
| 45 | "Quer proteção para danos que dependentes ou pet causem?" | opcional |
| 40 | "É apartamento ou casa?" (complemento diverge) | **obrigatória** |
| 30 | "O imóvel é seu e já está quitado?" | opcional |

Pergunta de valor que aperta a faixa em menos de R$ 5 mil não é feita, e nenhuma promete apertar mais do que a largura da faixa entregue. **Obrigatória trava a contratação; opcional só ajusta o valor.** Média: 2,77 perguntas por caso, sendo 0,34 obrigatória; 94 casos não têm nenhuma obrigatória.

## 6 · Confiança
**Geral (do caso):** cada dado crítico (tipo, vínculo, uso, área, bens) é **observado** (documento, transação ou confirmado), **estimado** (derivado ou inferido) ou **presumido**. Observado mais velho que a meia-vida do campo conta como estimado.
- **BAIXA:** área ou bens presumidos, ou algum presumido junto com estimado.
- **ALTA:** os 5 observados, elegível e sem pendência.
- **MÉDIA:** o resto. Resultado: alta 17 · média 101 · baixa 20.

**Por cobertura:** o pior dos dados que a cobertura usa. Incêndio: área, padrão, bens e fonte; vendaval: área, padrão e fonte; danos elétricos e roubo: bens. Assim, danos elétricos saem ALTA em 69 casos e o incêndio só é ALTA com área e padrão cadastrados.

## 7 · Jornada (gerente em último caso)
| Jornada               | Quando                                                                                                                                                                        | Casos                  |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **1 toque**           | Nenhuma pergunta obrigatória: contrata com a faixa sugerida                                                                                                                   | 63                     |
| **App com perguntas** | Pergunta obrigatória (elegibilidade, uso duvidoso) ou pouca familiaridade com o app. Na confiança baixa, o app pergunta primeiro e o gerente entra se a resposta mudar o caso | 37                     |
| **Gerente**           | Sinal de obra ou cliente sem o app                                                                                                                                            | 22 (18% dos elegíveis) |
| **Sem nova proposta** | Não elegível: o app informa e a ficha serve para revisar a apólice                                                                                                            | 16                     |

O campo `canal` (1 toque × gerente) continua existindo para o protótipo.

## 8 · Motivo (o porquê; `motor/motivo.py`)
Roteiro fixo, em linguagem de cliente:
1. **Fato dele:** "você gastou R$ 11 mil com vidraçaria nos últimos 2 anos".
2. **Quanto está em jogo:** "reconstruir o imóvel custaria cerca de R$ 394 mil pelo custo oficial do IBGE".
3. **Se escolher menos** (frase do slide 23): "roubo e vidros ficarão descobertos".
4. **Opção acima:** "o Total acrescenta perda de aluguel e despesas emergenciais".
5. **O que confirmar:** a pergunta obrigatória, se houver.
6. **Confiança** em uma frase: "a área foi estimada pelo IPTU e pela conta de luz".

Cada cobertura também tem a sua justificativa com os números do cliente, a frequência real de sinistros da BB e o dado oficial da cidade (Defesa Civil ou ANEEL). Números arredondados como gente fala ("R$ 49 mil"); estimativa sempre dita como estimativa.

Próxima: [[03 - Cada métrica explicada]]
