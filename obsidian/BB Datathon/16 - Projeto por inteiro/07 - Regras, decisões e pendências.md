---
tags: [projeto, regras, decisoes]
atualizado: 2026-10-28
---
# ⚖️ 07 · Regras, decisões e pendências

## Que regra cada parte atende
| Regra | Onde no projeto |
|---|---|
| RN-07 (revisada, D-08): idade nunca; renda só como reforço | Teste de justiça = 0; renda só nos bens sem compras |
| RN-08: combinar sinais | Plano por pontos; renda × região; fonte externa só reforça |
| RN-09: estimativa não é fato | Natureza de cada dado; "estimamos" no texto |
| RN-10: CEP e coordenadas fictícios | Não usados; teste do CEP |
| RN-11, RN-12: fonte documentada; funciona sem ela | `FONTES.md`; leitura que devolve `None`; testes sem arquivo |
| RN-15 a RN-19: elegibilidade antes; sinal fraco vira pergunta | Passo 2 |
| RN-21 a RN-24: coberturas do catálogo; assistências fora | Validador |
| RN-27: imóvel alugado | Observação de beneficiários; pergunta do contrato |
| RN-31 a RN-33: só números; faixa sempre; plano = coberturas | Validador |
| RN-34 a RN-39: explicável, confiança, poucas perguntas, alternativas, casos contrastantes | Motivo 2.0, confiança, perguntas, `casos_contrastantes.json` |
| RN-49 a RN-54 (banca): o motivo é o principal; gerente importa; equilíbrio | Motivo 2.0; relatório do gerente; 1 toque |
| D-07: sem superseguro nem subseguro | Aviso de limite; valor sugerido; ITV |

## Decisões do time (registro)
| Quando | Decisão |
|---|---|
| 28/10 | Seguro existente só vira NÃO com produto de seguridade BB (o campo não diz a seguradora) |
| 28/10 | Renda liberada como reforço dos bens sem compras (D-08, mentoria do BB; PR #14) |
| 28/10 | Gerente é o último recurso (mentoria): só obra ou sem app; confiança baixa pergunta no app antes |
| 28/10 | Perguntas obrigatórias × opcionais: 1 toque sem pergunta que trave |
| 28/10 | Média da região em degraus; CEP desligado (ruído) |
| 28/10 | SINAPI e IPCA ao vivo pelas APIs do IBGE e do BC, com reserva |
| 29/10 | Seguro existente com produto BB vira pergunta obrigatória, não NÃO (RN-19) |
| 29/10 | **Família nunca muda o plano**: só RC familiar como adicional ou pergunta (RN-07) |
| 29/10 | Inquilino de casa: só os bens no incêndio; a estrutura entra se o contrato pedir (D-07) |
| 29/10 | Fontes por nível de confiança; sinistros da matéria só como contexto |
| 29/10 | **Recomendação por necessidades** no lugar dos pontos: aluguel → Total; roubo e vidros → Prático; terceiros → RC; força "clara" ou "no limite" com pergunta decisiva |

## Ainda em aberto
- **Quem não usa o app** (16 casos): gerente direto ou convite ao app antes (D-01).
- **Limites de danos por água e danos elétricos:** são premissa e prendem a maioria das faixas.
- **Pergunta das compras fora do BB** (proposta do relatório: em 29 casos a renda sugere compras bem maiores que as vistas no BB).
- **P0 da entrega:** nome da equipe no README e vídeo de 5 min.

Ligações: [[Regras de negócio]] · [[Regras de negócio - arquivo para as IAs do grupo]] · [[Auditoria do código - 28-10]] · [[00 - Índice (leia nesta ordem)]]
