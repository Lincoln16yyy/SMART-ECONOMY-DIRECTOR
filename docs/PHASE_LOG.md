# Registro de fases

## 2026-11-08 — Publicação da especificação e contexto inicial

Objetivo: disponibilizar no GitHub os requisitos fornecidos pelo jogador para colaboração com outras IAs.

Arquivos: `README.md`, `docs/PROJECT_BRIEF.md`, `docs/AI_CONTEXT.md` e este registro.

Resultados:

- Especificação original preservada integralmente em `docs/PROJECT_BRIEF.md`.
- README com navegação para os documentos e estado real do projeto.
- Contexto para continuidade por outros agentes, com a Fase 0 explicitamente pendente.

Validação: comparação byte a byte do briefing com o arquivo enviado; verificação de links locais e de espaços com `git diff --check`.

Não executado: pesquisa do Smart Government, inspeção do jogo e dos mods, testes automatizados e testes de campanha. Não há implementação do mod nesta entrega.

Próxima fase: pesquisa e diagnóstico conforme `PROJECT_BRIEF.md`, com entrega de `docs/RESEARCH.md` baseada em evidências reais.

## 2026-11-08 — Fase 0: estudo da referência e arquitetura parcial

Objetivo: investigar o Smart Government e identificar os requisitos técnicos do Director antes de implementar.

Referência: `Lincoln16yyy/Smart-Government-Victoria-3-1.15`, commit `95b20870816b9ceabcaf0b7b9371a66c85dd8bf1`. Checkout separado, sem alterações rastreadas.

Entregas: `RESEARCH.md` com fontes fixadas, capacidades e arquitetura proposta; `COMPATIBILITY.md` com controles conhecidos e riscos pendentes; `MANUAL_RUNTIME_TEST.md` com plano sem resultados fictícios; `LOCAL_CODEX.md` com continuidade no CachyOS. README e AI_CONTEXT atualizados.

Validação: 26 testes de regressão da referência executados e aprovados. `python3 tools/validate.py` da referência terminou com exit 1 por instalação do jogo ausente. Não se trata de validação econômica do Director. Links locais e whitespace dos documentos verificados.

Bloqueio: jogo, Economy Advisor e demais mods não encontrados no executor. Caminhos históricos da máquina do jogador não existem aqui. O jogador pediu instruções para continuar pelo terminal local no CachyOS; continuidade documentada.

A Fase 0 permanece aberta. Não foram criados scripts do mod, APIs presumidas ou controles automáticos. Próximo passo: inspeção local do jogo e do ecossistema, completar a matriz de capacidades e apresentar o diagnóstico consolidado.


## 2026-11-08 — Fase 0: pesquisa inicial

Objetivo: estudar a referência, identificar a instalação e mapear sobreposição
com as automações existentes antes de programar.

Entregas: briefing original, README, pesquisa, arquitetura proposta, matriz
de compatibilidade, inventário de referências, contexto e roteiro de testes.
Foram consultados documentos e ciclo de vida do Smart Government, arquivos
vanilla 1.15.0, lista de carregamento e scripts instalados de economia/PMs.

Resultado: o Economy Advisor já executa ações econômicas; a arquitetura propõe
estratégia própria com um executor por domínio. Foram identificados mods extras
habilitados que alteram premissas de construção e produção.

Verificação nesta entrega: preservação do briefing e referências Markdown locais,
integridade JSON do inventário e whitespace do diff. Não há código do mod para
testar. Não foram executados testes interativos ou alterados saves/load order.

Fase 0 permanece aberta pelas lacunas listadas em RESEARCH.md. Fases 1–6 não
iniciadas. Pesos econômicos, classificações e desempenho ainda não calibrados.

## 2026-11-08 — Fase 0: auditoria reproduzível e fontes de indicadores

Objetivo: aprofundar Kuromi, filas, opções do Haiti e alterações de definições,
sem programar o mod ou modificar instalação, saves e ordem de carregamento.

Arquivos: ferramenta `tools/audit_environment.py`, nove testes, `.gitignore`,
ENVIRONMENT_AUDIT.json, LOCAL_AUDIT.md e METRICS.md; atualizados README,
pesquisa, arquitetura, compatibilidade, contexto e roteiro manual.

Resultados: dez mods listados encontrados; Kuromi 8.0 examinado no ZIP; 49
entradas vanilla visadas pelo Controllable Private Construction; administração
substituída pelo Auto Expand; 18 PMs redefinidos pelo ARoAI. A condição de
autobuild do ARoAI permite jogador com regra e flag específicas. O Advisor
considera níveis após fila, mas sua cobertura completa permanece sem teste.

O save Haiti contém gamestate binário e nome histórico do Kuromi. As quatro
strings do Advisor foram registradas como ocorrências, não flags ativas.
Nenhum save foi publicado. A matriz distingue funções GUI de primitivas de
script e aproximações de dados observados.

Validação: nove testes da auditoria passaram; os 26 testes de leis do Smart
Government passaram novamente. Seu validador completo executou com o jogo
local e retornou 178 erros do módulo de pesquisa tecnológica, sem alterar a
referência. O leitor da auditoria registrou seis arquivos vanilla de DNA não
interpretados; não são conclusões sobre economia ou aceitação pela engine.
A auditoria foi repetida com saída em `/tmp`; o relatório resultante foi
idêntico byte a byte. Sintaxe Python, JSON, links locais, briefing original e
`git diff --check` também foram verificados.

Não testado: opções efetivas por país, resolução de merge no jogo, primeira
construção/fila privada, bindings do Director, desempenho e campanhas. Fase 0
continua aberta; nenhuma Journal Entry ou ação econômica foi implementada.

## 2026-11-08 — Construção autorizada: diagnóstico 0.1.0

O jogador pediu explicitamente começar a construção do mod. A entrega ficou
restrita à Fase 1 de diagnóstico; as pendências da pesquisa sobre automação
foram mantidas como limites para fases posteriores.

Objetivo e riscos foram apresentados antes da implementação. Foram criados:
registro de métricas, gerador, cinco arquivos de scripts próprios, widget,
duas localizações, metadados e descritores, validador, empacotador e testes.
O workflow de GitHub Actions verifica a geração, valida e testa, e produz ZIP
como artefato, sem precisar dos arquivos proprietários do jogo.

Implementado: ativar/desativar, leitura sob solicitação ou mensal por um único
dispatcher, treze indicadores nacionais, razões com denominadores protegidos,
contagens de gargalos por estado/edifício e crescimento de PIB com âncoras de
meses distintos. A limpeza conserva só o schema. Não há ações econômicas,
ranking de investimentos, modos de execução ou dependência de outro mod.

Validação: **24 testes passaram** (nove de auditoria e quinze da implementação,
regras, validador e pacote). A geração atualizada, sintaxe, localização, BOM,
limites de efeitos, referências e presença do ícone na instalação local foram
verificados. O ZIP de 11 arquivos foi reproduzido byte a byte. Links da
documentação, briefing original e whitespace foram conferidos.

Runtime: a engine 1.15.0 reconheceu o mod e chegou ao menu numa execução isolada
com dados em `/tmp`, sem erros próprios identificados na inicialização limpa.
Um aviso inicial do marcador de schema foi corrigido. A cópia antiga do Haiti
não abriu porque exige uma regra do Auto-Diplomacy ausente no teste standalone.
O teste de nova campanha chegou à seleção da França e transição de início;
renderização em 1–2 FPS impediu concluir a interação com o diário.
Detalhes: RUNTIME_SMOKE.md.

Status: implementação inicial empacotada para testes; validação funcional da
Fase 1 permanece aberta. Pendentes: decisão/diário na campanha, comparação de
indicadores, agenda, limpeza na engine, salvar/recarregar e ecossistema completo.

## 2026-11-08 — Conferência da interface e instalação para teste do jogador

O teste com Gamescope headless e DXVK nativo permitiu entrar na campanha nova
da França. Foram conferidos ativação pela decisão, abertura e rolagem do diário,
atualização manual, agenda sob solicitação e congelamento das leituras enquanto
a campanha avançava para fevereiro. PIB, SoL e alfabetização corresponderam
à barra do jogo. O saldo observado do script diferiu da previsão da GUI;
nenhuma fórmula foi alterada sem fechar essa investigação.

O jogador preferiu fazer a conferência diretamente por causa da demora e da
sessão sem janela visível. O áudio dessa sessão foi silenciado e o processo de
teste foi encerrado. Não houve novos testes de campanha após esse pedido.

O pacote 0.1.0 foi conferido contra os arquivos gerados, instalado e habilitado
no prefixo real do jogo. As dez entradas preexistentes foram preservadas na
mesma ordem; o Director foi acrescentado ao final. Backup da lista original:
`sed_backups/content_load_20261108_222107_956307.json`. Saves não foram alterados.
O jogador abrirá o jogo e procurará a decisão de ativação. Fase 1 permanece em
validação, sem alegação de automação econômica ou compatibilidade completa.

## 2026-11-08 — Confirmação do jogador e direção para execução econômica

O jogador mostrou uma captura da campanha em 27 de fevereiro de 1846. O diário
do Smart Economy Director está aberto, com leituras e seção de limitações; a
instalação e a renderização da interface foram confirmadas no jogo normal.
Na mesma mensagem, esclareceu que quer botões para ativar recomendações
econômicas deste mod, conforme o escopo do briefing. O Smart Government Advisor
deve continuar limitado a recomendar leis, pois o jogador prefere decidir leis
separadamente.

Implicação de produto: a aprovação individual e execução revalidada de ações
econômicas é objetivo deste projeto, não apenas recomendações visuais. A 0.1.0
continua sendo só diagnóstico: não prometer que já executa recomendações. Fila,
compatibilidade, dados e segurança continuam pré-requisitos antes de cada tipo
de executor e antes de qualquer modo automático.

Na continuação, foi inspecionado o caminho real de construção: o Economy
Advisor usa `start_building_construction` em escopo de estado, verifica a fila
pública em níveis antes/depois e filtra edifícios existentes com
`level_after_queued_constructions`. A instalação também declara triggers de
níveis em filas públicas e privadas. Isso confirma peças do motor, não uma
integração segura; identidade de projeto privado, prédios inéditos, clique e
coexistência continuam pendentes. A captura do jogador confirma a interface na
campanha normal. A pesquisa e a arquitetura agora registram botões de aprovação
econômica como requisito, sem dar ao Director controle de leis.

## Fase 2 — Índice local de buildings e métodos de produção

Criado `tools/build_economy_data.py` para indexar IDs, grupos, tecnologias e
modificadores reconhecidos de buildings/PMs, incluindo origem, ordem, operação
e hash da definição. A ferramenta guarda as camadas; não aplica `INJECT` ou
`REPLACE` nem declara conhecer o resultado final da engine. O relatório com
conteúdo derivado dos mods permanece local e ignorado pelo Git.

Execução na instalação indicada pelo jogador: 122 buildings, 450 PMs, 203
grupos de PM, 67 IDs em camadas múltiplas e nenhum erro de parsing. Das
definições sobrepostas, 48 buildings são de CPC, um de Government Administration
Auto Expand e 18 PMs de ARoAI. `git diff --check` passou; os testes não foram
executados. Próxima etapa: confrontar um candidato econômico com as definições
efetivamente carregadas e as condições do save antes de criar sua recomendação
e botão de aprovação.

## Fase 2 — Primeira ação aprovada: expansão ferroviária 0.2.0

Implementado o primeiro fluxo vertical de recomendação e execução individual.
O diário lista até três estados incorporados do jogador com infraestrutura
negativa, ferrovia existente e ocupação de pelo menos 80%, sem falha de
contratação, escassez ou expansão já enfileirada. O botão revalida o estado ao
ser clicado e só fica habilitado com o jogo pausado, saldo semanal não negativo,
sem default e fila privada vazia. Ele solicita um nível público de ferrovia;
nenhuma ação ocorre sem clique, não há estimativa de retorno e não há repetição
automática. A solicitação pendente fica marcada até a expansão enfileirada ser
concluída ou cancelada; enquanto ela estiver na fila, o estado não é oferecido
novamente.

Gerados e empacotados os arquivos da 0.2.0. Validação estática do pacote e
`git diff --check` passaram; não foram executados testes unitários nem testes
na engine para esta ação. O parser estrutural foi ampliado para declarações GUI
de tipos. A 0.2.0 foi instalada no perfil local; a cópia anterior foi salva em
`sed_backups/mod_0.1.0_20261108_230131_474104`, e as 11 entradas preexistentes
da lista de mods foram preservadas. Próxima verificação: o jogador abrirá o
jogo normal e confirmará renderização da lista, tooltip e comportamento do
botão na campanha. Compatibilidade da ação e do datamodel permanece pendente.

## Fase 2 — Explicação do estado sem recomendações 0.2.1

O jogador mostrou a seção de oportunidades em campanha com zero estados em
déficit de infraestrutura. A interface já estava correta ao não sugerir uma
obra; o texto genérico não explicava qual filtro havia esvaziado a lista.
Atualizei a interface para distinguir “sem déficit de infraestrutura” de
“há déficit, mas nenhuma ferrovia passou pelos filtros”. Isso não altera os
critérios nem executa ações.

