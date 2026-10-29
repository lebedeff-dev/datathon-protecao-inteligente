---
tags: [projeto, assertividade, dados-faltantes, formulas, documentacao]
atualizado: 2026-10-28
---
# 🎯 11 · A assertividade de cada cálculo (explicada do zero)

> [!abstract] Em uma frase
> Quando falta um dado, o motor **calcula** o que falta. Esta nota mostra, para cada cálculo: **a fórmula**, **como chegamos nela**, **a conta feita num cliente real** e **quanto ela acerta**, medido contra o valor verdadeiro.

**Onde está no código:** `motor/assertividade.py` mede tudo; `motor/motor.py` usa os cálculos. O resultado sai em `entrega/assertividade.json` e em `metricas.json` (chave `assertividade`). **155 testes** garantem os números (`tests/test_assertividade.py`).

---

## 0. Antes de tudo: 7 palavras que aparecem nesta nota

| Palavra | O que quer dizer | Exemplo |
|---|---|---|
| **Mediana** | O valor do meio quando você põe todos em fila. Metade fica abaixo, metade acima. Usamos mediana, e não média, porque um valor absurdo não a puxa. | Áreas 50, 60, 70, 80 e 900 m²: a **média** é 232 m² (puxada pelo 900); a **mediana** é 70 m². |
| **Percentil** | O valor que deixa uma certa porcentagem abaixo dele. O percentil 9 deixa 9% abaixo; o 91 deixa 91% abaixo. | Entre 100 imóveis em fila, o percentil 25 é o 25º. |
| **Erro percentual** | Quanto a estimativa errou, em proporção do valor real. | Real 100 m², estimado 115 m²: erro de 15%. |
| **Erro mediano** | A mediana dos erros: metade dos imóveis errou menos que isso. | Erro mediano de 14%: em metade dos imóveis, o erro foi menor que 14%. |
| **"Chute"** | O pior método que ainda é honesto: dar a todo mundo o valor do meio da base. Todo cálculo é comparado com ele. | Dizer que todo imóvel tem a área mediana da base. |
| **Gabarito** | O valor verdadeiro, para conferir a estimativa. | A área **cadastrada** é o gabarito da área **estimada**. |
| **Validação cruzada em 5 dobras** | A "prova com gabarito escondido" (abaixo). | — |

### A prova com gabarito escondido (validação cruzada em 5 dobras)
Imagine um professor que quer saber se um aluno **aprendeu** ou só **decorou**. Ele não pode dar na prova as mesmas questões dos exercícios.

1. Pegamos os **1.016 imóveis** da base de desenvolvimento que **têm** a área cadastrada (o gabarito).
2. Sorteamos esses imóveis em **5 grupos** de ~203 (as "dobras"). O sorteio tem semente fixa (`SEMENTE = 0`), então sai igual toda vez.
3. **Rodada 1:** o motor aprende com os grupos 2, 3, 4 e 5 (por exemplo, quanto custa o IPTU por m² em cada cidade) e estima a área do grupo 1, **sem ver** a área verdadeira. Depois comparamos com o gabarito.
4. Repetimos com cada grupo fazendo a prova uma vez (5 rodadas).
5. No fim, **todos os 1.016 imóveis** foram estimados por um motor que **nunca os tinha visto**. É assim que bancos validam modelos de estimativa.

> [!info] Por que 5 e não 2?
> Antes medíamos com 2 metades. Com 5 dobras, o motor aprende com 80% da base em vez de 50% (fica mais parecido com o motor de verdade, que aprende com 100%), e o resultado varia menos com o sorteio.

---

## 1. A resposta curta (o "boletim" de cada cálculo)

