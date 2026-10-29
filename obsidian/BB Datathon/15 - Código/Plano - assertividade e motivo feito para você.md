---
tags: [plano, assertividade, motivo, dados-faltantes, motor, documentacao]
data: 2026-10-28
status: aprovado e executado em 28/10
---
# 🎯 Plano: a assertividade de cada cálculo + o motivo "feito para você"

> [!success] Executado em 28/10
> Área 14,1% de erro (chute 44,4%) · faixa de área × padrão 1,76× contendo o real em 88% (antes 2,7×) · motivo com casa e cidade em 138 de 138, 125 esqueletos únicos (antes 83), frase mais repetida em 32 (antes 93) · 155 testes · revisão de código com 8 achados, todos corrigidos. Explicação do zero: [[11 - Assertividade de cada cálculo (do zero)]] e [[12 - O motivo feito para você]].
>
> **O que mudou do plano:** (1) o limite do motivo subiu de 130 para 140 palavras, porque com 130 o fato e o risco da cidade cabiam em menos de 30% dos textos; (2) as metas de 130 esqueletos e semelhança < 0,15 não foram batidas (125 e 0,21); (3) a faixa de área × padrão foi alargada até a de padrão normal na revisão de código (contém o real em 88%, não 82%).

**Objetivo:** cada número que o motor inventa quando falta um dado vem com a **nota de acerto** dele, medida contra o valor real, e o motivo que o cliente lê passa a falar **da casa dele**, não do plano.

**Como:** (1) um arquivo novo, `motor/assertividade.py`, mede todos os cálculos do mesmo jeito; (2) a faixa da reconstrução, que hoje é larga demais, passa a ser calibrada; (3) o motivo escolhe os fatos que **diferenciam** este cliente dos vizinhos e diz a confiança em números; (4) uma nota nova no Obsidian explica tudo do zero.

**Ferramentas:** Python 3.11, pandas, numpy, pytest (nada novo no `requirements.txt`).

---

## 1. O que medimos hoje (a resposta curta)

**Como medimos:** é uma **prova com gabarito escondido**. Pegamos os 1.016 imóveis da base de desenvolvimento que **têm** área cadastrada, escondemos a área, deixamos o motor estimar e comparamos com a verdade. Fazemos isso em **5 rodadas**: em cada uma, o motor aprende com 4/5 dos imóveis e é testado no 1/5 que não viu. Isso se chama **validação cruzada em 5 dobras**. Assim, o motor nunca é testado num imóvel que já conhecia.

**O "chute":** para saber se um cálculo presta, comparamos com o pior método possível: dar a todo mundo o valor do meio da base (a **mediana geral**). Um cálculo bom tem que errar **muito menos** que o chute.

