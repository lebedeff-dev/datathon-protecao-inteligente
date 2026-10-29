---
tags: [dados, enriquecimento, diferencial]
status: planejado
---
# Enriquecimento com dados externos (diferencial)

> [!success] Atualização 28/10
> Em uso: [[Atlas Digital de Desastres]] (S2iD), [[ANEEL continuidade]], SINAPI, CUB oficial de 7 UFs, IPCA e FipeZAP. Atlas e ANEEL só reforçam o motivo; SINAPI, CUB, IPCA e FipeZAP formam os valores das faixas. O motor roda sem eles, com valores neutros e confiança baixa (ver [[04 - Fontes externas e APIs]]). Os sinistros da BB (imprensa) saíram em 29/10. Detalhes em `motor/externos/FONTES.md`.

> O que foi dito na apresentação (ver [[Transcrição da apresentação]], ~14:25–15:02): a organização entrega **UF, código IBGE, setor e coordenada aproximada**, mas **não** entrega índices de **alagamento, vendaval e furto**. Buscar esses dados é **opcional**, mas **a solução tem que funcionar sem eles**.
> Regra nossa: só **fontes oficiais, confiáveis e com data conhecida**, e cada uma citada no template e na apresentação.

## Como encaixar no motor (sem quebrar nada)
```
base do datathon ──(código IBGE / lat-long)──► tabela de risco por município
                                                     │
                     tem dado? ── sim ──► índice 0–1 ajusta coberturas + entra no MOTIVO
                                 └─ não ──► valor neutro (mediana) + flag "sem dado externo"
```
- **Chave de junção:** código IBGE do município (7 dígitos). Para polígonos de risco, usar **lat/long** e um teste *ponto-dentro-de-polígono* (*point-in-polygon*, biblioteca **geopandas**).
- **Módulo separado:** `src/datathon/enriquecimento.py`. O motor roda com ele ligado ou desligado (*feature flag*), o que prova que a solução funciona sem os dados externos.
- **Rastreabilidade (data lineage):** cada índice guarda **fonte + data de referência**, e dados velhos reduzem a confiança, com a mesma lógica do [[Ideias|grau de confiança]].
- **No motivo:** *"Seu município teve 6 registros oficiais de vendaval nos últimos 10 anos (Defesa Civil), por isso sugerimos cobertura de vendaval na faixa X."*

## Fontes candidatas
| Risco | Cobertura afetada | Fonte oficial | Granularidade | Observação |
|---|---|---|---|---|
| Enchente, alagamento, deslizamento, vendaval, granizo | Danos à estrutura, vendaval, conteúdo, RC | **Atlas Digital de Desastres no Brasil** (MIDR/Sedec, dados do **S2iD**) | Município, por tipo e período | Dados oficiais da Defesa Civil já tratados. Ver se exporta CSV |
| Áreas de risco geológico/hidrológico | Reconstrução, conteúdo | **SGB/CPRM: Setorização de Riscos** (geoportal GeoNetwork) | Polígonos dentro do município | Usar lat/long do imóvel; nem todo município tem |
| População em área de risco | Reconstrução | **IBGE: BATER** (base territorial de áreas de risco, municípios monitorados pelo **CEMADEN**) | Setor/município | Estudo com base no Censo 2010. Procurar versão mais nova |
| Raios (descargas atmosféricas) | **Danos elétricos** | **INPE/ELAT**: ranking de densidade de raios por município | Município | Rankings públicos antigos; procurar o mais recente |
| Furto/roubo a residência | Roubo/furto de bens (conteúdo) | **SINESP** (Ministério da Justiça, dados abertos) e **SSP estaduais** | UF/município (nem todo crime tem recorte municipal) | Dados com lacunas; usar como índice relativo |
| Custo de reconstrução | **Reconstrução** | **IBGE: SINAPI**, custo médio do m² por UF (mensal) | UF | Média nacional por volta de R$ 1.985/m² (jul/2026). Baixar a série oficial |
| Custo de reconstrução (alternativa) | Reconstrução | **CUB/m²** dos Sinduscon estaduais | UF, por padrão de obra | Distingue padrão baixo/normal/alto |

> Ideia do grupo: [[Imagem de satélite]] (só no nível do município, porque as coordenadas da base são perturbadas).

## Prioridade (pouco tempo)
1. **SINAPI por UF**: a mais importante, porque é base direta da cobertura de reconstrução. Fácil de baixar e juntar por UF.
2. **Atlas Digital de Desastres**: um índice por município (enchente/vendaval/granizo) vira argumento forte no motivo.
3. **ELAT (raios)**: liga direto com danos elétricos, uma das coberturas citadas.
4. SINESP/SSP e SGB, só se sobrar tempo.

## Checklist
- [ ] Confirmar na mentoria se dados externos precisam ser citados no template
- [ ] Baixar SINAPI (UF) → `data/external/sinapi_uf.csv`
- [ ] Extrair índice de desastres por município (Atlas) → `data/external/desastres_municipio.csv`
- [ ] Tabela `docs/notas/02 - Dados/Fontes externas usadas` com link, data de acesso e data de referência
- [ ] Rodar o motor **com** e **sem** enriquecimento e comparar (mostrar na apresentação)

## Referências
- [Atlas Digital de Desastres no Brasil (MIDR)](https://atlasdigital.mdr.gov.br)
- [S2iD: manual de acesso (MIDR)](https://www.gov.br/mdr/pt-br/assuntos/protecao-e-defesa-civil/sistema-integrado-de-informacoes-sobre-desastres/01_m0-acesso-ao-sistema.pdf)
- [SGB: exemplo de ficha de setorização de risco (Guajará-AM)](https://geoservicos.sgb.gov.br/geonetwork/srv/api/records/0ef9e8ae-c9db-4d8c-b8d3-a5a031efad39)
- [IBGE: estudo de população em áreas de risco (BATER)](https://agenciadenoticias.ibge.gov.br/agencia-noticias/21566-estudo-inedito-mostra-moradores-sujeitos-a-enchentes-e-deslizamentos.html)
- [IBGE: SINAPI](https://www.ibge.gov.br/estatisticas/sociais/populacao/9270-sistema-nacional-de-pesquisa-de-custos-e-indices-da-construcao-civil.html) · [Caderno SINAPI ago/2026](https://ftp.ibge.gov.br/Precos_Custos_e_Indices_da_Construcao_Civil/Fasciculo_Indicadores_IBGE/sinapi_202608caderno.pdf)
- [Agência FAPESP: ELAT/INPE e incidência de raios](https://agencia.fapesp.br/pesquisa-do-inpe-e-nasa-mostra-regioes-do-mundo-com-maior-incidencia-de-raios/295)
- [Pacote BrazilCrime (acesso ao SINESP VDE)](https://cran.r-project.org/web/packages/BrazilCrime/readme/README.html)

## Ligações
[[SINAPI]] · [[Atlas Digital de Desastres]] · [[INPE ELAT]] · [[SINESP]] · [[SGB setorização de risco]] · [[Risco do território no motivo]]
