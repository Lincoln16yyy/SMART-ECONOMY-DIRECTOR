# Contexto de continuidade

## Estado atual
- **0.7.44 gerada, testada, empacotada e instalada** (jogo fechado, backup `sed_backups/mod_before_0.7.44_20261114_014619_131213`, 14 arquivos, `descriptor.mod` 0.7.44, ZIP `dist/smart-economy-director-0.7.44.zip`). Inclui 0.7.43 e 0.7.44.
- **0.7.43 (incluída):** o bloqueio atual de orçamento (`sed_auto_current_budget`) também mostra quanto ouro falta para a guarda liberar (`sed_build_budget_gold_gap`), alinhado ao plano e ao status 22.
- **0.7.44:** modo Assistido passa a disparar eventos didáticos (`sed_pulse.21`–`29`, por objetivo) quando há recomendações (`sed_plan_count > 0`): cada aviso explica o motivo da recomendação (infraestrutura, escassez de bens, capacidade de construção, finanças, indústria ausente, burocracia, tributação, diversificação ou energia cara) e orienta abrir o Diário para aprovar item a item. Não enfileira nada; opções permitem atualizar/revisar, adiar ou silenciar (cooldown por `sed_assist_notice_month`). **Carregou/Campanha 0.7.43/0.7.44: NÃO VERIFICADO.**
- **Base anterior (0.7.40–0.7.42):** leitura tipada de bandeiras externas (0.7.40; Carregou 2026-11-13: 108 linhas no log, 0 comparações booleanas; ruído restante do ARoAI 1.3.5 incompatível com 1.15, recomendado desativado). `sed_build_budget_gold_gap` no orçamento (0.7.41) e no status 22 + limpeza de resíduos mortos do status 21/executor 12 (0.7.42). Coordenação: com Automático+`sed_coord_active`, `sed_coord_sync` liga só o executor do mês (Smart Construction do Advisor só com executor 1); "Atualizar diagnóstico" não chama sync. Kuromi's AI v8.0 instalado, sem conflito com `sed_*`.

## Verificações desta sessão
- **Teste sintético:** 433 testes aprovados (`python3 -m unittest discover -s tests -q`). **Estático:** `python3 tools/build_mod.py --check` e `python3 tools/validate.py --game "/home/lincoln-ii/Games/Victoria 3/game"` aprovados. **Entrega:** pacote e instalação local (jogo fechado) concluídos com backup.

## Pendências / bloqueios
- **Carregou/Campanha pendentes:** abrir jogo com 0.7.44 e conferir `error.log`; validar em campanha os eventos didáticos do Assistido (disparo, texto/motivo, cooldown, sem enfileirar) e `gold_gap` no bloqueio atual; seguir roteiros de `docs/MANUAL_RUNTIME_TEST.md`.
- **Calibragem:** unificar duração (capacidade nacional 10 pts/sem) × teto de materiais (2 pts/sem) mudaria limiar ~5× — decisão de balanceamento do usuário; fatores 4×/6× da guarda fiscal precisam de save.
- **Sem primitiva legível (não scriptável sem evidência nova):** autor/investidor da obra, qualificações, salário por profissão, abrir rota/tarifa/subvenção, consumo real de tropas, custo incremental exato.

## Ambiente
- Repo: `/home/lincoln-ii/Victoria3_Mod-2`, branch `codex/verified-fiscal-readings`, remote `origin https://github.com/Lincoln16yyy/SMART-ECONOMY-DIRECTOR.git`.
- Jogo base: `/home/lincoln-ii/Games/Victoria 3/game`. User data/log: `~/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3/`.
- Comandos: `python3 tools/build_mod.py [--check]`, `python3 tools/validate.py --game "<game>"`, `python3 -m unittest discover -s tests -q`, `python3 tools/package_mod.py`, `python3 tools/install_mod.py --user-data "<user data>"`. Instalar só com jogo fechado (`pgrep -x victoria3.exe`). `common/`, `events/`, `gui/` gerados pelo gerador.
