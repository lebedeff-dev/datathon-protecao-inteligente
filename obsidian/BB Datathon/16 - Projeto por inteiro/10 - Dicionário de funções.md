---
tags: [projeto, codigo, funcoes, iniciante]
atualizado: 2026-10-29
---
# 🔤 10 · Dicionário de funções (todas, uma a uma)

Cada função do projeto, em português simples. Para cada uma: **o que faz**, **recebe → devolve**, um **exemplo** e **por quê** (a regra ou a necessidade que ela atende). Os termos estão no [[00b - Glossário (termos de seguro e de dados)]].

> [!tip] Como ler código sem saber programar
> - Uma **função** é uma receita com nome: recebe ingredientes (os parâmetros) e devolve um resultado.
> - `r` é sempre **uma linha de dados de um cliente-imóvel** (o cadastro, as contas e o cliente juntos).
> - `cal` é a **calibração**: as referências que o motor aprendeu na base de desenvolvimento.
> - Uma função cujo nome começa com `_` é auxiliar, usada só dentro do próprio arquivo.

## Os 8 arquivos
| Arquivo | Papel |
|---|---|
| `motor/motor.py` | O motor: decide tudo e monta a ficha |
| `motor/motivo.py` | Escreve o texto que o cliente lê |
| `motor/parametros.py` | Guarda os números fixos e lê as fontes externas |
| `motor/metricas.py` | Calcula as provas para a banca |
| `motor/templates.py` | Confere as planilhas antes de gravar |
| `motor/gerar.py` | Roda tudo de ponta a ponta |
| `motor/api.py` | Serve a ficha pela internet (demonstração) |
| `motor/externos/coletar.py` | Atualiza as fontes externas pelas APIs |

---

## 1. `motor/motor.py`: o motor

### 1.1 Ler e aprender
| Função | O que faz | Recebe → devolve | Exemplo | Por quê |
|---|---|---|---|---|
| `carregar(origem)` | Lê as 5 tabelas, os 2 modelos de planilha e o catálogo, de uma pasta ou do zip oficial | caminho → dicionário de tabelas | `carregar("dados/teste_comum")` | Ponto de entrada dos dados |
| `calibrar(dados)` | Aprende as referências na base de desenvolvimento: IPTU e luz por m² por cidade, faixa de erro da área, médias da região, razão compras ÷ renda, backtests e teste do CEP | tabelas → `cal` | Curitiba: IPTU R$ 13,75/m² | O motor precisa de referências para estimar o que falta |
| `_calibrar_area(a)` | A parte do aprendizado que usa imóveis com área conhecida | imóveis com área → referências | Percentis 9% e 91% do erro = 0,728 e 1,299 | Separada para o backtest poder recalibrar em metades |
| `backtest(a)` | Divide a base em 2 metades, aprende numa e mede na outra: erro da área e acerto do padrão pelo IPTU | imóveis → resultados | Erro mediano 15%; faixa contém a real em 80,9% | Provar que a estimativa funciona (RN-47) |
| `teste_cep(a)` | Mede se o CEP explica o IPTU/m² melhor que um CEP sorteado | imóveis → R² do CEP e do sorteado | 0,215 contra 0,223 | Mostrar que o CEP da base é ruído (RN-10) |
| `_tipo_simples(df)` | Classifica cada imóvel como APTO ou CASA | tabela → coluna | — | Usado nas médias da região |
| `_degraus(df, coluna)` | Calcula a mediana de um dado em cada "degrau" regional (cidade + tipo, cidade, estado, geral), só com 20+ imóveis | tabela, coluna → tabela de medianas | Apartamentos de Belo Horizonte: 95 m² | Média da região para dado faltante (mentoria) |
| `regional(cal, campo, r)` | Busca a mediana do degrau mais próximo que tem dados | calibração, campo, cliente → (valor, degrau, nº de imóveis) | Londrina (fora da base) → sobe para o Paraná | Nunca ficar sem estimativa |
| `_compras_por_renda(...)` | Razão compras ÷ renda por cidade | imóveis com compras → razões | — | Base do uso da renda (D-08) |
| `_renda(r)` | Lê a renda como número; devolve vazio se faltar, for zero ou texto | cliente → número ou vazio | — | Não quebrar com dado ruim |
| `compras_pela_renda(r, cal)` | Compras esperadas pela renda do cliente | cliente → R$ ou vazio | — | Só para quem não tem compras |
| `_regiao_e_renda(med, pela_renda)` | Mistura região e renda (média geométrica), presa entre 0,5× e 2× a região | dois valores → um valor | Região 30 mil, renda 50 mil → 39 mil | A renda nunca decide sozinha (RN-08) |
| `_compras_sem_prova(r, cal)` | Estima as compras de quem não tem nenhuma | cliente → compras, fonte, degrau, usou renda? | — | Tratar o dado faltante |
| `backtest_bens_sem_compras(...)` | Finge que quem tem compras não tem e mede o erro da estimativa | imóveis → erros | Região 40,5% → região + renda 22,7% | Justifica o uso da renda |