| O que falta | Casos no teste (de 138) | Acerto medido | O chute | Veredito |
|---|---|---|---|---|
| **Área** (IPTU + luz) | **92** | erro mediano **14,1%**; **65%** a menos de 20% da área real; a faixa contém a área real em **81%** | erro 44,4%; 26% a menos de 20% | ✅ **3× melhor** que o chute |
| Área sem IPTU nem luz (região) | 0 | erro mediano 30,3% | 44,4% | 🟡 reserva |
| **Padrão** pelo IPTU/m² | **25** | classe exata **51%**; intervalo de 2 classes **97,8%** | 63% ("normal" sempre) | ⚠️ por isso é **intervalo** |
| **Área × padrão** (sem área e sem padrão) | **64** | faixa **1,76×** contendo o real em **88%** | pior caso: 2,7× (98%) | ✅ faixa 35% mais estreita |
| **Tipo** | 138 | as duas fontes concordam em **100%** (2.578 de 2.578) | — | ✅ sem gabarito, 2 fontes batem |
| **Vínculo** | 138 | observado nas contas em 51%; 0 conflitos | — | 🟡 "provável quitado" = ausência de sinal |
| **Uso** | 31 | **não dá para medir** | — | 🔴 vira pergunta (RN-19) |
| **Bens** | 138 | **não há gabarito**; compras × bens cadastrados concordam (0,63) | — | 🟡 mínimo comprovado; máximo é premissa |
| Bens sem compras (região + renda) | 0 | erro mediano **22,3%** | 40,0% (só região) | ✅ reserva |
| CEP agregado | — | explica 21,5% da variação; um CEP **sorteado** explica 22,3% | — | ❌ descartado (ruído) |

**O que isso quer dizer:** na base de teste, o que falta de verdade é a **área** (92 casos), o **padrão** (98 casos) e a confirmação de que o cliente **mora** no imóvel (31). Nenhum imóvel do teste está sem IPTU, sem conta de luz, sem compras ou sem renda. As reservas (região, renda) existem para a base real do banco, e também estão medidas.

---

## 2. A área do imóvel (92 dos 138 casos)

### O problema
67% dos imóveis do teste não têm área cadastrada. Sem área, não dá para saber quanto custa reconstruir a casa.

### A ideia (como chegamos nela)
Quem tem casa maior paga **mais IPTU** (a prefeitura cobra por m²) e gasta **mais luz** (mais cômodos, mais aparelhos). Então dá para "voltar" do valor pago para a área. Antes de decidir, **testamos cada sinal sozinho** nos 1.016 imóveis com gabarito:

| Sinal | Quanto acompanha a área (correlação, 0 a 1) | Erro mediano sozinho |
|---|---|---|
| IPTU | **0,86** | 19,0% |
| Conta de luz | **0,80** | 22,2% |
| Condomínio (só 384 pagam) | 0,83 | — |
| Conta de água | 0,50 | 34,5% |
| Renda | 0,01 | — |
| Internet | -0,03 | — |

**Decisão:** usar **IPTU e luz**, porque são os dois mais fortes e **todo** imóvel tem os dois. Água é fraca; renda e internet não têm nada a ver com área. Condomínio é forte, mas só 38% pagam.

### A fórmula, passo a passo
**Passo 1 · Quanto custa 1 m² de IPTU e de luz em cada cidade.** Nos imóveis com área cadastrada, dividimos o IPTU pela área e pegamos a **mediana por cidade**. Fazemos o mesmo com a luz. Usamos a mediana para que um imóvel com IPTU isento ou uma mansão não puxem o valor.

**Passo 2 · Duas estimativas da área.**
- Pelo IPTU: `área = IPTU anual ÷ R$ de IPTU por m² da cidade`
- Pela luz: `área = luz mensal ÷ R$ de luz por m² da cidade`

**Passo 3 · Juntar as duas com pesos 0,6 (IPTU) e 0,4 (luz), em média geométrica:**
`área = (área pelo IPTU)^0,6 × (área pela luz)^0,4`

**Passo 4 · A faixa:** `mínimo = área × 0,75` e `máximo = área × 1,32` (ver abaixo de onde vêm).

