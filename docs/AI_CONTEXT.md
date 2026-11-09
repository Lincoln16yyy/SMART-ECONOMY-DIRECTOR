# Contexto de continuidade

O usuário solicitou seguir `Texto colado.txt` e ir publicando no GitHub
`Lincoln16yyy/SMART-ECONOMY-DIRECTOR`. O conteúdo original está preservado
integralmente em PROJECT_BRIEF.md. Leia-o antes de trabalhar.

Fase atual: 1, implementação inicial 0.1.0 de diagnóstico, por pedido explícito
do jogador para começar a construção do mod. As lacunas da Fase 0 continuam
registradas e bloqueiam automação econômica, não a entrega de diagnóstico.
Existe pacote instalável gerado em `dist/`; a interface já foi conferida pelo
jogador em campanha, enquanto limpeza, recarga e compatibilidade seguem pendentes.
Não copiar economia de mods por suposição.

Atualização mais recente: a continuação conseguiu entrar na França com
Gamescope headless/DXVK e confirmou ativação por decisão, abertura/rolagem do
diário, atualização manual, agenda sob solicitação e congelamento das leituras
ao avançar de janeiro para fevereiro. PIB, SoL e alfabetização corresponderam
à barra do jogo; saldo observado e previsão da GUI diferiram (RESEARCH/RUNTIME
devem preservar essa distinção). Os demais testes interativos ainda estão
pendentes. O jogador reclamou da demora dos testes ocultos e preferiu abrir
o jogo pessoalmente: não voltar a iniciar testes gráficos prolongados sem
necessidade ou novo pedido. A sessão oculta foi encerrada.

A versão 0.1.0 foi então instalada em `mod/Smart Economy Director` no prefixo
Wine já identificado e adicionada ao final de `content_load.json`, preservando
as dez entradas anteriores. Backup:
`sed_backups/content_load_20261108_222107_956307.json`, nos dados do usuário.
O jogador enviou captura do jogo normal com o diário aberto e os indicadores
visíveis em 27/02/1846; a instalação, ativação e renderização estão confirmadas.
Ainda faltam limpeza/desativação, save/reload e teste dos demais mods em conjunto.

Observação do jogador em 2026-11-08: o diário e os indicadores apareceram na
campanha. Direção de produto confirmada: este projeto deve permitir executar,
por botões, recomendações econômicas dentro do escopo do briefing. O jogador
mantém o Smart Government Advisor separado e prefere que ele apenas recomende
leis. Não confundir aprovação de ações econômicas do Director com alterar leis,
nem tratar os botões de agenda/atualização da 0.1.0 como execução econômica.
Planejamento e ações continuam por fases: cada ação precisa de escopo,
viabilidade técnica, explicação, confirmação por clique e revalidação antes de
executar; automação em segundo plano só entra depois das proteções e pesquisas
previstas no briefing.

RESEARCH.md contém fontes e lacunas; ARCHITECTURE.md descreve propostas, não
funções concluídas. COMPATIBILITY.md diferencia instalação, habilitação no
launcher e automação ativa no país. SOURCE_INVENTORY.json registra commit da
referência, hash do briefing e exemplos com linhas para reproduzir buscas.

O ambiente real é Linux com instalação Windows via Hydra/Wine. Não alterar
instalação, saves ou load order na pesquisa. O Economy Advisor correto é
3778129206, já possui construção e PMs. Kuromi não aparece habilitado; ARoAI sim.
Não usar o nome OGAS como sinônimo do Advisor.

Continuação local: METRICS.md registra a matriz por indicador/GUI;
LOCAL_AUDIT.md e ENVIRONMENT_AUDIT.json registram o exame do Kuromi 8.0,
redefinições e nomes históricos do save. A ferramenta de pesquisa
`tools/audit_environment.py` tem nove testes aprovados e não é código do mod.
ARoAI redefine 18 PMs e pode construir para o jogador sob configuração.
Não copiar modelos aproximados de mão de obra/salários do Advisor como medidas.

Continuação Fase 2: `tools/build_economy_data.py` cria um índice local de
building/PM/PMG com proveniência por camada, sem resolver merge. Foi gerado em
`data/economy_catalog.local.json` (ignorado pelo Git): 122 buildings, 450 PMs,
203 grupos, 67 IDs em mais de uma camada e 0 erros de parsing. As sobreposições
incluem CPC em 48 buildings, Government Administration Auto Expand em um e
ARoAI em 18 PMs; o arquivo local não é fonte efetiva para recomendações.
Próximo: usar o relatório para escolher dados/candidatos cuja semântica final
possa ser confirmada no jogo e expor incertezas.

Fontes da implementação: `data/metrics.json` e `tools/build_mod.py`. Não editar
à mão os arquivos gerados em common/gui/localization e descritores. O schema
atual é 1, ativação sempre explícita por decisão. Só o dispatcher atualiza
mensalmente; a Journal Entry não tem segundo pulso. Desativar limpa tudo, menos
schema. A agenda pode ser mensal ou sob solicitação; não há modos de execução
econômica. O histórico mantém duas amostras-base mensais de PIB e leitura atual.

Comandos: `python3 tools/build_mod.py --check`,
`python3 tools/validate.py --game "/caminho/Victoria 3/game"`,
`python3 -m unittest discover -s tests -v`, `python3 tools/package_mod.py`.
Vinte e quatro testes passaram: nove de auditoria e quinze de diagnóstico,
validação e pacote. O interpretador restrito dos testes executa os scripts,
mas não confirma nomes de primitivas, listas ou GUI na engine.

Próximos passos: usar MANUAL_RUNTIME_TEST.md para desativação/reativação e
save/reload; continuar a pesquisa da fila/ownership e catálogo efetivo antes de
planejar os primeiros candidatos econômicos. O jogador confirmou a interface
no jogo normal. Não apresentar a execução de recomendações como implementada.

Houve teste de inicialização isolado em Xvfb/Wine, descrito em RUNTIME_SMOKE.md:
o mod foi reconhecido e chegou ao menu sem erros próprios na execução limpa.
O save Haiti exige uma regra do Auto-Diplomacy ausente no teste só com Director.
A campanha nova chegou à seleção da França e início da transição, mas a tela
virtual em 1–2 FPS impediu validar o diário. Não apresentar esses resultados
como teste de métricas, botões, desempenho de campanha ou compatibilidade.
Os 26 testes de leis da referência passaram localmente, mas seu validador
completo encontrou 178 erros de pesquisa tecnológica. Não corrigir o outro
projeto no escopo do Director. Validação documental não comprova script aceito
pela engine.

A etapa anterior na nuvem executou 26 testes da referência com sucesso; o
validador não localizou o jogo naquele executor. O registro histórico foi
preservado em PHASE_LOG.md e RESEARCH_CLOUD.md. LOCAL_CODEX.md mantém as
instruções de transição originais; seus caminhos já foram confirmados aqui.
