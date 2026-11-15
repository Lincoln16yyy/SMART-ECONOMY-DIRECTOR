# Contexto de continuidade

## Estado atual
- **CWE fiscal e escassez:** instalado. Director avalia imposto e salários em revisão mensal, inclusive com OGAS dono da fila. Salários militares têm guarda de prontidão. OGAS prioriza produtores ativos do bem em falta quando crescimento está ligado. Doze testes focados. Save/reload e campanha NÃO VERIFICADOS.
- **Smart Government para CWE:** pacote separado em `dist/smart-government-advisor-cwe.zip`, gerado da cópia local do projeto de leis e das definições CWE. 211 leis em 60 grupos, sete excluídas das sugestões por requisitos ausentes. Instalado e ativo após Cold War Era, OGAS e Director. Carregamento em campanha NÃO VERIFICADO.
- **Crescimento automático do CWE:** decisão instalada no OGAS que ativa construção, ferrovias, setores, métodos e gestão de mão de obra. Meta de fila de 12 semanas e pausa de novas obras quando faltar caixa, renda ou capacidade. Nove testes focados aprovados, campanha pendente.
- **OGAS para CWE:** adaptado localmente e ativo entre Cold War Era e Director. Migração do prédio de roupas para `building_clothes_factory` e retirada de trigger inválido sem chamadas eliminaram os erros no Tiger. Director cede a fila ao gerenciador geral do OGAS e deixa ferrovias ao gerenciador dedicado. Sete testes sintéticos. Campanha pendente.
- **Diário do Director CWE:** instalado em 0.7.46 com status da construção e confirmação pela fila pública. Cinco testes sintéticos e Tiger sem apontamentos para a edição. A sessão anterior avançou em janeiro de 1950 com as decisões visíveis. Diário atualizado e construção em campanha pendentes.
- **Perfil ativo:** Cold War Era 0.99 (commit `4d301a80`) seguido de OGAS para CWE e Director CWE 0.7.46. Ambos declaram 1.15.1. O executável local é 1.15.0. A conversão iniciou e registrou erros próprios de script e GUI. Perfil anterior e revisão CWE para 1.14.5 em `sed_backups/profile_before_cwe_play_20261115_172151_124926`. Better Politics 2.5.47 segue instalado fora do perfil ativo.
- **0.7.46:** após bloqueio por fila privada ou pausa, o Automático verifica a cada sete dias. No mesmo mês, só recalcula quando a trava sai ou outro limite interrompe a espera. Ao virar o mês, roda a revisão completa. Pacote em `dist/smart-economy-director-0.7.46.zip`. Instalada com backup `sed_backups/mod_before_0.7.46_20261115_164836_978933`. **Teste sintético:** 436 testes aprovados. Save/reload em campanha pendente.
- **0.7.45:** o Automático guarda imposto e salário civil no primeiro passo aplicável. O Diário distingue os cinco bloqueios de orçamento direto e mostra a diferença de ouro apenas no caso de reserva insuficiente. A última revisão conserva seu status. Pacote em `dist/smart-economy-director-0.7.45.zip`.
- **Instalação anterior: 0.7.44** (jogo fechado, backup `sed_backups/mod_before_0.7.44_20261114_014619_131213`, 14 arquivos, `descriptor.mod` 0.7.44, ZIP `dist/smart-economy-director-0.7.44.zip`). Inclui 0.7.43 e 0.7.44.
- **0.7.43 (incluída):** o bloqueio atual de orçamento (`sed_auto_current_budget`) também mostra quanto ouro falta para a guarda liberar (`sed_build_budget_gold_gap`), alinhado ao plano e ao status 22.
- **0.7.44:** modo Assistido passa a disparar eventos didáticos (`sed_pulse.21`–`29`, por objetivo) quando há recomendações (`sed_plan_count > 0`): cada aviso explica o motivo da recomendação (infraestrutura, escassez de bens, capacidade de construção, finanças, indústria ausente, burocracia, tributação, diversificação ou energia cara) e orienta abrir o Diário para aprovar item a item. Não enfileira nada; opções permitem atualizar/revisar, adiar ou silenciar (cooldown por `sed_assist_notice_month`). **Carregou/Campanha 0.7.43/0.7.44: NÃO VERIFICADO.**
- **Base anterior (0.7.40–0.7.42):** leitura tipada de bandeiras externas (0.7.40; Carregou 2026-11-13: 108 linhas no log, 0 comparações booleanas; ruído restante do ARoAI 1.3.5 incompatível com 1.15, recomendado desativado). `sed_build_budget_gold_gap` no orçamento (0.7.41) e no status 22 + limpeza de resíduos mortos do status 21/executor 12 (0.7.42). Coordenação: com Automático+`sed_coord_active`, `sed_coord_sync` liga só o executor do mês (Smart Construction do Advisor só com executor 1); "Atualizar diagnóstico" não chama sync. Kuromi's AI v8.0 instalado, sem conflito com `sed_*`.

## Auditoria da 0.7.44
- Revisados 33 commits marcados Codebuff e a evolução posterior dos fluxos. Inventário e achados em `docs/PHASE_LOG.md`.
- **Código:** efeito dos avisos didáticos definido e sem chamada. Fora do escopo atual, que é o Automático.
- **Código:** captura fiscal pode ocorrer sem alteração de nível, texto de ouro confunde outros bloqueios e duração de fila acima de 260 semanas aparece como 260. Save/reload e testes de campanha seguem pendentes.

## Verificações da 0.7.45
- **Teste sintético:** 435 testes aprovados. **Estático:** build --check e validate --game aprovados. Pacote conferido com unzip -t.

## Pendências / bloqueios
- **Carregou/Campanha 0.7.45: NÃO VERIFICADOS.** Próximo passo: roteiro 0.7.45 em `docs/MANUAL_RUNTIME_TEST.md`, com save/reload no mesmo mês e saída do Automático.
- **Calibragem:** unificar duração (capacidade nacional 10 pts/sem) × teto de materiais (2 pts/sem) mudaria limiar ~5× — decisão de balanceamento do usuário; fatores 4×/6× da guarda fiscal precisam de save.
- **Sem primitiva legível (não scriptável sem evidência nova):** autor/investidor da obra, qualificações, salário por profissão, abrir rota/tarifa/subvenção, consumo real de tropas, custo incremental exato.

## Ambiente
- Repo: `/home/lincoln-ii/Victoria3_Mod-2`, branch `codex/verified-fiscal-readings`, remote `origin https://github.com/Lincoln16yyy/SMART-ECONOMY-DIRECTOR.git`.
- Jogo base: `/home/lincoln-ii/Games/Victoria 3/game`. User data/log: `~/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3/`.
- Comandos: `python3 tools/build_mod.py [--check]`, `python3 tools/validate.py --game "<game>"`, `python3 -m unittest discover -s tests -q`, `python3 tools/package_mod.py`, `python3 tools/install_mod.py --user-data "<user data>"`. Instalar só com jogo fechado (`pgrep -x victoria3.exe`). `common/`, `events/`, `gui/` gerados pelo gerador.