### A conta num cliente real (`IMO_CASO_00001_01`, casa em condomínio em Recife)
| | Valor |
|---|---|
| IPTU do cliente | R$ 3.350 por ano |
| Luz do cliente | R$ 700 por mês |
| IPTU por m² em Recife (mediana) | R$ 11,28 |
| Luz por m² em Recife (mediana) | R$ 3,22 |
| **Área pelo IPTU** | 3.350 ÷ 11,28 = **297 m²** |
| **Área pela luz** | 700 ÷ 3,22 = **218 m²** |
| **Área final** | 297^0,6 × 218^0,4 = **262 m²** |
| **Faixa** | 262 × 0,75 = **197 m²** até 262 × 1,32 = **345 m²** |

### De onde veio cada número
- **Pesos 0,6 e 0,4.** No começo foi escolha nossa: o IPTU acompanha mais a área (0,86 contra 0,80) e erra menos sozinho (19% contra 22%), então ganhou peso maior. Depois **deixamos o computador escolher os pesos sozinho**: ele testa todas as combinações e fica com a que erra menos (isso se chama **regressão**). Resultado: **0,59 para o IPTU e 0,42 para a luz**. Praticamente os nossos 0,6 e 0,4. A escolha foi confirmada pelos dados.
- **Por que média geométrica, e não a média comum.** A média comum soma: com IPTU dizendo 100 m² e luz dizendo 200 m², dá 0,6 × 100 + 0,4 × 200 = **140 m²**. A geométrica multiplica: 100^0,6 × 200^0,4 = **132 m²**. A diferença: os erros de área são **proporcionais** ("errou 20%"), não fixos ("errou 20 m²"), e a média geométrica faz o meio-termo em proporção. Medimos: o erro mediano caiu de **15,0% para 14,1%**. A explicação muda uma palavra e o resultado melhora, então trocamos.
- **Por que não colocar água e tipo também.** Testamos: o erro cai de 14,1% para 13,4%, menos de 1 ponto, e a fórmula fica com 5 pesos difíceis de explicar à banca. Não vale a troca.
- **Faixa 0,75 a 1,32.** Para cada imóvel com gabarito, calculamos `área real ÷ área estimada`. Se der 1,10, o real era 10% maior. Colocamos essas razões em fila e pegamos os **percentis 9 e 91**. Assim, a faixa contém a área real em cerca de **80%** dos imóveis, a meta. Por que 9 e 91, e não 10 e 90: com 10 e 90, a faixa acertava 78,3% fora da amostra; com 9 e 91, passou de 80% (`P.AREA_QUANTIS`).
- **Sem IPTU, ou com IPTU zerado (isento):** usa só a luz, com peso inteiro. Antes, um IPTU isento "puxava" a área para baixo em 60%; foi corrigido.

### Quanto acerta (validação em 5 dobras, 1.016 imóveis)
| Método | Erro mediano | A menos de 20% da área real | A faixa contém a área real |
|---|---|---|---|
| Chute (área mediana da base para todos) | 44,4% | 26% | — |
| Mediana da região (cidade + tipo) | 30,3% | 31,5% | — |
| Só IPTU | 19,0% | 52% | 82% |
| Só luz | 22,2% | 46,5% | 81% |
| **O motor (IPTU 0,6 + luz 0,4, geométrica)** | **14,1%** | **65,4%** | **81,0%** |

**Em português:** em **2 de cada 3 imóveis**, a área estimada fica a menos de 20% da real. Isso aparece no texto do cliente: *"a área veio do seu IPTU e da sua conta de luz, comparados aos de Recife (erro abaixo de 20% em 2 de cada 3 testes)"*. O número vem do boletim; ninguém o escreve à mão.

### O que muda para o cliente
- O motivo diz "cerca de 262 m²", nunca "262 m²" (RN-09: estimativa não é fato).
- A pergunta da área diz por que está sendo feita: *"Qual a área do seu imóvel? Estimamos de 197 a 345 m². A resposta pode mudar o valor do incêndio em até R$ 148 mil."*

