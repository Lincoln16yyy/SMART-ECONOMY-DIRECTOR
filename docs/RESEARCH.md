# Fase 0 — pesquisa técnica

Estado atual da 0.6.0 em [PLANNING.md](PLANNING.md) e [STATUS.md](STATUS.md).
A implementação inclui plano nacional inicial e coordenação de sete opções
externas com snapshot e restauração. A autorização do jogador para coordenar
Economy Advisor e Supply Chain nesta sessão amplia o escopo dos adaptadores.
As seções anteriores abaixo preservam a evolução histórica das versões.


Atualização de auditoria (2026-11-09): a implementação chegou à 0.4.1, mas a
pesquisa crítica da Fase 0 não está completa. Os parágrafos de introdução
referem-se à entrega inicial 0.1.0. A [auditoria atual](AUDIT_2026-11-09.md)
separa código, fonte estática e prova de engine. Prioridade: fila por projeto,
opções por país e dados econômicos incrementais; não ampliar executor antes
de resolver essas dependências. Não foi programado recurso nesta auditoria.


Data: 2026-11-08. Resultado: pesquisa estática inicial, com lacunas explícitas.
Este documento apresenta o diagnóstico e a arquitetura antes da implementação.
Não certifica compatibilidade nem funcionamento dentro de uma campanha.

Atualização: após esse diagnóstico, o jogador solicitou começar a construção
do mod. Foi implementado o diagnóstico 0.1.0 descrito em [PHASE1.md](PHASE1.md),
sem ações econômicas. As pendências abaixo continuam válidas para planejar
e executar ações; não foram declaradas resolvidas por começar a implementação.

## Fontes e ambiente encontrados

- Referência: https://github.com/Lincoln16yyy/Smart-Government-Victoria-3-1.15
  e checkout local `/home/lincoln-ii/Victoria3_mod`. O commit inspecionado está
  registrado em `SOURCE_INVENTORY.json`; alterações locais podem existir.
- Instalação: `/home/lincoln-ii/Games/Victoria 3`. O arquivo
  `launcher/launcher-settings.json` informa `rawVersion: 1.15.0`; o log local
  `logs/system.log:1` registra `release/1.15.0 : 6338547985`.
- Dados de usuário: `~/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3`.
  Os caminhos Windows em `content_load.json` pertencem a esse prefixo Wine.
- Mods instalados foram examinados na subpasta `mod` desses dados, e não apenas
  pelos ZIPs em Downloads. Saves Haiti e uma cópia `haiti_1836_06_30_SG_TEST.v3`
  existem. Nenhum save ou arquivo da instalação foi modificado.
- `SOURCE_INVENTORY.json` registra exemplos por identificador, arquivo e linha,
  separados entre vanilla e mods. Uma ocorrência em mod é evidência de uso,
  não prova de aceitação pelo motor. Não contém código proprietário do jogo.

## Smart Government: padrões aproveitáveis

Foram consultados README, AI_CONTEXT, PHASE_LOG e MANUAL_RUNTIME_TEST, além do
ciclo de vida, Journal Entry, on-actions e organização dos geradores/testes.

O sistema usa dados reais de leis, IDs numéricos estáveis e scripts gerados.
Calcula benefício, risco, apoio político e viabilidade; compara o mérito com a
lei vigente antes de formar um ranking global de até três opções. Os textos
explicam componentes e riscos. O botão inicia a promulgação normal; não aprova
a lei instantaneamente. Esse modelo político não deve ser copiado para economia.

`sg_on_actions.txt` acrescenta dispatchers com `on_actions = { ... }`.
`sg_journal_entries.txt` associa um widget ao `custom_widget_container_3`, usa
`activation_description` e executa atualização mensal. `sg_effects.txt` guarda
schema, data de atualização e habilitação, evita Journal Entries duplicadas,
limpa o estado ao desativar e conserva o schema para impedir reativação automática.
Ignorar/restaurar opera por ID; ações devem acompanhar o candidato, não uma
posição mutável da lista. Contadores de ranking tornam o diagnóstico auditável.

Os geradores `build_law_data.py` e `build_gui.py`, o parser `pdx_parse.py`, os
testes em `tests/test_advisor_generation.py`, o validador, as duas localizações,
o descriptor e o instalador fornecem referências de organização. A documentação
registra falhas reais da engine: BOM, define com namespace, nomes de listas e
propriedades GUI inválidas. Portanto, validação textual não substitui runtime.
Na continuação local, os 26 testes de leis passaram novamente. O validador
completo encontrou 178 erros no módulo de pesquisa tecnológica da referência;
o resultado está detalhado em LOCAL_AUDIT.md. O Director não modifica esse mod.

## Economy Advisor: sobreposição comprovada nos arquivos

