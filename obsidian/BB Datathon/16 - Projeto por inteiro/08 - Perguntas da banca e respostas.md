---
tags: [projeto, banca, pitch, qa]
atualizado: 2026-10-29
---
# 🎤 08 · Perguntas da banca e respostas

Para estudar e saber de cor. Cada resposta traz o número que a sustenta. Quando a crítica **procede**, está marcado e há uma correção proposta.

> [!info] Legenda
> ✅ a crítica não procede (temos resposta) · 🟡 procede em parte · 🔴 procede (corrigir ou assumir como limitação)

---

## Parte 1 · Perguntas do time

### "O valor da casa usa o m² de quê? Da área danificada?"
**Não.** Usa a **área do imóvel inteiro**, porque a faixa do incêndio é a **importância segurada**: o máximo que o seguro paga se a casa for **toda** destruída (perda total). Antes do sinistro, ninguém sabe quanto vai ser danificado.
- **Na hora do sinistro**, o seguro paga o **dano real** (o conserto da parte atingida), até esse máximo. É o "primeiro risco absoluto" das Condições Gerais (cl. 15.1): não há rateio, paga o prejuízo até o limite.
- **Exemplo:** uma casa de 127 m² em Porto Alegre custa cerca de R$ 394 mil para reconstruir. Se um incêndio queima só a cozinha (R$ 40 mil de conserto), o seguro paga R$ 40 mil. Se queima tudo, paga até o limite contratado.
- **Por isso o motor estima a área inteira:** se ela for subestimada, o limite fica baixo e a perda total não é coberta (subseguro).

### "Como funciona a validação pelo IPTU e pela energia?"
1. **Aprender** (base de desenvolvimento, 1.016 imóveis com área cadastrada): em cada cidade, quanto se paga de IPTU por m² e de luz por m². Ex.: se em Curitiba a mediana é R$ 20/m² de IPTU por ano, um IPTU de R$ 2.200 indica cerca de 110 m².
2. **Estimar** quem não tem área: área = 0,6 × (IPTU ÷ IPTU/m² da cidade) + 0,4 × (luz ÷ luz/m² da cidade). O IPTU pesa mais porque é calculado sobre a área.
3. **Faixa:** a estimativa × [0,74 e 1,28] (os percentis de 9% e 91% do erro).
4. **Validar sem roubar:** escondemos a área de imóveis que **têm** área e comparamos.
   - Base de desenvolvimento, em duas metades: erro mediano de **15%**; a faixa contém a área real em **80,9%**.
   - **Base de teste, nunca usada para calibrar** (46 imóveis com área): erro mediano de **16,9%**; a faixa contém a real em **73,9%** (34 de 46; amostra pequena, margem de cerca de ±13 pontos).
   - **Padrão pelo IPTU:** 97,8% na desenvolvimento e **7 de 7** na base de teste.

### "E os dados mais antigos?"
Três mecanismos:
1. **Frescor na confiança:** cada campo tem uma meia-vida (vínculo e uso: 12 meses; bens: 36; área e tipo: 120). O peso do dado é `peso da fonte × 0,5^(idade ÷ meia-vida)`. Um dado observado mais velho que a meia-vida passa a contar como **estimado** e baixa a confiança.
2. **Inflação:** as compras de 36 meses são trazidas a preço de hoje pelo IPCA (fator 1,069 = (1 + 4,58%)^1,5, no meio da janela).
3. **Limitação honesta:** a base **não traz a data de cada registro**. O motor usa a idade típica de cada sinal (transações: 3 meses; compras: 18 meses em média). Por isso, **nenhum caso** desta base foi rebaixado por idade. O mecanismo existe e tem teste; com datas reais do banco, ele passa a agir.