A validação da geração e do pacote é estática; botão, nova localização e fluxo
de execução ainda precisam de conferência no jogo. Não foram executados testes
unitários nem sessão gráfica oculta.

Pacote 0.2.1 instalado no perfil local após backup de 0.2.0 em
`sed_backups/mod_0.2.0_20261108_231349_643103`. As 11 entradas preexistentes
foram preservadas e o mod permaneceu habilitado.

## Fase 2 — Testes automatizados alinhados à ação ferroviária

Troquei o interpretador restrito da 0.1.0 por um modelo de escopos de país,
estado e edifício, com variáveis por estado, listas, ordenação de estados,
`owner`/`prev`, leitura de triggers próprios e simulação controlada de
`start_building_construction`. Isso permite executar os scripts gerados da
0.2.1 sem emular a engine: os resultados continuam sendo regressões do recorte
de script, não validação de primitivas, datamodel ou renderização.

Foram acrescentados testes para os filtros de elegibilidade da ferrovia, o
ranking de até três estados por déficit, as mensagens de estado vazio, as cinco
travas de aprovação, a confirmação ou rejeição da inclusão na fila, o estado
pendente por estado e a limpeza de listas/variáveis. **33 testes passam** (nove
de auditoria e 24 da
implementação). A suíte revelou que a documentação descrevia a pendência como
se ela terminasse ao entrar na fila; o script mantém a marca enquanto a
expansão está enfileirada e a remove quando ela é concluída ou cancelada. O
texto foi corrigido sem alterar o comportamento econômico.

`build_mod.py --check` e a validação estática continuam passando. Nada foi
executado na engine nem em sessão gráfica. A conferência do botão, da pausa,
das travas, do contador público, da recarga e da coexistência com outros mods
segue pendente e depende do jogador em cópia de save.

## Fase 2 — Segunda ação aprovada: capacidade de construção 0.3.0

Acrescentei o segundo fluxo vertical de recomendação e execução. Quando a fila
pública tem pelo menos três projetos, o Director examina estados incorporados
com setor de construção existente, nível positivo, ocupação de ao menos 90%,
sem falha de contratação, falta de insumos ou expansão já enfileirada. Entre os
elegíveis, mostra no máximo o estado mais populoso. O botão revalida o edifício,
a fila pública mínima, a pausa, o saldo semanal não negativo, a ausência de
inadimplência e a fila privada vazia. A aprovação enfileira um único nível
público e confere o contador da fila; não há repetição automática.

A lista, o pedido pendente e o status são separados dos da ferrovia. A limpeza
remove as duas listas e as duas marcas estaduais. O validador passou a exigir
que cada ação aprovada enfileire somente o edifício declarado. A interface ganhou
uma seção própria, com estados vazios distintos para fila curta e para setores
rejeitados pelos filtros.

Validação: **40 testes passam** (nove de auditoria e 31 da implementação), a
geração está atualizada e a validação estática passa. O pacote 0.3.0 foi gerado.
A versão foi instalada no perfil local com backup da 0.2.1 em
`sed_backups/mod_0.2.1_20261108_232750`; as 11 entradas de
`content_load.json` foram preservadas e o Director permaneceu habilitado.
Não houve execução na engine nem sessão gráfica; renderização, clique, contador
público, recarga e coexistência com outros construtores continuam pendentes.

## Fase 2 — Confirmação visual da 0.3.0 em campanha

O jogador enviou uma captura do jogo normal com o diário da 0.3.0 aberto. A
nova seção **Capacidade de construção** renderizou abaixo das oportunidades de
infraestrutura, com o protótipo, o critério de três projetos e a mensagem de
fila curta: “A fila pública tem menos de três projetos. O Director não recomenda
ampliar a capacidade de construção agora.”

A leitura mostrada era de 1/1836, com 17 estados analisados, nenhum estado com
infraestrutura negativa ou acesso ao mercado abaixo de 100%, nenhum edifício com
insumos em falta, 22 com contratação incompleta, duas falhas de contratação,
capacidade de construção 10,0 e filas pública e privada em 0. Isso explica
corretamente a ausência de candidatos ferroviários e de capacidade de
construção. Nenhum botão de aprovação foi exibido ou clicado, portanto a
execução das duas ações continua sem confirmação na engine. A suíte permanece
com 40 testes aprovados e os artefatos instalados conferem com a geração.

## Fase 2 — Motivos de rejeição por estado 0.3.1

Quando não há candidato, o painel passa a decompor os estados por um único
motivo principal, em vez de apenas dizer que nenhum passou pelos filtros. Na
seção ferroviária, o total de estados com déficit de infraestrutura é dividido
em sem ferrovia, ferrovia não operante (nível, ocupação, contratação, insumos
ou expansão já enfileirada) e bloqueados por incorporação ou permissão de
construção. Na seção de capacidade de construção, o total de estados com
setor é dividido em setor não operante e bloqueados. As categorias são
disjuntas e as contagens somam o denominador exibido.

Os contadores são zerados a cada leitura e só aparecem quando há déficit/fila
suficiente sem candidatos; a nova linha some assim que surge um candidato. A
decomposição descreve os filtros atuais, não custos ou retornos. O pacote
0.3.1 foi gerado, validado estaticamente e a suíte passou com 45 testes
(nove de auditoria e 36 da implementação).

Não testado: renderização da linha de motivos e execução dos dois botões na
engine, desativação, recarga e coexistência com outros construtores. O
próximo passo é a conferência breve do jogador em cópia de save, com o jogo
pausado.

## Fase 2 — Confirmação em campanha da 0.3.1 (estados vazios)

O jogador enviou captura do diário da 0.3.1 em campanha (Império Otomano,
leitura de 1/1836): saldo semanal de script de £18,3K, reservas de £273K,
PIB de £5,41M, alfabetização de 12,5%, capacidade de construção de 16,0,
filas pública e privada em 0, 17 estados analisados, nenhum com
infraestrutura negativa ou acesso ao mercado abaixo de 100%, nenhum edifício
com insumos em falta, 22 com contratação incompleta e duas falhas de
contratação.

As duas seções exibem os estados vazios corretos: “Sem déficit atual de
infraestrutura” na seção ferroviária e “fila pública tem menos de três
projetos” na seção de capacidade de construção. A linha de motivos da 0.3.1
não apareceu, como esperado: ela só é exibida com déficit/fila suficiente
sem candidatos, condições que não existiam nesta leitura. Nenhum botão foi
exibido ou clicado, portanto a execução das ações e a renderização da linha
de motivos seguem não confirmadas na engine. Desativação, recarga e
coexistência também permanecem pendentes.

## Fase 2 — Atualização, desativação e candidato de construção em campanha

O jogador relatou que a atualização funciona, inclusive sob solicitação
(agenda não mensal), e que desativar faz os botões clicáveis (Atualizar,
atualizar todo mês, Desativar) desaparecerem — o ciclo de vida confirmado na
engine. Em nova leitura, o painel mostrou saldo de £22,3K, reservas de
£381K, PIB de £5,76M com variação de 6,4% em um mês, capacidade de
construção de 16,0, fila pública com 10 projetos, fila privada com 2, 17
estados analisados, nenhum com infraestrutura negativa ou insumos em falta,
31 edifícios com contratação incompleta e 93 falhas de contratação.

Com a fila pública acima de três projetos, a seção de capacidade de
construção passou a exibir um candidato: **Baixo Egito — setor de
construção**, com o texto de motivo e o botão “Aprovar: enfileirar 1 nível
do setor”. A seção ferroviária permaneceu no estado vazio correto, sem
déficit de infraestrutura, e a linha de motivos não apareceu em nenhuma
seção, como esperado.

Não foi relatado o clique no botão de aprovação, portanto a inclusão do
nível na fila pública, as travas de clique e a revalidação na engine
seguem sem confirmação. Recarga e coexistência com outros construtores
ainda permanecem pendentes.

## Fase 2 — Clique no botão bloqueado pela fila privada (5 de março de 1836)

O jogador clicou no botão “Aprovar: enfileirar 1 nível do setor” do
candidato Baixo Egito e nada aconteceu nem apareceu. A captura mostra o
tooltip do botão com cadeado **Bloqueado** e o texto: “Só funciona com o
game pausado, fila pública de ao menos três projetos, saldo semanal não
negativo, sem inadimplência e sem níveis na fila privada. Também revalida
o estado e as filas no clique.” Nesta leitura, a fila privada tem **2
projetos**, portanto a trava da fila privada mantém o botão desabilitado
e o clique é ignorado — comportamento correto.

Para confirmar a aprovação na engine, o jogador precisará esvaziar a fila
privada (ou usar uma cópia de save em que ela esteja vazia), com o jogo
pausado, e então clicar. A inclusão do nível na fila pública, a
revalidação no clique e o aviso de confirmação seguem sem confirmação.

## Fase 2 — Linha de motivo do botão bloqueado 0.3.2

O jogador fez um clique no botão de aprovação com a fila privada não vazia e
nada aconteceu sem explicação; o tooltip mostrava o cadeado e listava todas
as travas, mas não dizia qual falhava. A 0.3.2 mostra, sob o botão de
aprovar, a primeira guarda que falha: jogo rodando, fila privada não vazia,
inadimplência ou saldo semanal negativo (para a construção, também fila
pública abaixo de três projetos antes dessas). Cada linha é um SGUI em
escopo de estado avaliado na hora, com ordem em cascata, de modo que apenas
um motivo aparece por vez. As travas em si não mudaram; o comando de
aprovação continua revalidando no clique.

Validação: **46 testes passam** (nove de auditoria e 37 da implementação),
a geração está atualizada, validação estática e pacote
`dist/smart-economy-director-0.3.2.zip` concluídos. Renderização da linha de
motivo e execução dos botões na engine seguem pendentes.

## Fase 2 — Captura posterior ainda sem a 0.3.2 (4 de abril de 1836)

O jogador enviou nova captura do diário: leitura atualizada (PIB de £5,8M,
variação de 0,4% em um mês, filas pública 10 e privada 2, 86 falhas de
contratação) com o candidato **Médio Egito — setor de construção** e o
botão de aprovar. A linha “Botão bloqueado: há níveis na fila privada” da
0.3.2 **não apareceu** sob o botão, o que indica que o jogo ainda roda a
0.3.1 (o pacote 0.3.2 foi gerado, mas a instalação no perfil não foi
confirmada nesta captura). A troca de candidato entre leituras reflete a
recomputação a cada atualização (condições correntes de elegibilidade),
não um erro. Próximo passo: instalar o ZIP 0.3.2 no perfil e reconfirmar.

## Instalação local da 0.3.2

O descritor instalado no perfil ainda era **0.3.0** — nem 0.3.1 nem 0.3.2
havia sido instalada no prefixo (o ZIP da 0.3.2 foi extraído agora, com
backup da 0.3.0 em `sed_backups/`). O `content_load.json` não foi alterado
e o mod permanece habilitado. Próxima sessão: abrir o jogo e conferir a
linha de motivo do botão bloqueado e o clique de aprovação.

Atualização posterior: a leitura do perfil local confirma agora
`version="0.3.2"` em `mod/Smart Economy Director/descriptor.mod`, e a entrada
do mod continua habilitada entre as 11 entradas do load order. A captura sem a
linha de motivo foi feita antes dessa atualização e não valida a renderização
da 0.3.2. Ainda falta confirmar a linha e executar uma aprovação com as travas
satisfeitas.

## Fase 2 — Estado de recomendação desatualizada 0.3.3

Na revisão dos novos fluxos, identifiquei um estado silencioso possível: o
cartão fica na lista calculada na última leitura, mas o botão é revalidado ao
vivo. Depois de uma condição mudar — inclusive após enfileirar a própria ação —
o botão pode ficar desabilitado sem uma das mensagens das travas financeiras.
A 0.3.3 acrescenta uma mensagem de cartão desatualizado para as duas ações,
orientando nova leitura. A validação de clique permanece como autoridade e
nenhuma ação é executada pelo cartão obsoleto.

Geração e validação estática do pacote passaram; testes unitários e verificação
na engine não foram executados nesta alteração. A 0.3.3 foi instalada no perfil
local após backup da 0.3.2 em
`sed_backups/mod_0.3.2_20261109_002500_858490`; o mod segue habilitado e as 11
entradas anteriores foram preservadas. A mensagem precisa ser conferida numa
campanha.

## Fase 2 — Alerta de orçamento sem bloquear aprovação 0.3.4

O jogador esclareceu que saldo semanal negativo não deve impedir uma ação
econômica recomendada: o Director precisa expor o alerta e deixar a decisão
final ao botão de aprovação. Removi o saldo mínimo das duas validações de
aprovação e dos motivos de bloqueio; pausa, ausência de inadimplência, fila
privada vazia, elegibilidade estadual e a exigência de três projetos para
expandir o setor de construção continuam como travas.

