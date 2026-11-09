# Contexto de continuidade

O usuário solicitou seguir `Texto colado.txt` e ir publicando no GitHub
`Lincoln16yyy/SMART-ECONOMY-DIRECTOR`. O conteúdo original está preservado
integralmente em PROJECT_BRIEF.md. Leia-o antes de trabalhar.

Fase atual: protótipo da Fase 2 em 0.3.4. O jogador confirmou em campanha a
interface, os indicadores e a seção vazia de oportunidades. A 0.2.0 acrescentou
até três recomendações ferroviárias e um botão para aprovar uma por vez; a
0.2.1 explica se não há déficit de infraestrutura ou se há déficit sem
candidato elegível. A 0.3.0 acrescenta uma ação de capacidade de construção:
quando a fila pública tem pelo menos três projetos, mostra no máximo um setor
de construção operante no estado mais populoso e permite enfileirar um nível
após revalidação. A 0.3.1 acrescenta a decomposição dos motivos de rejeição por
estado quando não há candidato; a 0.3.2 mostra sob o botão a primeira
guarda que falha quando ele está bloqueado; a 0.3.3 explica quando um cartão
antigo deixou de passar os filtros ou já foi enfileirado. Em 0.3.4, saldo
semanal negativo é um alerta, não uma trava, e ação já enfileirada tem mensagem
própria. A execução dos botões e a coexistência com mods ainda não foram
validadas. Não há automação periódica. A versão 0.3.4 está instalada localmente.
A suíte reportou 46 testes para os dois fluxos existentes; ela não cobre as
mensagens novas nem a remoção da trava de saldo, e não foi executada nesta
alteração. Na captura mais recente do Haiti (11/01/1836), o saldo era -£4,27K,
reservas £0, dívida £268K de crédito £850K, 2 estados, nenhum com déficit de
infraestrutura, fila pública/privada 0/0 e capacidade 10. Como não há déficit de
infraestrutura nem fila pública de três projetos, os dois protótipos atuais
continuam sem candidato; remover a trava financeira não cria candidatos por si
só. Próxima prioridade: pesquisar um tipo de recomendação aplicável ao Haiti,
usando escassez específica de bens, mercado, produção e emprego sem presumir que
o contador agregado de escassez indica qual prédio construir. Em
2026-11-08, o jogador enviou capturas das seções vazias em campanha
(0.3.0 e 0.3.1, Império Otomano, 1/1836): estados vazios corretos nas duas
seções e, na 0.3.1, a linha de motivos corretamente oculta sem déficit/fila
suficiente. Depois, o jogador confirmou atualização (inclusive sob
solicitação) e desativação na engine: os botões clicáveis somem ao
ao desativar. Em leitura posterior, a seção de construção
renderizou o candidato Baixo Egito com o botão de aprovar, e a variação
mensal de PIB funcionou (6,4%). O jogador clicou no botão e nada
aconteceu: o tooltip mostrava o botão Bloqueado, e a fila privada tinha
2 projetos, satisfazendo corretamente a trava da fila privada. Para
confirmar a aprovação, será preciso fila privada vazia. Execução com
clique permitido, linha de motivos com déficit presente, recarga e
coexistência seguem pendentes.

Atualização histórica: a continuação conseguiu entrar na França com
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

Comandos de desenvolvimento permanecem: `python3 tools/build_mod.py --check`,
`python3 tools/validate.py --game "/caminho/Victoria 3/game"`,
`python3 -m unittest discover -s tests -v`, `python3 tools/package_mod.py`.
**46 testes passam** (nove de auditoria e 37 da implementação). O
interpretador de testes modela escopos de país/estado/edifício, listas,
ordenação e construção simulada, cobrindo filtros, ranking, mensagens de estado
vazio, contagens disjuntas de rejeição, linhas de motivo do botão bloqueado,
travas, confirmação/rejeição de fila e limpeza dos dois fluxos. Ele não
confirma primitivas, datamodel nem GUI na engine.

Próximos passos: pedir ao jogador uma conferência breve dos dois botões e das
linhas explicativas, em cópia de save, com o jogo pausado, seguindo os checklists
da 0.3.0–0.3.4 em MANUAL_RUNTIME_TEST.md. Registrar se os estados aparecem, se
as travas desabilitam os botões e se a fila pública ganha um único nível em
cada tipo. Conferir também a linha de motivo sob o botão bloqueado. Não iniciar
testes gráficos ocultos prolongados. Depois
verificar desativação, recarga e coexistência antes de ampliar os tipos de ação.
O comportamento real das pendências é: a marca permanece enquanto a expansão
está enfileirada e some quando ela é concluída ou cancelada.


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
