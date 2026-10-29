# 23 · Perguntas obrigatórias × opcionais, sugestões P1 e o projeto inteiro no vault

**Em uma frase:** o 1 toque virou 1 toque de verdade (sem pergunta que trave), a confiança baixa pergunta no app antes de chamar o gerente, aceitamos o PR #14 (renda) e aplicamos as sugestões de código do relatório de validação. E o projeto inteiro ficou explicado no vault.

**Onde estamos:** véspera da entrega · vault: `obsidian/BB Datathon/16 - Projeto por inteiro/`

## O que fizemos
**Perguntas e jornada**
- Cada pergunta agora é **obrigatória** (trava a contratação: elegibilidade, "você mora no imóvel?", "é casa ou apartamento?") ou **opcional** (só ajusta valor: bens, área, acabamento). Na planilha, as opcionais vêm com "(opcional)".
- **1 toque = nenhuma pergunta obrigatória:** 63 casos contratam direto com a faixa sugerida. 94 casos não têm nenhuma pergunta que trave.
- **Confiança baixa pergunta no app antes:** o gerente entra se a resposta mudar o caso ou não vier. Gerente: **35 → 22** (18% dos elegíveis; só obra ou sem app). STP: 72,5%.
- Pergunta dos bens com números arredondados ("R$ 22 mil", não "R$ 22.000").

**PR #14 (Eduardo): renda liberada e relatório de validação.** Aceito depois de rodar os testes numa cópia separada (91 passando) e conferir o código: a renda só reforça os bens de quem não tem compras, presa entre 0,5× e 2× a média da região, e nunca chega a plano, elegibilidade, jornada ou confiança. Erro fora da amostra 40,5% → 22,7%. As planilhas não mudam (todo caso da base tem compras). O merge foi feito localmente.

**Sugestões P1 do relatório, aplicadas**
| Sugestão | O que fizemos | Efeito |
|---|---|---|
| Confiança por cobertura quase constante | Cada cobertura usa a confiança dos dados que ela usa (área, padrão, bens, fonte); bens com compras + vínculo forte = ALTA | Danos elétricos ALTA 69 · roubo ALTA 56 · incêndio ALTA 6 (área e padrão cadastrados) |
| Escolher o mínimo gera subseguro | Valor **sugerido** em cada cobertura (meio da faixa; no incêndio, o valor em risco) | ITV no sugerido = 1,00 (no mínimo era 0,60) |
| Faixa da área contém a real em 78% | Percentis 9% e 91% | 80,9% fora da amostra (meta 80%) |
| Inquilino de casa paga a reconstrução | Pergunta opcional: "o contrato pede que você segure o imóvel?" | — |
| Ficaram para depois | Pergunta das compras fora do BB (P2); limites de água e elétricos (confirmar com a BB); família no plano | — |

**Vault: o projeto inteiro (pasta 16).** Índice + 7 notas: os dados e cada lacuna, o motor com todas as fórmulas, cada métrica do `metricas.json`, fontes e APIs, as saídas (cada coluna das planilhas, a ficha, a API), os 99 testes e as regras e decisões.

**Testes:** 99 passando. Planos, elegibilidade e confiança geral iguais; justiça = 0; reprodutível byte a byte.

## Como conferir
```bash
python -m pytest -q
python motor/gerar.py --entrega
```
Resultado esperado: 99 testes passando; `jornada` = 1 toque 63 · app 37 · gerente 22 · sem proposta 16.

## Frase para o pitch
> "Em 94 dos 138 casos, nada trava: o cliente contrata direto com a faixa sugerida e as perguntas só refinam o valor. O gerente entra em 22 casos, quando há obra ou o cliente não usa o app."

## Próximo passo
- Nome da equipe no README e vídeo de 5 min. Decidir família no plano e quem não usa o app.