Também separei o estado de ação pendente do cartão realmente desatualizado.
Depois de uma aprovação incluída na fila, a linha informa que não se deve
aprovar de novo; um cartão que perdeu elegibilidade pede nova leitura e deixa
claro que nada foi executado. O saldo negativo aparece como alerta junto a cada
candidato, com orientação para revisar custo e prazo na fila do jogo.

Geração, `build_mod.py --check`, validação estática no empacotamento e
`git diff --check` passaram. Não foram executados testes unitários nem feita
conferência na engine para a 0.3.4. O pacote foi instalado no perfil local após
backup da 0.3.3 em
`sed_backups/mod_0.3.3_20261109_005440_321706`; o mod continua habilitado e as
11 entradas do load order foram preservadas.

Na captura do Haiti (11/01/1836), havia 0 estados com déficit de infraestrutura,
fila pública/privada 0/0 e saldo semanal -£4,27K. Portanto, nenhuma das duas
ações estreitas gera candidato nesse cenário: ferrovia exige déficit de
infraestrutura e setor de construção exige fila pública de ao menos três
projetos. A nova regra permite aprovar uma oportunidade elegível mesmo com
saldo negativo, mas não inventa uma oportunidade. A próxima ação para cobrir
esse caso depende de identificar uma necessidade específica do mercado e uma
resposta produtiva compatível com emprego e insumos.

Continuação da pesquisa: no Economy Advisor instalado, o perfil gerado
consulta escassez nacional por bem com `market = { mg:<good> ?= {
market_goods_has_goods_shortage = yes } }` e escassez local com
`state = { sg:<good> ?= { state_goods_has_local_goods_shortage = yes } }`;
também compara sell orders, buy orders e demanda futura de métodos de produção
(`advisor_generated_profiles.txt:21264–21270`). Atualizei RESEARCH.md com essa
evidência e seus limites. Ela permite observar um bem específico, mas ainda
não identifica qual prédio produtor é seguro ampliar; o catálogo local preserva
camadas e não resolve merge nem método ativo. Nenhum novo botão foi criado por
palpite a partir da contagem agregada de prédios com falta de insumos.

## Fase 2 — Oferta local para bens em escassez 0.3.5

A partir do catálogo local, selecionei oito combinações vanilla de bem e prédio
produtor: madeira/acampamento madeireiro, ferro/mina de ferro, carvão/mina de
carvão, cereais/fazenda de trigo, tecido/plantação de algodão,
ferramentas/oficina de ferramentas, mantimentos/indústria alimentícia e
roupas/fábrica têxtil. Cada lista verifica que o método de produção ativo no
prédio gera positivamente aquele bem; métodos que consomem o próprio bem foram
excluídos.

O candidato exige escassez do bem no mercado do país, produtor existente em
estado incorporado, ocupação de ao menos 80%, sem falha de contratação, sem
falta de insumos e sem nível já enfileirado. Mostra até três estados por bem.
O clique exige jogo pausado, país fora de inadimplência e fila privada vazia,
revalida mercado/prédio e enfileira apenas um nível público. Saldo negativo
continua sendo aviso. Sem produtor elegível, a seção informa que a versão não
propõe prédio novo. Custos, preço futuro, contratação e retorno ainda não são
calculados.

A ferramenta de catálogo confirmou vínculo do método com o grupo de produção
do prédio e modificador de saída positivo para as oito combinações. A versão
0.3.5 foi gerada, passou validação estática contra o jogo 1.15.0 e
`git diff --check`. Isso não confirma execução dentro da engine. O próximo
passo é instalar esta versão e pedir ao jogador para conferir uma escassez que
gere candidato, as travas e a inclusão do nível na fila. Nenhum teste gráfico
foi iniciado.

## Fase 2 — modos de execução visíveis e automação opt-in 0.3.6

A captura do Egito mostrou o jogo pausado enquanto a aprovação individual dizia que era necessário pausar. A 0.3.6 remove essa trava das aprovações manuais: o clique revalida a elegibilidade, o modo Assistido, as filas e inadimplência. Os cartões mantêm botão visível nos três modos, com explicação quando o modo não permite agir. Os três modos têm controles visíveis no topo do diário e mostram status persistente. Saves antigos sem modo migram para Assistido.

Automático é opt-in. Uma revisão mensal pode enfileirar no máximo um nível ferroviário ou de um produtor local para um bem em escassez; requer filas vazias, ausência de inadimplência e construção não pausada, além de checar três flags conhecidas de construtores externos. A revisão agenda o evento no dia 23 para evitar parte dos construtores comuns do começo do mês. Não se presume compatibilidade completa com mods externos nem segurança para deixar a campanha sem supervisão. Validação estática contra a instalação 1.15 passou; ainda falta confirmar modos, clique e evento no jogo normal.

## Fase 3 — motivo visível da revisão automática 0.3.7

A captura do Egito (setembro de 1838) mostra o Director ativo e construção em andamento: fila pública com 46 níveis, fila privada com 2. A automação bloqueia corretamente nesses casos, mas o estado anterior era genérico e não ajudava a distinguir bloqueio de falha. A 0.3.7 atribui status diferentes a candidato ausente, inadimplência, fila ocupada, construção pausada e automação concorrente, e apresenta a razão no alto do diário.

A mudança não relaxa as travas nem habilita novas ações. Geração, validação estática e pacote contra os arquivos do jogo passaram. A 0.3.7 ainda precisa ser instalada no perfil local e a nova linha de status confirmada na campanha após um ciclo mensal.


## Continuação — recuperação da suíte da 0.3.7

A execução da suíte encontrou 34 falhas inicialmente: o harness ainda não
suportava o escopo de mercado usado desde a 0.3.5. Após modelar mercado, bens
opcionais ausentes, métodos de produção ativos, busca de estados e registro de
eventos, restaram expectativas antigas de pausa, saldo e variáveis estaduais.
Essas expectativas foram alinhadas às regras atuais. A restauração de leituras
entre subcasos ferroviários foi corrigida para restaurar o campo alterado.

Foram adicionados cenários para os três modos exclusivos, evento sem duplicata,
travas de inadimplência/filas/construção pausada/construtores conhecidos,
ausência de candidato, limite de uma ação e revalidação após inclusão. Os oito
produtores são exercitados com e sem escassez, método ativo, ocupação, falha de
contratação, falta de insumos e expansão prévia; nova aprovação não duplica.
Aprovações manuais com jogo rodando e saldo negativo também são cobertas.

Resultado: **51 testes passaram**; artefatos gerados atuais, validação estática
sem caminho do jogo e `git diff --check` passaram. Não houve mudança nos
arquivos carregáveis, reinstalação nem teste gráfico. A conferência da revisão
mensal e dos botões na engine continua pendente.


## Correções de execução 0.3.8

Dois testes novos reproduziram defeitos do gerador: a revisão automática usava
infraestrutura sem inverter o sinal, escolhendo déficit menor em vez da mesma
prioridade da lista; e uma substituição textual inseria limpeza de todas as
marcas de oferta também na resolução de um setor de construção. O sinal foi
alinhado e a substituição limitada ao bloco de desativação. A suíte de limpeza
agora preenche todas as marcas estaduais de oferta antes de desativar.

Os 53 testes passaram após a correção. Os arquivos carregáveis foram regenerados
como 0.3.8. A ordem entre tipos de ação permanece a mesma. A execução e a ordem
real na engine ainda precisam de conferência; nenhuma campanha foi iniciada.

Geração, validação estática contra o jogo local, empacotamento e
`git diff --check` passaram. Instalação local verificada byte a byte com o
gerador, sem jogo em execução. Backup: `mod_0.3.7_20261109_100657_248672`.
O load order foi preservado byte a byte. O envio ao GitHub segue impedido por
falha de resolução DNS de github.com.


## Status de tentativa automática sem confirmação 0.3.9

O teste de inserção recusada reproduziu, nos nove tipos de ação automática,
um estado incorreto: havia candidato e tentativa, mas a mensagem dizia que não
havia ação elegível. A revisão agora atribui 15 ao selecionar candidato e só
muda para sucesso com confirmação de aumento na fila pública. A GUI apresenta
uma linha em português/inglês para a inclusão não confirmada. Não há tentativa
de outro candidato na mesma revisão. A revisão mensal futura continua normal.
Os códigos antigos de status foram preservados.

O evento gerado também foi testado com Automático, Assistido, Manual e Director
desativado: revalida o modo, não age após desativação e libera o marcador para
agendar a próxima revisão no modo automático. São verificações do harness,
sem simular passagem de tempo ou persistência de eventos na engine.

Resultado: 55 testes aprovados, validação estática contra o jogo local e
empacotamento aprovados. Nenhum jogo foi iniciado. O error.log disponível é de
02:38 de 2026-11-09, anterior às instalações da 0.3.8/0.3.9; tem mensagens de
localização ausente dos status da 0.3.7, mas não comprova defeito na instalação
atual. As chaves estão nos dois arquivos de localização atuais.

Instalada a 0.3.9 sem jogo em execução, com backup `mod_0.3.8_20261109_100912_949247`.
Arquivos conferidos byte a byte com o gerador; load order preservado byte a byte.


## Diagnóstico de produtores rejeitados 0.4.0

As capturas do Império Otomano, 13 e 18/06/1839, confirmam apresentação do modo
Automático e da mensagem de revisão bloqueada por filas ocupadas. O diagnóstico
registra 45 projetos públicos, dois privados, zero estados com infraestrutura
negativa, dois setores de construção não operantes e escassez de ferro sem
produtor elegível. A leitura sob solicitação era de 6/1839; a captura não prova
que uma revisão ocorreu entre os dois dias nem que o executor incluiu obra.

Foi acrescentada a decomposição dos produtores estaduais rejeitados para os
oito bens. Só aparece na escassez sem candidato e identifica explicitamente
a última leitura. Conta estados com o prédio, inclusive nível zero, e atribui
um motivo principal pela ordem: pendente/enfileirado, não incorporado,
nível/ocupação, contratação, insumos, método ativo, permissão. Estados sem o
prédio não são produtores rejeitados. Zero produtores informa ausência de base
produtiva, sem sugerir construção nova. As variáveis entram no registro de
limpeza; são reiniciadas em cada atualização. Reutiliza exclusivamente
primitivas dos filtros já pesquisados e não modifica ações ou travas.

57 testes passaram, cobrindo os oito bens, rejeições múltiplas sem dupla
contagem, produtor elegível excluído das rejeições, estado sem produtor,
reinício dos contadores, visibilidade e limpeza completa. Geração, validação
estática contra Victoria 3 local, pacote e diff sem erros. A nova renderização
não foi conferida na engine e nenhuma campanha foi iniciada.

0.4.0 instalada sem jogo em execução. Backup: `mod_0.3.9_20261109_102912_254983`.
Arquivos conferidos byte a byte com o gerador; load order preservado byte a byte.


## Preferências por recomendação 0.4.1

Implementado o controle de ignorar/restaurar previsto no briefing. Usa somente
variáveis estaduais, escopos e botões já presentes no mod; não acrescenta
primitiva de jogo. Cada um dos dez tipos de ação tem marca própria por estado,
consultada no filtro compartilhado entre lista, aprovação e revisão automática.
O clique revalida elegibilidade, país jogador e ativação antes de gravar a
escolha e atualizar a leitura. As escolhas valem em todos os modos e persistem
nas atualizações. Restaurar limpa todas as escolhas nos estados atuais do país
e recalcula, preservando as obras pendentes. Desativar limpa também as escolhas.

Botões novos em cada cartão e controle no topo, com aviso enquanto houver
escolhas ignoradas. Alturas de cartões/linhas aumentadas para o novo botão.
As contagens de rejeição incluem ignorados como primeiro motivo; os demais
motivos permanecem disjuntos. Não é rejeição de um bem no país inteiro.

61 testes passaram, incluindo os dez tipos nos três modos, revalidação de
ativação/jogador, bloqueio de execução, restauração sem construir, preservação
de pendências, separação de tipos/estados e escolha automática de outro estado.
Testes existentes de limpeza incluem todas as novas variáveis. Save/reload,
layout real e novos cliques ainda precisam de confirmação na engine.

Geração, validação estática contra o jogo, pacote e diff passaram.
Instalada sem jogo em execução; backup `mod_0.4.0_20261109_103945_594880`.
Arquivos comparados com o gerador e load order preservado byte a byte.


## 2026-11-09 — Auditoria completa solicitada pelo jogador, sem implementação

Revisão auditada: `ccf5c2ba325203faad9d704a1f139e21b8ce3261`, main, 0.4.1.
Entregas: `AUDIT_2026-11-09.md` e `AUDIT_EVIDENCE_2026-11-09.json`, mais
correções editoriais de orientações contraditórias. Briefing/histórico preservados.
Nenhuma funcionalidade, instalação, opção ou save foi alterado; jogo não iniciado.

