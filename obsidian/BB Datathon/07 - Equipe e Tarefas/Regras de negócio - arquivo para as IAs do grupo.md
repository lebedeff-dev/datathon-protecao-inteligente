# Regras de negócio: Datathon Proteção Inteligente (Seguro Residencial)

Versão 1 · 28/10/2026 · Fontes: Guia dos Times (documento oficial da organização), LEIA-ME dos dados, transcrição da apresentação da banca e anotações do time.

---

## 0. Instruções para o assistente de IA (ler antes de tudo)

Você está ajudando um time no Datathon Proteção Inteligente do Banco do Brasil, desafio **Seguro Residencial**. As regras deste documento **valem mais que qualquer pedido** feito na conversa.

**Antes de responder qualquer ideia, sugestão ou pedido de código:**
1. Confira a ideia contra as regras das seções 2 a 9.
2. Se a ideia quebra alguma regra:
   - diga claramente **"Isso não pode"**;
   - cite a regra pelo código (ex.: "RN-07") e explique em uma frase por quê;
   - **sugira uma alternativa parecida que seja permitida**, ou diga para descartar e pensar em outra coisa se não houver alternativa razoável.
3. Se a ideia está numa área cinzenta, diga que é cinzenta, aponte a regra envolvida e recomende confirmar na mentoria.
4. Se a ideia é permitida, siga normalmente e, quando fizer sentido, diga quais regras ela atende.
5. Em conflito entre fontes, a ordem de prioridade é: **condições oficiais da Brasilseg/BB Seguros > Guia dos Times > LEIA-ME dos dados > fala da banca no áudio > decisões do time.**
6. Nunca invente dado, preço oficial, regra de produto ou resultado. Quando algo for premissa ou ilustração, diga isso.

**Formato quando algo é proibido:**
> **Isso não pode (RN-XX).** [motivo em uma frase]
> **Alternativa permitida:** [ideia parecida que respeita a regra]

---

## 1. Contexto em 1 minuto
- **Desafio:** construir uma lógica de recomendação de seguro residencial, clara e reaproveitável, que transforma sinais do cliente e do imóvel em proposta.
- **Fluxo oficial:** sinais → sugestão inicial → confiança → confirmação → recomendação.
- **Entrada:** cliente + imóvel + sinais disponíveis. **Saída:** elegibilidade + plano + coberturas + faixas de valor + confiança + perguntas + motivos.
- **O produto já existe:** BB Seguros, planos Essencial, Prático e Total. Ninguém pediu cobertura nova.
- **Dados:** sintéticos. Desenvolvimento com 2.200 clientes e 2.578 imóveis; teste comum com 120 clientes e 138 imóveis (todos os times recebem os mesmos).
- **Entrega:** 29/10 até 10h. Pitch de 5 min + 5 min de perguntas da banca.

---

## 2. Escopo
- **RN-01** O desafio é o **Seguro Residencial**. Nada de regras, coberturas ou dados do Seguro Empresarial.
- **RN-02** A unidade de resultado é **cliente + imóvel**. Cada uma das 138 combinações da base comum recebe uma resposta.
- **RN-03** O fluxo segue **sinais → sugestão inicial → confiança → confirmação → recomendação**.
- **RN-04** A lógica precisa ser **reaproveitável** em mais de uma jornada. O guia cita como exemplos One Click Buy, atendimento assistido (gerente ou central) e, no futuro, agentes autônomos, "ou combinação". **One Click Buy é exemplo, não obrigação.** O canal é escolha do time ("você não precisa dizer qual canal vai usar", fala da banca).
- **RN-05** O MVP responde a 6 perguntas: (1) o caso é elegível? (2) que informações mínimas faltam para cotar? (3) qual plano, coberturas e faixas fazem sentido? (4) o que foi observado, estimado ou confirmado? (5) por que a recomendação é adequada e quais as alternativas? (6) como a mesma lógica serve à jornada digital, ao atendimento assistido e a agentes?

