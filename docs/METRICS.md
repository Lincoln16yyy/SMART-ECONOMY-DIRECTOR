# Métricas: fonte, escopo e apresentação

Pesquisa estática de 2026-11-08. A versão 0.1.0 implementa o núcleo de leituras
em `data/metrics.json` e derivações/contagens descritas em PHASE1.md.
**Nenhum binding novo foi confirmado numa campanha do Director.**
Uma função na GUI não comprova que seu valor possa ser lido por um scripted
effect. Uma primitiva usada por outro mod não prova que o motor a tenha aceitado.

Raízes das referências: `V` = instalação `game/`; `A` = Economy Advisor
instalado; `S` = Smart Government. O inventário e LOCAL_AUDIT.md registram
versões e caminhos. Valores monetários recorrentes nas telas de orçamento são
semanais; reservas, dívida e crédito são estoques em libras. Razões devem ser
formatadas como percentuais, sem confundir 0,1 com 0,1%.

| Indicador | Leitura de script identificada / escopo | Apresentação identificada / limite |
| --- | --- | --- |
| Saldo total | `net_total_income`, país; A health:9 | Variável numérica no widget; validar contra saldo semanal, não previsão de receita |
| Saldo operacional | `net_fixed_income`, país; A core:1411 | Variável; exclui itens temporários conforme modelo do Advisor |
| Receita total | Mapeamento numérico de script pendente | V `budget_panel.gui:177`: `PredictWeeklyIncome`, previsão para GUI |
| Despesa total | Mapeamento por rubrica de script pendente | V budget:437: `GetWeeklyExpenses`; separar de despesas fixas |
| Despesas fixas | `fixed_expenses`, país; A core:1420 | Variável; validar componentes antes de calcular reserva mínima |
| Reservas | `gold_reserves`, país; A health:10 e V war_support values | V budget:1354: `GetGoldReserves` |
| Dívida | `principal`, país; A health:11 | V budget:1544: `GetPrincipal` |
| Crédito total / restante | `credit`, país; A health:12; restante derivado só após conferir semântica | V budget:1573: `GetRemainingCredit`, `GetMaxCredit` |
| Razão da dívida | `scaled_debt`, país; A health:13 | Variável; limite zero exige tratamento próprio |
| Juros pagos | Script para despesa observada ainda pendente; taxa é outra métrica | V budget:1016: `GetInterestPayment` |
| Construção pública | A: diferença `net_fixed_income - net_total_income` é modelo de gasto líquido | V budget:455: `GetConstructionGoodsExpenses` mostra bens; não equivale ao líquido do governo |
| Salários administrativos | Script por rubrica pendente | V budget:631: `PredictGovernmentWagesExpenses`; previsão identificada |
| Bens administrativos | Script por rubrica pendente | V budget:720: `GetGovernmentGoodsExpenses` |
| Salários militares | Script por rubrica pendente | V budget:756: `PredictMilitaryWagesExpenses` |
| Bens militares | Script por rubrica pendente | V budget:844: `GetMilitaryGoodsExpenses`; navios possuem rubricas separadas |
| Impostos | Script agregado por tipo/nível ainda pendente | V budget:253/266/280: renda, poll tax e consumo; 2045+ exibe níveis |
| Sustentação de déficit | Derivação de reserva/saldo; A usa `weeks_until_bankruptcy` quando há déficit | Estimativa condicional; não mostrar previsão de quebra como garantia |
| Preço por bem | `sg:<bem>.state_goods_pricier`, estado/bem, nos mods | Preço local relativo; não rotular como preço nacional em libras |
| Oferta / demanda | `market.mg:<bem>.market_goods_sell_orders` / `market_goods_buy_orders`; A generated candidate:7+ | Ordens no mercado inteiro, não apenas produção e consumo nacionais |
| Produção / consumo local | `sg:<bem>.state_goods_production` / `state_goods_consumption`; A candidate:9+ | Exibir por estado; agregação nacional exige tratar escopo e cobertura |
| Importações / exportações | `market_goods_imports` / `market_goods_exports`; A candidate:11+ | Mercado; não atribuir automaticamente todos os fluxos ao país subordinado |
| Dependência externa | Parcial: derivações exigem origem e propriedade dos fluxos | Não inferir de déficit de ordens; países no mesmo mercado compartilham oferta |
| Escassez de insumos | `building_has_goods_shortage`, edifício; `market_goods_has_goods_shortage`, mercado/bem | A candidate:2306+: há também `state_goods_has_local_goods_shortage` para bens locais |
| Excesso de produção | Parcial: ordens, preço e histórico | Uma amostra barata não comprova excesso estrutural |
| Produção setorial / capacidade | Níveis, PMs, throughput e emprego; catálogo de definitions | Derivada; deve considerar PMs redefinidos por mods |
| Rentabilidade | `weekly_profit`, edifício; A core e scripts de PM | V `building_details_panel.gui:675`: `Building.GetBalance`; conferir diferenças de unidade/semântica |
| Utilização | `occupancy`, edifício; A e Supply Chain | Razão de contratação; não garante ausência de gargalos por profissão |
| Métodos atuais / insumos | `has_active_production_method`; valores em definitions de PM | Leitura observável; calcular deltas com dados efetivos, não catálogo vanilla fixo |
| População nacional | `total_population`; V `ip5_je_values.txt:27` | V `country_panel.gui:988`: `Country.GetTotalPopulation` |
| População estadual | `state_population`; A profiles:6 | Estado; população total não é população economicamente ativa |
| Desemprego | `state_unemployment_rate`, estado; V decretos e A profiles | V `states_panel.gui:2790`: `GetNumUnemployedWorkingAdults`; taxa e contagem não intercambiáveis |
| Camponeses disponíveis | `pop_type_percent_state(pop_type:peasants)` nos mods | Disponibilidade para contratar requer adultos, mobilidade e vagas; modelo do Advisor é aproximação |
| Emprego e vagas | `occupancy`, `has_failed_hires`, emprego dos PMs | Total de vagas calculado não equivale à disposição real de contratar |
| Qualificações | Leitura quantitativa direta por profissão ainda não identificada | Alfabetização é indicador indireto; não exibir fator estimado como qualificação observada |
| Salários | Leitura média direta por estado/profissão ainda pendente | A estima wage unit com fallback; não copiar como salário observado |
| Padrão de vida | `average_sol`, país; A health:14 | V topbar:110/118: `GetAverageSoLByPopulation` / `GetFormattedStandardOfLivingAll`; médias escondem distribuição |
| Migração | Métrica e binding de script ainda pendentes | Não usar variação populacional como migração líquida sem separar natalidade/mortalidade |
| Infraestrutura | `infrastructure_delta`, `infrastructure_usage`, estado; Supply Chain ferroviário | Variáveis; projeção deve descontar projetos ainda não concluídos |
| Acesso ao mercado | `market_access`, estado; A construção | Razão, distinta de infraestrutura absoluta e do efeito local de preço |
| Ferrovias / portos | Níveis e PMs por edifício; custo/produção de infraestrutura em definitions | Existência não prova contratação, subsídio suficiente ou capacidade funcional |
| Capacidade de construção | `modifier:country_construction_add`, país; A core | Total de pontos; distinguir alocação privada, limite por projeto e desperdício |
| Filas pública / privada | `num_queued_government_constructions` / `num_queued_private_constructions` | Quantidade de projetos não é quantidade de níveis ou prazo |
| Níveis após fila | `level_after_queued_constructions`, edifício; A cache:325 | Cobertura de construção inédita, privada e cancelamento exige teste na engine |
| PIB | `gdp`, país; V ip5 values | V topbar:66: `Country.GetGDP`; fluxo anualizado, não receita fiscal semanal |
| PIB per capita | V `country_gdp_per_capita`: PIB dividido por população com guarda | Derivação exibível em variável; não confundir ranking com valor |
| Crescimento | Histórico próprio de PIB com data | Sem amostra anterior, indisponível; mudança de fronteira/mercado afeta comparabilidade |
| Alfabetização | `literacy_rate`, país/estado; V scripted values e JEs | V topbar:91: `GetIncorporatedLiteracyRate`; universo incorporado pode diferir do total |
| Educação | V `max_innovation` usa alfabetização; instituições e universidades são sinais distintos | Leitura de educação efetiva/cobertura ainda pendente; não reduzir educação ao número de universidades |
| Produtividade | Parcial: receita de bens, emprego e salários | Métricas modeladas do Advisor não substituem leitura observada validada |
| Industrialização / diversificação | Derivações por tipos/setores de edifícios e participação econômica | Definir índice e ponderação antes de exibir; quantidade de tipos não mede resiliência sozinha |

## Escopo seguro para a Fase 1

Diagnóstico inicial poderá usar saldo, reservas, principal/crédito, PIB,
população, padrão de vida, alfabetização, capacidade de construção e
infraestrutura nos escopos identificados. Deve informar data e universo da
medição, indicar valores não medidos e evitar pontuação ou execução econômica.

Receitas/despesas detalhadas podem ser exibidas com funções vanilla de GUI,
mas só entrarão em decisões calculadas após uma fonte de script comprovada.
Salários, qualificações, migração e previsões terão tratamento explícito de
indisponibilidade até fechar suas fontes. A situação fiscal não será declarada
saudável apenas porque um indicador ausente recebeu valor zero.

O teste mínimo da Fase 1 é comparar cada linha com a tela correspondente, no
mesmo país e data, registrar a diferença e ler os logs. Esse teste continua
pendente e não será substituído pelos testes da ferramenta de pesquisa.
