# Guia da equipe: como o motor usa os dados (e como explicar)

Para estudar antes do pitch, das perguntas e do vídeo. Repositório: `C:\Users\maxom\Documents\datathon-protecao-inteligente` (branch `revisao-qa-p1-p5`).

---

## 1. A ideia em 30 segundos
O banco já sabe muita coisa sobre o cliente: se paga aluguel, se tem financiamento, quanto paga de IPTU e de luz, o que comprou nos últimos 3 anos. O motor junta esses sinais e responde 5 perguntas para cada imóvel:

1. **Pode contratar?** (elegibilidade)
2. **Qual plano?** (Essencial, Prático ou Total, + adicionais)
3. **Quanto segurar em cada cobertura?** (faixa mínima e máxima em R$)
4. **Quanto confiamos nisso?** (ALTA, MÉDIA ou BAIXA, com o motivo)
5. **O que falta perguntar?** (até 3 perguntas, a mais útil primeiro)

Tudo por regras escritas, sem machine learning. Cada regra tem fonte e teste.

---

## 2. Cada dado e para que serve

### Tabela `enderecos_imoveis`
| Coluna | Para que o motor usa |
|---|---|
| `possui_termo_apartamento`, `possui_termo_condominio`, `complemento` | **Tipo do imóvel** (apartamento, casa, casa em condomínio). O complemento ("BLOCO B APTO 305") confere o tipo; se contradiz, a confiança cai e vira pergunta |
| `area_cadastrada_m2` | **Área** → base do valor de reconstrução. Vazia em 67% dos casos |
| `padrao_construtivo_cadastrado` | Ajusta o custo do m² (econômico 0,85 · normal 1,0 · superior 1,30). Vazio → faixa de 0,85 a 1,30 + pergunta |
| `material_parede_externa_cadastrado` | Elegibilidade: parede combustível → pergunta sobre madeira pré-fabricada ABNT |
| `situacao_imovel_cadastral` | Elegibilidade: tombado, desapropriado ou condenado → NAO |
| `endereco_principal_compativel` | **Uso**: é onde a pessoa mora? Se não, pode ser veraneio ou alugado |
| `uf_real`, `codigo_ibge_municipio` | Custo do m² do estado (SINAPI/CUB), aluguel da capital (FipeZAP), calibração da área por município |

### Tabela `sinais_imobiliarios` (transações)
| Coluna | Para que o motor usa |
|---|---|
| `pagamento_aluguel_recorrente`, `valor_aluguel_recorrente` | **Vínculo = inquilino** → Total (perda de aluguel). O valor do aluguel dimensiona a cobertura (6 a 12 meses) |
| `parcela_financiamento_imobiliario` | **Vínculo = financiado** → segundo risco (a estrutura tem seguro do financiamento) |
| `credito_recorrente_compativel_aluguel` | Recebe aluguel → **proprietário locador** → Total (o aluguel pode parar) |
| `pagamento_condominio_mensal` | Confirma condomínio |
| `pagamento_iptu_anual`, `energia_media_mensal_6m` | **Estimam a área** quando ela não está cadastrada (correlação 0,82 e 0,81 com a área real) |
| `compras_moveis/eletrodomesticos/eletronicos_36m` | **Valor dos bens** e pontos para o Prático (bens altos, eletrônicos) |
| `gastos_material_construcao_24m` | Possível reforma (≥ R$ 15 mil) → pergunta de elegibilidade |
| `gastos_vidracaria_24m` | Ponto para o Prático (quebra de vidros) e amplia a faixa de vidros |

### Tabela `bens_compras`
| Coluna | Para que o motor usa |
|---|---|
| `valor_bem_ponderado_referencia` | Bens vinculados ao imóvel, já ponderados pela chance de estarem lá. Entram no mínimo comprovado de bens |
| `tipo_bem` | Separa eletrônicos (base do roubo), eletrodomésticos (danos elétricos) e móveis (danos por água) |

### Tabela `clientes`
| Coluna | Para que o motor usa |
|---|---|
| `possui_seguro_residencial` | Elegibilidade: um imóvel só → NAO (já segurado) |
| `usuario_app`, `indice_maturidade_digital` | **Canal**: 1 toque no app ou gerente. Pelo comportamento digital, nunca pela idade |
| `quantidade_dependentes`, `possui_pet_informado` | **Só necessidade de RC familiar**, informada pelo cliente. Nunca valor, risco, canal ou confiança |
| `renda_mensal` | **Reforço dos bens de quem não tem compras nem bens ligados ao imóvel**, combinada com a média da região (liberada na mentoria do BB, 28/10). Quem tem compras segue pelas compras |
| `idade`, `origem_renda` | **Não usados.** Teste automático prova: trocar esses campos não muda nada |

