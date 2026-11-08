# Smart Economy Director — Victoria 3 1.15

Projeto de um planejador econômico nacional para Victoria 3: diagnóstico,
estratégia de desenvolvimento e execução controlada de ações comprovadamente
suportadas pelo jogo. Prefixo reservado: `sed_`.

**Estado atual: Fase 0, pesquisa técnica inicial documentada. Ainda não há mod
instalável, Journal Entry ou automação implementada.** A instalação local 1.15.0
e os scripts dos mods foram inspecionados; os testes de campanha estão pendentes.

O Economy Advisor já executa construção e mudanças de métodos de produção.
O Director deve acrescentar estratégia nacional sem disputar essas automações.
Nenhuma integração direta com outros mods foi comprovada.

- [Requisitos originais completos](docs/PROJECT_BRIEF.md)
- [Pesquisa e limitações técnicas](docs/RESEARCH.md)
- [Arquitetura proposta](docs/ARCHITECTURE.md)
- [Compatibilidade](docs/COMPATIBILITY.md)
- [Contexto para continuidade](docs/AI_CONTEXT.md)
- [Registro de fases](docs/PHASE_LOG.md)
- [Procedimento de testes de campanha](docs/MANUAL_RUNTIME_TEST.md)
- [Inventário de evidências locais](docs/SOURCE_INVENTORY.json)

O desenvolvimento seguirá as fases do documento original. A próxima entrega é
concluir as verificações pendentes da pesquisa; depois, implementar apenas o
diagnóstico econômico, sem ações automáticas.

A [pesquisa anterior na nuvem](docs/RESEARCH_CLOUD.md) e as
[instruções de continuidade local](docs/LOCAL_CODEX.md) também foram preservadas.
