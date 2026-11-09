# Compatibilidade — inventário inicial

Data: 2026-11-08. Habilitado significa listado em `content_load.json`, não
automação comprovadamente ativa em campanha. A interface de diagnóstico 0.1.0
foi confirmada pelo jogador. A ação ferroviária aprovada da 0.2.0 ainda não foi
conferida em campanha nem com os outros mods ativos.

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
implementada para expandir ferrovias em estados elegíveis. O jogador quer manter o Smart
Government Advisor apenas como recomendador de leis. Isso não autoriza o
Director a iniciar promulgações nem a escrever variáveis de outros mods.

Como Economy Advisor e Supply Chain Semi-Auto Builder estão habilitados, a
construção é um domínio disputado. O botão atual exige pausa, saldo semanal não
negativo, país fora de inadimplência e fila privada vazia; valida o estado e
nível ferroviário no clique, usa o efeito normal e confere o contador público.
Isso não foi validado na engine da campanha. Nenhuma automação mensal de
construção está habilitada. As opções por país dos outros construtores ainda
não foram confirmadas; a ação precisa de teste com o conjunto de mods e flags
registrados antes de ser tratada como segura para uso prolongado.

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