### 1.2 Ferramentas pequenas
| Função | O que faz | Exemplo |
|---|---|---|
| `_positivo(v)` | Diz se é um número maior que zero | `_positivo(0)` → não |
| `dado(...)` | Monta um dado com valor, natureza, confiança, fonte, tipo de fonte e idade | `dado(110, "OBSERVADO", "ALTA", "área cadastrada")` |
| `arred(v)` | Arredonda reais: de 500 em 500 até R$ 20 mil, de 1.000 em 1.000 acima | 18.644 → 18.500 |
| `faixa(lo, hi, cob)` | Prende a faixa nos limites do produto e arredonda | Incêndio 85 mil → 100 mil (mínimo do produto) |
| `pior(*confs)` | Devolve a pior confiança da lista | ALTA, MÉDIA → MÉDIA |
| `brl(v)` | Escreve em reais com ponto de milhar | 2287 → "R$ 2.287" |

### 1.3 Entender o imóvel
| Função | O que faz | Recebe → devolve | Exemplo | Por quê |
|---|---|---|---|---|
| `tipo_pelo_complemento(...)` | Lê o complemento do endereço (AP, BLOCO, CASA, LOTE) | texto → APARTAMENTO, CASA ou nada | "BLOCO B APTO 305" → apartamento | Conferir o tipo |
| `inferir_tipo(r)` | Decide apartamento, casa em condomínio ou casa pelos termos do endereço; marca se o complemento diverge | cliente → dado | "apartamento" no endereço → APARTAMENTO | Tipo muda o segundo risco e o vendaval |
| `inferir_vinculo(r)` | Decide inquilino (paga aluguel), financiado (paga parcela), locador (recebe aluguel e não mora) ou proprietário | cliente → dado | Parcela de R$ 950 → FINANCIADO | Vínculo decide a necessidade de aluguel |
| `inferir_uso(r, outro_principal)` | Decide moradia, alugado a terceiros ou veraneio | cliente → dado | Endereço principal → moradia | Veraneio muda o roubo |
| `_area_estimada(r, cal)` | Área = 0,6 × (IPTU ÷ IPTU/m²) + 0,4 × (luz ÷ luz/m²); usa só o que existe | cliente → m² | 1.650 ÷ 14,08 e 500 ÷ 3,52 → 127 m² | Área faltante |
| `iptu_relativo(r, cal)` | IPTU/m² do imóvel ÷ o da cidade (só com área cadastrada) | cliente → razão | 16,36 ÷ 13,75 = 1,19 | Deduzir o padrão |
| `inferir_area(r, cal)` | Usa a área cadastrada; senão estima pelo IPTU e luz; senão a média da região | cliente → dado com faixa | 127 m² (92–165) | A base do valor da casa |
| `_ancoras(compras, bens)` | Mínimo = maior(compras, bens ligados) × IPCA; máximo = 2,7 × compras × IPCA | valores → (mín, máx) | 20.750 → 22.190 a 59.914 | Bens a preço de hoje |
| `estimar_bens(r, bens, cal)` | Faixa dos bens por categoria (eletrônicos, eletrodomésticos, móveis) e as bases de roubo, danos elétricos e água. Sem compras: média da região (e renda) | cliente → dado | Bens de R$ 22 mil a R$ 60 mil | O que tem dentro de casa |
| `valor_imovel(...)` | Reconstrução = área × custo do m² (SINAPI a CUB) × padrão; marca segundo risco e "estrutura do locador" | cliente → valores | R$ 252 mil a R$ 392 mil | Valor do incêndio |

