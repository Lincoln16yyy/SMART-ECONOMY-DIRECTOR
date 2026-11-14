# Ambiente local confirmado

Os registros abaixo foram conferidos em 2026-11-11. Atualize os dados quando
houver mudança observada no ambiente.

## Sistema

- CachyOS Linux, conforme `/etc/os-release`. [confirmado 2026-11-11]
- Shell `/usr/bin/bash`, conforme `/proc/$$/exe`. [confirmado 2026-11-11]
- Python 3.14.9, conforme `python3 --version`. [confirmado 2026-11-11]
- Executável Windows em `/home/lincoln-ii/Games/Victoria 3/binaries/victoria3.exe`
  e dados em um prefixo Wine do Hydra. Os arquivos e diretórios existem.
  O comando exato de inicialização e a camada de compatibilidade em execução
  ainda precisam de confirmação. [confirmado 2026-11-11]

## Caminhos

- Jogo base em `/home/lincoln-ii/Games/Victoria 3/game`, usado em leitura.
- Dados do usuário em `/home/lincoln-ii/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3`.
- Director instalado em `/home/lincoln-ii/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3/mod/Smart Economy Director`.
- Log em `/home/lincoln-ii/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3/logs/error.log`.
- Advisor em `/home/lincoln-ii/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3/mod/3778129206_Economy_Advisor`.
- Supply Chain em `/home/lincoln-ii/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3/mod/3357811223_Supply_Chain_Semi-Auto_Builder`.
- Controllable Private Construction em `mod/3278770055_Controllable_Private_Construction`
  (Workshop 3278770055; sem `descriptor.mod`, só `.metadata/metadata.json`).
  O jogador mantém esse mod ativo. [confirmado 2026-11-11]
- Private Investments Only Expand Existing Buildings em
  `mod/3278371002_Private_Investments_Only_Expand_Existing_Buildings`
  (mesmo autor, mesma técnica; o jogador não citou como ativo).
  [confirmado 2026-11-11]
- Saves em `/home/lincoln-ii/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3/save games`.
- Smart Government Advisor em `mod/Smart Government Advisor` (1.0.0,
  `supported_version 1.15.*`, do jogador). Define `sg_enabled`,
  `sg_schema_version` (esquema 2), `sg_top_1..3_law` com ids de
  `data/law_ids.json`, `sg_ignored_*` e diário próprio. [confirmado 2026-11-11]
- Backups em `/home/lincoln-ii/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3/sed_backups`.

Todos esses caminhos existem. [confirmado 2026-11-11]

A pasta `/home/lincoln-ii/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3/docs` está ausente. A documentação exportada ainda precisa
ser gerada. [confirmado 2026-11-11]

## Ferramentas

- `vic3-tiger` 1.19.0 disponível em
  `/home/lincoln-ii/Victoria3_Mod-2/dist/tools/vic3-tiger-1.19.0/vic3-tiger-linux-v1.19.0/vic3-tiger`.
  Obtido do release oficial `amtep/tiger` v1.19.0. O binário declara suporte
  ao Victoria 3 1.13.5 e avisa sobre o jogo instalado 1.15.0.
- Cargo disponível em `/usr/bin/cargo`.
- Configuração do projeto em `vic3-tiger.conf`, com inglês e português brasileiro.
- Comando executado e conferido

```bash
dist/tools/vic3-tiger-1.19.0/vic3-tiger-linux-v1.19.0/vic3-tiger --game '/home/lincoln-ii/Games/Victoria 3' --config vic3-tiger.conf --no-color --json '/home/lincoln-ii/Victoria3_Mod-2'
```

O argumento `--game` usa a pasta principal do jogo. O relatório aponta três
campos de diário confirmados no vanilla 1.15 e avisos de estilo. As correções
0.7.16 retiraram os nove apontamentos de leitura removida e o aviso de escopo
na prontidão militar. A execução completa consta nos registros da entrega.

[confirmado 2026-11-11]

## Comandos verificados

