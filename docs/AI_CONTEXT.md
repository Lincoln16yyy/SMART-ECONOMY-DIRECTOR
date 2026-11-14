# Contexto de continuidade

## Estado atual
- **0.7.42 gerada, testada e instalada** (jogo fechado, backup `sed_backups/mod_before_0.7.42_20261114_005714_384642`, 14 arquivos, `descriptor.mod` 0.7.42). Melhorias sem mudar limiares: o status 22 (`sed_auto_status_budget`) agora mostra quanto ouro falta (`sed_build_budget_gold_gap`), e foram removidos resíduos mortos do antigo status 21/executor 12 (nada emitia `sed_auto_review_status = 21` desde 0.7.37). **Carregou 0.7.42: NÃO VERIFICADO.**
- **0.7.41:** adicionou `sed_build_budget_gold_gap = max(required_gold − gold_reserves, 0)` no texto do orçamento (leitura pura). Instalada; **Carregou: NÃO VERIFICADO.**
- **0.7.40 — Carregou (2026-11-13):** leitura tipada de bandeiras externas (presença para booleanas do Advisor/ARoAI, `> 0` só numéricas do Supply Chain). Reabertura final: `error.log` 108 linhas, **zero** comparações booleanas inválidas. Restaram 1.344 `Value of wrong type` (`aroai_preparation_effects.txt:47`) e 5 `Div/0`, todos do **ARoAI 1.3.5** (arquivos 2023, incompatível com 1.15) — **recomendado mantê-lo desativado**.
- **Kuromi's AI v8.0** (`3227982912`, 1.15.*): instalado em `mod/` com descritor `.mod`; auditado sem referências a `sed_*`/`aroai_*`/`advisor_*`/`zw_*` (IA/comportamento, sem conflito com o Director). Registrado em `ambiente-local.md` e `docs/COMPATIBILITY.md`.
- **Coordenação e Smart Construction do Advisor:** com Automático + `sed_coord_active`, `sed_coord_sync` remove as 7 opções externas e liga só a do executor do mês — religa o Smart Construction só quando executor = Advisor (1); em 0,2–11,13,5 fica suspenso. “Atualizar diagnóstico” não chama sync (revela estado). Sair do Automático/restaurar devolve o valor guardado na entrada; fora da coordenação o Director não toca na chave.

## Verificações desta sessão
- **Teste sintético:** 433 testes aprovados. **Estático:** `build_mod.py --check` e `validate.py --game "/home/lincoln-ii/Games/Victoria 3/game"` aprovados. **Entrega:** ZIP `dist/smart-economy-director-0.7.42.zip` e instalação local com backup.

## Pendências / bloqueios
- **Carregou/Campanha pendentes:** abrir jogo com 0.7.42 e conferir `error.log`; em campanha validar `gold_gap`/status 22, coordenação com mods externos, fallback Centro de Comércio, PMs/controle privado e roteiros de `docs/MANUAL_RUNTIME_TEST.md`.
- **Calibragem:** unificar duração (capacidade nacional 10 pts/sem) × teto de materiais (2 pts/sem) mudaria limiar ~5× — decisão de balanceamento do usuário; fatores 4×/6× da guarda fiscal precisam de save.
- **Sem primitiva legível (não scriptável sem evidência nova):** autor/investidor da obra, qualificações, salário por profissão, abrir rota/tarifa/subvenção, consumo real de tropas, custo incremental exato.

## Ambiente
- Repo: `/home/lincoln-ii/Victoria3_Mod-2`, branch `codex/verified-fiscal-readings`, remote `origin https://github.com/Lincoln16yyy/SMART-ECONOMY-DIRECTOR.git`.
- Jogo base: `/home/lincoln-ii/Games/Victoria 3/game`. User data/log: `~/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3/`.
- Comandos: `python3 tools/build_mod.py [--check]`, `python3 tools/validate.py --game "<game>"`, `python3 -m unittest discover -s tests -q`, `python3 tools/package_mod.py`, `python3 tools/install_mod.py --user-data "<user data>"`. Instalar só com jogo fechado (`pgrep -x victoria3.exe`). `common/`, `events/`, `gui/` gerados pelo gerador.
