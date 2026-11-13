# Contexto de continuidade

Última entrega do mod — 0.7.35 gerada e testada; instalação e campanha pendentes.
Código — 0.7.35 corrige a paralisia de campanha: escassez de bem sem produtor e
sem local apto em nenhum estado (ferro sem depósito, no Paraguai) marcava
objetivo 5 e barrava a trilha de crescimento por `sed_plan_missing_count = 0`,
ficando meses sem obra com caixa positivo. Agora `sed_missing_hostable` só é
verdadeiro se algum estado pode hospedar o produtor; sem local apto, a trilha
de crescimento recupera o mês. Objetivo 5 e mensagem seguem iguais.
Também confirmado em campanha (fotos): Economy Advisor com construção automática
ligada suspende a construção direta do Director por desenho de coordenação.
Antes: 0.7.34 acrescentou o setor de construção à trilha de crescimento (fila
pública ≥ 12 semanas, 25 pontos) e registra um achado de calibragem: a guarda de
materiais exige `despesas fixas × 4 + (custo semanal − renda) × semanas`; com
setor presente isso deu 88.600 de ouro no harness para país pequeno e pode ser o
motivo real do travamento em campanha (status 22). Hipotese, precisa de save.
Antes: 0.7.33 corrigiu o relato do Paraguai: economia equilibrada não gerava
prioridade e o mês terminava sem obra. `tools/core_growth.py` é a última
ramificação do despachante e expande madeira, ferro ou ferramentas (só prédio
existente, 1 nível/mês, sob as guardas) quando `sed_develop_core` vale: sem
burocracia negativa, sem estado acima da capacidade tributária, sem energia 20%
acima da base e sem bem sem produtor. Blocos explicativos do painel foram para
trás do botão de detalhes. Tarifa/subvenção: 13 nomes sondados no Tiger são
`unknown token`; presença/vantagem não é scriptável.
Antes: 0.7.32 deu executor próprio ao objetivo 9: sem ferramenta externa, o
executor próprio amplia `building_power_plant` um nível por mês, só em estado
incorporado com infraestrutura ≥ 0, `can_construct_building` aceitando (o jogo
exige `electrical_generation`) e eletricidade local ≥ 20% acima da base; 400
pontos reservados, conclusão inferida pelo nível, antes do Centro de Comércio.
Com Supply Chain detectado, o caminho externo continua. Antes: 0.7.31 fechou os
objetivos 6 e 7: sem ferramenta externa
detectada, o executor próprio amplia `building_government_administration` um
nível por mês (estado incorporado, infraestrutura ≥ 0, aceita a obra; no
objetivo 7 só onde `tax_capacity_usage > tax_capacity`), antes do fallback de
Centro de Comércio, com 100 pontos reservados e conclusão inferida pelo nível.
Antes disso, burocracia negativa terminava a revisão em status 2 sem obra.
Antes: Centro de Comércio como último recurso (0.7.30) quando o bem em escassez
não tem
produtor no país (`var:sed_plan_missing_<bem> = 1`, escopo país) e nenhum estado
pode receber a fundação, o Director amplia um Centro de Comércio existente ou
funda o primeiro, comprando capacidade de comércio. Não abre rota, não altera
tarifa/subvenção, não constrói sob Isolacionismo nem em estado com
`infrastructure_delta < 0`. Respeita fila privada, orçamento (100 pontos) e uma
tentativa por mês; conclusão inferida pelo nível. Antes: o evento de escassez
ensina a importação da 1.9+ e a localização inglesa foi corrigida (coluna de
idioma e `\n` escapado). Antes: cessão de PM ao Auto-Apply PMs; leitura do
Controllable Private Construction; unidade salarial por família; meta
plurianual; duração da fila pela engine. Comércio: script não abre rota
(removido na 1.9); autor/investidor e qualificações não têm primitiva legível.
Teste sintético — 424 testes aprovados.
Documentação — README e STATUS foram sincronizados com a 0.7.34; a lista de
lacunas herdada da 0.6.26 estava errada em PMs, fundação de prédios e salários
militares. Antes: README e STATUS sincronizados com a 0.7.30; a lista de
lacunas herdada da 0.6.26 estava errada em PMs, fundação de prédios e salários
militares, e o catálogo já tem doze bens (papel desde a 0.7.14). Nenhuma
mudança de comportamento nesta sincronização.
Estático — geração consistente e validação local 1.15 aprovadas. Tiger 1.19.0:
mesmos três campos de diário do vanilla 1.15 e 938 avisos (colocação de chaves
no GUI e OR de item único).
Carregou e Campanha — Centro de Comércio, retorno com salários, unidade por
estado, painel e pontuação de PMs seguem NÃO VERIFICADO.

Ler `AGENTS.md`, `docs/agent/vic3-modding/SKILL.md` e suas referências.
O ambiente registra o Tiger, o resultado da sondagem de comércio e o Smart
Government instalado (1.0.0, esquema 2, variáveis `sg_*`). A pasta de
documentação exportada do jogo continua ausente.
Próximo passo — ler a linha de status do painel em campanha: se aparecer 22, a
guarda de materiais é o bloqueio e precisamos do save para calibrar. Depois
executar `docs/MANUAL_RUNTIME_TEST.md`, seção 0.7.34 (setor de construção sob
fila longa), 0.7.33 (crescimento com economia equilibrada e painel curto), 0.7.32 (usina elétrica no objetivo 9,
tecnologia e fila privada), 0.7.31 (administração
pública nos objetivos 6 e 7, fila privada e save/reload), 0.7.30
(Centro de Comércio como último recurso, Isolacionismo e estado com
infraestrutura negativa), 0.7.29 (evento de importação com o novo texto, nos dois idiomas),
0.7.28 (PM cedido
com o Auto-Apply PMs ligado), 0.7.27 (seção de controle privado só com o outro
mod ativo), depois 0.7.23 (duração da
fila), 0.7.21 (evento de importação) e 0.7.17–0.7.19: unidade no painel, desvio
de fornecedor, pontuação de PMs, save/reload e limpeza. Depois retomar as
leituras fiscais e a fundação básica.

## 0.7.30 — Centro de Comércio como último recurso

Código — `sed_trade_center_needed` (país) exige bem em escassez com
`sed_plan_missing_<bem> = 1`, nenhuma candidata local elegível, nenhum pedido
próprio pendente e ausência de `law_type:law_isolationism`.
`sed_trade_center_candidate_eligible` (estado) exige `is_incorporated`,
`infrastructure_delta >= 0`, `can_construct_building = building_trade_center`,
sem pedido pendente, e ou nenhum Centro de Comércio, ou um com
`level_after_queued_constructions <= level`, ocupação ≥ 50% e sem contratação
falha. O despachante tenta a rota só depois de todas as candidatas locais falharem
(status 15) e `sed_run_trade_center_approval` confirma pela contagem de níveis do
governo. `sed_refresh_trade_center` roda no pulso mensal e infere conclusão pelo
nível. Orçamento: `TRADE_CENTER_POINTS = 100`
(`required_construction = construction_cost_very_low`,
`common/script_values/building_values.txt:7` no 1.15 instalado).

Descartes decididos por teste — a primeira versão usava
`sed_<bem>_supply_demand`, e 33 testes existentes quebraram: ela também cobre a
oportunidade de preço (bem caro sem escassez) e dispara com produtor apenas
esperando mão de obra ou insumo. Passou-se a exigir `sed_plan_missing_<bem>`,
que é exatamente "sem produtor no país", e `infrastructure_delta >= 0`, guarda
que o resto do mod já usa. Nenhum teste antigo foi alterado.

Teste sintético — 394 aprovados; 7 novos em `tests/test_trade_capacity.py`:
fundação sem produtor, expansão lendo o nível, bloqueio por Isolacionismo,
conclusão inferida no pulso, reserva de 100 pontos no orçamento, ausência de
compra de capacidade com produtor existente e texto do painel nos dois idiomas.

Estático — geração consistente, validação local 1.15 aprovada e Tiger 1.19.0
com 0 fatais, os mesmos 3 `unknown-field` de diário do vanilla 1.15 e 938
avisos.

NÃO VERIFICADO na engine: se o nível do Centro de Comércio realmente aumenta a
capacidade de comércio usada pelo Mercado Mundial, se a obra aparece na fila
do governo em campanha, se o fallback respeita o orçamento como esperado e como
o painel se comporta após save/reload.

## 0.7.29 — Evento de importação ensina o caminho da 1.9+ e loc em inglês

Relato do jogador: recebeu o evento de escassez de papel, não sabia como
importar, construiu a fábrica e descobriu depois que a 1.9 acabou com rota
manual. A descrição só dizia "abra a importação pela interface de comércio".

Código — a descrição do evento agora lista o caminho com termos conferidos no
jogo instalado 1.15: `building_trade_center` / `concept_trade_capacity`,
`concept_subventions` e `concept_tariffs`, `goods_transfer` (cláusula de
tratado) e `law_isolationism` com `country_disallow_trade_bool = yes`. A opção
passou a ser "Vou tentar importar pelo Mercado Mundial".