Verificado agora: 61 testes Director (52 diagnóstico/estrutura, 9 pesquisa),
26 testes SG separados; validador SG continua com 178 erros. Geração atual,
validação estática Director com jogo local, ZIP determinístico de 13 arquivos,
instalação idêntica sem extras, links locais válidos. Inventário atual: 11 mods,
6 exclusões de parsing vanilla DNA; catálogo local 122 buildings/450 PM/203 PMG,
67 IDs em camadas, zero erros do catálogo. Logs até 10:29, anteriores às versões
0.4.x, não apresentam sed_; têm 830 linhas atribuídas a caminhos ARoAI, sem
inferir causalidade do Director.

Conclusão: Fase 0 parcial; diagnóstico parcialmente comprovado; planejamento
nacional ausente; execução experimental. Fila/reconciliação, opções por país,
capacidade incremental e política fiscal são pré-requisitos antes de certificar
automação segura. Até 28 cartões possíveis, não top três global. CI ainda aponta
ZIP 0.1.0; não foi corrigido durante auditoria. `days=23` é atraso relativo,
não garantia de dia 23; falta guardião explícito de mês de execução. Os testes
não modelam tempo/save/reload e não comprovam inclusão real na engine.

GitHub consultado pelo conector: main `9366277…`; duas mudanças de recursos
0.4.0/0.4.1 estavam locais no início. Git fetch/push no shell falha por DNS,
mas o conector lê; não afirmar indisponibilidade de todos os acessos ao GitHub.
Próximo bloco recomendado: concluir pesquisa e teste mínimo de fila/domínios,
sem ampliar funcionalidades. A auditoria não alterou as guardas existentes.


Publicação da auditoria: conector GitHub permitiu criar branch
`audit/2026-11-09-state` e PR em rascunho
https://github.com/Lincoln16yyy/SMART-ECONOMY-DIRECTOR/pull/1
(commit remoto documental `bd4e7e3dfbdef3c8ae97d63289e8822354534f6d`).
Somente relatório e JSON seguro foram publicados nesse PR, com base remota
0.3.9 e referência explícita ao checkout local 0.4.1. Não foi feito merge nem
alterada a main remota. As correções editoriais e os dois commits de recursos
continuam locais; o transporte Git no terminal segue com erro de DNS.


## Continuação — artefato CI atual e contrato de fila

O CI de ada7c26 foi observado aprovado após o push do jogador. Seu workflow,
porém, ainda procurava o ZIP 0.1.0. Corrigida a entrega para caminho fixo
`dist/smart-economy-director.zip`, nome genérico de artefato e
`if-no-files-found: error`. A versão permanece nos descritores do ZIP; a CLI
local conserva seu default versionado. Nenhuma alteração no mod instalado.

61 testes e validação estática com jogo local passaram. O comando exato de
empacotamento do workflow foi executado; os 13 arquivos e seus bytes foram
comparados aos outputs, e metadata/descritor confirmaram 0.4.1. O upload novo
no GitHub ainda depende de execução do workflow após publicar esta mudança.

Pesquisa adicional em QUEUE_CONTRACT.md: fontes GUI dos projetos separadas das
primitivas de script; identificado que as opções ferroviária, elétrica e de
setores do Supply Chain independem de zw_var_expand_building. Matriz mínima
para verificar filas/identidade/persistência preparada, com todos os casos
explicitamente não executados. Não foi iniciado jogo ou alterado save/load order.


## Continuação — auxiliar separado para medir a fila

Implementado `tools/build_queue_probe.py` e seis testes. Gera o Smart Economy
Queue Probe (test) 0.1.0, independente, com decisão/JE e leitura sob solicitação.
Projetos e níveis nacionais separados; lista de dez tipos de edifício com
estado, nível atual, nível após fila e diferença. Não agrega a diferença como
se fosse cobertura de todos os projetos; ausência de linha não vira zero.

O auxiliar só escreve namespace próprio sedqp_. Sem construir, alterar PM,
cancelar/reordenar ou agendar eventos. Validador restrito protege o recorte de
efeitos; pacote principal continua sem seus scripts. Workflow publica ZIP
auxiliar separado. Manual em QUEUE_PROBE.md. Nenhuma instalação, save ou opção
foi alterada, e nenhum jogo foi iniciado. Main runtime permanece 0.4.1.

67 testes passaram: os 61 anteriores e seis do auxiliar, com amostras de
projetos/níveis distintos, nível zero sintético, lista recalculada, diferença
negativa, limpeza sem afetar Director/projetos, casos desativado/não jogador,
rejeição de mutação e ZIP determinístico separado. A consulta is_building_type
foi conferida no tutorial vanilla. Binding Building/lista, cobertura real de
primeira construção e persistência continuam sem verificação na engine.


## Interface principal legível e controles visíveis 0.5.0

O jogador esclareceu que só conseguirá testar quando houver botões visíveis e
textos legíveis, e pediu continuar a construção. Esta etapa prioriza a UI do
Director, sem depender do auxiliar de fila ou exigir uma rodada de testes sua.

Confirmado nos fontes locais que os controles antigos usavam som/tooltip,
sem template default_button que fornece textura/borda/estados. Corrigido em
todos os 30 botões gerados. Corpo usa fontsize_large (20), títulos fontsize_xxl
(26), controles 52 pixels. Modos cabem em uma linha de 500 pixels; ações e
ignorar em cartões usam 468 pixels. Conteúdo textual tem mínimo/máximo de
largura e multiline. Cartões/listas usam flowcontainer/datamodel de altura
natural, padrão encontrado em widgets vanilla, eliminando linhas fixas que
cortariam o texto ampliado. Background de container também existe no vanilla.

Recomendações vêm antes dos indicadores detalhados, com resumo de saldo,
reservas e filas no topo. Mostrar/Ocultar indicadores e detalhes só altera a
preferência sed_details_visible; não constrói. Contadores extensos e limites
ficam na visão detalhada. Mensagens curtas e tooltips preservam o escopo da
aprovação. Filtros, ações e travas econômicas não foram relaxados.

70 testes passaram: os 67 anteriores, mais controles nativos/altura/fonte,
toggle sem ações econômicas e cartões sem altura de linha fixa, com
recomendações antes dos detalhes. Geração, validação estática contra o jogo e
pacote 0.5.0 passaram. Aparência e layout na engine ainda não confirmados;
nenhuma sessão gráfica foi iniciada.

Instalada 0.5.0 sem jogo em execução; backup `mod_0.4.1_20261109_113054_750010`.
ZIP/arquivos instalados comparados byte a byte ao gerador, 13 outputs.
Load order preservado byte a byte. Não foi instalado o auxiliar de testes.


## Cartões acionáveis e atalho da fila 0.5.1

Acrescentados estado Aprovação disponível nos cartões elegíveis em Assistido,
controle Passar para Assistido em outros modos e Atualizar recomendações nos
cartões que perderam elegibilidade. A troca muda somente o modo e não aprova
obra; atualização só relê e recalcula, com revalidação dentro do efeito.
Mensagem de fila/default exige agora Assistido, evitando múltiplas orientações
operacionais quando a aprovação individual está desativada pelo modo. Pending
e stale continuam separados e não sugerem trocar modo como solução.

Abrir fila de construção no topo usa a chamada nativa identificada em
`game/gui/states_panel.gui:3809`, sem adicionar escrita em projetos. Fonte 20,
títulos 26, controles de 52 pixels e altura natural dos cartões preservados.
Guardas econômicas e critérios de construção não foram relaxados.

73 testes aprovados (70 anteriores + três novos), incluindo dez tipos em
Manual/Automático, troca sem construir, evento pendente respeitando Assistido,
prontidão e motivos coerentes com modo/fila/default/pending, atualização stale
sem construir e callback revalidado após mudança de condições/desativação.
Atalho verificado estruturalmente contra a chamada vanilla, não executado na
engine. Geração/validação estática/pacote executados; nenhum jogo foi iniciado
nem pedido outro teste ao jogador.

Instalada 0.5.1 sem jogo em execução; backup `mod_0.5.0_20261109_114658_276092`.
Os 13 outputs do ZIP/instalação conferem com o gerador, load order inalterado.


## Captura legível e painel temporal do Automático 0.5.2

O jogador enviou captura do Director: botões nativos com fundo/borda, textos
ampliados, modos, Abrir fila e Mostrar indicadores visíveis. Leitura 7/1839,
saldo £15.3K, reservas £2.36M, projetos públicos 45/privados 2, sem déficit de
infraestrutura. Confirma renderização da UI 0.5.x compatível com as alterações
0.5.1, não cliques, inclusão de obra ou execução do novo painel.

Implementado painel que distingue evento pendente/espera pelo pulso, primeiro
bloqueio operacional atual e último resultado datado. A última revisão grava
status/mês/ano ao terminar; modo/diagnóstico não apagam esse arquivo. O código
antigo sed_auto_action_status mantém seus valores para execução; a UI histórica
usa arquivo separado. Desativação limpa os três campos novos. Não migra data
fictícia para resultado antigo; mostra ausência de registro nesta versão.

As mensagens atuais são exclusivas por prioridade: default, filas, construção
pausada, construtor conhecido; sem essas guardas, informa que faltam avaliar os
candidatos. Não amplia cobertura das flags de terceiros nem modifica a política
fiscal ou a reconciliação de projetos. Agendamento continua days=23 relativo.

77 testes aprovados, com quatro novos de painel/histórico: agenda antes da
primeira execução, consulta sem revisão, motivo live exclusivo, arquivo
preservado por modos/refresh, virada de ano, limpeza e evento registrando novo
resultado. Validação estática contra jogo, geração e pacote passaram. Nenhum
jogo foi iniciado; passagem de tempo e textos novos continuam sem prova na
engine. Não foi cobrado teste adicional do jogador.

Instalada 0.5.2 sem jogo em execução; backup `mod_0.5.1_20261109_115813_269189`.
13 outputs conferidos byte a byte com ZIP/gerador; load order preservado.


## Limite mensal persistente da execução automática 0.5.3

A auditoria encontrou limite apenas por chamada de revisão. Criada a guarda
sed_auto_month_limit_reached, comparando year×12+month atuais com o marcador
sed_auto_last_attempt_month. Os efeitos registram a tentativa antes de chamar
construção, somente em Automático. A validação é feita também no efeito mutante;
chamadas repetidas ficam bloqueadas após a primeira, mesmo se a fila esvaziar.
Não altera o conjunto de tipos do dispatcher: setor continua só manual.

A política é conservadora: uma tentativa por mês, incluindo inclusão recusada
ou não confirmada. Revisões sem candidato ou bloqueadas antes de tentar não
consomem o limite. Assistido pode aprovar explicitamente sob suas guardas,
sem consumir/apagar a marca automática. No mês seguinte, a comparação usa o
calendário vivo; a data antiga do painel não mantém o bloqueio.

Mudança intencional no contrato de limpeza: preserva schema e um único mês de
segurança após desativar. Demais indicadores, preferências, histórico de revisão
e pendências continuam sendo removidos. PERSISTENT_VARIABLES torna a exceção
explícita; o validador rejeita a remoção da proteção e retenções não declaradas.
Interface ganhou status 16 e motivo atual de limite, após default e antes das
filas. Status antigos conservados. Registro não reconstrói todas as tentativas
anteriores ao upgrade. Save/reload não foi testado na engine.

81 testes aprovados (77 anteriores + quatro novos), com os dez efeitos,
reativação, mudanças de modo, fila vazia, falha consumindo limite, aprovação
manual permitida, virada de ano sem refresh e validador recusando limpeza da
marca. Casos existentes de revisão bloqueada/sem candidato verificam que a
marca não é criada. São testes de scripts no harness, não execução da engine.

Geração, validação estática e pacote passaram. Instalada 0.5.3 sem jogo em
execução; backup `mod_0.5.2_20261109_121259_782337`.
13 outputs conferidos byte a byte; load order preservado. Não houve teste
gráfico nem save/reload para essa proteção.

## Proteção de infraestrutura — 0.5.4

Produtores dos oito bens atendidos e setores de construção exigem saldo atual
de infraestrutura maior ou igual a zero. A aprovação revalida essa condição;
um cartão antigo não autoriza expansão se o estado entrar em déficit.
Ferrovias mantêm a elegibilidade em déficit para tratar esse gargalo.
Cartões mostram o saldo ao vivo e o bloqueio, e os detalhes contam rejeições
por infraestrutura separadamente, respeitando a prioridade dos demais motivos.

84 testes automatizados aprovados: incluem invalidação de cartões antigos,
limite zero, exceção ferroviária, escolha de outro estado pelo Automático e
contadores sem dupla contagem. Validação estática contra os arquivos locais
1.15.0 aprovada. Isso não verifica execução na engine, save/reload ou campanha.
A guarda considera déficit atual, sem projetar consumo do próximo nível nem
reservar capacidade para projetos concorrentes. Reconciliação completa das
filas e planejamento fiscal incremental continuam pendentes.

Instalação local 0.5.4: jogo fechado, backup `mod_0.5.3_20261109_122756_131472`, 13 arquivos conferidos com o pacote; configuração de carregamento preservada.


## Detecção de opções independentes do Supply Chain — 0.5.5

