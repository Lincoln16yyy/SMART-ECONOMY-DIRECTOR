# Estado dos requisitos — 0.7.53

## Coordenação com Economy Advisor

**Código:** a delegação considera o mesmo limiar de população abaixo do
padrão esperado e de queda de padrão de vida que o painel do Advisor.
A decisão de tesouro por endividamento mantém precedência. As opções
anteriores continuam restauradas ao sair da coordenação.
**Teste sintético:** caso Cuba, limiares de tendência e precedência de
dívida passaram. **Estático:** aprovado. **Campanha:** 0.7.49 NÃO VERIFICADA.
Em cópia do save de Cuba, entre no Automático coordenado, confira quem
é o executor e compare o objetivo aplicado com o painel do Advisor.

## Universidades no Automático

**Código:** enfileira um nível abaixo do teto de inovação. Ambas as filas
devem estar vazias. Exige saldo positivo, guarda fiscal e de materiais,
papel disponível e estado incorporado com infraestrutura e mão de obra.
A coordenação reserva a revisão para o Director quando a universidade é
elegível. Prioridades de oferta, infraestrutura, administração e energia
têm preferência.

**Teste sintético:** cinco testes específicos. **Estático:** validador passou.
Tiger apontou apenas os três campos de Diário 1.15 já registrados.
Instalação conferida com jogo fechado. **Campanha:** NÃO VERIFICADA.
Em cópia de save com inovação abaixo do teto, papel e orçamento adequados,
use Automático, deixe as filas vazias e avance até a revisão mensal.
A fila pública deve receber um nível e o Diário deve confirmar a inclusão.

## Expansões na série 1.15

**Economy Advisor:** 1.0.0 substituiu o OGAS no perfil Better Politics, com
backup e jogo fechado. Carregamento e migração do save do Marrocos NÃO
VERIFICADOS. Variáveis de automação do OGAS podem persistir em saves antigos.

**Debug:** atalho separado instalado. A inicialização gerou logs na pasta privada de debug. Console e conquistas em campanha NÃO VERIFICADOS.

**Auto-Recruit:** cópia local `z.260606.1` ativada no perfil Better Politics.
Ativação conferida no Hydra. Campanha NÃO VERIFICADA.

**Auto-Diplomacy:** cópia local `z.251212.1` ativada depois dos quatro mods do
perfil Better Politics. Perfil salvo com backup. Campanha NÃO VERIFICADA.

**OGAS no jogo base:** perfil ativo com Better Politics, OGAS adaptado e
versões normais do Director e Smart Government. 451 testes sintéticos,
build e validação estática aprovados. Execução em campanha ainda NÃO VERIFICADA.

**Smart Government para Better Politics:** edição 1.0.1 ativa no perfil
após Better Politics, OGAS e Director. Validador aprovou 231 leis em 40
grupos. O ranking exige os requisitos de tramitação e ganho de mérito.
Compara a posição dos grupos de interesse sobre a proposta e a lei vigente,
ponderada por influência, e dá peso dobrado à chance inicial. A votação
efetiva depende de condições calculadas pelo BPM após o início da reforma.
Campanha NÃO VERIFICADA.

Publicada no repositório Smart Government como prévia `v1.0.1-bpm`, no commit `f0f9daf` da branch `codex/better-politics-1.0.1`. O ZIP é idêntico ao instalado localmente.

**CWE fiscal e escassez:** instalado. Snapshot/restauração fiscal, prioridade
a produtor ativo com insumos e limite mensal cobertos por testes focados.
Tiger sem erros nos dois pacotes. Carregamento, campanha e save/reload
ainda NÃO VERIFICADOS.

**Smart Government para CWE:** edição separada, com 211 leis em 60 grupos.
Validador do projeto passou. O Tiger aponta os três campos conhecidos de
Diário da versão 1.15. Instalado e reativado com proteção para posições vazias no ranking.
O ranking em campanha registrou erros de comparação. A causa do
fechamento em 11/01/1950 segue NÃO VERIFICADA. O reteste com a edição de
leis desativada avançou até 15/01 sem erros do ranking.

