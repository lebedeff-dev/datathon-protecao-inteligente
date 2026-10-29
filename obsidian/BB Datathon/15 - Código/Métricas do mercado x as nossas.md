---
tags: [codigo, metricas, pesquisa, mercado]
data: 2026-10-28
---
# 📊 Métricas do mercado x as nossas

O que bancos e seguradoras medem, se a gente mede, e com que dado. Regra desta nota: **só entra métrica com dado real e verificável**, e o motor continua funcionando **sem** nenhuma fonte externa (RN-12). Fonte externa só reforça o motivo ou aperta a faixa.

> [!tip] Números mais recentes
> A tabela atualizada de todas as métricas está em [[Visão geral do motor (comece aqui)]] (STP agora é 63%, com o app com perguntas).

> [!metrica] Os números novos (base Teste Comum, `entrega/metricas.json`)
> - **STP (vai direto ao 1 toque):** 48,6% dos casos
> - **Esforço:** uma cotação tradicional pede em média **19,9 campos**; a nossa jornada faz **2,7 perguntas** → **86,4% menos esforço**
> - ~~Aderência aos sinistros reais~~: **retirada em 29/10**, junto com o dado de sinistros da BB (fonte de imprensa, sem como auditar)
> - **ITV do incêndio:** o máximo da faixa cobre o valor em risco (mediana 1,46); o mínimo fica em 0,60 → mostrar valor sugerido no meio
> - **Backtest fora da amostra:** área com erro mediano de **15%** e faixa que contém a área real em **78%** (meta: 80%); padrão pelo IPTU certo em **97,8%**

## 1. Métricas de mercado que agora calculamos
| Métrica | Quem usa e como | Como medimos | Dado |
|---|---|---|---|
| **STP** (*straight-through processing*) | Seguradoras: % de propostas sem intervenção manual | % de casos que vão ao One Click (elegível, sem pendência, confiança não baixa, usuário do app com maturidade ≥ 40) | Base do datathon |
| **Esforço economizado** | Gartner/CEB (*Customer Effort Score*): menos esforço prevê lealdade | Campos de uma cotação tradicional (5 dados do imóvel + 6 declarações de elegibilidade + 1 valor por cobertura) × nossas perguntas | Guia §9.1 + catálogo |
| **ITV** (*insurance-to-value*) | Seguradoras de imóvel nos EUA e no Reino Unido; referência de 80% do custo de reconstrução nas cláusulas de ITV | Importância segurada de incêndio ÷ valor em risco (reconstrução SINAPI/CUB + bens) | SINAPI (IBGE) + base |
| **Faixas limitadas pelo produto** | Subseguro (Código Civil, art. 778) | Coberturas em que a estimativa passa do limite | Base + limites do app |
| **Aderência ao perfil de sinistros** | Seguradoras precificam e desenham produto pela frequência de sinistros | % das recomendações com as coberturas mais acionadas | Dados da BB Seguros (abaixo) |
| **Backtest fora da amostra** | Bancos validam modelos assim (Fed SR 11-7; BCBS 239) | Calibra em metade da base de desenvolvimento, mede na outra | Base de desenvolvimento |

