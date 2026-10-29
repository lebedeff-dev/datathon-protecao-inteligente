# 22 · Renda liberada depois da mentoria do BB

**Em uma frase:** a renda deixou de ser tratada como dado sensível e passou a reforçar a estimativa dos bens de quem não tem compras, sempre junto com a média da região.

**Onde estamos:** pós-mentoria de 28/10 · branch `validacao/renda-liberada-e-relatorio` · relatório completo em [`../RELATORIO_VALIDACAO.md`](../RELATORIO_VALIDACAO.md)

## O que fizemos
- Revisamos a **RN-07**: na mentoria, o pessoal do Banco do Brasil disse que renda (salário) **não é dado sensível**. A LGPD (art. 5º, II) também não lista renda como sensível. A idade continua proibida como atalho.
- Registramos a decisão **D-08** nas regras do vault e trocamos os textos que diziam "renda nunca" (README, guia de pitch, especificações, protótipos).
- No motor, a renda entra **num ponto só**: `estimar_bens`, quando o imóvel não tem compras nem bens ligados. Compras estimadas = média geométrica entre a média da região e `renda × (compras ÷ renda do município)`.
- Novo teste fora da amostra (`backtest_bens_sem_compras`): na base de desenvolvimento, fingimos que quem tem compras não tem e estimamos.
- Quando a renda entra, o texto do cliente avisa: "usamos a média de casas parecidas na sua região e a sua renda".
- Parâmetro para desligar: `parametros.RENDA_NOS_BENS_SEM_COMPRAS`.

## Por que importa
- **Critério da banca:** uso inteligente dos dados (15%) e privacidade e responsabilidade (10%).
- **No pitch:** bloco "Dados" e bloco "Responsabilidade".

## O que você precisa entender
- **Por que média geométrica?** É a raiz do produto dos dois valores. Se um deles for muito alto ou muito baixo, o resultado fica no meio, então nenhum dos dois decide sozinho (RN-08).
- **Por que só para quem não tem compras?** A compra é o bem de verdade. A renda é uma pista. Quando há prova, a pista não precisa entrar.
- **Por que as planilhas não mudaram?** Na base comum (e na de desenvolvimento), todo imóvel tem compras ou bens ligados. O caminho novo existe para o cliente real que compra com cartão de outro banco.

## Decisões e o que descartamos
| Decidimos | Em vez de | Porque |
|---|---|---|
| Renda × região (média geométrica) | Só a renda | Só a renda erraria 37% e trataria igual quem ganha bem e mora com pouco |
| Renda × região | Só a região | Só a região erra 40,5%; com a renda, 22,7% |
| Renda só nos bens sem compras | Renda em plano, canal ou confiança | Não há ganho medido e seria o atalho que a banca procura |
| Renda fora da área | Usar a renda para estimar m² | Correlação de 0,01 com a área: não ajuda |
| Idade continua proibida | Liberar junto | A mentoria falou da renda; idade não diz nada do imóvel |

## Como conferir
```bash
python -m pytest -q          # 91 testes
python motor/gerar.py --entrega
```
Resultado esperado: 91 passando, 0 erros de validação, planilhas iguais às de antes e, em `entrega/metricas.json`, `dados_faltantes.backtest_bens_sem_compras` com 40,5 e 22,7.

## Pendências e riscos
- Revisão de código (28/10): a renda chegava ao plano pelos limiares de bens no caminho sem compras. Corrigido: bens presumidos não somam pontos ao plano, o texto diz "estimamos" e o resultado fica entre 0,5 × e 2 × a região (detalhes na seção 11 do relatório).
- O backtest só mede em quem tem compras (fingindo que não tem). Para quem realmente não compra pelo BB, 22,7% é otimista.
- O guia ainda diz "atributos pessoais". Na banca, dizer que a liberação veio da mentoria do BB e mostrar que a renda nunca decide sozinha.
- Próximo uso proposto (não implementado): em 29 dos 138 casos, a renda indica compras pelo menos 1,5 × maiores que as vistas no BB (8 casos acima de 2 ×). Isso pode virar a pergunta "comprou coisas para a casa em outros bancos?", sem mudar o valor sozinho.

## Frase para o pitch
> "Depois da mentoria passamos a usar a renda, mas só onde falta prova e sempre junto com outro sinal: para quem não tem compras, o erro cai de 40% para 23%."

## Próximo passo
- O time decide se a pergunta das compras fora do BB entra antes da entrega.
