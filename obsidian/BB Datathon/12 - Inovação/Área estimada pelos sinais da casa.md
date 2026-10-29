---
tags: [inovacao, v2]
---
# Área estimada pelos sinais da casa

**O que é:** 61% dos imóveis não têm área. Estimamos a área pelo IPTU, energia, água, tipo (casa/apto) e município, com uma faixa (intervalo) e confiança menor que a área cadastrada.

**Dados que usa:** `pagamento_iptu_anual` (correlação 0,82 com a área), `energia_media_mensal_6m` (0,81), `agua_media_mensal_6m` (0,51), tipo e município. **Renda e idade ficam de fora**: a renda tem correlação 0,01 com a área, então não ajuda aqui (mesmo liberada desde 28/10), e a idade segue proibida pela RN-07.

**E o gerente?** Recebe a área já com a explicação: "estimada pelo IPTU e pela conta de luz".

**E quem tem dificuldade com app?** Nenhuma pergunta extra. Se a confiança for baixa, vira uma pergunta simples: "sua casa tem mais ou menos 120 m²?".

**Regras:** RN-07, RN-08, RN-13, RN-14, RN-32.

**Esforço:** Médio. Uma regressão linear simples por tipo de imóvel resolve, treinada nos 1.016 imóveis com área cadastrada.

Ligações: [[Ideias v2 - proposta para o time]] · [[Regras de negócio]]
