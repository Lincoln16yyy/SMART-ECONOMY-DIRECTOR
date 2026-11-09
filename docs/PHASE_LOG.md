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