**Crescimento automático:** decisão instalada e testada no sintético. Ela liga
os gerenciadores do OGAS, usa uma meta de 12 semanas e verifica orçamento
antes de continuar a fila. Tiger sem erros novos. Campanha NÃO VERIFICADA.

**OGAS para CWE:** patch local corrige as referências ao prédio de roupas e
retira um trigger inválido que não tinha chamadas. Tiger 1.19.0 retornou
zero erros, 923 avisos e cinco dicas. A montagem do perfil está confirmada.
Sete testes sintéticos confirmam construção e coordenação do Director.
Execução conjunta em campanha permanece NÃO VERIFICADA.

**Instalação local:** `content_load.json` ativa Cold War Era 0.99, OGAS para CWE e
Director CWE 0.7.46, nessa ordem. A revisão do Cold War Era foi atualizada para
`4d301a80`, correspondente à fonte usada para gerar o Director. Os dois
declaram 1.15.1, e o jogo local está na 1.15.0. A sessão chegou à campanha de 1950, com erros de script e GUI da conversão.
A edição CWE agora inclui Diário, validado pelo Tiger e por cinco testes
sintéticos. Diário e execução em campanha ainda NÃO VERIFICADOS.
O perfil anterior e a cópia CWE para 1.14.5 estão preservados em backup.

- **Estático:** Director normal com Morgenröte 2.9.0 + CMF e com Better
  Politics 2.5.47. Edição CWE testada pelo Tiger contra os scripts do
  Cold War Era 0.99. Combinações, versões e limites em `COMPATIBILITY.md`.
- **Código e Teste sintético:** 439 testes aprovados, incluindo a edição CWE com seleção mensal de ferrovia,
  administração ou usina e custo de materiais derivado da conversão.
- **Carregou/Campanha: NÃO VERIFICADOS.** A instalação local é 1.15.0.
  A revisão CWE analisada declara 1.15.1.

## Retomada da construção no Automático na 0.7.46

- **Código:** após bloqueio por fila privada ou pausa, o evento existente
  volta a conferir em sete dias. Enquanto a trava persiste no mesmo mês,
  só lê as condições de espera. Quando a trava sai ou o mês vira, a
  revisão completa aplica as guardas e o limite mensal de tentativa.
- **Teste sintético:** 436 testes aprovados.
- **Estático:** gerador e validador aprovados. Tiger 1.19.0 com 999 avisos
  e os três apontamentos conhecidos de diário.
- **Campanha:** cronograma real e persistência do evento após save/reload
  ainda NÃO VERIFICADOS. Roteiro específico em `MANUAL_RUNTIME_TEST.md`.

## Automático na 0.7.45

- **Código:** a captura de imposto e salário civil só ocorre antes de um
  passo aplicável. Os snapshots de saves anteriores continuam legíveis e
  preservam a restauração já pendente. O Diário separa a situação atual do
  resultado registrado e informa o bloqueio específico da guarda de orçamento.
- **Teste sintético:** 435 testes aprovados, incluindo ajuste manual após
  revisão sem mudança e exclusividade dos bloqueios de orçamento.
- **Estático:** gerador e validador local aprovados. Tiger 1.19.0 reportou 999
  avisos e os três apontamentos conhecidos de campos de diário.
- **Carregou/Campanha: NÃO VERIFICADOS.** O roteiro 0.7.45 em
  `MANUAL_RUNTIME_TEST.md` cobre save/reload, restauração e leitura dos bloqueios.

## Protocolo de evidência adotado

