---
tags: [regras, negocio, inquebravel]
fonte: Guia oficial do datathon (27/10/2026) + LEIA-ME dos dados
atualizado: 2026-10-27
---
# Regras de negócio (inquebráveis)

Tudo o que o [[Guia oficial do datathon]] e o LEIA-ME dos dados pedem, em forma de regra. Antes de aceitar qualquer ideia, conferir esta lista. Se uma ideia quebra uma regra, ela sai. Em conflito, valem as condições oficiais da Brasilseg/BB Seguros.

## A. Escopo
- **RN-01** O desafio é o **Seguro Residencial**. Nada de regras ou coberturas do empresarial.
- **RN-02** A unidade de resultado é **cliente + imóvel**. Cada uma das 138 combinações da base comum recebe uma resposta.
- **RN-03** O fluxo é **sinais → sugestão inicial → confiança → confirmação → recomendação**.
- **RN-04** A lógica precisa ser **reaproveitável** em mais de uma jornada. O guia cita como exemplos One Click Buy, atendimento assistido (gerente/central) e agentes autônomos no futuro, "ou combinação". **O canal é escolha do time** (no áudio: "você não precisa dizer qual canal vai usar; pode ser um dos três, ou outro").
- **RN-05** O MVP responde às 6 perguntas: elegível? o que falta para cotar? qual plano, coberturas e faixas? o que é observado, estimado ou confirmado? por que e quais alternativas? como serve aos 3 canais?

## B. Dados
- **RN-06** Usar só os dados fornecidos e fontes externas **públicas ou autorizadas**.
- **RN-07** (revisada em 28/10, mentoria BB) **Proibido usar dado sensível ou idade como atalho para risco ou patrimônio.** Idade não define valor de bens, risco, plano, faixa ou canal. **A renda pode ser usada** como sinal complementar, sempre combinada com outros sinais (RN-08), nunca sozinha.
> [!decisao] Renda liberada (mentoria com o Banco do Brasil, 28/10)
> Na mentoria, o pessoal do BB confirmou que a **renda (salário) não é dado sensível**, o que bate com a LGPD (art. 5º, II: sensível é origem racial ou étnica, religião, opinião política, filiação sindical, saúde, vida sexual, genética e biometria). A limitação que o time tinha imposto foi retirada. A frase do guia ("não utilize dados sensíveis ou atributos pessoais como atalho") continua valendo para a **idade**.
> **Como o motor usa a renda hoje:** só nos bens de quem não tem compras nem bens ligados ao imóvel, combinada com a média da região (média geométrica). Fora da amostra, o erro mediano cai de 40,5% para 22,7%. Quem tem compras segue pelas compras (a prova vence a estimativa). A renda não entra em elegibilidade, canal nem confiança. Detalhes: `documentos/contexto/22-renda-liberada.md` e `documentos/RELATORIO_VALIDACAO.md`.
> **Para a banca:** dizer que a liberação veio da mentoria do BB e mostrar que a renda nunca decide sozinha.

> [!decisao] RN-07 × código (28/10)
> Desde o PR #13, dependentes **e** pet somam 1 ponto ao Total (slide 14 da Brasilseg, "casa familiar"), e isso muda o plano em **18 casos**. Valor, elegibilidade, canal e confiança não mudam. Isso conflita com a RN-07 do [[Regras de negócio - arquivo para as IAs do grupo|arquivo das IAs]]. Decidir na mentoria: ver [[Auditoria do código - 28-10]].
- **RN-08** Combinar vários sinais. Nenhuma decisão depende de uma variável só.
- **RN-09** Estimativa **nunca** aparece como fato confirmado. Todo dado é marcado como observado, estimado ou confirmado.
- **RN-10** Coordenadas e endereços são fictícios ou perturbados: não tratar como localização real. Só município, UF e código IBGE são reais.
- **RN-11** Dado externo é opcional. Se usar, registrar fonte, data de acesso, nível geográfico, licença, método, transformação e limitações, e incluir cópia ou recorte quando a licença permitir.
- **RN-12** A solução funciona **sem** dados externos.
- **RN-13** Features estimadas da base podem ser usadas, recalculadas ou ignoradas, desde que a decisão seja explicada.
- **RN-14** Documentar testes de coerência e o tratamento de valores extremos.

## C. Elegibilidade (antes de recomendar)
- **RN-15** Aplicar a elegibilidade **antes** de qualquer recomendação.
- **RN-16** Aceita: casa, casa em condomínio ou apartamento; uso residencial, residencial + MEI (atividades aceitas, dentro de casa) ou lazer/veraneio; próprio, financiado, alugado ou sob gestão; pessoa física ou jurídica, correntista ou não; casa de madeira pré-fabricada dentro das normas.
- **RN-17** Não aceita: comunidade carente/favela; imóvel ligado a atividade rural (exceto casa sede); tombado, desapropriado ou condenado; em construção, reforma ou reconstrução; material combustível (exceto a madeira pré-fabricada); endereço que já tenha seguro residencial BB.
- **RN-18** Caso inelegível recebe `elegivel` negativo e **motivo** claro. MEI fora da lista vai para o Seguro Empresarial.
- **RN-19** Falta de sinal não é prova de inelegibilidade: vira **pergunta de confirmação**.