### O que descartamos e por quê
- **Renda como atalho:** correlação de 0,88 com os bens. Depois da mentoria (o BB confirmou que renda não é dado sensível), ela entra **só onde falta prova**: para quem não tem compras, região + renda erra 22,7% contra 40,5% só da região (teste fora da amostra). Quem tem compras segue pelas compras, que são o bem de verdade.
- **Idade:** não diz nada sobre o imóvel.
- **Coordenadas e CEP:** são fictícios na base.
- **Ranking de raios do INPE:** desatualizado.

### Fontes externas (todas públicas)
| Fonte | Uso |
|---|---|
| SINAPI set/2026 (IBGE, API SIDRA) | Custo mínimo do m² por estado |
| CUB R8-N oficial (Sinduscons SP, DF, GO, BA, MG, RS, PR) | Custo máximo do m². Nos outros estados (RJ, PE, CE): SINAPI × 1,14 |
| IPCA 12 meses (Banco Central, API) | Traz as compras de 3 anos para o preço de hoje (fator 1,069) |
| FipeZAP Locação set/2026 | Aluguel por m² de quem mora no próprio imóvel |
| Condições Gerais BB v1.4 | Regras do produto (segundo risco, limite único, exclusões) |

---

## 3. Como sai cada coisa (passo a passo)

**Área estimada.** Na base de desenvolvimento, para imóveis com área conhecida, o motor calcula quanto se paga de IPTU por m² e de luz por m² em cada cidade. Para um imóvel sem área: área ≈ 60% × (IPTU ÷ IPTU por m² da cidade) + 40% × (luz ÷ luz por m² da cidade). A faixa usa o erro típico medido (percentis 10 e 90).

**Valor de reconstrução.** área × custo do m² (SINAPI a CUB) × padrão. Apartamento, condomínio ou financiado: só 25% a 40% disso (acabamentos), porque a estrutura tem seguro próprio (cláusula 15.2).

**Bens.** Mínimo = o maior entre compras de 36 meses e bens vinculados, × IPCA. Máximo = 2,7 × compras (a casa tem mais coisa do que o que foi comprado em 3 anos). Piso de R$ 15 mil.

**Incêndio** (a principal) = reconstrução + bens. Mínimo de R$ 100 mil, máximo de R$ 600 mil (limites do produto).

**Outras coberturas:** proporções da reconstrução e dos bens (ex.: vendaval 10% a 20% da reconstrução em casa, 2% a 5% em apartamento, porque apartamento expõe sobretudo as janelas).

**Plano por pontos:**
| Sinal | Plano | Pontos |
|---|---|---|
| Paga aluguel / recebe aluguel | Total | 2 |
| Prédio ou condomínio (vizinhos) | Total | 1 |
| Crianças **e** pets informados | Total | 1 |
| Bens comprovados ≥ R$ 36 mil | Prático | 2 |
| Eletrônicos ≥ R$ 10 mil | Prático | 1 |
| Casa fora de condomínio | Prático | 1 |
| Gasto com vidraçaria | Prático | 1 |

Total com 2+ pontos. Prático com 2 de Prático, ou 1 de Prático + 1 de Total ligado ao imóvel. Senão, Essencial.
**Adicional:** crianças ou pets + prédio/condomínio, sem Total → RC familiar como cobertura adicional.

**Confiança:** cada dado crítico (área, bens, uso, vínculo, tipo) é **observado** (documento, transação, confirmado), **estimado** (calculado de outros sinais) ou **presumido** (sem sinal).
- BAIXA: área ou bens presumidos, ou um presumido junto com um estimado.
- ALTA: os 5 observados e nada pendente.
- MÉDIA: o resto.

**Perguntas:** primeiro elegibilidade, depois o que muda o plano, depois o que mais aperta a faixa em R$ (o motor calcula quanto cada resposta pode cortar). Máximo 3.

**Jornada (gerente como último recurso, mentoria de 28/10):** não elegível → sem nova proposta (16). Confiança baixa, sinal de obra ou cliente sem app → gerente (35). Pendência que o app resolve com sim/não, ou maturidade digital < 40 → app com perguntas (20). O resto → 1 toque (67).

---

## 4. Perguntas prováveis da banca (e a resposta)

**"Por que não usaram machine learning?"**
Não há rótulo (não sabemos qual plano era o certo nem sinistros). Um modelo aprenderia a copiar a renda. Regras são explicáveis, auditáveis e o guia aceita.