Instalado como `3778129206_Economy_Advisor`, versão declarada 1.0.0,
`supported_version="1.15.*"`. Há decisões, três Journal Entries, scripted GUIs,
scripts gerados, análise econômica, orçamento, construção e avaliação de PMs.

- `common/on_actions/advisor_on_actions.txt`: monitoração mensal exige
  `advisor_enabled`; a construção exige `advisor_auto_construction_enabled`.
  Os comentários e eventos separam a construção para o dia 8 e PMs para o dia 15,
  evitando concentrar os cálculos pesados no início do mês.
- `advisor_automation_effects.txt:385` usa
  `start_building_construction = $BUILDING$`. Portanto, executa construções.
- A chamada ocorre em escopo de estado no efeito
  `advisor_auto_construction_start_rule_building` (`advisor_automation_effects.txt:382–390`).
  A rotina mede `construction_queue_num_queued_government_levels` antes e
  depois e só conta o projeto se a fila pública crescer (`:378–400`). Isso é
  uma referência de mecanismo e confirmação, não uma API pública a chamar.
- O mesmo mod filtra `can_construct_building = building_*` e, quando o prédio
  já existe, impede duplicar níveis consultando
  `level_after_queued_constructions > level` (`advisor_automation_effects.txt:131–140`).
  Esses exemplos não demonstram que todo prédio novo, regra injetada ou alvo
  privado seja tratado corretamente.
- A localização vanilla de triggers declara comparadores de
  `construction_queue_num_queued_government_levels` e
  `construction_queue_num_queued_private_levels`
  (`common/trigger_localization/00_trigger_localization.txt:4028–4088`). Há,
  portanto, uma forma de testar nível de fila pública e privada em triggers;
  esta inspeção não encontrou leitura numérica privada em script ativo.
- `advisor_core_values.txt:404–458` considera quantidade de projetos privados e
  governamentais, alocação privada e espaço de construção. O modelo também
  considera contratação, infraestrutura e efeito de preços após construção.
- `advisor_core_values.txt:1408–1448` usa `net_fixed_income`, `net_total_income`,
  `fixed_expenses`, reservas, crédito e custo de juros. Tem planos distintos de
  orçamento; a reserva de doze semanas é uma política desse mod, não regra universal.
- Os scripts de PM avaliam lucro, mão de obra, qualificações, insumos,
  infraestrutura e cooldown. `advisor_tax_capacity_effects.txt:471–479`
  contém aplicação real de PM administrativo.
- `advisor_lifecycle_effects.txt` remove flags de automação ao limpar o estado.
  Instalar o mod não demonstra que sua construção/PMs estejam ligados no save.

O mod está na lista habilitada do launcher. Ainda falta ler o estado de país
de uma cópia de save e confirmar na interface quais opções estão ativas.
Não existe contrato de integração documentado encontrado nesta inspeção.
Não chamar efeitos internos nem escrever suas variáveis como se fossem API.

## Capacidades e métricas

Legenda: **observável** indica leitura encontrada nos scripts; **executável**
indica mecanismo de ação encontrado; **parcial** indica modelo ou acesso
incompleto; **não suportado identificado** significa ausência de mecanismo
confiável nesta pesquisa, sem afirmar impossibilidade absoluta do motor.

Para exibição, valores numéricos lidos em script poderão ser transferidos a
variáveis `sed_` e formatados no widget, seguindo o padrão do Smart Government.
Isso é uma proposta; cada binding do novo widget precisa de teste de runtime.

