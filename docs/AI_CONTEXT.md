# Contexto para agentes de IA

## Fonte dos requisitos

Leia integralmente [PROJECT_BRIEF.md](PROJECT_BRIEF.md) antes de trabalhar. Esse documento preserva o texto fornecido pelo jogador e define o escopo, as fases, os critérios de qualidade e os testes desejados.

## Estado verificado

- O repositório começou apenas com um README contendo o nome do projeto.
- Esta entrega adiciona documentação; não implementa funcionalidades do mod.
- Fase 0 em andamento: Smart Government estudado no commit `95b20870816b9ceabcaf0b7b9371a66c85dd8bf1`; 26 testes de regressão passaram.
- Leia [RESEARCH.md](RESEARCH.md) para evidências, arquitetura proposta e capacidades pendentes.
- Leia [COMPATIBILITY.md](COMPATIBILITY.md), [MANUAL_RUNTIME_TEST.md](MANUAL_RUNTIME_TEST.md) e [LOCAL_CODEX.md](LOCAL_CODEX.md) para continuar no CachyOS.
- Instalação do jogo, versão efetiva, saves e arquivos dos mods ainda não foram inspecionados.
- Compatibilidade, métricas acessíveis, efeitos de script e automação não foram comprovados.
- Não há testes automatizados, build ou testes dentro do jogo disponíveis neste repositório.

## Próxima etapa: Fase 0

1. Retomar os resultados do estudo do Smart Government em `RESEARCH.md`; não repetir a pesquisa já registrada sem necessidade.
2. Identificar os caminhos reais da instalação Linux do jogo, saves e mods. Não presumir caminhos padrão, Steam ou necessidade de Wine.
3. Examinar Economy Advisor e os demais mods mencionados, com base nos arquivos reais.
4. Mapear dados e ações como executáveis, observáveis, parciais ou não suportados, registrando evidências e limitações.
5. Completar `docs/RESEARCH.md` e `docs/COMPATIBILITY.md` com os arquivos reais; ambos já contêm pesquisa parcial.
6. Apresentar as conclusões antes de iniciar a implementação.

Se os arquivos necessários não estiverem disponíveis, registrar a pesquisa parcial e o bloqueio; não declarar a fase concluída.

## Regras essenciais

- Usar identificadores próprios com prefixo `sed_`; preservar a independência do Smart Government (`sg_`).
- Não inventar APIs, métricas, efeitos, integrações ou resultados de testes.
- Evitar disputa da fila de construção e dos métodos de produção com outros mods.
- Preservar o controle do jogador sobre guerras e decisões políticas e diplomáticas importantes.
- Trabalhar em fases pequenas e atualizar este contexto e o registro de fases com evidências.
- Antes de cada fase, explicar objetivo, plano, arquivos previstos e riscos; depois, registrar resultados, testes e pendências.
- Não publicar saves, arquivos proprietários do jogo, credenciais ou dados pessoais no GitHub.

## Ambiente de desenvolvimento

Usar o checkout existente na tarefa em nuvem; não criar worktrees sem pedido explícito do jogador. Nesta etapa documental, não há dependências adicionais ou serviços a iniciar.
