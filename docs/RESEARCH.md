# Fase 0 — pesquisa técnica

Data: 2026-11-08. Resultado: pesquisa estática inicial, com lacunas explícitas.
Este documento apresenta o diagnóstico e a arquitetura antes da implementação.
Não certifica compatibilidade nem funcionamento dentro de uma campanha.

## Fontes e ambiente encontrados

- Referência: https://github.com/Lincoln16yyy/Smart-Government-Victoria-3-1.15
  e checkout local `/home/lincoln-ii/Victoria3_mod`. O commit inspecionado está
  registrado em `SOURCE_INVENTORY.json`; alterações locais podem existir.
- Instalação: `/home/lincoln-ii/Games/Victoria 3`. O arquivo
  `launcher/launcher-settings.json` informa `rawVersion: 1.15.0`; o log local
  `logs/system.log:1` registra `release/1.15.0 : 6338547985`.
- Dados de usuário: `~/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3`.
  Os caminhos Windows em `content_load.json` pertencem a esse prefixo Wine.
- Mods instalados foram examinados na subpasta `mod` desses dados, e não apenas
  pelos ZIPs em Downloads. Saves Haiti e uma cópia `haiti_1836_06_30_SG_TEST.v3`
  existem. Nenhum save ou arquivo da instalação foi modificado.
- `SOURCE_INVENTORY.json` registra exemplos por identificador, arquivo e linha,
  separados entre vanilla e mods. Uma ocorrência em mod é evidência de uso,
  não prova de aceitação pelo motor. Não contém código proprietário do jogo.

## Smart Government: padrões aproveitáveis

Foram consultados README, AI_CONTEXT, PHASE_LOG e MANUAL_RUNTIME_TEST, além do
ciclo de vida, Journal Entry, on-actions e organização dos geradores/testes.

O sistema usa dados reais de leis, IDs numéricos estáveis e scripts gerados.
Calcula benefício, risco, apoio político e viabilidade; compara o mérito com a
lei vigente antes de formar um ranking global de até três opções. Os textos
explicam componentes e riscos. O botão inicia a promulgação normal; não aprova
a lei instantaneamente. Esse modelo político não deve ser copiado para economia.

`sg_on_actions.txt` acrescenta dispatchers com `on_actions = { ... }`.
`sg_journal_entries.txt` associa um widget ao `custom_widget_container_3`, usa
`activation_description` e executa atualização mensal. `sg_effects.txt` guarda
schema, data de atualização e habilitação, evita Journal Entries duplicadas,
limpa o estado ao desativar e conserva o schema para impedir reativação automática.
Ignorar/restaurar opera por ID; ações devem acompanhar o candidato, não uma
posição mutável da lista. Contadores de ranking tornam o diagnóstico auditável.

Os geradores `build_law_data.py` e `build_gui.py`, o parser `pdx_parse.py`, os
testes em `tests/test_advisor_generation.py`, o validador, as duas localizações,
o descriptor e o instalador fornecem referências de organização. A documentação
registra falhas reais da engine: BOM, define com namespace, nomes de listas e
propriedades GUI inválidas. Portanto, validação textual não substitui runtime.
Na continuação local, os 26 testes de leis passaram novamente. O validador
completo encontrou 178 erros no módulo de pesquisa tecnológica da referência;
o resultado está detalhado em LOCAL_AUDIT.md. O Director não modifica esse mod.

## Economy Advisor: sobreposição comprovada nos arquivos

Instalado como `3778129206_Economy_Advisor`, versão declarada 1.0.0,
`supported_version="1.15.*"`. Há decisões, três Journal Entries, scripted GUIs,
scripts gerados, análise econômica, orçamento, construção e avaliação de PMs.

- `common/on_actions/advisor_on_actions.txt`: monitoração mensal exige
  `advisor_enabled`; a construção exige `advisor_auto_construction_enabled`.
  Os comentários e eventos separam a construção para o dia 8 e PMs para o dia 15,
  evitando concentrar os cálculos pesados no início do mês.
- `advisor_automation_effects.txt:385` usa
  `start_building_construction = $BUILDING$`. Portanto, executa construções.
- `advisor_core_values.txt:404–458` considera quantidade de projetos privados e
  governamentais, alocação privada e espaço de construção. O modelo também
  considera contratação, infraestrutura e efeito de preços após construção.
- `advisor_core_values.txt:1408–1448` usa `net_fixed_income`, `net_total_income`,
  `fixed_expenses`, reservas, crédito e custo de juros. Tem planos distintos de
  orçamento; a reserva de doze semanas é uma política desse mod, não regra universal.
- Os scripts de PM avaliam lucro, mão de obra, qualificações, insumos,
  infraestrutura e cooldown. `advisor_tax_capacity_effects.txt:471–479`
  contém aplicação real de PM administrativo.
- `advisor_lifecycle_effects.txt` remove flags de automação ao limpar o estado.
  Instalar o mod não demonstra que sua construção/PMs estejam ligados no save.

O mod está na lista habilitada do launcher. Ainda falta ler o estado de país
de uma cópia de save e confirmar na interface quais opções estão ativas.
Não existe contrato de integração documentado encontrado nesta inspeção.
Não chamar efeitos internos nem escrever suas variáveis como se fossem API.

## Capacidades e métricas

Legenda: **observável** indica leitura encontrada nos scripts; **executável**
indica mecanismo de ação encontrado; **parcial** indica modelo ou acesso
incompleto; **não suportado identificado** significa ausência de mecanismo
confiável nesta pesquisa, sem afirmar impossibilidade absoluta do motor.

