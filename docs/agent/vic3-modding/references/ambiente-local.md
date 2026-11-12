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

A última entrega executou 382 testes sintéticos e instalou a versão 0.7.27
com conferência de 14 arquivos. O último `--check` confirmou sincronia.
[confirmado 2026-11-11]

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