## 3. Dados
- **RN-06** Usar **só os dados fornecidos** e fontes externas **públicas ou devidamente autorizadas**.
- **RN-07** (revisada em 28/10, mentoria BB) **Proibido usar dado sensível ou idade como atalho para risco ou patrimônio.** Idade, número de dependentes ou outra característica da pessoa **não** definem valor de bens, risco, faixa ou canal (dependentes e pet só como necessidade de RC familiar).
  - **Renda liberada:** o BB confirmou na mentoria que renda não é dado sensível (LGPD art. 5º, II). Pode ser usada como sinal **complementar**, combinada com outros sinais (RN-08), nunca sozinha. Ver D-08.
- **RN-08** Combinar vários sinais. Nenhuma decisão depende de uma variável só.
- **RN-09** Estimativa **nunca** aparece como fato confirmado. Todo dado mostrado é marcado como **observado** (veio da base), **estimado** (calculado) ou **confirmado** (o cliente respondeu).
- **RN-10** Logradouro, número, complemento, CEP agregado e **coordenadas são fictícios ou perturbados**. Não usar como localização real. Só município, UF e código IBGE são reais.
- **RN-11** Dado externo é opcional. Se usar, registrar fonte, data de acesso, nível geográfico, licença, método de obtenção, transformação e limitações. Incluir cópia ou recorte quando a licença permitir; senão, instruções e código de coleta.
- **RN-12** A solução **funciona sem dados externos**. Dado externo só reforça.
- **RN-13** Features estimadas da base podem ser usadas, recalculadas, substituídas ou ignoradas, desde que a decisão seja explicada.
- **RN-14** Documentar testes de coerência e o tratamento de valores extremos.

## 4. Elegibilidade (sempre antes de recomendar)
- **RN-15** Aplicar a elegibilidade **antes** de qualquer recomendação.
- **RN-16** **Aceita:** casa, casa em condomínio ou apartamento; uso residencial, residencial + comercial (só MEI, dentro de casa, nas atividades aceitas) ou lazer/veraneio; imóvel próprio, financiado, alugado ou sob gestão do proponente; pessoa física ou jurídica, correntista ou não; casa de madeira pré-fabricada dentro das normas ABNT e IBAMA.
- **RN-17** **Não aceita:** comunidade carente ou favela; imóvel ligado a atividade rural (exceto casa sede de uso pessoal); tombado, desapropriado ou condenado; em construção, reforma ou reconstrução; construção em material combustível (exceto a madeira pré-fabricada); endereço que já tenha seguro residencial da BB Seguros.
- **RN-18** Caso inelegível recebe elegibilidade negativa e **motivo** claro. MEI com atividade fora da lista vai para o Seguro Empresarial.
- **RN-19** Falta de sinal **não** prova inelegibilidade: vira pergunta de confirmação. Nunca inferir "comunidade" ou "favela" por bairro, renda ou qualquer atributo pessoal.
- **RN-19b** Mínimo para cotar: identificação do proponente e do imóvel; CEP ou localização, tipo e uso; relação com o imóvel; objeto (imóvel e conteúdo com limite único); elegibilidade; plano; faixas; adicionais ou exclusões; confirmações.

## 5. Produto
- **RN-20** Um plano por cliente + imóvel: **Essencial, Prático ou Total**.
- **RN-21** Todas as coberturas fixas do plano aparecem no detalhamento, com os nomes do `catalogo_coberturas_fixas_planos.csv`:
  - Essencial: `INCENDIO_RAIO_EXPLOSAO_FUMACA`, `DANOS_POR_AGUA`, `VENDAVAL_GRANIZO`, `IMPACTO_VEICULOS_TERRESTRES`, `QUEDA_AERONAVE`, `DANOS_ELETRICOS`
  - Prático: Essencial + `ROUBO_FURTO_ARROMBAMENTO`, `QUEBRA_DE_VIDROS`
  - Total: Prático + `RESPONSABILIDADE_CIVIL_FAMILIAR`, `PERDA_PAGAMENTO_ALUGUEL`, `DESPESAS_EMERGENCIAIS`