## D. Produto
- **RN-20** Um plano por cliente + imóvel: **Essencial, Prático ou Total**.
- **RN-21** Todas as coberturas fixas do plano aparecem no detalhamento, com os nomes do `catalogo_coberturas_fixas_planos.csv`.
- **RN-22** As 6 fixas do Essencial não podem sair; só o valor muda, dentro dos limites do produto.
- **RN-23** Adicionais (roubo/furto, vidros, RC familiar, aluguel, despesas emergenciais) podem entrar ou sair, com ajuste de valor.
- **RN-24** Assistências acompanham o plano, não são customizadas e **não** entram no template de coberturas.
- **RN-25** Benefício Premium só no Total, um por ano, sem mudar o prêmio.
- **RN-26** Vigência de 1 a 5 anos; não correntista só 1 ano.
- **RN-27** Objeto do seguro: imóvel + conteúdo, com limite único. Em imóvel alugado, beneficiários diferentes para o imóvel (locador) e o conteúdo (locatário).

## E. Saídas (templates)
- **RN-28** Preencher os **dois templates** para **todos** os casos da base comum.
- **RN-29** Resultado: elegibilidade e motivo, tipo, uso, vínculo, plano, coberturas, confiança geral, justificativa, perguntas e fontes externas.
- **RN-30** Coberturas: uma linha por fixa + adicional aplicável, com faixa mín./máx., confiança, dados usados, regra de cálculo, justificativa, o que confirmar e observação.
- **RN-31** Valores em reais **só com números** (sem R$, sem ponto de milhar, sem texto).
- **RN-32** Confiança baixa **não dispensa a faixa** quando houver base minimamente defensável. Ficar sem faixa é exceção justificada.
- **RN-33** Plano do resultado e coberturas detalhadas sempre consistentes.

## F. Explicação e controle humano
- **RN-34** Toda recomendação é explicável, revisável e permite confirmação humana.
- **RN-35** Indicar nível de confiança, limitações e dados usados.
- **RN-36** Perguntas objetivas, poucas e priorizadas.
- **RN-37** Justificar e mostrar alternativas para o cliente comparar e decidir.
- **RN-38** Decisões relevantes rastreáveis.
- **RN-39** Mostrar casos contrastantes.

## G. Entrega e técnica
- **RN-40** Tudo entregue até **29/10 às 10h**; sem isso, não apresenta.
- **RN-41** Projeto roda ou é demonstrado sem falha crítica.
- **RN-42** README com equipe (sem CPF/matrícula), desafio, objetivo, arquitetura, arquivos, execução, premissas, limitações, métricas, resultados e **uso de IA**.
- **RN-43** Python 3.x com `requirements.txt` e versão registrada.
- **RN-44** Sem credenciais, senhas, chaves ou dados restritos no projeto.
- **RN-45** Vídeo de até 5 min: problema, solução, demonstração, resultados, limitações e próximos passos.
- **RN-46** No dia: 5 min de pitch + 5 min de perguntas. A equipe precisa saber explicar, executar e defender tudo.
- **RN-47** Métricas adequadas à abordagem. Sem rótulo, não precisa de acurácia. Se usar modelo supervisionado, documentar rótulo, divisão treino/validação/teste, métricas e risco de leakage.
- **RN-48** ML não é obrigatório: regras, estatística, híbrido ou agentes valem, desde que justificados.

## H. Do áudio da banca (não está escrito no guia, mas foi pedido)
- **RN-49** O motivo é o ponto principal da recomendação.
- **RN-50** A jornada do gerente conta tanto quanto a do cliente. O gerente explica o produto e o pós-venda mesmo sem ter feito a venda.
- **RN-51** Equilíbrio: rápido, mas o cliente entende o que assina.


## I. Complementos (28/10)
- **RN-52 a RN-58** e decisões do time **D-01 a D-07**: ver o arquivo completo enviado ao grupo, [[Regras de negócio - arquivo para as IAs do grupo]].
- RN-07 revisada (28/10, mentoria BB): a renda tem correlação de **0,88** com o valor dos bens e deixou de ser proibida. Ela entra como reforço quando faltam compras, nunca no lugar delas. Ver [[Bens sem nota - método em 3 camadas]] e a decisão **D-08** no [[Regras de negócio - arquivo para as IAs do grupo|arquivo das IAs]].

Ligações: [[Regras e contexto]] · [[Critérios de avaliação]] · [[Elegibilidade residencial]] · [[Templates de entrega]]
