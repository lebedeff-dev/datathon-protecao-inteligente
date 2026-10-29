---
tags: [app, especificacao, datathon-bb]
status: pronto para construir
data: 2026-10-28
---
# Especificação do app v2 (ligado ao motor)

> **Para o próximo assistente:** leia antes [[HANDOFF_CONTEXTO]], [[Regras e contexto]] e [[Trajetória do projeto]]. Esta nota é o plano de construção do app da demo. O motor já está pronto e não deve ser mudado sem necessidade (PR [pedroiaan/datathon-protecao-inteligente#13](https://github.com/pedroiaan/datathon-protecao-inteligente/pull/13)).

## 1. Decisão (28/10, Matheus)
- **Continuar com o app simulado dentro do app do Banco do Brasil.** Não criar um app "BB Seguros" separado.
- O app é **só demonstração** (vídeo de 5 min e pitch). Ninguém de fora vai usá-lo. O guia pede "jornada funcionando do início ao resultado" e "projeto em condições de demonstração" (guia §7 e §12).
- **O motor é o produto.** O app é a vitrine: tudo que aparece na tela tem de vir da ficha que o motor gera, nunca de número escrito à mão.
- Melhorias aprovadas: **ligar ao motor**, **botões A/B/C** (perfis do slide 14), **modo raio-X** para a banca e **tela do gerente** usando a ficha.

**Por que não um app novo:** (1) o diferencial é "o banco já sabe, o cliente só confirma", e isso só faz sentido onde o cliente já está logado; (2) o guia fala em One Click Buy dentro das jornadas existentes; (3) prazo: entrega 29/10 às 10h; (4) a nota da jornada premia simplicidade, não tamanho.

## 2. Arquivo base
- **Usar:** `prototipos/indexprototipo_gerente.html` do repositório do Pedro (clone local: `C:\Users\maxom\Documents\datathon-protecao-inteligente`, branch `revisao-qa-p1-p5`).
- Ele foi construído a partir do protótipo do Matheus (`C:\Users\maxom\Documents\Claude BB Datathon\prototipo\index.html`): mesmas telas, mesmas funções (`telaGancho`, `telaEsse`, `telaCasa`, `telaPlano`, `telaCobre`, `telaAjuste`, `telaFechar`, `telaMeu`), mesmo visual BB. **E já lê as fichas do motor** (`aplicarFicha`, `window.FICHAS_DEMO`).
- **Não usar** o `index.html` do Matheus para gravar: ele tem números à mão que não batem com o motor (diz "Recomendamos o Total" e incêndio de R$ 260 mil para o caso de Curitiba; o motor diz **Prático + RC adicional** e incêndio de **R$ 100 mil a R$ 203 mil**).
- Arquivo único HTML + `fichas_demo.js`, abre com dois cliques, sem servidor. Manter assim.
- Design: seguir [[Regras de design BB]] (amarelo BB, azul, cantos arredondados, linguagem simples).

## 3. De onde vêm os dados do app
`python motor/gerar.py --entrega` grava `prototipos/fichas_demo.js`:

```js
window.FICHAS_DEMO = {
  casos: { perfil_A_apto_urbano: "IMO_CASO_00005_01", perfil_B_casa_familiar: "IMO_CASO_00031_01",
           perfil_C_casa_lazer: "IMO_CASO_00010_01", nao_elegivel_seguro_existente: "IMO_CASO_00001_01",
           one_click_limpo: "...", inquilino_total: "IMO_CASO_00008_01", elegibilidade_a_confirmar: "IMO_CASO_00003_01" },
  fichas: { "<imovel_id>": { ...ficha..., sinais: {parcela, aluguel, vidracaria, obra} } }
}
```

### Contrato da ficha (campos que o app deve usar)
| Campo | Exemplo (caso A, Curitiba) | Onde usar no app |
|---|---|---|
| `local`, `complemento` | "Curitiba/PR", "BLOCO B APTO 305" | Cabeçalho, tela "Sua casa" |
| `campos.{tipo,vinculo,uso,area,bens}.valor` | APARTAMENTO, FINANCIADO, RESIDENCIAL_HABITUAL, 110, 41052 | Tela "Sua casa" |
| `campos.X.natureza` | OBSERVADO / ESTIMADO / INFERIDO / CONFIRMADO | Selo de cada dado (✓ observado, ≈ estimado) |
| `campos.X.fonte` | "parcela de financiamento de R$ 950/mês" | Texto "de onde veio" e raio-X |
| `campos.X.classe` | OBSERVADO / ESTIMADO / PRESUMIDO | Raio-X (base da confiança) |
| `campos.area.min/max`, `campos.bens.min/max` | 110–110; 22.190–59.914 | Faixas na tela e no raio-X |
| `elegibilidade` | SIM / NAO | Desvio para a tela de não elegível |
| `pendencias[]` | {codigo, texto, pergunta} | Perguntas de elegibilidade, aviso ao gerente |
| `avisos[]` | "imóvel de veraneio: roubo não cobre…" | Alerta na tela do plano |
| `plano` | PRATICO | Plano recomendado |
| `motivos_plano[]` | [{codigo: VIDROS, texto: "há gastos recentes de R$ 11.000 com vidraçaria"}] | "Recomendamos porque…" |
| `motivos[]`, `pontos` | todos os sinais e a soma | Raio-X ("como o plano foi escolhido") |
| `por_que_nao_abaixo` | "o Essencial não cobre roubo…" | "Se você escolher menos…" (slide 23) |
| `por_que_nao_acima` | "o Total acrescenta…, mas os sinais ainda são fracos" | "Por que não o mais caro" |
| `alternativa` | {plano: TOTAL, texto} | Comparação entre planos |
| `adicionais[]` | [{cobertura: RESPONSABILIDADE_CIVIL_FAMILIAR, motivo}] | Cobertura adicional ligada no ajuste |
| `coberturas[]` | {cobertura, tipo FIXA/ADICIONAL, min, max, confianca, regra, justificativa, confirmar, observacao} | "O que cobre", "Ajustar", raio-X |
| `perguntas[]` | {texto, codigo, prioridade, reduz_faixa_ate} | Até 3 perguntas; mostrar "esta resposta pode apertar sua faixa em até R$ X" |
| `confianca`, `confianca_motivo`, `confianca_score` | ALTA, "todos os dados críticos observados", 76 | Selo de confiança + raio-X |
| `completude` | {faltantes: [...], pct} | Raio-X |
| `canal` | ONE_CLICK / GERENTE | 1 toque ou "fale com o gerente" |
| `valor_imovel` | reconstrução 214–358 mil, segundo_risco true, fator_padrao [0.85, 1.3] | Raio-X ("como calculamos") |
| `fontes[]` | SINAPI, CUB, IPCA, CG… | Rodapé do raio-X |

**Regra de ouro do app:** nunca mostrar estimativa como fato. Todo valor estimado leva "≈" ou "faixa" e a origem.

## 4. O que construir (em ordem de prioridade)

### P1. Números 100% do motor (obrigatório)
- [ ] Ao trocar de caso, todas as telas leem a ficha: plano, motivos, coberturas, faixas, perguntas, confiança e canal.
- [ ] Tela "Seu plano": título "Recomendamos o {plano}" + `motivos_plano` + bloco "Se você escolher menos: {por_que_nao_abaixo}, e essas necessidades ficarão descobertas" + "Por que não o mais caro: {por_que_nao_acima}".
- [ ] Coberturas mostram **faixa** (mín–máx), não só o meio. O slider de ajuste começa no meio e fica preso entre mín e máx do produto.
- [ ] Cobertura adicional (`tipo: ADICIONAL`) aparece ligada no ajuste, com a etiqueta "adicional" e o motivo.
- [ ] Perguntas: só as de `perguntas[]`, na ordem. Mostrar `reduz_faixa_ate` como "Responder isso pode deixar sua faixa até R$ X mais precisa".
- [ ] Selo de confiança na tela "Sua casa" com o texto do `confianca_motivo` em linguagem simples.
- [ ] Conferir: o caso A tem de mostrar **Prático + RC adicional**, incêndio **R$ 100.000 a R$ 203.000**.
- [ ] Preço: o protótipo calcula preço com `BASE = 18.34` e `PACOTE = 6` (valores tirados de prints do app atual). Rotular como "preço ilustrativo" no raio-X. O motor não calcula prêmio.

### P2. Botões A / B / C
- [ ] Já existem botões na tela inicial do protótipo (lidos de `FICHAS_DEMO.casos`). Rótulos atuais: "A · Apto urbano", "B · Casa familiar", "C · Imóvel de lazer", "Já segurado", "1 toque", "Inquilino · Total", "A confirmar".
- [ ] Deixar A, B e C em destaque (são os perfis do slide 14) e os outros num "mais casos".
- [ ] Ao trocar, voltar para a tela "Sua casa" e animar a mudança de plano.
- [ ] O que cada perfil deve mostrar:

| Perfil | Caso | Plano | Mensagem principal |
|---|---|---|---|
| A · Apartamento urbano | IMO_CASO_00005_01 (Curitiba) | Prático + RC adicional | Gasto com vidraçaria e vizinhos; crianças ou pets → RC. Confiança ALTA, 1 toque |
| B · Casa familiar | IMO_CASO_00031_01 | Total | Casa em condomínio, crianças e pets, bens e eletrônicos altos. Confiança MÉDIA |
| C · Imóvel de lazer | IMO_CASO_00010_01 | Essencial + RC | Apartamento de veraneio: o roubo não cobre residência desocupada. Confiança BAIXA → gerente |
| Já segurado | IMO_CASO_00001_01 | — | Não elegível: endereço já tem seguro BB |

### P3. Modo raio-X (para a banca)
- [ ] Botão discreto no canto (ícone de olho ou "raio-X"), com atalho de teclado (ex.: tecla `X`).
- [ ] Ligado, **a mesma tela** ganha uma camada lateral ou sobreposta, sem trocar de tela, mostrando:
  - **Dados:** cada campo com valor, natureza, classe, fonte e idade do dado;
  - **Plano:** a tabela de pontos (`motivos` com peso, `pontos.pratico`, `pontos.total`) e a regra "Total ≥ 2; Prático ≥ 2 ou 1 + 1";
  - **Faixas:** para cada cobertura, `regra` e `dados_utilizados` (ex.: "área 110 m² × R$ 1.944–3.253/m² × 25%–40% + bens");
  - **Confiança:** nível, motivo, as 3 classes dos 5 dados e a regra (BAIXA / ALTA / MÉDIA);
  - **Perguntas:** por que cada uma foi escolhida (`reduz_faixa_ate`);
  - **O que NÃO foi usado:** "idade: não usada (teste de justiça = 0 casos); renda: só reforça os bens de quem não tem compras (`campos.bens.usou_renda`)";
  - **Fontes:** `fontes[]`.
- [ ] Frase no topo do raio-X: "Isso é o que o banco vê. O cliente vê só a versão simples."
- [ ] Desligado por padrão.

### P4. Tela do gerente (já existe: `id: "gerente"`)
- [ ] Usar a ficha: origem de cada dado, `pendencias`, `perguntas`, `confianca_motivo`, `alternativa`, onde o cliente parou.
- [ ] Bloco "O que o motor sugere revisar": dados ESTIMADO/PRESUMIDO e pendências de elegibilidade.
- [ ] Roteiro de conversa gerado a partir de `motivos_plano` e `por_que_nao_abaixo`.
- [ ] Mostrar que **o gerente não muda a regra**, só confirma dados; a proposta ajustada volta para o cliente decidir (telas `retorno` e `ajustada`, que já existem).

### P5. Tela de não elegível
- [ ] Quando `elegibilidade === "NAO"`: tela própria, sem botão de contratar. Texto: "Este endereço já tem seguro residencial da BB Seguros. Não é possível fazer outra proposta para o mesmo endereço." + "Quer revisar seu seguro atual com o gerente?".
- [ ] Mostrar a recomendação só como "referência para revisar a apólice atual".

### P6. Detalhes que valem ponto
- [ ] Botão "Ajuda" em todas as telas (já existe), modo simples e leitura em voz (já existem). Manter.
- [ ] Para `canal === "GERENTE"`, o botão principal vira "Falar com meu gerente" em vez de "Contratar em 1 toque".
- [ ] Casa de veraneio (`avisos`): alerta claro sobre roubo em residência desocupada.

## 5. Critérios de pronto
- [ ] Abre com dois cliques (`indexprototipo_gerente.html`), sem erro no console.
- [ ] Os perfis A, B e C mostram plano, faixas e motivo **iguais** à planilha `entrega/template_resultado_times.csv` e `template_coberturas_times.csv`.
- [ ] O raio-X liga e desliga em qualquer tela.
- [ ] O caso "Já segurado" não deixa contratar.
- [ ] Testado em largura de celular (375 px) e desktop.
- [ ] `python -m pytest -q` continua com 49 testes passando (se mexer no motor).
- [ ] Commit no nome do Matheus, sem menção a IA, mensagem no padrão `feat:` / `fix:` / `docs:`.

## 6. Como conferir rápido
```bash
cd C:\Users\maxom\Documents\datathon-protecao-inteligente
.venv\Scripts\python -m pytest -q
.venv\Scripts\python motor\gerar.py --entrega
```
Depois abrir `prototipos/indexprototipo_gerente.html` no navegador. Para testar com as ferramentas do navegador, servir a pasta: `.venv\Scripts\python -m http.server 8765 --bind 127.0.0.1` dentro de `prototipos/`.

## 7. Uso no vídeo (5 min)
| Tempo | Bloco | Tela |
|---|---|---|
| 0:00–0:30 | Problema (17% dos lares com seguro, slide 6) | Aviso |
| 0:30–1:00 | Ideia: sinais → sugestão → confiança → confirmação → recomendação | Desenho simples |
| 1:00–2:30 | Demo: perfil A do início ao fim (1 toque); troca para B e C | App + botões A/B/C |
| 2:30–3:00 | Ligar o raio-X: "isso é o que o banco vê" | Raio-X |
| 3:00–3:30 | Gerente recebe o caso C (confiança baixa) | Painel do gerente |
| 3:30–4:20 | Código: `pytest` (49 passando), `gerar.py`, `parametros.py`; métricas do README | Terminal + README |
| 4:20–5:00 | Responsabilidade, limitações, próximos passos | Slide |

Dizer no vídeo: "protótipo de como ficaria no app do BB; os números vêm do motor".

## 8. O que não fazer
- Não escrever números à mão no app.
- Não usar idade em nada (nem no texto). Renda só como o motor usa (reforço dos bens sem compras, avisado ao cliente); nunca mostrar o valor da renda na tela do gerente.
- Não chamar o protótipo de app oficial do BB.
- Não colocar link em mensagem de WhatsApp (padrão de golpe; o protótipo já trata isso).
- Não refazer o motor: mudanças nele exigem rodar testes, regerar planilhas e atualizar o PR.

Relacionado: [[Jornada dentro do app - ideias v3]], [[App atual - falhas e nosso fluxo]], [[Jornada do gerente]], [[Grau de confiança]], [[Guia da equipe - dados e pitch]], [[Correções P1-P5 no motor]].
