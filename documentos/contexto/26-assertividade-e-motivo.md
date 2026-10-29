# 26 · A assertividade de cada cálculo e o motivo feito para você

**Em uma frase:** todo cálculo que completa um dado faltante agora tem a sua **nota de acerto**, medida contra o valor real, e o motivo que o cliente lê passou a falar **da casa, da cidade e dos números dele**.

**Onde estamos:** véspera da entrega (28/10 à noite) · vault: `16 - Projeto por inteiro/11 - Assertividade de cada cálculo (do zero).md` e `12 - O motivo feito para você.md`

## Por que mudamos
| Problema | Evidência |
|---|---|
| Não sabíamos quanto cada conta de dado faltante acertava | O time pediu "a assertividade de cada cálculo, explicada do zero" |
| A faixa do incêndio era larga demais quando faltavam a área e o padrão | Pior caso × pior caso: 2,7× de largura (Recife: R$ 310 mil a R$ 961 mil) |
| O motivo era um modelo com números trocados | 83 esqueletos únicos em 138; nenhum citava a cidade; uma frase repetida em 93 motivos |

## O que fizemos
- `motor/assertividade.py` (novo): validação cruzada em **5 dobras** e comparação com o "chute" para área, região, padrão e área × padrão; concordância entre fontes para tipo, vínculo, uso e bens; teste do CEP. Os backtests saíram de `motor.py` para cá.
- Área pela **média geométrica** (IPTU^0,6 × luz^0,4): erro de 15,0% para 14,1%. Os pesos foram confirmados por regressão (0,59 e 0,42).
- **Faixa calibrada de área × padrão** nos 64 casos sem área e sem padrão: 1,76× de largura, contendo o real em 88% (antes 2,7× e 98%).
- Motivo novo: casa e cidade · porquê · **fato que diferencia dos vizinhos** (percentis da cidade) · **risco da cidade** (ANEEL, Defesa Civil) · o que fica descoberto **em reais** · confiança com o **acerto medido**. Até 140 palavras, com prioridade por frase.
- Perguntas dizem o porquê em reais ("a resposta pode mudar o valor do incêndio em até R$ 148 mil").
- `entrega/assertividade.json` e a chave `assertividade` em `metricas.json`.
- Revisão de código: 8 achados, todos corrigidos, e mais 1 na conferência final (o custo do m² aparecia com o fator de padrão na regra).

## Resultado
| | Antes | Depois |
|---|---|---|
| Área: erro mediano (chute: 44,4%) | 15,0% | **14,1%** |
| Faixa de área × padrão (sem os dois) | 2,7× · 98% | **1,76× · 88%** |
| Motivo cita a casa e a cidade | 0 | **138** |
| Esqueletos únicos | 83 | **125** |
| Frase mais repetida | 93 motivos | **32** |
| Testes | 111 | **155** |
| Planos | Prático 66 · Total 38 · Essencial 34 | iguais |

## O que não fizemos (e por quê)
- Metas de 130 esqueletos e semelhança < 0,15: chegamos a 125 e 0,21. O resto é legítimo (mesmo plano, cidade e tipo, sem fato distintivo).
- Água e tipo na fórmula da área: melhoram menos de 1 ponto e deixam a conta difícil de explicar.
- Valor dos bens e uso do imóvel continuam sem gabarito: dizemos isso em vez de inventar uma acurácia.

## Próximo passo
Revisar com o time as notas 11 e 12 do vault antes do pitch.
