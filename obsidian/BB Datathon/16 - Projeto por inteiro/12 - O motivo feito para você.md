---
tags: [projeto, motivo, justificativa, personalizacao, documentacao]
atualizado: 2026-10-28
---
# 💬 12 · O motivo feito para você (passo a passo)

> [!abstract] Em uma frase
> Com só 3 planos, o diferencial é o **porquê**. O motivo deixou de ser um modelo com números trocados e passou a falar da **casa**, da **cidade** e dos **números** de cada cliente, comparando-o com os vizinhos e dizendo, em reais, o que fica descoberto.

**Onde está no código:** `motor/motivo.py` (função `justificativa`). O motor só entrega os números (`motor.py`: `comparar_com_vizinhos`, `territorio`); o `motivo.py` só escreve o texto, não decide nada.

## 1. Antes e depois (medido nos 138 casos)
| Medida | Antes (27/10) | Agora | O que mede |
|---|---|---|---|
| Motivos com "esqueleto" único | 83 | **125** | O texto sem os números. Se dois motivos têm o mesmo esqueleto, são o mesmo modelo com valores trocados |
| Citam a cidade e o tipo de imóvel | **0** | **138** | "o seu apartamento de 95 m² em São Paulo" |
| Semelhança média entre dois motivos | 0,29 | **0,21** | Pedaços de 3 palavras em comum (0 = nada; 1 = iguais) |
| A frase mais repetida aparece em | **93** motivos | **32** | Antes: a da proteção para terceiros. Agora: a do que fica descoberto no Prático |
| Com o fato que diferencia dos vizinhos | — | **38%** (53 dos 71 que têm um fato) | Só entra quem está fora do meio |
| Com o risco oficial da cidade | — | **47%** | ANEEL ou Defesa Civil |
| Palavras (mediana · máximo) | 103 · 130 | 127 · **140** | ~1 minuto de leitura |

> [!warning] Metas que não batemos (e por quê)
> O plano pedia ≥ 130 esqueletos únicos e semelhança < 0,15. Chegamos a **125** e **0,21**. O que sobra de parecido é legítimo: dois clientes do Prático na mesma cidade, com o mesmo tipo de imóvel e sem fato distintivo, recebem o mesmo roteiro. Inventar diferença seria pior.

## 2. O roteiro: cada frase, de onde vem e por que existe
Exemplo real (`IMO_CASO_00004_01`, Brasília, Prático):

> **[1]** Para o seu apartamento de 105 m² em Brasília, recomendamos o plano Prático com a responsabilidade civil familiar. **[2]** Isso porque suas compras para a casa nos últimos 3 anos valem hoje pelo menos R$ 50 mil; você tem pelo menos R$ 13 mil em eletrônicos, os itens mais levados num arrombamento; e, no prédio e com dependentes ou pet, um acidente seu pode atingir outras pessoas. **[3]** Em eletrônicos, você está acima de 3 em cada 4 clientes com apartamento em Brasília. **[4]** Em Brasília, a distribuidora de luz ficou entre as piores no ranking de quedas de energia da ANEEL (25º de 33, 2025); o plano cobre danos elétricos. **[5]** Se você escolher menos, R$ 13 mil em eletrônicos no seu apartamento ficam descobertos contra roubo e quebra de vidros. **[6]** Confiança alta: os dados vêm do seu cadastro e das suas contas.

| # | Frase | De onde vem | Por que existe |
|---|---|---|---|
| 1 | **A casa dele** | tipo, área e cidade da ficha. Área cadastrada: "105 m²"; estimada: "**cerca de** 105 m²"; da região: sem área | Fala do imóvel dele, não do plano. "Cerca de" porque estimativa não é fato (RN-09) |
| 2 | **O porquê** | as **provas** das necessidades (ver [[02 - O motor passo a passo]]): aluguel, roubo e vidros, terceiros | É a razão do plano, com o dado do cliente |
| 3 | **O fato que diferencia** | `comparar_com_vizinhos`: o cliente contra os clientes da mesma cidade e tipo | Mostra que olhamos para **ele**, não para a média |
| 4 | **O risco da cidade** | ANEEL (quedas de energia) e Atlas de Desastres / Defesa Civil (chuva, alagamento, vendaval) | Conscientização (mentoria de 28/10): o risco de onde ele mora |
| 5 | **O que fica descoberto, em reais** | os bens comprovados (ou o aluguel) | Aversão à perda: "R$ 13 mil descobertos" pesa mais que "roubo não coberto" |
| 6 | **A confiança, com o acerto medido** | o boletim de `assertividade.py` | Honestidade: "erro abaixo de 20% em 2 de cada 3 testes" |

Outras frases que entram quando cabem: **o valor em jogo** (reconstrução ou acabamentos + bens), **a opção acima** ("O Total acrescenta perda de aluguel…"), **"perto do limite"** (quando a recomendação foi por pouco) e **"Antes de contratar"** (as perguntas de elegibilidade).

## 3. O fato que diferencia (como chegamos)
### A conta
1. Na base de desenvolvimento, para cada **cidade + tipo** (ex.: apartamentos de Brasília, 180 imóveis), calculamos os **percentis 10, 25, 75 e 90** de três coisas: compras para a casa em 36 meses, compras de eletrônicos e aluguel pago.
2. Colocamos o cliente nessa fila:
   - acima do percentil 90 → "acima de **9 em cada 10**";
   - acima do 75 → "acima de **3 em cada 4**";
   - abaixo do 25 → "abaixo de 3 em cada 4"; abaixo do 10 → "abaixo de 9 em cada 10";
   - **entre o 25 e o 75 → nada.** O meio não diferencia ninguém, e não inventamos diferença.
