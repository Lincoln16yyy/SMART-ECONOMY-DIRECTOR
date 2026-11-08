# Compatibilidade — inventário inicial

Data: 2026-11-08. Habilitado significa listado em `content_load.json`, não
automação comprovadamente ativa em campanha. Nenhuma combinação foi testada
com o Director, que ainda não tem código executável.

| Mod | Evidência local / responsabilidade | Conflito e coexistência proposta |
| --- | --- | --- |
| Smart Government | Habilitado; recomenda leis com prefixo `sg_` | Manter `sed_` independente; não modificar leis ou suas variáveis |
| Economy Advisor | Habilitado; orçamento, construção, análise, PMs e ações econômicas | Sobreposição alta; escolher um construtor e um controlador por domínio de PM; sem API identificada |
| Supply Chain Semi-Auto Builder | Habilitado; `zw_scsab_je.txt:84–115` agenda setores, administração, ferrovias, energia e expansão | Disputa a fila; evitar execução simultânea no mesmo domínio |
| Auto-Apply PMs | Habilitado; efeitos `zw_aap_*` usam preços locais, opções e `activate_production_method` | Director não altera PMs; pode observar efeitos. Não assumir que todos os caminhos avaliam emprego/lucro |
| Auto-Apply Automation PMs | Habilitado; JE mensal usa `zw_trigger_aaap_state_workforce_low`, transporte e flags de automação | Considera escassez de mão de obra e preços em caminhos examinados; algumas verificações estão comentadas. Não há garantia de segurança uniforme |
| Auto-Diplomacy and Advanced Subject Management | Habilitado; decisões, ações diplomáticas, efeitos de relações/súditos e leis | Auditoria inicial de estrutura; acompanhar efeitos fiscais sem controlar diplomacia |
| Auto-Recruit & One-Click Recruit Commanders | Habilitado; decisões, JE, efeitos de recrutamento | Auditoria inicial de estrutura; reservar capacidade fiscal sem iniciar expansão militar |
| Kuromi's AI | ZIP em Downloads, ausente da lista habilitada e da pasta ativa encontrada | Conteúdo e efeito sobre jogador ainda pendentes; não confundir com ARoAI |
| ARoAI 1.3.5 | Habilitado; scripts próprios de construção, orçamento, PMs e condições `is_player` | Amplia a auditoria necessária; não concluir que só afeta IA pelo nome |
| Controllable Private Construction | Habilitado; redefine buildings, decretos e triggers de expansão | Ler definições efetivas; catálogo vanilla isolado pode estar incorreto |
| Government Administration Auto Expand | Habilitado; arquivo `common/buildings/z0z_government.txt` | Pode ampliar administração; coordenar com Advisor e Supply Chain |
| Private Investments Only Expand Existing Buildings | Instalado, ausente da lista habilitada | Altera buildings quando ligado; não pressupor regras de investimento vanilla |
| OGAS for CWE | Instalado, ausente da lista habilitada | Não é o Economy Advisor; nenhuma dependência proposta |

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
leitura independente dos dados do jogo. Pendente: diff de identificadores,
overrides efetivos, ordem de carregamento e testes combinados em cópias de saves.
