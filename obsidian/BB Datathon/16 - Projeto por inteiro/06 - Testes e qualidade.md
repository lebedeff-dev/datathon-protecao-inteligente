---
tags: [projeto, testes, qa]
atualizado: 2026-10-28
---
# ✅ 06 · Testes e qualidade

**99 testes** (`python -m pytest -q`), que rodam sozinhos no GitHub a cada envio (`.github/workflows/testes.yml`: testes + geração das 138 planilhas). Nenhum teste usa a internet.

| Grupo | Arquivo | Testes | O que prova |
|---|---|---|---|
| T1 · Parâmetros e fontes | `test_motor.py` | 7 | Custo do m² com CUB oficial ou razão; IPCA; aluguel; a renda só em um parâmetro |
| T2 · Bens e área | `test_motor.py` | 15 | Bens pelas compras; sem compras, região (+ renda, presa em 2×); renda e idade não mexem em quem tem compras; tipo pelo complemento |
| T3 · Elegibilidade, plano e coberturas | `test_motor.py` | 32 | Obra e seguro existente viram pergunta; segundo risco; veraneio não puxa o Prático; padrão pelo IPTU; subseguro; RN-27; território e sinistros só no texto |
| T4 · Planilhas | `test_motor.py` | 4 | Planilhas válidas, 138 casos na ordem, o validador pega erros (inclusive RN-33) |
| T5 · Confiança, justiça e coerência | `test_motor.py` | 9 | Dado antigo pesa menos; justiça (renda e idade não mudam a ficha); área maior nunca reduz o incêndio; extremos; reprodutível byte a byte |
| T6 · Métricas | `test_motor.py` | 1 | Métricas e casos contrastantes saem |
| Motivo 2.0 | `test_motor.py` | 5 | Nenhum motivo genérico; sem jargão; até 130 palavras; valor em risco; coberturas personalizadas |
| F2 · Média da região | `test_motor.py` | 4 | Degraus (município e tipo → estado); CEP é ruído |
| F3 · Jornada | `test_motor.py` | 7 | Gerente só com obra ou sem app; confiança baixa pergunta no app; 1 toque sem pergunta obrigatória; "(opcional)" na planilha |
| P1 · Relatório de validação | `test_motor.py` | 5 | Faixa da área em ~80%; confiança por cobertura varia; valor sugerido dentro da faixa; pergunta do contrato ao inquilino |
| API | `test_api.py` | 6 | Ficha, 404, confirmar bens sobe a confiança, área inválida recusada, `/fontes` |
| Atualizador | `test_coletar.py` | 4 | API ao vivo grava; API fora do ar ou resposta incompleta mantém o salvo |

## Como fizemos QA
- **Teste antes do código** (TDD) em toda mudança: o teste falha, a mudança faz passar.
- **Revisão de código** a cada bloco grande (ver [[Auditoria do código - 28-10]]). A última achou 7 pontos, e 5 foram corrigidos (por exemplo, o atualizador apagava o CSV se a API respondesse pela metade).
- **Verificação antes de dizer "pronto":** testes, planilhas com 0 erros, métricas conferidas e duas gerações idênticas.
- **Relatório de validação** do Eduardo (`documentos/RELATORIO_VALIDACAO.md`): achados P0, P1 e P2; os P1 de código foram aplicados.

Próxima: [[07 - Regras, decisões e pendências]]