Dois defeitos de localização achados pelo teste novo: (a) `pt` era reutilizada
como rótulo em `for policy, pt, en` e `for good, pt, en`, então
`localization('english')` gravava português — o arquivo inglês estava errado
desde que esses laços entraram; agora a coluna é fixada antes dos laços.
(b) Quebras de parágrafo saíam como newline real, inválido em loc; agora são
`\n` escapado.

Teste sintético — 387 aprovados; três novos: termos do caminho de importação
nos dois idiomas, coluna de idioma correta (inglês sem "Ignorar", português sem
"Approve") e uma entrada por linha com `\n` escapado.

NÃO VERIFICADO na engine: exibição do texto longo do evento e das opções nos
dois idiomas; se as quebras escapadas aparecem corretamente no jogo.

## 0.7.28 — Cessão de PM ao Auto-Apply PMs

Auditoria dos 12 mods instalados: `docs/COMPATIBILITY.md`. Achados que mudam
código: Auto-Apply PMs (3353797125) mexe nos mesmos grupos de PM principais que
o Director moderniza, com um botão por prédio e botões de grupo
(`..._group_farms`, `..._group_mines`, `..._group_plantations`); OGAS for CWE é
de 1.13 + Cold War Era e não deve rodar nesta campanha; Government
Administration Auto Expand faz `REPLACE` inteiro do prédio vanilla e perde
`ai_value`.

Código — `EXTERNAL_PM_VARIABLES` em `tools/production_methods.py` mapeia prédio
→ botões do outro mod; a elegibilidade de modernização/recuperação ganhou
`owner = { NOT = { has_variable = ... } }` (a elegibilidade roda em escopo de
estado, então a variável de país precisa de `owner`). `sed_pm_external_managed`
e a linha `sed_pm_external` no painel avisam quando há cessão. Fundações novas
continuam recebendo a configuração inicial.

Teste sintético — 384 aprovados; dois novos cobrem a cessão pelo botão do
prédio e o alcance dos botões de grupo (fazendas/plantações, sem vazar para
serraria).

NÃO VERIFICADO na engine: se a cessão evita de fato a disputa de PM em campanha.

## 0.7.27 — Leitura do controle de construção privada

O jogador mantém ativo o Controllable Private Construction (3278770055). Ele
injeta `can_build_private`/`can_build_government` por prédio com
`INJECT_OR_CREATE:` e substitui `default_auto_expand_rule` com `REPLACE:`, e
publica uma variável de país por botão do diário dele.

Código — `sed_private_control_configured` (OR de 12 `has_variable`) e uma seção
no painel com uma linha por restrição ligada. `sed_auto_current_queue_control`
aparece quando a fila privada bloqueia o Automático e o controle está ativo.

Por que não controlar de fato: injetar `can_build_private` nos mesmos prédios
colidiria com a injeção do outro mod (mesma chave, ordem de carregamento
define o vencedor) e quebraria os botões dele em silêncio. O Director só lê.
A escrita dessas variáveis continua proibida pelo validador (variável externa).

Teste sintético — 382 aprovados; quatro novos cobrem a lista das 12 variáveis,
a ausência delas em `sed_competing_builder_configured` (ler não bloqueia o
executor próprio), a visibilidade da seção/aviso e a localização nos dois idiomas.

NÃO VERIFICADO na engine: se a leitura aparece em campanha, se a recusa de obra
pela intervenção no investimento estrangeiro surge como falha de ação e se a seção
some ao desativar o outro mod.

## 0.7.26 — Unidade salarial por família de prédio

Sondagem em `/tmp/sed_dur` com Tiger 1.19.0: `pop_qualifications`,
`state_pop_qualifications`, `has_pop_qualifications`, `wages`, `wage_rate` e
`average_wage` são `unknown token`. Só existe `average_sol` para leitura social e
`set_pop_qualifications` como efeito (escrita). Portanto qualificação e salário
por profissão não são filtráveis por script; o proxy continua sendo
`occupancy` e `has_failed_hires`, já usados desde as versões anteriores.

Código — `sed_refresh_investment_wages` passou a acumular custo e empregos por
família de prédio e a publicar `sed_investment_wage_unit_<prédio>` /
`_known_<prédio>` (país e estado). `sed_investment_<prédio>_return` usa a amostra
da família quando existe; caso contrário cai na média nacional, que agora o
`sed_investment_<prédio>_return_national` isola para teste.

Teste sintético — 378 aprovados; um novo compara a amostra da família com a
média nacional e confere o fallback.

NÃO VERIFICADO na engine: se a amostra por família melhora a escolha de fornecedor
em campanha real.

## 0.7.25 — Meta plurianual de escassez

Código — a meta anual da 0.6.4 continua; quando o bem volta a ser meta em anos
consecutivos, `sed_<bem>_goal_streak` sobe (máx. 5) e `sed_<bem>_meta_since`
guarda o primeiro ano. Estreak ≥ 2 dá +15 de prioridade e mantém a linha da meta
visível enquanto `sed_<bem>_short_months` existir; um ano pulado reinicia a
contagem. `sed_prev_year` (= `year - 1`) existe porque o validador do projeto
rejeita aritmética inline em igualdade de variável.

Teste sintético — 377 aprovados; dois novos cobrem a continuidade entre 1836/1837
(pontuação 195 → 210) e o reinício após ano pulado com teto em 5.

NÃO VERIFICADO na engine: exibição da meta plurianual em janeiro e peso de +15
na decisão real.

## 0.7.24 — Contagem de projetos e limite de autoria

Sondagem em `/tmp/sed_dur` com Tiger 1.19.0: `num_queued_constructions`,
`num_queued_government_constructions` e `num_queued_private_constructions` são
triggers de **país** (contam projetos, não níveis). `is_under_construction`
existe em escopo de prédio. `is_government_construction`, `is_privately_constructed`
e `construction_owner_is_government` são `unknown token`, e `construction_queue_size`
o Tiger 1.19.0 ainda não conhece.

Conclusão — não há primitiva para saber o autor/investidor de um item da fila.
O mod continua reconciliando por `level_after_queued_constructions` e marcas por
estado; a 0.7.24 só acrescenta o que a engine oferece: as contagens de projetos
do governo e privados no painel, ao lado dos níveis.

## 0.7.23 — Duração real da fila no orçamento direto

Evidência — `common/trigger_localization/00_trigger_localization.txt` registra
`construction_queue_duration`, `construction_queue_government_duration` e
`construction_queue_private_duration`; `triggers_l_english.yml` diz "Remaining
duration of construction queue is X weeks". Sondagem em `/tmp/sed_dur` com o
Tiger 1.19.0: zero erros, inclusive comparação contra script value à direita.

Código — o script não consegue ler o número, então `sed_refresh_direct_budget`
usa uma cadeia `if/else_if` guardada por `> 0` e publica
`sed_build_budget_queue_weeks_engine` arredondado para cima em faixas (2, 4, 6,
8, 12, 16, 20, 26, 32, 40, 52, 78, 104, 156, 208; acima disso 260). 0 significa
fila do governo vazia. A linha `sed_build_budget_project` do painel mostra as
duas leituras: referência do plano e leitura da engine.

Teste sintético — 374 aprovados; dois novos cobrem nove durações nas faixas e a
presença da variável nos dois idiomas.

NÃO VERIFICADO na engine: se o trigger aceita `> 0` em país sem fila de governo e
se a faixa exibida bate com a barra de obras.

## 0.7.22 — Pedidos do mercado no evento de importação

Antes de disparar, `sed_check_import_notices` grava
`sed_import_notice_<bem>_buy`/`_sell` a partir de `market_goods_buy_orders` e
`market_goods_sell_orders`. A descrição do evento imprime os dois valores com
`[ROOT.GetCountry.MakeScope.Var('…').GetValue|D]` — padrão verificado em
`negotiation.1.d6` do vanilla. A diferença indica o tamanho da lacuna; custo,
frete e comboios não são estimados. Unidade/período dos pedidos (semana) e a
exibição em evento seguem NÃO VERIFICADO na engine.

## 0.7.21 — Evento consultivo de importação

Código — `sed_check_import_notices` roda no pulso mensal e, para cada um dos
doze bens, dispara `sed_pulse.2..13` quando há escassez (`sed_<bem>_supply_demand`)
e nenhum estado tem candidata elegível nem pedido pendente. O evento é visível,
tem `duration = 3`, ícone vanilla `event_industry.dds` e três opções inline
(sem `effect = {}`, como no vanilla `1848.1`): "vou abrir a rota" (cooldown 12
meses), "recalcular o plano agora" (`sed_refresh_diagnostics`, padrão) e "só me
avise em 2 anos" (24 meses). O `immediate` grava 6 meses de cooldown em
`sed_import_notice_<bem>_month`, variável limpa ao desativar.

Evidência — sondagem com Tiger: `create_trade_route` removido na 1.9;
`add_trade_route_level`, `cancel_trade_route` e `establish_trade_route` são
tokens desconhecidos. Portanto o evento orienta, não age. `duration` em meses e
a escolha automática de opção ao expirar seguem NÃO VERIFICADO; as três opções
são inofensivas por desenho.

