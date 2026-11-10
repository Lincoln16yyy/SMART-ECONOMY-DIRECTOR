# Contrato de leitura da fila — pesquisa em andamento

Inspeção: 2026-11-09, Victoria 3 1.15.0, build
`6338547985dbc271523e149f362a6fd93dc62975`. Director instalado: 0.4.1.
Nenhuma campanha iniciada, fila modificada ou funcionalidade econômica nova.
Este documento fecha o recorte de fontes da pesquisa; o contrato de execução
continua **parcial**, pois faltam verificações dentro da engine.

## O que a instalação realmente expõe

Raízes: V = `Games/Victoria 3/game`; A = Economy Advisor 1.0.0 instalado;
S = Supply Chain Semi-Auto Builder z.260702.1 instalado.

| Dado/ação | Fonte inspecionada | Camada | Resultado e limite |
| --- | --- | --- | --- |
| Projetos públicos/privados | A `advisor_core_values.txt`; Director data/metrics.json | Script de país | `num_queued_government_constructions` e `num_queued_private_constructions`; agregados, não projetos individuais |
| Níveis públicos/privados | V `common/trigger_localization/00_trigger_localization.txt:4028–4088` | Triggers de país | Comparadores `construction_queue_num_queued_government_levels` e `construction_queue_num_queued_private_levels`; nomes localizados não bastam para provar leitura numérica completa |
| Níveis após a fila | A `common/scripted_effects/advisor_generated_candidate_effects.txt:324–326` | Script de edifício | Itera buildings e calcula `level_after_queued_constructions - level`; não identifica lado ou investidor de cada projeto |
| Inclusão pública | A `common/scripted_effects/advisor_automation_effects.txt:382–400` | Effect em estado | `start_building_construction`, compara contador público antes/depois; aumento agregado não identifica sozinho a intenção criada |
| Listas paginadas | V `gui/construction_queue.gui:336,350` | Somente GUI | `Country.AccessPagedPrivateConstructionQueue` e `Country.AccessPagedGovernmentConstructionQueue`; usam paginação/filtro do ConstructionPanel |
| Prédio e estado do projeto | V `gui/construction_queue.gui:389,393,436` | Somente GUI | `ConstructionQueueElement.GetBuilding`, `.GetState`, `.AccessBuilding` |
| Investidor/financiamento | V `gui/construction_queue.gui:409–416,649–659` | Somente GUI | `.GetInvestorCountry`, `.IsPrivatelyFundedConstruction`; país investidor não deve ser presumido igual ao dono do estado |
| Progresso e atividade | V `gui/construction_queue.gui:456,474,692` | Somente GUI | `.CalcPercentComplete`, `.GetConstructionSpeed`, `.IsCurrentlyUnderConstruction`; presente na tela, acesso numérico no effect ainda não identificado |
| Mover/cancelar | V `gui/construction_queue.gui:371,590–633` | Ação nativa GUI | `.MoveToIndex`, `.MoveUp`, `.MoveToTop`, `.MoveDown`, `.MoveToBottom`, `.CancelConstruction`; não são scripted effects identificados |

**Não transportar chamadas de GUI para scripts como se fossem primitivas.**
Não foi localizado, neste recorte de fontes, iterador de script que entregue
cada projeto com identidade, estado, tipo, investidor, lado e progresso. Isso
não demonstra que a engine não disponha de outro mecanismo. Os arquivos
inspecionados comprovam fontes distintas, não integração segura.

A lista mini da barra usa `AccessShownCurrentlyConstructingGovernmentQueue`
e `AccessShownCurrentlyConstructingPrivateQueue` em `gui/timemanip.gui:527,560`.
Ela contém o que está sendo mostrado/construído, não deve ser usada como prova
de cobertura de toda a fila. Paginação e filtros também podem ocultar projetos.

## Concorrência: flags reais encontradas no Supply Chain

A JE `common/journal_entries/zw_scsab_je.txt:84–126` chama rotinas distintas.
A opção de cadeias não é um interruptor geral dessas rotinas.

| Rotina | Fonte em S/common/scripted_effects | Opção/condição encontrada | Protegida pela flag de cadeias lida pelo Director? |
| --- | --- | --- | --- |
| Cadeias produtivas | `zw_scsab_effects_5_supply_chains.txt:3` | `zw_var_expand_building` | Sim, essa flag é checada |
| Ferrovias | `zw_scsab_effects_3_railway.txt:4–5` | `zw_var_scsab_construct_railway` e tecnologia railways | Não |
| Energia | `zw_scsab_effects_4_power_plant.txt:4` | `zw_var_scsab_construct_power_plant` | Não |
| Setores de construção | `zw_scsab_effects_1_construction_sector.txt:5–7` | `zw_var_more_construction_sectors`; ramo de reservas configurável | Não |
| Administração para instituições | `zw_scsab_effects_2_gov_admin.txt:9` | Compara `zw_var_scsab_gov_admin_for_institution` ao nível de instituição | Não; configuração não é simples bool |
| Administração tributária | `zw_scsab_effects_2_gov_admin.txt:132` | Usa `zw_var_scsab_gov_admin_for_tax` em ramo da rotina | Não; cadeia de guardas completa ainda precisa revisão |