As orientações do usuário estão em `AGENTS.md` e
`docs/agent/vic3-modding/SKILL.md`, com fontes e ambiente em `references/`.
Código, Teste sintético, Estático, Carregou e Campanha identificam evidências
distintas. A 0.7.17 tem Código e Estático registrados, com execução do Tiger 1.19.0.
A verificação pelo Tiger levou à correção de nove leituras removidas e de um escopo inadequado.
Restam três campos do diário apontados como desconhecidos, presentes no vanilla
1.15 e documentados no jogo. O Tiger declara suporte até 1.13.5. Os avisos de
formatação e de OR de um item permanecem visíveis. A documentação exportada
continua ausente. Carregou e Campanha das leituras fiscais, da prontidão e do
novo retorno salarial e da pontuação de PMs segue NÃO VERIFICADO. Teste sintético — 433 testes aprovados. A 0.7.42 acrescenta a distância em ouro ao texto do status 22 e remove resíduos mortos do status 21/executor 12; a 0.7.43 alinha o bloqueio atual de orçamento (`sed_auto_current_budget`). A 0.7.44 acrescenta eventos didáticos no modo Assistido (por objetivo, com motivo e opções de revisar/adiar/silenciar, sem enfileirar) — Carregou/Campanha NÃO VERIFICADOS. A auditoria encontrou o efeito de disparo sem nenhuma chamada, portanto os avisos são inalcançáveis no fluxo atual. O evento consultivo de importação segue NÃO VERIFICADO na engine. Há relato histórico da obra de Centro de Comércio no Paraguai com 0.7.36 (commit `edfbc81`), com save/reload, efeito na capacidade e segunda revisão ainda pendentes de verificação.

O inventário da auditoria e os casos de snapshot fiscal, orçamento e leitura de fila estão em `PHASE_LOG.md`.

Esta matriz acompanha o briefing e os esclarecimentos do jogador sobre um
coordenador que define objetivos e orienta Economy Advisor e Supply Chain.
Implementação, teste sintético e confirmação de campanha são evidências separadas.