## 0.7.20 — Leis delegadas ao Smart Government

Código — o painel ganhou duas linhas: `sed_laws_scope` (leis, imposto de
consumo e gasto discricionário ficam fora do Director) e `sed_laws_external`
(exibida só quando o país tem `sg_enabled`), que informa que o Smart Government
Advisor está detectado e que as recomendações dele não são repetidas aqui.
Visibilidade por `sed_laws_external_visible_sgui`, em escopo de país. Nenhum
efeito novo altera leis.

Evidência — li o mod instalado em
`mod/Smart Government Advisor` (1.0.0, `supported_version 1.15.*`). Ele define
`sg_enabled`, `sg_schema_version` (esquema 2), `sg_top_1..3_law` com ids
estáveis de `data/law_ids.json`, `sg_ignored_*` e um diário próprio. O Director
só lê `sg_enabled`; não lê `sg_top_*` porque traduzir o id exigiria copiar o
`law_ids.json` deles, que pode mudar entre versões.

Teste sintético — regressão nova cobre as duas linhas, a visibilidade condicional
(sem `sg_enabled` fica oculta) e a ausência de `activate_law` nos efeitos gerados.

Não verificado — exibição do painel com os dois mods na engine e interação
com os diários. Roteiro curto em `docs/MANUAL_RUNTIME_TEST.md`.

## 0.7.19 — Unidade salarial visível no painel

Código — o painel do diário ganhou duas linhas fixas e três chaves de
texto PT/EN: `sed_investment_policy` (regra de retorno), `sed_investment_wage`
(unidade nacional por emprego ponderado, visível quando
`sed_investment_wage_known = 1`) e `sed_investment_wage_unknown` (fallback
material). Visibilidade por `sed_investment_wage_visible_sgui` e
`sed_investment_wage_unknown_visible_sgui`, ambas em escopo de país.
A unidade mostrada é a média nacional; a leitura por estado continua interna.

Evidência — comércio exterior não é scriptável na 1.15. Uma sondagem isolada
(`create_trade_route` em mod de teste, Tiger 1.19.0) respondeu
"`create_trade_route` was removed in 1.9 — replaced with world trade system".
O item "comércio" da lista de lacunas fica como limitação de engine, não como
pendência de implementação. No binário do jogo só restam comandos internos.

Teste sintético — nova regressão verifica as duas linhas no GUI, a visibilidade
e que a chave de fallback não referencia a variável da unidade.

Não verificado — layout do painel na engine, formatação `|2` da unidade e
comportamento após save/reload. Roteiro em `docs/MANUAL_RUNTIME_TEST.md`.

## 0.7.18 — Salários na pontuação de modernização e recuperação

Código — `tools/production_methods.py` calcula `wage_delta`, a diferença de
`weighted_jobs` entre o método alvo e o atual de cada par estático. Na
pontuação nacional de `sed_modernize_existing_industry` e de
`sed_recover_existing_industry`, o ganho material continua escalado por nível
e ocupação e passa a subtrair `wage_delta × nível × ocupação ×
var:sed_investment_wage_unit` quando `sed_investment_wage_known = 1` e a troca
adiciona emprego ponderado. A escolha global exige pontuação acima de zero,
então um par materialmente positivo pode ser descartado. Sem amostra salarial
do estado, a pontuação é a anterior.

Não mudou — o filtro estático de pares, as guardas de ocupação, insumos,
tecnologia, contratação, fila, pausa, limites mensais, reserva de insumos e
o intervalo de três meses por prédio seguem iguais. A configuração inicial
das fundações continua apenas material. Taxas por profissão e salário real
pago não são modelados.

Evidência — comparação com bloco de valor à direita é forma vanilla:
`common/diplomatic_actions/30_fund_lobby.txt` usa `net_fixed_income >= { ... }`.
`var:sed_investment_wage_unit` e `sed_investment_wage_known` são gerados pela
0.7.17 em escopo de estado.

Teste sintético — 2 regressões novas: unidade observada reduz a pontuação
(200 − 250 × 0,2 = 150) e unidade alta zera a pontuação e impede a troca.

Não verificado — ordem dos pares ainda é material; o ganho real da troca,
o impacto em ocupação futura e a calibragem da unidade seguem pendentes.

## 0.7.17 — Folha salarial observada no retorno do investimento

Código — `sed_refresh_investment_wages` é chamado no fim de
`sed_refresh_investment_prices`. Para cada prédio de estado próprio, com nível
positivo, ocupação de ao menos 80%, sem contratação falha, sem escassez de
insumos, não subsidiado, com `earnings > 0` e `weekly_profit <= earnings`,
soma-se `earnings - weekly_profit` como folha salarial semanal e
`pesos de emprego × nível × ocupação` como denominador. `sed_investment_wage_unit`
guarda o gasto por emprego ponderado; cada estado usa a própria amostra quando
existe e, senão, a média do país. `sed_investment_wage_known = 0` mantém a
margem material anterior.

Código — `sed_investment_<tipo>_return` desconta do valor material a folha
prevista do novo nível: pesos da configuração ativa, quando o prédio existe, e
pesos da configuração básica, quando é fundação. `data/employment_profiles.json`
traz emprego e `weighted_jobs` por método de 17 tipos de prédio, extraídos de
`common/production_methods` e dos `wage_weight` de `common/pop_types` locais.
As elegibilidades, as preferências entre variantes e `sed_plan_<ação>_margin`
passam a usar `_return`; o nome da variável do plano foi preservado.

Evidência — `earnings` aparece como valor semanal ao lado de salários em
`TOOLTIP_BUILDING_HEALTH_WORLD` e em `EARNINGS_BREAKDOWN`, ambos da
localização vanilla; `weekly_profit` consta em `TRIGGER_WEEKLY_PROFIT` e em
diários vanilla. `is_subsidized`, `occupancy`, `has_failed_hires` e
`building_has_goods_shortage` têm uso vanilla no escopo de prédio.
`owner.var:` é usado em `04_country_specific_ideological_movements.txt`.

Não verificado — a folha observada inclui o que a engine classificar como
lucro e pode divergir de salário pago; `earnings` semanal só está documentado
pela localização; a unidade é uma média nacional/estadual, não salário por
profissão. A renda do novo nível usa 75% da receita e 125% dos insumos, então
o retorno é conservador e pode bloquear obras viáveis. Sem amostra saudável,
o comportamento antigo é retomado. Confirmação em campanha pendente.

## 0.7.16 — Leituras fiscais e prontidão verificadas

Código — despesas fixas passam a ser calculadas por `fixed_income` menos
`net_fixed_income`, com piso zero. A mesma leitura alimenta diagnóstico,
reservas, política fiscal, recuperação salarial e orçamento de construção.
O nome da variável de diagnóstico foi preservado para os saves existentes.
O valor numérico antigo `fixed_expenses` consta como removido na versão 1.12
em `src/vic3/tables/targets.rs` do Tiger 1.19.0. Os dois operandos novos são
aceitos pelo validador. `fixed_income` tem exemplo no vanilla instalado em
`common/script_values/ip4_je_values.txt`, no valor `yearly_gross_income`.

Código — prontidão usa `is_diplomatic_play_committed_participant`,
`is_diplomatic_play_initiator`, `is_diplomatic_play_target` e
`is_diplomatic_play_undecided_participant`, todos de escopo país nas tabelas
Tiger. Os três primeiros aparecem no trigger vanilla
`is_active_in_diplomatic_play`, em `common/scripted_triggers/00_scripted_triggers.txt`.
A leitura anterior `has_diplomatic_play` é de região estratégica.

Estático — Tiger 1.19.0 executado contra o jogo instalado. A execução inicial
registrou nove usos numéricos removidos e um aviso de escopo nessa guarda.
Esses dez apontamentos desapareceram após as correções. Restam três erros
`unknown-field` para `activation_description`, `disable_evaluation` e `outcome`
no diário. Os campos constam do vanilla 1.15, em exemplos de journal entries
e em `common/journal_entries/journal_entries.md`. O Tiger declara suporte
até 1.13.5 e alerta sobre o jogo 1.15. Não foram aplicadas supressões.
Avisos de formatação e OR de item único permanecem no relatório.

Carregou e Campanha — alterações fiscais e de prontidão da 0.7.16 seguem
NÃO VERIFICADO. A restauração e a confirmação após save/reload permanecem
no roteiro de campanha. Previsão de lucro com salários continua pendente.

## 0.7.15 — Insumos de uma configuração inicial concreta

No Automático, a previsão de fundação das indústrias geridas usa a primeira configuração
verificada de cada grupo de PM. A regra se aplica a todas as indústrias do
catálogo. Pesquisar métodos avançados deixa de acrescentar suas entradas à
previsão de uma fundação básica. A reserva de pedidos sem prédio usa a mesma
configuração. Após existir prédio, seus métodos ativos determinam os insumos.

O Assistido conserva a previsão anterior mais ampla. As opções ativas de
controle de PMs do Advisor também a conservam, pois esse executor assume a
configuração inicial. Ferrovia e
setor de construção também conservam seu modelo anterior. O Director continua
avaliando melhorias iniciais por tecnologia, oferta e margem material, com
revalidação de ativação e reserva mensal dos insumos escolhidos.