### 1.4 Decidir
| Função | O que faz | Recebe → devolve | Exemplo | Por quê |
|---|---|---|---|---|
| `avaliar_elegibilidade(r, uso, n)` | Diz se pode contratar. NÃO só com prova; obra, seguro existente e material viram pergunta obrigatória | cliente → SIM/NÃO, pendências, avisos | R$ 26 mil em obra → "Está em obra?" | RN-15 a RN-19 |
| `familia_declarada(r)` | Diz se há dependentes e se informou pet | cliente → (sim/não, sim/não) | — | Acende a necessidade de terceiros |
| `_forca_por_limite(v, limite)` | "No limite" se o valor está a menos de 15% do limite; senão "clara" | valor, limite → força | 9.411 ÷ 10.000 = 0,94 → no limite | Dizer quando a decisão foi por pouco |
| `avaliar_necessidades(...)` | As três perguntas: **aluguel em jogo**, **roubo e vidros**, **danos a terceiros**, cada uma com sim/não, prova, força e (se no limite) a pergunta que decide | cliente → 3 necessidades | Inquilino → aluguel: sim, claro | O coração da recomendação |
| `escolher_plano(...)` | O menor plano que cobre as necessidades: aluguel → Total; roubo → Prático; senão Essencial. Monta o motivo, a alternativa e a força | cliente → plano e textos | Vidraçaria → Prático, claro | RN-20, RN-37 |
| `coberturas_adicionais(r, tipo, plano)` | RC familiar como adicional quando há necessidade de terceiros e o plano não é o Total | → lista de adicionais | Prédio → RC adicional | Guia 9.2 |
| `contexto_territorio(cob, r)` | Frase com dado oficial da cidade (Defesa Civil para água e vento, ANEEL para danos elétricos) | cobertura, cliente → frase | "Em Curitiba, a Defesa Civil registrou 10 vendavais..." | Motivo local |
| `faixa_bruta_incendio(ctx)` | Incêndio antes dos limites: reconstrução + bens (segundo risco: 25–40%; inquilino de casa: só bens) | contexto → (mín, máx) | 85 mil a 217 mil | Base do incêndio e das emergências |
| `dimensionar(cob, ctx)` | A faixa de uma cobertura, com confiança, dados usados, regra, justificativa, o que confirmar, observação e valor sugerido | cobertura → linha da planilha 2 | Danos elétricos: R$ 12,5–30 mil | RN-30 |
| `saida(...)` (dentro de `dimensionar`) | Prende a faixa, avisa subseguro, cita sinistros reais e território, calcula o sugerido | → dicionário da cobertura | — | Evita repetir o mesmo acabamento em cada cobertura |

### 1.5 Perguntar e medir a confiança
| Função | O que faz | Exemplo | Por quê |
|---|---|---|---|
| `valor_da_informacao(...)` | Quantos R$ cada resposta (bens, área, acabamento) pode tirar da faixa | Área: R$ 278 mil | Perguntar primeiro o que mais importa |
| `montar_perguntas(...)` | Junta as candidatas, ordena pela prioridade, corta as que valem menos de R$ 5 mil e fica com 3; marca obrigatória ou opcional | Pergunta decisiva (65) antes das de valor (58, 56, 54) | RN-36 |
| `peso_dado(d, campo)` | Nota de 0 a 1 = peso da fonte × frescor (dado velho vale menos) | Transação de 3 meses: 0,8 × 0,84 | Detalhe da confiança |
| `campos_faltantes(r)` | Quais campos do imóvel vieram vazios | área, padrão, material | Completude |
| `classe_dado(d, campo)` | Observado, estimado ou presumido; observado mais velho que a meia-vida vira estimado | — | RN-09 |
| `confianca_geral(...)` | Alta (5 observados, sem pendência), baixa (presumido em área ou bens, ou presumido + estimado), média (o resto) | — | RN-35 |

