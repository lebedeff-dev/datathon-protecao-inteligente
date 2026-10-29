---
tags: [app, ilustracoes, design, prompt, datathon-bb]
data: 2026-10-29
status: enviado ao time para gerar
arquivo: app-expo/assets/ilustracoes/PROMPT_ChatGPT.md
---
# 🎨 Prompt das ilustrações (ChatGPT)

As ilustrações em SVG feitas no código funcionam, mas o time vai trocá-las por imagens geradas no ChatGPT, com mais acabamento. O prompt completo está em **`app-expo/assets/ilustracoes/PROMPT_ChatGPT.md`**: é só copiar e colar.

## O que tem no arquivo
1. **Passo a passo em português**: um chat só para todas as imagens; anexar a referência BB Digital Week; prompt mestre primeiro; uma imagem por mensagem; como pedir correção.
2. **Prompt mestre em inglês** (o modelo segue com mais precisão), com a **bíblia de estilo**:
   - **Tom (regras de negócio):** informar, nunca assustar ("o aviso justifica com fatos, não é isca"). Ninguém ferido, nenhum ladrão, nenhum dinheiro, nenhum texto ou logo.
   - **Estilo:** vetor chapado, personagens com braços e pernas alongados, contorno azul-marinho uniforme, sem degradê, sem 3D e sem sombra.
   - **Paleta com hex exato** e proporção 60/30/10. **Sem verde**, porque o app é só azul: plantas em turquesa.
   - **Tela:** PNG com **fundo transparente** (o app desenha o fundo em blocos), margem segura de 8% e faixa central de 1400 × 800.
   - **Teste da miniatura:** a cena tem que ler bem a 220 px de largura, que é o tamanho real no celular.
   - **Elenco fixo:** Bia (cliente), Davi, Seu Jorge (vizinho), Ricardo (gerente), com pele, cabelo e roupa definidos.
   - **Autochecagem antes de mostrar cada imagem**, com regra de refazer se algo falhar.
3. **17 pedidos de imagem**, cada um com o nome do arquivo e o tamanho: 00 folha de personagens (trava a consistência), 01 herói da entrada, 02 a 13 as situações do Passo 2 (vizinho e vendaval em versão apê e casa), 14 casa protegida, 15 Ricardo, 16 portal do gerente.
4. **Checklist de aprovação** e frases de correção que funcionam.

## Skills aplicadas dentro do prompt
- **imagegen-frontend-mobile:** bíblia de estilo travada antes de gerar, consistência entre imagens, paleta controlada, nada genérico ("AI tells" proibidos), legibilidade em tamanho real, refazer o que ficar fraco em vez de aceitar.
- **impeccable / better-ui:** um ponto focal por imagem, formas grandes, sem enfeite sem função, contorno de espessura única.
- **Regras de design BB** (vault, 13 - Design): azuis do BB, amarelo de destaque, turquesa e coral só em ilustração.
- **Regras do produto:** idade e renda não aparecem, nenhum medo como gatilho, diversidade, casas brasileiras reais (muro e portão, porcelanato, ventilador de teto).

## Como as imagens entram no app
- Salvar os PNGs em `app-expo/assets/ilustracoes/` com o nome exato.
- Descomentar a linha da imagem em `app-expo/src/ui/imagens.ts`.
- Enquanto a imagem não existe, o app mostra o SVG atual (`Ilustracao`, `HeroiCasa` e `CasaProtegida` em `ilustracoes.tsx` escolhem sozinhos). O fundo em blocos diagonais continua em código, por baixo da imagem transparente.

Ligações: [[App Expo - app de verdade no celular]] · [[Portal do gerente]] · [[Regras de design BB]]