Um pedido próprio parcialmente ocupado pode confirmar a configuração básica
ou retornar seu grupo principal ao básico sem exigir de novo todos os empregos,
quando os grupos auxiliares já estão básicos e o PM principal preserva a
quantidade de empregos. Mudar grupos auxiliares que ampliem empregos continua
exigindo a verificação normal de trabalho. A regra vale durante a configuração
inicial rastreada. Preços e materiais continuam orientando a comparação econômica.
Previsão de lucro completo, salários por profissão e confirmação do resultado
real permanecem pendentes.

## 0.7.14 — Papel e bloqueio de orçamento do Advisor

O catálogo próprio passa a doze bens, incluindo papel. O Director pode fundar
a primeira fábrica ou ampliar uma existente. As rotinas geradas incluem plano,
aprovação revalidada, previsão de insumos, referência de materiais e duração,
reserva de trabalhadores, acompanhamento de pedidos e métodos de produção.
Os coeficientes foram extraídos do vanilla local 1.15. A configuração básica
usa 30 de madeira para 40 de papel e 5.000 empregos por nível. Métodos mais
avançados acrescentam enxofre, corantes e insumos de automação. Madeira,
ferramentas e carvão participam da propagação de prioridades do catálogo.
A produção própria de enxofre e corantes continua pendente.

A fundação automática diante de escassez também pode usar uma ocupação inicial
parcial. A reserva estimada precisa cobrir pelo menos 25% dos empregos e os
trabalhadores suficientes para o déficit atual com 25% de folga, usando a saída
do método básico. Esses limiares são heurísticas iniciais. A aprovação Assistida
e a expansão de produtores conservam a exigência de trabalho anterior.
O projeto enfileirado continua comprometendo todos os empregos do nível.
Essa regra evita exigir uma fábrica inteira para suprir uma demanda pequena,
mas contratação real, qualificações e rentabilidade ainda exigem calibração.
No save foram encontradas leituras de reserva estimada próximas de 1,6 mil e
2 mil, abaixo dos 5 mil empregos antes exigidos para fundar papel.

O save `paraguai_1843_03_06.v3` contém o estado 4 do Advisor, cuja rotina
corresponde a bloqueio de orçamento. As variáveis salvas registram compromisso
semanal de 7.289,95, margem de 2.679,70655, dez pontos e reserva disponível de
161.151,98626. O compromisso por 26 semanas exige 189.538,70. Esses números
foram lidos nos registros numéricos de variáveis do save binário, em escala
100.000, e confrontados com as rotinas instaladas. O diagnóstico explica a
espera registrada pelo executor externo. Os pontos gratuitos contam como
capacidade. A ausência de setor, isoladamente, não determina essa espera.

A rota própria de papel conserva seus filtros e pode usar a capacidade gratuita
com a referência de materiais dos setores existentes. A obra depende de
tecnologia, permissão, trabalhadores e insumos elegíveis. A inclusão na fila
real e o efeito na universidade precisam de confirmação em campanha.

## 0.7.13 — Investimento civil antes da escassez

O teste do Paraguai em 1842 confirmou avanço da revisão mensal até julho,
reservas de 163 para 170 mil e fila vazia em agosto. O país fotografado tinha os dez pontos gratuitos e nenhum setor. Esses
pontos entram em `country_construction_add`, conforme o modificador vanilla
`country_gdp_construction`. A ausência de setor, por si só, não explica a
inatividade do Advisor. O motivo exato da seleção externa permanece pendente.

O Director agora inclui no catálogo próprio bens civis com compras positivas,
compras superiores às vendas e preço de mercado pelo menos 20% acima da base.
Essa oportunidade exige margem material estimada positiva e conserva as
verificações de trabalho, insumos, infraestrutura, fila e orçamento. A regra
vale no Automático. Escassez e insumos estratégicos mantêm seus critérios.
A propagação de necessidades também considera esses alvos civis caros.
O limiar de 20% é uma heurística inicial que exige calibração em campanha.
A inclusão depende de um fornecedor elegível. O resultado do Paraguai após
esta mudança ainda precisa de confirmação na engine.

## 0.7.12 — Preços observados nas referências de investimento

A escolha de fornecedores incorpora sinais de preços atuais. O mercado usa
leitura direta de `market_goods_pricier` e `market_goods_cheaper`, cuja forma
numérica foi verificada nos artigos vanilla de transferência de bens. Os
estados usam comparações nativas de preços locais em faixas de 10%, com ponto
adicional em 75%. Os preços-base continuam fornecendo a unidade monetária.

A referência inferior de receita e superior de insumos conservam folga de
25% do preço-base e incluem a incerteza da faixa local. As referências são
limitadas ao intervalo de zero a duas vezes o preço-base. A definição vanilla
`PRICE_RANGE = 0.75` e as comparações locais foram verificadas no jogo instalado.

Informação local tem precedência. Na ausência dela, a leitura usa o mercado.
A ausência de ambas as observações deixa a referência em torno do preço-base.
As leituras ficam em cache por país e estado e são renovadas na atualização
do plano e na aprovação. Os estados adicionados após uma leitura também têm
cálculo de referência disponível. Desativar limpa os caches.

Essas referências alimentam a seleção de fornecedores das obras próprias,
incluindo fundações. O diagnóstico renova dados. Ações econômicas continuam
sob as autorizações de execução. Retorno real, salários, qualificações,
modificadores de produtividade e impacto futuro da nova oferta nos preços
precisam de modelo e calibração. Confirmação na engine segue pendente.

## 0.7.11 — Escolha econômica dos fornecedores

A necessidade nacional escolhe o bem. No Automático, os fornecedores elegíveis
desse bem são comparados por margem material de referência, oferta e desempate
econômico. Havendo alternativas com margem estimada não negativa, elas têm
preferência. Nesse grupo, a maior saída do bem-alvo vem primeiro e a margem
desempata ofertas iguais. Se todas as referências forem negativas, a seleção
mantém uma opção para a necessidade estratégica.

A mesma regra escolhe a variante dentro do estado e ordena os três pares do
plano, com revalidação na aprovação automática. A margem contabiliza 75% do
valor de todas as saídas conhecidas e 125% do custo dos insumos, a preços-base.
As quantidades respeitam os métodos ativos e as mudanças de produtos
secundários. Uma fundação usa a configuração básica como referência inicial.
A saída líquida do bem-alvo precisa ser positiva para integrar os fornecedores.

O campo `all_outputs` de `data/founding_method_economics.json` foi extraído dos
PMs vanilla locais. O novo gerador `tools/investment.py` fornece referências por
nível. Salários, qualificações, preços locais, bônus de produtividade, despesas
operacionais futuras e lucro real ainda precisam de modelo e calibração. As
referências servem à escolha dentro do catálogo atual.

## 0.7.10 — Recuperação de produtores com insumos em falta

A revisão automática avalia recuperação antes da modernização. O candidato
precisa ter escassez de insumos no prédio e confirmação de escassez de um
insumo que o método alvo elimine. A troca preserva os outros grupos de PMs,
não introduz insumos nem aumenta quantidades de entrada ou empregos do grupo.
A configuração alvo precisa ter margem material positiva a preços-base.

A saída nominal estimada do bem-alvo precisa preservar pelo menos metade da
saída atual e continuar positiva. Essa conta usa todos os PMs ativos conhecidos,
incluindo mudanças de produção secundária. As quantidades dos demais produtos são
preservadas. Todos os insumos que restariam após a troca precisam estar sem
escassez observada, considerando também os outros grupos de PMs. O requisito de
ocupação é de pelo menos 50%. O maior custo de insumos evitado, ponderado por
nível e ocupação, seleciona o candidato nacional.

Recuperação usa a tentativa mensal compartilhada com modernização e construção.
Ela pode ocorrer em default, em estados não incorporados, com infraestrutura
negativa e expansão já enfileirada, pois a mudança reduz as dependências do
método e abrange os níveis existentes/futuros do mesmo tipo. O intervalo de
observação anterior de uma modernização pode ser superado para tratar a
escassez. A troca confirmada inicia novo intervalo de três meses antes de
modernizar novamente. Controles externos e marcas de ignorar têm precedência.

A recuperação pode reduzir a produção nominal. O piso e a margem são referências
baseadas nos coeficientes vanilla. Preços locais, qualificações, remuneração e
produção efetiva ainda exigem desenvolvimento e verificação. O resultado da
revisão confirma a troca do método, com avaliação econômica posterior pendente.

## 0.7.9 — Modernização contínua dos produtores existentes

O Automático avalia produtores de bens em escassez ou insumos priorizados.
Compara mudanças do grupo principal que aumentem a saída do bem-alvo,
preservem os demais produtos, não aumentem o total de empregos do grupo e
melhorem a margem material estressada a preços-base. O maior ganho estimado,
escalado pelo nível e ocupação, escolhe o prédio nacional.