O Automático suspende tentativas quando encontra uma das configurações
`zw_var_more_construction_sectors`, `zw_var_scsab_construct_railway` ou
`zw_var_scsab_construct_power_plant`, mesmo sem `zw_var_expand_building`.
A presença configura a opção; os botões do mod externo removem a variável ao
desligá-la. Fonte: Supply Chain instalado, `zw_scsab_buttons.txt:90–153,
383–479, 483–547`; efeitos 1, 3 e 4, limites iniciais; JE, pulso mensal.

Política deliberadamente conservadora: detecta configuração, sem reproduzir
tecnologia, calendário, orçamento ou seleção estadual do outro executor.
Pode suspender o Director mesmo quando o outro mod não construiria neste mês.
Não confirma que o diário externo esteja ativo. Não escreve em variáveis
externas. Assistido preserva aprovação explícita com suas guardas existentes.
Executor, resultado 13 e painel ao vivo consultam um único trigger
`sed_competing_builder_configured`, evitando divergência entre UI e execução.

86 testes passam, incluindo opções independentes com cadeias desligadas,
bloqueio sem consumir o mês, liberação ao remover a opção, painel ao vivo e
aprovação Assistida sem alterar configuração externa. Validação estática
contra o jogo local 1.15.0 aprovada. Pacote 0.5.5 gerado; não instalado nesta
etapa. Instalação permanece 0.5.4. Nenhum jogo foi iniciado.
As opções de administração, reconciliação de projetos, save/reload e política
fiscal incremental continuam pendentes. Não cobrar novo teste do jogador agora.


## Administração do Supply Chain — 0.5.6

A guarda de configuração agora inclui `zw_var_scsab_gov_admin` e
`zw_var_scsab_gov_admin_for_tax`. A primeira habilita a rotina geral, que pode
reagir à burocracia negativa mesmo sem meta institucional; a segunda habilita
uma rotina tributária independente. `zw_var_scsab_gov_admin_for_institution`
isolada não habilita nenhuma dessas rotinas e não bloqueia o Director.

Fontes locais: Supply Chain instalado, efeito
`common/scripted_effects/zw_scsab_effects_2_gov_admin.txt:1–185`, botões
`common/scripted_buttons/zw_scsab_buttons.txt:215–383` e pulso
`common/journal_entries/zw_scsab_je.txt:84–126`. O primeiro limite exige a
configuração geral; o alvo institucional só altera o cálculo interno.
O efeito tributário exige sua própria configuração e tecnologia; seleciona
estados com capacidade tributária insuficiente. Os botões removem as opções
ao desligar. A política do Director detecta configuração, sem reproduzir
calendário, tecnologia, burocracia, orçamento ou seleção estadual externos.
Isso pode suspender o Automático mesmo sem obra externa naquele mês.
Não comprova ativação do diário externo nem resolve reconciliação da fila.

87 testes aprovados: os casos das opções independentes agora incluem as duas
configurações administrativas; novo cenário confirma que uma meta institucional
isolada não bloqueia nem é alterada. Painel, resultado 13 e guarda de execução
continuam usando o mesmo trigger. Validação estática local 1.15.0 e pacote
0.5.6 aprovados. Nenhum jogo iniciado; engine e save/reload não verificados.
Pacote não instalado: instalação local permanece 0.5.4.


## Revalidação no efeito de construção — 0.5.7

Os dez triggers de aprovação agora consultam `sed_auto_executor_safe` quando
o modo é Automático. Antes, somente o dispatcher checava fila pública vazia,
construção não pausada e configurações concorrentes; o efeito mutante
revalidava apenas elegibilidade, jogador/ativação, default, fila privada e
limite mensal. Chamadas diretas aos efeitos podiam escapar dessas três guardas.
Agora as mesmas condições são exigidas também pelo efeito que chama
`start_building_construction`, sem nova primitiva ou novo tipo no dispatcher.
Setor de construção continua fora da seleção automática. Assistido mantém
aprovação explícita sob as guardas anteriores, inclusive com fila pública,
construção pausada ou outro executor configurado. Isso não autoriza operações
novas na interface nem transforma aprovação em garantia fiscal.

88 testes aprovados. A nova matriz percorre dez ações e doze bloqueios,
valida elegibilidade antes da mudança e chama o efeito após a mudança.
Confere ausência de inclusão, marca mensal e pendência; depois verifica o
comportamento Assistido. Os testes mensais anteriores continuam aprovados.
É simulação dos scripts gerados, sem reprodução de concorrência na engine.
Validação estática local 1.15.0 e pacote 0.5.7 aprovados. Nenhum jogo iniciado;
instalação permanece 0.5.4. Reconciliação de projetos, persistência em save e
planejamento fiscal incremental continuam pendentes.


## Autorização explícita do modo no efeito — 0.5.8

Os dez efeitos mutantes exigem `sed_execution_mode_permits_approval` no país:
Assistido sem Automático, ou Automático com `sed_auto_executor_safe`.
Qualquer marca Manual impede a aprovação, inclusive em combinação inconsistente
de modos; ausência de modo também bloqueia. Antes, a condição aceitava qualquer
modo não automático, deixando chamadas diretas no Manual passarem. A interface
já exigia Assistido; a correção fecha o contrato dos efeitos internos sem
acrescentar execução, primitiva ou tipo ao dispatcher. Diagnóstico continua
podendo inicializar o modo padrão de saves antigos conforme regra existente.

90 testes aprovados. Novos cenários cobrem dez ações em Manual, sem modo e com
marcas conflitantes contendo Manual, sem construção, pendência ou consumo de
mês; cobrem também mudança de Assistido para Manual após análise e retorno ao
Assistido. O harness ganhou avaliação de bloco AND, usado para exigir Assistido
sem Automático. A sintaxe existe nos triggers vanilla locais de 1.15.0
(`common/scripted_triggers/00_scripted_triggers.txt:50`). Validação estática,
geração e pacote 0.5.8 aprovados. Isso não comprova execução/persistência na
engine. Nenhum jogo iniciado; instalação local permanece 0.5.4.
Reconciliação por projeto, save/reload e planejamento fiscal continuam pendentes.

## Entrega local 0.5.8 — 2026-11-09

Instalada com jogo fechado. Backup:
`sed_backups/mod_before_0.5.8_20261109_212722_719786`.
Os 13 outputs foram conferidos byte a byte; `content_load.json` preservado.
A pasta antiga foi retirada antes de gerar a nova, sem arquivos remanescentes.
Isso atualiza as notas anteriores de instalação 0.5.4; engine e save/reload
continuam sem teste nesta etapa.


## Explicação das opções externas — 0.5.9

O painel Automático lista ao vivo as oito opções externas detectadas, com
nomes de mod e função, mesmo quando default, limite mensal, pausa ou fila
aparecem como primeiro bloqueio. Sem opções, em Manual/Assistido ou desativado,
a lista fica oculta. O texto explica que configuração ligada já suspende o
Director sem esperar obra, e orienta usar Assistido ou ajustar o outro mod.
Não altera opções externas, regras econômicas, dispatcher ou histórico.
Uma tabela no gerador alimenta guarda, linhas e traduções para manter cobertura
coerente. A meta institucional isolada continua fora da detecção.

91 testes aprovados, incluindo cada opção isolada, todas juntas, retirada ao
vivo, coexistência com fila ocupada, modos, desativação e leitura sem mutação.
Geração, validação estática local 1.15.0 e pacote aprovados. Layout novo não foi
verificado na engine. Preparada enquanto o jogador testa: NÃO instalada;
a instalação usada pelo jogador permanece 0.5.8. Não atualizar durante a
sessão nem interpretar capturas da 0.5.8 como confirmação da lista nova.


## Planejamento e coordenação 0.6.0

Direção confirmada pelo jogador em 09/11. O Director deve definir objetivos e
ativar somente caminhos necessários de Economy Advisor e Supply Chain. A versão
implementa plano nacional inicial, três prioridades globais e adaptadores
reversíveis de sete opções. Selecionar Automático guarda as opções de ferramentas
detectadas, escolhe executor por objetivo e impede construção própria em paralelo.
Sair para Manual/Assistido, liberar ou desativar restaura presença e valores.

Plano cobre infraestrutura, oferta e ausência de tipos de produtor atendidos,
capacidade, crescimento/diversificação, burocracia, tributos e energia local.
A classificação fiscal usa saldos, quatro semanas de despesas fixas em ouro e
dívida até 75% do crédito. São parâmetros iniciais escolhidos na implementação,
com testes por escala. Calibração em campanha e custo incremental ficam abertos.

A seleção interna do Advisor permanece sob sua política própria. O adaptador
controla autorização, sem transmitir estado/prédio. Os executores externos
conservam agendas e quantidades. O resultado 18 registra orientação aplicada.
ARoAI construtor detectado suspende a delegação. Autoexpansões nativas ainda
têm cobertura pendente. Impostos/gastos próprios, projeção futura de emprego e
insumos, reconciliação por projeto e estratégia plurianual continuam parciais.

Código em tools/planning.py e tools/coordination.py, integrado ao gerador.
O validador admite as sete opções externas apenas nos dois efeitos adaptadores
com guardas de jogador e coordenação ativa. Testes negativos cobrem escrita
fora desse limite. A política, fontes e roteiro estão em PLANNING.md e STATUS.md.
O relato dos testes anteriores foi pouca mudança visível enquanto outros mods
construíam. Ainda falta confirmação dos novos fluxos na engine e save/reload.

## Entrega local 0.6.0

Instalada com jogo fechado. Os 13 outputs conferem byte a byte com o gerador,
e content_load.json foi preservado. Backup em
`sed_backups/mod_before_0.6.0_20261109_220347_442062`.
115 testes sintéticos aprovados, geração atual, validação estática contra
Victoria 3 1.15.0 e ZIP aprovados. A instalação substitui a 0.5.8.
Selecionar Automático novamente aplica os adaptadores em save da 0.5.x.
Coordenação, novo layout e save/reload ainda aguardam verificação na engine.

Conferência final da 0.6.0 inclui ocultação das listas vazias do plano,
115 testes aprovados e reinstalação dos 13 outputs com jogo fechado.
Backup dessa conferência em
`sed_backups/mod_before_0.6.0_20261109_220620_787220`.
O backup inicial `mod_before_0.6.0_20261109_220347_442062` conserva a 0.5.8.

## Objetivo e orçamento do Advisor 0.6.1

Integração de quatro opções verificadas do Advisor, além das sete de construção.
Ao escolher Advisor, o Director aplica crescimento, padrão de vida quando bens
essenciais lideram o plano ou retorno ao tesouro quando a dívida positiva chega
a 50% do crédito. A orientação financeira tem prioridade. Crescimento/social
usam orçamento equilibrado do Advisor, com sua reserva de doze semanas. Retorno
ao tesouro preserva reservas. A opção de endividamento do Advisor fica desligada
enquanto ele recebe essa orientação. O limiar de 50% é uma decisão inicial da
implementação com calibração em campanha pendente.

Snapshot e restauração incluem presença e valores das quatro opções. Migração
de uma coordenação 0.6.0 ativa captura antes da primeira escrita. Liberar antes
de capturar preserva as opções. Delegação ao Supply Chain mantém a política do
Advisor. A autorização de escrita do validador cobre apenas as onze opções nos
dois efeitos adaptadores existentes.

120 testes aprovados, geração atual, validação estática e ZIP aprovados.
A integração nova ainda aguarda confirmação de engine e save/reload. Fontes e
política em PLANNING.md. Instalação e publicação registradas na entrega abaixo.

Entrega local 0.6.1 instalada com jogo fechado, 13 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.1_20261109_222628_869777`.

## Construção financiada por reservas 0.6.2

A guarda fiscal 1–4 exigia saldo semanal não negativo, então a coordenação
parava sempre que um déficit operacional coberto por reservas aparecia — mesmo
com ouro suficiente para o horizonte do Advisor. A 0.6.2 acrescenta a
classificação 5, aplicada antes de 2–4: receita fixa não negativa, déficit total
observado, sem dívida e ouro cobrindo doze semanas de despesas fixas mais 26
semanas desse déficit. A guarda escala com as leituras e não aprova sem ouro.

`sed_coord_fiscal_safe` combina a guarda antiga com a classificação 5 quando o
Advisor foi detectado. A entrada de `sed_coord_sync` e o objetivo de
crescimento/diversificação usam essa guarda. Os ramos do Supply Chain mantêm
`sed_auto_fiscal_safe` cada um, de modo que a classificação 5 delega apenas ao
Advisor. Somente as classificações 3 e 4 substituem o objetivo por
estabilização; a 5 permite crescimento.

Também corrigi o limite automático mensal: a comparação usava aritmética
embutida na igualdade (`var:x = { value = year ... }`), que a engine não avalia.
Agora compara com o script value `sed_live_month_key`, e o validador rejeita
essa forma em qualquer igualdade `var:`. A variável não usada
`sed_supply_action_status` saiu do registro de limpeza.

Validação: **124 testes sintéticos aprovados**, geração atual,
`build_mod.py --check`, validação estática sem caminho do jogo e
`git diff --check`. Nenhum jogo foi iniciado e a classificação 5 ainda não foi
observada em campanha.

Entrega local 0.6.2 instalada com jogo fechado, 14 outputs conferidos
byte a byte e content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.2_20261109_235909_180351`. ZIP em
`dist/smart-economy-director-0.6.2.zip`. A verificação da classificação 5,
do novo limite mensal e da delegação somente ao Advisor segue pendente na engine.

