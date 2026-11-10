# Planejamento e coordenação — 0.6.1

Esta versão implementa política nacional inicial e adaptadores de opções de
construção. Não é um controlador econômico completo nem comprova crescimento
em campanha. O briefing permanece o objetivo; o estado vivo está em
[STATUS.md](STATUS.md). A auditoria de 0.4.1 é histórica.

## Fluxo implementado

1. Ativação continua explícita e começa em Assistido em país sem modo.
2. Ao escolher Automático, se detectar Advisor habilitado, uma opção de
   construção verificada ou configurações persistentes do Supply Chain, guarda as sete
   opções de construção e passa à coordenação. Selecionar novamente não
   sobrescreve o snapshot. Sem ferramenta detectada mantém o executor próprio.
3. Forma um plano com dados atuais, objetivo, situação fiscal, data e até três
   pares estado/tipo. Atualizar diagnóstico recalcula o plano sem construir.
4. Com coordenação ativa, configura um executor externo e impede as dez ações
   próprias de construir em paralelo. Sem coordenação, o executor próprio
   revalida suas guardas e usa somente o par que ficou em primeiro lugar.
5. Reavalia a coordenação no pulso mensal e na revisão agendada. A agenda
   manual dos indicadores não desliga essas revisões do Automático.
6. Sair do Automático, liberar coordenação ou desativar restaura a presença e
   os valores numéricos das opções originais. As opções criadas pelo adaptador
   que originalmente não existiam são removidas. A escolha Manual não inicia
   construções pelo Director, mas a restauração pode reativar o construtor
   externo que o jogador tinha escolhido antes. O texto do controle informa isso.

Mudanças manuais feitas nas sete opções durante a coordenação podem ser
substituídas na próxima sincronização e na restauração pelo snapshot original.
Use o botão de restaurar antes de reconfigurar os executores manualmente.
Não remover os arquivos do mod com coordenação ativa sem antes restaurar:
saves guardam variáveis, mas não executam efeitos de um mod removido.

## Política fiscal inicial

Novas tentativas próprias e autorizações externas exigem:

- Saldo semanal e saldo sem itens temporários maiores ou iguais a zero.
- Ouro cobrindo pelo menos quatro semanas de despesas fixas não negativas.
- Sem dívida, ou crédito positivo e dívida até 75% desse limite.
- Sem inadimplência. A coordenação também suspende autorização com construção pausada.

Classificação: 1 condições iniciais de expansão; 2 cautela se uma dessas
condições falhar; 3 crise se o déficit consome as reservas em menos de quatro
semanas, se dívida ultrapassa 90% do crédito ou existe dívida sem crédito
positivo; 4 emergência por default. Os limiares são decisões explícitas da
política inicial, testadas por escala, não calibradas em campanhas Haiti/rico.
Não são custo incremental, previsão de falência, serviço da dívida ou prova de
sustentabilidade. Não mudam alíquotas, salários ou despesas. Assistido continua
permitindo aprovação explícita sob suas guardas anteriores.

O limite próprio de uma tentativa/mês não limita as construções do Advisor ou
Supply Chain: eles têm agendas, quantidades e critérios próprios. A proteção
fiscal é periódica, não um bloqueio transacional ao redor de cada chamada
externa. Não cancela projetos existentes nem anula dívidas.

## Pontuação nacional inicial

Filtros de incorporação, autorização, prédio existente, emprego atual,
contratação, insumos, fila, escolha ignorada e infraestrutura continuam sendo
aplicados antes da pontuação. O ranqueamento não torna um candidato rejeitado
executável.

| Ação | Pontos |
| --- | --- |
| Ferrovia | 100 + déficit absoluto de infraestrutura, limitado a 100 pontos extras |
| Madeira, ferro, carvão, tecido e ferramentas | 90 + 100 × falta relativa de oferta |
| Cereais, mantimentos e roupas | 100 + 100 × falta relativa de oferta |
| Setor de construção | 40, somente com ao menos três projetos públicos e setor elegível |

