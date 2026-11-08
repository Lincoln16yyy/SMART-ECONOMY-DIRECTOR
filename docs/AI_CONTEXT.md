# Contexto para agentes de IA

## Fonte dos requisitos

Leia integralmente [PROJECT_BRIEF.md](PROJECT_BRIEF.md) antes de trabalhar. Esse documento preserva o texto fornecido pelo jogador e define o escopo, as fases, os critérios de qualidade e os testes desejados.

## Estado verificado

- O repositório começou apenas com um README contendo o nome do projeto.
- Esta entrega adiciona documentação; não implementa funcionalidades do mod.
- Fase 0 pendente: o Smart Government ainda não foi estudado nesta entrega.
- Instalação do jogo, versão efetiva, saves e arquivos dos mods ainda não foram inspecionados.
- Compatibilidade, métricas acessíveis, efeitos de script e automação não foram comprovados.
- Não há testes automatizados, build ou testes dentro do jogo disponíveis neste repositório.

## Próxima etapa: Fase 0

1. Estudar o repositório Smart Government e os documentos e sistemas listados na especificação.
2. Identificar os caminhos reais da instalação Linux do jogo, saves e mods. Não presumir caminhos padrão, Steam ou necessidade de Wine.
3. Examinar Economy Advisor e os demais mods mencionados, com base nos arquivos reais.
4. Mapear dados e ações como executáveis, observáveis, parciais ou não suportados, registrando evidências e limitações.
5. Produzir `docs/RESEARCH.md` com diagnóstico técnico e arquitetura proposta e documentar a compatibilidade.
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