## Produtores alternativos 0.6.3

O catálogo tratava cada bem como um único prédio produtor. Um país com fazendas
de milho ou arroz, por exemplo, recebia "sem base produtiva" para cereais
mesmo com escassez e produtor operante — caso provável no Haiti. Verifiquei nos
arquivos vanilla 1.15 que cinco fazendas produzem cereais e que a fazenda de
gado produz tecido pelos métodos de ovelhas.

Cada bem agora aceita uma lista de variantes. O filtro de elegibilidade é uma
disjunção de triggers por prédio; a aprovação enfileira o primeiro produtor
elegível na ordem declarada; o diagnóstico de produtor ausente e as contagens
de rejeição usam as mesmas variantes. A correção também completou os métodos
das fazendas de trigo (fertilização e farinha de arenque) e de arroz.

O validador passou a aceitar todos os prédios declarados em cada efeito de
aprovação, exigindo que nenhuma construção ocorra fora deles. 126 testes
sintéticos aprovados, geração atual, validação estática com o jogo 1.15,
`git diff --check` e pacote aprovados.

Entrega local 0.6.3 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.3_20261110_002209_786280`. ZIP em
`dist/smart-economy-director-0.6.3.zip`. As novas combinações ainda não foram
observadas em campanha nem na engine.

## 2026-11-10 — Metas industriais anuais 0.6.4

Objetivo: definir metas econômicas a partir da observação, em vez de apenas
reagir à escassez do mês corrente, sem criar candidatos fora dos filtros.

O plano passou a contar meses consecutivos de escassez de mercado por bem
estratégico (`sed_<bem>_short_months`). No terceiro mês, o Director grava a meta
anual (`sed_<bem>_meta_year`) correspondente ao ano civil. Enquanto a meta vale,
o bem recebe 25 pontos adicionais na pontuação e uma linha própria no diário
("Meta industrial anual: ampliar a oferta de ..."). A meta expira em janeiro;
se a falta continuar, os três meses seguintes a reativam. Ela não cria
candidato e não dispensa trabalhadores, insumos, fila, infraestrutura,
permissão ou proteção fiscal, nem altera objetivo macro, impostos, gastos ou
orçamento externo.

O texto do setor ausente também passou a listar todos os produtores verificados,
em vez de nomear apenas o prédio principal. Três meses e 25 pontos são decisões
desta implementação, sem calibração em campanha.

129 testes sintéticos aprovados (três novos: ativação no terceiro mês e
expiração anual, prioridade sobre falta mais aguda mas recente, limpeza ao
desativar). Geração atual, validação estática contra Victoria 3 1.15 e
`git diff --check` aprovados.

Entrega local 0.6.4 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.4_20261110_005319_526047`. ZIP em
`dist/smart-economy-director-0.6.4.zip`. A meta ainda não foi observada na
engine nem em campanha.

## 2026-11-10 — Política fiscal própria 0.6.5

Objetivo: agir sobre a receita, não apenas ler a situação fiscal e bloquear
construção. O Director passa a ajustar o nível de imposto, preservando o
controle reversível já usado nas opções externas.

No Automático, `sed_apply_fiscal_policy` move um passo por revisão mensal:
sobe em cautela, crise ou default (até `very_high`) e desce com classificação
1/5, superávit, sem dívida e ouro cobrindo doze semanas de despesas fixas (até
`low`). O nível original é guardado em `sed_tax_level_saved` na primeira
alteração e restaurado por `sed_restore_fiscal_policy` ao sair do Automático ou
desativar. Mudanças manuais durante o Automático são substituídas na revisão
seguinte; Manual e Assistido não alteram impostos.

Fontes vanilla 1.15: efeito `set_tax_level` em
`common/effect_localization/00_country_effects_loc.txt:44`, trigger `tax_level`
em `common/trigger_localization/00_trigger_localization.txt:3242` e níveis
ordenados em `common/history/countries/hai - haiti.txt:25` e
`common/scripted_progress_bars/00_sepoy_mutiny_progress_bars.txt:250,271`.

O validador autoriza `set_tax_level` somente nos dois efeitos fiscais, com
valores do enum, e exige guarda explícita de modo Automático. Salários,
despesas, impostos de consumo, leis e dívida continuam fora do controle.
Passo único, piso `low` e teto `very_high` são decisões iniciais sem calibração.

132 testes sintéticos aprovados (três novos: subida e restauração por troca de
modo, teto e restauração ao desativar, descida apenas com saúde fiscal).
Geração, validação estática contra Victoria 3 1.15 e `git diff --check`
aprovados.

Entrega local 0.6.5 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.5_20261110_010449_284523`. ZIP em
`dist/smart-economy-director-0.6.5.zip`. Nada observado na engine; a aceitação
de `set_tax_level` em scripted effects e o efeito real na receita seguem sem
confirmação.

## 2026-11-10 — Salários do governo 0.6.6

Objetivo: começar o controle de gastos pelo salário civil do governo, com a
mesma reversibilidade dos impostos. Em crise ou default, o Director desce um
nível (piso `low`); com classificação 1/5, superávit, sem dívida e doze semanas
de despesas fixas em ouro, sobe um nível (teto `medium`). Cautela, Manual e
Assistido não alteram salários. O nível original é guardado em
`sed_gov_wage_saved` e restaurado ao sair do Automático ou desativar.

Fontes vanilla 1.15: `set_government_wage_level` em
`common/effect_localization/00_country_effects_loc.txt:279`, trigger
`government_wage_level` em
`common/trigger_localization/00_trigger_localization.txt:3269` e níveis em
`common/static_modifiers/00_code_static_modifiers.txt:366–393`. O efeito não é
usado por scripts ou históricos vanilla, apenas pela localização; a aceitação
na engine é a principal incerteza, maior que no `set_tax_level`.

O validador autoriza `set_government_wage_level` somente em
`sed_apply_wage_policy` e `sed_restore_wage_policy`, com valores do enum, e
exige guarda de modo Automático. Salários militares, despesas, subsídios e
impostos de consumo seguem fora do controle.

135 testes sintéticos aprovados (três novos: corte até o piso e restauração,
subida até o teto e restauração ao desativar, ausência de mudança em cautela).
Geração, validação estática contra Victoria 3 1.15 e `git diff --check`
aprovados.

Entrega local 0.6.6 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.6_20261110_011134_926784`. ZIP em
`dist/smart-economy-director-0.6.6.zip`. Nada observado na engine.

## 2026-11-10 — Livro de resultados por alvo 0.6.7

Objetivo: medir o que acontece depois da aprovação, em vez de registrar apenas
que a obra entrou na fila. Cada pedido confirmado dos oito bens estratégicos
guarda no estado o nível do produtor antes da fila (`sed_<bem>_intent_level`) e
a variante enfileirada (`sed_<bem>_intent_variant`). A confirmação incrementa
`sed_<bem>_intents`.

Quando o pedido sai da fila, o nível atual é comparado à linha de base: nível
maior conta `sed_<bem>_completed`, igual ou menor conta `sed_<bem>_abandoned`.
`sed_<bem>_result` (1/2) e `sed_<bem>_result_month` guardam o último desfecho.
O plano exibe pedidos, concluídos e abandonados somente após o primeiro pedido.

A conclusão é inferida por fila e nível, não por identidade de projeto;
cancelamento seguido de obra externa no mesmo estado/prédio pode distorcer a
contagem. Ferrovia e setor de construção continuam sem registro. A captura usa
`b:<prédio>.level` como valor de script, forma presente no Advisor instalado
(`advisor_core_values.txt:1040`; `:1579–1580`), além das comparações de nível
já usadas pelo Director.

136 testes sintéticos aprovados (um novo: linha de base e variante, conclusão
por nível maior, abandono por fila vazia sem novo nível e acumulação de dois
pedidos). Geração, validação estática contra Victoria 3 1.15 e
`git diff --check` aprovados.

Entrega local 0.6.7 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.7_20261110_012225_626750`. ZIP em
`dist/smart-economy-director-0.6.7.zip`. Nada observado na engine: a leitura de
`b:<prédio>.level` em valor e a ordem entre conclusão, cancelamento e limpeza
mensal seguem sem confirmação.

## 2026-11-10 — Livro completo 0.6.8

Objetivo: estender o livro de resultados a ferrovia e setor de construção,
fechando os dez tipos de ação do Director. A aprovação grava
`sed_railway_intent_level` ou `sed_construction_intent_level` no estado e a
confirmação incrementa `sed_<tipo>_intents`. Quando o pedido sai da fila, nível
maior conta como concluído; nível igual ou menor, ou prédio ausente, como
abandonado. `sed_<tipo>_result` (1/2) e `_result_month` guardam o último
desfecho, e o plano exibe pedidos/concluídos/abandonados após o primeiro.

A conclusão continua inferida por fila e nível, sem identidade de projeto.
Desativar limpa os marcadores estaduais e os contadores nacionais; a limpeza
foi corrigida para incluir os marcadores dos oito bens e as escolhas ignoradas,
que o gerador havia deixado fora do bloco após a mudança de formato.

137 testes sintéticos aprovados (um novo: ferrovia concluída e setor
abandonado no mesmo cenário). Geração, validação estática contra Victoria 3
1.15 e `git diff --check` aprovados.

Entrega local 0.6.8 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.8_20261110_013400_273582`. ZIP em
`dist/smart-economy-director-0.6.8.zip`. Nada observado na engine.

## Revisão da continuação 0.6.9

Revisados os commits 03aa0a6 a d0fca76. Metas contavam chamadas como meses e
políticas fiscais podiam executar múltiplos passos no mesmo mês. A amostragem
agora usa meses de calendário consecutivos observados. Histórico sem data de
amostragem é reiniciado na primeira leitura. Imposto e salário civil têm
marcadores mensais persistentes independentes, preservados em troca de modo e
desativação. O imposto para no piso baixo e marcas conflitantes com Manual ou
Assistido impedem alterações.

O livro acompanha a variante solicitada e verifica presença e linha de base do
produtor. Uma fila de outro produtor do mesmo bem deixa de reter o pedido.
Pedidos antigos sem variante conservam a aproximação anterior. O livro continua
inferindo resultados por nível/fila e não identifica projetos.

146 testes aprovados, geração e validação estática local 1.15.0 aprovadas.
Uma inicialização isolada de três minutos com os mods da campanha chegou ao
menu, sem erros atribuídos ao Director nos logs rotacionados. Leitura dos
efeitos de imposto e salário aceita na engine. Mudanças em campanha e
save/reload ainda aguardam observação. O jogador ofereceu capturas para essa
etapa. Detalhes e evidências em REVIEW_2026-11-10.md.

PERSISTENT_VARIABLES passa a conter schema, limite de construção e os dois
marcadores de ajuste fiscal. Snapshots continuam sendo restaurados e removidos
na saída. Instalação e publicação da 0.6.9 registradas na entrega abaixo.