**"Como estimam a área se 67% não têm?"**
Pelo IPTU e pela luz, comparados com imóveis da mesma cidade com área conhecida. A faixa usa o erro real medido. E a área vira a primeira pergunta quando é ela que mais aperta a faixa.

**"Vocês usam a renda? O guia fala em atributos pessoais."**
Na mentoria, o BB confirmou que renda não é dado sensível, e a LGPD também não a lista como sensível. Mesmo assim, ela nunca decide sozinha: só reforça a estimativa dos bens de quem não tem compras, junto com a média da região (o erro cai de 40,5% para 22,7% fora da amostra), e o cliente lê isso no motivo. Quem tem compras segue pelas compras. Elegibilidade, canal e confiança não usam renda, e a elegibilidade fica igual em todas as faixas de renda (regra dos 80%: 0,85). A idade continua fora de tudo.

**"Por que usam crianças e pets se é atributo pessoal?"**
Não usamos como risco nem como valor. O slide 14 aponta "casa familiar → RC familiar": é uma necessidade que o próprio cliente informou. Provamos que isso nunca muda faixa, elegibilidade, canal ou confiança (0 casos).

**"Como garantem que a confiança não é chute?"**
Ela diz qual dado foi visto, qual foi estimado e qual falta. Mexemos 20% nos pesos e nenhum caso mudou de nível. E quanto menor a confiança, mais larga a faixa (ALTA 1,89 · MÉDIA 2,33 · BAIXA 2,56).

**"Por que 16 casos não elegíveis?"**
São clientes que já têm seguro residencial BB e um imóvel só: o seguro é desse endereço, e o guia proíbe duas propostas. Quem tem dois imóveis recebe a pergunta "qual já tem seguro?".

**"E favela, área rural, MEI?"**
A base não tem esses dados. Viram declaração na contratação. Está nas limitações.

**"Por que a casa de veraneio ficou no Essencial?"**
O roubo do Prático não cobre residência desocupada (cláusula de roubo 2.1 c). Recomendar o Prático porque a casa fica vazia seria vender uma cobertura que pode não pagar.

**"Isso funciona de verdade no banco?"**
Roda os 138 casos em menos de um segundo, tem 91 testes, os testes rodam a cada mudança no GitHub, gera as mesmas planilhas toda vez e tem uma API pronta para o app, o gerente ou um agente chamarem. As premissas estão num arquivo só (`parametros.py`), para o atuário ajustar sem mexer na lógica.

**"O que fariam com mais tempo?"**
Calibrar as proporções com dados de sinistro da Brasilseg, enriquecer com risco do território (Atlas Digital de Desastres), CUB oficial dos 6 estados que faltam e medir a conversão do 1 toque num piloto.

---

## 5. Roteiro do vídeo (5 min)
| Tempo | O que mostrar | Quem fala |
|---|---|---|
| 0:00–0:40 | Problema: só 17% dos lares têm seguro (slide 6); o cliente não sabe quanto segurar | |
| 0:40–1:20 | Ideia: o banco já sabe; sinais → sugestão → confiança → confirmação → recomendação | |
| 1:20–2:30 | **Demo:** protótipo do gerente, botões A, B e C. Mostrar plano, faixas, motivo e perguntas mudando entre os 3 perfis | |
| 2:30–3:20 | **Código:** `parametros.py` (premissas com fonte), `escolher_plano` (pontos), `confianca_geral` (regra). Rodar `python -m pytest -q` (91 passando) e `python motor/gerar.py --entrega` | |
| 3:20–4:10 | Evidências: tabela de métricas do README (justiça 0, estabilidade, confiança, regra dos 80%) | |
| 4:10–5:00 | Limitações e próximos passos; responsabilidade (idade fora, renda só como reforço e avisada ao cliente, controle humano, IA declarada) | |

**Dica:** gravem a tela rodando os testes ao vivo. "91 passed" na tela vale mais que um slide.

---

## 6. O que cada um precisa saber explicar (mínimo)
- **Todos:** o fluxo dos 5 passos, onde a renda entra (só reforço dos bens sem compras, liberada na mentoria) e onde não entra, o que é a confiança.
- **Quem mostra o código:** onde está cada regra (`motor.py`), onde mudar um número (`parametros.py`), como rodar.
- **Quem faz o pitch:** os 3 perfis e por que cada um tem um plano diferente; a tabela de métricas.
- **Quem responde perguntas:** seção 4 deste guia.