### "Como cada cobertura e cada motivo são escolhidos?"
- **As coberturas não são escolhidas uma a uma:** vêm do **plano** (catálogo oficial). Essencial = 6 fixas (incêndio, água, vendaval, impacto de veículos, queda de aeronave, danos elétricos); Prático = + roubo e vidros; Total = + RC familiar, perda de aluguel e despesas emergenciais.
- **O plano sai das necessidades** (desde 29/10): aluguel em jogo → Total; roubo e vidros → Prático; danos a terceiros → RC familiar. Cada necessidade tem uma prova do cliente. Explicação em [[02 - O motor passo a passo]].
- **Adicional:** a RC familiar entra em prédio ou condomínio com dependentes ou pet, quando o plano não é o Total.
- **O motivo do plano** é a prova da necessidade que decidiu, com os números do cliente. Ex.: "você gastou R$ 11 mil com vidraçaria" acendeu a necessidade de roubo e vidros, que o Prático resolve.
- **O motivo de cada cobertura** é o valor calculado + a frequência real de sinistros da BB + o dado oficial da cidade.

### "A tabela da jornada: do que se trata?"
Ela diz **por qual caminho cada cliente contrata**. As telas do app vão seguir isso:

| Caminho | O cliente vê | Exemplo real |
|---|---|---|
| **1 toque** (63) | A proposta pronta, o motivo e um botão "Contratar". As perguntas aparecem como "quer ajustar?" e são opcionais | `IMO_CASO_00005_01`: apartamento financiado em Curitiba; contrata direto |
| **App com perguntas** (37) | A proposta + 1 a 3 perguntas de sim ou não **antes** do botão. Ex.: "O seu seguro atual é da BB?", "Você mora neste imóvel?" | Se a resposta mantém o caso, contrata no app. Se muda (ex.: "o imóvel está alugado"), o motor refaz a proposta ou chama o gerente |
| **Gerente** (22) | A proposta + o botão "falar com o gerente". O gerente abre a **ficha** (relatório) com tudo pronto | Obra no imóvel (9) ou cliente que não usa o app (13) |
| **Sem nova proposta** (16) | "Você já tem o seguro da BB neste endereço" + revisão da apólice | Seguro existente |

**Onde o gerente aparece mesmo fora dos 22:** em qualquer tela há o botão de ajuda (D-02). Antes dele vem a **ajuda contextual** (as dúvidas comuns daquela tela). Se o cliente ainda pedir, o gerente recebe a mesma ficha.

### "As fontes externas em PDF são válidas?"
O guia aceita "fontes externas **públicas ou devidamente autorizadas**", desde que registradas: fonte, data de acesso, nível geográfico, método, transformação e limitação (RN-11). Um PDF **oficial** (IBGE, Sinduscon, Fipe) é fonte pública válida. Mesmo assim, **API é melhor**: atualiza sozinha e é mais fácil provar a origem. Como cada fonte está hoje:

| Fonte | Como chega | Confiabilidade | Proposta |
|---|---|---|---|
| SINAPI (IBGE) | ✅ API | Oficial | Manter |
| IPCA (Banco Central) | ✅ API | Oficial | Manter |
| ANEEL | Página oficial | Oficial | **Passar para a API** de dados abertos (testada: responde) |
| CUB (Sinduscons) | PDF ou site oficial | Oficial, sem API | Manter, ou trocar por "SINAPI × razão" sempre |
| Atlas / S2iD | Arquivo oficial (sem API) | Oficial | Manter (só texto) |
| FipeZAP | PDF | Privada (Fipe), reconhecida | Manter, ou trocar pelo aluguel do IPCA via SIDRA (é índice, não R$/m²) |
| Sinistros BB | **Matéria de jornal** com dado da BB | A mais fraca | **Tirar**, ou citar como "segundo a BB Seguros" e deixar como contexto do pitch |

---

## Parte 2 · A crítica em papel de banca (23 pontos)