3. Grupo com menos de 20 imóveis: sobe de degrau (cidade → estado → base inteira), e o texto diz "clientes de DF", nunca o nome errado da cidade.

**Conta real (Brasília):** eletrônicos do cliente R$ 12.150 em 3 anos. Apartamentos de Brasília: percentil 75 = R$ 11.775; percentil 90 = R$ 17.035. 12.150 > 11.775 e < 17.035 → **"acima de 3 em cada 4"**.

### Qual fato, para qual plano
| Plano | Fato procurado | Por quê |
|---|---|---|
| Total | aluguel acima dos vizinhos; senão, eletrônicos ou compras acima | O aluguel é a necessidade do Total |
| Prático | eletrônicos acima; senão, compras acima | Roubo é a necessidade do Prático |
| Essencial | eletrônicos **abaixo** ("o roubo pesa menos para você"); senão, compras acima ("um incêndio levaria mais do que na maioria das casas") | Explica por que o Essencial basta, **nunca como crítica** |

### Dois cuidados
- **Sem número repetido diferente.** Se o porquê já disse "R$ 13 mil em eletrônicos" (valor de hoje, corrigido pela inflação), o fato só diz a comparação ("Em eletrônicos, você está acima de…"). Antes, o texto dizia "R$ 13 mil" e depois "você comprou R$ 12 mil", o que confundia. A posição na fila é a mesma com ou sem a inflação, porque a correção multiplica todo mundo pelo mesmo fator.
- **Cidade com acento e preposição certa.** A base grava "Sao Paulo"; o cliente lê "em São Paulo", "no Rio de Janeiro", "de Goiânia".

## 4. O risco da cidade (como escolhemos a frase)
Em ordem, a primeira que valer:
1. **Distribuidora de luz entre os 25% piores** do ranking de continuidade da ANEEL de 2025 (posição ≥ 75% de 33, ou seja, 25º para baixo) → "ficou entre as piores no ranking de quedas de energia; o plano cobre danos elétricos". **Porto Alegre** é a 33ª de 33: "em último lugar".
2. Senão, **chuva forte, alagamento ou enxurrada** registrados pela Defesa Civil de 2016 a 2025 → "o plano cobre alagamento". O BB cobre alagamento em danos por água (ver [[Catálogo do Seguro Residencial BB]]).
3. Senão, **vendaval ou granizo** de 2016 a 2025.
4. Senão, **nada**. Ex.: Fortaleza (23ª de 33 e nenhum registro desde 2016). Ausência de registro não prova ausência de risco, e não inventamos (RN-53).

**Por que 25%:** "entre as piores" só é verdade no último quarto. Em 21º de 33 (Recife), a frase seria exagero.

## 5. O limite de palavras (como o texto cabe)
Cada frase tem uma **prioridade**. Se o texto passar de **140 palavras**, saem primeiro as menos importantes:

| Prioridade | Frase | Pode sair? |
|---|---|---|
| 100 | Abertura (casa e cidade), não elegível | nunca |
| 98 · 97 · 96 · 95 | Antes de contratar · Atenção · Confiança · Porquê | nunca |
| 93 | Valor em jogo, **quando é o único jeito** de o texto ter dois valores em reais | nunca |
| 92 · 91 · 90 | Perto do limite · opção acima no Essencial (a única alternativa do texto, RN-37) · o que fica descoberto | nunca |
| 72 | Fato que diferencia | sai por último |
| 70 | Risco da cidade | sai antes do fato |
| 60 | Valor em jogo (quando o porquê e a lacuna já têm os reais) | sai cedo |
| 50 | Opção acima (Prático e Total) | sai primeiro |

Com perguntas de elegibilidade, a confiança perde o acerto em números para caber.

**Por que 140, e não 130:** com 130, o fato e o risco da cidade cabiam em menos de 30% dos motivos. Com 140 (~1 minuto de leitura), cabem em 38% e 47%. Trocamos 10 palavras por personalização.

## 6. As perguntas também dizem o porquê
| Antes | Agora |
|---|---|
| "Estimamos que o imóvel tem cerca de 262 m². Confere?" | "Qual a área do seu imóvel? Estimamos de 197 a 345 m². A resposta pode mudar o valor do incêndio em até R$ 148 mil." |
| "O acabamento do imóvel é simples, normal ou de alto padrão?" | "… A resposta pode mudar o valor do incêndio em até R$ 133 mil." |
| "Seus móveis, eletrodomésticos e eletrônicos ficam entre R$ 47 mil e R$ 128 mil?" | "… valem entre R$ 47 mil e R$ 128 mil? A resposta pode mudar a proteção dos seus bens em até R$ 80 mil." |

O "até R$ X" é o **valor da informação**: quanto da faixa a resposta pode eliminar. Desde a revisão de código, na faixa calibrada ele nunca passa da largura real da reconstrução.

## 7. Regras que o motivo respeita
- **RN-07:** nunca usa idade. Teste: mudar a idade de 25 para 80 não muda uma letra.
- **RN-09:** estimativa é dita como estimativa ("cerca de", "estimamos", "os bens que estimamos em").
- **RN-37:** sempre há uma alternativa: o que fica descoberto se escolher menos, ou o que o plano acima acrescenta.
- **RN-53:** nada inventado. Sem fato distintivo ou sem dado da cidade, a frase some.
- **0 termos internos** ("presumido", "segundo risco"…) no texto do cliente.

Ligações: [[11 - Assertividade de cada cálculo (do zero)]] · [[02 - O motor passo a passo]] · [[03 - Cada métrica explicada]] · [[Motivo da recomendação]]