| Requisito | Código e teste sintético | Verificação de campanha e trabalho restante |
|---|---|---|
| Diagnóstico econômico e diário | Implementados, com métricas, data e atualização manual/mensal | Leitura e correção de snapshot observadas na campanha de 1842. Atualização do executor no diagnóstico corrigida na 0.6.16, pendente de confirmação |
| Objetivo nacional atual | Implementado para gargalos, fiscal, crescimento/diversificação e meta industrial anual por escassez persistente | Amostragem mensal corrigida na 0.6.9. Validar seleção e transições em campanha |
| Até três prioridades nacionais | Implementado sobre pares estado/tipo elegíveis. Desde a 0.7.11, fornecedores do mesmo bem são comparados por oferta e margem material estimada, incluindo subprodutos e insumos dos PMs. Desde a 0.7.12, preços observados do mercado e faixas locais alimentam a referência. Desde a 0.7.17, elegibilidade, preferência e plano usam o retorno após a folha salarial observada | Validar layout, unidade salarial e desvios de preferência na engine |
| Setores estratégicos ausentes | Doze bens, incluindo papel desde a 0.7.14, armas, artilharia e munição; cereais cobrem cinco tipos de fazenda e tecido cobre plantação e pecuária. Desde a 0.7.0 o Automático funda a base em estado incorporado apto quando o país não tem produtor verificado | Demais bens ainda têm um único produtor. Confirmar `can_construct_building`, terra e custo real em campanha. Importações continuam fora do escopo |
| Emprego e insumos | Na 0.7.15, fundações industriais próprias usam os insumos da configuração básica verificada e respeitam o controle externo de PMs. Filtros de ocupação, contratação e insumos, mais reserva de mão de obra na 0.6.19 e previsão de insumos adicionais por PMs e compromissos conhecidos na 0.6.20 | Na 0.7.3, fundações e pedidos próprios sem prédio também reservam trabalho e insumos. Calibrar aproximação demográfica e coeficientes. Incluir qualificações, migração e atração de trabalhadores. Calibrar insumos projetados e cobrir modificadores, comércio e produção futuros |
| Reserva, dívida e ritmo | Desde a 0.7.41 o orçamento mostra quanto ouro falta até a reserva exigida (`sed_build_budget_gold_gap = max(ouro exigido − ouro, 0)`); na 0.7.42 o status 22 de revisão também exibe esse valor. Na 0.7.38 a janela de financiamento é `projeto + fila + 4`, sem piso fixo de 26 semanas. Na 0.7.37 a guarda fiscal tem piso único (4 × despesas fixas; 6 × sem dívida em déficit operacional), a classificação 5 e a guarda de saque de 26 semanas foram removidas, e o executor 12/status 21 deixaram de existir (resíduos de UI limpos na 0.7.42). Desde a 0.7.6 a reserva exigida considera fila e novo projeto, sem teto de 56 semanas | Sem mudar limiar. Referência de materiais desde a 0.6.17/0.6.18. Calibrar limiares e custo real incremental, duração com fila concorrente e serviço da dívida |
| Impostos e gastos | Nível de imposto, salário civil e, desde a 0.7.5, salários militares durante crise operacional na paz, com limite mensal, snapshot e restauração | Leitura das rotinas aceita no menu da engine. Observar alterações em campanha e calibrar limiares |
| Coordenação Advisor/Supply Chain | Adaptadores de sete opções de construção, quatro de objetivo/orçamento e três de política do Supply Chain, com restauração | Verificar efeitos reais, save/reload e compatibilidade das versões instaladas |
| Ativar somente caminho necessário | Automático usa rotinas específicas para administração, tributação, energia e, preferencialmente, setores de construção. Desde a 0.7.31, sem ferramenta externa detectada, o executor próprio amplia a administração pública para os objetivos 6 e 7 (burocracia negativa, estado acima da capacidade tributária), um nível por mês e só no estado que excede a capacidade quando o objetivo é 7 | Oferta elegível pode usar alvo direto do plano. Nas rotas externas, a seleção continua sob o algoritmo da ferramenta escolhida. Desde a 0.7.32 o objetivo 9 também tem executor próprio (usina elétrica, 400 pontos, só em estado com energia 20% acima da base e com a tecnologia exigida pelo próprio jogo); com Supply Chain detectado, o caminho externo continua. Conferir em campanha as obras de administração e de usina, e o efeito na burocracia, na capacidade tributária e na oferta de energia |
| Construção própria automática | Desde a 0.7.13 inclui bens civis caros com demanda superior à oferta e margem material positiva. Consome a primeira prioridade, revalida guardas e limita tentativa mensal. Desde a 0.6.25 atua com a fila pública ocupada; só a fila privada precisa estar vazia. Desde a 0.6.26 expande também o setor de construção quando ele lidera o plano e agenda uma segunda revisão no mês após bloqueio por fila privada ou pausa. Desde a 0.7.1 funda a primeira ferrovia em estado com déficit e sem ferrovia | Inclusão direta e persistência ainda exigem evidência de campanha. Espera por obra e transição após fim da escassez tiveram confirmação visual parcial. A fila longa recebe referência de trabalho e materiais desde a 0.7.6; desde a 0.7.23 o painel compara essa referência com a duração restante medida pela engine (`construction_queue_government_duration`, em faixas de 2 a 260 semanas). Progresso já executado, autoria e custo incremental preciso continuam pendentes. A segunda revisão permanece NÃO VERIFICADA. O relato da 0.7.36 registra a construção de Centro de Comércio no Paraguai |
| Evitar executor próprio em paralelo | Executor próprio exclusivo para primeira prioridade de oferta na 0.6.15; opções externas suspensas | ARoAI detectado suspende delegação, autoexpansões nativas continuam sem controle |
| Controle da construção privada externa | Desde a 0.7.27, o painel lê as doze restrições do Controllable Private Construction (`zw_var_*`, somente `has_variable`) e mostra quais estão ligadas, inclusive no bloqueio por fila privada. O Director não escreve essas variáveis nem injeta `can_build_private`/`can_build_government`: isso colidiria com a injeção do próprio mod no mesmo prédio | Exibir a seção e apontar o diário não muda a engine. Se a intervenção no investimento estrangeiro fizer o jogo recusar uma obra pública, a recusa deve aparecer como falha de ação; NÃO VERIFICADO em campanha. A autoexpansão nativa continua fora de controle quando o mod não está ativo |
| Desativar e devolver opções | Restaura presença e valor original das onze opções, com testes de idempotência | Limites fiscais preservados por mês. Confirmar restauração após save/reload e atualização de versão |
| Manual e Assistido | Autorizações e trocas de modo testadas | Restauração pode reativar opções externas originalmente ligadas |
| Histórico | Resultado mensal datado, status externo e livro dos doze bens, ferrovia e setor de construção | Conclusão é inferida pela fila e nível; reduzir ambiguidade de cancelamento |
| Fila sem duplicação | Guardas agregadas, nível após fila e marcas por tipo/estado | Acompanhamento relacionado na 0.6.12. Autor/investidor por item não tem primitiva: sondagem com Tiger 1.19.0 mostra que `is_government_construction`, `is_privately_constructed` e `construction_owner_is_government` são tokens desconhecidos; existem só contagens de país (`num_queued_government_constructions`, `num_queued_private_constructions`, desde a 0.7.24 no painel) e `is_under_construction` por prédio. Identidade do autor e reconciliação completa permanecem pendentes. Com a fila pública ocupada (0.6.25), a não duplicação depende de `level_after_queued_constructions` e das marcas por estado |
| Planejamento de longo prazo | Direção atual, reavaliação periódica e meta anual de oferta para escassez persistente | Na 0.7.4, propagação por vários elos do catálogo, com espera por obra, alternativas e término de ciclos. Desde a 0.7.25, meta de escassez repetida em anos consecutivos vira plurianual (`sed_<bem>_goal_streak` até 5, +15 de prioridade, linha visível enquanto a escassez persistir); bens fora do catálogo e diversificação medida seguem pendentes. Desde a 0.7.39 há feedback de resultado: quando a escassez deixa de ser observada com meta ativa, o painel informa anos de duração e a variação de preço desde o início (`sed_<bem>_goal_result_*`), sobrescrita pela meta seguinte |
| Métodos de produção | Configuração inicial em fundações acompanhadas desde a 0.7.7. Seleção inicial e, desde a 0.7.9, modernização contínua do grupo principal para gargalos, por saída e margem material estimada a preços-base, com reserva mensal de insumos. Desde a 0.7.10, recuperação de escassez por método com menor dependência de insumos e piso de saída nominal. A 0.7.17 fornece a unidade salarial observada aos filtros de oferta; a 0.7.18 desconta a folha da mudança na pontuação de modernização e recuperação | Confirmar na engine. Preços reais pendentes. Qualificações e salários por profissão não têm primitiva legível (sondagem Tiger 1.19.0: `pop_qualifications`, `state_pop_qualifications`, `wages`, `wage_rate`, `average_wage` são tokens desconhecidos); o proxy é `occupancy` + `has_failed_hires`, e desde a 0.7.26 a unidade salarial é por família de prédio com fallback nacional. Desde a 0.7.28 a modernização cede o prédio que o Auto-Apply PMs já administra (`zw_var_auto_pm_building_<prédio>` e os botões de grupo de fazendas/plantações), em vez de disputar o mesmo grupo. Automação dos demais grupos pendente. A ordem dos pares e a configuração inicial seguem apenas materiais |
| Economia militar | Custos, participação das despesas, guerra e cinco bens monitorados. Expansões de armas, artilharia e munição na 0.6.14, com bônus de prioridade em guerra | Confirmar leituras na engine, identificar consumo nacional, planejar indústria bélica, modernização e coordenação do recrutamento |
| Leis, guerra e diplomacia | Fora das mutações econômicas implementadas. Desde a 0.7.20 o painel declara a fronteira e reconhece o Smart Government Advisor instalado (`sg_enabled`), sem repetir recomendações de leis | Mantidas sob responsabilidade dos módulos e decisões previstos pelo briefing. Conferir a exibição com os dois mods na engine |
| Comércio exterior | Limitação de engine confirmada: `create_trade_route` foi removido na 1.9 (Tiger 1.19.0) e `add_trade_route_level`, `cancel_trade_route` e `establish_trade_route` são tokens desconhecidos. Desde a 0.7.21, `sed_pulse.2..13` avisa em evento quando a escassez não tem candidata local, com prazo e três opções; desde a 0.7.22 a descrição mostra os pedidos de compra e venda do mercado. Desde a 0.7.30, quando o bem em escassez não tem produtor no país (`var:sed_plan_missing_<bem> = 1`) e nenhum estado pode receber a fundação, o Automático amplia ou funda um Centro de Comércio para comprar capacidade (`TRADE_CENTER_POINTS = 100`), sem abrir rota, sem tarifa/subvenção e sem construir sob Isolacionismo ou em estado com infraestrutura negativa | Abrir rota continua ação do jogador. Tarifa e subvenção também não são scriptáveis (sondagem 2026-11-12: 13 nomes candidatos responderam `unknown token`), então o sistema de presença/vantagem da 1.9+ não pode ser automatizado por script. Abrir rota continua ação do jogador. Conferir em campanha se o nível aumenta a capacidade usada pelo Mercado Mundial, a entrada na fila do governo, a reserva de 100 pontos e o comportamento após save/reload. Desde a 0.7.29 a descrição ensina o caminho da 1.9+ com termos conferidos no jogo instalado (Centro de Comércio, capacidade de comércio, tarifa/subvenção, Transferência de Bens, `country_disallow_trade_bool` do Isolacionismo). Relato de Campanha (0.7.36): o Automático construiu Centro de Comércio no Paraguai. Efeito na capacidade comercial, distinção entre fundação e ampliação, save/reload, prazo e cooldown permanecem NÃO VERIFICADOS. |
| Haiti, país rico e crise | Cenários sintéticos fiscais e de seleção | Campanhas registradas e comparáveis permanecem pendentes |
| Crescimento em campanha longa | Ainda sem evidência | Medir PIB, SoL, emprego, dívida, reservas e diversificação durante vários anos |
| Localização | Desde a 0.7.29 o arquivo inglês recebe a coluna em inglês. Até a 0.7.28 a bandeira do idioma era reutilizada como rótulo de laço (`for policy, pt, en` e `for good, pt, en`), então `localization('english')` gerava português. Também desde a 0.7.29 parágrafos usam `\n` escapado, porque quebra real invalida a entrada | Conferir no jogo a exibição nos dois idiomas. Não havia teste de idioma antes da 0.7.29 |
| Compatibilidade com mods instalados | **Carregou (2026-11-13):** o jogo abriu com a 0.7.39 e o `error.log` mostrou 1.627 erros `Left side and right side during comparison were of different types`, todos vindos de `advisor_enabled`, `advisor_auto_construction_enabled` e `aroai_autobuild` — bandeiras que o Economy Advisor e o ARoAI criam com `set_variable = <flag>` (valor booleano) e que o Director comparava com `> 0`. Na 0.7.40 a leitura é tipada por dono (presença para booleana, `> 0` só para as numéricas do Supply Chain). **Carregou (0.7.40, reabertura em 2026-11-13):** `error.log` com 108 linhas e zero erros de comparação; os 1.344 `Value of wrong type` de `aroai_preparation_effects.txt:47` e os 5 `Div/0` restantes são todos do ARoAI 1.3.5, cujos arquivos são de 2023 e cujo `supported_game_version` está vazio — recomendado mantê-lo **desativado**. Kuromi's AI v8.0 foi instalado e auditado: `supported_game_version "1.15.*"`, sem referências a `sed_*`, `aroai_*`, `advisor_*` ou `zw_*`. A 0.7.41/0.7.42 ainda não foram reabertas. Auditoria dos 12 mods instalados em `docs/COMPATIBILITY.md`. Desde a 0.7.27 o painel lê o Controllable Private Construction; desde a 0.7.28 a modernização cede o prédio ao Auto-Apply PMs (`zw_var_auto_pm_building_*`) | Conferir em campanha a seção de controle privado e a cessão de PM. `OGAS for CWE` é de 1.13 + Cold War Era e não deve ser usado nesta campanha; Government Administration Auto Expand remove `ai_value` do prédio vanilla |
| Entrega | Gerador, validador, testes, ZIP e instalador com backup | Entrega da 0.6.9 com backup, conferência dos outputs e PR de revisão |