Para exibição, valores numéricos lidos em script poderão ser transferidos a
variáveis `sed_` e formatados no widget, seguindo o padrão do Smart Government.
Isso é uma proposta; cada binding do novo widget precisa de teste de runtime.

| Métrica ou ação | Fonte real identificada | Classe e limitações |
| --- | --- | --- |
| Saldo total / operacional | Advisor: `net_total_income`, `net_fixed_income` | Observável em país; conferir unidade semanal na tela |
| Reservas | Vanilla `war_support_values.txt`: `gold_reserves`, `gold_reserves_limit` | Observável; reserva não é receita recorrente |
| Dívida / crédito | Advisor health: `principal`, `credit`, `scaled_debt` | Observável; proteger divisões com limite zero |
| Juros | Advisor budget: modificadores de taxa | Parcial: taxa calculada não é toda a decomposição da despesa observada |
| Receita/despesa detalhada, tributos e gastos militar/administrativo | Tela de orçamento; `fixed_expenses` no Advisor | Parcial: total fixo encontrado; falta mapear cada rubrica script/GUI |
| Gastos públicos de construção | Advisor: diferença entre saldo operacional e total | Parcial; inclui interpretação de transferências, validar contra orçamento |
| PIB | Vanilla `ip5_je_values.txt`: `gdp` | Observável; crescimento exige amostras datadas |
| PIB per capita | Vanilla `country_gdp_per_capita` | Observável como script value vanilla; conferir população e unidade |
| Padrão de vida | Advisor health: `average_sol` | Observável; média pode ocultar pobreza de grupos |
| Preços / oferta / demanda | Vanilla usa `market_goods_buy_orders`; mods usam `sg:goods`, `state_goods_pricier`, `state_goods_delta` | Parcial: escopo local e mercado distintos; confirmar venda e preço por bem |
| Importação/exportação e dependência externa | Scripts `advisor_generated_export_*`; mercado do jogo | Parcial: falta separar produção nacional e circulação em mercado compartilhado |
| Escassez de insumos | `building_has_goods_shortage` nos mods | Observável no edifício; preço alto sozinho não prova escassez |
| Lucro / utilização / PM atual | `weekly_profit`, `occupancy`, `has_active_production_method` | Observável; lucro não equivale ao benefício nacional |
| Produção setorial / capacidade / insumos futuros | Buildings, PMs e modificadores vanilla; perfis gerados do Advisor | Parcial: requer catálogo próprio e cálculo com throughput e emprego |
| Mão de obra / desemprego / qualificações / salários | Triggers de workforce e valores de avaliação do Advisor | Parcial: falta validar separadamente cada primitiva e escopo |
| Alfabetização / educação / migração / população regional | Sistemas vanilla e interface | Parcial: mapeamento script e GUI ainda pendente por indicador |
| Infraestrutura | `infrastructure_delta`, `infrastructure_usage`; Supply Chain ferroviário | Observável por estado; fila pode consumir a margem futura |
| Capacidade de construção | Advisor: `modifier:country_construction_add` | Observável; considerar parcela privada e limite por projeto |
| Fila pública / privada | Advisor: `num_queued_government_constructions`, `num_queued_private_constructions` | Parcial: totais não bastam para deduplicar estado + tipo + níveis |
| Tecnologia disponível | `has_technology_researched` nos scripts | Observável; Director não controlará pesquisa nesta etapa |
| Construir normalmente | `start_building_construction` em estado | Executável em scripts existentes; precisa validar custo/fila na 1.15 para o Director |
| Trocar PM | `activate_production_method`, com `can_activate_production_method` | Executável; deixar aos controladores de PM no ecossistema |
| Histórico / avaliação de resultados | Variáveis persistentes e amostras mensais | Parcial; correlação observada não prova causalidade da construção |
| Aprendizado de máquina / previsão econômica exata | Nenhuma implementação confiável encontrada em script | Não suportado identificado; usar avaliação transparente de resultados |
| Coordenação atômica entre mods | Nenhum protocolo encontrado | Não suportado identificado; exigir um único executor configurado |

## Conclusão técnica e pendências

É viável propor um diagnóstico em Journal Entry e um planejador com ranking
explicável. Há mecanismos de execução, mas coexistência segura depende da fila
completa e de escolher quem executa. Replicar o construtor/PM do Advisor agora
duplicaria funções já existentes. A arquitetura proposta está em ARCHITECTURE.md.

A continuação produziu [LOCAL_AUDIT.md](LOCAL_AUDIT.md), incluindo Kuromi,
redefinições por ID e leitura da fila usada pelo Advisor, e uma
[matriz por indicador](METRICS.md) com fontes de GUI encontradas na instalação.
A ferramenta e o JSON permitem reproduzir a inspeção sem modificar os fontes.

A Fase 0 permanece aberta: o estado das automações por país não foi decodificado
do save binário; a cobertura da fila privada e de primeira construção requer
teste no motor; faltam fontes diretas de script para algumas métricas, além de
medição de desempenho. As leituras e bindings do núcleo de diagnóstico foram
identificados em fontes, mas ainda não comparados em campanha. Não tratar
essas lacunas como dados iguais a zero. A Fase 1 só começa após fechar o
diagnóstico técnico necessário e apresentar suas conclusões.

## Pesquisa anterior preservada

[Pesquisa na nuvem](RESEARCH_CLOUD.md) conserva as fontes fixadas e os resultados
prévios: 26 testes da referência aprovados; validador bloqueado pela ausência do
jogo naquele executor. Os caminhos e mods agora encontrados atualizam esse
diagnóstico. Esses testes não foram repetidos na presente sessão local.