A seleção exige pelo menos 90% de ocupação, contratação sem falha, ausência de
escassez atual de insumos, infraestrutura e incorporação adequadas, ausência
de expansão enfileirada e permissão tecnológica/do jogo. Os insumos adicionais
são projetados para todos os níveis e recebem margem de 25%. A reserva mensal
é aplicada antes de novas leituras do plano.

Há uma tentativa mensal nacional, compartilhada com a construção direta, e
um intervalo de três meses por prédio após troca confirmada. O limite mensal
é marcado antes do comando, inclusive em falha. Trocas de modo preservam o
intervalo por prédio. Desativação limpa o acompanhamento por prédio e preserva
o marcador mensal. Após a tentativa, a coordenação suspende as opções
verificadas de construção externa até o mês seguinte, sob executor 13.

Os controles `advisor_pm_balance_enabled` e `advisor_labor_auto_enabled` foram
verificados na agenda e rotina de PMs do Advisor instalado. Quando estão
ativos, a modernização própria aguarda e o preparo inicial é entregue ao
controlador externo. ARoAI ativo também impede modernização própria.

A análise continua limitada ao catálogo e ao grupo principal. Qualificações,
salários por profissão, preços locais, lucro real, automação dos demais grupos
e modernização das unidades militares permanecem pendentes. Uma nova leitura
após a troca reavalia os gargalos. A confirmação na engine segue necessária.

## 0.7.8 — Escolha econômica inicial de PMs

A configuração das fundações compara os métodos do grupo principal. O cálculo
usa 75% da receita a preços-base e 125% dos insumos a preços-base. Uma
alternativa precisa aumentar a saída do bem-alvo, melhorar a margem material
sobre a básica, ter margem positiva e não aumentar a soma de empregos do grupo.
Entre alternativas elegíveis, a maior margem de referência é tentada primeiro.
Os outros grupos usam a configuração básica anterior. Tecnologia, permissão
do jogo, insumos e reserva demográfica continuam revalidados antes da mudança.

O novo `data/founding_method_economics.json` contém coeficientes de entradas,
saídas, empregos e tecnologias do grupo principal, extraídos dos arquivos
vanilla locais, e preços-base dos bens. A seleção é inicial e ocorre nas
fundações acompanhadas. Modernização contínua dos prédios estabelecidos,
salários por profissão, preços locais, qualificações e lucro real ainda
exigem desenvolvimento e calibração.

A reserva integral estressada de insumos das configurações efetivamente
alteradas passa a integrar as leituras de margem até o fim do mês civil.
Assim, a atualização do plano ou um diagnóstico no mesmo mês preserva o
compromisso quando a demanda de mercado ainda não foi recalculada. A reserva
expira na mudança do mês e é limpa na saída do Automático ou desativação.
Essa regra pode adiar ações mesmo depois de a demanda real já incorporar o PM.

## 0.7.7 — Configuração inicial das indústrias fundadas

Fundações automáticas de produtores recebem uma marca de configuração inicial
após inclusão confirmada. Na revisão automática, o Director tenta aplicar o
primeiro método vanilla de cada grupo de produção do prédio, formando uma
configuração básica. O registro de grupos foi extraído da instalação local.

A operação exige prédio presente com nível atual e após fila de no máximo um,
estado incorporado, ausência de marca de ignorar, reserva demográfica cobrindo
os compromissos e margem para todos os insumos da configuração básica com 25%
de estresse. Todos os métodos precisam estar ativos ou passar por
`can_activate_production_method` antes de qualquer mudança. A confirmação usa
os métodos ativos. Trocas realizadas reservam os insumos na leitura corrente
para impedir que outra configuração use a mesma margem.

A marca é removida após confirmação, saída do Automático, desativação,
cancelamento identificado, expansão além do primeiro nível ou marca de ignorar.
Atualizar o diagnóstico continua sem executar configuração. O método aplicado
passa a integrar o prédio. A função usa `activate_production_method` em escopo
de estado, com a assinatura verificada no executável e no adaptador de
administração do Advisor instalado.

A escolha é uma configuração básica inicial. Comparação de produtividade,
preços, rentabilidade, qualificações e modernização dos prédios estabelecidos
continua pendente. A guarda conservadora de insumos para autorizar a fundação
continua usando os métodos tecnologicamente disponíveis. O acompanhamento é
baseado no livro inferido existente, sem identidade de projeto. A primeira
aplicação real ainda exige confirmação na engine.

## 0.7.6 — Compromissos da fila e retomada por reservas

O orçamento direto soma a construção de níveis pendentes nos tipos vanilla
verificados em `data/queued_building_costs.json`, incluindo fundações próprias
que ainda não têm prédio. A fila pública agregada limita a soma. Níveis sem
correspondência usam 6000 pontos, o maior custo vanilla verificado. A janela
estimada soma fila/capacidade nacional, duração do novo projeto e quatro
semanas, com piso de 26 semanas. O teto anterior de 56 semanas foi removido.

A referência semanal considera os pontos que os projetos públicos existentes
mais o novo podem consumir em paralelo, limitada pela capacidade nacional e
pelo material dos setores ocupados. A guarda de reservas usa essa referência
durante a janela estimada. O executor direto pode operar com déficit semanal
se o saldo operacional é não negativo, não há dívida e as duas guardas de
reservas e materiais são satisfeitas. Com coordenação, a prioridade própria
é avaliada antes da espera genérica por fila pública financiada por reservas.
Os caminhos específicos do Supply Chain mantêm suas guardas anteriores.

Os pontos da fila incluem o custo integral dos níveis pendentes e ignoram o
progresso já feito. Leituras por prédio podem incluir outro investidor e não
identificam projetos estrangeiros do país. O fallback cobre a falta de
correspondência na contagem agregada. Custos modificados por outros mods,
eficiência local, ordem exata, autoria e despesas operacionais futuras
continuam sem previsão precisa. A cobertura é uma referência de estresse.

## 0.7.5 — Despesa militar durante recuperação fiscal

O Automático passa a reduzir salários militares em crise/default com saldo
operacional negativo e despesas militares positivas. Cada mês permite um passo,
com piso baixo. Guerra, jogada diplomática ou formação mobilizada impedem o
corte. Déficit apenas de construção preserva essa despesa.

O primeiro corte captura o nível original. Com prontidão militar exigida,
a revisão pode recuperar um passo até médio, limitado ao original, mesmo
em crise. Acima de médio, ou na paz, a recuperação exige superávit,
saldo operacional não negativo, ausência de dívida, doze semanas de despesas
fixas em reservas e saldo de pelo menos metade da despesa militar observada.
Essa margem é um parâmetro conservador inicial, sem previsão exata do novo
salário. O limite mensal também vale para a recuperação de prontidão.

Sair do Automático ou desativar restaura o nível capturado. O marcador mensal
persiste para impedir cortes repetidos por troca de modo. Saves anteriores
sem snapshot capturam o nível no primeiro corte efetivo. A atualização de
diagnóstico continua sem executar políticas.

Fontes locais verificadas incluem o efeito `set_military_wage_level` e sua
assinatura no executável 1.15, a localização `SET_MILITARY_WAGE_LEVEL`, o
trigger `has_diplomatic_play` do executável e `any_military_formation` com
`is_mobilized` nos objetivos tutoriais vanilla. Aceitação e resultados em
campanha continuam pendentes. Recrutamento e modernização permanecem pendentes.

## 0.7.4 — Planejamento de insumos em vários elos

O Automático recalcula as prioridades a partir da escassez atual e propaga a
necessidade pelos fornecedores intermediários. Expansões e fundações podem
participar da cadeia. A propagação para quando encontra um fornecedor elegível
ou uma obra relacionada já enfileirada. Uma alternativa elegível em outro
estado evita priorizar os insumos de um produtor bloqueado.

Cada leitura limpa as prioridades anteriores. A propagação tem no máximo uma
passagem por bem de insumo suportado, encerrando antes quando nada muda. Isso
cobre os caminhos simples do catálogo e termina em dependências circulares.
O livro de fundações próprias passa a contar também na identificação de oferta
enfileirada, mesmo antes de existir prédio.

A execução continua limitada a uma tentativa por mês e ao catálogo atual.
Bens fora do catálogo, comércio, escolha de PMs e ciclos sem fornecedor viável
continuam pendentes. Nenhuma produção futura é creditada como oferta atual.
O plano volta a avaliar o gargalo após a mudança real da oferta.

## 0.7.3 — Fundações com reserva de trabalho e insumos

Correção da revisão de 0.7.2. As fundações de produtores e da primeira ferrovia
passam por guardas próprias de trabalho e insumos, revalidadas na aprovação.
`data/founding_method_groups.json` contém grupos e tecnologias extraídos dos
arquivos vanilla locais de 1.15. Os coeficientes continuam em
`data/input_profiles.json`. Para prédio ausente, cada insumo soma o maior
consumo de um método tecnologicamente disponível por grupo. Restrições de leis
ou princípios não reduzem essa referência. Ela pode bloquear um prédio que
seria viável com método mais simples. Escolher e aplicar PMs continua pendente.

