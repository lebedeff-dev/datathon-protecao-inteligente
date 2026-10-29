---
tags: [projeto, glossario, iniciante]
atualizado: 2026-10-29
---
# 📖 00b · Glossário: termos de seguro e de dados

Leia antes das outras notas. Cada termo tem uma explicação curta e um exemplo do projeto.

## Seguro
| Termo | O que é | Exemplo no projeto |
|---|---|---|
| **Seguro residencial** | Contrato que paga prejuízos na casa (estrutura e bens) e dá assistências (chaveiro, encanador) | O produto da BB Seguros que o desafio pede para recomendar |
| **Plano** | Pacote pronto de coberturas. A BB tem três: Essencial, Prático e Total. Cada um é o anterior mais algumas coberturas | Essencial (6 coberturas) → Prático (+ roubo e vidros) → Total (+ RC, aluguel, emergências) |
| **Cobertura** | Um tipo de prejuízo que o seguro paga | Incêndio, danos por água, danos elétricos, roubo... |
| **Cobertura adicional** | Uma cobertura de um plano acima que entra no plano escolhido sem trocar de plano (o guia permite, item 9.2) | A RC familiar entra no Prático de quem mora em prédio |
| **Importância segurada (ou limite)** | O **máximo** que o seguro paga numa cobertura. É o que as nossas faixas recomendam | Incêndio de R$ 100 mil a R$ 217 mil: o cliente escolhe um valor nessa faixa |
| **Faixa** | O mínimo e o máximo recomendados para a importância segurada de uma cobertura | Danos elétricos: R$ 12,5 mil a R$ 30 mil |
| **Valor sugerido** | O valor dentro da faixa que o motor recomenda escolher (o meio dela) | Incêndio: R$ 151 mil |
| **Limite do produto** | O mínimo e o máximo que o produto da BB aceita em cada cobertura | Incêndio: entre R$ 100 mil e R$ 600 mil |
| **Sinistro (ou acionamento)** | Quando algo acontece e o cliente pede o pagamento | Um raio queima a TV: o cliente aciona danos elétricos |
| **Primeiro risco absoluto** | Regra da BB (Condições Gerais, cl. 15.1): paga o prejuízo real até o limite, sem desconto proporcional | Limite de R$ 200 mil; o fogo destrói R$ 40 mil → paga R$ 40 mil |
| **Segundo risco** | Quando outro seguro paga primeiro (cl. 15.2). Em prédio ou casa financiada, o seguro do condomínio ou do financiamento cobre a estrutura; o residencial cobre o resto | Apartamento: o residencial cobre só os acabamentos (25% a 40% da reconstrução) e os bens |
| **Limite único** | Uma só importância para prédio e conteúdo no incêndio, com prioridade para o prédio (cl. 5.5–5.6) | — |
| **Reconstrução** | O custo de construir o imóvel de novo, sem o terreno | 110 m² × R$ 2.287 a R$ 3.561 por m² |
| **RC familiar (responsabilidade civil)** | Paga danos que você, a sua família ou o seu pet causem **a outras pessoas** | Um cano estoura e estraga o apartamento de baixo |
| **Perda de aluguel** | Paga outra moradia (inquilino) ou repõe o aluguel que deixa de entrar (dono que aluga), enquanto o imóvel é reparado | Só existe no Total |
| **Subseguro** | Segurar menos do que o valor em risco: num sinistro grande, parte do prejuízo fica com o cliente | Escolher o mínimo da faixa |
| **Superseguro** | Segurar mais do que pode perder (o Código Civil proíbe, art. 778) | Inquilino segurando a estrutura que é do dono |
| **ITV (insurance-to-value)** | Importância segurada ÷ valor em risco. Abaixo de 0,8, há subseguro | Sugerido ÷ cenário pessimista = 0,67 |
| **Elegibilidade** | Se o imóvel pode ser segurado (guia 9.1) | Imóvel em obra não pode; vira pergunta |
| **Condições Gerais (CG)** | O contrato oficial do produto (BB Seguro Residencial v1.4) | Usamos as cláusulas 5, 6, 15 e 24 |
| **Bancassurance** | Seguro vendido pelo banco aos próprios clientes | O cenário do desafio |

## Recomendação (o nosso motor)
| Termo | O que é |
|---|---|
| **Ficha** | O resultado do motor para um cliente-imóvel: plano, faixas, perguntas, confiança, jornada e motivo. Tudo sai dela |
| **Necessidade** | Um risco real que o cliente tem e que uma cobertura resolve. São três: **aluguel em jogo**, **roubo e vidros**, **danos a terceiros** |
| **Prova** | O dado do cliente que acende uma necessidade (ex.: "paga R$ 3 mil de aluguel") |
| **Força da recomendação** | **Clara** (a prova está longe do limite) ou **no limite** (a menos de 15% do limite) |
| **Pergunta decisiva** | Quando a recomendação está no limite, a pergunta cuja resposta decide o plano |
| **Pergunta obrigatória × opcional** | Obrigatória trava a contratação (elegibilidade, "mora aí?"); opcional só ajusta o valor |
| **Jornada** | O caminho de contratação: 1 toque, app com perguntas ou gerente |
| **Motivo (justificativa)** | O texto que explica o porquê, com os números do cliente |
| **Observado · estimado · presumido** | De onde veio o dado: da base (cadastro, contas) · calculado · suposto sem sinal |
| **Confiança** | Alta, média ou baixa, conforme os dados críticos sejam observados ou estimados |

## Dados e estatística
| Termo | O que é | Exemplo |
|---|---|---|
| **Base de desenvolvimento** | Os 2.578 imóveis com que o motor **aprende** | Mediana do IPTU por m² de cada cidade |
| **Base de teste** | Os 138 imóveis que o motor **responde**; vão para as planilhas | — |
| **Mediana** | O valor do meio quando se ordena tudo (metade abaixo, metade acima). Não é puxada por extremos como a média | Bens de R$ 36 mil = a mediana da base |
| **Percentil** | O valor abaixo do qual fica certa porcentagem | Percentil 9% e 91% definem a faixa da área |
| **Calibrar** | Aprender as referências numa base antes de usar em outra | IPTU por m² por cidade |
| **Backtest (validação fora da amostra)** | Esconder um dado que conhecemos e ver se o motor acerta | Esconder a área cadastrada: erro mediano de 15% |
| **Erro mediano** | A metade dos erros é menor que esse valor | 15% na área |
| **CSV** | Planilha em texto, uma linha por registro | As duas planilhas da entrega |
| **JSON** | Formato de texto para dados com campos | A ficha |
| **API** | Endereço na internet que devolve dados para um programa | SINAPI pela API do IBGE |
| **Código IBGE** | Número oficial de cada município | Curitiba = 4106902 |
| **SINAPI** | Custo médio do m² de construção por estado (IBGE) | PR: R$ 2.287/m² |
| **CUB** | Custo do m² de construção dos sindicatos da construção | PR: R$ 2.739/m² |
| **IPCA** | A inflação oficial (Banco Central/IBGE) | 4,58% em 12 meses |
| **Teste automático** | Código que confere outro código; roda com `python -m pytest -q` | 155 testes |
| **Reprodutível** | Rodar de novo dá exatamente o mesmo arquivo | Garantido por teste |

Próxima: [[01 - Os dados e como tratamos]]