### 1.6 Montar e entregar
| Função | O que faz | Por quê |
|---|---|---|
| `processar_caso(...)` | Chama tudo, na ordem, e devolve a **ficha** de um cliente-imóvel | O motor em uma chamada |
| `escolher_jornada(...)` | 1 toque, app com perguntas, gerente (só obra ou sem app) ou sem nova proposta | Gerente é o último recurso (mentoria) |
| `processar(dados, cal)` | Roda `processar_caso` para todos os imóveis da base | — |
| `justificativa(f)` | Chama `motivo.justificativa` | Compatibilidade |
| `para_templates(fichas, template)` | Transforma as fichas nas 2 planilhas, na ordem do modelo | RN-28 a RN-31 |
| `_limpo(v)` | Converte números do numpy para gravar em JSON | Detalhe técnico |

---

## 2. `motor/motivo.py`: o texto do cliente
| Função | O que faz | Exemplo |
|---|---|---|
| `reais(v)` | Escreve reais como se fala | 48.552 → "R$ 49 mil"; 1.234.567 → "R$ 1,2 milhão" |
| `faixa_reais(lo, hi)` | "de R$ 22 mil a R$ 60 mil" ou "cerca de R$ 30 mil" | — |
| `motivos_de_patrimonio(vinculo, bens)` | O porquê do Essencial: o prejuízo seria todo seu + quanto valem os aparelhos + danos elétricos são 53% dos acionamentos | Substituiu o antigo "não há sinais" |
| `_em_jogo(f)` | Quanto o cliente perderia: reconstrução (ou acabamentos) e bens | "Reconstruir custaria cerca de R$ 397 mil" |
| `_se_escolher_menos(f)` | A frase do slide 23: "Se você escolher menos, X ficará descoberto" | — |
| `_no_limite(f)` | Diz com franqueza que a recomendação foi por pouco | "Você está perto de precisar do Prático" |
| `_opcao_acima(f)` | O que o plano acima acrescenta | "O Total acrescenta perda de aluguel" |
| `_confianca(f)` | A confiança em uma frase | "a área foi estimada pelo IPTU e pela conta de luz" |
| `_nao_elegivel(f)` | O texto de quando não pode haver proposta | — |
| `justificativa(f)` | Junta tudo na ordem: plano e prova → em jogo → RC → menos → no limite ou acima → confirmar → confiança | O texto da planilha |

## 3. `motor/parametros.py`: números fixos e fontes
| Função ou constante | O que é |
|---|---|
| `custo_m2(uf)` · `fonte_custo(uf)` · `fonte_disponivel(uf)` | Custo do m² (SINAPI a CUB) do estado e de onde veio |
| `fator_padrao(padrao)` · `fator_padrao_pelo_iptu(rel)` | Fator do acabamento (0,85 · 1,00 · 1,30) e o estreitamento pelo IPTU |
| `aluguel_m2(uf)` | Aluguel por m² da capital (FipeZAP) |
| `sinistros_pct(cob)` · `desastres(cod)` · `continuidade_energia(cod)` | Dados de fora só para o texto |
| `referencia(arquivo, coluna)` | A data de referência de uma fonte salva |
| `_ler_csv`, `_tabela_*`, `_ipca_12m` | Leitura dos arquivos (devolvem vazio se faltar) |
| `LIMITES_PRODUTO` | Mínimo e máximo de cada cobertura |
| `BENS_RELEVANTES` (R$ 36 mil) · `PORTATEIS_RELEVANTES` (R$ 10 mil) · `FAIXA_NO_LIMITE` (15%) | Limites da necessidade de roubo e a faixa "no limite" |
| `FATOR_IPCA`, `FATOR_ESTOQUE` (2,7), `BENS_PISO` (R$ 15 mil) | Bens |
| `PESO_FONTE`, `MEIA_VIDA_MESES`, `CLASSE_FONTE` | Confiança |
| `MAX_PERGUNTAS` (3), `VALOR_MINIMO_PERGUNTA` (R$ 5 mil), `AREA_QUANTIS` (9% e 91%) | Perguntas e área |
| `REGIONAL_MIN_IMOVEIS` (20), `USAR_CEP` (não) | Média da região |
| `RENDA_NOS_BENS_SEM_COMPRAS` (sim) | Liga ou desliga o uso da renda (D-08) |

