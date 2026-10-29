# Protótipo v2: Seguro Residencial BB (fluxo enxuto + jornada do gerente)

Especificação para recriar e evoluir o protótipo clicável do time no Datathon Proteção Inteligente (Banco do Brasil). Versão 2, 28/10/2026. Evolui a versão 1 (`ESPECIFICACAO_PROTOTIPO.md` / `indexprototipo.html`).

> **Para quem vai continuar o trabalho:** este documento traz o que mudou da v1 para a v2 e tudo o que é preciso para refazer a v2: objetivo, regras de densidade, telas, painéis opcionais, jornada do gerente, design, lógica de preço e checklist de aceite. O arquivo de referência é `indexprototipo_v2.html` (um arquivo só, HTML + CSS + JavaScript, sem build). A v1 continua na pasta para comparação de "antes e depois".

---

## Sumário
1. [O que mudou da v1 para a v2](#1-o-que-mudou-da-v1-para-a-v2)
2. [Regras que o protótipo não pode quebrar](#2-regras-que-o-protótipo-não-pode-quebrar)
3. [Regras de densidade](#3-regras-de-densidade)
4. [Medição antes e depois](#4-medição-antes-e-depois)
5. [Caso usado na demonstração](#5-caso-usado-na-demonstração)
6. [Stack e estrutura](#6-stack-e-estrutura)
7. [Design](#7-design)
8. [Produto e lógica de preço](#8-produto-e-lógica-de-preço)
9. [Telas, uma por uma](#9-telas-uma-por-uma)
10. [Painéis opcionais](#10-painéis-opcionais)
11. [Jornada do gerente](#11-jornada-do-gerente)
12. [Elementos fixos e acessibilidade](#12-elementos-fixos-e-acessibilidade)
13. [Painel lateral de apresentação](#13-painel-lateral-de-apresentação)
14. [O que é ilustrativo](#14-o-que-é-ilustrativo)
15. [Checklist de aceite](#15-checklist-de-aceite)
16. [Como pedir para o assistente recriar](#16-como-pedir-para-o-assistente-recriar)
17. [Pendências para o time decidir](#17-pendências-para-o-time-decidir)

---

## 1. O que mudou da v1 para a v2
**Objetivo da v2:** diminuir o fluxo e a carga cognitiva sem perder nada da v1 e sem deixar nenhuma página densa.

**Princípio:** um caminho curto para todos; profundidade só para quem pedir. Nada foi apagado: o que não é essencial para decidir virou um **painel opcional** que sobe de baixo, com um assunto por painel.

| v1 (caminho obrigatório) | v2 |
|---|---|
| 1. E se acontecer? · 2. Sua casa · 3. Seu plano | **Tela A · Sua proteção** (passo 1 de 2) |
| 4. O que cobre · 5. Ajustar · 6. Conferir e contratar | **Tela B · Confira e contrate** (passo 2 de 2) |
| 7. Meu seguro | **Pronto** |
| Cenários, dados com origem, outros planos, cômodos, ajuste de valores, vigência | **Painéis opcionais** abertos por link |
| Gerente: tela "Pedir ajuda" + tela "Gerente avisado" | **Um painel** dentro de Ajuda, com confirmação no mesmo lugar |
| Gerente: tela "Proposta ajustada" | **Faixa no topo da Tela B** ("Ricardo mudou 2 coisas · Ver") |
| Painel do gerente com tudo aberto | Resumo no topo; "Dados e origem" e "Objeções" recolhidos |
| Emojis como ícones (assistências, sino) | Ícones SVG de traço único |
| Alertas do navegador quando falta responder | Botão principal desabilitado até poder avançar |

## 2. Regras que o protótipo não pode quebrar
Herdadas da v1 (tiradas do guia oficial). Continuam valendo em todas as telas.

| Código | Regra |
|---|---|
| RN-07 | Idade e atributos pessoais nunca decidem risco, plano, valor ou canal. Renda liberada na mentoria do BB (28/10) só como reforço combinado (D-08). |
| RN-09 | Estimativa nunca aparece como fato. Todo dado mostra a origem: observado, estimado ou confirmado. |
| RN-12 | O fluxo funciona sem dado externo. Dado externo só enriquece o texto, com fonte e data. |
| RN-15 a RN-19 | Elegibilidade antes de contratar. Falta de dado vira pergunta, não recusa. |
| RN-21 a RN-24 | As coberturas fixas não saem (só muda o valor). Adicionais do Prático e do Total podem entrar ou sair. |
| RN-26 | Vigência de 1 a 5 anos. |
| RN-34, RN-37 | Recomendação explicável, revisável, com confirmação humana e alternativas. |
| RN-36 | Poucas perguntas, objetivas, de preferência sim/não. |

**Regras do time:** tudo acontece dentro do app do BB; WhatsApp só como aviso, **sem link e sem dados da proposta**. O gerente ajusta a proposta, mas **quem contrata é sempre o cliente**.

## 3. Regras de densidade
Valem para todas as telas do celular. Quem mexer no protótipo deve conferir estas regras antes de entregar.

- **1 título** de até 6 palavras e no máximo **1 frase de apoio**.
- **1 ação principal** (botão amarelo) e no máximo **2 links secundários**.
- No máximo **3 blocos** e **3 números** por tela. Nunca card dentro de card.
- Cada painel opcional trata de **um assunto só**, com até 5 itens.
- O botão principal fica **desabilitado** (cinza) até o cliente poder avançar. Nada de `alert()`.
- Textos em segunda pessoa, sem jargão. Se a frase pode perder metade das palavras, ela perde.

## 4. Medição antes e depois
Medido nos protótipos com o mesmo script (palavras visíveis na área de conteúdo de cada tela).

| Métrica | v1 | v2 |
|---|---|---|
| Telas até contratar | 6 | **2** |
| Toques mínimos (do aviso ao "Contratar") | 9 | **6** |
| Palavras por tela no caminho principal (média) | 106 | **62** |
| Palavras na tela mais densa do caminho | 164 (Ajustar) | 63 (Confira e contrate) |

Os 6 toques da v2: aviso → "Sim, moro aqui" → "Continuar" → confirmação 1 → confirmação 2 → "Contratar". As duas confirmações foram mantidas separadas de propósito (a de elegibilidade tem peso legal).

## 5. Caso usado na demonstração
O mesmo da v1: **CASO_00005 / IMO_CASO_00005_01** da base de teste.

| Campo | Valor | Origem mostrada |
|---|---|---|
| Município | Curitiba (PR) | |
| Complemento | Bloco B, apto 305 | cadastro |
| Tipo | Apartamento | observado, "pelo endereço" |
| Área | 110 m² | observado, "cadastro do IPTU" |
| Relação | Seu, financiado (parcela R$ 950) | observado, "parcela no BB" |
| Dependentes | 1 | observado, "cadastro" (na v1 estava "estimado") |
| Bens | cerca de R$ 13.000 | estimado, "pelas compras" |
| Vidraçaria (24 meses) | R$ 11.000 | observado, usado no painel do gerente |
| Outro imóvel | sim, 1 cadastrado | observado, usado no painel do gerente |

**Plano recomendado: Total.** Motivo exibido: "Um vazamento no seu apê pode chegar ao vizinho de baixo. Só o Total paga esse conserto."

## 6. Stack e estrutura
- **Um arquivo só:** `indexprototipo_v2.html` com CSS e JavaScript puros. Abre com dois cliques ou por um servidor local.
- **Fontes:** Google Fonts, `Nunito` (títulos) e `Inter` (texto).
- **Layout da página:** fundo `#dfe3ec`; moldura de celular (390 × 820 px) à esquerda; painel de apresentação (380 px) à direita. Na tela do gerente, a moldura some e aparece um painel largo (940 px).
- **Estado:** objeto `st` em memória. Campos novos em relação à v1: `sheet` (painel aberto), `ajudaPasso`, `duvida`, `canal`, `origem`, `ger`, `antes`, `motivo`, `ajustado`.
- **Navegação:** `ir(n)` troca de tela e fecha painéis; `abrir(nome)` / `fechar()` controlam os painéis; `T(id)` devolve o índice de uma tela pelo id.
- **Painéis:** objeto `SHEETS` com uma função por painel. Cada função devolve o HTML do painel, começando pelo cabeçalho padrão `cab(titulo, subtitulo)` com botão de fechar.
- **Voz:** `speechSynthesis` em `pt-BR`. Se houver painel aberto, lê o painel; senão, lê a tela.

### Skills usadas (assistente de IA)
| Skill | Para quê |
|---|---|
| `impeccable` (modo distill) | Cortar o que não ajuda a decidir; regras de densidade; checagem de qualidade e detector de padrões ruins |
| `signup` | Reduzir atrito: menos campos, padrões já preenchidos, um passo por decisão, botão desabilitado em vez de erro |
| `cro` | Hierarquia: uma ação principal por tela, plano recomendado com motivo |

## 7. Design
Mantém a identidade da v1. Ajustes da v2:

| Token | v1 | v2 | Por quê |
|---|---|---|---|
| `--suave` | `#6C7077` | `#5E6269` | Mais contraste no texto de apoio (≥ 4,5:1) |
| `--verde` | `#0E8A4F` | `#0E7A46` | Mais contraste sobre o verde-claro |
| Sombra da moldura e do painel | azulada | neutra (`rgba(0,0,0,.22)`) | O detector apontou sombra colorida como padrão a evitar |

- **Novos elementos:** `.sheet` (painel que sobe, com alça e botão de fechar), `.link` (link sublinhado azul-escuro), `.linha-ed` (linha tocável com valor e seta), `.faixa` (aviso do gerente no topo da Tela B), `.mini` (chips pequenos), `.btn[disabled]`.
- **Ícones:** SVG de traço único (`ICO.ok`, `ICO.nao`, `ICO.seta`, `ICO.chat`, `ICO.fone`, `ICO.gerente`, `ICO.familia`, `ICO.sino`, `ICO.relogio`, `ICO.som`). Nenhum emoji.
- **Superfícies do navegador:** seleção de texto em amarelo, anel de foco azul de 3 px (`:focus-visible`), barra de rolagem fina.
- **Movimento:** o painel sobe com uma curva suave (0,28 s) e respeita `prefers-reduced-motion`.

## 8. Produto e lógica de preço
**Igual à v1** (seção 7 da especificação v1): mesmas coberturas, limites, franquias, planos, fórmula `BASE + pacotes × PACOTE + Σ taxa × valor / 1000` e descontos por vigência. Ajustes do motor já aplicados ao caso: incêndio R$ 260.000 e danos por água R$ 18.000.

Uso novo na v2: **o impacto de cada sugestão do gerente no preço** (`impacto(k) = (sugestão − valor atual) × taxa / 1000`), mostrado ao lado da sugestão. Exemplo: vidros para R$ 11.000 = +R$ 34,01/mês; roubo para R$ 13.000 = +R$ 35,00/mês.

## 9. Telas, uma por uma
Textos entre aspas são os usados no protótipo.

### Tela 1 · Aviso (tela de bloqueio)
- Notificação do app: **"Temporada de chuva em Curitiba"** / "O seguro do condomínio não cobre o que tem dentro do seu apê. Veja em 1 minuto."
- WhatsApp (só aviso): "Sua proteção está pronta no app do BB, em Seguros. *O BB nunca pede senha por aqui.*" Sem link, sem valores.
- Tocar em qualquer aviso abre a Tela A.

### Tela A · Sua proteção (passo 1 de 2)
- Título: "Sua proteção está *pronta*"
- Apoio: "Apartamento em Curitiba, 110 m²." + link **O que usamos** (painel `dados`).
- **Bloco do plano** (borda azul e selo "Recomendado para você" quando o plano é o recomendado): nome, preço/mês, o motivo em uma frase e **um** exemplo em reais numa linha: "Se o apê alagar: você paga **R$ 1.780** em vez de ~~R$ 17.800~~." Links: **Outros planos** (painel `planos`) e **Outras situações** (painel `cenarios`).
- **Bloco da confirmação:** "Você mora neste apartamento?" com dois botões grandes ("Sim, moro aqui" / "Não"). Depois de responder: "✓ Proposta confirmada".
- Botão: **CONTINUAR COM O [PLANO]**, desabilitado até a resposta.

### Tela B · Confira e contrate (passo 2 de 2)
- Se o gerente ajustou a proposta: faixa no topo "Ricardo mudou 2 coisas" + link **Ver** (painel `mudou`).
- Título: "Confira e *contrate*"
- **Bloco do resumo:** "Plano [nome]" + preço final/mês; 2 linhas do que cobre e 1 do que não cobre (por plano); links **Ver por cômodo** (painel `cobre`) e **Ajustar valores** (painel `ajustar`); linhas tocáveis **Vigência · 1 ano ›** (painel `vigencia`) e **Pagamento · Débito em conta ›** (painel `pagamento`).
- **Duas confirmações separadas:** "Entendi que o [plano] não cobre [X]." e "O imóvel não está em obra e é de alvenaria."
- Apoio: "Você pode desistir em até 7 dias pelo app."
- Botão: **CONTRATAR POR R$ X/MÊS**, desabilitado até as duas confirmações.

| Plano | Cobre (2 linhas) | Não cobre |
|---|---|---|
| Essencial | Fogo, água e raio · Assistência 24h (encanador, chaveiro) | roubo nem o conserto do vizinho |
| Prático | Fogo, água e raio · Roubo com arrombamento e vidros | o conserto do vizinho |
| Total | Fogo, água, raio e roubo · O conserto do vizinho | desgaste natural nem obra |

### Tela · Pronto (Meu seguro)
- "Sua casa está *protegida*", card azul com plano, endereço e preço, um pedido de assistência em andamento ("Encanador a caminho · chega em cerca de 40 min"), links **O que cobre** e **Avisar sinistro**, botão "Recomeçar a demonstração".

### Tela · Aviso do gerente (tela de bloqueio)
- "**Ricardo atualizou sua proposta**" / "Toque para conferir. Nada foi contratado." Abre a Tela B com a faixa do gerente.

## 10. Painéis opcionais
Todos sobem de baixo, têm alça, título, botão de fechar e um assunto só. Tocar fora fecha.

| Painel | Aberto por | Conteúdo |
|---|---|---|
| `dados` | "O que usamos" (Tela A) | 5 dados com chip de origem e a barra de confiança (72% antes da confirmação, 94% depois) |
| `planos` | "Outros planos" | Os 3 planos em lista vertical, com preço e uma linha do que muda. Tocar troca o plano e fecha |
| `cenarios` | "Outras situações" | Os 4 cenários da v1 (alagou, raio, vizinho, arrombamento) com desenho e "Sem seguro × Com o plano" |
| `cobre` | "Ver por cômodo" | 6 cômodos em grade 3 × 2; situações com "Coberto" / "Não coberto" e franquia; assistências do plano em uma linha |
| `ajustar` | "Ajustar valores" | Barra de preço fixa no topo, barras deslizantes e chaves da v1, avisos de equivalência (Prático = Essencial; Total = Prático) |
| `vigencia` | linha "Vigência" | 1 a 5 anos com desconto e economia em reais |
| `pagamento` | linha "Pagamento" | Débito em conta ou cartão |
| `mudou` | faixa do gerente | Motivo escrito pelo gerente, antes → depois de cada valor e do preço, "Nada foi contratado. Só você decide." |
| `ajuda` | botão Ajuda (todas as telas) | Ver seção 11 |

## 11. Jornada do gerente
**Ideia:** o cliente pede ajuda sem sair do app e sem repetir nada; o gerente recebe a proposta pronta, ajusta e devolve; o cliente confere e contrata com um toque.

**No celular (painel `ajuda`):**
1. **Menu:** "Falar com meu gerente", "Conversar agora" (especialista), "Me liguem", "Alguém de confiança".
2. **Falar com o Ricardo:** "Sobre o que é a dúvida?" (O valor · O que cobre · Se meu imóvel pode · Outra coisa) e "Como prefere falar?" (Aqui no app, já marcado · Ligação · WhatsApp). Botão **ENVIAR PARA O RICARDO**, desabilitado até escolher a dúvida. Abaixo: "Ele vê esta proposta. Seus extratos e sua renda, não."
3. **Recebeu (no mesmo painel):** "Proposta enviada · Protocolo BB-8K2" e "Resposta em até 15 min · Se ele estiver ocupado, a Juliana assume." Se o canal for WhatsApp: "No WhatsApp chega só o protocolo, sem link e sem dados." Botão de demonstração **Ver o lado do gerente**.

**No painel do gerente (tela larga):**
- **Topo:** selo "Pedido de ajuda · há 2 min · BB-8K2 · [canal]", título "Dúvida sobre *[dúvida]*" e uma linha de resumo com a tela de onde veio o pedido.
- **Coluna da proposta:** troca de plano, barras de vidros e roubo com chip "sugestão R$ X" / "sugestão aplicada", **novo preço ao vivo**, campo "Motivo que o cliente vai ler" (já preenchido), botões **Ligar para o cliente** e **Enviar ao app do cliente**.
- **Coluna do motor:** "O motor sugere" (vidros: R$ 11.000 em vidraçaria em 24 meses; roubo: bens ≈ R$ 13.000; outro imóvel cadastrado), cada sugestão com o impacto no preço, e o botão **Aplicar sugestões**; "Roteiro" com 3 perguntas.
- **Recolhidos:** "Dados e origem" (tabela com chips) e "Objeções prováveis" (está caro → Prático ajustado; condomínio já cobre → cobre o prédio; seguro do financiamento → protege imóvel e dívida).
- **Privacidade:** "Você vê um resumo, não o extrato. A renda não aparece e só ajuda a estimar os bens de quem não tem compras; a idade não decide nada. Acesso registrado no protocolo BB-8K2."

**Volta para o cliente:** aviso na tela de bloqueio → Tela B com a faixa "Ricardo mudou 2 coisas" → painel `mudou` → contrata com as duas confirmações.

## 12. Elementos fixos e acessibilidade
- **Ajuda** no rodapé de todas as telas do celular, ao lado do botão principal.
- **Aa** (modo simples, tudo ~25% maior) e **Ouvir** (leitura em voz alta) no canto superior direito.
- **Seta de voltar:** Tela B → Tela A → Aviso.
- Botões com no mínimo 50 px de altura; uma decisão por tela; perguntas de sim/não com botões grandes.
- Anel de foco visível em tudo que é tocável; controles com `aria-label`; painéis com `role="dialog"`.
- Modo simples oferecido pelo comportamento digital, nunca pela idade (RN-07).

## 13. Painel lateral de apresentação
Para cada tela: título, **3 métricas fixas** (6 → 2 telas · 9 → 6 toques · 106 → 62 palavras por tela), caixa vermelha **"Antes:"** (o problema na v1 ou no app atual), caixa verde **"Agora:"** (a solução na v2), nota sobre o caso e botões para pular para qualquer tela (1 a 6).

## 14. O que é ilustrativo
- **Preços:** fórmula própria calibrada nas prints do app. Não é a tabela oficial.
- **Prejuízos dos cenários**, nomes (Ricardo, Juliana, Carlos), protocolo, prazos de resposta e a conversa do chat.
- **"Temporada de chuva em Curitiba"** precisa de fonte oficial (INMET ou Defesa Civil) antes do vídeo.
- **Sugestões do motor** (vidros R$ 11.000, roubo R$ 13.000) estão escritas no código; quando o motor existir, devem vir do JSON do cliente-imóvel.
- **Visual do BB:** cores e estilo, sem logo.

## 15. Checklist de aceite
- [ ] Abre sem instalar nada; o console do navegador não mostra erros.
- [ ] Caminho principal: Aviso → Tela A → Tela B → Pronto, com 6 toques no mínimo.
- [ ] Nenhuma tela do caminho principal passa de ~65 palavras, 3 blocos e 1 botão principal.
- [ ] Botões principais ficam desabilitados até poder avançar (sem `alert()`).
- [ ] Todos os 9 painéis abrem, fecham pelo X e por toque fora, e tratam de um assunto só.
- [ ] Trocar o plano no painel `planos` atualiza a Tela A, a Tela B e os cenários.
- [ ] O painel `ajustar` muda o preço na hora e mostra os avisos de equivalência.
- [ ] As duas confirmações da Tela B continuam separadas.
- [ ] Ajuda → gerente → enviar → painel do gerente mostra a dúvida, o canal e a tela de origem certos.
- [ ] "Aplicar sugestões" + "Enviar ao app" levam ao aviso de retorno e à faixa "Ricardo mudou 2 coisas" na Tela B.
- [ ] Nenhuma decisão usa idade; a renda só como o motor usa (bens sem compras, D-08); o WhatsApp nunca leva link nem dados.
- [ ] Aa aumenta tudo; Ouvir lê a tela ou o painel aberto.
- [ ] O detector da skill impeccable roda sem apontamentos (`impeccable detect --json indexprototipo_v2.html`).

## 16. Como pedir para o assistente recriar
Cole este documento inteiro (e, se quiser, também a especificação v1) e depois o pedido abaixo:

```
Use este documento como especificação. Recrie o protótipo como um único
index.html (HTML, CSS e JavaScript puros, sem framework), seguindo:
- as regras da seção 2 e as regras de densidade da seção 3;
- o design da seção 7 (tokens da v1 com os ajustes de contraste da v2,
  ícones SVG, nada de emoji);
- a lógica de preço da v1, mais o impacto das sugestões da seção 8;
- as telas da seção 9, os painéis da seção 10 e a jornada do gerente
  da seção 11, com os textos indicados;
- os elementos fixos da seção 12 e o painel lateral da seção 13.
Use as skills impeccable (distill), signup e frontend-design. Depois de
pronto, abra no navegador, percorra o caminho principal e a jornada do
gerente e confira o checklist da seção 15.
Mudanças que eu quero nesta versão: [descrever aqui].
```

## 17. Pendências para o time decidir
1. **Dados do caso que não batem com a base:** os bens aparecem como ~R$ 13.000, mas as compras de 36 meses somam R$ 20.750; a pergunta "Você mora neste apartamento?" já tem resposta na base (`endereco_principal_compativel = SIM`). Uma pergunta mais útil seria sobre os vidros ou sobre o segundo imóvel.
2. **Calibrar o preço de roubo e vidros:** com a fórmula atual, as sugestões do gerente levam o Total de R$ 126 para R$ 195/mês. Ou recalibrar as taxas, ou deixar claro no vídeo que o preço é ilustrativo.
3. **Incêndio de R$ 260 mil num apartamento:** a notificação diz que o condomínio cobre o prédio, mas o valor sugerido reconstrói a área inteira. Vale revisar para não parecer cobrança dupla.
4. **Pequenos reparos:** aparece no app, mas não no catálogo do datathon. Perguntar na mentoria.
5. **Cupom:** fora do fluxo. Se voltar, só na Tela B, como link.