Estes comandos foram executados neste projeto. A validação Tiger permanece
pendente. A instalação registra backup e verifica os arquivos do pacote.

```bash
python3 tools/build_mod.py
python3 tools/build_mod.py --check
python3 tools/validate.py --game '/home/lincoln-ii/Games/Victoria 3/game'
python3 -m unittest discover -s tests -q
python3 tools/package_mod.py
python3 tools/install_mod.py --user-data '/home/lincoln-ii/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3'
```

A 0.7.33 executou 419 testes sintéticos (186 s), `--check` sincronizado,
validação local aprovada e Tiger 1.19.0 com 0 fatais, 3 `unknown-field` de
diário do vanilla 1.15 e 949 avisos. Instalação local da 0.7.33 confirmada:
14 arquivos, backup em
`sed_backups/mod_before_0.7.33_20261112_201035_100577`, ordem de mods
inalterada e `descriptor.mod` instalado com `version="0.7.33"`. O
`logs/error.log` da sessão anterior (0.7.30, 1832 linhas) não tem nenhuma
referência a `sed_`. Nenhuma partida foi aberta com a 0.7.33.
[confirmado 2026-11-12]

### Conferir se o jogo está fechado antes de instalar

`pgrep -f "binaries/victoria3.exe"` **não serve**: o próprio comando contém o
padrão, então o `pgrep` casa com a linha de comando do shell que o executa e
reporta "jogo aberto" sempre. Isso abortou duas instalações (0.7.34 e 0.7.35)
antes de perceber. Use um destes:

```bash
pgrep -x victoria3.exe || echo fechado
ps -eo pid,args | grep -i victoria | grep -v grep | grep -v "ps -eo"
```

[confirmado 2026-11-12 — sem processo `victoria3.exe` e instalação da 0.7.35
concluída: 14 arquivos, backup em
`sed_backups/mod_before_0.7.35_20261112_211602_983311`, ordem de mods
inalterada, `descriptor.mod` = 0.7.35]

## Documentação exportada do jogo

A geração local de `script_docs` e `dump_data_types` permanece pendente.
Os passos de inicialização em debug, abertura do console e diretório final
precisam ser confirmados na engine antes de serem registrados como verificados.

## Evidência de comportamento

- No vanilla 1.15 instalado, `earnings` é valor adicionado semanal de escopo de
  prédio: `EARNINGS_BREAKDOWN` mostra `Value: GetEarnings` contra
  `Revenue: GetLastRevenue` mais despesas de material, e
  `BUILDING_BALANCE_BREAKDOWN` chama essa base de "Weekly Revenue".
  `TOOLTIP_BUILDING_HEALTH_WORLD` mostra `Earnings` ao lado de
  `GetLastWagesExpenses`, e `TRIGGER_WEEKLY_PROFIT` confirma `weekly_profit`.
  Todos em `localization/english/interfaces_l_english.yml` e
  `triggers_l_english.yml`. [confirmado 2026-11-11]

- A captura enviada pelo usuário mostrou a construção básica de papel
  permitida, com 30 de madeira e 40 de papel por nível. A captura confirma
  essa previsão da interface. A construção automática da 0.7.15 e sua
  contratação real ainda precisam de confirmação. [confirmado 2026-11-11]
- Os testes sintéticos executam o subconjunto modelado por
  `tests/script_harness.py`. Os resultados são registrados como Teste sintético.

## Pendências

- Reavaliar os alertas Tiger quando houver versão compatível com o jogo 1.15.
- Comparação com bloco de valor à direita é forma vanilla: `net_fixed_income >=
  { ... }` em `common/diplomatic_actions/30_fund_lobby.txt`. [confirmado 2026-11-11]
- Comércio não é scriptável na 1.15: a sondagem de `create_trade_route` em mod
  isolado fez o Tiger 1.19.0 responder "removed in 1.9 — replaced with world
  trade system". O binário só mantém comandos internos. Não insistir nesse
  caminho. [confirmado 2026-11-11]