Pedidos próprios de fundação reservam mão de obra e insumos enquanto ainda
não há prédio. Quando ele aparece, a leitura usa nível, fila e PMs ativos,
evita dupla contagem e libera a reserva após o acompanhamento encerrar o
pedido. As reservas dependem do livro inferido existente. Obras externas sem
prédio continuam sem identidade disponível. Fundações bloqueadas por insumos
entram nas prioridades de fornecedores, inclusive fundação do fornecedor.

O objetivo de evolução confirmado pelo jogador inclui recuperação econômica,
planejamento produtivo, comércio, PMs e fortalecimento militar conforme a
necessidade e os recursos. Modernização e recrutamento ainda estão pendentes.
Priorizar execução em segundo plano e pedir campanha só em marcos significativos.

## 0.7.2 — Duração e materiais do primeiro projeto

`sed_refresh_direct_budget` identifica a ação com `sed_plan_<ação>_rank = 1` e
usa `PROJECT_POINTS` (vanilla `required_construction` por tipo) para gravar
pontos, semanas estimadas e materiais do projeto. A reserva exigida usa
`max(26, semanas + 4)` com teto de 56 semanas. Novas variáveis em
`sed_build_budget_project_*`, painel e localização PT/EN. 247 testes
sintéticos aprovados; duração real de fila concorrente e salários continuam
fora da estimativa.

## 0.7.1 — Primeira ferrovia e pendência de fundação

Estado incorporado com déficit de infraestrutura e sem `building_railway`
entra no plano como `sed_railway_found_site`, desde que aceite
`can_construct_building` e não tenha pedido pendente. A aprovação de ferrovia
lê nível 0 quando não há prédio e infere conclusão quando ele aparece. A
limpeza de pendências agora mantém o pedido de fundação (ferrovia ou
indústria) enquanto houver níveis na fila pública e nenhum prédio; antes, a
primeira leitura após enfileirar marcava a fundação como abandonada e liberava
uma duplicação. Testes em `tests/test_planning.py`; 246 testes sintéticos
aprovados. Engine e campanha pendentes.

## 0.7.0 — Fundação da indústria ausente

Quando um bem está em escassez, o país não tem produtor verificado e algum
estado incorporado aceita `can_construct_building`, o estado entra como alvo
normal de oferta no plano. O Automático pode então enfileirar um nível do
prédio novo (intenção com nível 0) usando o dispatcher, a aprovação e o livro
de resultados existentes, sob as guardas fiscais, de materiais, de fila
privada, de pausa e o limite mensal. Sem estado apto, o objetivo 5 permanece e
nada é forçado. Implementação em `sed_<bem>_found_site` e no ramo de enqueue de
`sed_run_<bem>_approval`; o gatilho exige que nenhum estado tenha pedido
pendente daquele bem, limitando a uma fundação por país. Testes em
`tests/test_planning.py`. 244 testes sintéticos aprovados; engine e campanha
pendentes.

## 0.6.26 — Setor de construção e segunda revisão no Automático

O dispatcher automático passou a aceitar o setor de construção quando ele é a
primeira prioridade do plano, com as guardas fiscais, de materiais e de fila
existentes. Uma revisão bloqueada pela fila privada (11) ou pela construção
pausada (12) agenda uma segunda tentativa sete dias depois, no máximo uma por
mês de calendário (`sed_auto_retry_month`). 241 testes sintéticos aprovados;
geração e validação estática locais aprovadas; comportamento na engine
pendente.

## 0.6.25 — Automático com fila pública ocupada

O executor próprio agora age com a fila pública ocupada; exige somente a fila
privada vazia. O status 11 e o painel passaram a descrever a fila privada.
Limite mensal, proteção fiscal, referência de materiais, construtores
conhecidos e `level_after_queued_constructions` por prédio continuam iguais.
238 testes sintéticos aprovados; geração e validação estática locais
aprovadas; comportamento na engine pendente.

Antes dela, as 0.6.21–0.6.24 escolheram o fornecedor de maior saída estimada e
adicionaram prioridade automática do insumo que bloqueia uma expansão.

Entrega 0.6.20 instalada com jogo fechado, 14 outputs conferidos no ZIP e na
instalação, ordem preservada. Backup
`sed_backups/mod_before_0.6.20_20261110_190043_106415`.

## 0.6.20 — Previsão de insumos das expansões de oferta

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


Entrega 0.6.19 instalada com jogo fechado, 14 outputs conferidos no ZIP e na
instalação, ordem preservada. Backup
`sed_backups/mod_before_0.6.19_20261110_184103_355322`.

## 0.6.19 — Reserva estimada de mão de obra nas expansões de oferta

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


Entrega 0.6.18 instalada com jogo fechado, 14 outputs conferidos no ZIP e na
instalação, ordem preservada. Backup
`sed_backups/mod_before_0.6.18_20261110_182955_164469`.

## 0.6.18 — Limite material dos setores existentes

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


Entrega 0.6.17 instalada com jogo fechado, 14 outputs conferidos no ZIP e na
instalação, ordem preservada. Backup
`sed_backups/mod_before_0.6.17_20261110_181948_765186`.

## 0.6.17 — Referência de materiais para a execução direta

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


Entrega 0.6.16 instalada com jogo fechado, 14 outputs conferidos no ZIP e na
instalação, ordem preservada. Backup
`sed_backups/mod_before_0.6.16_20261110_180333_870620`.

## 0.6.16 — Ritmo de investimento por reservas e sincronização

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


Entrega 0.6.15 instalada com jogo fechado, 14 outputs conferidos no ZIP e na
instalação, ordem preservada. Backup
`sed_backups/mod_before_0.6.15_20261110_121434_509591`.

## 0.6.15 — Execução direta da prioridade de oferta na coordenação

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


Entrega 0.6.14 instalada com jogo fechado, 14 outputs conferidos no ZIP e na
instalação, ordem preservada. Backup
`sed_backups/mod_before_0.6.14_20261110_120531_431140`.

## 0.6.14 — Expansões da indústria bélica

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


Entrega 0.6.13 instalada com jogo fechado, 14 outputs conferidos no ZIP e na
instalação, ordem preservada. Backup
`sed_backups/mod_before_0.6.13_20261110_115247_160824`.

## 0.6.13 — Avaliação econômico-militar

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


Entrega 0.6.12 instalada com jogo fechado, 14 outputs conferidos no ZIP e na
instalação, ordem preservada. Backup
`sed_backups/mod_before_0.6.12_20261110_114152_397000`.

## 0.6.12 — Acompanhamento de gargalos com obras na fila

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


Entrega 0.6.11 instalada com jogo fechado, 14 outputs conferidos no ZIP e na
instalação, ordem preservada. Backup
`sed_backups/mod_before_0.6.11_20261110_111421_898799`.

## 0.6.11 — Política e acompanhamento da delegação

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


Entrega 0.6.10 instalada com jogo fechado, 14 outputs conferidos e ordem de mods
preservada. Backup `sed_backups/mod_before_0.6.10_20261110_105919_917684`.

## 0.6.10 — Objetivo e executor

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


Entrega 0.6.9 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.9_20261110_101047_639382`.
146 testes aprovados, validação estática local e pacote aprovados.

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

Entrega local 0.6.8 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.8_20261110_013400_273582`.

## Livro completo 0.6.8

O livro de resultados cobre também ferrovia e setor de construção:
`sed_railway_intent_level` / `sed_construction_intent_level` guardam o nível
na aprovação; `sed_<tipo>_intents`, `_completed`, `_abandoned`, `_result` e
`_result_month` registram o desfecho quando a fila esvazia. Prédio ausente
conta como abandono. É inferência por fila/nível, sem identidade de projeto.
Desativar limpa marcadores estaduais e contadores. 137 testes aprovados; sem
confirmação na engine.

## Entrega local 0.6.7

Entrega local 0.6.7 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.7_20261110_012225_626750`.

## Livro de resultados por alvo 0.6.7

Cada aprovação dos oito bens grava no estado `sed_<bem>_intent_level` (nível do
produtor antes da fila) e `sed_<bem>_intent_variant`. A confirmação incrementa
`sed_<bem>_intents`. Quando o pedido sai da fila, o nível atual é comparado à
linha de base: maior conta `sed_<bem>_completed`, igual ou menor conta
`sed_<bem>_abandoned`; `sed_<bem>_result` e `_result_month` guardam o último
desfecho. O plano mostra pedidos/concluídos/abandonados só quando há histórico.
É inferência por fila e nível, não identidade de projeto; cancelamento com obra
externa pode distorcer. Ferrovia e setor ainda sem registro. A captura usa
`b:<prédio>.level` como valor (forma do Advisor instalado,
`advisor_core_values.txt:1040`). 136 testes aprovados; sem confirmação na engine.

## Entrega local 0.6.6

Entrega local 0.6.6 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.6_20261110_011134_926784`.

## Salários do governo 0.6.6

`sed_apply_wage_policy` move o salário civil do governo um passo por revisão no
Automático: desce em crise/default (piso `low`) e sobe com classificação 1/5,
superávit, sem dívida e doze semanas de despesas fixas em ouro (teto `medium`).
`sed_gov_wage_saved` guarda o original e `sed_restore_wage_policy` o devolve ao
sair do Automático ou desativar. Cautela, Manual e Assistido não alteram
salários; militares e despesas ficam fora. O efeito
`set_government_wage_level` só aparece na localização vanilla, sem uso em
scripts: aceitação na engine é a principal incerteza. 135 testes aprovados.