Entrega 0.6.9 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.9_20261110_101047_639382`.
146 testes aprovados, validação estática local e pacote aprovados.

## 2026-11-10 — Coordenação por objetivo, 0.6.10

Capturas do jogador confirmaram revisão automática de outubro a dezembro de
1837 no Uruguai. No teste otomano, o objetivo de capacidade tributária coexistia
com orientação geral de crescimento ao Advisor. Obras novas foram observadas,
mas sua autoria e relação causal com o Director não foram comprovadas.

Administração, tributação e energia agora exigem os adaptadores específicos do
Supply Chain. Sem ferramenta disponível ou sem a proteção fiscal específica,
a coordenação suspende novas opções e mostra execução pendente. O Advisor
continua recebendo orientação geral para os demais objetivos compatíveis.
A rotina específica de setores de construção tem preferência sobre o Advisor.
O diagnóstico tributário só considera estados incorporados. Isso não altera os
filtros internos do Supply Chain, incluindo sua seleção de estados.

A última revisão distingue delegação, falta de executor específico, bloqueio
fiscal e conflito com ARoAI. Snapshots e restauração permanecem cobertos por
regressões. Cinco testes novos, 151 testes aprovados no total, geração e
validação estática contra os arquivos locais 1.15 aprovadas. A UI e as novas
transições ainda aguardam confirmação na campanha. A fila nativa e os níveis
fiscais foram vistos em capturas anteriores, sem comprovação causal das mudanças.

## 2026-11-10 — Política de delegação e histórico fiscal

O Director guarda e controla três opções adicionais do Supply Chain. Expansões
ficam restritas a estados incorporados pelas opções verificadas
`zw_var_develop_incorporated_states` e `zw_var_ip_incorporated`. A meta de
instituições `zw_var_scsab_gov_admin_for_institution` fica suspensa durante a
coordenação para que administração responda à burocracia atual. Os valores e
a ausência originais são restaurados ao sair do Automático ou desativar.
Snapshots são capturados uma vez antes da primeira alteração, inclusive em
coordenações salvas por versões anteriores. Sair de um save antigo sem uma nova
sincronização preserva as opções ainda não capturadas.

Limites numéricos de administração, tributação, energia, ferrovia e setores
passam a um nível por local selecionado pela rotina externa. A soma nacional
pode superar um nível. Advisor e cadeias gerais mantêm a semântica anterior.
Essa escolha é um ritmo inicial conservador, ainda sem calibração de campanha.

O painel informa a agenda verificada no `zw_scsab_je.txt` instalado. A rotina
tributária roda nos meses de script 5/11 (junho/dezembro), e setores em 1/7
(fevereiro/agosto). Agenda e algoritmo continuam pertencendo ao Supply Chain.

Impostos e salários civis mostram o último comando do Director, com mês,
ano e níveis anterior/solicitado. Esse registro comprova a passagem pelo efeito,
mas o resultado deve ser conferido no orçamento. Reavaliações sem alteração
não criam histórico; restauração de modo não reescreve o último comando
automático; desativar remove o histórico e preserva as travas mensais.

158 testes sintéticos aprovados, gerador e validação estática local aprovados.
A nova interface, o efeito das opções externas e save/reload continuam pendentes
do teste conjunto do jogador. Nenhuma nova inicialização de engine nesta etapa.

## 2026-11-10 — Acompanhamento de gargalos na fila

Quando não há outra expansão elegível, o plano mantém o objetivo de
infraestrutura ou oferta se detectar expansão relacionada enfileirada.
Para oferta, exige escassez atual, estado incorporado e método de produção
verificado para o bem, incluindo produtores alternativos. Estados ignorados
pelo jogador não mantêm essa espera. Para administração, tributação e energia,
a espera exige expansão correspondente em estado incorporado afetado pelo
problema. Crise fiscal mantém precedência sobre acompanhamento de obra.

A coordenação mostra executor 10 e resultado mensal 20 enquanto aguarda.
Nesse estado, as opções externas de novas obras permanecem suspensas.
Cancelamento, conclusão, fim da escassez ou surgimento de outra prioridade
provocam reavaliação pelos filtros normais. A detecção usa nível atual e nível
após fila, sem atribuir autoria, identidade ou impacto previsto ao projeto.

A espera é conservadora. Uma obra relacionada pode suspender a autorização
nacional da rotina enquanto não houver outra prioridade elegível. A versão
acompanha expansões de prédios reconhecidos pelas leituras existentes; novos
prédios ainda não expostos nessas leituras podem ficar fora da detecção.

165 testes sintéticos aprovados, geração e validação estática local aprovadas.
Sete novas regressões cobrem fila, cancelamento, resolução, prioridade
alternativa, métodos produtivos, localização da energia e precedência fiscal.
Novas mensagens e transições ainda aguardam o teste conjunto em campanha.

## 2026-11-10 — Avaliação econômico-militar

O briefing inclui financiamento do exército, indústria bélica e marinha.
A nova avaliação é atualizada pela entrada normal do plano nacional e lê
`military_expenses`, `military_expenses_share` e `is_at_war`, verificados nos
scripts vanilla locais. A participação é apresentada como indicador do jogo,
sem presumir denominador diferente do fornecido pela engine.

Armas leves, artilharia, munição, navios de guerra à vela e blindados são
monitorados no mercado. Avisos exigem demanda positiva e escassez. Um mercado
compartilhado pode ter demanda de outros países; esses sinais ainda não
identificam o consumo das forças nacionais.

Diretrizes distinguem observar demanda, sustentar a força atual, investigar
abastecimento, estabilizar orçamento e estudar modernização. A última exige
saldo positivo, guarda fiscal de expansão, ausência de dívida e doze semanas
de despesas fixas em reservas, sem escassez militar detectada. Esse limiar é
inicial e não estima o custo de uma modernização específica. Crise/default ou
saldo operacional negativo têm precedência. Sem despesa militar positiva,
a escassez compartilhada não cria inferência de necessidade nacional.

A avaliação é informativa e não muda a seleção dos executores, recrutamento,
PMs, salários militares ou composição das forças. Construção militar dirigida,
consumo nacional, prontidão e coordenação do recrutador permanecem pendentes.

172 testes sintéticos aprovados. Sete novas regressões cobrem atualização
normal, escassez, ausência de demanda, limites fiscais, resolução e limpeza.
Geração, ZIP e validação estática local passaram. Novos dados e layout ainda
exigem observação na campanha, junto do roteiro acumulado.

## 2026-11-10 — Expansões militares elegíveis

O catálogo passa de oito para onze bens com armas leves, artilharia e munição.
Doze métodos ativos e seus outputs foram conferidos no `01_industry.txt`
vanilla local. Os novos alvos reutilizam elegibilidade, aprovação, limite
mensal, fila, histórico de resultado, ignorar/restaurar e metas anuais.

Candidatas militares exigem despesa militar positiva, demanda de mercado
positiva e escassez atual. O produtor deve existir, produzir o bem pelo método
ativo, estar em estado incorporado, com ocupação mínima de 80%, sem falha de
contratação, falta de insumos, déficit de infraestrutura ou expansão na fila.
Isso ainda usa despesa nacional como sinal parcial de necessidade. Demanda
do mercado compartilhado não identifica precisamente consumo das tropas.

A pontuação recebe bônus de 20 durante guerra. A regra é inicial e não foi
calibrada em campanha. Prioridades civis continuam concorrendo pela pontuação;
crise fiscal continua prevalecendo no objetivo macro e na proteção automática.

Assistido permite aprovar um nível de produtor militar elegível. Automático
próprio aplica os limites fiscais e de fila já existentes. Com coordenação
externa ativa, o Director preserva a delegação geral e não executa em paralelo.
O Advisor/Supply Chain ainda seleciona os próprios projetos, sem garantia de
executar o alvo militar específico. Navios continuam no diagnóstico; nova
fábrica, PMs das tropas e recrutamento seguem pendentes.

180 testes sintéticos aprovados. As oito novas regressões militares cobrem
aprovação, demanda, trabalhadores, insumos, ranking, proteção fiscal,
coordenação e livro de resultados. Geração, ZIP e validação estática local
aprovados. Inclusão real de obra e layout ainda exigem teste de campanha.

## 2026-11-10 — Prioridade executada na coordenação

A coordenação agora escolhe o Director (executor 11) quando o objetivo de
oferta tem uma primeira prioridade elegível e passa pela guarda fiscal
normal. As sete opções verificadas de construção externa são suspensas antes
da execução. Infraestrutura e demais objetivos mantêm as rotas anteriores;
a delegação geral permanece para casos sem alvo direto viável.

O modo apenas seleciona a rota; a inclusão ocorre na revisão automática.
`sed_auto_run_direct` é compartilhado pelo Automático próprio e pelo novo
executor coordenado. Exige jogador, mod habilitado, Automático exclusivo,
filas pública e privada vazias, construção ativa, proteção fiscal e limite
mensal. Conflito com ARoAI ou outro switch conhecido impede execução.
A exceção de coordenação exige executor 11, objetivo 2 e primeira prioridade
atualmente elegível. Cada aprovação também exige o rank 1 daquele tipo/estado
quando a coordenação está ativa. Um candidato de outro tipo no mesmo estado
não pode aproveitar a autorização.

O resultado mensal registra a inclusão observada na fila, falha, bloqueio de
fila ou limite mensal. Continua sendo uma tentativa por mês; falha consome a
tentativa. A política de restauração permanece intacta. Obras existentes,
construtores desconhecidos e autoexpansões nativas continuam fora do controle.
A guarda ainda usa a política fiscal inicial, sem previsão completa de custo
incremental, trabalhadores e insumos futuros.

189 testes sintéticos aprovados. Oito regressões exercitam execução direta,
restauração, limite, filas, revalidação, tipo/estado, finanças e ARoAI. Um teste
de validação adversarial rejeita autoridade ampliada, remoção da guarda e rank
menos restritivo. Validação estática e gerador aprovados. Inclusão real e UI
permanecem pendentes de campanha.

## 2026-11-10 — Controle do ritmo por reservas

O teste do jogador em março–maio de 1842 mostrou diagnóstico de ferro,
rejeição por expansão na fila e ocupação, acompanhamento de obra relacionada,
fim do aviso de escassez e retorno do objetivo para crescimento/diversificação.
A execução direta e a autoria da expansão ainda não foram comprovadas.
A leitura manual corrigiu uma divergência entre números registrados e a barra
atual do jogo. Leituras continuam representando snapshots.

Foi corrigida a sincronização após `sed_refresh_diagnostics`. O diagnóstico
atualiza o plano e, em coordenação ativa, reaplica a seleção de executor e as
opções autorizadas. Não enfileira obra, ajusta impostos/salários ou reescreve o
resultado arquivado da última revisão automática. Essa mudança pode alterar
as opções de construção externas durante o clique de diagnóstico.

Durante déficit financiado por reservas, níveis públicos já enfileirados
selecionam executor 12 e resultado 21. Novas opções externas ficam suspensas
nas revisões até a fila pública liberar. A fila privada sozinha não impõe essa
pausa. Com saldo não negativo, as rotas anteriores permanecem. O orçamento é
revalidado antes de liberar o Advisor; guardas de default e ARoAI prevalecem.
Obras existentes continuam; o mod não estima seu custo restante.

O painel mostra piso de doze semanas de despesas fixas, ouro acima desse piso,
cobertura em semanas do déficit atual e total exigido pela guarda de 26
semanas. Esses números explicam o limiar já existente, sem alterar seus fatores
ou prever custos incrementais. Casos de saldo zero e despesas negativas são
tratados para evitar divisão por zero e reservas mínimas negativas.

196 testes sintéticos aprovados. Sete regressões adicionais cobrem fila pública,
retomada, fila privada, sincronização sem execução/histórico alterado e contas
de reservas. Geração e validação estática local aprovadas. Novas transições e
layout ainda aguardam campanha.

## 2026-11-10 — Referência de materiais no executor direto

A proteção direta agora inclui referência conservadora de materiais para o
próximo projeto. Os quatro métodos de `13_construction.txt`, seus insumos,
pontos de construção e nove preços-base foram conferidos na instalação local.
O módulo `construction_budget.py` calcula materiais por ponto com preços-base
acrescidos de 75%, usando o maior custo entre métodos ativos dos setores.
O número de pontos é limitado pela capacidade nacional e pelo limite semanal
por projeto fornecido pelo jogo. Setor ativo com método desconhecido torna a
referência indisponível. Ausência de setores resulta em referência material
zero para a capacidade restante, sujeita às demais guardas.

A obra automática precisa de saldo cobrindo a referência semanal ou, sem
dívida, ouro cobrindo quatro semanas de despesas fixas mais 26 semanas da
diferença entre referência e saldo. As guardas fiscais anteriores continuam
obrigatórias. O cálculo é atualizado no plano, no executor direto e antes de
cada aprovação automática. Bloqueio de orçamento registra resultado 22 e
não consome tentativa. Assistido mantém aprovação explícita.

Esse cálculo é uma referência de estresse e pode superestimar o gasto. Ele
cobra todos os pontos potenciais pelo método ativo mais caro, inclusive quando
há capacidade gratuita ou métodos mistos. Não prevê duração, salários futuros,
subsídios, preços locais, modificadores de custo ou custos operacionais do
prédio concluído. Expansão de setores de construção ainda precisa de um modelo
separado de seu custo recorrente. Rotas externas continuam com seus orçamentos.

205 testes sintéticos aprovados. Nove regressões cobrem os perfis, capacidade,
limites de renda/reservas, dívida, método desconhecido, revalidação e limpeza.
A validação adversarial também verifica remoção da guarda de orçamento e da
atualização antes da execução. Geração e validação estática local aprovadas.
Referência e bloqueios precisam de calibração e observação em campanha.

## 2026-11-10 — Calibração da referência material

A referência da 0.6.17 podia aplicar o método ativo mais caro a pontos nacionais
que incluem construção gratuita. A origem da parcela gratuita é escalada pelo
PIB nos modificadores vanilla; não foi adotada uma dedução fixa de pontos.

A referência agora é limitada à soma de materiais dos setores existentes,
com seus níveis e ocupação atuais, mantendo preços-base acrescidos de 75%.
Cada estado soma os insumos de seu método reconhecido. A soma é recalculada em
cada leitura. O orçamento usa o menor valor entre essa soma e a referência
por pontos do próximo projeto. O limite semanal por projeto e as guardas
financeiras continuam iguais. A distribuição privada não introduz nova regra,
pois o executor direto já exige as duas filas vazias antes de construir.

Exemplo sintético com capacidade nacional 10 e um setor de madeira nível 1,
ocupação integral. Referência por pontos anterior de 17.500/semana passa a ser
limitada pelos materiais do setor em 3.500/semana. A reserva exigida para saldo
100 e despesas fixas 50 passa de 452.600 para 88.600. Esses valores são do
cenário de teste, sem confirmação de despesa real na campanha do jogador.

A referência continua sendo um cenário de materiais. Pode superestimar,
inclusive a parcela gratuita e os métodos mistos, e pode divergir do custo
real por preços locais, modificadores, emprego futuro e duração. Salários e
subsídios futuros permanecem fora do cálculo. O teto por ocupação atual não é
uma garantia contra crescimento futuro do consumo dos setores.

209 testes aprovados. Quatro regressões adicionais cobrem setor pequeno,
níveis/ocupação, soma entre estados e atualização, além do teto por projeto.
O harness suporta o iterador numérico de estados usado por scripts vanilla.
Geração e validação estática local aprovadas. Novos valores e comportamento
precisam de calibração em campanha.

## 2026-11-10 — Referência de mão de obra

As candidatas dos onze bens agora exigem reserva estimada de trabalhadores
para um nível adicional do produtor escolhido. O filtro aplica-se à
recomendação, aprovação Assistida e execução direta automática. Rotas externas
mantêm seus próprios critérios. Ferrovia e setor de construção entram no
cálculo de compromissos, mas seus filtros de candidatura permanecem anteriores.

A reserva demográfica usa população, referência de participação no trabalho
(0,25 mais modificador estadual, limitada entre 0,05 e 1), desemprego e metade
da participação de camponeses. Taxas são limitadas ao intervalo 0–1. Essa
fórmula é uma aproximação; não representa contagem direta de trabalhadores.
Não inclui qualificações, migração futura ou atração de empregados de outros
setores. Por isso pode rejeitar investimentos que seriam viáveis por esses
mecanismos.

A reserva é reduzida pelos compromissos conhecidos dos 18 tipos de prédio
registrados. Inclui vagas estimadas dos níveis atuais e os níveis adicionais
na fila, usando ocupação atual e coeficiente por nível. O coeficiente é a soma
dos maiores empregos de cada grupo de PMs vanilla do tipo, desconsiderando
economias de automação. O registro `data/labor_requirements.json` foi extraído
dos edifícios, grupos e métodos locais. Outros tipos de prédio e alterações
de emprego por outros mods continuam fora desse registro.

Os valores são calculados ao vivo nos filtros e registrados por estado na
leitura do plano. Cartões mostram reserva e compromissos; o diagnóstico de
rejeição tem motivo específico e coeficientes por produtor. Cancelar obra ou
liberar vagas muda a avaliação na próxima leitura. Desativar limpa snapshots.

217 testes sintéticos aprovados, incluindo oito regressões de referência,
fronteira, vagas, filas, camponeses, revalidação, variantes e limpeza. O harness
compara script values numéricos no lado esquerdo das condições. Geração e
validação estática local aprovadas. Novas leituras e bloqueios ainda aguardam
calibração e observação em campanha, junto do roteiro acumulado.

O jogador pediu testes apenas após mudanças relevantes. Acumular validações
locais e evitar solicitar capturas para cada alteração pequena.

## 2026-11-10 — Previsão de demanda por insumos

A recomendação e a aprovação dos onze bens agora verificam a demanda adicional
pelos PMs ativos do produtor. O registro `data/input_profiles.json` contém
coeficientes verificados para 18 tipos de prédio e 124 entradas de métodos.
A demanda de um nível completo recebe margem inicial de 25%.

O modelo mantém a oferta atual e desconta vagas e expansões enfileiradas dos
tipos conhecidos. Bens de mercado usam oferta/demanda agregadas e compromissos
dos estados do país, incluindo não incorporados. Eletricidade e transporte
usam produção/consumo e compromissos do próprio estado. A previsão aguarda
quando a nova demanda levaria a oferta/demanda abaixo de 50%, conforme o limiar
verificado nos defines vanilla locais. Na igualdade, a candidata é permitida.

As margens são calculadas por leitura e armazenadas, evitando varredura
nacional por candidata. A aprovação recalcula antes de validar. Métodos ativos
são lidos ao vivo. Falta de dados do insumo produz margem zero. Insumo com
quantidade ativa zero não exige margem. Desativar remove snapshots. Os
cartões usam ScriptValue, padrão verificado nos widgets vanilla, para mostrar
referências e margens por insumo; há motivo próprio de rejeição por previsão.

A oferta de projetos futuros não é creditada. Mudanças futuras de preços,
comércio, emprego, PMs, produção e modificadores de throughput/consumo ainda
podem alterar o resultado. Tipos e métodos fora do registro e compromissos de
outros países permanecem fora da projeção adicional. O modelo é uma referência
que precisa de calibração. Construtores externos mantêm seus próprios filtros.

O exemplo de autoconsumo de carvão citado durante o desenvolvimento foi
corrigido após conferir os arquivos. Os perfis atuais da mina de carvão usam
outros insumos conforme o PM, sem crédito especial de produção no modelo.
Nenhuma exceção de carvão foi incluída no código.

231 testes sintéticos aprovados, com 14 regressões adicionais de coeficientes,
limiar, ausência de insumo, filas, vagas, energia local, revalidação, retomada,
limpeza e proteção do validador. Geração e validação estática local aprovadas.
Interface, desempenho e decisões novas ainda aguardam campanha. Manter a
preferência do jogador por testes agrupados após mudanças relevantes.

## 2026-11-10 — Setor de construção e segunda revisão no Automático (0.6.26)

O jogador pediu que o Automático aja por conta própria, sem depender de
explicações. Além da fila pública ocupada liberada na 0.6.25, o dispatcher
automático passou a aceitar o setor de construção quando ele é a primeira
prioridade do plano. A elegibilidade continua exigindo fila pública de ao
menos três projetos, setor com nível positivo, ocupação de 90%, sem falha de
contratação, falta de insumos ou expansão enfileirada, e guardas fiscais e de
materiais aprovadas.

Uma revisão bloqueada pela fila privada ou pela construção pausada agenda uma
segunda tentativa sete dias depois. Só uma segunda revisão é agendada por mês
de calendário, controlada por `sed_auto_retry_month`. A tentativa mensal só é
consumida quando há inclusão confirmada, como antes.

241 testes sintéticos aprovados, incluindo setor ranqueado e não ranqueado,
fila pública ocupada e a segunda revisão única. Geração, validação estática e
verificação de artefatos aprovadas. Sem instalação, engine ou campanha nesta
etapa.

## 2026-11-10 — Automático age com a fila pública ocupada (0.6.25)

O jogador pediu que o modo Automático aja sozinho, sem depender de explicações
ou de filas livres. A revisão mensal parava sempre que a fila pública tinha
qualquer projeto, inclusive obras de outros construtores, e por isso quase não
enfileirava nada em campanha.

A guarda do executor próprio agora exige apenas a fila privada vazia. A fila
pública pode estar ocupada e recebe no máximo um nível por revisão. Limite
mensal, inadimplência, construção pausada, construtores conhecidos, proteção
fiscal, referência de materiais, elegibilidade do prédio e
`level_after_queued_constructions` por prédio permanecem. O status 11 e o painel
passaram a descrever somente a fila privada. Manual, Assistido e a expansão
manual de setores de construção não mudaram.

A 0.6.24, ainda não documentada, escolhe o fornecedor de maior saída estimada e
marca o insumo que bloqueia uma expansão.

238 testes sintéticos aprovados, incluindo fila pública ocupada com inclusão
confirmada, bloqueio da segunda tentativa no mesmo mês e fila privada ainda
bloqueando. Geração e validação estática locais aprovadas. Sem instalação,
execução na engine ou campanha nesta etapa; custo incremental de fila longa e
concorrência real seguem sem confirmação.

## 2026-11-10 — Fundação da indústria ausente (0.7.0)

O jogador pediu que o Automático aja como gestor e transforme qualquer país com
os recursos que ele tem. A lacuna era a base produtiva ausente: o Director
identificava o bem em escassez sem produtor, mas não podia construir porque a
aprovação exigia um prédio existente para expandir.

A 0.7.0 inclui estados aptos a fundar a base no candidato normal do bem. Um
estado entra quando é incorporado, não tem nenhuma variante do prédio, aceita
`can_construct_building` para alguma variante e o país não tem produtor
verificado daquele bem. A fundação usa o ranking, o dispatcher, a aprovação e
o livro de resultados existentes; o nível inicial é 0 e a conclusão é inferida
quando o nível sobe ao sair da fila. As guardas fiscais, de materiais, de fila
privada, de pausa e o limite mensal continuam valendo. Sem estado apto, o
objetivo 5 permanece e nada é forçado.

243 testes sintéticos aprovados, incluindo fundação automática, ausência de
estado apto e as regressões anteriores. Geração, validação estática e verificação de artefatos locais
aprovadas. Sem instalação, engine ou campanha nesta etapa; custo real, terra
disponível e concorrência seguem sem confirmação.

## 2026-11-10 — Fundação única por país (correção da 0.7.0)

O gatilho de fundação podia duplicar a mesma indústria: enquanto a obra estava
na fila não existia prédio, o bem continuava marcado como ausente e outro
estado sem pedido pendente voltava a ser elegível na revisão seguinte. O
gatilho agora exige que nenhum estado tenha `sed_<bem>_request_pending`, então
só há uma fundação por país. Quando o prédio conclui, o bem deixa de ser
ausente e a expansão normal assume.

244 testes sintéticos aprovados, incluindo duas revisões mensais com dois
estados aptos e apenas uma inclusão. Geração e validação estática locais
aprovadas; comportamento na engine continua pendente.

## 2026-11-10 — Primeira ferrovia e pendência de fundação (0.7.1)

A 0.7.0 permitia fundar indústria, mas não ferrovia: um estado com
infraestrutura negativa e nenhuma ferrovia ficava só na contagem e nunca
recebia obra. A 0.7.1 aceita esse estado como candidato normal quando ele é
incorporado, aceita `can_construct_building` e não tem pedido pendente. A
aprovação grava nível 0 e o livro de ferrovias infere a conclusão quando o
prédio aparece, como já fazia com a indústria.

Ao revisar o caminho, apareceu uma falha da 0.7.0: sem prédio, a limpeza de
pendências marcava a fundação como abandonada na primeira leitura seguinte e
removia o marcador, permitindo fundar de novo em outro estado. Agora o pedido
de fundação permanece enquanto houver níveis na fila pública; só encerra
quando o prédio aparece ou a fila esvazia. A regra vale para ferrovia e para
os onze bens.

246 testes sintéticos aprovados, incluindo fundação automática de ferrovia e
persistência do pedido após diagnóstico intermediário. Geração, validação
estática e verificação de artefatos locais aprovadas. Sem instalação, engine
ou campanha nesta etapa; terra, permissão e concorrência reais seguem sem
confirmação.

## 2026-11-10 — Duração e materiais do primeiro projeto (0.7.2)

O orçamento direto ainda media a reserva por uma janela fixa de 26 semanas e
não dizia o tamanho da obra escolhida. A 0.7.2 identifica a ação em primeiro
lugar no plano e usa a construção exigida do prédio na base vanilla
(`required_construction`): 200 pontos para fazendas, madeira e tecido; 400 para
ferro e carvão; 600 para ferramentas, alimentos, roupas e indústria bélica;
800 para ferrovia, aço e munição; 25 para o setor de construção.

O painel passa a mostrar pontos, semanas e materiais de referência do projeto
inteiro. A reserva exigida usa a maior janela entre 26 e a duração mais quatro
semanas, limitada a 56. Projetos curtos mantêm o piso anterior; ferrovia e
munição exigem mais ouro, mas uma obra de até um ano de déficit coberto segue
autorizada. Fila concorrente, salários, subsídios e modificadores ainda podem
alongar o prazo e não entram na conta.

247 testes sintéticos aprovados, incluindo ferrovia de 800 pontos, 80 semanas e
reserva limitada a 56 semanas. Geração, validação estática e verificação de
artefatos locais aprovadas. Sem instalação, engine ou campanha nesta etapa.


## 2026-11-10 — Guardas de fundação e fornecedores ausentes (0.7.3)

A revisão encontrou fundações de indústrias sem as guardas de trabalhadores e
insumos das expansões. A aprovação agora revalida trabalho e insumos antes de
inserir a indústria, e a primeira ferrovia também recebe essas guardas. A
referência de insumos soma máximos por grupo de PM tecnologicamente disponível,
com grupos e tecnologias extraídos do vanilla local. Pode adiar uma fundação
viável com método simples. O Director ainda precisa selecionar e aplicar PMs.

Pedidos próprios sem prédio reservam trabalho e insumos. A leitura migra para
os PMs e a fila do prédio assim que ele existe, com regressões para dupla
contagem, cancelamento e alteração das condições antes da aprovação. Um
fornecedor ausente pode entrar no plano para desbloquear a indústria final.

253 testes sintéticos aprovados. Validação estática contra a instalação 1.15
aprovada. Confirmação na engine continua pendente.

Instalada com jogo fechado, backup `mod_before_0.7.3_20261110_230423_163114`
e conferência dos 14 arquivos pelo instalador.
