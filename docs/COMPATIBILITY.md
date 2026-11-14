# Compatibilidade — estado auditado e inventário histórico

Estado atual da 0.6.0 em [PLANNING.md](PLANNING.md) e [STATUS.md](STATUS.md).
A implementação inclui plano nacional inicial e coordenação de sete opções
externas com snapshot e restauração. A autorização do jogador para coordenar
Economy Advisor e Supply Chain nesta sessão amplia o escopo dos adaptadores.
As seções anteriores abaixo preservam a evolução histórica das versões.


## Reauditoria de 2026-11-11 (código 0.7.28)

Leitura direta dos arquivos de cada mod instalado na pasta de mods do usuário;
nenhum arquivo de outro mod foi alterado. Esta seção atualiza a tabela de
08/11, que dizia "Director não altera PMs" — ele altera desde a 0.7.9. Onde as
duas discordarem, vale esta.

| Mod | O que faz | Relação com o Director | Evidência |
| --- | --- | --- | --- |
| **Controllable Private Construction** (`3278770055`) | Injeta `can_build_private`/`can_build_government` por prédio e troca `default_auto_expand_rule`; 12 botões restringem a construção privada | Lido desde a 0.7.27 (só `has_variable`). Não escrever nem injetar: colidiria na mesma chave | Tiger 0 erros na pasta dele; seção "Controle de construção privada" |
| **Private Investments Only Expand Existing Buildings** (`3278371002`) | Mesmo autor e técnica, fixa "só prédios existentes" | Mesma colisão se o Director injetar prédios; hoje irrelevante | `INJECT_OR_CREATE:` em `common/buildings/` |
| **Auto-Apply PMs** (`3353797125`) | Um botão por prédio aplica o "melhor" método principal; botões de grupo para fazendas, minas e plantações | **Conflito real**: mesmos grupos de PM da modernização. A 0.7.28 cede o prédio com botão ligado | `zw_var_auto_pm_building_<prédio>`, `_group_farms/_mines/_plantations` |
| **Auto-Apply Automation PMs** (`3344726320`) | PMs de automação/transporte por estado quando falta mão de obra | Conflito indireto: muda ocupação, que é guarda do Director. Não escreve os grupos do Director | `zw_var_auto_pm_automation_*`, `zw_var_auto_pm_transportation` |
| **Supply Chain Semi-Auto Builder** (`3357811223`) | Constrói setores, ferrovias, energia, administração e cadeias | Já coordenado: sete opções em `COMPETING_BUILDERS` e `coordination.py` | `zw_var_expand_building`, `zw_var_scsab_*` |
| **Economy Advisor** (`3778129206`, 1.0.0) | Construção automática e política de PM/orçamento | Já coordenado/cedido: `advisor_auto_construction_enabled`, `advisor_pm_balance_enabled`, `advisor_labor_auto_enabled` | arquivos do Advisor |
| **ARoAI** (`ARoAI-1.3.5`) | Revisão da IA + autobuild com regra de jogo e evento de configuração | Já detectado: `aroai_autobuild` suspende a modernização e a execução. **Incompatível na prática com a 1.15** (arquivos de 2023, `supported_game_version` vazio): produz 1.300 `start_building_construction` falsos, 1.344 `Value of wrong type` e 5 `Div/0` no `error.log`. Recomendado desativar | `ARoAI_events_l_english.yml`, `error.log` de 2026-11-13 |
| **Kuromi's AI** (`3227982912`, 8.0) | Estratégias de IA (`ai_strategies`, `defines/kai_ai.txt`) com `INJECT:` em prédios, leis, tratados e mobilização | Neutro: nenhum `on_actions`, scripted effect ou variável própria do Director é tocado, e ele não escreve `sed_*`. Convive sem adaptador | `supported_game_version "1.15.*"`, varredura por `sed_*`/`aroai_*`/`advisor_*`/`zw_*` sem ocorrência |
| **Smart Government Advisor** (`1.0.0`) | Leis e instituições (`sg_*`, esquema 2) | Reconhecido no painel desde a 0.7.20; o Director não propõe leis | `sg_enabled`, `sg_schema_version` |
| **Government Administration Auto Expand** (`2934542706`) | `REPLACE:building_government_administration` com regra de autoexpansão e **sem `ai_value`** | Não toca o Director, mas o `REPLACE` apaga campo do vanilla 1.15 e disputa a definição com o `INJECT_OR_CREATE` do Controllable Private Construction: vence quem carregar por último | comparado com `game/common/buildings/07_government.txt` |
| **Auto-Recruit & One-Click Recruit Commanders** (`3279201462`) | Recruta comandantes por botão/decisão | Fora do escopo (militar não é mutado) | `zw_recruit_generals_*` |
| **Auto-Diplomacy And Advanced Subject Management** (`3432933121`) | Diplomacia e súditos automáticos | Fora do escopo; pode mudar fronteiras, que afetam a leitura de PIB | `zw_adnasm_*` |
| **OGAS for CWE** (`3770300244`) | Gestor completo de construção, pesos, PMs, setor e ferrovia | **Não usar nesta campanha**: README declara Victoria 3 1.13.x + Cold War Era (1950) e referencia prédios do CWE (`building_advanced_weaponry_factory`) inexistentes no vanilla 1.15. Já está instalado mas fora da lista habilitada | `README_OGAS_FOR_CWE.txt`, `supported_game_version 1.13.*` |

