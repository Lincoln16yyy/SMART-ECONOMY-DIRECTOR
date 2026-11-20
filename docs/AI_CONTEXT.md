# Contexto de continuidade

## Estado atual
- **0.7.61 instalada:** primeiro setor de construção com manutenção, insumos e salários; quatro fábricas avançadas e minas de chumbo/enxofre; avaliação de lucro/salário após obras próprias; fases de dívida por fluxo e tendência.
- **Base anterior:** 0.7.60 instalada/publicada, 502 testes sintéticos aprovados. Crescimento civil sem escassez, orçamento por projeto, dívida sustentável e custo público por tecnologia.
- **Novos dados:** `tools/extend_industry_catalog.py` extrai seis cadeias da base 1.15; `advanced_sources.json` registra arquivos/hash. Melhorias de PM usam apenas o grupo principal, sem misturar produção e explosivos/luxo.
- **Primeiro setor:** apenas sem outro setor/pendência, com amostra salarial, caixa recorrente e crédito/ouro de segurança; métodos futuros disponíveis entram na previsão conservadora. Respeita prioridades essenciais.
- **Avaliação:** orçamento esperado é cotado antes de enfileirar e só registrado após confirmação. Após conclusão e três meses, média por nível de prédio não subsidiado/contratado ajusta crescimento. Não é causalidade marginal.
- **Dívida:** saldo negativo com dívida estabiliza; saldo positivo pode investir sob guardas 0.7.60; >80% do crédito ou duas altas mensais >1% priorizam amortização. Sem novos setters de dinheiro, imposto ou salário.
- **Migração:** novos IDs mudam a legenda de recibos antigos; `sed_development_schema` limpa somente o último recibo anterior uma vez. Prédios e intenções são preservados.
- **Validação:** 524 testes sintéticos aprovados; geração e validate aprovados; Tiger mantém os três campos conhecidos do Diário. Instalada com jogo fechado, backup e 14 arquivos idênticos ao pacote. Próximo: observar contratação/caixa/retorno em campanha e confirmar reload real. Campanha e save/reload na engine NÃO VERIFICADOS.
- **Perfil:** Better Politics 2.5.47 → Economy Advisor 1.0.0 → Director → Smart Government Advisor BPM 1.0.2 → Auto-Diplomacy → Auto-Recruit. OGAS fora do perfil ativo.
- **Governo:** fonte própria em `~/Victoria3_mod` pertence a outro trabalho; não editar. BPM 1.0.2 instalado e publicado no repositório Smart Government (commit 4f92fe5, release v1.0.2-bpm).
- **Ferramentas:** Tiger 1.19.0 suporta 1.13.5; conserva três campos de Diário 1.15 como erros conhecidos. Não confundir testes sintéticos/estáticos com campanha.
- **Armadilhas:** calendário em script value ficou preso em 1836 nos saves; desde 0.7.59 usar captura por efeito/variável. Se fila muda no efeito, cotar retorno antes da mudança. Histórico detalhado em `docs/PHASE_LOG.md`.

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