| O que falta | Casos na base de teste (de 138) | Como o motor completa | Acerto medido | Chute (para comparar) | Veredito |
|---|---|---|---|---|---|
| **Área** | **92** | IPTU (peso 0,6) e conta de luz (0,4) comparados ao R$/m² da cidade | erro mediano **15%**; **64%** dos imóveis a menos de 20% da área real; a faixa contém a área real em **82%** | erro mediano 44%; só 26% a menos de 20% | ✅ **3× melhor que o chute** |
| Área sem IPTU nem luz | **0** | mediana da região (cidade + tipo → cidade → estado) | erro mediano 30% | 44% | 🟡 reserva; não é usada no teste |
| **Padrão** (econômico, normal, superior) com área cadastrada | **34** | IPTU por m² comparado à mediana da cidade | acerta a **classe exata** só em **51%** (o chute "normal" acerta 63%); acerta o **intervalo** de 2 classes em **98%** | 63% (classe exata) | ⚠️ o IPTU **não** diz o padrão exato; só descarta um extremo. Por isso o motor usa intervalo |
| **Padrão** sem área | **64** | intervalo inteiro (0,85 a 1,30) | contém o real em 100%, mas é o mais largo | — | ⚠️ é aqui que a faixa explode (ver seção 2) |
| **Tipo** (casa ou apartamento) | 138 (sempre conferido) | termo do endereço × complemento (AP, BLOCO × CASA, LOTE) | as duas fontes **concordam em 100%** (2.578 de 2.578) | — | ✅ não há gabarito, mas duas fontes independentes batem |
| **Vínculo** (inquilino, financiado, dono) | 138 | aluguel pago, parcela de financiamento, crédito de aluguel | **observado** nas transações em 70 de 138; nenhum caso com aluguel **e** financiamento juntos | — | 🟡 os **47** "provável quitado" não têm prova: só ausência de sinal |
| **Uso** (mora ou não mora) | **31** sem o endereço principal | crédito de aluguel → alugado; outro imóvel principal → veraneio; senão, pergunta | **não dá para medir** (sem gabarito). Testamos a conta de luz: imóvel principal e não principal gastam igual (1,00 × 1,00), então a luz **não** indica casa vazia | — | 🔴 vira pergunta obrigatória (RN-19) |
| **Bens** | 138 | compras de 36 meses corrigidas pelo IPCA (mínimo) até 2,7 × compras (máximo) | **não há gabarito** do valor dos bens. O que dá para medir: compras e bens ligados ao imóvel **concordam** (correlação de postos 0,63) | — | 🟡 o mínimo é comprovado; o 2,7 é **premissa** (vida útil de ~8 anos) |
| Bens sem compras | **0** | média da região combinada com a renda | erro mediano **23%** (só região: 41%) | — | ✅ reserva; não é usada no teste |
| CEP agregado | — | testado e **descartado** | explica 21,5% da variação; um CEP **sorteado** explica 22,3% | — | ❌ é ruído (RN-10) |

> [!tip] A conta 0,6 + 0,4 foi confirmada pelos dados
> Deixamos o computador **aprender** os pesos sozinho, por regressão. Ele chegou a **0,59 para o IPTU e 0,42 para a luz**: praticamente os 0,6 e 0,4 que escolhemos. Acrescentar a conta de água e o tipo melhora pouco (15,0% → 13,4%) e deixa a conta difícil de explicar. **Decisão proposta:** manter os pesos e trocar a média comum pela **média geométrica** (erro 15,0% → 14,1%; a explicação muda só uma palavra).

---

## 2. O problema que a medição revelou: a faixa do incêndio larga demais

O valor de reconstruir é **área × custo do m² × padrão**. Hoje o motor pega o **pior caso de cada um** e multiplica:

> menor área possível × menor padrão … até … maior área possível × maior padrão

Exemplo real (`IMO_CASO_00001_01`, Recife): área de 193 a 345 m² × padrão de 0,85 a 1,30 → reconstrução de **R$ 310 mil a R$ 961 mil**. Isso é **3,1 vezes** de distância entre o mínimo e o máximo. Para o cliente, uma faixa assim diz pouco.

**Por que exagera:** a área e o padrão quase nunca erram para o mesmo lado ao mesmo tempo. Medimos:

| Faixa de "área × padrão" (imóveis sem padrão e sem área) | Contém o valor real | Largura (máx ÷ mín) |
|---|---|---|
| **Hoje** (pior caso × pior caso) | 97% | **2,73×** |
| **Calibrada** (percentis 9% e 91% do erro real, como já fazemos na área) | **82%** | **1,68×** |

**Decisão proposta:** nos **64** casos de teste com área estimada **e** padrão desconhecido, usar a faixa calibrada. A meta é a mesma da área: conter o valor real em ~80% dos casos. Os outros casos não mudam.

---

## 3. O motivo "feito para você"