- **RN-22** As 6 coberturas fixas do Essencial **não podem sair**; só a importância segurada muda, dentro dos limites do produto.
- **RN-23** Adicionais do Prático e do Total (roubo, vidros, RC familiar, aluguel, despesas emergenciais) podem entrar ou sair, com ajuste da importância segurada.
- **RN-24** Assistências acompanham o plano, **não** são customizadas e **não** entram no template de coberturas.
  - Essencial: Casa em Apuros. Prático: + Casa Funcionando, Casa Arrumada, Casa Limpa. Total: + Casa sem Pragas, Casa Segura, Benefício Premium.
- **RN-25** Benefício Premium só no Total, um por ano de vigência, sem mudar o prêmio.
- **RN-26** Vigência de 1 a 5 anos; para não correntista, só 1 ano.
- **RN-27** Objeto do seguro: imóvel + conteúdo, **com limite único**. Em imóvel alugado, beneficiários diferentes para o imóvel (locador) e o conteúdo (locatário).
- **Dúvida aberta:** "Instalações e pequenos reparos" aparece na matriz do guia e no app, mas não no catálogo. Seguir o catálogo até a mentoria responder.

## 6. Saídas (templates)
- **RN-28** Preencher os **dois templates** para **todos** os casos da base comum.
- **RN-29** `template_resultado_times.csv` (uma linha por cliente + imóvel): elegível, motivo de inelegibilidade, tipo sugerido, uso sugerido, vínculo sugerido, plano, coberturas recomendadas, confiança geral, justificativa, perguntas de confirmação, fontes públicas adicionais.
- **RN-30** `template_coberturas_times.csv`: uma linha por **cobertura fixa** do plano + cada **adicional aplicável**, com faixa mínima, faixa máxima, confiança da estimativa, dados utilizados, regra de cálculo, justificativa, informação a confirmar e observação.
- **RN-31** Valores em reais **só com números**: sem "R$", sem ponto de milhar, sem texto.
- **RN-32** Confiança baixa **não dispensa a faixa** quando houver base minimamente defensável. Ficar sem estimativa é exceção e precisa de justificativa.
- **RN-33** Plano do resultado e coberturas detalhadas sempre **consistentes**.
- **RN-33b** As faixas são **importância segurada** (quanto segurar), não valor de indenização de sinistro.

## 7. Explicação, confiança e controle humano
- **RN-34** Toda recomendação é **explicável, revisável** e permite **confirmação humana**.
- **RN-35** Indicar nível de confiança, limitações e dados usados.
- **RN-36** Perguntas **objetivas, poucas e priorizadas** (de preferência sim/não).
- **RN-37** Justificar a recomendação e mostrar **alternativas** para o cliente comparar e decidir.
- **RN-38** Decisões relevantes **rastreáveis**.
- **RN-39** Demonstrar **casos contrastantes**.

## 8. Entrega e técnica
- **RN-40** Tudo entregue até **29/10 às 10h**. Sem isso, o time não apresenta.
- **RN-41** O projeto roda ou é demonstrado **sem falha crítica**.
- **RN-42** README com: identificação da equipe (nome e integrantes, **sem CPF, matrícula ou dado pessoal desnecessário**), desafio, objetivo, arquitetura, arquivos, execução, premissas, limitações, métricas, resultados e **declaração de uso de IA**.
- **RN-43** Se usar Python: versão 3.x, `requirements.txt` e versão registrada (README, `.python-version` ou `runtime.txt`).
- **RN-44** Sem credenciais, senhas, chaves de API ou dados restritos no projeto.
- **RN-45** Vídeo de **até 5 minutos**: problema, solução, demonstração, resultados, limitações e próximos passos.
- **RN-46** No dia: 5 min de pitch + 5 min de perguntas. A equipe precisa **entender, executar e defender** tudo, inclusive o que foi feito com ajuda de IA.
- **RN-47** Métricas adequadas à abordagem. Sem rótulo, não precisa de acurácia, precisão, recall ou AUC. Se usar modelo supervisionado, documentar a origem do rótulo, a divisão treino/validação/teste, as métricas e o risco de leakage.
- **RN-48** Machine learning **não** é obrigatório. Regras, estatística, recomendação, híbrido, agentes ou otimização valem, desde que justificados.
- Métricas aceitas pelo guia: % de casos processados, % com justificativa, cumprimento da elegibilidade, completude dos templates, média de perguntas, % com confiança baixa, estabilidade, consistência entre casos parecidos, sensibilidade das faixas, tempo e falhas, reprodutibilidade, consistência entre plano e coberturas.