Pendências de compatibilidade:

- **Auto-Apply PMs por grupo**: o botão de grupo faz o Director ceder todos os
  prédios do grupo, mesmo com o botão individual desligado. Se o outro mod mudar
  essa regra, revisar `EXTERNAL_PM_VARIABLES` em `tools/production_methods.py`.
- **Government Administration Auto Expand**: recomendo desativar. Substitui a
  definição inteira do prédio e anula injeções de outros mods conforme a ordem.
- **Economy Advisor, Smart Construction**: em Automático com coordenação ativa, o
  Director remove as sete opções externas a cada `sed_coord_sync` e reabilita só
  a do executor escolhido no mês. Isso deixa o Smart Construction desmarcado em
  todo mês em que a execução não é delegada ao Advisor (executor 0, 2–10, 13 ou
  5 com ARoAI). É por desenho, mas o jogador não deve re-marcar dentro da
  coordenação esperando persistência: sair do Automático ou "Restaurar opções"
  devolve o valor guardado na entrada.
- **Ordem de carregamento** não é controlada pelo Director. Para leitura por
  `has_variable`, ordem não importa; para injeção em prédio, importa.

Atualização de 2026-11-09, código 0.4.1: há onze mods listados, incluindo o
Director. A lista e a instalação foram reinspecionadas; opções efetivas no país
continuam desconhecidas. Ver [auditoria, seção 7](AUDIT_2026-11-09.md#7-ecossistema-de-mods).
Há executor mensal opt-in no código, mas sem inclusão real comprovada e sem
reconciliação completa. Aprovações individuais não exigem pausa desde 0.3.6.
As três flags de concorrência não cobrem todos os controles do Supply Chain
nem autoexpansão administrativa. Co-renderização não prova coexistência segura.

O inventário abaixo preserva a pesquisa inicial de 08/11; versão declarada
não equivale a compatibilidade verificada na engine.


Data: 2026-11-08. Habilitado significa listado em `content_load.json`, não
automação comprovadamente ativa em campanha. A interface e o estado vazio da
seção de oportunidades foram confirmados pelo jogador, assim como a renderização
da seção de capacidade de construção da 0.3.0 com fila pública vazia. As ações
ferroviária e de capacidade de construção da 0.3.0 ainda não foram conferidas em
campanha nem com os outros mods ativos.

| Mod | Evidência local / responsabilidade | Conflito e coexistência proposta |
| --- | --- | --- |
| Smart Government | Habilitado; recomenda leis com prefixo `sg_` | Manter `sed_` independente; não modificar leis ou suas variáveis |
| Economy Advisor | Habilitado; orçamento, construção, análise, PMs e ações econômicas | Sobreposição alta; escolher um construtor e um controlador por domínio de PM; sem API identificada |
| Supply Chain Semi-Auto Builder | Habilitado; `zw_scsab_je.txt:84–115` agenda setores, administração, ferrovias, energia e expansão | Disputa a fila; evitar execução simultânea no mesmo domínio |
| Auto-Apply PMs | Habilitado; efeitos `zw_aap_*` usam preços locais, opções e `activate_production_method` | Director não altera PMs; pode observar efeitos. Não assumir que todos os caminhos avaliam emprego/lucro |
| Auto-Apply Automation PMs | Habilitado; JE mensal usa `zw_trigger_aaap_state_workforce_low`, transporte e flags de automação | Considera escassez de mão de obra e preços em caminhos examinados; algumas verificações estão comentadas. Não há garantia de segurança uniforme |
| Auto-Diplomacy and Advanced Subject Management | Habilitado; decisões, ações diplomáticas, efeitos de relações/súditos e leis | Auditoria inicial de estrutura; acompanhar efeitos fiscais sem controlar diplomacia |
| Auto-Recruit & One-Click Recruit Commanders | Habilitado; decisões, JE, efeitos de recrutamento | Auditoria inicial de estrutura; reservar capacidade fiscal sem iniciar expansão militar |
| Kuromi's AI | ZIP examinado: versão 8.0, declara 1.15.*; ausente da lista atual, nome presente no save Haiti antigo | Injeções de buildings e pesos de IA; não foi encontrado construtor independente do jogador. Reativação exige rever administração e defines |
| ARoAI 1.3.5 | Habilitado; 18 PMs vanilla redefinidos, inclusive dados econômicos; autobuild para jogador condicionado a regra e variável | Catálogo vanilla fixo pode divergir; confirmar `aroai_autobuild` no país antes de permitir outro construtor |
| Controllable Private Construction | Habilitado; redefine buildings, decretos e triggers de expansão | Ler definições efetivas; catálogo vanilla isolado pode estar incorreto |
| Government Administration Auto Expand | Habilitado; arquivo `common/buildings/z0z_government.txt` | Pode ampliar administração; coordenar com Advisor e Supply Chain |
| Private Investments Only Expand Existing Buildings | Instalado, ausente da lista habilitada | Altera buildings quando ligado; não pressupor regras de investimento vanilla |
| OGAS for CWE | Instalado, ausente da lista habilitada | Não é o Economy Advisor; nenhuma dependência proposta |

## Controles de execução pedidos pelo jogador

O Director deve mostrar ações econômicas recomendadas com controles de
aprovação que executem a ação real do jogo. A primeira versão desse fluxo está
implementada para expandir ferrovias em estados elegíveis e, na 0.3.0, para
ampliar um setor de construção quando a fila pública tem pelo menos três
projetos. O jogador quer manter o Smart
Government Advisor apenas como recomendador de leis. Isso não autoriza o
Director a iniciar promulgações nem a escrever variáveis de outros mods.

Como Economy Advisor e Supply Chain Semi-Auto Builder estão habilitados, a
construção é um domínio disputado. Os botões atuais exigem modo Assistido, país fora de
inadimplência e fila privada vazia; saldo semanal negativo aparece como alerta,
mas não bloqueia aprovação manual. A ferrovia valida
o estado e o nível no clique, e o setor de construção revalida a fila pública
mínima e o edifício. Ambos usam o efeito normal e conferem o contador público.
Isso não foi validado na engine da campanha. Existe automação mensal opt-in no código atual; a escolha efetiva no país
e sua execução bem-sucedida não foram verificadas nesta auditoria. As opções por país dos outros construtores ainda
não foram confirmadas; as ações precisam de teste com o conjunto de mods e flags
registrados antes de serem tratadas como seguras para uso prolongado.

No Supply Chain, a rotina ferroviária ordena estados por infraestrutura,
verifica ocupação e construção existente em certos caminhos, e executa
`start_building_construction`. Há agenda mensal e opções configuráveis; não é
apenas um botão que recomenda cadeias. A implementação completa ainda precisa
ser auditada para cobertura da fila privada e construções inéditas.

No Auto-Apply Automation, a JE filtra estados por mão de obra, mas há ramos
de PM com requisitos comentados em `zw_aaap_effects.txt`. Isso impede afirmar
que todo upgrade verifica insumos e lucratividade. O Director deve reavaliar
seus indicadores depois dessas mudanças, sem tentar revertê-las em disputa.

Integração segura proposta: coexistência por responsabilidade configurada e
leitura independente dos dados do jogo. A comparação estática de identificadores
e operações de injeção está em [LOCAL_AUDIT.md](LOCAL_AUDIT.md), com
[resultado estruturado](ENVIRONMENT_AUDIT.json). Um caminho diferente do vanilla
não impede redefinição por ID. A auditoria não simula a resolução final da engine.
Continuam pendentes opções ativas no país, definições efetivamente carregadas
e testes combinados em cópias de saves.


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

## Atualização 0.5.6 — configurações de administração

O Automático também suspende por `zw_var_scsab_gov_admin` ou
`zw_var_scsab_gov_admin_for_tax`. Meta institucional isolada não bloqueia,
pois depende da configuração geral. É detecção conservadora de configuração,
sem previsão da execução externa. Fontes, condições e limites registrados em
[RESEARCH.md](RESEARCH.md#administração-do-supply-chain--056).
A lacuna administrativa descrita nas seções históricas foi investigada para
essa versão instalada do Supply Chain; cobertura de outros executores e
reconciliação por projeto continuam parciais.

## Revalidação 0.5.7

A detecção de configuração concorrente também é consultada pelos dez efeitos
mutantes em Automático, junto das filas, pausa e limite mensal. Assistido
preserva aprovação explícita. Cobertura sintética não comprova sincronização
entre executores na engine.