**Medimos os 138 motivos de hoje:**
| Medida | Hoje | Meta |
|---|---|---|
| Motivos com um "esqueleto" único (o texto sem os números) | 83 de 138 | **≥ 130** |
| Motivos que citam a cidade ou o tipo de imóvel do cliente | **0** | **138** |
| Semelhança média entre dois motivos (0 = nada em comum, 1 = iguais) | 0,29 | **< 0,15** |
| A frase mais repetida | "Incluímos a responsabilidade civil familiar…" em **93** motivos | nenhuma frase em mais de 40 |
| Tamanho | 103 palavras (mediana) | até 130 |

**O novo roteiro (5 frases, todas com dado do cliente):**
1. **A casa dele:** "Para o seu apartamento de cerca de 80 m² em São Paulo, recomendamos o Essencial."
2. **O fato que diferencia** (comparado com imóveis da mesma cidade e tipo, da base de desenvolvimento): só entra se o cliente estiver entre os 25% de cima ou de baixo. Ex.: "Você comprou R$ 13 mil em eletrônicos em 3 anos, mais que 3 em cada 4 apartamentos de Brasília."
3. **O risco do lugar:** a frase escolhida pelo dado da cidade (Atlas de Desastres, ranking da ANEEL) e, sem ele, pela cobertura mais acionada (danos elétricos, 53,3%). Nunca a mesma frase para todos.
4. **O que fica descoberto, em reais:** "Sem o Prático, os R$ 13 mil em eletrônicos ficam sem proteção contra roubo."
5. **A confiança em números, em português simples:** "A área foi estimada pelo IPTU e pela conta de luz. Em imóveis com área conhecida, essa conta ficou a menos de 20% da área real em 2 de cada 3 casos." O número vem do arquivo de assertividade, nunca escrito à mão.

**O que não muda:** o plano continua sendo escolhido pelas necessidades (aluguel → Total; roubo e vidros → Prático; terceiros → RC). Nada de idade (RN-07). A renda só aparece quando entrou na conta (D-08). Estimativa é sempre dita como estimativa (RN-09).

**As perguntas:** cada pergunta passa a dizer **por que** está sendo feita, em reais. Ex.: "Qual a área do seu imóvel? Hoje estimamos de 193 a 345 m²; a sua resposta deixa o valor do incêndio mais preciso." Continuam no máximo 3.

---

## 4. Regras conferidas no vault
| Regra | Como o plano atende |
|---|---|
| RN-08 (combinar sinais) | Área por 2 sinais; padrão por intervalo; fato distintivo sempre ao lado da necessidade, nunca sozinho |
| RN-09 (estimativa não é fato) | Toda estimativa no texto diz "estimamos" e mostra o acerto |
| RN-32 (faixa sempre) | A faixa calibrada continua existindo para os 138 casos |
| RN-35 (confiança e limitações) | Assertividade de cada cálculo no README, no JSON e no texto |
| RN-47 (métricas adequadas; sem rótulo, sem acurácia) | Onde há gabarito, medimos acerto; onde não há (bens, uso), dizemos isso e medimos a concordância entre fontes |
| RN-49 (o motivo é o principal) | Seção 3 |
| App congelado | **Nenhum arquivo de `prototipos/`** é editado; `canal` e as chaves de `casos_contrastantes` ficam iguais |

---

## 5. Tarefas