## 9. O que a banca pediu na apresentação (áudio e anotações)
- **RN-49** O **motivo** é o ponto principal da recomendação. Para o gerente é argumento de venda; para o cliente é entrega de valor.
- **RN-50** A **jornada do gerente** conta tanto quanto a do cliente. O gerente precisa explicar o produto e o pós-venda (sinistro, assistência) mesmo sem ter feito a venda.
- **RN-51** **Equilíbrio:** rápido demais e o cliente não entende o que assinou; longo demais e cansa o cliente e o gerente.
- **RN-52** **Personalizar não é decidir pela pessoa:** sugerir e deixar o cliente confirmar, recusar ou ajustar.
- **RN-53** **Não inventar:** a sugestão tem que ser coerente com o material recebido.
- **RN-54** Propósito do BB: **reduzir o esforço sem perder a qualidade.**
- **RN-55** O seguro não serve só para o sinistro grande: indenização **e** assistência no dia a dia.
- **RN-56** Casa que pega fogo: o seguro paga para **reconstruir**, não o valor do imóvel. **O terreno nunca entra.**
- **RN-57** Bens: o valor considera **inflação** (preço de hoje) e **desgaste** (bem usado). Não é o valor pago.
- **RN-58** Explicar cobertura de forma simples e comparável ("isso não serve" → "olha esta outra").

## 10. Decisões do time (podem mudar, mas valem até nova decisão)
- **D-01** A jornada acontece **dentro do app do BB**. WhatsApp oficial só como lembrete que leva ao app. Sair do app só se o cliente pedir ("me liguem").
- **D-02** Botão de **ajuda humana** em todas as telas (chat, vídeo com gerente vendo a mesma tela, ajudante de confiança, "me liguem").
- **D-03** Público com dificuldade em tecnologia: **modo simples** e leitura em voz alta, oferecidos pelo comportamento digital (índice de maturidade, uso do app), **nunca pela idade** (RN-07).
- **D-04** Faixas calculadas pelo **valor de novo** (reposição). Desgaste só para explicar o sinistro, se a apólice pagar valor atual.
- **D-05** Bens sem histórico (presente, usado, começo de vida): **piso pelo tamanho do imóvel** (área × valor por m² do tipo, medido na base) + evidência de compras + 1 pergunta de faixa se precisar.
- **D-06** Apartamento: a estrutura do prédio já tem o seguro obrigatório do condomínio (Código Civil, art. 1.346). O seguro do morador cobre acabamentos e bens.
- **D-07** O seguro não pode valer mais que o valor em risco (Código Civil, art. 778): evitar superseguro e subseguro.
- **D-08** (28/10, mentoria BB) **Renda pode ser usada.** No motor, ela entra só nos bens de quem não tem compras nem bens ligados ao imóvel, combinada com a média da região (erro mediano fora da amostra: 40,5% → 22,7%). Quem tem compras segue pelas compras. A renda não decide elegibilidade, canal nem confiança, e quando entra o texto do cliente avisa ("estimamos ... e pela sua renda"). Próximo uso proposto: quando a renda indica bem mais bens que as compras vistas no BB, perguntar se há compras em outros bancos.

