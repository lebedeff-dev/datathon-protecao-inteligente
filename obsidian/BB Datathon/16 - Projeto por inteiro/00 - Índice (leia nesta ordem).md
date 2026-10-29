---
tags: [projeto, indice, documentacao]
atualizado: 2026-10-28
---
# 📚 O projeto por inteiro (leia nesta ordem)

Tudo o que o projeto faz, explicado do zero: os dados, o tratamento, cada passo do motor, cada métrica, as fontes, as saídas, os testes e as regras. Números da versão de 28/10 à noite (base Teste Comum, 138 casos; **105 testes passando**).

> [!tip] Se só der tempo de ler uma coisa
> [[Visão geral do motor (comece aqui)]] resume tudo numa página. Esta pasta é a versão completa, para entender e defender cada detalhe na banca.

| # | Nota | Responde |
|---|---|---|
| 1 | [[01 - Os dados e como tratamos]] | Que dados recebemos, o que falta e o que fazemos com cada lacuna |
| 2 | [[02 - O motor passo a passo]] | Como sai o plano, cada faixa, cada pergunta, a confiança, a jornada e o motivo (com as fórmulas) |
| 3 | [[03 - Cada métrica explicada]] | O que cada número do `metricas.json` mede, como é calculado e por que importa |
| 4 | [[04 - Fontes externas e APIs]] | De onde vem cada dado de fora, como atualiza e o que acontece sem internet |
| 5 | [[05 - Saídas - planilhas, ficha, API e demo]] | O que vai em cada coluna das planilhas, o que tem na ficha e como a API e a demo usam |
| 6 | [[06 - Testes e qualidade]] | Os 105 testes, o que cada grupo prova e como rodar |
| 7 | [[07 - Regras, decisões e pendências]] | Que regra cada parte atende, as decisões do time e o que ainda falta decidir |
| 8 | [[08 - Perguntas da banca e respostas]] | As perguntas difíceis, com a resposta e o número de cada uma |
| 9 | [[09 - Cada escolha conta por conta]] | **Dois clientes reais seguidos passo a passo**, com cada conta e de onde vem cada número fixo |
| 10 | [[Mapa do código]] | Cada arquivo e cada função |

## O projeto em 5 frases
1. **Problema:** o cliente não sabe responder "quanto valem seus eletrônicos?" e desiste, ou contrata um seguro que não serve para a casa dele.
2. **Solução:** um motor de regras explicáveis que lê o que o banco já sabe e monta, para cada cliente-imóvel, uma **ficha** com plano, faixas, perguntas, confiança e o porquê.
3. **O diferencial:** o **motivo** fala com os números do próprio cliente ("você gastou R$ 11 mil com vidraçaria"; "reconstruir custaria cerca de R$ 394 mil") e diz o que fica descoberto se ele escolher menos.
4. **Duas jornadas, uma ficha:** o cliente contrata no app (1 toque); o gerente só entra em último caso (obra ou cliente sem app) e recebe a mesma ficha como relatório.
5. **Provar, não prometer:** testes de justiça, validação fora da amostra, fontes oficiais com data e geração reprodutível.

## Como rodar tudo
```bash
pip install -r requirements.txt
python -m pytest -q                        # 105 testes
python motor/gerar.py --entrega            # 2 planilhas + métricas + fichas da demo
python motor/externos/coletar.py --ao-vivo # opcional: SINAPI e IPCA pelas APIs oficiais
```
