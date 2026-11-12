# Instruções para agentes — Smart Economy Director (Victoria 3)

Este arquivo é lido automaticamente no início de cada sessão. Siga-o antes de
qualquer outra coisa.

## Antes de tocar em qualquer arquivo
1. Leia `docs/agent/vic3-modding/SKILL.md` (fluxo completo de modding) e siga
   o "Ritual de início de sessão".
2. Leia `docs/agent/vic3-modding/references/ambiente-local.md`. Se faltar
   caminho ou comando, descubra uma vez e grave lá.
3. Leia só o **bloco de estado no topo** de `docs/AI_CONTEXT.md`.

## Regras que não se negociam
- **Nada de suposição.** Efeito, trigger, escopo ou ID novo só entra com
  evidência: arquivo do jogo base, documentação exportada (`script_docs`) ou
  `vic3-tiger`. Sem evidência = marque NÃO VERIFICADO e crie teste de engine.
- Duas hipóteses falhas seguidas ⇒ pare, colete evidência ou peça checagem
  ao usuário. Não gaste a sessão adivinhando.
- `common/`, `events/` e `gui/` são **gerados** por `tools/build_mod.py`.
  Edite o gerador e regenere; nunca edite o arquivo gerado.
- Teste sintético ≠ funciona no jogo. Use os rótulos de evidência do SKILL.md.
- Efeitos que alteram impostos, salários ou leis precisam de snapshot,
  restauração e teste de save/reload.
- Instalação no jogo: jogo fechado, com backup.
- Idioma: responda e documente em português.

## Antes de encerrar a sessão
Atualize o bloco de estado de `docs/AI_CONTEXT.md` (máx. ~40 linhas),
`docs/STATUS.md` e `references/ambiente-local.md`; depois faça o commit.
