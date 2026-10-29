---
tags: [dados]
status: dados-recebidos
atualizado: 2026-10-27
---
# Dicionário de dados

Pacote **Seguro Residencial** (dados sintéticos). No repositório: `data/raw/desenvolvimento/` e `data/raw/teste_comum/`. Achados em [[Achados iniciais dos dados]].

## Arquivos
| Arquivo | Desenvolvimento | Teste comum | 1 linha = | Chave |
|---|---|---|---|---|
| `clientes.csv` | 2.200 | 120 | cliente | `cliente_id` |
| `enderecos_imoveis.csv` | 2.578 | 138 | imóvel | `imovel_id` (+ `cliente_id`, `territorio_id`) |
| `sinais_imobiliarios.csv` | 2.578 | 138 | imóvel | `cliente_id` + `imovel_id` |
| `bens_compras.csv` | 8.988 | 494 | bem/compra | `bem_id` (+ `imovel_id_referencia`) |
| `territorio.csv` | 2.578 | 138 | território do imóvel | `territorio_id` |
| `catalogo_coberturas_fixas_planos.csv` | 25 | 25 | plano + cobertura fixa | |
| `template_resultado_times.csv` | 2.578 | 138 | cliente + imóvel (saída) | |
| `template_coberturas_times.csv` | só cabeçalho | só cabeçalho | cobertura (saída) | |
| `dicionario_dados.csv` | 97 campos | | | |

Natureza dos campos (guia): **cadastral/observado**, **derivado** (fórmula), **estimado** (premissa), mais confiança, origem e limitação.

## Clientes
| Campo | O que é | Observação |
|---|---|---|
| `idade` | atributo pessoal | **Não usar como atalho para patrimônio/risco** (guardrail) |
| `renda_mensal` | renda (não é dado sensível: mentoria BB, 28/10) | Pode ser usada como **reforço**, combinada com outros sinais; no motor, só nos bens de quem não tem compras (D-08) |
| `origem_renda` / `confianca_renda` | INFORMADA (ALTA) ou PRESUMIDA (MEDIA) | metade de cada |
| `indice_maturidade_digital`, `usuario_app`, `frequencia_acesso_app_90d` | uso digital | bom para escolher o **canal** (app × gerente) |
| `quantidade_dependentes`, `possui_pet_informado` | família | sinal para RC familiar |
| `qtd_produtos_seguridade` | quantos seguros tem | |
| `possui_seguro_residencial` | já tem seguro residencial BB | elegibilidade (mesmo endereço não pode) |

## Endereços e imóveis
| Campo | O que é | Observação |
|---|---|---|
| `complemento` | texto tipo "AP 204", "LOTE 04", "CASA FUNDOS" | ajuda a definir tipo |
| `possui_termo_apartamento/casa/bloco/condominio` | palavras achadas no endereço | apartamento × casa × casa em condomínio |
| `endereco_principal_compativel` | bate com o endereço principal do cliente | NAO → pode ser veraneio ou imóvel de terceiros |
| `area_cadastrada_m2` + `origem_area` + `confianca_area` | área | **61% sem área** (valor 0, NAO_DISPONIVEL) |
| `padrao_construtivo_cadastrado` | ECONOMICO / NORMAL / SUPERIOR | 73% sem dado |
| `material_parede_externa_cadastrado` | ALVENARIA | 78% sem dado (elegibilidade) |
| `situacao_imovel_cadastral` | REGULAR | todos regulares |
| `municipio_real`, `uf_real`, `codigo_ibge_municipio` | território real | 10 capitais |

## Sinais imobiliários
Aluguel pago, crédito recorrente compatível com aluguel (recebe aluguel), parcela de financiamento, condomínio, IPTU anual, energia, água, internet, compras de móveis/eletrodomésticos/eletrônicos (36 meses), gastos com material de construção e vidraçaria (24 meses).

## Bens e compras
`tipo_bem` (ELETRONICO, ITEM_LAZER, ELETRODOMESTICO, MOVEL), `valor_cadastrado`, se é da mesma UF/município, se foi financiado pelo banco, `probabilidade_bem_no_imovel_referencia` (estimado), `nivel_confianca_vinculo` (ALTA ≥ 0,76; MEDIA 0,56–0,66; BAIXA ≤ 0,48), `valor_bem_ponderado_referencia` = valor × probabilidade.

## Território
Coordenada **perturbada** (não é o domicílio real), `chave_enriquecimento_publico` = código IBGE + coordenada. Sem índices de risco: [[Enriquecimento externo]] é opcional.

Ligações: [[Achados iniciais dos dados]] · [[Elegibilidade residencial]] · [[Templates de entrega]]
