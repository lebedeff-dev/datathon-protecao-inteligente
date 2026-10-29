# 25 · Recomendação por necessidades e documentação completa

**Em uma frase:** o plano deixou de sair de uma pontuação confusa e passou a sair de **três necessidades** com prova: aluguel em jogo → Total; roubo e vidros → Prático; danos a terceiros → RC. Cada recomendação diz se é **clara** ou **no limite**, e quem está no limite recebe a pergunta que decide.

**Onde estamos:** dia da entrega (29/10) · vault: `16 - Projeto por inteiro/` (glossário, dicionário de funções, motor passo a passo, conta por conta)

## Por que mudamos
| Problema da pontuação | Evidência |
|---|---|
| Dois placares com "força 2" nos dois lados; difícil de explicar | Dúvida do próprio time |
| "Mora em prédio" contava para o Total, mas só empurrava para o Prático, que não cobre vizinhos | 6 casos |
| 7 de 78 imóveis em prédio ficavam sem RC | — |
| Um terço dos planos decidido por menos de 15% do limite, sem aviso | 27 (bens) e 24 (eletrônicos) perto do limite |
| Veraneio com bens altos ia para o Prático, mas o roubo não cobre casa desocupada | 2 casos |

## O que fizemos
- `avaliar_necessidades`: as três perguntas, cada uma com sim/não, prova, força e (no limite) a pergunta decisiva.
- `escolher_plano`: o menor plano que cobre as necessidades.
- RC familiar como adicional para **todo** prédio, condomínio ou família abaixo do Total.
- Pergunta decisiva (prioridade 65, opcional) e aviso no motivo ("você está perto de precisar do Prático").
- Métricas novas: `necessidades`, `forca_da_recomendacao`, `instaveis_marcados_no_limite_pct`.
- Revisão de código: 4 achados, todos corrigidos.
- Vault: **glossário** e **dicionário de funções** (todas as funções dos 8 arquivos), mais as notas 02 e 09 refeitas.

## Resultado
| | Antes | Depois |
|---|---|---|
| Planos | Prático 68 · Total 38 · Essencial 32 | Prático 66 · Total 38 · Essencial 34 (mudaram só os 2 de veraneio) |
| RC familiar adicional | 52 | 93 |
| Força dita | — | clara 124 · no limite 14 |
| Caso instável (±5%) marcado | — | 100% |
| Testes | 105 | **111** |

## Como conferir
```bash
python -m pytest -q
python motor/gerar.py --entrega
```

## Frase para o pitch
> "Não somamos pontos: perguntamos do que o cliente precisa. Quem paga aluguel precisa da perda de aluguel, e por isso o Total. Quem tem o que perder num roubo precisa do Prático. Quem mora colado no vizinho precisa da RC. E quando a decisão é por pouco, dizemos isso e perguntamos."
