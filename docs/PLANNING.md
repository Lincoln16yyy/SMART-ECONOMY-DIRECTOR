# Planejamento e coordenação — 0.6.5

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

## Construção financiada por reservas na 0.6.2

A guarda fiscal 1–4 exige saldo semanal não negativo. Isso impedia a
coordenação sempre que o déficit operacional era coberto por reservas, mesmo
com ouro suficiente para o horizonte do Advisor. A 0.6.2 acrescenta a
classificação 5, aplicada antes das classificações 2–4:

- `net_fixed_income` não negativo (o déficit não vem de despesas fixas).
- `net_total_income` negativo (há déficit observado a financiar).
- Sem dívida (`principal <= 0`).
- Ouro maior ou igual a doze semanas de despesas fixas mais 26 semanas do
déficit observado: `12 × max(fixed_expenses, 0) + 26 × (−net_total_income)`.

A guarda escala com as leituras e não aprova sem ouro nem com despesa fixa
acima da receita fixa. Os fatores doze e 26 são decisões desta implementação
e exigem calibração em campanha; não são previsão de falência nem custo
incremental.

`sed_coord_fiscal_safe` aceita a guarda inicial 1–4 ou, com Advisor detectado,
a classificação 5. A entrada da coordenação usa essa guarda mais ampla. Os
caminhos do Supply Chain mantêm `sed_auto_fiscal_safe` em cada ramo, portanto a
classificação 5 delega somente ao Advisor, que avalia o investimento com o
próprio orçamento. O crescimento/diversificação (objetivo 8) também usa a
guarda ampla; apenas as classificações 3 e 4 substituem o objetivo por
estabilização. Sem Advisor, a classificação 5 não altera a coordenação.

O limite automático de uma tentativa por mês passou a comparar a variável com
o script value `sed_live_month_key` (ano × 12 + mês), em vez de aritmética
embutida na igualdade, que a engine não avalia. O validador rejeita essa forma
em qualquer igualdade `var:`.

124 testes sintéticos aprovados incluem escala da nova guarda, autorização do
Advisor até o piso de ouro, bloqueio com dívida e ausência de construções
próprias. A classificação 5 ainda não foi observada em campanha.

## Produtores alternativos na 0.6.3

Cada bem estratégico tinha um único prédio produtor verificado. Países com
outro tipo de produtor recebiam a mensagem de base ausente e nenhuma
recomendação, mesmo com o bem em escassez. A 0.6.3 acrescenta alternativas
verificadas nos arquivos vanilla 1.15:

| Bem | Produtores verificados |
| --- | --- |
| Cereais | Fazendas de trigo, centeio, arroz, milho e milhete |
| Tecido | Plantação de algodão e fazenda de gado (métodos de ovelhas) |

Fontes: `common/buildings/02_agro.txt:3–245`; grupos em
`common/production_method_groups/02_agro.txt:1–175`; métodos com saída positiva
de `grain` em `common/production_methods/02_agro.txt` e de `fabric` em
`pm_simple_ranch`, `pm_sheep_farms` e `pm_intensive_grazing_ranch`.

O filtro de elegibilidade passa a ser uma disjunção por prédio: estado
incorporado, sem déficit de infraestrutura, sem escolha ignorada nem pedido
pendente, mercado em escassez e ao menos um produtor com nível positivo,
ocupação de 80%, sem falha de contratação, sem falta de insumos, sem expansão
enfileirada, método ativo de saída e permissão de construção. Cada alternativa
tem seu próprio trigger `sed_<bem>_<prédio>_eligible`.

A aprovação enfileira o primeiro produtor elegível na ordem declarada. O
cartão e o botão deixam de nomear um prédio único quando há alternativas; o
tooltip informa que o prédio existente é revalidado. O diagnóstico de produtor
ausente usa a mesma disjunção, e as rejeições contam o primeiro motivo do
primeiro prédio presente no estado. Estados sem qualquer variante continuam
fora do denominador.

126 testes sintéticos aprovados incluem fazenda de milho planejada e
enfileirada, fazenda de gado elegível para tecido e ausência de falso produtor
para cereais. Nenhuma dessas combinações foi observada em campanha.