Essas flags foram lidas em arquivos, não confirmadas como ativas na campanha.
Não se deve escrever em variáveis do Supply Chain nem chamar seus efeitos
internos como API pública. A próxima proteção precisa considerar o domínio e
as condições completas, não apenas acrescentar nomes sem verificar semântica.

## Invariantes que a execução precisa satisfazer

1. Toda intenção identifica tipo de prédio e estado; financiamento/investidor
   e dono devem ser tratados separadamente quando a engine os disponibilizar.
2. Intenção pendente não é sucesso: confirmação deve corresponder ao alvo,
   não apenas ao aumento de um total que outro executor também pode alterar.
3. Enquanto um projeto relevante existir, o mesmo pedido não pode ser repetido.
4. Conclusão e cancelamento devem produzir resultados distintos; se o dado
   não permitir distingui-los, a interface deve informar resultado desconhecido.
5. Save/reload e mudança de modo não podem gerar nova intenção por perder a
   memória de um evento ou projeto. Uma marca estadual isolada não demonstra isso.
6. Se um dado crítico não puder ser lido de forma confiável, o executor não
   deve declarar a ação segura. Não inventar identidade ou valor zero.

O Director 0.4.1 implementa uma proteção aproximada com contador, nível após
fila e marca estadual. Ainda não atende a todos esses invariantes. Nenhuma
alteração nessa execução foi feita nesta etapa de pesquisa.

## Matriz pequena de verificação na engine

Usar uma cópia dedicada, com um executor escolhido e opções registradas. Não
usar o único save nem sobrescrever a cópia SG_TEST. Não há resultado aprovado
abaixo; cada caso continua **não executado**.

| Caso | Preparação | Registrar antes/depois | Critério |
| --- | --- | --- | --- |
| Expansão pública existente | Um prédio de nível positivo | Prédio/estado, projetos e níveis públicos, nível atual/após fila | +1 nível do alvo; sem nova intenção ao atualizar |
| Mesmo tipo em dois estados | Dois alvos distintos | Identidade dos estados e projetos | O botão corresponde ao estado mostrado |
| Projeto privado existente | Mesmo tipo/estado ou tipo diferente | Lado privado, investidor, níveis por alvo | Determinar se level_after_queued_constructions inclui esse projeto |
| Primeira construção | Prédio ainda sem nível concluído | Existência de escopo building, level e nível após fila | Confirmar se iteração de buildings cobre nível zero |
| Expansão externa | Outro executor escolhe o mesmo alvo | Opções, momento da inclusão e leitura do Director | Diretor reconhece compromisso sem pedir outra expansão |
| Cancelamento | Cancelar somente a obra de teste pela UI | Projeto desaparece, nível final, marca pendente | Não confundir com conclusão |
| Conclusão | Deixar concluir a obra de teste | Nível final/emprego/insumos e desaparecimento do projeto | Reconhecer conclusão e reavaliar com novos dados |
| Save/reload | Obra/evento/ignore pendentes | Estado persistido e fila antes/depois | Nenhuma inclusão extra por recarga |
| Troca de modo | Evento agendado, depois Manual/Assistido | Data, modo, revisão e fila | Nenhuma ação do evento após sair de Automático |
| Desativar/reativar | Evento antigo ainda agendado | Datas, flags e ações | Não criar duas revisões válidas por perder o marcador |

Além da UI, registrar a leitura equivalente do script quando houver mecanismo
verificado para obtê-la. Sem essa medição, a comparação permanece parcial; uma
captura apenas do total da fila não encerra os casos de identidade.

## Próxima decisão técnica

Depois da matriz, escolher explicitamente entre: reconciliação por projeto
com dados comprovados; ou escopo conservador que suspenda execução quando a
identidade/cobertura for desconhecida. O planejador global e novos tipos de
construção continuam posteriores a essa decisão.


## Instrumento preparado para a matriz

O auxiliar opcional [QUEUE_PROBE.md](QUEUE_PROBE.md) implementa leituras manuais
dos agregados e de nível atual/após fila por prédio, em mod separado. Isso
permite preparar a comparação de script versus UI, mas não executa os casos
da matriz e não fornece identidade de projeto. Os casos acima continuam não
executados até haver observação da engine registrada com build/mods/opções.


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
