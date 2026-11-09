# Smart Economy Director — Victoria 3 1.15

Versão de desenvolvimento **0.4.1 — modos Manual, Assistido e Automático com
controle de recomendações ignoradas**. O mod tem diário próprio, leituras manuais ou
mensais, recomendações limitadas de infraestrutura e capacidade de construção,
além de produtores locais para oito bens em escassez. Os três modos aparecem em
botões no topo do diário. Manual só diagnostica; Assistido mostra botões para
aprovar ações individuais; Automático revisa mensalmente e pode enfileirar no
máximo um nível quando as filas estão vazias, o país está fora de inadimplência
e não há uma das automações concorrentes detectadas ativa. Cada botão de ação
permanece visível no cartão e é revalidado no clique. Quando
não há candidato, o painel decompõe os estados por motivo principal; quando o
botão de aprovação está bloqueado, o painel indica a guarda que bloqueia a ação. O estado do Automático identifica fila ocupada, inadimplência, construção pausada, outro construtor conhecido ou ausência de candidato.
Saldo semanal negativo aparece como alerta, sem bloquear a aprovação. O modo
Automático pode agir apenas em ferrovias elegíveis e produtores existentes
para madeira, ferro, carvão, cereais, tecido, ferramentas, mantimentos e roupas
em escassez; não altera PMs nem leis. A 0.4.1 passou validação estática; modos,
botões e execução agendada ainda precisam de confirmação na campanha antes de
serem considerados validados na engine.

Cada cartão elegível permite ignorar apenas aquele tipo de expansão naquele estado.
A escolha bloqueia recomendações e execução nos três modos até usar
**Restaurar recomendações ignoradas**, no topo do diário. Desativar limpa essas
escolhas; ignorar ou restaurar não cancela nem enfileira obras.

O painel mostra finanças, PIB, população, padrão de vida, alfabetização,
capacidade de construção, filas e sinais de infraestrutura, abastecimento e
contratação. Os dados correspondem à última leitura indicada no painel.
O crescimento do PIB requer amostras em meses distintos.

**Estado: interface, indicadores, atualização sob solicitação, desativação e candidatos anteriores foram confirmados em campanha nas versões 0.3.0–0.3.5.** As capturas do Império Otomano em junho de 1839 confirmaram modo Automático visível e mensagem de revisão bloqueada por filas ocupadas. Inclusão automática, aprovação permitida e o novo detalhamento de oferta ainda precisam de confirmação na engine. Compatibilidade ampliada continua pendente; não é uma versão para deixar uma campanha sem supervisão.

## Instalação e uso

Consulte [instalação e geração do ZIP](docs/INSTALL.md). O pacote gerado em
`dist/smart-economy-director-0.4.1.zip` contém a pasta do mod e o descritor
externo. Ative no launcher e use a decisão **Ativar Smart Economy Director**.
O modo inicial é Assistido; a automação só começa se o jogador selecionar
Automático no diário.

## Desenvolvimento e verificação

```bash
python3 tools/build_mod.py
python3 tools/build_mod.py --check
python3 tools/validate.py --game "/caminho/Victoria 3/game"
python3 tools/package_mod.py
```

Requer Python 3.10+ e somente a biblioteca padrão. Os scripts usam o prefixo
`sed_`, português brasileiro e fallback inglês. Não sobrescrevem arquivos
originais nem escrevem em variáveis de terceiros. Testes estáticos não
substituem a validação no motor do jogo.

## Documentação

- [Entrega, arquitetura implementada e limites da Fase 1](docs/PHASE1.md)
- [Requisitos originais completos](docs/PROJECT_BRIEF.md)
- [Pesquisa técnica](docs/RESEARCH.md)
- [Arquitetura por fases](docs/ARCHITECTURE.md)
- [Compatibilidade](docs/COMPATIBILITY.md)
- [Métricas e fontes](docs/METRICS.md)
- [Auditoria local de mods e saves](docs/LOCAL_AUDIT.md)
- [Relatório estruturado da auditoria](docs/ENVIRONMENT_AUDIT.json)
- [Inventário inicial de fontes](docs/SOURCE_INVENTORY.json)
- [Contexto para continuidade](docs/AI_CONTEXT.md)
- [Registro de fases](docs/PHASE_LOG.md)
- [Testes de campanha e da interface](docs/MANUAL_RUNTIME_TEST.md)
- [Resultado do teste de inicialização na engine](docs/RUNTIME_SMOKE.md)

A [pesquisa anterior na nuvem](docs/RESEARCH_CLOUD.md) e as
[instruções de continuidade local](docs/LOCAL_CODEX.md) foram preservadas.
PMs continuam sob responsabilidade dos outros mods. Os botões adicionam um
nível público após checagens atuais. Em modo Automático, um evento mensal pode
enfileirar no máximo um nível elegível e bloqueia com filas ocupadas,
inadimplência, construção pausada ou flags conhecidas de outros construtores.
A recomendação do setor de construção exige fila pública com pelo menos três
projetos e não promete contratação futura.