### Tarefa 1 · `motor/assertividade.py` (refatoração + medição)
**Arquivos:** criar `motor/assertividade.py`; tirar de `motor/motor.py` as funções `backtest`, `teste_cep` e `backtest_bens_sem_compras` (movidas, não copiadas); `calibrar` chama o módulo novo; teste em `tests/test_assertividade.py`.
**Produz:** `medir_tudo(dados) -> dict` com uma entrada por cálculo (`area`, `area_regional`, `padrao_iptu`, `area_x_padrao`, `tipo`, `vinculo`, `uso`, `bens`, `bens_sem_compras`, `cep`). Cada entrada é um **boletim** com as mesmas chaves: `o_que_estima`, `como`, `casos_no_teste`, `tem_gabarito` (bool), `metodo` ("5 dobras" ou "concordância entre fontes"), `erro_mediano_pct`, `ate_20pct_pct`, `na_faixa_pct`, `chute_erro_mediano_pct`, `veredito`.
- [ ] Teste: `test_boletim_da_area` → `erro_mediano_pct` entre 13 e 17; `na_faixa_pct` entre 77 e 86; `chute_erro_mediano_pct > 2 * erro_mediano_pct`.
- [ ] Teste: `test_sem_gabarito_e_dito` → `medir_tudo(...)["bens"]["tem_gabarito"] is False` e `erro_mediano_pct is None`.
- [ ] Teste: `test_dobras_reprodutiveis` → duas chamadas devolvem o mesmo dicionário (semente fixa 0).
- [ ] Teste: `test_motor_funciona_sem_assertividade` → `processar` roda com `cal` sem a chave `assertividade` (RN-12).
- [ ] Rodar `pytest -q`: os 111 testes antigos + os novos passam. Commit `refactor: assertividade de cada cálculo em um módulo, validação em 5 dobras`.

### Tarefa 2 · Área pela média geométrica + faixa calibrada de área × padrão
**Arquivos:** `motor/motor.py` (`_area_estimada`, `_calibrar_area`, `valor_imovel`, texto da regra do incêndio em `dimensionar`, `valor_da_informacao`); `motor/parametros.py` (`FATOR_PADRAO_MEIO = 1.05`).
**Produz:** `cal["area_padrao_q"] = (q09, q91)`; em `valor_imovel`, quando `area["natureza"] == "ESTIMADO"` e `origem_padrao == "não cadastrado"`: `reconstrucao = (area["valor"] × 1,05 × q09 × custo_min, area["valor"] × 1,05 × q91 × custo_max)` e `origem_padrao = "faixa calibrada de área × padrão"`.
- [ ] Teste: `test_media_geometrica` → IPTU dá 100 m² e luz dá 200 m² ⇒ 100^0,6 × 200^0,4 ≈ 131,95 m².
- [ ] Teste: `test_faixa_calibrada_mais_estreita` → nos 64 casos, mediana de `reconstrucao_max / reconstrucao_min` cai de ~3,1 para ≤ 2,2; os outros 74 casos ficam iguais.
- [ ] Teste: `test_faixa_calibrada_contem_80` → boletim `area_x_padrao.na_faixa_pct` entre 77 e 86.
- [ ] Validador dos templates: 0 erros. Commit `feat: faixa calibrada de área × padrão (2,7× → 1,7×) e área pela média geométrica`.

### Tarefa 3 · Fatos distintivos
**Arquivos:** `motor/motor.py` (`calibrar` guarda `cal["pares"]`: percentis 25/50/75 de compras totais e de eletrônicos por degrau cidade+tipo → cidade → estado → geral, mínimo de 20 imóveis, reaproveitando `_degraus`); `motor/motivo.py` (`fato_distintivo(f, cal) -> str | None`).
- [ ] Teste: `test_fato_distintivo_acima` → eletrônicos acima do percentil 75 da cidade ⇒ texto com "mais que 3 em cada 4" e o nome da cidade.
- [ ] Teste: `test_fato_distintivo_no_meio_some` → entre os percentis 25 e 75 ⇒ `None`.
- [ ] Teste: `test_fato_nunca_usa_idade` → mudar `idade` não muda o texto (RN-07).
- [ ] Commit `feat: fato que diferencia o cliente dos vizinhos (percentis da cidade)`.

