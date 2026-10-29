---
tags: [codigo, visao-geral, motor, metricas, apis]
atualizado: 2026-10-28
---
# 🚀 Visão geral do motor (comece aqui)

> [!info] Versão completa
> Cada dado, passo, métrica, fonte, saída e teste explicado em detalhe: [[00 - Índice (leia nesta ordem)]] (pasta 16 - Projeto por inteiro).

Uma página só com **o que o motor faz, que números ele entrega, de onde vêm os dados e onde está cada detalhe**. Números da base Teste Comum (138 casos), versão de 28/10 à noite.

> [!tip] Em uma frase
> O motor lê o que o banco já sabe do cliente (contas, compras, IPTU, energia, aluguel, financiamento) e devolve para cada imóvel um plano, as faixas de cada cobertura, até 3 perguntas e **o porquê, com os números do próprio cliente**. Funciona sem internet.

## 1. O que acontece com cada cliente-imóvel
```mermaid
flowchart TD
  A[Dados do banco] --> B[1 · Entender o imóvel<br>tipo, vínculo, uso, área, bens]
  B --> C[2 · Elegibilidade<br>NÃO só com prova; dúvida vira pergunta]
  C --> D[3 · Plano por pontos<br>Essencial, Prático ou Total]
  D --> E[4 · Faixa de cada cobertura<br>custo oficial do m² + bens a preço de hoje]
  E --> F[5 · Até 3 perguntas<br>as que mais apertam a faixa]
  F --> G[6 · Confiança e jornada<br>1 toque, app com perguntas ou gerente]
  G --> H[7 · Motivo para o cliente<br>fato dele, quanto perderia, o que fica descoberto]
  H --> I[(Ficha) → 2 planilhas · app · gerente · API]
```

| Passo | O que faz | Exemplo (apartamento em Curitiba) | Arquivo |
|---|---|---|---|
| 1 · Entender o imóvel | Deduz tipo, vínculo, uso, área e bens pelos dados | Apartamento, financiado (R$ 950/mês), 110 m², bens de R$ 22 mil a R$ 60 mil | `motor.py` |
| 2 · Elegibilidade | Só diz NÃO com prova; o resto vira pergunta | Elegível | `motor.py` |
| 3 · Plano | Três necessidades (aluguel, roubo e vidros, terceiros); o menor plano que cobre | Prático (gastou R$ 11 mil com vidros) + RC (prédio) | `motor.py` |
| 4 · Faixas | Reconstrução pelo SINAPI/CUB + bens pelo IPCA, dentro dos limites do produto | Incêndio de R$ 100 mil a R$ 203 mil | `motor.py` |
| 5 · Perguntas | Até 3, pelo quanto apertam a faixa | "Seus bens ficam entre R$ 22 mil e R$ 60 mil?" | `motor.py` |
| 6 · Confiança e jornada | Alta, média ou baixa por regra; gerente só em último caso | Confiança alta → 1 toque | `motor.py` |
| 7 · Motivo | O texto que o cliente e a banca leem | "Recomendamos o Prático porque você gastou R$ 11 mil com vidraçaria..." | `motivo.py` |

**Quando falta dado**, o motor não para:

| Falta | O que o motor faz | Casos |
|---|---|---|
| Área | Estima pelo IPTU e pela conta de luz; sem os dois, usa a média da região | 92 estimadas |
| Padrão de acabamento | Deduz pelo IPTU por m² (acerta 98%); senão, faixa aberta + pergunta | 25 pelo IPTU · 73 com pergunta |
| Compras | Média de compras de imóveis parecidos da região | 0 nesta base |
| Uso (mora lá?) | Confiança baixa + pergunta; vai ao gerente | 18 |

Mais detalhes: [[Mapa do código]] (cada função) · [[Plano - motivo, dados faltantes e gerente]].

### Quem vai direto e quem tem confiança baixa (28/10)
| Grupo | Casos | Perguntas | Para onde vai |
|---|---|---|---|
| Confiança **alta** | 17 | 1 ou 2 (sempre a dos bens; às vezes o acabamento) | 1 toque (15) · gerente (2, sem app) |
| **1 toque** | 67 | 1 a 3, todas de **ajuste de valor** (bens, acabamento, área) | Contrata no app |
| App com perguntas | 20 | Inclui uma de elegibilidade ("seu seguro atual é da BB?") | App |
| Confiança **baixa** | 20 | Sempre a de uso ("é onde você mora, veraneio ou alugado?") + área ou bens | Gerente (18) · sem proposta (2) |

- **Nenhum caso sai com 0 perguntas:** a dos bens aparece para todos, porque a faixa dos bens é sempre maior que R$ 5 mil.
- **Por que a confiança fica baixa:** nos 20 casos, o motor não sabe se a pessoa **mora** no imóvel (o endereço não bate com o principal, ou ela mora em outro imóvel cadastrado). Eles ainda recebem plano, faixas e motivo, mas a faixa de incêndio é mais larga (máximo ÷ mínimo 2,56, contra 1,89 na confiança alta) e a primeira pergunta é a do uso.
- **Em discussão:** separar pergunta que **trava** a contratação (elegibilidade, uso) de pergunta **opcional de ajuste** (bens, acabamento, área), e na confiança baixa perguntar o uso no app antes de chamar o gerente.