O jogador relatou que seus testes anteriores produziram pouca mudança visível, pois outros construtores já atuavam. Esse relato motivou os adaptadores da 0.6.1.
A 0.6.2 acrescentou a classificação fiscal 5 para construção financiada por reservas e corrigiu a comparação de mês do limite automático. A 0.6.3 amplia o catálogo de produtores locais: cereais em fazendas de trigo, centeio, arroz, milho e milhete, e tecido em plantação de algodão ou fazenda de gado. Ele ainda não confirma os novos fluxos de coordenação, aprovação, persistência ou resultados de crescimento.
A 0.6.4 acrescenta metas industriais anuais: escassez por três meses consecutivos marca o bem como meta até o fim do ano civil, com 25 pontos adicionais no plano e uma linha própria no diário. A meta expira em janeiro ou se reativa se a falta continuar, não dispensa os filtros existentes e não altera objetivo macro, impostos ou orçamento externo. Três meses e 25 pontos são parâmetros iniciais sem calibração em campanha.
A 0.6.5 acrescenta política fiscal própria: no Automático, o nível de imposto sobe um passo em cautela/crise/default e desce um passo quando há superávit, sem dívida e doze semanas de despesas fixas em ouro. O nível original é restaurado ao sair do Automático ou desativar. Salários, despesas, impostos de consumo e leis continuam fora do controle; o efeito real na receita e a aceitação de `set_tax_level` em scripted effects ainda não foram confirmados na engine.
A 0.6.6 estende a política fiscal ao salário civil do governo: corte de um nível em crise/default (piso `low`) e recuperação de um nível com saúde fiscal (teto `medium`), com snapshot e restauração. Cautela, Manual e Assistido não alteram salários. O efeito `set_government_wage_level` só aparece na localização de efeitos vanilla, sem uso em scripts; a aceitação na engine é a principal incerteza. Salários militares, despesas e impostos de consumo continuam fora do controle.
A 0.6.7 acrescenta o livro de resultados dos oito bens: na aprovação o estado guarda nível e variante do produtor; ao sair da fila, nível maior conta como concluído e nível igual ou menor como abandonado. A leitura é inferida, não usa identidade de projeto, e pode ser distorcida por cancelamento seguido de obra externa. Ferrovia e setor de construção ainda não têm registro. A captura usa `b:<prédio>.level` como valor, forma presente no Advisor instalado.
A 0.6.9 estende o livro de resultados a ferrovia e setor de construção, com a mesma inferência por fila e nível. Desativar limpa marcadores e contadores.
Os testes implementados ficam em `tests/test_planning.py`, `tests/test_coordination.py` e na suíte anterior. As fontes e decisões de política estão em [PLANNING.md](PLANNING.md). O roteiro de engine permanece em [MANUAL_RUNTIME_TEST.md](MANUAL_RUNTIME_TEST.md).
A 0.7.2 estima duração e materiais do primeiro projeto e amplia a reserva requerida conforme a duração, com teto de 56 semanas.
A 0.7.1 permite fundar a primeira ferrovia em estado com déficit e sem ferrovia, com as mesmas guardas. Também corrige a pendência da fundação: sem prédio, o pedido deixava de ser tratado como em andamento na leitura seguinte e podia ser duplicado.
A 0.7.0 permite ao Automático fundar a indústria ausente que causa escassez. Se o país não tem produtor verificado e algum estado incorporado aceita a construção, esse estado entra no plano normal e a aprovação enfileira um nível novo, com as guardas fiscais, de materiais, de fila e o limite mensal. Sem estado apto, o objetivo 5 permanece e a obra não é forçada.
A 0.6.26 acrescenta o setor de construção ao dispatcher automático quando ele lidera o plano, com as mesmas guardas fiscais, de materiais e de fila, além de uma segunda revisão por mês após bloqueio pela fila privada ou pela pausa da construção. A execução automática do setor usa a mesma elegibilidade da aprovação manual; a diferença é o limite de uma tentativa mensal.
A 0.6.25 remove a exigência de fila pública vazia do executor próprio. O Automático passa a poder enfileirar seu único nível mensal mesmo com obras de outros construtores na fila; a fila privada continua bloqueando. O limite mensal, a proteção fiscal, a referência de materiais e a checagem por prédio permanecem. Custo incremental de uma fila longa e concorrência real ainda precisam de observação em campanha.
A revisão de calendário, política fiscal e acompanhamento de variantes está registrada em [REVIEW_2026-11-10.md](REVIEW_2026-11-10.md).