## Entrega local 0.6.5

Entrega local 0.6.5 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.5_20261110_010449_284523`.

## Política fiscal própria 0.6.5

No Automático, `sed_apply_fiscal_policy` move o nível de imposto um passo por
revisão mensal: sobe em cautela, crise ou default (até `very_high`) e desce com
classificação 1/5, superávit, sem dívida e doze semanas de despesas fixas em
ouro (até `low`). `sed_tax_level_saved` guarda o nível original e
`sed_restore_fiscal_policy` o devolve ao sair do Automático ou desativar.
Mudanças manuais durante o Automático são substituídas na revisão seguinte.
O validador limita `set_tax_level` a esses dois efeitos e exige a guarda de modo.
Salários, despesas, impostos de consumo e leis não são alterados; efeito real na
receita e aceitação na engine não confirmados. 132 testes aprovados.

## Entrega local 0.6.4

Entrega local 0.6.4 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.4_20261110_005319_526047`.

## Metas industriais anuais 0.6.4

Escassez de mercado por três meses consecutivos define uma meta industrial
anual para o bem: `sed_<bem>_short_months` conta a sequência e
`sed_<bem>_meta_year` grava o ano. A meta vale até a virada do ano civil, recebe
25 pontos adicionais no plano e aparece em linha própria no diário. Não cria
candidato: elegibilidade, fila, insumos, trabalhadores, infraestrutura,
permissão e política fiscal continuam obrigatórias. Desativar limpa contadores
e marcadores. Três meses e 25 pontos são parâmetros iniciais sem calibração em
campanha. Metas plurianuais, cadeias completas e feedback por alvo continuam
pendentes. 129 testes aprovados; comportamento na engine não confirmado.

## Entrega local 0.6.3

