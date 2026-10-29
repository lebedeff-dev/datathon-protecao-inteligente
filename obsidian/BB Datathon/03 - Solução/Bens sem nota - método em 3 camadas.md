---
tags: [solucao, calculo, conteudo, regras]
data: 2026-10-28
status: proposta
---
# Bens sem nota: método em 3 camadas

**Problema levantado pelo time:** nem todo bem tem histórico de compra. A pessoa ganhou de presente, comprou usado, comprou em outro banco ou está começando a vida. O desgaste de um bem usado é incerto.

## 1. Dá para usar o salário? **Sim, desde 28/10, como reforço.**
> [!decisao] Atualizado depois da mentoria com o BB (28/10)
> Antes respondíamos "não" pela RN-07. Na mentoria, o BB confirmou que **renda não é dado sensível** (a LGPD, art. 5º, II, também não a lista). A regra foi revisada (D-08).
- **Onde entra:** como uma camada extra para quem **não tem compras nem bens ligados ao imóvel**: compras estimadas = média geométrica entre a média da região e renda × (compras ÷ renda do município). Fora da amostra, o erro mediano cai de **40,5%** (só região) para **22,7%** (região + renda).
- **Onde não entra:** quem tem compras segue pelas compras (a prova vence a estimativa); a renda não decide elegibilidade, canal nem confiança, e nunca decide sozinha (RN-08).
- **O cuidado que continua:** usar só a renda trataria igual quem ganha bem e mora com pouco, e penalizaria quem tem renda baixa e bens herdados. Por isso ela é combinada com a região e o cliente lê no motivo que a renda entrou ("estimamos ... e pela sua renda").
- **Argumento de pitch:** "A renda explica muito dos bens (correlação 0,88). Depois da mentoria passamos a usá-la, mas só onde falta prova, e sempre junto com outro sinal."

## 2. Dá para usar Open Finance?
- **No MVP: não como dado.** Ele não vem na base do datathon (RN-06) e inventar extratos seria apresentar estimativa como fato (RN-09).
- **Como "próximo passo", sim:** com consentimento do cliente (validade de até 12 meses, finalidade clara), o BB poderia ver compras feitas em cartões de outros bancos. O cartão de crédito já faz parte do compartilhamento de dados; o Banco Central ainda discute o escopo.
- **Limite:** Open Finance mostra compras. Não mostra presente, herança nem bem usado comprado em dinheiro. Ou seja, ajuda, mas não resolve sozinho.
- **No protótipo:** dá para mostrar a **tela de consentimento** ("Quer trazer suas compras de outros bancos para calcular melhor?"), sem usar números inventados.

## 3. O método (permitido pelas regras)
### Base: segurar pelo **valor de novo** (reposição)
Quanto custaria comprar tudo de novo hoje. Assim, **não importa como o bem chegou** (compra, presente, usado): o que conta é quanto custa repor. Esse é o modelo mais comum no Reino Unido ("new-for-old"). O desgaste só aparece na explicação do sinistro, e só se a apólice pagar valor atual (pergunta para a mentoria).

### Camada 1: piso pelo tamanho do imóvel
- Inspiração: seguro de conteúdo **por número de quartos** no Reino Unido (bedroom-rated), em que a seguradora define o valor dos bens pelo tamanho da casa, sem perguntar o que o cliente comprou.
- Na nossa base não há quartos, mas há área. Medido nos 1.016 imóveis com área observada (desenvolvimento), valor de bens por m²:

| Tipo | 25% mais baixos (P25) | Mediana | P75 |
|---|---|---|---|
| Apartamento | R$ 188/m² | R$ 284/m² | R$ 509/m² |
| Casa | R$ 146/m² | R$ 208/m² | R$ 333/m² |

- **Piso = área × P25 do tipo.** Cobre quem ganhou tudo de presente ou não tem histórico, porque depende da casa, não da pessoa.
- Usa só sinais do imóvel (área e tipo). Nada de renda ou idade.

### Camada 2: evidência (o que o banco vê)
- Compras de 36 meses (móveis, eletrodomésticos, eletrônicos) e bens cadastrados, corrigidos pela inflação (valor de novo).
- Bens com vínculo de confiança baixa com o imóvel entram com peso menor (a base já traz a probabilidade).

