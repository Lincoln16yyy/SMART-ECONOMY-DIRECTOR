# Compatibilidade — estado auditado e inventário histórico

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