Entrega local 0.6.3 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.3_20261110_002209_786280`.

## Produtores alternativos 0.6.3

O catálogo deixou de assumir um prédio por bem. Cereais aceitam fazendas de
trigo, centeio, arroz, milho e milhete; tecido aceita plantação de algodão e
fazenda de gado. Cada variante tem trigger próprio `sed_<bem>_<prédio>_eligible`;
a elegibilidade é uma disjunção e a aprovação enfileira o primeiro produtor
elegível. O diagnóstico de produtor ausente e as rejeições usam as mesmas
variantes. Fontes vanilla e limites em PLANNING.md. 126 testes aprovados;
combinações novas ainda sem confirmação na engine.

## Entrega local 0.6.2

Instalada com jogo fechado, 14 outputs conferidos e content_load.json
preservado. Backup em `sed_backups/mod_before_0.6.2_20261109_235909_180351`.

## Construção financiada por reservas 0.6.2

A classificação fiscal 5 permite coordenação quando o déficit operacional é
coberto por reservas: receita fixa não negativa, déficit total observado, sem
dívida e ouro cobrindo doze semanas de despesas fixas mais 26 semanas do
déficit. `sed_coord_fiscal_safe` aceita a guarda antiga ou a 5 com Advisor
detectado; os ramos do Supply Chain continuam exigindo saldo não negativo. A
classificação 5 permite crescimento e não força estabilização. O limite
mensal automático passou a usar o script value `sed_live_month_key`, e o
validador rejeita aritmética embutida em igualdades `var:`. 124 testes
aprovados; instalação e comportamento em campanha ainda não confirmados.

## Entrega local 0.6.1

Instalada com jogo fechado, 13 outputs conferidos e content_load.json
preservado. Backup em `sed_backups/mod_before_0.6.1_20261109_222628_869777`.

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

## Entrega local 0.6.0

Instalada com jogo fechado. Os 13 outputs conferem byte a byte com o gerador,
e content_load.json foi preservado. Backup em
`sed_backups/mod_before_0.6.0_20261109_220347_442062`.
115 testes sintéticos aprovados, geração atual, validação estática contra
Victoria 3 1.15.0 e ZIP aprovados. A instalação substitui a 0.5.8.
Selecionar Automático novamente aplica os adaptadores em save da 0.5.x.
Coordenação, novo layout e save/reload ainda aguardam verificação na engine.

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

## Entrega local 0.5.8 — 2026-11-09

Instalada com jogo fechado. Backup:
`sed_backups/mod_before_0.5.8_20261109_212722_719786`.
Os 13 outputs foram conferidos byte a byte; `content_load.json` preservado.
A pasta antiga foi retirada antes de gerar a nova, sem arquivos remanescentes.
Isso atualiza as notas anteriores de instalação 0.5.4; engine e save/reload
continuam sem teste nesta etapa.

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

## Continuação — limite mensal persistente de tentativas 0.5.3

Instalada sem jogo em execução; backup `mod_0.5.2_20261109_121259_782337`;
13 outputs conferidos e load order preservado.

O Automático agora admite uma tentativa por mês, gravando
sed_auto_last_attempt_month antes de construir. A guarda é consultada no
executor e nos dez efeitos de aprovação quando o modo é Automático; isso não
adiciona setor de construção ao dispatcher automático. Inclusão sem confirmação
consome o mês; sem candidato/operacionalmente bloqueado não consome.

Importante mudança de limpeza: PERSISTENT_VARIABLES declara schema e marcador
mensal. Desativar limpa runtime/leituras/pendências, mas preserva essa única
marca de segurança quando existe. Evita reiniciar limite por modo/desativação.
Validador foi ajustado para exigir a preservação e não aceitar outras sobras.
Assistido continua explícito e sem esse limite, sujeito às guardas existentes.
A comparação usa year/month atuais, não sed_month_key do diagnóstico.

81 testes passam (77 anteriores + quatro), incluindo dez tipos, fila esvaziada,
troca de modo, reativação, falha de inclusão, Assistido, virada de ano sem
refresh e regressão negativa de limpeza. O contador sintético não comprova
fila real; persistência de variáveis continua sem save/reload na engine.
Proteção não é reconciliação completa, nem calibração fiscal, e não recupera
um histórico completo de versões anteriores. Manter interface legível e não
cobrar teste do jogador agora.

## Continuação — status temporal do Automático 0.5.2

Instalada sem jogo em execução; backup `mod_0.5.1_20261109_115813_269189`;
13 outputs conferidos e load order preservado.

Captura enviada pelo jogador confirma renderização legível dos botões nativos,
modos, resumo e botão Abrir fila, compatível com a UI 0.5.x. Leitura 7/1839,
saldo £15.3K, reservas £2.36M, projetos públicos/privados 45/2 e ausência de
déficit de infraestrutura. Isso não comprova clique de aprovação nem abertura
da fila, só apresentação. Não exigir nova rodada de testes agora.

0.5.2 separa revisão agendada/aguardando pulso, bloqueios atuais (leitura live)
e último resultado registrado com mês/ano. Arquivo do resultado usa variáveis
próprias, não é apagado por trocar modo/atualizar diagnóstico. Desativar limpa.
Saves antigos sem data/arquivo mostram que ainda não há registro nesta versão,
sem inventar uma data. Não há mudança no agendamento, guardas ou execução.

77 testes passam (73 anteriores + quatro do painel). Início com evento
pendente, consulta sem executar, exclusividade dos bloqueios, histórico versus
condição atual, troca de modo, virada do ano, limpeza e gravação pelo evento
cobertos no harness. Novos textos e passagem de tempo ainda não testados na
engine. A captura confirma a melhoria visual anterior, sem fechar a Fase 0.

## Continuação — cartões acionáveis 0.5.1

Instalada sem jogo em execução; backup `mod_0.5.0_20261109_114658_276092`,
13 outputs conferidos e load order preservado byte a byte.

O jogador pediu seguir construindo sem depender de testes seus agora. Mantida
a interface legível: cartões exibem aprovação disponível, Passar para Assistido
(sem construir) e Atualizar recomendações para cartão desatualizado. Guardas de
fila/default só aparecem como bloqueio da aprovação individual no Assistido;
fora dele, o cartão elegível oferece a troca de modo. Pendências/stale não
mostram troca de modo como se ela fosse resolver a elegibilidade.

Atalho Abrir fila de construção usa InformationPanelBar.OpenPanelTab com o
mesmo alvo production_methods/construction_queues do vanilla states_panel.gui.
Não é nova primitiva de construção. Os 73 testes passam (70 anteriores e três
novos cobrindo dez ações). Fluxos e atalhos ainda sem prova visual na engine;
sem teste oculto e sem solicitação de teste ao jogador nesta etapa.

## Direção atual do jogador e interface 0.5.0

0.5.0 instalada sem jogo em execução; backup `mod_0.4.1_20261109_113054_750010`,
load order preservado byte a byte. Auxiliar de teste não instalado.

O jogador não consegue testar enquanto botões não forem claramente visíveis
e os textos forem minúsculos. Pediu continuar construindo até melhorar isso;
não cobrar agora nova rodada de testes nem instalar auxiliar separado para ele.
A prioridade passou para a interface principal do Director.

Implementado 0.5.0: default_button da instalação nativa, texto principal 20,
títulos 26, botões 52 pixels. Recomendações antes dos indicadores completos;
controle Mostrar/Ocultar indicadores e detalhes, sem ação econômica. Cartões
agora usam flowcontainer/datamodel com altura natural, texto limitado à largura
e sem linhas fixas que cortam mensagens. Descrições repetidas encurtadas,
tooltips e dados mantidos. Nenhuma mudança nos filtros de construção.

70 testes passam (67 anteriores + três de controles/legibilidade/toggle).
Fontes vanilla conferidas: gui/shared/buttons.gui default_button;
gui/shared/defaults.gui fontsize_large=20 e fontsize_xxl=26;
great_game_widgets.gui usa flowcontainer/datamodel; tsarpoints_widgets.gui usa
background em flowcontainer. Validação estática não confirma renderização.
Nenhum jogo foi iniciado para teste oculto prolongado.

## Continuação — auxiliar de inspeção de filas

Criado `tools/build_queue_probe.py`: gera um mod auxiliar independente 0.1.0,
namespace sedqp_, com decisão/JE, leituras manuais de projetos e níveis por
lado, e nível atual/após fila/diferença por prédio dos dez tipos do Director.
Não tem mutações econômicas nem agenda. Não foi instalado/habilitado; runtime
do Director continua 0.4.1. Instruções e limitações em
[QUEUE_PROBE.md](QUEUE_PROBE.md). Não apresentar nível zero sintético, variáveis
Building ou listas no harness como confirmação da engine.

67 testes passam (61 anteriores + 6 do auxiliar). A entrega separa os dois
ZIPs; o principal não inclui scripts sedqp_. Próximo passo útil: conferir uma
linha pública, uma privada e primeira construção em cópia, registrando o que
foi realmente exposto. Ainda não há reconciliação por projeto, política fiscal
incremental ou inclusão real confirmada. Não iniciar teste oculto prolongado.

## Continuação — entrega CI e contrato de fila

A etapa seguinte corrigiu `.github/workflows/validate.yml`: publica o pacote
em caminho fixo `dist/smart-economy-director.zip`, sem versão duplicada, e
falha se o artefato não existir. O pacote continua contendo a versão atual em
seus descritores; CLI local sem --output mantém ZIP versionado. Sem mudança
no runtime/instalação 0.4.1.

Leia [QUEUE_CONTRACT.md](QUEUE_CONTRACT.md) para novas fontes da fila e a matriz
mínima ainda não executada. UI nativa expõe projetos/investidor/progresso, mas
isso não prova acesso por scripted effect. Supply Chain tem opções separadas
de ferrovia/energia/setores/admin que a flag geral de cadeias não protege.
61 testes e validação estática passaram; ZIP de CI conferido contra os 13
outputs. Nenhum jogo foi iniciado. O jogador enviou a auditoria para main;
o CI de `ada7c26` foi confirmado aprovado, sem inferir publicação de ZIP válido
pelo path antigo (upload-artifact pode só emitir warning).

## Orientação atual após auditoria — 2026-11-09

Leia [AUDIT_2026-11-09.md](AUDIT_2026-11-09.md) antes de continuar. Código auditado:
`ccf5c2ba325203faad9d704a1f139e21b8ce3261`, main, 0.4.1. Não houve alteração de
funcionalidade na auditoria. 61 testes do Director passaram agora; 26 da
referência passaram separadamente e seu validador tem 178 erros. A instalação
corresponde aos 13 outputs; isso não é comprovação de execução econômica.

Fase 0 parcial, diagnóstico parcialmente verificado, planejamento nacional
não implementado e executor experimental. Próximo bloco: contrato de fila,
reconciliação e opções dos outros executores, antes de novos tipos de obra ou
ranking. Sem leitura confiável dos projetos relevantes, não certificar
construção automática como segura. Não iniciar jogo oculto prolongado nem
alterar a campanha para obter candidatos.

Aprovação manual atual não exige pausa nem saldo positivo; exige Assistido,
elegibilidade, fora de default e fila privada vazia. Automático existe opt-in,
com guardas limitadas e sem teste de inclusão bem-sucedida na engine. Ignorar/
restaurar e diagnósticos 0.4.0/0.4.1 estão implementados e testados no harness,
mas sem cliques ou save/reload comprovados. As capturas de junho/1839 confirmam
texto do modo e bloqueio por fila ocupada, sem identificar commit da sessão.

GitHub main consultada pelo conector: `9366277…`; os dois commits de recursos
0.4.0/0.4.1 estavam locais no início da auditoria. Fetch/push por Git no shell
falham por DNS; o conector consegue ler. Não reescrever histórico para contornar.
Relatório/JSON publicados pelo conector no PR em rascunho #1:
https://github.com/Lincoln16yyy/SMART-ECONOMY-DIRECTOR/pull/1
A branch de auditoria usa a main remota 0.3.9 e não inclui os recursos locais
0.4.x; não confundir essa publicação documental com envio do código.

## Registros anteriores — consultar sua data e versão

Os resumos abaixo são históricos. Números de testes, exigência de pausa,
“sem modos” e próximos passos antigos não substituem a orientação da auditoria.
Referências a comportamento de pendências descrevem o script/harness, salvo
quando um teste de engine estiver explicitamente registrado.


O usuário solicitou seguir `Texto colado.txt` e ir publicando no GitHub
`Lincoln16yyy/SMART-ECONOMY-DIRECTOR`. O conteúdo original está preservado
integralmente em PROJECT_BRIEF.md. Leia-o antes de trabalhar.

Fase atual: ignorar e restaurar recomendações 0.4.1.
Instalada; backup `mod_0.4.0_20261109_103945_594880`; load order preservado. Cada cartão elegível tem
botão para ignorar apenas o tipo de expansão no estado. A variável estadual
permanece nas leituras e modos, bloqueia lista, aprovação e seleção automática.
O topo oferece restauração de todas as escolhas nos estados atuais do país,
com aviso enquanto existir escolha. Desativar limpa tudo. Obras enfileiradas
não são canceladas e restaurar não enfileira obras. Marcadores de pendência
continuam separados. Motivos de rejeição agora incluem escolhas ignoradas.
Os 61 testes passam; validação estática e conferência na engine seguem sendo
coisas distintas. Confirmar os novos botões, recarga com escolhas e layout no
jogo normal; não iniciar testes gráficos prolongados.

Estado anterior de referência: Fase atual: diagnóstico de rejeição de produtores locais 0.4.0.
Instalada localmente; backup `mod_0.3.9_20261109_102912_254983`; load order preservado. Quando um bem
está escasso e não há candidato, mostra quantidade de estados com produtor e
sete motivos principais disjuntos, da última leitura. Cada produtor estadual
entra no primeiro motivo aplicável: expansão pendente/enfileirada, incorporação,
nível/ocupação, contratação, insumos, método ativo e permissão. Não acrescenta
ações nem altera guardas. 57 testes passam, incluindo todos os bens, cascata,
reset e visibilidade; validação estática contra o jogo local passou.
As capturas enviadas pelo jogador mostram Império Otomano em 13 e 18/06/1839:
modo Automático e mensagem de filas ocupadas renderizados; última leitura
6/1839, 45 projetos públicos/2 privados, infraestrutura negativa zero, dois
setores de construção não operantes e ferro escasso sem produtor elegível.
Isso confirma apresentação do bloqueio, não inclusão de obra ou revisão neste
dia específico. Modo sob solicitação estava selecionado. Não iniciar teste
gráfico prolongado. Detalhamento novo e inclusão real seguem pendentes.

Continuação em 2026-11-09: a suíte foi retomada e os **51 testes passaram**.
O harness agora modela mercado/bens ausentes, métodos ativos, existência de
estado elegível e registro de eventos agendados. Foram atualizados cenários
históricos que ainda exigiam pausa/saldo positivo e ignoravam as oito marcas
estaduais de oferta. Novos cenários cobrem exclusividade dos modos, agendamento
sem duplicata, razões de bloqueio, máximo de uma ação com revalidação da fila,
e elegibilidade/expansão sem duplicata dos oito produtores. Esses resultados
são simulação dos scripts gerados, não confirmação da engine. Nenhum arquivo
carregável ou instalação foi alterado. Os números e regras das seções abaixo
são históricos; a conferência da revisão mensal em campanha segue pendente.

Fase anterior: protótipo da Fase 2 em 0.3.4. O jogador confirmou em campanha a
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

Instalação local 0.5.4: jogo fechado, backup `mod_0.5.3_20261109_122756_131472`, 13 arquivos conferidos com o pacote; configuração de carregamento preservada.

Conferência final da 0.6.0 inclui ocultação das listas vazias do plano,
115 testes aprovados e reinstalação dos 13 outputs com jogo fechado.
Backup dessa conferência em
`sed_backups/mod_before_0.6.0_20261109_220620_787220`.
O backup inicial `mod_before_0.6.0_20261109_220347_442062` conserva a 0.5.8.