## 2. As métricas (o que provamos e onde)
Todas saem em `entrega/metricas.json` a cada execução.

> [!metrica] As que a banca mais vai olhar (o porquê)
> | Métrica | Valor | O que significa |
> |---|---|---|
> | Motivos genéricos | **0** de 138 | Ninguém recebe "não há sinais" |
> | Motivo com fato do próprio cliente | **100%** | Sempre um número dele (aluguel, compras, vidros...) |
> | Justificativa com o valor em risco | **100%** | Diz quanto ele perderia |
> | Alternativas mostradas | **100%** | Mais barato e mais completo (RN-37) |
> | Termos internos no texto | **0** | Sem "presumido", "estimado:"... |
> | Tamanho | mediana de **100 palavras** | Lê em menos de 1 minuto |

| Grupo | Métricas | Valores |
|---|---|---|
| **Pedidas pelo guia (§8)** | processados, com justificativa, coberturas completas, faixas vazias | 100% · 100% · 100% · 0 |
| | planos | Prático 66 · Total 38 · Essencial 34 (por necessidades: aluguel → Total; roubo → Prático) |
| | elegibilidade | SIM 138 (16 com pergunta obrigatória: "seu seguro é da BB?") |
| | confiança | alta 17 · média 101 · baixa 20 |
| | perguntas por caso | 2,78 (0,46 obrigatória) |
| | estabilidade, sensibilidade, reprodutibilidade | 1 caso muda com ±5% · área +10% → incêndio +4,7% · arquivos idênticos |
| **Responsabilidade** | teste de justiça (troca renda e idade) | **0** casos mudam |
| | regra dos 80% por faixa de renda | 1,00 |
| **Jornada** | 1 toque · app com perguntas · gerente | 63 · 49 · **26** (gerente: 19%, só obra ou sem app) |
| **Mercado** ([[Métricas do mercado x as nossas]]) | 1 toque puro · sem pessoa no meio | 45,7% · 81,2% dos elegíveis |
| | esforço: perguntas × campos de cotação comum | 2,7 × 19,9 (86% menos) |
| | ITV do incêndio (segurado ÷ valor em risco) | máximo 1,48 · mínimo 0,62 · sugerido ÷ pessimista 0,67 |
| **Validação fora da amostra** | erro da área · faixa contém a real · padrão pelo IPTU | 15% · 80,9% (73,9% na base de teste) · 98% |

## 3. As fontes externas e as APIs
> [!fonte] Regra
> O motor **nunca chama a internet enquanto roda**. Ele lê os dados salvos em `motor/externos/`. As fontes que têm API oficial são renovadas com `python motor/externos/coletar.py --ao-vivo`; se a API falhar, fica o último valor salvo, com a data. Fonte externa **só reforça**: o motor funciona só com a base do datathon (RN-12).

| Fonte | Para quê | Como chega | Data |
|---|---|---|---|
| **SINAPI** (IBGE) | Custo mínimo do m² para reconstruir | ✅ **API SIDRA**, ao vivo | set/2026 |
| **IPCA** (Banco Central) | Compras a preço de hoje | ✅ **API SGS**, ao vivo | até set/2026 |
| **CUB** (Sinduscons) | Custo máximo do m² | Site/PDF oficial (7 de 10 estados) | set/2026 |
| **FipeZAP** (Fipe) | Aluguel por m² (perda de aluguel) | PDF | set/2026 |
| **[[Atlas Digital de Desastres]] / S2iD** | Chuvas e vendavais na cidade (só no texto) | Arquivo oficial (sem API) | 1991–2025 |
| **[[ANEEL continuidade]]** | Quedas de energia da distribuidora (só no texto) | Ranking oficial | 2025 |
| Condições Gerais BB v1.4 | As regras do produto | PDF | v1.4 |

Detalhe de licença, transformação e limitações: `motor/externos/FONTES.md`.

## 4. Regras que mais pesam no motor
- **RN-07 (revisada em 28/10, mentoria BB):** idade e outros atributos pessoais nunca decidem nada. A **renda foi liberada** (não é dado sensível) e entra num ponto só: os bens de quem não tem compras nem bens ligados ao imóvel, combinada com a média da região (decisão D-08). Quem tem compras segue pelos **próprios gastos**, que são a evidência direta. A renda não decide plano, elegibilidade, jornada nem confiança. Ver [[Regras de negócio]].
- **RN-09:** estimativa sempre dita como estimativa.
- **RN-10:** CEP e coordenadas são fictícios (testamos: o CEP é ruído).
- **RN-12:** funciona sem dado externo.

## 5. Onde está cada coisa
| Quero ver... | Onde |
|---|---|
| Cada arquivo e função | [[Mapa do código]] |
| O que mudou e quando | [[Log de alterações do código]] |
| Erros encontrados e corrigidos | [[Auditoria do código - 28-10]] |
| Plano pós-mentoria (motivo, região, gerente, APIs) | [[Plano - motivo, dados faltantes e gerente]] |
| Métricas de bancos e seguradoras | [[Métricas do mercado x as nossas]] |
| Regras | [[Regras de negócio]] · [[Regras de negócio - arquivo para as IAs do grupo]] |
| Próxima tarefa (app) | [[Especificação do app v2 - ligado ao motor]] |
