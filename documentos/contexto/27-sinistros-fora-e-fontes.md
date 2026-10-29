# 27 · Sinistros da BB fora e o motor sem as fontes externas

**Em uma frase:** tiramos o dado de sinistros da BB (fonte de imprensa, sem como auditar) e provamos que o motor roda sem internet e até sem os arquivos externos.

**Onde estamos:** dia da entrega (29/10) · vault: `16 - Projeto por inteiro/04 - Fontes externas e APIs.md`

## O que fizemos
- Removemos `sinistros_residencial_bb.csv`, `sinistros_pct`, `FONTE_SINISTROS`, a frase "Na BB Seguros, X% dos acionamentos…" das coberturas, a cláusula dos 53,3% no motivo do Essencial (trocada por "um pico de energia pode queimar vários de uma vez") e as duas métricas de aderência.
- Teste novo: `test_sem_dado_de_sinistro_da_bb`.
- Rodamos o motor com a rede bloqueada (0 erros) e sem nenhum arquivo externo.

## Resultado
| | Sem internet | Sem nenhum arquivo externo |
|---|---|---|
| Erros nas planilhas | 0 | 0 |
| Elegibilidade, jornada, confiança | iguais | iguais (138 de 138) |
| Plano | igual | 137 de 138 (1 caso "no limite", pelo IPCA) |
| Faixa do incêndio | igual | meio da faixa muda 0% na mediana (−10,5% a +8,9%) |

Nenhum plano nem faixa mudou ao tirar os sinistros. 155 testes passando.

## Próximo passo
Decidir a proposta dos bens (vida útil por categoria) e o frescor.