### A. O que pode derrubar
1. ✅ **Corrigido em 29/10.** 16 NÃO por indício. Procede: "produto de seguridade" pode ser vida ou previdência (8 dos 16 têm só 1 produto). Isso fere a RN-19. **Correção proposta:** SIM + pergunta obrigatória "O seu seguro residencial atual é da BB?"; a demo mostra o NÃO como resposta do cliente. O plano não muda (ele já é calculado para os 16: Essencial 6, Prático 6, Total 4).
2. ✅ **Corrigido em 29/10:** agora é sugerido ÷ cenário pessimista = **0,67** (15 casos ≥ 0,8). ITV de 1,00 era circular. Procede: no incêndio, o sugerido **é** o valor em risco. **Correção:** trocar pela métrica independente "sugerido ÷ estimativa pessimista" ou tirar a afirmação.
3. 🟡 **Calibrou e avaliou no mesmo backtest.** Procede em parte. Na base de teste (nunca usada), a faixa contém a área real em **73,9%** (46 imóveis). Dizer os dois números.
4. 🟡 **Água e danos elétricos são o teto.** Os limites são premissa (sem print do app). A personalização aparece na **confiança**, no **valor sugerido** e no **texto**. **Ação:** dizer que é premissa e pedir o limite real; se houver tempo, buscar o máximo no simulador público da BB.
5. 🔴 **Material vazio tratado como alvenaria (109 casos).** Procede pela RN-09. **Correção:** uma **declaração única de elegibilidade** na contratação, para todos: "não é favela ou comunidade, não é rural, não está em obra, não é de madeira ou material combustível, não é tombado". Um toque de confirmação, sem travar o 1 toque.

### B. Coerência
6. ✅ **Corrigido em 29/10:** 1 toque puro **45,7%** dos elegíveis, sem pessoa **81,2%**. STP de 72,5% estava inflado. Procede. O 1 toque puro é **63 de 122 elegíveis (52%)**. **Correção:** mostrar os dois: "52% contratam sem nenhuma pergunta obrigatória; até 82% sem falar com uma pessoa".
7. ✅ **94 × 63.** Os 31 de diferença são: **14 não elegíveis**, **9 com pouca familiaridade com o app** (maturidade < 40: modo simples) e **8 que não usam o app**. Falta escrever isso no relatório.
8. ✅ **Tratado em 29/10:** os pontos viraram necessidades, e quem está a menos de 15% do limite é marcado "no limite" e recebe a pergunta que decide (14 casos; o único instável está entre eles). **Limiar do plano na mediana.** A mediana é escolha de produto (os bens acima de metade da carteira merecem roubo), não risco atuarial; não temos sinistralidade por faixa. Assumir como premissa e citar o caso instável (`IMO_CASO_00013_01`).
9. 🟡 **Proporções sem dado** (vendaval 10–20%, água 3–8%, RC 70 m² × 30–60%, despesas 2–5%). São premissas do time e estão em `parametros.py`. Defesa: telhado e esquadrias são uma fração da obra; RC usa o tamanho médio de um apartamento vizinho. **Ação:** citar a composição de custo por etapa do CUB, se der tempo, ou assumir como premissa.
10. ✅ **Corrigido em 29/10:** por padrão só os bens; a estrutura entra se o contrato pedir. Inquilino de casa com a estrutura no incêndio (15 casos). Procede pela D-07 e pela Lei do Inquilinato. **Correção:** por padrão, só bens; a estrutura entra se o contrato pedir (a pergunta já existe).