## Sincronização de documentação (2026-11-12)

O README e esta matriz foram confrontados com o gerador da 0.7.30. A lista de lacunas herdada da 0.6.26 estava desatualizada em três pontos: métodos de produção (configuração inicial desde a 0.7.7, modernização contínua desde a 0.7.9, recuperação por insumo desde a 0.7.10 e cessão ao Auto-Apply PMs desde a 0.7.28), fundação de prédios (indústria desde a 0.7.0, primeira ferrovia desde a 0.7.1, Centro de Comércio desde a 0.7.30) e salários militares (controlados em crise na paz desde a 0.7.5). O catálogo tem doze bens desde a 0.7.14, e o livro de resultados cobre os doze, a ferrovia e o setor de construção. Continuam fora: comércio exterior por rota, leis, imposto de consumo, gasto discricionário, dívida, recrutamento e consumo real das tropas, custo incremental real, identidade de projeto, qualificações e construtores nativos.
`python3 tools/build_mod.py --check` confirmou sincronia e 394 testes sintéticos passaram; nenhuma mudança de comportamento nesta sincronização.

## Recuperação de fila — 0.7.51

**Código:** dois intervalos mensais delegados ao Advisor com fila pública
vazia permitem uma tentativa direta por candidato elegível. Mantém
guardas fiscais e de materiais e o limite mensal. Fila ocupada zera a
contagem. Pausa e fila privada suspendem a observação.
**Teste sintético:** quatro testes passaram, incluindo devolução ao
Advisor após enfileiramento. **Estático:** validado. Campanha NÃO
VERIFICADA. Obras podem terminar entre as leituras de fila.