### A reserva: sem IPTU e sem luz (0 casos no teste)
Usa a **mediana da área** de imóveis parecidos, em degraus: mesma cidade e mesmo tipo → mesma cidade → mesmo estado → base inteira. Um degrau só vale com pelo menos **20 imóveis** (`REGIONAL_MIN_IMOVEIS`), para não tirar mediana de 3 casas. Erra 30,3%: melhor que o chute (44,4%), pior que os sinais. Faixa de ±30%, e confiança **baixa**.

---

## 3. O padrão construtivo (25 casos usam o IPTU; 64 ficam na faixa calibrada)

### O problema
O padrão (econômico, normal, superior) muda o custo de reconstruir. 98 dos 138 imóveis não têm o padrão cadastrado.

### Os fatores (premissa do time)
| Padrão | Fator | Leitura |
|---|---|---|
| Econômico | 0,85 | 15% mais barato que o normal |
| Normal | 1,00 | o custo oficial (SINAPI/CUB) |
| Superior | 1,30 | 30% mais caro |

### A ideia: o IPTU por m² diz algo sobre o acabamento
A prefeitura cobra mais IPTU por m² de imóvel de alto padrão. Então comparamos o **IPTU por m² do imóvel** com o **da cidade**: `IPTU relativo = (IPTU ÷ área) ÷ mediana da cidade`. Só funciona com **área cadastrada**. Se a área foi estimada pelo próprio IPTU, a conta seria circular (o IPTU explicaria a si mesmo).

### Como chegamos nos cortes 0,90 e 1,15
Nos 273 imóveis com área **e** padrão cadastrados, olhamos o IPTU relativo de cada padrão:

| Padrão real | 25% mais baixos até | Mediana | 75% mais baixos até |
|---|---|---|---|
| Econômico | 0,72 | **0,81** | 0,96 |
| Normal | 0,83 | **0,98** | 1,13 |
| Superior | 1,15 | **1,35** | 1,51 |

As faixas se **sobrepõem**: um normal pode ter 0,85 e um econômico também. Então o IPTU **não** consegue dizer o padrão exato. Mas abaixo de **0,90** quase não há superior, e acima de **1,15** quase não há econômico. Daí a regra:
- IPTU relativo **< 0,90** → econômico **ou** normal (fator 0,85 a 1,00);
- IPTU relativo **> 1,15** → normal **ou** superior (fator 1,00 a 1,30);
- entre os dois → não estreita (0,85 a 1,30).

### A conta num cliente real (`IMO_CASO_00002_01`, apartamento em São Paulo)
95 m² cadastrados, IPTU de R$ 2.150 → 2.150 ÷ 95 = **R$ 22,63 por m²**. Mediana de São Paulo: R$ 18,44. **IPTU relativo = 22,63 ÷ 18,44 = 1,23** → acima de 1,15 → **não é econômico** → fator de 1,00 a 1,30.

### Quanto acerta (5 dobras, 273 imóveis)
| Pergunta | Resultado |
|---|---|
| Se o IPTU tentasse dizer o padrão **exato** | acerta **51%** (o chute "todo mundo é normal" acerta **63%**) ❌ |
| O **intervalo** de 2 padrões que o motor usa | estreita **182** dos 273; o padrão real fica dentro em **97,8%** ✅ |

**Conclusão honesta:** se usássemos o IPTU para "adivinhar" o padrão, seríamos piores que um chute. Por isso o motor usa o IPTU só para **descartar um extremo**, o que ele faz com segurança.

---

## 4. Área × padrão: quando faltam os dois (64 casos)

### O problema (que a medição revelou)
A reconstrução é `área × padrão × custo do m²`. Quando faltam a área **e** o padrão, o motor antigo pegava o **pior caso de cada um**:
> menor área × padrão econômico … até … maior área × padrão superior

