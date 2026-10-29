---
tags: [plano, recomendacao, motor, documentacao]
data: 2026-10-29
status: aprovado e executado em 29/10
---
# 🎯 Plano: recomendação por necessidades + documentação completa

> [!success] Executado em 29/10
> Planos: Prático 66 · Total 38 · Essencial 34 · RC adicional 93 · força clara 124 · no limite 14 (todos com pergunta decisiva) · 111 testes. Documentação: [[00b - Glossário (termos de seguro e de dados)]] e [[10 - Dicionário de funções]].

## 1. O problema da pontuação de hoje
| Problema | Evidência (base de teste) |
|---|---|
| Difícil de explicar: dois placares separados, com "força 2" nos dois lados | Dúvida do próprio time |
| "Mora em prédio" vale 1 ponto para o **Total**, mas sozinho nunca leva ao Total; só empurra para o **Prático**, que não cobre vizinhos | 6 Práticos dependem dessa regra |
| O risco de atingir o vizinho não é coberto: prédio ou condomínio sem família não ganha RC | **7 de 78** imóveis em prédio ficam sem RC |
| Plano decidido "por pouco", sem aviso | **27** casos a menos de 15% do limite de bens; **24** do de eletrônicos |
| Veraneio com bens altos vai para o Prático, mas o roubo não cobre casa desocupada (CG, Roubo 2.1 c) | 2 casos |

## 2. A decisão: três necessidades, cada uma resolvida pela cobertura certa
O motor deixa de somar pontos. Ele faz **três perguntas sobre o cliente**, e cada resposta "sim" vem com a **prova** (o dado) e a **cobertura que resolve**:

| Necessidade | Quando é "sim" | Cobertura que resolve | Onde ela está |
|---|---|---|---|
| **A · Aluguel em jogo** | Paga aluguel deste imóvel **ou** recebe aluguel dele | Perda de aluguel | Só no **Total** |
| **B · Roubo e vidros** | Bens comprovados ≥ R$ 36 mil **ou** eletrônicos ≥ R$ 10 mil **ou** gastou com vidraçaria. **Não conta** em imóvel de veraneio (o roubo não cobre casa desocupada) | Roubo e quebra de vidros | **Prático** e Total |
| **C · Danos a terceiros** | Mora em prédio ou condomínio (o vizinho está colado) **ou** tem dependentes ou pet | RC familiar | No Total; nos outros, **adicional** |

**O plano é o menor que cobre as necessidades:**
- tem A → **Total** (já cobre B e C);
- senão, tem B → **Prático**, + RC adicional se tiver C;
- senão → **Essencial**, + RC adicional se tiver C.

Renda, idade, dependentes e pet **nunca** mudam o plano. Dependentes e pet só acendem a necessidade C.

## 3. Mais assertivo: a força de cada recomendação
Cada necessidade ganha uma **força**:
- **Clara:** a prova é observada (transação ou cadastro) e está a mais de 15% do limite. Ex.: paga R$ 3 mil de aluguel; tem R$ 49 mil em bens.
- **No limite:** o valor está a menos de 15% do limite, para cima ou para baixo. Ex.: R$ 9.411 em eletrônicos contra o limite de R$ 10 mil.

**Quando a recomendação está no limite:**
1. o motor faz a **pergunta que decide o plano** ("Seus eletrônicos (TV, notebook, celulares) passam de R$ 10 mil?"), à frente das perguntas de valor;
2. o motivo diz isso com franqueza ("você está perto de precisar do Prático"; ou o contrário);
3. a ficha marca `forca: "no_limite"`, e o gerente vê isso no relatório.

**Os limites continuam R$ 36 mil e R$ 10 mil** (medianas da base de desenvolvimento, ou seja, "mais que a metade das casas"). Não temos dado de sinistro ou de preço para um limite atuarial. A faixa de ±15% assume essa incerteza em vez de esconder.