## Metas industriais anuais na 0.6.4

O plano mensal reagia à escassez do mês. Um pico passageiro de outro bem podia
deslocar uma falta recorrente, e o diário não distinguia escassez estrutural de
oscilação. A 0.6.4 acrescenta uma meta anual de oferta derivada da observação:

- `sed_<bem>_short_months` conta meses consecutivos com escassez de mercado;
  sem escassez, o contador é removido.
- Ao atingir três meses consecutivos, o Director grava
  `sed_<bem>_meta_year = ano` e declara a meta industrial anual daquele bem.
- A meta vale até a virada do ano civil. Se a escassez persistir, os três meses
  seguintes a reativam no novo ano; se tiver acabado, ela expira em janeiro.
- Enquanto a meta vale, o bem recebe 25 pontos adicionais na pontuação do plano.
  Isso mantém prioridade sobre uma falta mais aguda, mas recente, sem criar
  candidato: a elegibilidade continua exigindo mercado em escassez, produtor
  verificado, ocupação, insumos, fila, infraestrutura, permissão e política
  fiscal.

O diário mostra uma linha por bem com meta ativa: "Meta industrial anual:
ampliar a oferta de ...". O texto informa que a meta não dispensa os filtros e
não promete obra, custo ou resultado. Desativar o Director remove contadores e
marcadores anuais.

Três meses e 25 pontos são decisões desta implementação, escolhidas para
separar recorrência de ruído mensal; não foram calibradas em campanha. A meta
não altera o objetivo macro, impostos, gastos ou o orçamento dos executores
externos. Metas plurianuais, cadeias completas e feedback de resultados por
alvo continuam pendentes.

129 testes sintéticos aprovados incluem ativação no terceiro mês, expiração na
virada do ano, limpeza ao desativar e prioridade da meta sobre falta mais aguda
mas recente. O comportamento na engine e em save/reload ainda não foi
observado.

## Política fiscal própria na 0.6.5

O Director lia a situação fiscal e bloqueava ou coordenava construção, mas não
agia sobre a receita. A 0.6.5 acrescenta uma alteração de nível de imposto por
revisão mensal, somente no modo Automático e com o Director ativado:

- Cautela, crise ou default (classificações 2, 3 e 4): sobe um nível, até
  `very_high`.
- Classificação 1 ou 5 com saldo total positivo, sem dívida e ouro cobrindo
  doze semanas de despesas fixas: desce um nível, até `low`.
- Nenhuma outra combinação altera o nível, e só uma alteração ocorre por
  revisão mensal.

O nível original é capturado na primeira alteração em `sed_tax_level_saved` e
restaurado ao sair do Automático ou desativar. Mudanças manuais de imposto
feitas durante o Automático são substituídas na revisão seguinte; para manter
controle manual, use Manual ou Assistido. O snapshot segue o mesmo princípio já
usado nas opções dos executores externos.

Fontes vanilla 1.15: `common/effect_localization/00_country_effects_loc.txt:44`
(`set_tax_level`), `common/trigger_localization/00_trigger_localization.txt:3242`
(`tax_level`) e os níveis ordenados `very_low`–`very_high` usados em
`common/history/countries/hai - haiti.txt:25` e
`common/scripted_progress_bars/00_sepoy_mutiny_progress_bars.txt:250,271`.

O validador autoriza `set_tax_level` somente em `sed_apply_fiscal_policy` e
`sed_restore_fiscal_policy`, com valores do enum, e exige a guarda explícita de
modo Automático no efeito de aplicação. A política não altera salários
(militares ou civis), despesas, impostos de consumo, leis ou dívida; esses
controles continuam pendentes. O passo único por mês e os limites `low` e
`very_high` são decisões iniciais sem calibração em campanha, e a resposta da
receita a cada passo não é estimada.

132 testes sintéticos aprovados incluem subida em cautela, teto `very_high`,
descida com reservas e superávit, ausência de alteração fora do Automático,
restauração ao trocar de modo e ao desativar. Nada foi observado na engine: a
aceitação de `set_tax_level` fora do histórico e o efeito real na receita
continuam sem confirmação.