No cliente de Recife: 197 × 0,85 = **167 m² de padrão normal** até 345 × 1,30 = **448**. Com o custo, a reconstrução ia de **R$ 310 mil a R$ 961 mil**: o máximo era **3,1 vezes** o mínimo. Para o cliente, uma faixa assim diz pouco.

### Por que o pior caso exagera
A área e o padrão quase nunca erram **para o mesmo lado ao mesmo tempo**. Além disso, o IPTU já carrega o padrão (casa de alto padrão paga mais por m²), então a estimativa da área pelo IPTU já "puxa" na direção certa.

### Como chegamos na faixa nova
1. Nos 273 imóveis com área e padrão cadastrados, calculamos o valor real de `área × fator do padrão` (o que de fato multiplica o custo do m²).
2. Comparamos com `área estimada × 1,05` (1,05 é o padrão do meio: √(0,85 × 1,30) = 1,05).
3. A razão `real ÷ estimado` em fila, fora da amostra, deu percentis 9 e 91 de **0,73 e 1,21**.
4. **Correção da revisão de código:** a faixa nunca pode ficar **mais estreita** que a de quem tem padrão **normal** cadastrado. Quem sabe menos não pode receber um teto menor. Então a faixa é a **união** das duas.
5. Nesta base, a união coincide com a **faixa da área com padrão normal** (0,75 a 1,32 da área). Ou seja: a faixa da área já cobre a variação do padrão.

| Faixa de área × padrão | Contém o valor real | Largura (máximo ÷ mínimo) |
|---|---|---|
| Pior caso (antes) | 97,8% | **2,70×** |
| **Calibrada (agora)** | **88,3%** | **1,76×** |

### A conta no cliente de Recife
- Área × padrão: de **197 a 345** m² de padrão normal (antes: 167 a 448).
- Custo do m² em Pernambuco: R$ 1.888 (SINAPI, o mínimo) a R$ 2.145 (o máximo, pela razão CUB/SINAPI).
- **Reconstrução: 197 × 1.888 = R$ 371 mil até 345 × 2.145 = R$ 740 mil** (antes: R$ 310 mil a R$ 961 mil).
- É casa em condomínio (segundo risco): o seguro dele paga os **acabamentos**, 25% a 40% da reconstrução, mais os bens. **Incêndio: de R$ 141 mil a R$ 427 mil** (antes: R$ 126 mil a R$ 516 mil).
- No CSV, a regra diz exatamente isso: *"área × padrão 197–345 m² de padrão normal (área estimada 262 m², padrão desconhecido; faixa calibrada de área × padrão: contém o valor real em 88% dos testes fora da amostra) × R$ 1.888–R$ 2.145/m²…"*

---

## 5. O tipo do imóvel (138 casos, sempre conferido)
**Fórmula:** o termo "apartamento" no endereço → apartamento; "condomínio" → casa em condomínio; senão, casa. Depois **conferimos com o complemento** ("AP", "APTO", "BLOCO", "TORRE" contra "CASA", "LOTE", "QUADRA", "SOBRADO", "FUNDOS").
**Quanto acerta:** não existe gabarito do tipo. O que medimos é se **duas fontes independentes concordam**: o termo e o complemento batem em **100%** (2.578 de 2.578). Se discordarem, a confiança cai para média e entra a pergunta "É apartamento ou casa?".

## 6. O vínculo (inquilino, financiado, dono)
**Fórmula, em ordem:** paga aluguel → inquilino; paga parcela de financiamento → financiado; recebe crédito de aluguel e o imóvel não é o endereço principal → dono que aluga; nenhum sinal → **provável quitado**.
**Quanto acerta:** sem gabarito. Medimos que é **observado nas transações** em 51% da base de desenvolvimento, e que **nunca** aparece aluguel e financiamento juntos (0 conflitos). Os 40% sem sinal são "provável quitado": é **ausência de prova**, não prova. Por isso o texto diz "não há aluguel nem financiamento nas suas contas", e não "o imóvel é seu".