### Tarefa 4 · O motivo novo
**Arquivos:** `motor/motivo.py` (`justificativa` com o roteiro da seção 3; `_confianca` lê `cal["assertividade"]`); `motor/metricas.py` (`qualidade_do_motivo` ganha `esqueletos_unicos`, `cita_cidade_pct`, `semelhanca_media`, `frase_mais_repetida_n`).
- [ ] Teste: `test_motivo_cita_casa_e_cidade` → os 138 motivos contêm o tipo e a cidade do imóvel.
- [ ] Teste: `test_motivos_diferentes` → `esqueletos_unicos >= 130` e `semelhanca_media < 0.15`.
- [ ] Teste: `test_confianca_com_numero` → motivo de área estimada contém "2 de cada 3" (vindo do boletim, não escrito à mão).
- [ ] Teste: `test_tamanho_e_termos` → até 130 palavras; 0 `TERMOS_INTERNOS`.
- [ ] Ler 10 motivos em voz alta (skill `copywriting`) e corrigir o que soar robótico. Commit `feat: motivo feito para você (casa, fato distintivo, risco do lugar, lacuna em reais, confiança em números)`.

### Tarefa 5 · Perguntas com o "por quê"
**Arquivos:** `motor/motor.py` (`montar_perguntas`: texto da pergunta + "hoje estimamos X; a resposta deixa Y mais preciso"); `para_templates` mantém o prefixo "(opcional) ".
- [ ] Teste: `test_pergunta_da_area_diz_a_faixa` → contém a faixa de área atual em m².
- [ ] Teste: `test_maximo_3_perguntas` continua passando. Commit.

### Tarefa 6 · Gerar, revisar e documentar
- [ ] `python motor/gerar.py`; validador 0 erros; `entrega/assertividade.json` novo; `metricas.json` atualizado.
- [ ] `code-review` no diff; `verification-before-completion` com os números.
- [ ] **Obsidian:** nota nova `16 - Projeto por inteiro/11 - Assertividade de cada cálculo (do zero).md`. Para cada cálculo: o problema em uma frase → a conta passo a passo com um caso real → como medimos (a prova com gabarito escondido) → o resultado → a comparação com o chute → o que isso muda para o cliente → a limitação. Atualizar 00 (índice), 01 (dados), 02 (motor), 03 (métricas), 09 (conta por conta), 10 (dicionário de funções), Mapa do código, Painel.
- [ ] README (seção de métricas e limitações), `documentos/contexto/26-assertividade-e-motivo.md` e `00-mapa.md`.
- [ ] Commit direto na `main`, sem coautoria; push.

---

## 6. Pontos de atenção (o que pode dar errado)
1. **Cidade com poucos imóveis na base de desenvolvimento:** o fato distintivo desce de degrau (estado, depois geral) e o texto diz "no seu estado" ou "nas casas da base", nunca o nome errado da cidade.
2. **Fato distintivo "para baixo"** (o cliente compra menos que os vizinhos): só entra quando ajuda a decisão (ex.: explica por que o Essencial basta). Nunca como crítica.
3. **Município sem dado de desastre nem da ANEEL:** a frase do risco usa a cobertura mais acionada; o motivo não fica sem a frase 3.
4. **Faixa calibrada no limite do produto:** a faixa continua presa aos limites mínimo e máximo de cada cobertura (`faixa()`), como hoje.
5. **Imóvel não elegível:** o motivo novo não oferece plano acima nem diz "recomendamos"; segue a frase de não elegível de hoje.

## 7. Skills de cada etapa
| Etapa | Skill | Por quê |
|---|---|---|
| Plano | `writing-plans` | Este documento |
| Código | `test-driven-development` | Cada regra nasce de um teste que falha |
| Texto do motivo e das perguntas | `copywriting` + `marketing-psychology` | Especificidade, perda concreta, sem medo vazio e sem inventar |
| Documentação | `better-writing` | Português claro para quem nunca viu o projeto |
| Revisão | `code-review` + `verification-before-completion` | Provar com números antes de dizer "pronto" |

Ligações: [[Plano - recomendação por necessidades]] · [[02 - O motor passo a passo]] · [[03 - Cada métrica explicada]] · [[10 - Dicionário de funções]]
