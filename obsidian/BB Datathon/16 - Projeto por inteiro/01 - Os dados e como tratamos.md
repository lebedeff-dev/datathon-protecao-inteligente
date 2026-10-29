---
tags: [projeto, dados, tratamento]
atualizado: 2026-10-28
---
# 🗂️ 01 · Os dados e como tratamos

## 1. O que recebemos
Duas bases sintéticas com as mesmas tabelas: **desenvolvimento** (2.200 clientes, 2.578 imóveis), usada para **aprender** (calibrar), e **teste comum** (120 clientes, 138 imóveis), onde o motor **responde** e que vai para as planilhas.

| Tabela | Uma linha por | O que o motor usa |
|---|---|---|
| `clientes` | cliente | uso do app, maturidade digital, dependentes, pet, produtos de seguridade, seguro residencial, **renda** (só nos bens de quem não tem compras; D-08) |
| `enderecos_imoveis` | imóvel | município, UF, código IBGE, termos do endereço (apartamento, casa, condomínio), complemento, área cadastrada, padrão, material, situação cadastral, endereço principal |
| `sinais_imobiliarios` | imóvel | aluguel pago, crédito de aluguel, parcela de financiamento, condomínio, IPTU, energia, compras de 36 meses (móveis, eletrodomésticos, eletrônicos), material de construção e vidraçaria (24 meses) |
| `bens_compras` | bem | tipo do bem, valor, chance de estar no imóvel e confiança desse vínculo |
| `territorio` | imóvel | coordenada aproximada (**não usamos**: é perturbada, RN-10) |

**O que nunca entra em decisão:** idade (RN-07), coordenadas e CEP (fictícios, RN-10). A renda entra num ponto só (ver seção 4).

## 2. Juntar e calibrar
1. **Juntar:** endereço + sinais + cliente por `imovel_id` e `cliente_id` (`motor.processar`).
2. **Calibrar na base de desenvolvimento** (`motor.calibrar`), nos 1.016 imóveis com área cadastrada:
   - quanto custa o **IPTU por m²** e a **energia por m²** em cada município (mediana; zeros ignorados);
   - o erro típico da área estimada, que define a faixa (percentis de 9% e 91%);
   - as **médias da região em degraus** para área e compras;
   - a razão compras ÷ renda por município (para quem não tem compras);
   - os **backtests fora da amostra** (seção 6) e o **teste do CEP**.

## 3. Cada lacuna e o que fazemos
Na base de teste, só 3 dos 138 casos têm tudo preenchido. Por isso o tratamento de lacunas é central.

| Dado | Falta em | O que o motor faz | Rótulo no dado |
|---|---|---|---|
| **Área** | 92 de 138 | Estima pelo IPTU (peso 0,6) e pela energia (0,4) comparados ao município. Se um dos dois faltar, usa só o outro. Sem nenhum, usa a média da região em degraus. Faixa: estimativa × [percentil 9%, 91%] | estimado (DERIVADO) ou presumido (região) |
| **Padrão de acabamento** | 98 | Com área cadastrada, o **IPTU/m² ÷ mediana do município** indica o padrão: abaixo de 0,90 descarta o superior; acima de 1,15, o econômico (acerta 97,8% fora da amostra). Senão, faixa aberta (fator 0,85 a 1,30) + pergunta | "estimado pelo IPTU/m²" ou "não cadastrado" |
| **Material da parede** | 109 | Trata como alvenaria (o comum). Só pergunta se o cadastro disser outro material | — |
| **Compras** | 0 (na base de teste) | Média de compras da região, combinada com a renda quando houver (média geométrica, entre 0,5× e 2× a região) | presumido (região e renda) |
| **Uso (mora lá?)** | 20 duvidosos | Confiança baixa + pergunta obrigatória no app; o gerente entra se a resposta mudar o caso | presumido |
| **Vínculo** | sempre deduzido | Aluguel pago → inquilino; parcela → financiado; recebe aluguel e não mora → locador; senão → proprietário | observado ou inferido |

**Média da região em degraus** (mentoria de 28/10): município + tipo → município → estado → geral, com no mínimo 20 imóveis em cada degrau. Exemplo: apartamento em Curitiba sem área usa a mediana dos apartamentos de Curitiba; um município fora da base sobe para o estado.

**Por que não o CEP:** o mentor sugeriu média por CEP, mas o guia diz que o CEP da base é fictício. Testamos: o CEP "explica" 21,5% da variação do IPTU/m², e um CEP sorteado explica 22,3%. É ruído. O degrau de CEP existe no código (`P.USAR_CEP`), desligado, pronto para o CEP real.

## 4. Os bens (o que tem dentro de casa)
Três âncoras (`motor.estimar_bens`), sempre **a preço de hoje** (IPCA de 12 meses, fator `(1 + IPCA)^1,5`):
- **Mínimo comprovado:** o maior entre as compras de 36 meses e os bens ligados ao imóvel (ponderados pela chance de estarem lá).
- **Máximo de estoque:** 2,7 × as compras de 36 meses (uma casa acumula cerca de 8 anos de compras).
- **Piso:** R$ 15 mil (cesta mínima).

Por categoria: eletrônicos (base do **roubo**), eletrônicos + eletrodomésticos (base de **danos elétricos**), tudo (base de **danos por água**). Confiança dos bens: **ALTA** com compras + bens de vínculo forte (60% do valor ou mais), **MÉDIA** com um dos dois, **BAIXA** sem nenhum.

> [!decisao] A renda (D-08, PR #14)
> Na mentoria, o BB confirmou que renda não é dado sensível. Ela entra **só** nos bens de quem não tem compras nem bens ligados ao imóvel, combinada com a média da região. Fora da amostra, o erro cai de **40,5% para 22,7%**. Quem tem compras segue pelas compras, e a renda não entra em plano, elegibilidade, jornada nem confiança. Pode ser desligada em `parametros.RENDA_NOS_BENS_SEM_COMPRAS`. Na base de teste, nenhum caso usa a renda (todos têm compras).

## 5. O valor da casa (reconstrução)
`área × custo do m² × fator do padrão`:
- **custo do m²:** mínimo pelo **SINAPI** do estado (IBGE, sem desoneração) e máximo pelo **CUB R8-N oficial** (7 estados) ou SINAPI × 1,14 (RJ, PE e CE, sem CUB oficial);
- **fator do padrão:** econômico 0,85 · normal 1,0 · superior 1,30;
- **segundo risco** (apartamento, condomínio ou financiado): a estrutura tem seguro próprio, então o residencial cobre só **25% a 40%** (acabamentos), conforme as Condições Gerais (cl. 15.2). O terreno nunca entra.

## 6. Validação dos dados estimados (fora da amostra)
Calibra em metade da base de desenvolvimento e mede na outra, e vice-versa:

| Estimativa | Resultado |
|---|---|
| Área pelo IPTU e pela energia | erro mediano **15%** · a faixa contém a área real em **80,9%** (meta: 80%) |
| Padrão pelo IPTU/m² | intervalo certo em **97,8%** dos 180 estreitados |
| Compras de quem não tem (região × região + renda) | erro mediano **40,5% → 22,7%** |

## 7. Valores extremos e robustez
- Valores fora dos limites do produto ficam no limite, e a observação avisa que o excedente fica descoberto (subseguro).
- IPTU ou energia zerados não encolhem a área; área de 5.000 m² ou compras de R$ 900 mil não quebram nada (teste de extremos).
- A API recusa área zero ou negativa.

Próxima: [[02 - O motor passo a passo]]
