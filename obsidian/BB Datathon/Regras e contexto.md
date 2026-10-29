---
tags: [regras, contexto]
atualizado: 2026-10-27
---
# Regras e contexto

Nota viva. Fonte principal: [[Guia oficial do datathon]]. Quando algo mudar, atualizo aqui primeiro.

> **As 51 regras que não podem ser quebradas estão em [[Regras de negócio]]. Toda ideia passa por elas antes de entrar.**

## O desafio (oficial)
- Datathon **Proteção Inteligente**. O guia oferece dois desafios; o nosso pacote é o **Seguro Residencial**.
- Fluxo: **sinais → sugestão inicial → confiança → confirmação → recomendação**.
- Canais: o guia dá como **exemplos** One Click Buy, atendimento assistido (gerente/central) e futuros agentes autônomos. **Nenhum é obrigatório**; o que é obrigatório é a lógica ser reaproveitável. Ver [[Onde está a inovação]].
- Saída por cliente + imóvel: elegibilidade, tipo/uso/vínculo, plano (Essencial, Prático, Total), coberturas com faixa mín./máx., [[Grau de confiança]], [[Perguntas de confirmação]] e [[Motivo da recomendação]], com alternativas.
- Não é obrigatório usar machine learning.

## Guardrails do guia
- Só dados fornecidos e fontes externas públicas ou autorizadas, documentadas.
- [[Elegibilidade residencial]] antes de recomendar.
- **Idade e dados sensíveis não podem ser atalho para risco ou patrimônio.** A renda foi liberada na mentoria do BB (28/10): pode entrar como reforço, combinada com outros sinais ([[Regras de negócio]], RN-07 revisada).
- Estimativa nunca aparece como fato confirmado.
- Recomendação explicável, revisável e com confirmação humana.

## Entrega: 29/10 até 10h (obrigatória para apresentar)
- [[Templates de entrega]] para os 138 imóveis do teste comum, com todas as coberturas fixas do plano. Valores só com números.
- README com equipe, desafio, arquitetura, execução, premissas, limitações, métricas, resultados e **uso de IA**.
- Código, `requirements.txt` e versão do Python.
- Vídeo de até 5 min. No dia: 5 min de pitch + 5 min de perguntas.
- Pesos da nota em [[Critérios de avaliação]].

## O que a apresentadora reforçou (áudio)
- [[Jornada do cliente]] **e** [[Jornada do gerente]].
- O motivo é o ponto principal.
- [[Personalizar sem decidir pela pessoa]], poucas perguntas, [[Alternativas comparáveis]].
- **Equilíbrio:** rápido, mas o cliente entende o que assina e o gerente sabe explicar o pós-venda. Ver [[Ideias de equilíbrio]].

## Foco (28/10)
- O foco é motor + planilhas dos 138 casos. O app é só a demonstração. Plano: [[Plano de preenchimento das planilhas]].
- Crianças e pets (revisado em 28/10, slide 14): só como **necessidade informada pelo cliente** para RC familiar. Crianças e pet juntos somam 1 ponto ao Total; só um dos dois vira pergunta. Nunca mudam valor, elegibilidade, canal ou confiança. Idade segue fora de tudo (RN-07); a renda só reforça os bens de quem não tem compras (D-08).
- Cliente com seguro BB e um imóvel só = NAO elegível. Com dois imóveis = SIM + pergunta "qual já tem seguro?".
- Confiança: o nível sai de **regra** sobre a classe de cada dado crítico (observado, estimado, presumido), nunca de corte numa nota (com corte, 101 de 138 casos ficavam na borda). CUB só entra se for oficial.
- Correções aplicadas no motor do Pedro: [[Correções P1-P5 no motor]].

## App (decidido em 28/10)
- App da demo = simulação dentro do app do BB, ligada ao motor (nunca número à mão), com botões A/B/C, modo raio-X e tela do gerente. Não criar app separado. Plano: [[Especificação do app v2 - ligado ao motor]].

## Regras do grupo e deste chat
- Tudo sai no nome do Matheus. Nada de menção a IA em commits, issues ou textos da equipe.
- Uso de IA: declaração curta no README (exigência do guia), decidida em 27/10. Fora isso, nenhuma menção a IA em commits, issues ou mensagens.
- Texto do repositório simples e direto, com cara de projeto de aluno.
- Não adiantar planejamento no quadro de tarefas.
- Este vault é o cérebro completo e fica só no computador do Matheus. A equipe usa GitHub e Drive.
- Os dados do datathon são sintéticos e ficam no repositório privado (`data/raw/`). Arquivo gerado não sobe.
- Dados externos só de fontes oficiais, com fonte, data de acesso, licença, método e limitações.
- Termos técnicos explicados no [[Stack e glossário]].
- Design do MVP segue as [[Regras de design BB]].
- Antes de cada tarefa, ler esta nota.

## Onde está cada coisa
- Código e dados: [repositório](https://github.com/matfsouza/datathon-bb-seguro-residencial)
- Quadro (vazio): [GitHub Projects](https://github.com/users/matfsouza/projects/1)
- Briefing: [[Desafio - resumo]], [[Guia oficial do datathon]], [[Transcrição da apresentação]]
- Dados: [[Dicionário de dados]], [[Achados iniciais dos dados]]
- Em debate agora: [[Jornada dentro do app - ideias v3]] (tudo dentro do app do BB; sair só para suporte)
- Ideias: [[Ideias v2 - proposta para o time]] (atual), [[Ideias descartadas ou adiadas]], [[Métricas de bancos e seguradoras]]
- Design: [[Regras de design BB]], [[Catálogo do Seguro Residencial BB]]