- Sondagem de primitiva desconhecida: criar pasta temporária com
  `common/scripted_effects/probe.txt` e `.metadata/metadata.json` mínimo e rodar
  `vic3-tiger --game '<jogo>' <pasta>`. O relatório responde se o efeito existe,
  foi removido ou quais campos aceita. [confirmado 2026-11-11]
- Gerar e indexar a documentação exportada do jogo instalado.
- Confirmar em campanha a fundação, os PMs iniciais e a contratação da 0.7.15,
  além das leituras fiscais e de prontidão da 0.7.16.
- Confirmar save/reload, restauração e alterações fiscais em campanha.

## Sondagem de primitivas: comércio e formato de opção de evento (2026-11-11)

Pasta temporária com `.metadata/metadata.json` e `common/scripted_effects/probe.txt`,
validada com o Tiger 1.19.0 (`--game '/home/lincoln-ii/Games/Victoria 3'`):

- `create_trade_route` → `warning(removed): was removed in 1.9`, "replaced
  with world trade system". Não usar.
- `add_trade_route_level`, `cancel_trade_route`, `establish_trade_route` →
  `error(unknown-field): unknown token`. Não existem como efeito de script.
- Conclusão: script só lê comércio (pedidos, faixa de preço, escassez). Abrir
  rota é ação da UI/IA do jogador.

- Tarifa e subvenção (sondagem 2026-11-12, `/tmp/sed_tariff`, Tiger 1.19.0):
  `set_tariff`, `set_tariffs`, `set_tariff_rate`, `add_tariff`,
  `set_trade_route_tariff`, `set_goods_tariff`, `set_subvention`,
  `add_subvention`, `set_goods_subvention`, `set_market_subvention`,
  `add_tariff_to_goods`, `set_country_tariff` e `change_tariff` são todos
  `unknown token`. O sistema de presença/vantagem da 1.9+ não tem efeito de
  script; não insistir nesse caminho. [confirmado 2026-11-12]

Formato de evento (vanilla `events/1848.txt`, evento `1848.1`): `type`, `placement`,
`title`, `desc`, `flavor`, `duration`, `icon`, `on_created_soundeffect`,
`trigger`, `immediate` e `option` com `name`, `custom_tooltip`, `ai_chance`,
`default_option` e **efeitos inline**. `effect = { ... }` dentro de `option` é
`unknown-field` na 1.15. Ícones disponíveis em
`game/gfx/interface/icons/event_icons/` (`event_industry.dds` usado na 0.7.21).

`duration` do evento é tratado como meses na documentação interna do mod;
semântica e escolha automática ao expirar seguem NÃO VERIFICADO.

## Sondagem: duração da fila de construção (2026-11-11)

`/tmp/sed_dur` (metadata + `common/scripted_effects/probe.txt`), Tiger 1.19.0,
zero erros:

