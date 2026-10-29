# 24 · Críticas em papel de banca: o que corrigimos

**Em uma frase:** uma revisão em papel de banca levantou 23 perguntas. Corrigimos as 6 que procediam e cabiam no código, decidimos a família no plano e escrevemos a resposta de todas no vault (`16 - Projeto por inteiro/08 - Perguntas da banca e respostas.md`).

**Onde estamos:** dia da entrega (29/10)

## O que mudou
| Crítica | Antes | Agora |
|---|---|---|
| NÃO por indício (RN-19) | 16 NÃO por "seguro residencial + produto de seguridade BB" | SIM + pergunta obrigatória "O seu seguro atual é da BB?"; NÃO só com prova |
| Família mudava o plano (RN-07) | 18 casos subiam para o Total | Nunca muda o plano; só pede a RC familiar (adicional ou pergunta) |
| Inquilino de casa com a estrutura | Incêndio = reconstrução + bens | Só os bens (a estrutura é do locador, Lei do Inquilinato, art. 22, VIII); entra se o contrato pedir |
| Vidros e RC genéricos | 12% e 37% de textos distintos | 88% e 96%, com a área e o tipo do imóvel; RC usa o vizinho do mesmo tamanho |
| STP inflado | 72,5% sobre os 138 | 1 toque puro 45,7% · sem pessoa 81,2% (sobre os elegíveis) |
| ITV circular | sugerido ÷ valor em risco = 1,00 por construção | sugerido ÷ cenário pessimista = 0,67 (15 casos ≥ 0,8) |
| Fontes | sinistros da matéria no mesmo nível das oficiais | Hierarquia de fontes no `FONTES.md`; a matéria virou só contexto |
| Reprodutibilidade | não dita | README explica: planilhas com os dados salvos; `--ao-vivo` muda de propósito |

**Números novos:** Prático 68 · Total 38 · Essencial 32 · elegível 138 (37 com confirmação, 16 "provável BB") · jornada: 1 toque 63 · app com perguntas 49 · gerente 26 (19%) · regra dos 80% = 1,00 · justiça = 0 · **105 testes**.

**Validação honesta da área:** na base de teste, nunca usada para calibrar, a faixa contém a área real em 73,9% (46 imóveis); na base de desenvolvimento, 80,9%.

**ANEEL pela API:** testado. A API CKAN só expõe os limites regulatórios; os valores apurados estão num zip de 30 MB. O ranking segue da página oficial do gov.br, e isso está registrado no `FONTES.md`.

**Achado ao rastrear um caso conta por conta:** a pergunta da RC para casas com família (prioridade 45) sumia atrás das perguntas de valor em 23 de 34 casos. Subiu para 59: agora 33 de 34 recebem a oferta. O rastro completo está em `16 - Projeto por inteiro/09 - Cada escolha conta por conta.md`.

## Ainda em aberto
- Quem não usa o app (16): gerente direto ou convite ao app antes.
- Limites reais de água e danos elétricos.
- Registro escrito da liberação da renda (nome do mentor e mensagem).
- Nome da equipe no README e vídeo.

## Frase para o pitch
> "Só dizemos não com prova. Na dúvida, o app pergunta. E a família do cliente nunca muda o plano: ela só pede a proteção a terceiros que faz sentido."