| Métrica ou ação | Fonte real identificada | Classe e limitações |
| --- | --- | --- |
| Saldo total / operacional | Advisor: `net_total_income`, `net_fixed_income` | Observável em país; conferir unidade semanal na tela |
| Reservas | Vanilla `war_support_values.txt`: `gold_reserves`, `gold_reserves_limit` | Observável; reserva não é receita recorrente |
| Dívida / crédito | Advisor health: `principal`, `credit`, `scaled_debt` | Observável; proteger divisões com limite zero |
| Juros | Advisor budget: modificadores de taxa | Parcial: taxa calculada não é toda a decomposição da despesa observada |
| Receita/despesa detalhada, tributos e gastos militar/administrativo | Tela de orçamento; `fixed_expenses` no Advisor | Parcial: total fixo encontrado; falta mapear cada rubrica script/GUI |
| Gastos públicos de construção | Advisor: diferença entre saldo operacional e total | Parcial; inclui interpretação de transferências, validar contra orçamento |
| PIB | Vanilla `ip5_je_values.txt`: `gdp` | Observável; crescimento exige amostras datadas |
| PIB per capita | Vanilla `country_gdp_per_capita` | Observável como script value vanilla; conferir população e unidade |
| Padrão de vida | Advisor health: `average_sol` | Observável; média pode ocultar pobreza de grupos |
| Preços / oferta / demanda | Vanilla usa `market_goods_buy_orders`; mods usam `sg:goods`, `state_goods_pricier`, `state_goods_delta` | Parcial: escopo local e mercado distintos; confirmar venda e preço por bem |
| Importação/exportação e dependência externa | Scripts `advisor_generated_export_*`; mercado do jogo | Parcial: falta separar produção nacional e circulação em mercado compartilhado |
| Escassez nacional por bem | Economy Advisor `advisor_generated_profiles.txt:21264–21270` consulta `market = { mg:iron ?= { market_goods_has_goods_shortage = yes } }` | Mostra o padrão de leitura de escassez no mercado por bem; uso pelo mod não certifica o runtime do Director |
| Escassez local por bem | O mesmo perfil consulta `state = { sg:iron ?= { state_goods_has_local_goods_shortage = yes } }` | Separada da escassez geral do mercado; ainda não identificamos por script qual prédio deve aumentar a oferta |
| Escassez em edifícios | `building_has_goods_shortage` nos mods | Observável por edifício; preço alto sozinho não prova escassez e a flag não nomeia o insumo |
| Lucro / utilização / PM atual | `weekly_profit`, `occupancy`, `has_active_production_method` | Observável; lucro não equivale ao benefício nacional |
| Produção setorial / capacidade / insumos futuros | Buildings, PMs e modificadores vanilla; perfis gerados do Advisor | Parcial: requer catálogo próprio e cálculo com throughput e emprego |
| Mão de obra / desemprego / qualificações / salários | Triggers de workforce e valores de avaliação do Advisor | Parcial: falta validar separadamente cada primitiva e escopo |
| Alfabetização / educação / migração / população regional | Sistemas vanilla e interface | Parcial: mapeamento script e GUI ainda pendente por indicador |
| Infraestrutura | `infrastructure_delta`, `infrastructure_usage`; Supply Chain ferroviário | Observável por estado; fila pode consumir a margem futura |
| Capacidade de construção | Advisor: `modifier:country_construction_add` | Observável; considerar parcela privada e limite por projeto |
| Fila pública / privada | Advisor: `num_queued_government_constructions`, `num_queued_private_constructions` | Parcial: totais não bastam para deduplicar estado + tipo + níveis |
| Tecnologia disponível | `has_technology_researched` nos scripts | Observável; Director não controlará pesquisa nesta etapa |
| Construir normalmente | `start_building_construction` em escopo de estado; `can_construct_building`; contagem pública antes/depois | Mecanismo confirmado no Advisor 1.0.0. Para o Director, ainda falta validar chamada em clique, alvo persistente/recalculado, prédio inédito, regras efetivas de mods, fila privada e combinação com outros construtores |
| Trocar PM | `activate_production_method`, com `can_activate_production_method` | Executável; deixar aos controladores de PM no ecossistema |
| Histórico / avaliação de resultados | Variáveis persistentes e amostras mensais | Parcial; correlação observada não prova causalidade da construção |
| Aprendizado de máquina / previsão econômica exata | Nenhuma implementação confiável encontrada em script | Não suportado identificado; usar avaliação transparente de resultados |
| Coordenação atômica entre mods | Nenhum protocolo encontrado | Não suportado identificado; exigir um único executor configurado |

## Conclusão técnica e pendências

### Pesquisa de mercado por bem para a próxima ação

Na continuação da 0.3.4, foi conferido no código instalado do Economy Advisor
um padrão de consulta de shortage para bens específicos: escopo `market` com
`mg:<good>.market_goods_has_goods_shortage`, e escopo estadual `sg:<good>` com
`state_goods_has_local_goods_shortage` (`advisor_generated_profiles.txt`, linhas
21264–21270, versão local 1.0.0). O Advisor também compara sell orders, buy
orders e demanda de PM pendente. Isso mostra como uma recomendação futura pode
explicar o bem que está em falta; não é uma API de integração do Advisor e não
prova a aceitação dessas consultas pelo motor nesta campanha.

O índice local de buildings/PMs contém possíveis bens de saída e camadas de
definição, mas não resolve `INJECT`/`REPLACE`, nem identifica sozinho o PM ativo
no save. A versão 0.3.5 usa a escassez por bem e o PM ativo do prédio para
selecionar oito pares vanilla de produtor e bem. Exige estado incorporado,
ocupação mínima, ausência de falha de contratação, falta de insumos ou expansão
enfileirada, revalida no clique e usa a fila pública normal. Isso elimina o
palpite a partir do contador agregado, mas não calcula preço/retorno nem
contratação futura; a aprovação precisa ser conferida em campanha.