## 4. `motor/metricas.py`: as provas
| Função | O que faz |
|---|---|
| `calcular_metricas(...)` | Todas as métricas do guia §8 e mais: justiça (troca renda e idade), família, estabilidade (±5% nos valores e ±20% nos pesos), sensibilidade (área +10%), confiança por cobertura, jornada, necessidades e força |
| `qualidade_do_motivo(fichas)` | Motivos genéricos, fato do cliente, valor em risco, alternativas, jargão, tamanho |
| `dados_faltantes(fichas, cal)` | Como cada lacuna foi tratada |
| `metricas_de_mercado(fichas)` | 1 toque e sem pessoa, esforço, ITV, faixas no limite do produto, aderência aos sinistros |
| `renda_por_quinto(m, por_id)` | Plano e elegibilidade por faixa de renda (regra dos 80%) |
| `casos_contrastantes(fichas)` | Escolhe os casos da demo (perfis A, B e C do slide 14 etc.) |
| `_incendio_meio(f)` | Meio da faixa de incêndio (para a sensibilidade) |

## 5. `motor/templates.py`
| Função | O que faz |
|---|---|
| `validar_templates(...)` | Confere as planilhas: colunas e ordem, campos obrigatórios, SIM/NÃO, motivo de cada NÃO, nomes do catálogo, valores inteiros e não negativos, confiança válida, linhas repetidas, coberturas fixas do plano e RN-33. Devolve a lista de erros (vazia = ok) |

## 6. `motor/gerar.py`
| Função | O que faz |
|---|---|
| `gerar(saida, entrega)` | Calibra → processa os 138 → valida → grava planilhas, fichas e métricas; com `--entrega`, copia para `entrega/` |
| `resumo(fichas, segundos)` | O resumo impresso na tela |
| `escrever_fichas_demo(...)` | Grava as fichas dos casos da demo para o protótipo |

## 7. `motor/api.py`
| Função (rota) | O que faz |
|---|---|
| `saude()` (`GET /saude`) | Diz se a API está no ar |
| `fontes()` (`GET /fontes`) | A data de cada fonte externa |
| `ficha(id)` (`GET /fichas/{id}`) | A ficha de um imóvel |
| `recomendar(c)` (`POST /recomendar`) | Recalcula com as respostas do cliente (bens "menos/isso/mais", área) |
| `_ficha(...)` | Monta a ficha a partir da base de teste |

## 8. `motor/externos/coletar.py`
| Função | O que faz |
|---|---|
| `atualizar_tudo(timeout)` | Tenta cada API; a que falhar mantém o arquivo salvo |
| `atualizar_sinapi(...)` | SINAPI pela API SIDRA do IBGE (valida antes de gravar) |
| `atualizar_ipca(...)` | IPCA pela API do Banco Central (valida antes de gravar) |
| `resumir_atlas(caminho)` | Transforma a base da Defesa Civil (86 MB) na tabela das 10 capitais |
| `_baixar_json`, `_numero` | Auxiliares |

Ligações: [[00 - Índice (leia nesta ordem)]] · [[02 - O motor passo a passo]] · [[09 - Cada escolha conta por conta]] · [[Mapa do código]]