> [!fonte] Sinistros da BB Seguros (RETIRADO do motor em 29/10: fonte secundária, de imprensa; fica só como registro)
> Carteira do Seguro Residencial BB, **jan/2023 a mai/2026**: danos elétricos **53,3%** · danos por água **14,6%** · vendaval e granizo **11,5%** · roubo e furto com arrombamento **2,1%**. Em **jan–jul/2026**: mais de 13,5 mil acionamentos, cerca de R$ 47 milhões em indenizações (≈ R$ 3,5 mil por acionamento) e danos elétricos em cerca de **66%**.
> Fontes: [Monitor Mercantil, 22/07/2026](https://monitormercantil.com.br/mais-da-metade-dos-sinistros-residenciais-envolve-danos-eletricos/) · [release da Brasilseg reproduzido pelo Legismap, 09/09/2026](https://legismap.com.br/conteudos/artigos-e-noticias/os-riscos-dentro-de-casa-mudaram-e-a-forma-de-proteger-o-patrimonio-tambem). Salvo em `motor/externos/sinistros_residencial_bb.csv`.
> **Como o motor usava:** só no texto do motivo, nunca no valor. Saiu em 29/10 (teste `test_sem_dado_de_sinistro_da_bb`); nenhum plano ou faixa mudou.

## 2. O que conferimos contra o mercado
| Nosso | Mercado | Bate? |
|---|---|---|
| Danos elétricos em **todos** os planos (vem no Essencial) | É a causa de 53% a 66% dos acionamentos da BB | ✅ coerente |
| Roubo puxa o Prático (59 casos) | Roubo é só 2,1% dos acionamentos da BB | 🟡 coerente em valor (sinistro raro, mas caro), mas vale explicar no pitch que o Prático é proteção de cauda |
| Faixa q10–q90 da área | Deveria conter a área real ~80% das vezes | ✅ 78,3% fora da amostra |
| Penetração do seguro residencial | 17% dos domicílios (FenSeg/CNseg, dado de **2021**; matérias de 2026 repetem o número) | Contexto para o pitch; não é métrica do motor |
| Subseguro | EUA: estudos com 60% a 71% dos imóveis subsegurados ([Insurance Business](https://www.insurancebusinessmag.com/us/news/catastrophe/insurers-own-rebuild-estimates-are-driving-most-underinsurance-study-finds-591416.aspx)) | Nosso ITV mostra o mesmo risco se o cliente escolher o mínimo |

## 3. Sinal novo sem API externa: padrão pelo IPTU
> [!codigo] Por que funciona
> A **planta genérica de valores** do IPTU considera o padrão de acabamento ao calcular o valor venal (ex.: [lei de Valença-RJ](https://valenca.rj.gov.br/wp-content/uploads/2013/08/Lei-Complementar-126.pdf)). Então, com a área cadastrada, o IPTU por m² comparado à mediana do município indica o padrão.
> Na base de desenvolvimento, a mediana dessa razão é **0,82** no econômico, **0,98** no normal e **1,32** no superior. Abaixo de 0,90 o motor descarta o superior; acima de 1,15, o econômico. Fora da amostra: 180 de 273 estreitados, **97,8%** certos.

## 4. Fontes territoriais (atualizado 28/10 à noite)
> [!success] Já em uso (só no texto do motivo)
> - **[[Atlas Digital de Desastres]] (S2iD):** registros oficiais de chuva, alagamento e enxurrada (água) e de vendaval e granizo (vento) nas 10 capitais, de 1991 a 2025.
> - **[[ANEEL continuidade]]:** posição da distribuidora de cada capital no ranking de quedas de energia de 2025 (danos elétricos).
> - **CUB oficial:** agora 7 de 10 estados (MG, RS e PR conferidos nos sites oficiais); a razão para os outros 3 passou de 1,09 para 1,14.

| Fonte | O que traria | Para quê | Status |
|---|---|---|---|
| **SUSEP SES** (ramo 0114, Compreensivo Residencial) | Prêmios e sinistros por seguradora e UF, atualizado semanalmente ([SES](https://www2.susep.gov.br/menuestatistica/ses/principal.aspx)) | Sinistralidade por UF no motivo; penetração por UF | Base completa para download; falta montar o recorte |
| **ANEEL DEC/FEC** por conjunto elétrico | Quedas de energia no bairro, não só na distribuidora | Motivo de danos elétricos mais local | ✅ ranking por distribuidora em uso; conjunto elétrico é o próximo passo (30 MB) |
| **Atlas Digital de Desastres** (MIDR/S2iD) | Registros oficiais por município, 1991–2025 | Motivo de vendaval e danos por água | ✅ em uso |
| **CUB oficial** de RJ, PE e CE | Máximo do custo do m² | Fecha a issue #11 | 🟡 MG, RS e PR feitos; os sites de RJ, PE e CE estavam fora do ar ou sem o valor |

> [!regra] Como uma fonte nova entra no motor
> CSV em `motor/externos/` + linha no `FONTES.md` (fonte, data de acesso, licença, nível, transformação, limitação) + leitura em `parametros.py` que devolve `None` quando o arquivo falta + teste mostrando que o motor roda sem ela (RN-11, RN-12).

Ligações: [[Métricas de bancos e seguradoras]] · [[Auditoria do código - 28-10]] · [[Mapa do código]] · [[Enriquecimento externo]] · [[Danos elétricos]]