## 4. Impacto esperado
| O quê | Hoje | Depois (estimativa a confirmar) |
|---|---|---|
| Planos | Prático 68 · Total 38 · Essencial 32 | Quase iguais: muda o veraneio (2 casos) |
| RC para quem mora em prédio | 71 de 78 | **78 de 78** |
| Recomendação com a força dita | 0 | **100%** (clara ou no limite) |
| Pergunta que decide o plano | não existe | nos casos no limite (cerca de 45) |
| Motivo | sinais soltos | "Você precisa de X porque [prova]; quem resolve é Y" |

A **personalização** continua nos valores (cada faixa sai dos números do cliente) e no texto. O plano responde "de que **tipo** de proteção você precisa".

## 5. Tarefas
| # | Tarefa | Arquivos | Teste que prova |
|---|---|---|---|
| 1 | `avaliar_necessidades(r, tipo, vinculo, uso, bens)` → lista de necessidades (código, sim/não, prova, força, cobertura que resolve) | `motor/motor.py` | inquilino → A forte; R$ 9.411 em eletrônicos → B no limite; prédio sem família → C; veraneio com bens altos → B não conta |
| 2 | `escolher_plano` passa a usar as necessidades (menor plano que cobre); mantém os campos que o protótipo lê (`motivos_plano`, `por_que_nao_*`, `alternativa`) | `motor/motor.py` | 136 dos 138 planos iguais; os 2 de veraneio viram Essencial; justiça = 0 |
| 3 | RC adicional para prédio e condomínio mesmo sem família | `motor/motor.py` | 78 de 78 com RC |
| 4 | Pergunta decisiva quando a recomendação está no limite (prioridade 65, opcional) | `motor/motor.py` | caso de R$ 9.411 recebe "Seus eletrônicos passam de R$ 10 mil?" |
| 5 | Motivo por necessidade, com a força ("perto de precisar") | `motor/motivo.py` | 0 motivos genéricos; 100% com prova; tamanho até 130 palavras |
| 6 | Métricas: `forca_da_recomendacao` (clara × no limite), `necessidades` (quantos com A, B, C), estabilidade (todo caso que muda com ±5% está marcado "no limite") | `motor/metricas.py` | métrica sai; os instáveis ⊂ os marcados |
| 7 | Regenerar, revisar o código (`code-review`), conferir (`verification-before-completion`), commit e push | — | 0 erros; reprodutível |

## 6. A documentação no Obsidian (para quem não sabe nada)
Reescrever a pasta **16 - Projeto por inteiro** no nível "nunca vi o projeto":
| Nota | O que terá |
|---|---|
| **00 · Comece aqui** | O que é o datathon, o problema, a solução em 5 frases e a ordem de leitura |
| **00b · Glossário** (nova) | Termos de seguro (importância segurada, sinistro, primeiro e segundo risco, RC, franquia, subseguro, ITV) e de dados (mediana, percentil, backtest, API, CSV) com exemplos |
| 01 · Dados | Cada tabela e campo usado, o que fazemos quando falta (revisada) |
| 02 · O motor passo a passo | A **nova** recomendação por necessidades, explicada com exemplos |
| 03 · Métricas | Cada métrica com "o que é, conta, valor, por que importa" (revisada) |
| 04–08 | Revisadas com os números novos |
| 09 · Conta por conta | Os dois casos refeitos com a lógica nova |
| **10 · Dicionário de funções** (nova) | **Todas as funções** dos 8 arquivos Python. Para cada uma: o que faz em uma frase, o que recebe, o que devolve, um exemplo com número e por que existe (que regra atende) |

## 7. Skills
| Etapa | Skill | Por quê |
|---|---|---|
| Plano | `writing-plans` | Este documento |
| Código | `test-driven-development` | Cada regra nova nasce de um teste |
| Texto do motivo | `copywriting` | Necessidade + prova + solução, sem jargão |
| Documentação | `better-writing` | Português claro para leigos |
| QA | `code-review` + `verification-before-completion` | Revisar o diff e provar com números antes de dizer "pronto" |

Ligações: [[02 - O motor passo a passo]] · [[09 - Cada escolha conta por conta]] · [[08 - Perguntas da banca e respostas]]