Falta relativa = `(ordens de compra − ordens de venda) / ordens de compra`,
limitada ao intervalo 0–1. Sem escopo do bem ou com compras zero não divide;
nenhum candidato é criado só por esse valor. A escassez continua exigindo o
trigger real, e as ordens são do mercado inteiro, não apenas do país.

O algoritmo repete três seleções: melhor tipo ainda não escolhido em cada
estado; melhor estado; marca o par escolhido e repete. Isso permite três tipos
no mesmo estado sem repetir o mesmo par. Empate de tipo segue a ordem declarada
no código; empate entre estados depende da iteração da engine, sem garantia de
ID estável. Não usar a ordem sintética do harness como prova dessa estabilidade.
As listas completas por tipo ficam nos detalhes; só três prioridades aparecem
na parte principal. A pontuação exibida é da última análise e a aprovação
revalida o alvo; não promete benefício em libras, contratação futura ou prazo.

## Objetivos e adaptação externa

O primeiro par ranqueado define infraestrutura, oferta ou capacidade de
construção. Sem par, escassez de um dos oito bens sem o tipo de produtor atendido
pelo protótipo gera investigação de base produtiva. Isso não demonstra ausência
de todos os produtores alternativos e não impõe autossuficiência.

Sem esses gargalos, condições fiscais iniciais permitem objetivo de crescimento
/diversificação; burocracia negativa, capacidade tributária insuficiente ou
energia local 20% acima da base podem substituir esse objetivo por investigação
administrativa/tributária/energética. Prioridade fiscal de crise/default substitui
o objetivo por estabilização. A lista local de expansões e o objetivo macro não
são garantia de um plano plurianual completo.

| Objetivo | Executor escolhido, quando disponível |
| --- | --- |
| Infraestrutura | Supply Chain, somente ferrovias; alternativa Advisor |
| Oferta, base atendida ausente ou crescimento/diversificação | Advisor; alternativa Supply Chain cadeias |
| Capacidade de construção | Advisor; alternativa Supply Chain setores |
| Burocracia | Supply Chain administração geral; alternativa Advisor |
| Capacidade tributária | Supply Chain administração tributária; alternativa Advisor |
| Energia local cara | Supply Chain energia; alternativa Advisor |
| Fiscal bloqueada, pausa ou ARoAI construtor detectado | Nenhum dos dois adaptadores autorizado |

Opções verificadas: `advisor_auto_construction_enabled`, `zw_var_expand_building`,
`zw_var_more_construction_sectors`, `zw_var_scsab_construct_railway`,
`zw_var_scsab_construct_power_plant`, `zw_var_scsab_gov_admin`,
`zw_var_scsab_gov_admin_for_tax`. Valores prévios são conservados; se a opção
necessária estava ausente, padrões são respectivamente 1, 0, 5, 1, 1, 10 e 1.
Zero em cadeias significa presente/ligado, não desligado.

O adaptador altera autorização, objetivo de investimento e política de orçamento
do Advisor. O scan mensal usa `advisor_scan_goal = 10` e consulta as opções de
objetivo configuradas para ordenar os candidatos. A seleção do par estado/prédio
é executada pelo algoritmo do Advisor. Supply Chain conserva categorias,
metas institucionais e outros parâmetros internos. Um deles pode não construir
por seus próprios filtros, agenda ou indisponibilidade. O resultado 18 significa
orientação atualizada, nunca inclusão confirmada. PMs, comércio, diplomacia e
outras funções desses mods não são alterados.

ARoAI construtor é detectado, mas não controlado; os adaptadores suspendem seus
dois executores se encontrarem `aroai_autobuild`. Autoexpansões nativas de
edifícios e mods fora desses adaptadores não são controladas. Não há trava
universal contra concorrência nem identidade confiável de projetos. Troca de
versão dos mods exige revalidar esses adaptadores privados.

## Fontes locais consultadas