- `construction_queue_duration`, `construction_queue_government_duration` e
  `construction_queue_private_duration` são triggers de país relativos ao tempo
  restante da fila em **semanas** (`triggers_l_english.yml`: "Remaining duration
  of construction queue is X weeks").
- Aceitam comparação contra script value à direita: `... > var:probe_b` passou.
- São triggers, não script values: não dá para ler o número. Para exibir, usar
  cadeia `if/else_if` com faixas (ver `queue_bands()` em
  `tools/construction_budget.py`).
- `if` dentro do `value = { }` de `set_variable` é `unknown-field`: efeitos
  condicionais precisam ficar fora do cálculo (comportamento do Tiger já
  conhecido, reconfirmado aqui).

## Sondagem: autor/investidor da fila e contagens de projeto (2026-11-11)

`/tmp/sed_dur` com Tiger 1.19.0:

- Existem e são de **país**: `num_queued_constructions`,
  `num_queued_government_constructions`, `num_queued_private_constructions`
  (projetos, não níveis). Usar em escopo de estado gera
  `warning(scopes): ... is for country`.
- `is_under_construction` existe em escopo de **prédio**
  (`b:building_x = { is_under_construction = yes }`).
- Não existem (todos `error(unknown-field)`): `is_government_construction`,
  `is_privately_constructed`, `construction_owner_is_government`,
  `construction_queue_size`.
- Conclusão: autor/investidor por item não é scriptável na 1.15. Não prometer
  reconciliação de identidade; usar as contagens por lado e as marcas próprias.

## Regra do validador: aritmética em igualdade de variável (2026-11-11)

`tools/validate.py` recusa `var:x = { value = year subtract = 1 }` com
"Inline arithmetic in variable equality requires a named script value". Para
comparar com um valor calculado, criar variável própria no início do efeito
(ex.: `sed_prev_year = year - 1`) e comparar `var:x = var:sed_prev_year`.

## Sondagem: qualificação e salário por profissão (2026-11-11)

`/tmp/sed_dur`, Tiger 1.19.0 — todos `error(unknown-field)`:
`pop_qualifications`, `state_pop_qualifications`, `has_pop_qualifications`,
`wages`, `wage_rate`, `average_wage`.

O que existe: `average_sol` (leitura, país) e o efeito `set_pop_qualifications`
(escrita, `common/effect_localization/00_pop_effects_loc.txt`). Modificadores de
qualificação são só `*_mult` em leis/tecnologias, não leitura de estoque.

Conclusão: não prometer filtro por qualificação nem salário por profissão. Proxy
do mod: `occupancy` + `has_failed_hires`; salário observado sai de
`earnings - weekly_profit` por prédio.

## Mod de construção privada do jogador: Controllable Private Construction (2026-11-11)

Lido em `mod/3278770055_Controllable_Private_Construction` (Workshop 3278770055,
autor `zw_*`). Nada dele foi alterado. É o mod que o jogador "sempre ativa".

Mecânica, com evidência dos arquivos dele:

- `common/buildings/zw_cpc_0*.txt` usam `INJECT_OR_CREATE:building_<x> = { ... }`
  para sobrescrever `can_build_private` e `can_build_government` em cada prédio.
  Os testes chamam `zw_trigger_autonom_investment_<ramo>` e
  `zw_trigger_gov_investment`, que leem `scope:investor_country` e variáveis de
  país. Conclusão: **é possível restringir a autoexpansão privada nativa**, mas
  só por injeção em `can_build_private` (campo por prédio).
- `common/scripted_triggers/zw_cpc_triggers_auto_expand.txt` usa
  `REPLACE:default_auto_expand_rule`, contra o vanilla
  `game/common/scripted_triggers/00_scripted_triggers.txt:985`
  (`cash_reserves_ratio > 0.95`, `state.market_access >= 0.95`,
  `occupancy >= 0.95`). O mod troca por lucro semanal ≥ 200 × nível etc.
  Os grupos de prédio apontam para essa regra em `should_auto_expand`
  (`game/common/building_groups/00_building_groups.txt`).
- Botões em `common/scripted_buttons/` e diário
  `je_zw_autonom_invest_management` (loc pt-br mantém o nome em inglês,
  "Private Constructions Management"). Cada botão liga/desliga uma variável de
  país `zw_var_auto_invest_*` / `zw_var_no_foreign_private_investment_*` /
  `zw_var_intervene_investment_from_abroad_*`; presença = restrição ligada.
- `decree_zw_no_state_private_investment` ("Ban Private Constructions", custo 0,
  só jogador) bloqueia construção privada no estado; é decreto, ocupa slot.
- Os dois modificadores de intervenção em investimento estrangeiro custam
  `country_bureaucracy_mult = -0.05`.

Regra para o Director: **ler** essas variáveis é seguro (`has_variable`;
ausente = falso). **Escrever** é variável externa para `tools/validate.py`, e
injetar `can_build_private` nos mesmos prédios colide com a injeção do outro mod
(mesma chave; a ordem de carregamento define o vencedor, sem aviso). Por isso a
0.7.27 só lê. [confirmado 2026-11-11]

Tiger 1.19.0 rodado só na pasta dele
(`vic3-tiger --game '<jogo>' '<pasta do mod>'`): 0 erros, 88 avisos; portanto
`INJECT_OR_CREATE:` em `common/buildings/` e `REPLACE:` em scripted trigger são
formas aceitas na 1.15. [confirmado 2026-11-11]

Se um dia for preciso controlar de fato, a alternativa é oferecer o próprio
`can_build_private` e pedir ao jogador para desativar o outro mod — não rodar
os dois.

## Mods de PM instalados (2026-11-11)

- **Auto-Apply PMs** (`mod/3353797125_Auto-Apply_PMs`, z.260514.1): um botão por
  prédio no diário `je_zw_auto_pm`; liga/desliga `zw_var_auto_pm_building_<prédio>`
  (`building_` removido). Botões de grupo ligam
  `zw_var_auto_pm_building_group_farms` / `_mines` / `_plantations`, e nesse caso
  o efeito roda por prédio do grupo. Ajustes globais: `zw_var_auto_pm_num_3`,
  `_higher_frequency`, `_electric`. Os métodos são decididos por
  `zw_effect_auto_pm_building_<prédio>`, que usa preço local e
  `can_activate_production_method`; escreve no mesmo grupo principal que o
  Director moderniza. [confirmado 2026-11-11]
- **Auto-Apply Automation PMs** (`mod/3344726320_Auto-Apply_Automation_PMs`):
  variáveis `zw_var_auto_pm_automation_basic` / `_electric` / `_oil` /
  `_transportation` / `_slower_automation`; mexe em PMs de automação e
  transporte por estado (`zw_effect_change_state_pm_automation` /
  `_transportation`). [confirmado 2026-11-11]
- Ordem de carregamento não é controlada por nós. Para leitura por
  `has_variable`, ordem não importa; para injeção em prédio, importa.

## Evidência de comércio e Centro de Comércio (2026-11-12)

- `building_trade_center` é construível pelo governo e por investidores privados:
  `can_build_government`/`can_build_private` leem
  `trade_center_construction_allowed` (`common/buildings/` do 1.15 instalado).
- `required_construction = construction_cost_very_low`; o valor está em
  `common/script_values/building_values.txt:7` e vale **100 pontos** de
  construção (usado em `tools/construction_budget.py` como
  `TRADE_CENTER_POINTS`).
- Capacidade de comércio é gerada por nível de Centro de Comércio e consumida
  pelo Mercado Mundial (`concept_trade_capacity_desc`). O script não abre rota
  (`create_trade_route` removido na 1.9); o caminho de script é ampliar/fundar
  o prédio.
- `law_isolationism` desliga o comércio com o Mercado Mundial
  (`country_disallow_trade_bool = yes`), então capacidade extra é inútil sob
  essa lei.
- Tiger 1.19.0 na 0.7.30: 0 fatais, 3 `unknown-field` de diário (os mesmos do
  vanilla 1.15) e **938** avisos (933 na 0.7.29; os cinco novos vêm das caixas
  de texto do painel). O binário continua declarando suporte até 1.13.5.
  [confirmado 2026-11-12]

[confirmado 2026-11-13 — instalação da 0.7.38 concluída com jogo fechado
(`pgrep -x victoria3.exe` sem processo): 14 arquivos, backup em
`sed_backups/mod_before_0.7.38_20261113_211121_616441`, ordem de mods
inalterada, `descriptor.mod` = `version="0.7.38"`. Pacote em
`dist/smart-economy-director-0.7.38.zip`. Conferido no arquivo instalado:
`sed_build_budget_funding_weeks` sem `min = 26` e a guarda fiscal com a
ramificação de déficit a `multiply = 6`. Nenhuma partida aberta com a 0.7.38;
evidência Carregou continua pendente.]

[confirmado 2026-11-13 — instalação da 0.7.39 com jogo fechado: 14 arquivos,
backup em `sed_backups/mod_before_0.7.39_20261113_214040_320070`, ordem de mods
inalterada, `descriptor.mod` = `version="0.7.39"`. Conferido no instalado: loc
`sed_meta_grain_result` nos dois idiomas, `goal_result_years` em
`common/scripted_effects/sed_effects.txt` e a linha no
`gui/journal_entry_widgets/sed_diagnostics.gui`. Nenhuma partida aberta.]

### Ler o error.log — primeira evidência Carregou (2026-11-13)

O log fica em `.../Documents/Paradox Interactive/Victoria 3/logs/error.log` e
é reescrito a cada abertura; confira `ls -l --time-style=full-iso` antes de
interpretar. Padrões úteis:

```bash
grep -o "sed_triggers.txt:[0-9]*" "$LOG" | sort | uniq -c | sort -rn | head
grep -v "Script location:" "$LOG" | grep -v "^common/" | sed -E 's/[0-9]+/N/g' | sort | uniq -c | sort -rn
```

Resultado da 0.7.39 (jogo aberto pelo usuário, 8.151 linhas): 1.627
`Left side and right side during comparison were of different types (left was
'boolean', right was 'value')` em `sed_triggers.txt:2747/2754/2691/3866/3867`.
Causa provada nos mods instalados: `advisor_enabled` e
`advisor_auto_construction_enabled` são criados pelo Economy Advisor com
`set_variable = <flag>` (nulo de valor ⇒ booleano; `decisions/advisor_decisions.txt:19`,
`scripted_guis/advisor_scripted_guis.txt:415`), e `aroai_autobuild` pelo ARoAI
do mesmo jeito (`events/aroai_autobuild_events.txt:39`). As opções do Supply
Chain são numéricas (`scripted_buttons/zw_scsab_buttons.txt:580`). Regra: nunca
comparar com `> 0` uma bandeira que o dono grava com `set_variable` nu.

Também aparecem 16 `Failed to approximate weeks left in construction queue: The
total construction speed is zero` — mensagem do vanilla com fila vazia, sem
relação com `sed_`.

[instalação da 0.7.40: jogo fechado, 14 arquivos, backup em
`sed_backups/mod_before_0.7.40_20261113_222607_201024`, ordem de mods inalterada,
zero ocorrências de `var:advisor_enabled > 0`, `var:advisor_auto_construction_enabled > 0`
e `var:aroai_autobuild > 0` nos três arquivos instalados. Log limpo confirmado na
terceira leitura (seção seguinte).]

### Diagnóstico do log de segunda leitura (2026-11-13, 0.7.40)

Após corrigir as comparações booleanas, o log da 0.7.40 tem 381.855 bytes,
com estas mensagens distintas, todas vindas de outros mods (não de `sed_`):

- 1.300 `start_building_construction returned false` em
  `common/scripted_effects/aroai_construction_effects.txt:377` — o ARoAI tenta
  construir edifícios que não estão no seu banco: `building_war_machine_industry`,
  `building_tooling_workshops`, `building_textile_mills`, `building_synthetics_plants`,
  `building_steel_mills`, `building_shipyards`, `building_paper_mills`,
  `building_naval_base`, `building_munition_plants`, `building_furniture_manufacturies`,
  `building_chemical_plants`, `building_barracks`, `building_arts_academy`. São
  edifícios do ARoAI que o jogo não reconhece. Erro do ARoAI.
- 123 `has_potential_resource returned false` em
  `aroai_evaluation_triggers.txt` — `target: Not found in database class
  CBuildingDatabase` (mesmo grupo de edifícios). Erro do ARoAI.
- 52 `remove_building returned false` no `aroai_preparation_effects.txt` (mesmo
  grupo). Erro do ARoAI.
- 50 `start_building_construction` por um **reator** do ARoAI (loop de construção
  fora do Escopo Common, 50×), e 26 do `aroai_preparation_effects`. Extraídos de
  `aroai_construction_effects.txt` (linhas 284/377 e 1273/1280/1285/1490 etc.).
- 48 `Failed to approximate weeks left in construction queue: The total construction
  speed is zero` (mesma do vanilla; fila vazia).

Nenhuma linha com `var:advisor_enabled > 0`, `var:advisor_auto_construction_enabled > 0`
ou `var:aroai_autobuild > 0` depois da correção. Os erros de comparação booleanas
(the "jomini_script_system_error") sumiram. O ARoAI é o responsável de todos os
demais avisos; não são do Director.

### Terceira leitura do log — 0.7.40 confirmada (2026-11-13 22:49)

Reabertura depois de desativar o ARoAI: `error.log` de 16.116 bytes e 108 linhas.
Zero `Left side and right side during comparison were of different types` — a
correção da 0.7.40 está confirmada na engine. O que sobra:

- 1.344 `Value of wrong type` em `common/scripted_effects/aroai_preparation_effects.txt:47`
  (o ARoAI grava `none` onde o jogo espera valor);
- 5 `Division by zero` em `aroai_preparation_effects.txt:834` e
  `script_values/aroai_preparation_values.txt:232`.

Tudo do ARoAI, nada de `sed_`. Conclusão registrada: manter o ARoAI **desativado**
nesta campanha; ele é incompatível com a 1.15 na prática (arquivos de 2023,
`supported_game_version` vazio).

### Kuromi's AI v8.0 — auditoria e instalação (2026-11-14)

Origem: `~/Downloads/3227982912_Kuromi__x27_s_AI(1).zip`. Conteúdo conferido:
`supported_game_version "1.15.*"`, `common/ai_strategies/00_default_strategy.txt`
mais `kai_*`, `common/defines/kai_ai.txt`, `INJECT:` em prédios (incluindo
`building_construction_sector`, só com `ai_value`), leis, tratados, mobilização,
botões, triggers e values. Varredura por `sed_*, aroai_*, advisor_*, zw_*`: zero
ocorrências — sem cruzamento com o Director nem com os adaptadores de coordenação.

Instalado com o jogo fechado, sem sobrescrever nada: pasta
`mod/3227982912 Kuromi's AI` e descritor `mod/3227982912 Kuromi's AI.mod`
criado à mão (`version="8.0"`, `name="Kuromi's AI"`, `supported_version="1.15.*"`,
`path="mod/3227982912 Kuromi's AI"`). O zip não traz `.mod`, então sem esse
arquivo o launcher não lista o mod.

[instalação da 0.7.41: jogo fechado, 14 arquivos, backup em
`sed_backups/mod_before_0.7.41_20261113_235654_504707`, ordem de mods inalterada,
`descriptor.mod` = `version="0.7.41"`, `sed_build_budget_gold_gap` presente no
efeito instalado e nos dois idiomas da localização. Reabrir o jogo: PENDENTE.]

[instalação da 0.7.42: jogo fechado, 14 arquivos, backup em
`sed_backups/mod_before_0.7.42_20261114_005714_384642`, ordem de mods inalterada,
`descriptor.mod` = `version="0.7.42"`. Status 22 mostra `sed_build_budget_gold_gap`
e resíduos do status 21/executor 12 removidos dos artefatos instalados. Reabrir
o jogo: PENDENTE.]


[instalação da 0.7.44: jogo fechado, 14 arquivos, backup em
`sed_backups/mod_before_0.7.44_20261114_014619_131213`, ordem de mods inalterada,
`descriptor.mod` = `version="0.7.44"`, ZIP
`dist/smart-economy-director-0.7.44.zip`. Inclui 0.7.43 (`sed_build_budget_gold_gap`
no bloqueio atual `sed_auto_current_budget`) e 0.7.44 (eventos didáticos do
Assistido `sed_pulse.21`–`29`, por objetivo, sem enfileirar; cooldown
`sed_assist_notice_month`). Reabrir o jogo e validar em campanha: PENDENTE.]
