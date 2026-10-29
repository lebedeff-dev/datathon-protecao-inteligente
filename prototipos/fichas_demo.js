// Gerado por motor/gerar.py. Não edite à mão.
window.FICHAS_DEMO = {
 "casos": {
  "perfil_A_apto_urbano": "IMO_CASO_00004_01",
  "perfil_B_casa_familiar": "IMO_CASO_00001_01",
  "perfil_C_casa_lazer": "IMO_CASO_00010_01",
  "nao_elegivel_seguro_existente": "IMO_CASO_00014_01",
  "one_click_limpo": "IMO_CASO_00005_01",
  "inquilino_total": "IMO_CASO_00008_01",
  "elegibilidade_a_confirmar": "IMO_CASO_00003_01"
 },
 "fichas": {
  "IMO_CASO_00004_01": {
   "cliente_id": "CASO_00004",
   "imovel_id": "IMO_CASO_00004_01",
   "local": "Brasilia/DF",
   "complemento": "TORRE 2 AP 702",
   "canal_digital": {
    "usuario_app": "NAO",
    "maturidade_digital": 26
   },
   "campos": {
    "tipo": {
     "valor": "APARTAMENTO",
     "natureza": "INFERIDO",
     "confianca": "ALTA",
     "fonte": "termo 'apartamento' no endereço; confirmado pelo complemento",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "diverge": false,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "vinculo": {
     "valor": "FINANCIADO",
     "natureza": "OBSERVADO",
     "confianca": "ALTA",
     "fonte": "parcela de financiamento de R$ 2.350/mês",
     "fonte_tipo": "TRANSACAO",
     "idade_meses": 3,
     "peso": 0.673,
     "classe": "OBSERVADO"
    },
    "uso": {
     "valor": "RESIDENCIAL_HABITUAL",
     "natureza": "OBSERVADO",
     "confianca": "ALTA",
     "fonte": "endereço compatível com o endereço principal do cliente",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "area": {
     "valor": 105,
     "natureza": "OBSERVADO",
     "confianca": "ALTA",
     "fonte": "área cadastrada (CADASTRO_PUBLICO_MUNICIPAL)",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "min": 105.0,
     "max": 105.0,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "bens": {
     "valor": 92590,
     "natureza": "ESTIMADO",
     "confianca": "ALTA",
     "fonte": "compras de R$ 46.800 nos últimos 36 meses (corrigidas pelo IPCA) e 2 bens vinculados (R$ 11.800 ponderado pela chance de estarem no imóvel)",
     "fonte_tipo": "TRANSACAO",
     "idade_meses": 18,
     "min": 50048.91164710883,
     "max": 135132.06144719385,
     "categorias": {
      "eletronicos": {
       "min": 12993.467446845561,
       "max": 35082.362106483015
      },
      "eletrodomesticos": {
       "min": 16362.14419232404,
       "max": 44177.78931927491
      },
      "moveis": {
       "min": 20693.30000793923,
       "max": 55871.91002143591
      }
     },
     "portateis": {
      "min": 12993.467446845561,
      "max": 35082.362106483015
     },
     "eletricos": {
      "min": 29355.6116391696,
      "max": 79260.15142575793
     },
     "molhaveis": {
      "min": 50048.91164710883,
      "max": 135132.06144719385
     },
     "peso": 0.566,
     "classe": "OBSERVADO"
    }
   },
   "valor_imovel": {
    "custo_m2": [
     1833.05,
     2060.16
    ],
    "fator_padrao": [
     0.85,
     0.85
    ],
    "origem_padrao": "cadastrado",
    "reconstrucao_min": 192000,
    "reconstrucao_max": 216000,
    "segundo_risco": true,
    "estrutura_do_locador": false
   },
   "elegibilidade": "SIM",
   "pendencias": [],
   "avisos": [],
   "plano": "PRATICO",
   "motivos": [
    {
     "plano": "TOTAL",
     "peso": 1,
     "codigo": "VIZINHOS",
     "texto": "em prédio ou condomínio, um vazamento ou incêndio no seu imóvel pode atingir o vizinho"
    },
    {
     "plano": "PRATICO",
     "peso": 2,
     "codigo": "BENS_ALTOS",
     "texto": "suas compras para a casa nos últimos 3 anos valem hoje pelo menos R$ 50 mil"
    },
    {
     "plano": "PRATICO",
     "peso": 1,
     "codigo": "ELETRONICOS",
     "texto": "você tem pelo menos R$ 13 mil em eletrônicos, os itens mais levados num arrombamento"
    }
   ],
   "motivos_plano": [
    {
     "plano": "PRATICO",
     "peso": 2,
     "codigo": "BENS_ALTOS",
     "texto": "suas compras para a casa nos últimos 3 anos valem hoje pelo menos R$ 50 mil"
    },
    {
     "plano": "PRATICO",
     "peso": 1,
     "codigo": "ELETRONICOS",
     "texto": "você tem pelo menos R$ 13 mil em eletrônicos, os itens mais levados num arrombamento"
    }
   ],
   "pontos": {
    "pratico": 3,
    "total": 1
   },
   "alternativa": {
    "plano": "TOTAL",
    "texto": "Total: acrescenta o conserto de danos a terceiros, a perda de aluguel e as despesas emergenciais"
   },
   "por_que_nao_abaixo": "o Essencial não cobre roubo com arrombamento e quebra de vidros",
   "por_que_nao_acima": "o Total acrescenta a perda de aluguel e as despesas emergenciais (a RC familiar já entra como adicional), mas esses sinais ainda são poucos",
   "adicionais": [
    {
     "cobertura": "RESPONSABILIDADE_CIVIL_FAMILIAR",
     "motivo": "há dependentes ou pet na casa e vizinhos por perto; a RC familiar paga danos que eles causem a terceiros"
    }
   ],
   "coberturas": [
    {
     "cobertura": "INCENDIO_RAIO_EXPLOSAO_FUMACA",
     "tipo": "FIXA",
     "min": 100000,
     "max": 222000,
     "confianca": "ALTA",
     "dados_utilizados": "área, tipo, vínculo, UF, padrão, compras 36m, bens; SINAPI, CUB, IPCA",
     "regra": "área 105–105 m² × R$ 1.833–R$ 2.060/m² (SINAPI DF até CUB DF oficial) × 25%–40% (acabamentos) + bens",
     "justificativa": "A estrutura tem seguro próprio (condomínio ou financiamento); o seu paga os acabamentos, estimados em de R$ 48 mil a R$ 87 mil, e repõe o que você comprou para a casa, de R$ 50 mil a R$ 135 mil.",
     "confirmar": "Área do imóvel e valor dos bens",
     "observacao": "Segundo risco (CG cl. 15.2): a estrutura é paga primeiro pelo seguro do condomínio ou do financiamento.",
     "limitada_pelo_produto": false,
     "sugerido": 160000,
     "valor_em_risco": 160000,
     "valor_em_risco_max": 222000
    },
    {
     "cobertura": "DANOS_POR_AGUA",
     "tipo": "FIXA",
     "min": 31000,
     "max": 50000,
     "confianca": "ALTA",
     "dados_utilizados": "bens molháveis, reconstrução",
     "regra": "50%–100% dos bens molháveis + 3%–8% da reconstrução (pisos e acabamentos)",
     "justificativa": "Um cano rompido ou uma chuva forte estraga móveis e eletrodomésticos, e os seus valem hoje de R$ 50 mil a R$ 135 mil. A faixa cobre esses bens e parte de pisos e paredes. Na BB Seguros, 14,6% dos acionamentos do residencial são de danos por água (jan/2023 a mai/2026). Em Brasilia, a Defesa Civil registrou 2 ocorrências de chuvas intensas, alagamentos ou enxurradas desde 1991 (2 nos últimos 10 anos; a última em 2024).",
     "confirmar": "",
     "observacao": "O máximo estimado (R$ 152.000) passa do limite do produto (R$ 50.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 40000
    },
    {
     "cobertura": "VENDAVAL_GRANIZO",
     "tipo": "FIXA",
     "min": 4000,
     "max": 11000,
     "confianca": "ALTA",
     "dados_utilizados": "tipo, reconstrução",
     "regra": "2%–5% da reconstrução",
     "justificativa": "Em apartamento, vento e granizo atingem sobretudo janelas e esquadrias: repor de 2% a 5% do imóvel custa de R$ 3,8 mil a R$ 11 mil. Na BB Seguros, 11,5% dos acionamentos do residencial são de vendaval e granizo (jan/2023 a mai/2026). Em Brasilia, a Defesa Civil registrou 3 ocorrências de vendaval, ciclone ou granizo desde 1991 (1 nos últimos 10 anos; a última em 2016).",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 7500
    },
    {
     "cobertura": "IMPACTO_VEICULOS_TERRESTRES",
     "tipo": "FIXA",
     "min": 10000,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel",
     "regra": "padrão do produto (casa até R$ 20 mil)",
     "justificativa": "Em apartamento, um carro raramente atinge a sua unidade; fica no valor padrão de R$ 10 mil.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 10000
    },
    {
     "cobertura": "QUEDA_AERONAVE",
     "tipo": "FIXA",
     "min": 10000,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "padrão do produto",
     "regra": "padrão do produto",
     "justificativa": "Evento raro: fica no valor padrão do produto, R$ 10 mil, sem precisar de pergunta.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 10000
    },
    {
     "cobertura": "DANOS_ELETRICOS",
     "tipo": "FIXA",
     "min": 29000,
     "max": 30000,
     "confianca": "ALTA",
     "dados_utilizados": "compras de eletrônicos e eletrodomésticos (36m), bens vinculados; IPCA",
     "regra": "eletrônicos + eletrodomésticos: comprovado → estoque, a preço de hoje",
     "justificativa": "Seus eletrônicos e eletrodomésticos valem hoje de R$ 29 mil a R$ 79 mil, e um pico de energia pode queimar vários de uma vez. Desgaste e mau uso não são cobertos. Na BB Seguros, 53,3% dos acionamentos do residencial são de danos elétricos (jan/2023 a mai/2026). A distribuidora de Brasilia (NEOENERGIA BRASILIA) ficou em 25º de 33 no ranking de continuidade da ANEEL de 2025 (1º = menos quedas de energia).",
     "confirmar": "Principais aparelhos da casa",
     "observacao": "O máximo estimado (R$ 79.000) passa do limite do produto (R$ 30.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 30000
    },
    {
     "cobertura": "ROUBO_FURTO_ARROMBAMENTO",
     "tipo": "FIXA",
     "min": 13000,
     "max": 35000,
     "confianca": "ALTA",
     "dados_utilizados": "compras de eletrônicos (36m), bens vinculados; IPCA",
     "regra": "eletrônicos e portáteis: comprovado → estoque, a preço de hoje",
     "justificativa": "Seus eletrônicos, os itens mais levados num arrombamento, valem hoje de R$ 13 mil a R$ 35 mil; a faixa repõe esses bens a preço de hoje. Na BB Seguros, 2,1% dos acionamentos do residencial são de roubo ou furto com arrombamento (jan/2023 a mai/2026).",
     "confirmar": "Bens portáteis de maior valor",
     "observacao": "Não cobre joias, relógios, dinheiro, drones nem bicicleta fora de casa (CG cl. 6; Roubo 2.1).",
     "limitada_pelo_produto": false,
     "sugerido": 24000
    },
    {
     "cobertura": "QUEBRA_DE_VIDROS",
     "tipo": "FIXA",
     "min": 2000,
     "max": 5000,
     "confianca": "BAIXA",
     "dados_utilizados": "tipo do imóvel, gastos com vidraçaria 24m",
     "regra": "faixa por tipo, ampliada para 1,2 × o gasto com vidraçaria",
     "justificativa": "Num apartamento de cerca de 105 m², repor box, janelas e tampos de vidro costuma custar de R$ 2 mil a R$ 5 mil.",
     "confirmar": "Há vidros grandes (sacada, box, fachada)?",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 3500
    },
    {
     "cobertura": "RESPONSABILIDADE_CIVIL_FAMILIAR",
     "tipo": "ADICIONAL",
     "min": 58000,
     "max": 130000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel; SINAPI, CUB",
     "regra": "reparo de uma unidade vizinha do mesmo tamanho: 105 m² × R$ 1.833–R$ 2.060/m² (SINAPI DF até CUB DF oficial) × 30%–60%",
     "justificativa": "Um vazamento ou incêndio no seu imóvel pode atingir a unidade vizinha, de tamanho parecido com a sua (cerca de 105 m²): repará-la custa de R$ 58 mil a R$ 130 mil, e a cobertura paga isso no seu lugar.",
     "confirmar": "",
     "observacao": "Cobertura adicional ao plano Prático (guia 9.2): há dependentes ou pet na casa e vizinhos por perto; a RC familiar paga danos que eles causem a terceiros.",
     "limitada_pelo_produto": false,
     "sugerido": 94000
    }
   ],
   "perguntas": [
    {
     "prioridade": 58,
     "texto": "Seus móveis, eletrodomésticos e eletrônicos ficam entre R$ 50 mil e R$ 135 mil?",
     "codigo": "BENS",
     "obrigatoria": false,
     "reduz_faixa_ate": 85000
    }
   ],
   "perguntas_candidatas": 1,
   "confianca": "ALTA",
   "confianca_score": 76,
   "confianca_motivo": "todos os dados críticos observados",
   "completude": {
    "faltantes": [
     "material_parede_externa_cadastrado"
    ],
    "pct": 67
   },
   "canal": "GERENTE",
   "jornada": "GERENTE",
   "motivo_jornada": "o cliente não usa o app",
   "fontes": [
    "SINAPI 2026-09 (IBGE)",
    "CUB R8-N oficial dos Sinduscons",
    "IPCA 12m até 09/2026, série 433 (Banco Central)",
    "Condições Gerais BB Seguro Residencial v1.4",
    "Atlas Digital de Desastres no Brasil / S2iD (Sedec/MIDR), registros de 1991 a 2025",
    "BB Seguros, dado divulgado à imprensa (Monitor Mercantil, 22/07/2026): acionamentos jan/2023 a mai/2026 [fonte secundária]",
    "Ranking de Continuidade do Fornecimento 2025 (ANEEL)"
   ],
   "sinais": {
    "parcela": 2350.0,
    "aluguel": 0.0,
    "vidracaria": 0.0,
    "obra": 0.0
   }
  },
  "IMO_CASO_00001_01": {
   "cliente_id": "CASO_00001",
   "imovel_id": "IMO_CASO_00001_01",
   "local": "Recife/PE",
   "complemento": "CASA FUNDOS",
   "canal_digital": {
    "usuario_app": "SIM",
    "maturidade_digital": 100
   },
   "campos": {
    "tipo": {
     "valor": "CASA_EM_CONDOMINIO",
     "natureza": "INFERIDO",
     "confianca": "ALTA",
     "fonte": "termos 'casa' + 'condomínio' no endereço e pagamento de condomínio; confirmado pelo complemento",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "diverge": false,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "vinculo": {
     "valor": "PROPRIETARIO",
     "natureza": "INFERIDO",
     "confianca": "MEDIA",
     "fonte": "sem aluguel pago nem financiamento: provável imóvel quitado",
     "fonte_tipo": "INFERIDO",
     "idade_meses": 3,
     "peso": 0.505,
     "classe": "ESTIMADO"
    },
    "uso": {
     "valor": "RESIDENCIAL_HABITUAL",
     "natureza": "OBSERVADO",
     "confianca": "ALTA",
     "fonte": "endereço compatível com o endereço principal do cliente",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "area": {
     "valor": 265,
     "natureza": "ESTIMADO",
     "confianca": "MEDIA",
     "fonte": "estimada pelo IPTU (R$ 3.350/ano) e energia (R$ 700/mês) comparados a imóveis de Recife",
     "fonte_tipo": "DERIVADO",
     "idade_meses": 3,
     "min": 193.02989505051514,
     "max": 344.6302666651339,
     "peso": 0.688,
     "classe": "ESTIMADO"
    },
    "bens": {
     "valor": 89821,
     "natureza": "ESTIMADO",
     "confianca": "ALTA",
     "fonte": "compras de R$ 45.400 nos últimos 36 meses (corrigidas pelo IPCA) e 1 bens vinculados (R$ 550 ponderado pela chance de estarem no imóvel)",
     "fonte_tipo": "TRANSACAO",
     "idade_meses": 18,
     "min": 48551.72198245173,
     "max": 131089.6493526197,
     "categorias": {
      "eletronicos": {
       "min": 16201.731013967923,
       "max": 43744.67373771339
      },
      "eletrodomesticos": {
       "min": 12833.054268489444,
       "max": 34649.2465249215
      },
      "moveis": {
       "min": 19516.936699994363,
       "max": 52695.72908998478
      }
     },
     "portateis": {
      "min": 16201.731013967923,
      "max": 43744.67373771339
     },
     "eletricos": {
      "min": 29034.785282457367,
      "max": 78393.92026263489
     },
     "molhaveis": {
      "min": 48551.72198245173,
      "max": 131089.6493526197
     },
     "peso": 0.566,
     "classe": "OBSERVADO"
    }
   },
   "valor_imovel": {
    "custo_m2": [
     1605.04,
     2789.14
    ],
    "fator_padrao": [
     0.85,
     1.3
    ],
    "origem_padrao": "não cadastrado",
    "reconstrucao_min": 310000,
    "reconstrucao_max": 961000,
    "segundo_risco": true,
    "estrutura_do_locador": false
   },
   "elegibilidade": "SIM",
   "pendencias": [
    {
     "codigo": "SEGURO_EXISTENTE",
     "prioridade": 100,
     "texto": "há seguro residencial, mas nenhum produto de seguridade do BB; se o seguro atual for de outra seguradora, a proposta é permitida",
     "pergunta": "O seu seguro residencial atual é da BB Seguros?"
    }
   ],
   "avisos": [],
   "plano": "PRATICO",
   "motivos": [
    {
     "plano": "TOTAL",
     "peso": 1,
     "codigo": "VIZINHOS",
     "texto": "em prédio ou condomínio, um vazamento ou incêndio no seu imóvel pode atingir o vizinho"
    },
    {
     "plano": "PRATICO",
     "peso": 2,
     "codigo": "BENS_ALTOS",
     "texto": "suas compras para a casa nos últimos 3 anos valem hoje pelo menos R$ 49 mil"
    },
    {
     "plano": "PRATICO",
     "peso": 1,
     "codigo": "ELETRONICOS",
     "texto": "você tem pelo menos R$ 16 mil em eletrônicos, os itens mais levados num arrombamento"
    }
   ],
   "motivos_plano": [
    {
     "plano": "PRATICO",
     "peso": 2,
     "codigo": "BENS_ALTOS",
     "texto": "suas compras para a casa nos últimos 3 anos valem hoje pelo menos R$ 49 mil"
    },
    {
     "plano": "PRATICO",
     "peso": 1,
     "codigo": "ELETRONICOS",
     "texto": "você tem pelo menos R$ 16 mil em eletrônicos, os itens mais levados num arrombamento"
    }
   ],
   "pontos": {
    "pratico": 3,
    "total": 1
   },
   "alternativa": {
    "plano": "TOTAL",
    "texto": "Total: acrescenta o conserto de danos a terceiros, a perda de aluguel e as despesas emergenciais"
   },
   "por_que_nao_abaixo": "o Essencial não cobre roubo com arrombamento e quebra de vidros",
   "por_que_nao_acima": "o Total acrescenta a perda de aluguel e as despesas emergenciais (a RC familiar já entra como adicional), mas esses sinais ainda são poucos",
   "adicionais": [
    {
     "cobertura": "RESPONSABILIDADE_CIVIL_FAMILIAR",
     "motivo": "há dependentes ou pet na casa e vizinhos por perto; a RC familiar paga danos que eles causem a terceiros"
    }
   ],
   "coberturas": [
    {
     "cobertura": "INCENDIO_RAIO_EXPLOSAO_FUMACA",
     "tipo": "FIXA",
     "min": 126000,
     "max": 516000,
     "confianca": "MEDIA",
     "dados_utilizados": "área, tipo, vínculo, UF, padrão, compras 36m, bens; SINAPI, CUB, IPCA",
     "regra": "área 193–345 m² × R$ 1.605–R$ 2.789/m² (SINAPI PE até SINAPI PE × 1.136 (razão CUB/SINAPI das UFs com CUB oficial), padrão não cadastrado: fator 0,85 a 1,30) × 25%–40% (acabamentos) + bens",
     "justificativa": "A estrutura tem seguro próprio (condomínio ou financiamento); o seu paga os acabamentos, estimados em de R$ 77 mil a R$ 384 mil, e repõe o que você comprou para a casa, de R$ 49 mil a R$ 131 mil.",
     "confirmar": "Área do imóvel e valor dos bens",
     "observacao": "Segundo risco (CG cl. 15.2): a estrutura é paga primeiro pelo seguro do condomínio ou do financiamento.",
     "limitada_pelo_produto": false,
     "sugerido": 321000,
     "valor_em_risco": 321000,
     "valor_em_risco_max": 516000
    },
    {
     "cobertura": "DANOS_POR_AGUA",
     "tipo": "FIXA",
     "min": 34000,
     "max": 50000,
     "confianca": "MEDIA",
     "dados_utilizados": "bens molháveis, reconstrução",
     "regra": "50%–100% dos bens molháveis + 3%–8% da reconstrução (pisos e acabamentos)",
     "justificativa": "Um cano rompido ou uma chuva forte estraga móveis e eletrodomésticos, e os seus valem hoje de R$ 49 mil a R$ 131 mil. A faixa cobre esses bens e parte de pisos e paredes. Na BB Seguros, 14,6% dos acionamentos do residencial são de danos por água (jan/2023 a mai/2026). Em Recife, a Defesa Civil registrou 8 ocorrências de chuvas intensas, alagamentos ou enxurradas desde 1991 (1 nos últimos 10 anos; a última em 2022).",
     "confirmar": "",
     "observacao": "O máximo estimado (R$ 208.000) passa do limite do produto (R$ 50.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 42000
    },
    {
     "cobertura": "VENDAVAL_GRANIZO",
     "tipo": "FIXA",
     "min": 31000,
     "max": 60000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo, reconstrução",
     "regra": "10%–20% da reconstrução",
     "justificativa": "Vento e granizo atingem primeiro o telhado: refazer de 10% a 20% de uma casa como a sua custa de R$ 31 mil a R$ 192 mil. Na BB Seguros, 11,5% dos acionamentos do residencial são de vendaval e granizo (jan/2023 a mai/2026).",
     "confirmar": "",
     "observacao": "O máximo estimado (R$ 192.000) passa do limite do produto (R$ 60.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 46000
    },
    {
     "cobertura": "IMPACTO_VEICULOS_TERRESTRES",
     "tipo": "FIXA",
     "min": 10000,
     "max": 20000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel",
     "regra": "padrão do produto (casa até R$ 20 mil)",
     "justificativa": "Um carro desgovernado atinge primeiro muro, portão e fachada; por isso a casa vai até R$ 20 mil.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 15000
    },
    {
     "cobertura": "QUEDA_AERONAVE",
     "tipo": "FIXA",
     "min": 10000,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "padrão do produto",
     "regra": "padrão do produto",
     "justificativa": "Evento raro: fica no valor padrão do produto, R$ 10 mil, sem precisar de pergunta.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 10000
    },
    {
     "cobertura": "DANOS_ELETRICOS",
     "tipo": "FIXA",
     "min": 29000,
     "max": 30000,
     "confianca": "ALTA",
     "dados_utilizados": "compras de eletrônicos e eletrodomésticos (36m), bens vinculados; IPCA",
     "regra": "eletrônicos + eletrodomésticos: comprovado → estoque, a preço de hoje",
     "justificativa": "Seus eletrônicos e eletrodomésticos valem hoje de R$ 29 mil a R$ 78 mil, e um pico de energia pode queimar vários de uma vez. Desgaste e mau uso não são cobertos. Na BB Seguros, 53,3% dos acionamentos do residencial são de danos elétricos (jan/2023 a mai/2026). A distribuidora de Recife (NEOENERGIA PERNAMBUCO) ficou em 21º de 33 no ranking de continuidade da ANEEL de 2025 (1º = menos quedas de energia).",
     "confirmar": "Principais aparelhos da casa",
     "observacao": "O máximo estimado (R$ 78.000) passa do limite do produto (R$ 30.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 30000
    },
    {
     "cobertura": "ROUBO_FURTO_ARROMBAMENTO",
     "tipo": "FIXA",
     "min": 16000,
     "max": 44000,
     "confianca": "ALTA",
     "dados_utilizados": "compras de eletrônicos (36m), bens vinculados; IPCA",
     "regra": "eletrônicos e portáteis: comprovado → estoque, a preço de hoje",
     "justificativa": "Seus eletrônicos, os itens mais levados num arrombamento, valem hoje de R$ 16 mil a R$ 44 mil; a faixa repõe esses bens a preço de hoje. Na BB Seguros, 2,1% dos acionamentos do residencial são de roubo ou furto com arrombamento (jan/2023 a mai/2026).",
     "confirmar": "Bens portáteis de maior valor",
     "observacao": "Não cobre joias, relógios, dinheiro, drones nem bicicleta fora de casa (CG cl. 6; Roubo 2.1).",
     "limitada_pelo_produto": false,
     "sugerido": 30000
    },
    {
     "cobertura": "QUEBRA_DE_VIDROS",
     "tipo": "FIXA",
     "min": 3000,
     "max": 8000,
     "confianca": "BAIXA",
     "dados_utilizados": "tipo do imóvel, gastos com vidraçaria 24m",
     "regra": "faixa por tipo, ampliada para 1,2 × o gasto com vidraçaria",
     "justificativa": "Numa casa de cerca de 265 m², repor box, janelas e tampos de vidro costuma custar de R$ 3 mil a R$ 8 mil.",
     "confirmar": "Há vidros grandes (sacada, box, fachada)?",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 5500
    },
    {
     "cobertura": "RESPONSABILIDADE_CIVIL_FAMILIAR",
     "tipo": "ADICIONAL",
     "min": 128000,
     "max": 200000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel; SINAPI, CUB",
     "regra": "reparo de uma unidade vizinha do mesmo tamanho: 265 m² × R$ 1.605–R$ 2.789/m² (SINAPI PE até SINAPI PE × 1.136 (razão CUB/SINAPI das UFs com CUB oficial), padrão não cadastrado: fator 0,85 a 1,30) × 30%–60%",
     "justificativa": "Um vazamento ou incêndio no seu imóvel pode atingir a unidade vizinha, de tamanho parecido com a sua (cerca de 265 m²): repará-la custa de R$ 128 mil a R$ 443 mil, e a cobertura paga isso no seu lugar.",
     "confirmar": "",
     "observacao": "Cobertura adicional ao plano Prático (guia 9.2): há dependentes ou pet na casa e vizinhos por perto; a RC familiar paga danos que eles causem a terceiros. O máximo estimado (R$ 443.000) passa do limite do produto (R$ 200.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 164000
    }
   ],
   "perguntas": [
    {
     "prioridade": 100,
     "texto": "O seu seguro residencial atual é da BB Seguros?",
     "codigo": "SEGURO_EXISTENTE",
     "obrigatoria": true
    },
    {
     "prioridade": 58,
     "texto": "Estimamos que o imóvel tem cerca de 265 m². Confere?",
     "codigo": "AREA",
     "obrigatoria": false,
     "reduz_faixa_ate": 169000
    },
    {
     "prioridade": 56,
     "texto": "O acabamento do imóvel é simples, normal ou de alto padrão?",
     "codigo": "PADRAO",
     "obrigatoria": false,
     "reduz_faixa_ate": 133000
    }
   ],
   "perguntas_candidatas": 5,
   "confianca": "MEDIA",
   "confianca_score": 57,
   "confianca_motivo": "estimado: área, vínculo; elegibilidade a confirmar",
   "completude": {
    "faltantes": [
     "area_cadastrada_m2",
     "padrao_construtivo_cadastrado",
     "material_parede_externa_cadastrado"
    ],
    "pct": 0
   },
   "canal": "ONE_CLICK",
   "jornada": "APP_COM_PERGUNTAS",
   "motivo_jornada": "o app confirma seguro existente",
   "fontes": [
    "SINAPI 2026-09 (IBGE)",
    "CUB R8-N oficial dos Sinduscons",
    "IPCA 12m até 09/2026, série 433 (Banco Central)",
    "Condições Gerais BB Seguro Residencial v1.4",
    "Atlas Digital de Desastres no Brasil / S2iD (Sedec/MIDR), registros de 1991 a 2025",
    "BB Seguros, dado divulgado à imprensa (Monitor Mercantil, 22/07/2026): acionamentos jan/2023 a mai/2026 [fonte secundária]",
    "Ranking de Continuidade do Fornecimento 2025 (ANEEL)"
   ],
   "sinais": {
    "parcela": 0.0,
    "aluguel": 0.0,
    "vidracaria": 0.0,
    "obra": 0.0
   }
  },
  "IMO_CASO_00010_01": {
   "cliente_id": "CASO_00010",
   "imovel_id": "IMO_CASO_00010_01",
   "local": "Salvador/BA",
   "complemento": "APTO 101",
   "canal_digital": {
    "usuario_app": "SIM",
    "maturidade_digital": 55
   },
   "campos": {
    "tipo": {
     "valor": "APARTAMENTO",
     "natureza": "INFERIDO",
     "confianca": "ALTA",
     "fonte": "termo 'apartamento' no endereço; confirmado pelo complemento",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "diverge": false,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "vinculo": {
     "valor": "PROPRIETARIO",
     "natureza": "INFERIDO",
     "confianca": "MEDIA",
     "fonte": "sem aluguel pago nem financiamento: provável imóvel quitado",
     "fonte_tipo": "INFERIDO",
     "idade_meses": 3,
     "peso": 0.505,
     "classe": "ESTIMADO"
    },
    "uso": {
     "valor": "LAZER_VERANEIO",
     "natureza": "INFERIDO",
     "confianca": "BAIXA",
     "fonte": "cliente mora em outro imóvel cadastrado",
     "fonte_tipo": "PRESUMIDO",
     "idade_meses": 0,
     "peso": 0.5,
     "classe": "PRESUMIDO"
    },
    "area": {
     "valor": 104,
     "natureza": "ESTIMADO",
     "confianca": "MEDIA",
     "fonte": "estimada pelo IPTU (R$ 1.000/ano) e energia (R$ 400/mês) comparados a imóveis de Salvador",
     "fonte_tipo": "DERIVADO",
     "idade_meses": 3,
     "min": 75.8259031281665,
     "max": 135.37748237570156,
     "peso": 0.688,
     "classe": "ESTIMADO"
    },
    "bens": {
     "valor": 35908,
     "natureza": "ESTIMADO",
     "confianca": "MEDIA",
     "fonte": "compras de R$ 18.150 nos últimos 36 meses (corrigidas pelo IPCA) e 3 bens vinculados (R$ 2.450 ponderado pela chance de estarem no imóvel)",
     "fonte_tipo": "TRANSACAO",
     "idade_meses": 18,
     "min": 19409.994581090283,
     "max": 52406.985368943766,
     "categorias": {
      "eletronicos": {
       "min": 4705.453231779463,
       "max": 12704.72372580455
      },
      "eletrodomesticos": {
       "min": 10212.972355339516,
       "max": 27575.025359416693
      },
      "moveis": {
       "min": 4491.568993971306,
       "max": 12127.236283722525
      }
     },
     "portateis": {
      "min": 4705.453231779463,
      "max": 12704.72372580455
     },
     "eletricos": {
      "min": 14918.425587118978,
      "max": 40279.74908522124
     },
     "molhaveis": {
      "min": 19409.994581090283,
      "max": 52406.985368943766
     },
     "peso": 0.566,
     "classe": "OBSERVADO"
    }
   },
   "valor_imovel": {
    "custo_m2": [
     1678.15,
     2916.19
    ],
    "fator_padrao": [
     0.85,
     1.3
    ],
    "origem_padrao": "não cadastrado",
    "reconstrucao_min": 127000,
    "reconstrucao_max": 395000,
    "segundo_risco": true,
    "estrutura_do_locador": false
   },
   "elegibilidade": "SIM",
   "pendencias": [],
   "avisos": [],
   "plano": "ESSENCIAL",
   "motivos": [
    {
     "plano": "TOTAL",
     "peso": 1,
     "codigo": "VIZINHOS",
     "texto": "em prédio ou condomínio, um vazamento ou incêndio no seu imóvel pode atingir o vizinho"
    }
   ],
   "motivos_plano": [
    {
     "plano": "ESSENCIAL",
     "peso": 0,
     "codigo": "VERANEIO",
     "texto": "o imóvel é de lazer e fica vazio parte do tempo, quando fogo, água, vento e danos elétricos seguem cobertos, mas o roubo do Prático não cobre residência desocupada"
    },
    {
     "plano": "ESSENCIAL",
     "peso": 0,
     "codigo": "APARELHOS",
     "texto": "seus eletrônicos e eletrodomésticos valem hoje de R$ 15 mil a R$ 40 mil, e danos elétricos são 53,3% dos acionamentos do residencial da BB"
    }
   ],
   "pontos": {
    "pratico": 0,
    "total": 1
   },
   "alternativa": {
    "plano": "PRATICO",
    "texto": "Prático: acrescenta roubo com arrombamento e quebra de vidros"
   },
   "por_que_nao_abaixo": "",
   "por_que_nao_acima": "o Prático acrescenta roubo com arrombamento e quebra de vidros, mas hoje não vemos eletrônicos de valor alto nem gasto com vidros que peçam isso",
   "adicionais": [
    {
     "cobertura": "RESPONSABILIDADE_CIVIL_FAMILIAR",
     "motivo": "há dependentes ou pet na casa e vizinhos por perto; a RC familiar paga danos que eles causem a terceiros"
    }
   ],
   "coberturas": [
    {
     "cobertura": "INCENDIO_RAIO_EXPLOSAO_FUMACA",
     "tipo": "FIXA",
     "min": 100000,
     "max": 210000,
     "confianca": "MEDIA",
     "dados_utilizados": "área, tipo, vínculo, UF, padrão, compras 36m, bens; SINAPI, CUB, IPCA",
     "regra": "área 76–135 m² × R$ 1.678–R$ 2.916/m² (SINAPI BA até CUB BA oficial, padrão não cadastrado: fator 0,85 a 1,30) × 25%–40% (acabamentos) + bens",
     "justificativa": "A estrutura tem seguro próprio (condomínio ou financiamento); o seu paga os acabamentos, estimados em de R$ 32 mil a R$ 158 mil, e repõe o que você comprou para a casa, de R$ 19 mil a R$ 52 mil.",
     "confirmar": "Área do imóvel e valor dos bens",
     "observacao": "Segundo risco (CG cl. 15.2): a estrutura é paga primeiro pelo seguro do condomínio ou do financiamento.",
     "limitada_pelo_produto": false,
     "sugerido": 131000,
     "valor_em_risco": 131000,
     "valor_em_risco_max": 210000
    },
    {
     "cobertura": "DANOS_POR_AGUA",
     "tipo": "FIXA",
     "min": 13500,
     "max": 50000,
     "confianca": "MEDIA",
     "dados_utilizados": "bens molháveis, reconstrução",
     "regra": "50%–100% dos bens molháveis + 3%–8% da reconstrução (pisos e acabamentos)",
     "justificativa": "Um cano rompido ou uma chuva forte estraga móveis e eletrodomésticos, e os seus valem hoje de R$ 19 mil a R$ 52 mil. A faixa cobre esses bens e parte de pisos e paredes. Na BB Seguros, 14,6% dos acionamentos do residencial são de danos por água (jan/2023 a mai/2026). Em Salvador, a Defesa Civil registrou 8 ocorrências de chuvas intensas, alagamentos ou enxurradas desde 1991 (2 nos últimos 10 anos; a última em 2022).",
     "confirmar": "",
     "observacao": "O máximo estimado (R$ 84.000) passa do limite do produto (R$ 50.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 32000
    },
    {
     "cobertura": "VENDAVAL_GRANIZO",
     "tipo": "FIXA",
     "min": 2500,
     "max": 19500,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo, reconstrução",
     "regra": "2%–5% da reconstrução",
     "justificativa": "Em apartamento, vento e granizo atingem sobretudo janelas e esquadrias: repor de 2% a 5% do imóvel custa de R$ 2,5 mil a R$ 20 mil. Na BB Seguros, 11,5% dos acionamentos do residencial são de vendaval e granizo (jan/2023 a mai/2026). Em Salvador, a Defesa Civil registrou 1 ocorrências de vendaval, ciclone ou granizo desde 1991 (0 nos últimos 10 anos; a última em 1995).",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 11000
    },
    {
     "cobertura": "IMPACTO_VEICULOS_TERRESTRES",
     "tipo": "FIXA",
     "min": 10000,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel",
     "regra": "padrão do produto (casa até R$ 20 mil)",
     "justificativa": "Em apartamento, um carro raramente atinge a sua unidade; fica no valor padrão de R$ 10 mil.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 10000
    },
    {
     "cobertura": "QUEDA_AERONAVE",
     "tipo": "FIXA",
     "min": 10000,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "padrão do produto",
     "regra": "padrão do produto",
     "justificativa": "Evento raro: fica no valor padrão do produto, R$ 10 mil, sem precisar de pergunta.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 10000
    },
    {
     "cobertura": "DANOS_ELETRICOS",
     "tipo": "FIXA",
     "min": 15000,
     "max": 30000,
     "confianca": "MEDIA",
     "dados_utilizados": "compras de eletrônicos e eletrodomésticos (36m), bens vinculados; IPCA",
     "regra": "eletrônicos + eletrodomésticos: comprovado → estoque, a preço de hoje",
     "justificativa": "Seus eletrônicos e eletrodomésticos valem hoje de R$ 15 mil a R$ 40 mil, e um pico de energia pode queimar vários de uma vez. Desgaste e mau uso não são cobertos. Na BB Seguros, 53,3% dos acionamentos do residencial são de danos elétricos (jan/2023 a mai/2026). A distribuidora de Salvador (NEOENERGIA COELBA) ficou em 8º de 33 no ranking de continuidade da ANEEL de 2025 (1º = menos quedas de energia).",
     "confirmar": "Principais aparelhos da casa",
     "observacao": "O máximo estimado (R$ 40.000) passa do limite do produto (R$ 30.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 22000
    },
    {
     "cobertura": "RESPONSABILIDADE_CIVIL_FAMILIAR",
     "tipo": "ADICIONAL",
     "min": 52000,
     "max": 182000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel; SINAPI, CUB",
     "regra": "reparo de uma unidade vizinha do mesmo tamanho: 104 m² × R$ 1.678–R$ 2.916/m² (SINAPI BA até CUB BA oficial, padrão não cadastrado: fator 0,85 a 1,30) × 30%–60%",
     "justificativa": "Um vazamento ou incêndio no seu imóvel pode atingir a unidade vizinha, de tamanho parecido com a sua (cerca de 104 m²): repará-la custa de R$ 52 mil a R$ 182 mil, e a cobertura paga isso no seu lugar.",
     "confirmar": "",
     "observacao": "Cobertura adicional ao plano Essencial (guia 9.2): há dependentes ou pet na casa e vizinhos por perto; a RC familiar paga danos que eles causem a terceiros.",
     "limitada_pelo_produto": false,
     "sugerido": 117000
    }
   ],
   "perguntas": [
    {
     "prioridade": 70,
     "texto": "Este imóvel é onde você mora, uma casa de veraneio ou está alugado para outra pessoa?",
     "codigo": "USO",
     "obrigatoria": true
    },
    {
     "prioridade": 58,
     "texto": "Estimamos que o imóvel tem cerca de 104 m². Confere?",
     "codigo": "AREA",
     "obrigatoria": false,
     "reduz_faixa_ate": 69000
    },
    {
     "prioridade": 56,
     "texto": "O acabamento do imóvel é simples, normal ou de alto padrão?",
     "codigo": "PADRAO",
     "obrigatoria": false,
     "reduz_faixa_ate": 55000
    }
   ],
   "perguntas_candidatas": 5,
   "confianca": "BAIXA",
   "confianca_score": 52,
   "confianca_motivo": "presumido: uso do imóvel; estimado: área, vínculo",
   "completude": {
    "faltantes": [
     "area_cadastrada_m2",
     "padrao_construtivo_cadastrado",
     "material_parede_externa_cadastrado"
    ],
    "pct": 0
   },
   "canal": "ONE_CLICK",
   "jornada": "APP_COM_PERGUNTAS",
   "motivo_jornada": "confiança baixa: o app pergunta primeiro se o cliente mora no imóvel; o gerente entra se a resposta mudar o caso ou não vier",
   "fontes": [
    "SINAPI 2026-09 (IBGE)",
    "CUB R8-N oficial dos Sinduscons",
    "IPCA 12m até 09/2026, série 433 (Banco Central)",
    "Condições Gerais BB Seguro Residencial v1.4",
    "Atlas Digital de Desastres no Brasil / S2iD (Sedec/MIDR), registros de 1991 a 2025",
    "BB Seguros, dado divulgado à imprensa (Monitor Mercantil, 22/07/2026): acionamentos jan/2023 a mai/2026 [fonte secundária]",
    "Ranking de Continuidade do Fornecimento 2025 (ANEEL)"
   ],
   "sinais": {
    "parcela": 0.0,
    "aluguel": 0.0,
    "vidracaria": 0.0,
    "obra": 0.0
   }
  },
  "IMO_CASO_00014_01": {
   "cliente_id": "CASO_00014",
   "imovel_id": "IMO_CASO_00014_01",
   "local": "Sao Paulo/SP",
   "complemento": "BLOCO B APTO 305",
   "canal_digital": {
    "usuario_app": "NAO",
    "maturidade_digital": 12
   },
   "campos": {
    "tipo": {
     "valor": "APARTAMENTO",
     "natureza": "INFERIDO",
     "confianca": "ALTA",
     "fonte": "termo 'apartamento' no endereço; confirmado pelo complemento",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "diverge": false,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "vinculo": {
     "valor": "PROPRIETARIO",
     "natureza": "INFERIDO",
     "confianca": "MEDIA",
     "fonte": "sem aluguel pago nem financiamento: provável imóvel quitado",
     "fonte_tipo": "INFERIDO",
     "idade_meses": 3,
     "peso": 0.505,
     "classe": "ESTIMADO"
    },
    "uso": {
     "valor": "RESIDENCIAL_HABITUAL",
     "natureza": "OBSERVADO",
     "confianca": "ALTA",
     "fonte": "endereço compatível com o endereço principal do cliente",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "area": {
     "valor": 90,
     "natureza": "OBSERVADO",
     "confianca": "ALTA",
     "fonte": "área cadastrada (LAUDO_FINANCIAMENTO)",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "min": 90.0,
     "max": 90.0,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "bens": {
     "valor": 59155,
     "natureza": "ESTIMADO",
     "confianca": "MEDIA",
     "fonte": "compras de R$ 29.900 nos últimos 36 meses (corrigidas pelo IPCA) e 5 bens vinculados (R$ 11.850 ponderado pela chance de estarem no imóvel)",
     "fonte_tipo": "TRANSACAO",
     "idade_meses": 18,
     "min": 31975.69355231953,
     "max": 86334.37259126273,
     "categorias": {
      "eletronicos": {
       "min": 12137.930495612933,
       "max": 32772.41233815492
      },
      "eletrodomesticos": {
       "min": 8608.840571778335,
       "max": 23243.869543801506
      },
      "moveis": {
       "min": 11228.922484928264,
       "max": 30318.090709306314
      }
     },
     "portateis": {
      "min": 12137.930495612933,
      "max": 32772.41233815492
     },
     "eletricos": {
      "min": 20746.771067391266,
      "max": 56016.28188195642
     },
     "molhaveis": {
      "min": 31975.69355231953,
      "max": 86334.37259126273
     },
     "peso": 0.566,
     "classe": "OBSERVADO"
    }
   },
   "valor_imovel": {
    "custo_m2": [
     1881.47,
     2238.58
    ],
    "fator_padrao": [
     0.85,
     1.0
    ],
    "origem_padrao": "estimado pelo IPTU/m²",
    "reconstrucao_min": 169000,
    "reconstrucao_max": 201000,
    "segundo_risco": true,
    "estrutura_do_locador": false
   },
   "elegibilidade": "SIM",
   "pendencias": [
    {
     "codigo": "SEGURO_EXISTENTE",
     "prioridade": 100,
     "provavel_bb": true,
     "texto": "provável seguro BB neste endereço: há seguro residencial e produto de seguridade do BB; se o seguro for da BB, não pode haver nova proposta para o mesmo endereço",
     "pergunta": "O seu seguro residencial atual é da BB Seguros? Se for, ele já protege este endereço."
    }
   ],
   "avisos": [],
   "plano": "PRATICO",
   "motivos": [
    {
     "plano": "TOTAL",
     "peso": 1,
     "codigo": "VIZINHOS",
     "texto": "em prédio ou condomínio, um vazamento ou incêndio no seu imóvel pode atingir o vizinho"
    },
    {
     "plano": "PRATICO",
     "peso": 1,
     "codigo": "ELETRONICOS",
     "texto": "você tem pelo menos R$ 12 mil em eletrônicos, os itens mais levados num arrombamento"
    }
   ],
   "motivos_plano": [
    {
     "plano": "PRATICO",
     "peso": 1,
     "codigo": "ELETRONICOS",
     "texto": "você tem pelo menos R$ 12 mil em eletrônicos, os itens mais levados num arrombamento"
    }
   ],
   "pontos": {
    "pratico": 1,
    "total": 1
   },
   "alternativa": {
    "plano": "TOTAL",
    "texto": "Total: acrescenta o conserto de danos a terceiros, a perda de aluguel e as despesas emergenciais"
   },
   "por_que_nao_abaixo": "o Essencial não cobre roubo com arrombamento e quebra de vidros",
   "por_que_nao_acima": "o Total acrescenta a perda de aluguel e as despesas emergenciais (a RC familiar já entra como adicional), mas esses sinais ainda são poucos",
   "adicionais": [
    {
     "cobertura": "RESPONSABILIDADE_CIVIL_FAMILIAR",
     "motivo": "há dependentes ou pet na casa e vizinhos por perto; a RC familiar paga danos que eles causem a terceiros"
    }
   ],
   "coberturas": [
    {
     "cobertura": "INCENDIO_RAIO_EXPLOSAO_FUMACA",
     "tipo": "FIXA",
     "min": 100000,
     "max": 167000,
     "confianca": "MEDIA",
     "dados_utilizados": "área, tipo, vínculo, UF, padrão, compras 36m, bens; SINAPI, CUB, IPCA",
     "regra": "área 90–90 m² × R$ 1.881–R$ 2.239/m² (SINAPI SP até CUB SP oficial, padrão estimado pelo IPTU/m²: fator 0,85 a 1,00) × 25%–40% (acabamentos) + bens",
     "justificativa": "A estrutura tem seguro próprio (condomínio ou financiamento); o seu paga os acabamentos, estimados em de R$ 42 mil a R$ 81 mil, e repõe o que você comprou para a casa, de R$ 32 mil a R$ 86 mil.",
     "confirmar": "Área do imóvel e valor dos bens",
     "observacao": "Segundo risco (CG cl. 15.2): a estrutura é paga primeiro pelo seguro do condomínio ou do financiamento.",
     "limitada_pelo_produto": false,
     "sugerido": 121000,
     "valor_em_risco": 121000,
     "valor_em_risco_max": 167000
    },
    {
     "cobertura": "DANOS_POR_AGUA",
     "tipo": "FIXA",
     "min": 21000,
     "max": 50000,
     "confianca": "MEDIA",
     "dados_utilizados": "bens molháveis, reconstrução",
     "regra": "50%–100% dos bens molháveis + 3%–8% da reconstrução (pisos e acabamentos)",
     "justificativa": "Um cano rompido ou uma chuva forte estraga móveis e eletrodomésticos, e os seus valem hoje de R$ 32 mil a R$ 86 mil. A faixa cobre esses bens e parte de pisos e paredes. Na BB Seguros, 14,6% dos acionamentos do residencial são de danos por água (jan/2023 a mai/2026). Em Sao Paulo, a Defesa Civil registrou 40 ocorrências de chuvas intensas, alagamentos ou enxurradas desde 1991 (4 nos últimos 10 anos; a última em 2020).",
     "confirmar": "",
     "observacao": "O máximo estimado (R$ 102.000) passa do limite do produto (R$ 50.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 36000
    },
    {
     "cobertura": "VENDAVAL_GRANIZO",
     "tipo": "FIXA",
     "min": 3500,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo, reconstrução",
     "regra": "2%–5% da reconstrução",
     "justificativa": "Em apartamento, vento e granizo atingem sobretudo janelas e esquadrias: repor de 2% a 5% do imóvel custa de R$ 3,4 mil a R$ 10 mil. Na BB Seguros, 11,5% dos acionamentos do residencial são de vendaval e granizo (jan/2023 a mai/2026). Em Sao Paulo, a Defesa Civil registrou 3 ocorrências de vendaval, ciclone ou granizo desde 1991 (0 nos últimos 10 anos; a última em 2012).",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 7000
    },
    {
     "cobertura": "IMPACTO_VEICULOS_TERRESTRES",
     "tipo": "FIXA",
     "min": 10000,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel",
     "regra": "padrão do produto (casa até R$ 20 mil)",
     "justificativa": "Em apartamento, um carro raramente atinge a sua unidade; fica no valor padrão de R$ 10 mil.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 10000
    },
    {
     "cobertura": "QUEDA_AERONAVE",
     "tipo": "FIXA",
     "min": 10000,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "padrão do produto",
     "regra": "padrão do produto",
     "justificativa": "Evento raro: fica no valor padrão do produto, R$ 10 mil, sem precisar de pergunta.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 10000
    },
    {
     "cobertura": "DANOS_ELETRICOS",
     "tipo": "FIXA",
     "min": 21000,
     "max": 30000,
     "confianca": "MEDIA",
     "dados_utilizados": "compras de eletrônicos e eletrodomésticos (36m), bens vinculados; IPCA",
     "regra": "eletrônicos + eletrodomésticos: comprovado → estoque, a preço de hoje",
     "justificativa": "Seus eletrônicos e eletrodomésticos valem hoje de R$ 21 mil a R$ 56 mil, e um pico de energia pode queimar vários de uma vez. Desgaste e mau uso não são cobertos. Na BB Seguros, 53,3% dos acionamentos do residencial são de danos elétricos (jan/2023 a mai/2026). A distribuidora de Sao Paulo (ENEL SP) ficou em 30º de 33 no ranking de continuidade da ANEEL de 2025 (1º = menos quedas de energia).",
     "confirmar": "Principais aparelhos da casa",
     "observacao": "O máximo estimado (R$ 56.000) passa do limite do produto (R$ 30.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 26000
    },
    {
     "cobertura": "ROUBO_FURTO_ARROMBAMENTO",
     "tipo": "FIXA",
     "min": 12000,
     "max": 33000,
     "confianca": "MEDIA",
     "dados_utilizados": "compras de eletrônicos (36m), bens vinculados; IPCA",
     "regra": "eletrônicos e portáteis: comprovado → estoque, a preço de hoje",
     "justificativa": "Seus eletrônicos, os itens mais levados num arrombamento, valem hoje de R$ 12 mil a R$ 33 mil; a faixa repõe esses bens a preço de hoje. Na BB Seguros, 2,1% dos acionamentos do residencial são de roubo ou furto com arrombamento (jan/2023 a mai/2026).",
     "confirmar": "Bens portáteis de maior valor",
     "observacao": "Não cobre joias, relógios, dinheiro, drones nem bicicleta fora de casa (CG cl. 6; Roubo 2.1).",
     "limitada_pelo_produto": false,
     "sugerido": 22000
    },
    {
     "cobertura": "QUEBRA_DE_VIDROS",
     "tipo": "FIXA",
     "min": 2000,
     "max": 5000,
     "confianca": "BAIXA",
     "dados_utilizados": "tipo do imóvel, gastos com vidraçaria 24m",
     "regra": "faixa por tipo, ampliada para 1,2 × o gasto com vidraçaria",
     "justificativa": "Num apartamento de cerca de 90 m², repor box, janelas e tampos de vidro costuma custar de R$ 2 mil a R$ 5 mil.",
     "confirmar": "Há vidros grandes (sacada, box, fachada)?",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 3500
    },
    {
     "cobertura": "RESPONSABILIDADE_CIVIL_FAMILIAR",
     "tipo": "ADICIONAL",
     "min": 51000,
     "max": 121000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel; SINAPI, CUB",
     "regra": "reparo de uma unidade vizinha do mesmo tamanho: 90 m² × R$ 1.881–R$ 2.239/m² (SINAPI SP até CUB SP oficial, padrão estimado pelo IPTU/m²: fator 0,85 a 1,00) × 30%–60%",
     "justificativa": "Um vazamento ou incêndio no seu imóvel pode atingir a unidade vizinha, de tamanho parecido com a sua (cerca de 90 m²): repará-la custa de R$ 51 mil a R$ 121 mil, e a cobertura paga isso no seu lugar.",
     "confirmar": "",
     "observacao": "Cobertura adicional ao plano Prático (guia 9.2): há dependentes ou pet na casa e vizinhos por perto; a RC familiar paga danos que eles causem a terceiros.",
     "limitada_pelo_produto": false,
     "sugerido": 86000
    }
   ],
   "perguntas": [
    {
     "prioridade": 100,
     "texto": "O seu seguro residencial atual é da BB Seguros? Se for, ele já protege este endereço.",
     "codigo": "SEGURO_EXISTENTE",
     "obrigatoria": true
    },
    {
     "prioridade": 58,
     "texto": "Seus móveis, eletrodomésticos e eletrônicos ficam entre R$ 32 mil e R$ 86 mil?",
     "codigo": "BENS",
     "obrigatoria": false,
     "reduz_faixa_ate": 54000
    },
    {
     "prioridade": 56,
     "texto": "O acabamento do imóvel é simples, normal ou de alto padrão?",
     "codigo": "PADRAO",
     "obrigatoria": false,
     "reduz_faixa_ate": 12000
    }
   ],
   "perguntas_candidatas": 4,
   "confianca": "MEDIA",
   "confianca_score": 74,
   "confianca_motivo": "estimado: vínculo; elegibilidade a confirmar",
   "completude": {
    "faltantes": [
     "padrao_construtivo_cadastrado"
    ],
    "pct": 67
   },
   "canal": "GERENTE",
   "jornada": "GERENTE",
   "motivo_jornada": "o cliente não usa o app",
   "fontes": [
    "SINAPI 2026-09 (IBGE)",
    "CUB R8-N oficial dos Sinduscons",
    "IPCA 12m até 09/2026, série 433 (Banco Central)",
    "Condições Gerais BB Seguro Residencial v1.4",
    "Atlas Digital de Desastres no Brasil / S2iD (Sedec/MIDR), registros de 1991 a 2025",
    "BB Seguros, dado divulgado à imprensa (Monitor Mercantil, 22/07/2026): acionamentos jan/2023 a mai/2026 [fonte secundária]",
    "Ranking de Continuidade do Fornecimento 2025 (ANEEL)"
   ],
   "sinais": {
    "parcela": 0.0,
    "aluguel": 0.0,
    "vidracaria": 0.0,
    "obra": 0.0
   }
  },
  "IMO_CASO_00005_01": {
   "cliente_id": "CASO_00005",
   "imovel_id": "IMO_CASO_00005_01",
   "local": "Curitiba/PR",
   "complemento": "BLOCO B APTO 305",
   "canal_digital": {
    "usuario_app": "SIM",
    "maturidade_digital": 62
   },
   "campos": {
    "tipo": {
     "valor": "APARTAMENTO",
     "natureza": "INFERIDO",
     "confianca": "ALTA",
     "fonte": "termo 'apartamento' no endereço; confirmado pelo complemento",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "diverge": false,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "vinculo": {
     "valor": "FINANCIADO",
     "natureza": "OBSERVADO",
     "confianca": "ALTA",
     "fonte": "parcela de financiamento de R$ 950/mês",
     "fonte_tipo": "TRANSACAO",
     "idade_meses": 3,
     "peso": 0.673,
     "classe": "OBSERVADO"
    },
    "uso": {
     "valor": "RESIDENCIAL_HABITUAL",
     "natureza": "OBSERVADO",
     "confianca": "ALTA",
     "fonte": "endereço compatível com o endereço principal do cliente",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "area": {
     "valor": 110,
     "natureza": "OBSERVADO",
     "confianca": "ALTA",
     "fonte": "área cadastrada (CADASTRO_IPTU)",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "min": 110.0,
     "max": 110.0,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "bens": {
     "valor": 41052,
     "natureza": "ESTIMADO",
     "confianca": "MEDIA",
     "fonte": "compras de R$ 20.750 nos últimos 36 meses (corrigidas pelo IPCA) e 3 bens vinculados (R$ 2.500 ponderado pela chance de estarem no imóvel)",
     "fonte_tipo": "TRANSACAO",
     "idade_meses": 18,
     "min": 22190.48967259633,
     "max": 59914.322116010095,
     "categorias": {
      "eletronicos": {
       "min": 9410.906463558926,
       "max": 25409.4474516091
      },
      "eletrodomesticos": {
       "min": 3047.8503887662428,
       "max": 8229.196049668857
      },
      "moveis": {
       "min": 9731.732820271161,
       "max": 26275.678614732136
      }
     },
     "portateis": {
      "min": 9410.906463558926,
      "max": 25409.4474516091
     },
     "eletricos": {
      "min": 12458.756852325168,
      "max": 33638.643501277955
     },
     "molhaveis": {
      "min": 22190.48967259633,
      "max": 59914.322116010095
     },
     "peso": 0.566,
     "classe": "OBSERVADO"
    }
   },
   "valor_imovel": {
    "custo_m2": [
     2287.43,
     3560.61
    ],
    "fator_padrao": [
     1.0,
     1.3
    ],
    "origem_padrao": "estimado pelo IPTU/m²",
    "reconstrucao_min": 252000,
    "reconstrucao_max": 392000,
    "segundo_risco": true,
    "estrutura_do_locador": false
   },
   "elegibilidade": "SIM",
   "pendencias": [],
   "avisos": [],
   "plano": "PRATICO",
   "motivos": [
    {
     "plano": "TOTAL",
     "peso": 1,
     "codigo": "VIZINHOS",
     "texto": "em prédio ou condomínio, um vazamento ou incêndio no seu imóvel pode atingir o vizinho"
    },
    {
     "plano": "PRATICO",
     "peso": 1,
     "codigo": "VIDROS",
     "texto": "você gastou R$ 11 mil com vidraçaria nos últimos 2 anos, e vidro quebrado custa caro para repor"
    }
   ],
   "motivos_plano": [
    {
     "plano": "PRATICO",
     "peso": 1,
     "codigo": "VIDROS",
     "texto": "você gastou R$ 11 mil com vidraçaria nos últimos 2 anos, e vidro quebrado custa caro para repor"
    }
   ],
   "pontos": {
    "pratico": 1,
    "total": 1
   },
   "alternativa": {
    "plano": "TOTAL",
    "texto": "Total: acrescenta o conserto de danos a terceiros, a perda de aluguel e as despesas emergenciais"
   },
   "por_que_nao_abaixo": "o Essencial não cobre roubo com arrombamento e quebra de vidros",
   "por_que_nao_acima": "o Total acrescenta a perda de aluguel e as despesas emergenciais (a RC familiar já entra como adicional), mas esses sinais ainda são poucos",
   "adicionais": [
    {
     "cobertura": "RESPONSABILIDADE_CIVIL_FAMILIAR",
     "motivo": "há dependentes ou pet na casa e vizinhos por perto; a RC familiar paga danos que eles causem a terceiros"
    }
   ],
   "coberturas": [
    {
     "cobertura": "INCENDIO_RAIO_EXPLOSAO_FUMACA",
     "tipo": "FIXA",
     "min": 100000,
     "max": 217000,
     "confianca": "MEDIA",
     "dados_utilizados": "área, tipo, vínculo, UF, padrão, compras 36m, bens; SINAPI, CUB, IPCA",
     "regra": "área 110–110 m² × R$ 2.287–R$ 3.561/m² (SINAPI PR até CUB PR oficial, padrão estimado pelo IPTU/m²: fator 1,00 a 1,30) × 25%–40% (acabamentos) + bens",
     "justificativa": "A estrutura tem seguro próprio (condomínio ou financiamento); o seu paga os acabamentos, estimados em de R$ 63 mil a R$ 157 mil, e repõe o que você comprou para a casa, de R$ 22 mil a R$ 60 mil.",
     "confirmar": "Área do imóvel e valor dos bens",
     "observacao": "Segundo risco (CG cl. 15.2): a estrutura é paga primeiro pelo seguro do condomínio ou do financiamento.",
     "limitada_pelo_produto": false,
     "sugerido": 151000,
     "valor_em_risco": 151000,
     "valor_em_risco_max": 217000
    },
    {
     "cobertura": "DANOS_POR_AGUA",
     "tipo": "FIXA",
     "min": 18500,
     "max": 50000,
     "confianca": "MEDIA",
     "dados_utilizados": "bens molháveis, reconstrução",
     "regra": "50%–100% dos bens molháveis + 3%–8% da reconstrução (pisos e acabamentos)",
     "justificativa": "Um cano rompido ou uma chuva forte estraga móveis e eletrodomésticos, e os seus valem hoje de R$ 22 mil a R$ 60 mil. A faixa cobre esses bens e parte de pisos e paredes. Na BB Seguros, 14,6% dos acionamentos do residencial são de danos por água (jan/2023 a mai/2026). Em Curitiba, a Defesa Civil registrou 17 ocorrências de chuvas intensas, alagamentos ou enxurradas desde 1991 (10 nos últimos 10 anos; a última em 2025).",
     "confirmar": "",
     "observacao": "O máximo estimado (R$ 91.000) passa do limite do produto (R$ 50.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 34000
    },
    {
     "cobertura": "VENDAVAL_GRANIZO",
     "tipo": "FIXA",
     "min": 5000,
     "max": 19500,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo, reconstrução",
     "regra": "2%–5% da reconstrução",
     "justificativa": "Em apartamento, vento e granizo atingem sobretudo janelas e esquadrias: repor de 2% a 5% do imóvel custa de R$ 5 mil a R$ 20 mil. Na BB Seguros, 11,5% dos acionamentos do residencial são de vendaval e granizo (jan/2023 a mai/2026). Em Curitiba, a Defesa Civil registrou 10 ocorrências de vendaval, ciclone ou granizo desde 1991 (7 nos últimos 10 anos; a última em 2025).",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 12000
    },
    {
     "cobertura": "IMPACTO_VEICULOS_TERRESTRES",
     "tipo": "FIXA",
     "min": 10000,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel",
     "regra": "padrão do produto (casa até R$ 20 mil)",
     "justificativa": "Em apartamento, um carro raramente atinge a sua unidade; fica no valor padrão de R$ 10 mil.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 10000
    },
    {
     "cobertura": "QUEDA_AERONAVE",
     "tipo": "FIXA",
     "min": 10000,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "padrão do produto",
     "regra": "padrão do produto",
     "justificativa": "Evento raro: fica no valor padrão do produto, R$ 10 mil, sem precisar de pergunta.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 10000
    },
    {
     "cobertura": "DANOS_ELETRICOS",
     "tipo": "FIXA",
     "min": 12500,
     "max": 30000,
     "confianca": "MEDIA",
     "dados_utilizados": "compras de eletrônicos e eletrodomésticos (36m), bens vinculados; IPCA",
     "regra": "eletrônicos + eletrodomésticos: comprovado → estoque, a preço de hoje",
     "justificativa": "Seus eletrônicos e eletrodomésticos valem hoje de R$ 12 mil a R$ 34 mil, e um pico de energia pode queimar vários de uma vez. Desgaste e mau uso não são cobertos. Na BB Seguros, 53,3% dos acionamentos do residencial são de danos elétricos (jan/2023 a mai/2026). A distribuidora de Curitiba (COPEL) ficou em 27º de 33 no ranking de continuidade da ANEEL de 2025 (1º = menos quedas de energia).",
     "confirmar": "Principais aparelhos da casa",
     "observacao": "O máximo estimado (R$ 34.000) passa do limite do produto (R$ 30.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 21000
    },
    {
     "cobertura": "ROUBO_FURTO_ARROMBAMENTO",
     "tipo": "FIXA",
     "min": 9500,
     "max": 25000,
     "confianca": "MEDIA",
     "dados_utilizados": "compras de eletrônicos (36m), bens vinculados; IPCA",
     "regra": "eletrônicos e portáteis: comprovado → estoque, a preço de hoje",
     "justificativa": "Seus eletrônicos, os itens mais levados num arrombamento, valem hoje de R$ 9,4 mil a R$ 25 mil; a faixa repõe esses bens a preço de hoje. Na BB Seguros, 2,1% dos acionamentos do residencial são de roubo ou furto com arrombamento (jan/2023 a mai/2026).",
     "confirmar": "Bens portáteis de maior valor",
     "observacao": "Não cobre joias, relógios, dinheiro, drones nem bicicleta fora de casa (CG cl. 6; Roubo 2.1).",
     "limitada_pelo_produto": false,
     "sugerido": 17000
    },
    {
     "cobertura": "QUEBRA_DE_VIDROS",
     "tipo": "FIXA",
     "min": 2000,
     "max": 13000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel, gastos com vidraçaria 24m",
     "regra": "faixa por tipo, ampliada para 1,2 × o gasto com vidraçaria",
     "justificativa": "Você gastou R$ 11 mil com vidraçaria nos últimos 2 anos; a faixa cobre janelas, box e tampos de vidro.",
     "confirmar": "Há vidros grandes (sacada, box, fachada)?",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 7500
    },
    {
     "cobertura": "RESPONSABILIDADE_CIVIL_FAMILIAR",
     "tipo": "ADICIONAL",
     "min": 75000,
     "max": 200000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel; SINAPI, CUB",
     "regra": "reparo de uma unidade vizinha do mesmo tamanho: 110 m² × R$ 2.287–R$ 3.561/m² (SINAPI PR até CUB PR oficial, padrão estimado pelo IPTU/m²: fator 1,00 a 1,30) × 30%–60%",
     "justificativa": "Um vazamento ou incêndio no seu imóvel pode atingir a unidade vizinha, de tamanho parecido com a sua (cerca de 110 m²): repará-la custa de R$ 75 mil a R$ 235 mil, e a cobertura paga isso no seu lugar.",
     "confirmar": "",
     "observacao": "Cobertura adicional ao plano Prático (guia 9.2): há dependentes ou pet na casa e vizinhos por perto; a RC familiar paga danos que eles causem a terceiros. O máximo estimado (R$ 235.000) passa do limite do produto (R$ 200.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 138000
    }
   ],
   "perguntas": [
    {
     "prioridade": 58,
     "texto": "Seus móveis, eletrodomésticos e eletrônicos ficam entre R$ 22 mil e R$ 60 mil?",
     "codigo": "BENS",
     "obrigatoria": false,
     "reduz_faixa_ate": 38000
    },
    {
     "prioridade": 56,
     "texto": "O acabamento do imóvel é simples, normal ou de alto padrão?",
     "codigo": "PADRAO",
     "obrigatoria": false,
     "reduz_faixa_ate": 36000
    }
   ],
   "perguntas_candidatas": 2,
   "confianca": "ALTA",
   "confianca_score": 76,
   "confianca_motivo": "todos os dados críticos observados",
   "completude": {
    "faltantes": [
     "padrao_construtivo_cadastrado",
     "material_parede_externa_cadastrado"
    ],
    "pct": 33
   },
   "canal": "ONE_CLICK",
   "jornada": "UM_TOQUE",
   "motivo_jornada": "nenhuma pergunta trava a contratação: contrata com a faixa sugerida e as perguntas só ajustam o valor",
   "fontes": [
    "SINAPI 2026-09 (IBGE)",
    "CUB R8-N oficial dos Sinduscons",
    "IPCA 12m até 09/2026, série 433 (Banco Central)",
    "Condições Gerais BB Seguro Residencial v1.4",
    "Atlas Digital de Desastres no Brasil / S2iD (Sedec/MIDR), registros de 1991 a 2025",
    "BB Seguros, dado divulgado à imprensa (Monitor Mercantil, 22/07/2026): acionamentos jan/2023 a mai/2026 [fonte secundária]",
    "Ranking de Continuidade do Fornecimento 2025 (ANEEL)"
   ],
   "sinais": {
    "parcela": 950.0,
    "aluguel": 0.0,
    "vidracaria": 11000.0,
    "obra": 0.0
   }
  },
  "IMO_CASO_00008_01": {
   "cliente_id": "CASO_00008",
   "imovel_id": "IMO_CASO_00008_01",
   "local": "Fortaleza/CE",
   "complemento": "AP 204",
   "canal_digital": {
    "usuario_app": "SIM",
    "maturidade_digital": 93
   },
   "campos": {
    "tipo": {
     "valor": "APARTAMENTO",
     "natureza": "INFERIDO",
     "confianca": "ALTA",
     "fonte": "termo 'apartamento' no endereço; confirmado pelo complemento",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "diverge": false,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "vinculo": {
     "valor": "INQUILINO",
     "natureza": "OBSERVADO",
     "confianca": "ALTA",
     "fonte": "aluguel recorrente de R$ 1.500/mês",
     "fonte_tipo": "TRANSACAO",
     "idade_meses": 3,
     "peso": 0.673,
     "classe": "OBSERVADO"
    },
    "uso": {
     "valor": "RESIDENCIAL_HABITUAL",
     "natureza": "OBSERVADO",
     "confianca": "ALTA",
     "fonte": "endereço compatível com o endereço principal do cliente",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "area": {
     "valor": 125,
     "natureza": "OBSERVADO",
     "confianca": "ALTA",
     "fonte": "área cadastrada (CADASTRO_PUBLICO_MUNICIPAL)",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "min": 125.0,
     "max": 125.0,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "bens": {
     "valor": 36700,
     "natureza": "ESTIMADO",
     "confianca": "ALTA",
     "fonte": "compras de R$ 18.550 nos últimos 36 meses (corrigidas pelo IPCA) e 5 bens vinculados (R$ 7.750 ponderado pela chance de estarem no imóvel)",
     "fonte_tipo": "TRANSACAO",
     "idade_meses": 18,
     "min": 19837.763056706597,
     "max": 53561.96025310781,
     "categorias": {
      "eletronicos": {
       "min": 8983.137987942611,
       "max": 24254.47256744505
      },
      "eletrodomesticos": {
       "min": 3796.445221094794,
       "max": 10250.402096955942
      },
      "moveis": {
       "min": 7058.179847669194,
       "max": 19057.085588706825
      }
     },
     "portateis": {
      "min": 8983.137987942611,
      "max": 24254.47256744505
     },
     "eletricos": {
      "min": 12779.583209037404,
      "max": 34504.874664400995
     },
     "molhaveis": {
      "min": 19837.763056706597,
      "max": 53561.96025310781
     },
     "peso": 0.566,
     "classe": "OBSERVADO"
    }
   },
   "valor_imovel": {
    "custo_m2": [
     1976.96,
     2920.12
    ],
    "fator_padrao": [
     1.0,
     1.3
    ],
    "origem_padrao": "estimado pelo IPTU/m²",
    "reconstrucao_min": 247000,
    "reconstrucao_max": 365000,
    "segundo_risco": true,
    "estrutura_do_locador": false
   },
   "elegibilidade": "SIM",
   "pendencias": [],
   "avisos": [],
   "plano": "TOTAL",
   "motivos": [
    {
     "plano": "TOTAL",
     "peso": 2,
     "codigo": "INQUILINO",
     "texto": "você paga R$ 1,5 mil de aluguel por mês e, se o imóvel ficar inabitável, precisaria pagar outra moradia"
    },
    {
     "plano": "TOTAL",
     "peso": 1,
     "codigo": "VIZINHOS",
     "texto": "em prédio ou condomínio, um vazamento ou incêndio no seu imóvel pode atingir o vizinho"
    }
   ],
   "motivos_plano": [
    {
     "plano": "TOTAL",
     "peso": 2,
     "codigo": "INQUILINO",
     "texto": "você paga R$ 1,5 mil de aluguel por mês e, se o imóvel ficar inabitável, precisaria pagar outra moradia"
    },
    {
     "plano": "TOTAL",
     "peso": 1,
     "codigo": "VIZINHOS",
     "texto": "em prédio ou condomínio, um vazamento ou incêndio no seu imóvel pode atingir o vizinho"
    }
   ],
   "pontos": {
    "pratico": 0,
    "total": 3
   },
   "alternativa": {
    "plano": "PRATICO",
    "texto": "Prático: mais barato, sem o conserto de danos a terceiros, a perda de aluguel e as despesas emergenciais"
   },
   "por_que_nao_abaixo": "o Prático não cobre o conserto de danos a terceiros, a perda de aluguel e as despesas emergenciais",
   "por_que_nao_acima": "",
   "adicionais": [],
   "coberturas": [
    {
     "cobertura": "INCENDIO_RAIO_EXPLOSAO_FUMACA",
     "tipo": "FIXA",
     "min": 100000,
     "max": 200000,
     "confianca": "MEDIA",
     "dados_utilizados": "área, tipo, vínculo, UF, padrão, compras 36m, bens; SINAPI, CUB, IPCA",
     "regra": "área 125–125 m² × R$ 1.977–R$ 2.920/m² (SINAPI CE até SINAPI CE × 1.136 (razão CUB/SINAPI das UFs com CUB oficial), padrão estimado pelo IPTU/m²: fator 1,00 a 1,30) × 25%–40% (acabamentos) + bens",
     "justificativa": "A estrutura tem seguro próprio (condomínio ou financiamento); o seu paga os acabamentos, estimados em de R$ 62 mil a R$ 146 mil, e repõe o que você comprou para a casa, de R$ 20 mil a R$ 54 mil.",
     "confirmar": "Área do imóvel e valor dos bens",
     "observacao": "Segundo risco (CG cl. 15.2): a estrutura é paga primeiro pelo seguro do condomínio ou do financiamento. Imóvel alugado: beneficiários distintos (locador para o imóvel, locatário para o conteúdo).",
     "limitada_pelo_produto": false,
     "sugerido": 141000,
     "valor_em_risco": 141000,
     "valor_em_risco_max": 200000
    },
    {
     "cobertura": "DANOS_POR_AGUA",
     "tipo": "FIXA",
     "min": 17500,
     "max": 50000,
     "confianca": "MEDIA",
     "dados_utilizados": "bens molháveis, reconstrução",
     "regra": "50%–100% dos bens molháveis + 3%–8% da reconstrução (pisos e acabamentos)",
     "justificativa": "Um cano rompido ou uma chuva forte estraga móveis e eletrodomésticos, e os seus valem hoje de R$ 20 mil a R$ 54 mil. A faixa cobre esses bens e parte de pisos e paredes. Na BB Seguros, 14,6% dos acionamentos do residencial são de danos por água (jan/2023 a mai/2026). Em Fortaleza, a Defesa Civil registrou 3 ocorrências de chuvas intensas, alagamentos ou enxurradas desde 1991 (0 nos últimos 10 anos; a última em 2004).",
     "confirmar": "",
     "observacao": "O máximo estimado (R$ 83.000) passa do limite do produto (R$ 50.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 34000
    },
    {
     "cobertura": "VENDAVAL_GRANIZO",
     "tipo": "FIXA",
     "min": 5000,
     "max": 18500,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo, reconstrução",
     "regra": "2%–5% da reconstrução",
     "justificativa": "Em apartamento, vento e granizo atingem sobretudo janelas e esquadrias: repor de 2% a 5% do imóvel custa de R$ 4,9 mil a R$ 18 mil. Na BB Seguros, 11,5% dos acionamentos do residencial são de vendaval e granizo (jan/2023 a mai/2026).",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 12000
    },
    {
     "cobertura": "IMPACTO_VEICULOS_TERRESTRES",
     "tipo": "FIXA",
     "min": 10000,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel",
     "regra": "padrão do produto (casa até R$ 20 mil)",
     "justificativa": "Em apartamento, um carro raramente atinge a sua unidade; fica no valor padrão de R$ 10 mil.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 10000
    },
    {
     "cobertura": "QUEDA_AERONAVE",
     "tipo": "FIXA",
     "min": 10000,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "padrão do produto",
     "regra": "padrão do produto",
     "justificativa": "Evento raro: fica no valor padrão do produto, R$ 10 mil, sem precisar de pergunta.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 10000
    },
    {
     "cobertura": "DANOS_ELETRICOS",
     "tipo": "FIXA",
     "min": 13000,
     "max": 30000,
     "confianca": "ALTA",
     "dados_utilizados": "compras de eletrônicos e eletrodomésticos (36m), bens vinculados; IPCA",
     "regra": "eletrônicos + eletrodomésticos: comprovado → estoque, a preço de hoje",
     "justificativa": "Seus eletrônicos e eletrodomésticos valem hoje de R$ 13 mil a R$ 35 mil, e um pico de energia pode queimar vários de uma vez. Desgaste e mau uso não são cobertos. Na BB Seguros, 53,3% dos acionamentos do residencial são de danos elétricos (jan/2023 a mai/2026). A distribuidora de Fortaleza (ENEL CE) ficou em 23º de 33 no ranking de continuidade da ANEEL de 2025 (1º = menos quedas de energia).",
     "confirmar": "Principais aparelhos da casa",
     "observacao": "O máximo estimado (R$ 35.000) passa do limite do produto (R$ 30.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 22000
    },
    {
     "cobertura": "ROUBO_FURTO_ARROMBAMENTO",
     "tipo": "FIXA",
     "min": 9000,
     "max": 24000,
     "confianca": "ALTA",
     "dados_utilizados": "compras de eletrônicos (36m), bens vinculados; IPCA",
     "regra": "eletrônicos e portáteis: comprovado → estoque, a preço de hoje",
     "justificativa": "Seus eletrônicos, os itens mais levados num arrombamento, valem hoje de R$ 9 mil a R$ 24 mil; a faixa repõe esses bens a preço de hoje. Na BB Seguros, 2,1% dos acionamentos do residencial são de roubo ou furto com arrombamento (jan/2023 a mai/2026).",
     "confirmar": "Bens portáteis de maior valor",
     "observacao": "Não cobre joias, relógios, dinheiro, drones nem bicicleta fora de casa (CG cl. 6; Roubo 2.1).",
     "limitada_pelo_produto": false,
     "sugerido": 16500
    },
    {
     "cobertura": "QUEBRA_DE_VIDROS",
     "tipo": "FIXA",
     "min": 2000,
     "max": 5000,
     "confianca": "BAIXA",
     "dados_utilizados": "tipo do imóvel, gastos com vidraçaria 24m",
     "regra": "faixa por tipo, ampliada para 1,2 × o gasto com vidraçaria",
     "justificativa": "Num apartamento de cerca de 125 m², repor box, janelas e tampos de vidro costuma custar de R$ 2 mil a R$ 5 mil.",
     "confirmar": "Há vidros grandes (sacada, box, fachada)?",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 3500
    },
    {
     "cobertura": "RESPONSABILIDADE_CIVIL_FAMILIAR",
     "tipo": "FIXA",
     "min": 74000,
     "max": 200000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel; SINAPI, CUB",
     "regra": "reparo de uma unidade vizinha do mesmo tamanho: 125 m² × R$ 1.977–R$ 2.920/m² (SINAPI CE até SINAPI CE × 1.136 (razão CUB/SINAPI das UFs com CUB oficial), padrão estimado pelo IPTU/m²: fator 1,00 a 1,30) × 30%–60%",
     "justificativa": "Um vazamento ou incêndio no seu imóvel pode atingir a unidade vizinha, de tamanho parecido com a sua (cerca de 125 m²): repará-la custa de R$ 74 mil a R$ 219 mil, e a cobertura paga isso no seu lugar.",
     "confirmar": "",
     "observacao": "O máximo estimado (R$ 219.000) passa do limite do produto (R$ 200.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 137000
    },
    {
     "cobertura": "PERDA_PAGAMENTO_ALUGUEL",
     "tipo": "FIXA",
     "min": 9000,
     "max": 18000,
     "confianca": "ALTA",
     "dados_utilizados": "aluguel pago (transações)",
     "regra": "aluguel mensal × 6 a 12 meses",
     "justificativa": "Você paga R$ 1,5 mil de aluguel por mês; se o imóvel ficar inabitável, a faixa paga outra moradia por 6 a 12 meses.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 13500
    },
    {
     "cobertura": "DESPESAS_EMERGENCIAIS",
     "tipo": "FIXA",
     "min": 2000,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "faixa de incêndio",
     "regra": "2%–5% da faixa de incêndio",
     "justificativa": "Lona no telhado, retirada de entulho e outras medidas urgentes para o dano não aumentar: de 2% a 5% da faixa de incêndio, ou de R$ 2 mil a R$ 10 mil.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 6000
    }
   ],
   "perguntas": [
    {
     "prioridade": 58,
     "texto": "Seus móveis, eletrodomésticos e eletrônicos ficam entre R$ 20 mil e R$ 54 mil?",
     "codigo": "BENS",
     "obrigatoria": false,
     "reduz_faixa_ate": 34000
    },
    {
     "prioridade": 56,
     "texto": "O acabamento do imóvel é simples, normal ou de alto padrão?",
     "codigo": "PADRAO",
     "obrigatoria": false,
     "reduz_faixa_ate": 34000
    }
   ],
   "perguntas_candidatas": 2,
   "confianca": "ALTA",
   "confianca_score": 76,
   "confianca_motivo": "todos os dados críticos observados",
   "completude": {
    "faltantes": [
     "padrao_construtivo_cadastrado"
    ],
    "pct": 67
   },
   "canal": "ONE_CLICK",
   "jornada": "UM_TOQUE",
   "motivo_jornada": "nenhuma pergunta trava a contratação: contrata com a faixa sugerida e as perguntas só ajustam o valor",
   "fontes": [
    "SINAPI 2026-09 (IBGE)",
    "CUB R8-N oficial dos Sinduscons",
    "IPCA 12m até 09/2026, série 433 (Banco Central)",
    "Condições Gerais BB Seguro Residencial v1.4",
    "Atlas Digital de Desastres no Brasil / S2iD (Sedec/MIDR), registros de 1991 a 2025",
    "BB Seguros, dado divulgado à imprensa (Monitor Mercantil, 22/07/2026): acionamentos jan/2023 a mai/2026 [fonte secundária]",
    "Ranking de Continuidade do Fornecimento 2025 (ANEEL)"
   ],
   "sinais": {
    "parcela": 0.0,
    "aluguel": 1500.0,
    "vidracaria": 0.0,
    "obra": 1500.0
   }
  },
  "IMO_CASO_00003_01": {
   "cliente_id": "CASO_00003",
   "imovel_id": "IMO_CASO_00003_01",
   "local": "Curitiba/PR",
   "complemento": "QUADRA 8 CASA 15",
   "canal_digital": {
    "usuario_app": "SIM",
    "maturidade_digital": 66
   },
   "campos": {
    "tipo": {
     "valor": "CASA",
     "natureza": "INFERIDO",
     "confianca": "ALTA",
     "fonte": "termo 'casa' no endereço, sem condomínio; confirmado pelo complemento",
     "fonte_tipo": "DOCUMENTO",
     "idade_meses": 0,
     "diverge": false,
     "peso": 0.9,
     "classe": "OBSERVADO"
    },
    "vinculo": {
     "valor": "PROPRIETARIO_LOCADOR",
     "natureza": "INFERIDO",
     "confianca": "MEDIA",
     "fonte": "recebe crédito recorrente compatível com aluguel (R$ 8.350/mês)",
     "fonte_tipo": "TRANSACAO",
     "idade_meses": 3,
     "peso": 0.673,
     "classe": "OBSERVADO"
    },
    "uso": {
     "valor": "RESIDENCIAL_LOCADO_A_TERCEIROS",
     "natureza": "INFERIDO",
     "confianca": "MEDIA",
     "fonte": "não é o endereço principal e há crédito de aluguel",
     "fonte_tipo": "TRANSACAO",
     "idade_meses": 3,
     "peso": 0.673,
     "classe": "OBSERVADO"
    },
    "area": {
     "valor": 166,
     "natureza": "ESTIMADO",
     "confianca": "MEDIA",
     "fonte": "estimada pelo IPTU (R$ 2.650/ano) e energia (R$ 450/mês) comparados a imóveis de Curitiba",
     "fonte_tipo": "DERIVADO",
     "idade_meses": 3,
     "min": 120.53540444339436,
     "max": 215.20059659694616,
     "peso": 0.688,
     "classe": "ESTIMADO"
    },
    "bens": {
     "valor": 77159,
     "natureza": "ESTIMADO",
     "confianca": "ALTA",
     "fonte": "compras de R$ 39.000 nos últimos 36 meses (corrigidas pelo IPCA) e 4 bens vinculados (R$ 9.100 ponderado pela chance de estarem no imóvel)",
     "fonte_tipo": "TRANSACAO",
     "idade_meses": 18,
     "min": 41707.42637259069,
     "max": 112610.05120599487,
     "categorias": {
      "eletronicos": {
       "min": 9678.261760819121,
       "max": 26131.30675421163
      },
      "eletrodomesticos": {
       "min": 12565.698971229247,
       "max": 33927.38722231897
      },
      "moveis": {
       "min": 19463.465640542323,
       "max": 52551.35722946427
      }
     },
     "portateis": {
      "min": 9678.261760819121,
      "max": 26131.30675421163
     },
     "eletricos": {
      "min": 22243.96073204837,
      "max": 60058.6939765306
     },
     "molhaveis": {
      "min": 41707.42637259069,
      "max": 112610.05120599487
     },
     "peso": 0.566,
     "classe": "OBSERVADO"
    }
   },
   "valor_imovel": {
    "custo_m2": [
     1944.32,
     3560.61
    ],
    "fator_padrao": [
     0.85,
     1.3
    ],
    "origem_padrao": "não cadastrado",
    "reconstrucao_min": 234000,
    "reconstrucao_max": 766000,
    "segundo_risco": false,
    "estrutura_do_locador": false
   },
   "elegibilidade": "SIM",
   "pendencias": [
    {
     "codigo": "POSSIVEL_REFORMA",
     "prioridade": 100,
     "texto": "gastos de R$ 15.150 em material de construção em 24 meses podem indicar reforma, que impede a contratação",
     "pergunta": "Notamos R$ 15 mil em material de construção nos últimos 2 anos. O imóvel está em obra ou reforma agora?"
    }
   ],
   "avisos": [],
   "plano": "TOTAL",
   "motivos": [
    {
     "plano": "TOTAL",
     "peso": 2,
     "codigo": "RECEBE_ALUGUEL",
     "texto": "este imóvel rende cerca de R$ 8,3 mil de aluguel por mês, que para de entrar se ele precisar de reparo"
    },
    {
     "plano": "PRATICO",
     "peso": 2,
     "codigo": "BENS_ALTOS",
     "texto": "suas compras para a casa nos últimos 3 anos valem hoje pelo menos R$ 42 mil"
    },
    {
     "plano": "PRATICO",
     "peso": 1,
     "codigo": "CASA_SEM_CONDOMINIO",
     "texto": "a casa fica fora de condomínio, mais exposta a arrombamento"
    }
   ],
   "motivos_plano": [
    {
     "plano": "TOTAL",
     "peso": 2,
     "codigo": "RECEBE_ALUGUEL",
     "texto": "este imóvel rende cerca de R$ 8,3 mil de aluguel por mês, que para de entrar se ele precisar de reparo"
    },
    {
     "plano": "PRATICO",
     "peso": 2,
     "codigo": "BENS_ALTOS",
     "texto": "suas compras para a casa nos últimos 3 anos valem hoje pelo menos R$ 42 mil"
    }
   ],
   "pontos": {
    "pratico": 3,
    "total": 2
   },
   "alternativa": {
    "plano": "PRATICO",
    "texto": "Prático: mais barato, sem o conserto de danos a terceiros, a perda de aluguel e as despesas emergenciais"
   },
   "por_que_nao_abaixo": "o Prático não cobre o conserto de danos a terceiros, a perda de aluguel e as despesas emergenciais",
   "por_que_nao_acima": "",
   "adicionais": [],
   "coberturas": [
    {
     "cobertura": "INCENDIO_RAIO_EXPLOSAO_FUMACA",
     "tipo": "FIXA",
     "min": 276000,
     "max": 600000,
     "confianca": "MEDIA",
     "dados_utilizados": "área, tipo, vínculo, UF, padrão, compras 36m, bens; SINAPI, CUB, IPCA",
     "regra": "área 121–215 m² × R$ 1.944–R$ 3.561/m² (SINAPI PR até CUB PR oficial, padrão não cadastrado: fator 0,85 a 1,30) + bens",
     "justificativa": "Se um incêndio atingir o imóvel, reconstruir custaria de R$ 234 mil a R$ 766 mil pelo custo oficial de construção, e repor o que você comprou para a casa, de R$ 42 mil a R$ 113 mil. Com limite único, a reconstrução é paga primeiro.",
     "confirmar": "Área do imóvel e valor dos bens",
     "observacao": "Limite único prédio + conteúdo, com prioridade do prédio (CG cl. 5.5–5.6). Imóvel alugado a terceiros: os bens do inquilino são dele (locatário); confirme se o imóvel é alugado mobiliado com bens seus. O máximo estimado (R$ 879.000) passa do limite do produto (R$ 600.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 577000,
     "valor_em_risco": 577000,
     "valor_em_risco_max": 879000
    },
    {
     "cobertura": "DANOS_POR_AGUA",
     "tipo": "FIXA",
     "min": 28000,
     "max": 50000,
     "confianca": "MEDIA",
     "dados_utilizados": "bens molháveis, reconstrução",
     "regra": "50%–100% dos bens molháveis + 3%–8% da reconstrução (pisos e acabamentos)",
     "justificativa": "Um cano rompido ou uma chuva forte estraga móveis e eletrodomésticos, e os seus valem hoje de R$ 42 mil a R$ 113 mil. A faixa cobre esses bens e parte de pisos e paredes. Na BB Seguros, 14,6% dos acionamentos do residencial são de danos por água (jan/2023 a mai/2026). Em Curitiba, a Defesa Civil registrou 17 ocorrências de chuvas intensas, alagamentos ou enxurradas desde 1991 (10 nos últimos 10 anos; a última em 2025).",
     "confirmar": "",
     "observacao": "O máximo estimado (R$ 174.000) passa do limite do produto (R$ 50.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 39000
    },
    {
     "cobertura": "VENDAVAL_GRANIZO",
     "tipo": "FIXA",
     "min": 23000,
     "max": 60000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo, reconstrução",
     "regra": "10%–20% da reconstrução",
     "justificativa": "Vento e granizo atingem primeiro o telhado: refazer de 10% a 20% de uma casa como a sua custa de R$ 23 mil a R$ 153 mil. Na BB Seguros, 11,5% dos acionamentos do residencial são de vendaval e granizo (jan/2023 a mai/2026). Em Curitiba, a Defesa Civil registrou 10 ocorrências de vendaval, ciclone ou granizo desde 1991 (7 nos últimos 10 anos; a última em 2025).",
     "confirmar": "",
     "observacao": "O máximo estimado (R$ 153.000) passa do limite do produto (R$ 60.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 42000
    },
    {
     "cobertura": "IMPACTO_VEICULOS_TERRESTRES",
     "tipo": "FIXA",
     "min": 10000,
     "max": 20000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel",
     "regra": "padrão do produto (casa até R$ 20 mil)",
     "justificativa": "Um carro desgovernado atinge primeiro muro, portão e fachada; por isso a casa vai até R$ 20 mil.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 15000
    },
    {
     "cobertura": "QUEDA_AERONAVE",
     "tipo": "FIXA",
     "min": 10000,
     "max": 10000,
     "confianca": "MEDIA",
     "dados_utilizados": "padrão do produto",
     "regra": "padrão do produto",
     "justificativa": "Evento raro: fica no valor padrão do produto, R$ 10 mil, sem precisar de pergunta.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 10000
    },
    {
     "cobertura": "DANOS_ELETRICOS",
     "tipo": "FIXA",
     "min": 22000,
     "max": 30000,
     "confianca": "ALTA",
     "dados_utilizados": "compras de eletrônicos e eletrodomésticos (36m), bens vinculados; IPCA",
     "regra": "eletrônicos + eletrodomésticos: comprovado → estoque, a preço de hoje",
     "justificativa": "Seus eletrônicos e eletrodomésticos valem hoje de R$ 22 mil a R$ 60 mil, e um pico de energia pode queimar vários de uma vez. Desgaste e mau uso não são cobertos. Na BB Seguros, 53,3% dos acionamentos do residencial são de danos elétricos (jan/2023 a mai/2026). A distribuidora de Curitiba (COPEL) ficou em 27º de 33 no ranking de continuidade da ANEEL de 2025 (1º = menos quedas de energia).",
     "confirmar": "Principais aparelhos da casa",
     "observacao": "O máximo estimado (R$ 60.000) passa do limite do produto (R$ 30.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 26000
    },
    {
     "cobertura": "ROUBO_FURTO_ARROMBAMENTO",
     "tipo": "FIXA",
     "min": 9500,
     "max": 26000,
     "confianca": "ALTA",
     "dados_utilizados": "compras de eletrônicos (36m), bens vinculados; IPCA",
     "regra": "eletrônicos e portáteis: comprovado → estoque, a preço de hoje",
     "justificativa": "Seus eletrônicos, os itens mais levados num arrombamento, valem hoje de R$ 9,7 mil a R$ 26 mil; a faixa repõe esses bens a preço de hoje. Na BB Seguros, 2,1% dos acionamentos do residencial são de roubo ou furto com arrombamento (jan/2023 a mai/2026).",
     "confirmar": "Bens portáteis de maior valor",
     "observacao": "Não cobre joias, relógios, dinheiro, drones nem bicicleta fora de casa (CG cl. 6; Roubo 2.1).",
     "limitada_pelo_produto": false,
     "sugerido": 18000
    },
    {
     "cobertura": "QUEBRA_DE_VIDROS",
     "tipo": "FIXA",
     "min": 3000,
     "max": 8000,
     "confianca": "BAIXA",
     "dados_utilizados": "tipo do imóvel, gastos com vidraçaria 24m",
     "regra": "faixa por tipo, ampliada para 1,2 × o gasto com vidraçaria",
     "justificativa": "Numa casa de cerca de 166 m², repor box, janelas e tampos de vidro costuma custar de R$ 3 mil a R$ 8 mil.",
     "confirmar": "Há vidros grandes (sacada, box, fachada)?",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 5500
    },
    {
     "cobertura": "RESPONSABILIDADE_CIVIL_FAMILIAR",
     "tipo": "FIXA",
     "min": 30000,
     "max": 60000,
     "confianca": "MEDIA",
     "dados_utilizados": "tipo do imóvel; SINAPI, CUB",
     "regra": "casa: faixa de referência de danos a terceiros",
     "justificativa": "Numa casa de cerca de 166 m², o risco a terceiros vem de muro, telhado ou árvore que atinge o vizinho, ou de um acidente com dependentes ou pet; a faixa de referência vai de R$ 30 mil a R$ 60 mil.",
     "confirmar": "",
     "observacao": "",
     "limitada_pelo_produto": false,
     "sugerido": 45000
    },
    {
     "cobertura": "PERDA_PAGAMENTO_ALUGUEL",
     "tipo": "FIXA",
     "min": 30000,
     "max": 30000,
     "confianca": "MEDIA",
     "dados_utilizados": "aluguel recebido (transações)",
     "regra": "aluguel mensal × 6 a 12 meses",
     "justificativa": "Você recebe cerca de R$ 8,3 mil de aluguel por mês; se o imóvel precisar de reparo, a faixa repõe de 6 a 12 meses.",
     "confirmar": "Valor de aluguel de um imóvel equivalente",
     "observacao": "Toda a estimativa (R$ 100.000) passa do limite do produto (R$ 30.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 30000
    },
    {
     "cobertura": "DESPESAS_EMERGENCIAIS",
     "tipo": "FIXA",
     "min": 5500,
     "max": 15000,
     "confianca": "MEDIA",
     "dados_utilizados": "faixa de incêndio",
     "regra": "2%–5% da faixa de incêndio",
     "justificativa": "Lona no telhado, retirada de entulho e outras medidas urgentes para o dano não aumentar: de 2% a 5% da faixa de incêndio, ou de R$ 5,5 mil a R$ 30 mil.",
     "confirmar": "",
     "observacao": "O máximo estimado (R$ 30.000) passa do limite do produto (R$ 15.000): o valor acima do limite fica descoberto.",
     "limitada_pelo_produto": true,
     "sugerido": 10000
    }
   ],
   "perguntas": [
    {
     "prioridade": 100,
     "texto": "Notamos R$ 15 mil em material de construção nos últimos 2 anos. O imóvel está em obra ou reforma agora?",
     "codigo": "POSSIVEL_REFORMA",
     "obrigatoria": true
    },
    {
     "prioridade": 58,
     "texto": "Estimamos que o imóvel tem cerca de 166 m². Confere?",
     "codigo": "AREA",
     "obrigatoria": false,
     "reduz_faixa_ate": 324000
    },
    {
     "prioridade": 56,
     "texto": "O acabamento do imóvel é simples, normal ou de alto padrão?",
     "codigo": "PADRAO",
     "obrigatoria": false,
     "reduz_faixa_ate": 265000
    }
   ],
   "perguntas_candidatas": 4,
   "confianca": "MEDIA",
   "confianca_score": 56,
   "confianca_motivo": "estimado: área; elegibilidade a confirmar",
   "completude": {
    "faltantes": [
     "area_cadastrada_m2",
     "padrao_construtivo_cadastrado",
     "material_parede_externa_cadastrado"
    ],
    "pct": 0
   },
   "canal": "GERENTE",
   "jornada": "GERENTE",
   "motivo_jornada": "sinal de obra ou reforma, que impede a contratação e pede conversa",
   "fontes": [
    "SINAPI 2026-09 (IBGE)",
    "CUB R8-N oficial dos Sinduscons",
    "IPCA 12m até 09/2026, série 433 (Banco Central)",
    "Condições Gerais BB Seguro Residencial v1.4",
    "Atlas Digital de Desastres no Brasil / S2iD (Sedec/MIDR), registros de 1991 a 2025",
    "BB Seguros, dado divulgado à imprensa (Monitor Mercantil, 22/07/2026): acionamentos jan/2023 a mai/2026 [fonte secundária]",
    "Ranking de Continuidade do Fornecimento 2025 (ANEEL)"
   ],
   "sinais": {
    "parcela": 0.0,
    "aluguel": 0.0,
    "vidracaria": 0.0,
    "obra": 15150.0
   }
  }
 }
};