O extrator foi corrigido para ler atribuições de modificadores cujo operador é
`=`. O relatório local agora inclui `possible_producers_by_good`, com as camadas
de prédio, grupo de métodos e método de produção que podem gerar cada bem. Na
instalação examinada, o índice cobre 52 bens; isso confirma a ligação entre
definições, mas não demonstra que um método esteja ativo, que o prédio possa ser
construído naquele país ou que sua expansão seja lucrativa. O JSON local fica
fora do Git porque inclui dados de mods habilitados. A interface agora mostra
cada escassez reconhecida e explica quando nenhum produtor local passa pelos
filtros; o contador agregado da tela do Haiti continua insuficiente para
identificar um bem específico.

É viável propor um diagnóstico em Journal Entry e um planejador com ranking
explicável. Há mecanismos de execução, mas coexistência segura depende da fila
completa e de escolher quem executa. Replicar o construtor/PM do Advisor agora
duplicaria funções já existentes. A arquitetura proposta está em ARCHITECTURE.md.

A continuação produziu [LOCAL_AUDIT.md](LOCAL_AUDIT.md), incluindo Kuromi,
redefinições por ID e leitura da fila usada pelo Advisor, e uma
[matriz por indicador](METRICS.md) com fontes de GUI encontradas na instalação.
A ferramenta e o JSON permitem reproduzir a inspeção sem modificar os fontes.

A Fase 0 permanece aberta: o estado das automações por país não foi decodificado
do save binário; a cobertura da fila privada e de primeira construção requer
teste no motor; faltam fontes diretas de script para algumas métricas, além de
medição de desempenho. Os identificadores de fila em níveis existem como
triggers vanilla, mas sua leitura útil e sua identidade por estado/edifício
precisam de validação antes de proteger uma execução do Director. O mecanismo
de construção do Advisor serve como referência, não como integração nem prova
de coexistência segura. As leituras e bindings do núcleo de diagnóstico foram
identificados em fontes e conferidos em campanha pelo jogador. Não tratar
lacunas restantes como dados iguais a zero. A implementação começou por nova
instrução explícita do jogador, usando apenas o núcleo de leituras identificado.
As demais métricas continuam indisponíveis ou em pesquisa.

## Pesquisa anterior preservada

[Pesquisa na nuvem](RESEARCH_CLOUD.md) conserva as fontes fixadas e os resultados
prévios: 26 testes da referência aprovados; validador bloqueado pela ausência do
jogo naquele executor. Os caminhos e mods agora encontrados atualizam esse
diagnóstico. Esses testes não foram repetidos na presente sessão local.


### Diagnóstico de oferta 0.4.0

O detalhamento das rejeições reutiliza `has_building`, `has_variable`,
`level_after_queued_constructions`, `level`, `occupancy`, `has_failed_hires`,
`building_has_goods_shortage`, `has_active_production_method`,
`is_incorporated` e `can_construct_building`, os mesmos filtros de oferta da
0.3.5. É uma contagem por estado com o prédio associado, não por prédio mundial
nem por trabalhador. O primeiro motivo impede dupla contagem. Métodos fora da
lista verificada são classificados sem produção confirmada; isso não afirma
que um método de outro mod não produz o bem. Leituras não demonstram viabilidade
econômica do nível novo, disponibilidade de trabalhadores ou retorno.


### Preferências de recomendações 0.4.1

Usa os mesmos `set_variable`, `remove_variable`, `every_scope_state`, `owner`,
`has_variable` e `any_scope_state` já empregados na execução e seleção atual.
A preferência fica no estado, com namespace `sed_<ação>_ignored`. Não é uma
ordem de cancelamento nem uma restrição a construtores externos. A restauração
e a limpeza alcançam estados atualmente pertencentes ao país; transferência
de território não tem migração de preferências entre países implementada.


### Continuação: contrato de fila e limites da GUI

[QUEUE_CONTRACT.md](QUEUE_CONTRACT.md) fixa as novas referências da interface
nativa 1.15.0 e das rotinas do Advisor/Supply Chain. As listas paginadas de
projetos têm prédio, estado, investidor, tipo de financiamento e progresso na
GUI; não foi identificado iterador equivalente em scripted effect neste
recorte. A prova dentro da engine permanece pendente. A pesquisa não ampliou
as ações do Director nem alterou opções dos outros mods.

## Infraestrutura de expansões — investigação 0.5.4

Arquivos locais Victoria 3 1.15.0: `common/building_groups/00_building_groups.txt`
registra consumo por nível em bg_construction (2), bg_mining (2),
bg_agriculture (1), bg_plantations (1) e bg_light_industry (1.5).
`common/buildings/13_construction.txt` vincula o setor a bg_construction.
Esses valores motivam a guarda de déficit atual; não foram transformados em
previsão de custo efetivo. Mods, modificadores e projetos podem mudar a margem.
Validação estática e 84 testes sintéticos não comprovam execução na engine.


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