## 7. O uso (mora, veraneio ou alugado; 31 casos sem o endereço principal)
**Fórmula:** endereço igual ao principal → mora; crédito de aluguel → alugado; o cliente mora em outro imóvel → veraneio; senão → **pergunta obrigatória**.
**Quanto acerta:** **não dá para medir.** Tentamos uma ideia: casa vazia gasta menos luz. Medimos a luz em relação à cidade: imóvel principal = **1,00**, não principal = **1,00**. Nenhuma diferença. A luz não serve para isso nesta base. Então não inventamos: vira pergunta (RN-19).

## 8. Os bens (138 casos)
### A fórmula
- **Mínimo** = o maior entre (compras de móveis, eletrodomésticos e eletrônicos nos últimos 36 meses) e (bens cadastrados ligados ao imóvel), **corrigido pela inflação**.
- **Máximo** = **2,7 × compras** de 36 meses, corrigido pela inflação.

### A conta no cliente de Recife
Compras de 36 meses: R$ 18.250 (móveis) + R$ 12.000 (eletrodomésticos) + R$ 15.150 (eletrônicos) = **R$ 45.400**.
- Correção pela inflação: IPCA dos últimos 12 meses = 4,58% → fator = 1,0458^1,5 = **1,069**.
- **Mínimo** = 45.400 × 1,069 = **R$ 48,6 mil**.
- **Máximo** = 2,7 × 45.400 × 1,069 = **R$ 131 mil**.

### De onde veio cada número
- **Por que ^1,5 na inflação:** as compras se espalham pelos 36 meses. Em média, uma compra foi feita há **18 meses = 1,5 ano**. Então corrigimos 1,5 ano de inflação.
- **Por que 2,7:** a casa tem mais coisas do que as compradas nos últimos 3 anos. Se a pessoa compra no mesmo ritmo e as coisas duram ~8 anos, o que ela tem é cerca de 8 anos de compras: 8 ÷ 3 = **2,67 ≈ 2,7** vezes as compras de 3 anos. **É uma premissa**: não há dado para medir quanto vale o que está dentro de uma casa.
### Quanto acerta
**Não há gabarito** do valor dos bens. O que medimos: as **compras** e os **bens cadastrados** ligados ao imóvel concordam. A correlação de postos é **0,63** (0 = nada a ver; 1 = mesma ordem). Quem compra mais também tem mais bens cadastrados. O mínimo é **comprovado** (está nas contas). O máximo é premissa, e o texto diz "pelo menos R$ 49 mil" quando o argumento usa o mínimo.

### A reserva: sem compras e sem bens (0 casos no teste)
Mediana das compras de imóveis parecidos (cidade + tipo → cidade → estado), **combinada com a renda** por média geométrica, presa entre metade e o dobro da região (para a renda nunca decidir sozinha: RN-08, D-08). Fingimos que 2.578 imóveis não tinham compras e estimamos: **só a região erra 40,0%; região + renda erra 22,3%**. A renda corta o erro quase pela metade.

## 9. O CEP agregado (descartado)
**A ideia da mentoria:** usar a média do bairro (CEP) quando falta dado.
**O teste:** se o CEP tem informação, ele deve explicar o IPTU por m² **melhor que um CEP sorteado ao acaso**. Resultado: o CEP real explica **21,5%** da variação; um CEP **sorteado** explica **22,3%**. Ou seja, o CEP desta base é **ruído** (a base avisa que ele é fictício; RN-10). Fica desligado (`USAR_CEP = False`) e pode ser ligado com CEP real.

---

## 10. Como conferir sozinho
```bash
python -m pytest -q tests/test_assertividade.py    # os boletins e a faixa calibrada
python motor/gerar.py                              # grava motor/saida/assertividade.json
```
Ligações: [[02 - O motor passo a passo]] · [[03 - Cada métrica explicada]] · [[12 - O motivo feito para você]] · [[10 - Dicionário de funções]] · [[Plano - assertividade e motivo feito para você]]