### C. Renda, justiça e privacidade
11. 🟡 **A renda foi liberada de forma verbal.** Precisamos do **nome do mentor e de um registro** (mensagem ou e-mail). Peçam ao Eduardo.
12. ✅ **O teste de justiça dá 0 porque ninguém usa a renda?** Na base, sim. Mas há **testes com casos sintéticos** sem compras (`test_sem_compras_renda_nao_muda_plano_nem_jornada`, `test_renda_nao_passa_de_2x_a_regiao`) que rodam o caminho da renda e provam a regra. O 22,7% é otimista para quem realmente não tem compras (está escrito no relatório).
13. ✅ **Decidido em 29/10: só RC familiar como adicional ou pergunta; a família nunca muda o plano** (planos: Prático 68 · Total 38 · Essencial 32). Família mudava o plano (18 casos). Decidir hoje. Recomendação: **só RC como adicional** (a família nunca muda o plano), o que fecha a RN-07 sem perder o slide 14.
14. 🟡 **Base legal (LGPD).** Resposta: **legítimo interesse** (art. 7º, IX e art. 10) para oferecer produto a quem já é cliente, com transparência (o app mostra de onde veio cada dado), minimização (só dados do imóvel e das contas) e direito de contestar (o cliente corrige qualquer dado e a proposta recalcula). Em produção: aviso de privacidade e opção de não receber oferta.
15. 🟡 **Renda por tabela no plano.** Testamos com a mesma faixa de bens e renda diferente: nos **bens baixos** e **altos**, o plano quase não muda com a renda. Na **faixa média**, a renda alta tem menos Essencial (4% contra 22%), porque é nessa faixa que fica o limiar de R$ 36 mil em bens: quem tem mais renda tende a ter um pouco mais de bens **dentro** da faixa. O plano segue os bens, não a renda.

### D. Jornada e conscientização
16. 🟡 **Gerente virou exceção, mas a banca disse que ele importa (RN-50).** O gerente **não sai da jornada**: recebe a ficha de **qualquer** cliente que pedir ajuda, faz o pós-venda (sinistro, assistência, renovação) e é o canal dos 22 casos. Mostrar a tela do gerente na demo.
17. 🟡 **Conscientizar sem preço.** Não temos tarifa e não vamos inventar (RN-53). No app, o preço vem do **cotador da BB** (ponto de integração). A ficha entrega o "o que muda" e o cotador entrega o "quanto custa".
18. ✅ **Corrigido em 29/10:** vidros 88% e RC 96% de textos distintos, com a área e o tipo do imóvel. Motivo genérico em vidros e RC. Procede em parte: vidros (12% de textos distintos) e RC (37%) são as coberturas que fazem subir de plano. **Correção:** usar o tipo e a área ("num apartamento de 110 m², repor box e janelas custa de R$ 2 mil a R$ 5 mil") e, na RC, o tamanho do vizinho pela área do próprio imóvel.
19. ✅ **Frase local.** **138 de 138** recebem a frase da Defesa Civil (todas as 10 capitais têm registros de chuva) e a da ANEEL.
20. 🟡 **Entendimento não é medido.** É a "checagem de entendimento" das ideias v2: no fim, uma pergunta de sim ou não sobre o que está coberto. Proposta para o app; não há métrica no motor.

### E. Entrega e operação
21. ✅ **README atualizado em 29/10.** Reprodutibilidade × `--ao-vivo`. As planilhas usam os CSVs **commitados** (SINAPI set/2026, IPCA até set/2026). Rodar o coletor muda as planilhas de propósito. **Ação:** escrever isso no README.
22. 🟡 **Viabilidade.** O motor lê tabelas que o banco já tem (cadastro, transações categorizadas, débitos de IPTU e luz). Em produção: rodada diária em lote, gravação das fichas e API para o app e o gerente. **Piloto:** 2 agências ou um % do app, comparando a conversão do 1 toque, o abandono, o esforço (CES) e, em 12 meses, a sinistralidade e a renovação.
23. 🔴 **P0:** nome da equipe no README e vídeo de 5 min. Definir quem faz e até que horas.

## Resumo para a decisão do time
| Corrigir no código (rápido) | Decidir |
|---|---|
| 1 · NÃO vira pergunta · 2 · ITV independente · 6 · STP honesto · 10 · inquilino só bens · 18 · vidros e RC com área · 21 · README · ANEEL pela API · tirar ou rebaixar os sinistros da matéria | 13 · família no plano · 11 · registro da mentoria · 5 · declaração de elegibilidade (texto) · 4 · limites reais |

Ligações: [[00 - Índice (leia nesta ordem)]] · [[07 - Regras, decisões e pendências]] · [[02 - O motor passo a passo]]