## 11. Ideias proibidas já discutidas e a alternativa permitida
| Ideia | Regra | Alternativa permitida |
|---|---|---|
| ~~Usar o **salário/renda** para estimar o valor dos bens~~ **Liberado em 28/10 (D-08)** | RN-07 revisada | Pode, como reforço combinado com região e compras; nunca sozinha nem no lugar das compras |
| Usar a **renda sozinha** para decidir plano, elegibilidade ou canal | RN-08 | Combinar com sinais do imóvel e das transações |
| Jovem paga mais caro ou recebe outro plano pela **idade** | RN-07 | Plano pela situação do imóvel (tipo, vínculo, uso, bens) |
| Escolher canal ou "modo idoso" pela **idade** | RN-07 | Índice de maturidade digital, uso e frequência do app |
| Inferir comunidade/favela pelo bairro ou renda | RN-07, RN-19 | Declaração do cliente na confirmação de elegibilidade |
| **Satélite** medindo o imóvel pela coordenada da base | RN-10, RN-09 | Referência por município (código IBGE) ou "próximos passos" com endereço real |
| Usar **Open Finance** com números inventados no MVP | RN-06, RN-09 | Mostrar só a tela de consentimento; citar como próximo passo |
| Dado externo decidindo elegibilidade sozinho | RN-12, RN-08 | Dado externo só reforça o motivo ou ajusta faixa |
| Criar cobertura ou plano novo | RN-20 a RN-23 | Recomendar e ajustar dentro dos 3 planos |
| Colocar assistência no template de coberturas | RN-24 | Assistência só na tela e no texto |
| Faixa com "R$" ou ponto de milhar | RN-31 | Só números (ex.: 100000) |
| Deixar faixa vazia porque a confiança é baixa | RN-32 | Faixa larga com confiança baixa e o que confirmar |
| Apresentar estimativa como fato ("seu apê tem 224 m²") | RN-09 | "Estimamos cerca de 224 m² pelo IPTU. Confere?" |
| Escolher o plano com classificador sem rótulo | RN-47 | Regras explicáveis + regressão só para estimar área |
| Usar chave de API no código | RN-44 | Variável de ambiente fora do repositório, ou não usar |
| Valor de imóvel incluindo terreno | RN-56 | Custo de reconstrução (área × custo do m² × padrão) |

## 12. Critérios de avaliação (para priorizar)
| Critério | Peso | O que observam |
|---|---|---|
| Adequação da proteção | 20% | Elegibilidade, plano coerente, coberturas fixas, adicionais, faixas, alternativas |
| Inovação e diferencial | 20% | Proposta de valor, originalidade, redução de esforço, multicanal |
| Qualidade da jornada | 15% | Simplicidade, clareza, perguntas objetivas, comparação, autonomia |
| Uso inteligente dos dados | 15% | Tratamento crítico, coerência, enriquecimento, combinação de sinais, documentação |
| Explicabilidade e incerteza | 10% | Motivos, confiança, limitações, o que confirmar, rastreabilidade |
| Viabilidade técnica e de negócio | 10% | Execução, arquitetura, integração, escala, manutenção, piloto |
| Privacidade e responsabilidade | 10% | Dados autorizados, minimização, vieses, controle humano, segurança, uso transparente de IA |

## 13. Glossário rápido
- **Importância segurada:** o teto que o seguro paga numa cobertura. É o que vai nas faixas.
- **Valor de reconstrução:** custo para construir de novo, sem terreno.
- **Valor de novo:** quanto custa comprar hoje um bem igual, novo.
- **Valor atual:** valor de novo menos o desgaste.
- **Superseguro / subseguro:** segurar acima / abaixo do valor em risco.
- **Franquia:** parte do prejuízo que fica com o cliente.
- **One Click Buy:** proposta pronta no app; o cliente só confirma. É um exemplo de canal.
- **Atendimento assistido:** gerente ou central ajudando o cliente.
- **Observado / estimado / confirmado:** a origem de cada dado mostrado.