### Camada 3: o cliente confirma (só quando precisa)
- Se a evidência ficar abaixo do piso, ou a confiança for baixa, **uma pergunta de faixa**: *"Se você tivesse que comprar tudo de novo hoje, quanto gastaria mais ou menos?"* [até R$ 20 mil] [R$ 20 a 50 mil] [R$ 50 a 100 mil] [mais de R$ 100 mil]
- Depois de contratar, no "Meu seguro": **inventário guiado por cômodo** (foto e valor), opcional. Inspiração: o app de inventário da NAIC (associação dos reguladores de seguro dos EUA), que organiza os bens por cômodo, com foto e código de barras.

### Faixa de conteúdo
```
mínimo = maior entre (piso por m²) e (evidência no valor de novo)
máximo = maior entre (área × P75 do tipo) e (evidência × 1,25)
se o cliente respondeu a pergunta de faixa → a faixa passa a ser a resposta dele, limitada por piso e teto do produto
```

## 4. Exemplos
| Caso | Situação | Piso (camada 1) | Evidência (camada 2) | Faixa | Pergunta? |
|---|---|---|---|---|---|
| CASO_00005, apto 110 m², Curitiba | Tem compras recentes | 110 × 188 = **R$ 20.680** | **R$ 21.586** | R$ 21.586 a R$ 55.990 | Não |
| Apto 60 m², jovem saindo de casa, móveis de presente | Quase sem compras no banco | 60 × 188 = **R$ 11.280** | R$ 3.000 | R$ 11.280 a R$ 30.540 | **Sim** (evidência abaixo do piso) |
| Casa 200 m², bens herdados | Compras de 36 meses baixas | 200 × 146 = **R$ 29.200** | R$ 8.000 | R$ 29.200 a R$ 66.600 | **Sim** |

O segundo e o terceiro casos são o ponto do time: sem histórico de compra, o piso pelo imóvel garante uma faixa defensável (RN-32), e a pergunta ajusta.

## 5. Onde aparece
- **Template:** a cobertura de incêndio (imóvel + conteúdo) usa essa faixa de conteúdo; `dados_utilizados` cita área, tipo e compras; `informacao_a_confirmar` cita a pergunta de faixa quando ela foi necessária.
- **App (tela "Sua casa"):** *"Seus bens: estimamos entre R$ X e R$ Y pelo tamanho do seu apê e pelas suas compras. Ganhou coisas de presente ou tem móveis antigos? Isso também entra."*
- **Gerente:** "Mesmo quem não comprou nada com o BB tem uma faixa mínima pelo tamanho do imóvel."
- **Pitch:** teste de justiça (trocar a renda não muda nada) + "funciona para quem está começando a vida".

## Fontes
- Seguro de conteúdo por quartos e new-for-old: [Which?](https://www.which.co.uk/money/insurance/home-insurance/guides/home-insurance-explained) · [Choose](https://choose.co.uk/guide/contents-insurance-cover) · [Sheffield (esquema municipal)](https://www.sheffield.gov.uk/sites/default/files/2025-08/home-contents-insurance-250075-sheffield-s37-web-pack.pdf)
- Inventário por cômodo: [NAIC Home Inventory (Wisconsin OCI)](https://oci.wi.gov/Pages/Consumers/NAIC-Home-Inventory-App.aspx) · [NerdWallet](https://www.nerdwallet.com/insurance/homeowners/learn/home-inventory-app-template)
- Open Finance: [Finsiders (cartões)](https://finsidersbrasil.com.br/noticias-sobre-fintechs/trazer-cartoes-para-o-open-finance-esta-na-mesa-diz-bc) · [Convergência Digital (62 milhões de consentimentos)](https://convergenciadigital.com.br/mercado/open-finance-adesao-quase-dobra-em-12-meses-e-chega-a-62-milhoes-de-consentimentos/) · [Let's Money (revisão do BC)](https://www.letsmoney.com.br/noticias/banco-central-revisa-parcerias-dados-open-finance/)

Ligações: [[Como calcular o valor dos bens e da casa]] · [[Regras de negócio]] · [[Conteúdo]] · [[Open Insurance com consentimento]] · [[Painel de evidências]]