## Acompanhamento de obras e reação anual — 0.7.52

**Código:** acompanha o nível concluído dos projetos próprios de madeira,
ferro e ferramentas. Contratação abaixo de 80%, falhas de contratação ou
escassez de insumos conservam a marca de acompanhamento e bloqueiam
nova expansão direta da faixa de crescimento. Candidatos de escassez já
exigem suas guardas de ocupação e insumos.

Reserva reduzida de quatro para duas semanas apenas na construção direta
com orçamento material conhecido, sem dívida, saldo fixo não negativo e
superávit cobrindo o custo material semanal. Financiamento por reserva
continua com o piso anterior. A comparação anual sem avanço de ranking
nem de padrão de vida favorece Standard of Living na delegação ao Advisor.

**Teste sintético:** conclusão/recuperação, fronteira fiscal e reação anual
com restauração ao sair do Automático. **Estático:** validador aprovado.
**Campanha:** NÃO VERIFICADA. Save de Toscana anterior não contém os
marcadores de observação da 0.7.51. Para verificar, use cópia de save,
observe obra própria concluída com ocupação baixa e confira o diagnóstico.

## Resultados de investimento — 0.7.53

**Código:** compara níveis mensais de madeira, ferro, ferramentas,
papel, alimentos e roupas. Expansão observada fica acompanhada enquanto
há contratação limitada, insumos ausentes ou excesso de oferta com
preço abaixo da base. A diversificação delegada de objetivo 8 espera
a recuperação. Outros objetivos continuam com as prioridades existentes.
A primeira leitura cria a referência, sem atribuir autoria à obra.

**Teste sintético:** primeira construção após referência, recuperação
de insumos, mercado comprador, retorno da delegação, deduplicação mensal
e limpeza. Dez testes focados passaram junto às rotinas 0.7.51/0.7.52.
**Estático:** aprovado. Tiger mantém três campos de Diário conhecidos.
**Campanha:** NÃO VERIFICADA. Saves locais disponíveis são anteriores
às versões recentes. Em cópia de save, registre uma leitura, conclua
uma expansão e avance um mês. Confira o diagnóstico no Diário e o
objetivo aplicado na coordenação.