- Vanilla 1.15.0: `common/script_values/ip5_je_values.txt:1268–1276`, ordens em
  escopo opcional de mercado/bem; `00_gfx_route_graphics_values.txt:44–51`, vendas.
- Vanilla `common/political_movements/04_country_specific_ideological_movements.txt:2067`,
  acesso `owner.var`; comparações/aritmética/listas já presentes no Director.
- Supply Chain: `zw_scsab_je.txt:84–126`; `zw_scsab_buttons.txt` e efeitos 1–5.
  Efeito 2 exige opção geral para burocracia e opção tributária independente;
  efeito 4 investiga `sg:electricity.state_goods_pricier >= 0.20`.
- Advisor instalado: `advisor_scripted_guis.txt:407–416`, toggle por presença;
  `advisor_automation_effects.txt:1–80`, guarda e seleção interna; eventos
  `advisor_pulse_events.txt:33–48` revalidam autorização antes da rotina.
- ARoAI 1.3.5: `aroai_preparation_triggers.txt:10–29`, autorização por regra e
  `aroai_autobuild`. O adaptador não escreve nessa variável.
- Government Administration Auto Expand: `common/buildings/z0z_government.txt`,
  `should_auto_expand` por ocupação/capacidade; não oferece opção de país verificada.

São fontes de script, não verificação de que os adaptadores funcionaram em
campanha. Os testes executam os scripts gerados em fixtures, não os outros mods
nem a engine. Guardas, dados e limites de [QUEUE_CONTRACT.md](QUEUE_CONTRACT.md)
continuam relevantes.

## Objetivo e orçamento do Advisor na 0.6.1

Quatro opções adicionais são coordenadas e restauradas.

| Opção | Controle aplicado |
| --- | --- |
| `advisor_setting_sc_goal_sol` | Priorizar padrão de vida quando cereais, mantimentos ou roupas lideram o plano ou aparecem como lacuna prioritária |
| `advisor_setting_sc_goal_treasury` | Priorizar retorno ao tesouro quando há dívida positiva atingindo pelo menos 50% do crédito |
| `advisor_setting_treasury_off` | Preservar reservas na orientação de retorno ao tesouro |
| `advisor_setting_borrow` | Remover autorização de endividamento enquanto o Advisor recebe orientação do Director |

A prioridade financeira antecede a social. Nas demais condições o objetivo é
crescimento, com orçamento equilibrado. O orçamento equilibrado do Advisor
reserva doze semanas de despesas fixas pelo cálculo próprio dele. Isso se
combina com a guarda inicial do Director de quatro semanas. O limiar de 50%
foi escolhido nesta implementação e precisa de calibração em campanha.

A desativação da opção de endividamento orienta o planejamento do Advisor. A
fila existente e outras decisões do jogo continuam podendo consumir reservas
e crédito. O controle das alíquotas e de gastos públicos segue na matriz de
trabalho pendente.

O snapshot das quatro opções usa `sed_coord_policy_saved` e conserva presença
e valores exatos. Ao iniciar uma coordenação nova, as opções são guardadas
quando o Advisor foi detectado. Para saves com coordenação 0.6.0 já ativa, a
captura ocorre na primeira seleção do Advisor, antes de qualquer alteração.
Liberar uma coordenação antiga antes dessa captura preserva as quatro opções
atuais. As opções só recebem a política nova quando o Advisor é o executor
selecionado.

Fontes adicionais do Advisor instalado são
`common/scripted_guis/advisor_scripted_guis.txt:492–530,550–557`,
`common/script_values/advisor_core_values.txt:1390–1465` e
`common/scripted_effects/advisor_generated_candidate_effects.txt:4375–4376`.
Os toggles verificam presença das opções, e a geração de candidatos lê as
flags social/tesouro para atribuir a pontuação do objetivo.

120 testes sintéticos aprovados incluem migração de coordenação ativa,
restauração de valores, configuração original ausente, limites da dívida,
prioridade social/financeira e preservação da política durante delegação ao
Supply Chain. A integração das novas opções ainda aguarda confirmação na engine.
