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
- Saves em `/home/lincoln-ii/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3/save games`.
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

A última entrega executou 361 testes sintéticos e instalou a versão 0.7.18
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
- Gerar e indexar a documentação exportada do jogo instalado.
- Confirmar em campanha a fundação, os PMs iniciais e a contratação da 0.7.15,
  além das leituras fiscais e de prontidão da 0.7.16.
- Confirmar save/reload, restauração e alterações fiscais em campanha.
