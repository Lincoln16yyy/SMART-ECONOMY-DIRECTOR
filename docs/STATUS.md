# Estado dos requisitos — 0.7.21

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
novo retorno salarial e da pontuação de PMs seguem NÃO VERIFICADO. Teste
sintético — 370 testes aprovados. O evento consultivo de importação da 0.7.21
segue NÃO VERIFICADO na engine.

Esta matriz acompanha o briefing e os esclarecimentos do jogador sobre um
coordenador que define objetivos e orienta Economy Advisor e Supply Chain.
Implementação, teste sintético e confirmação de campanha são evidências separadas.

| Requisito | Código e teste sintético | Verificação de campanha e trabalho restante |
| --- | --- | --- |
| Diagnóstico econômico e diário | Implementados, com métricas, data e atualização manual/mensal | Leitura e correção de snapshot observadas na campanha de 1842. Atualização do executor no diagnóstico corrigida na 0.6.16, pendente de confirmação |
| Objetivo nacional atual | Implementado para gargalos, fiscal, crescimento/diversificação e meta industrial anual por escassez persistente | Amostragem mensal corrigida na 0.6.9. Validar seleção e transições em campanha |
| Até três prioridades nacionais | Implementado sobre pares estado/tipo elegíveis. Desde a 0.7.11, fornecedores do mesmo bem são comparados por oferta e margem material estimada, incluindo subprodutos e insumos dos PMs. Desde a 0.7.12, preços observados do mercado e faixas locais alimentam a referência. Desde a 0.7.17, elegibilidade, preferência e plano usam o retorno após a folha salarial observada | Validar layout, unidade salarial e desvios de preferência na engine |
| Setores estratégicos ausentes | Doze bens, incluindo papel desde a 0.7.14, armas, artilharia e munição; cereais cobrem cinco tipos de fazenda e tecido cobre plantação e pecuária. Desde a 0.7.0 o Automático funda a base em estado incorporado apto quando o país não tem produtor verificado | Demais bens ainda têm um único produtor. Confirmar `can_construct_building`, terra e custo real em campanha. Importações continuam fora do escopo |
| Emprego e insumos | Na 0.7.15, fundações industriais próprias usam os insumos da configuração básica verificada e respeitam o controle externo de PMs. Filtros de ocupação, contratação e insumos, mais reserva de mão de obra na 0.6.19 e previsão de insumos adicionais por PMs e compromissos conhecidos na 0.6.20 | Na 0.7.3, fundações e pedidos próprios sem prédio também reservam trabalho e insumos. Calibrar aproximação demográfica e coeficientes. Incluir qualificações, migração e atração de trabalhadores. Calibrar insumos projetados e cobrir modificadores, comércio e produção futuros |
| Reserva, dívida e ritmo | Guarda proporcional inicial, classificações 1–4 e construção financiada por reservas (5). Desde a 0.7.6 a reserva exigida considera a fila e o novo projeto, sem teto de 56 semanas, e o executor direto pode usar financiamento por reservas | Referência de materiais implementada na 0.6.17 e limitada por níveis/ocupação na 0.6.18. Calibrar limiares e custo real incremental, duração com fila concorrente e serviço da dívida |
| Impostos e gastos | Nível de imposto, salário civil e, desde a 0.7.5, salários militares durante crise operacional na paz, com limite mensal, snapshot e restauração | Leitura das rotinas aceita no menu da engine. Observar alterações em campanha e calibrar limiares |
| Coordenação Advisor/Supply Chain | Adaptadores de sete opções de construção, quatro de objetivo/orçamento e três de política do Supply Chain, com restauração | Verificar efeitos reais, save/reload e compatibilidade das versões instaladas |
| Ativar somente caminho necessário | Automático usa rotinas específicas para administração, tributação, energia e, preferencialmente, setores de construção | Oferta elegível pode usar alvo direto do plano. Nas rotas externas, a seleção continua sob o algoritmo da ferramenta escolhida |
| Construção própria automática | Desde a 0.7.13 inclui bens civis caros com demanda superior à oferta e margem material positiva. Consome a primeira prioridade, revalida guardas e limita tentativa mensal. Desde a 0.6.25 atua com a fila pública ocupada; só a fila privada precisa estar vazia. Desde a 0.6.26 expande também o setor de construção quando ele lidera o plano e agenda uma segunda revisão no mês após bloqueio por fila privada ou pausa. Desde a 0.7.1 funda a primeira ferrovia em estado com déficit e sem ferrovia | Inclusão direta e persistência ainda exigem evidência de campanha. Espera por obra e transição após fim da escassez tiveram confirmação visual parcial. A fila longa recebe referência de trabalho e materiais desde a 0.7.6. Progresso real, autoria e custo incremental preciso continuam pendentes. Agenda da segunda revisão não observada na engine |
| Evitar executor próprio em paralelo | Executor próprio exclusivo para primeira prioridade de oferta na 0.6.15; opções externas suspensas | ARoAI detectado suspende delegação, autoexpansões nativas continuam sem controle |
| Desativar e devolver opções | Restaura presença e valor original das onze opções, com testes de idempotência | Limites fiscais preservados por mês. Confirmar restauração após save/reload e atualização de versão |
| Manual e Assistido | Autorizações e trocas de modo testadas | Restauração pode reativar opções externas originalmente ligadas |
| Histórico | Resultado mensal datado, status externo e livro dos oito bens, ferrovia e setor de construção | Conclusão é inferida pela fila e nível; reduzir ambiguidade de cancelamento |
| Fila sem duplicação | Guardas agregadas, nível após fila e marcas por tipo/estado | Acompanhamento relacionado na 0.6.12. Identidade, lado, investidor e reconciliação completa permanecem pendentes. Com a fila pública ocupada (0.6.25), a não duplicação depende de `level_after_queued_constructions` e das marcas por estado |
| Planejamento de longo prazo | Direção atual, reavaliação periódica e meta anual de oferta para escassez persistente | Na 0.7.4, propagação por vários elos do catálogo, com espera por obra, alternativas e término de ciclos. Metas plurianuais, bens fora do catálogo, diversificação medida e feedback de resultados |
| Métodos de produção | Configuração inicial em fundações acompanhadas desde a 0.7.7. Seleção inicial e, desde a 0.7.9, modernização contínua do grupo principal para gargalos, por saída e margem material estimada a preços-base, com reserva mensal de insumos. Desde a 0.7.10, recuperação de escassez por método com menor dependência de insumos e piso de saída nominal. A 0.7.17 fornece a unidade salarial observada aos filtros de oferta; a 0.7.18 desconta a folha da mudança na pontuação de modernização e recuperação | Confirmar na engine. Preços reais, qualificações, salários por profissão e automação dos demais grupos pendentes. A ordem dos pares e a configuração inicial seguem apenas materiais |
| Economia militar | Custos, participação das despesas, guerra e cinco bens monitorados. Expansões de armas, artilharia e munição na 0.6.14, com bônus de prioridade em guerra | Confirmar leituras na engine, identificar consumo nacional, planejar indústria bélica, modernização e coordenação do recrutamento |
| Leis, guerra e diplomacia | Fora das mutações econômicas implementadas. Desde a 0.7.20 o painel declara a fronteira e reconhece o Smart Government Advisor instalado (`sg_enabled`), sem repetir recomendações de leis | Mantidas sob responsabilidade dos módulos e decisões previstos pelo briefing. Conferir a exibição com os dois mods na engine |
| Comércio exterior | Limitação de engine confirmada: `create_trade_route` foi removido na 1.9 (Tiger 1.19.0) e `add_trade_route_level`, `cancel_trade_route` e `establish_trade_route` são tokens desconhecidos. Desde a 0.7.21, `sed_pulse.2..13` avisam em evento quando a escassez não tem candidata local, com prazo e três opções | Abrir rota continua ação do jogador. Confirmar no jogo a exibição do evento, o prazo de 3 e o cooldown de 6/12/24 meses |
| Haiti, país rico e crise | Cenários sintéticos fiscais e de seleção | Campanhas registradas e comparáveis permanecem pendentes |
| Crescimento em campanha longa | Ainda sem evidência | Medir PIB, SoL, emprego, dívida, reservas e diversificação durante vários anos |
| Entrega | Gerador, validador, testes, ZIP e instalador com backup | Entrega da 0.6.9 com backup, conferência dos outputs e PR de revisão |

O jogador relatou que seus testes anteriores produziram pouca mudança visível,
pois outros construtores já atuavam. Esse relato motivou os adaptadores da 0.6.1.
A 0.6.2 acrescentou a classificação fiscal 5 para construção financiada por
reservas e corrigiu a comparação de mês do limite automático. A 0.6.3 amplia o
catálogo de produtores locais: cereais em fazendas de trigo, centeio, arroz,
milho e milhete, e tecido em plantação de algodão ou fazenda de gado. Ele ainda
não confirma os novos fluxos de coordenação, aprovação, persistência ou
resultados de crescimento.

A 0.6.4 acrescenta metas industriais anuais: escassez por três meses
consecutivos marca o bem como meta até o fim do ano civil, com 25 pontos
adicionais no plano e uma linha própria no diário. A meta expira em janeiro ou
se reativa se a falta continuar, não dispensa os filtros existentes e não
altera objetivo macro, impostos ou orçamento externo. Três meses e 25 pontos
são parâmetros iniciais sem calibração em campanha.

A 0.6.5 acrescenta política fiscal própria: no Automático, o nível de imposto
sobe um passo em cautela/crise/default e desce um passo quando há superávit,
sem dívida e doze semanas de despesas fixas em ouro. O nível original é
restaurado ao sair do Automático ou desativar. Salários, despesas, impostos de
consumo e leis continuam fora do controle; o efeito real na receita e a
aceitação de `set_tax_level` em scripted effects ainda não foram confirmados na
engine.

A 0.6.6 estende a política fiscal ao salário civil do governo: corte de um
nível em crise/default (piso `low`) e recuperação de um nível com saúde fiscal
(teto `medium`), com snapshot e restauração. Cautela, Manual e Assistido não
alteram salários. O efeito `set_government_wage_level` só aparece na
localização de efeitos vanilla, sem uso em scripts; a aceitação na engine é a
principal incerteza. Salários militares, despesas e impostos de consumo
continuam fora do controle.

A 0.6.7 acrescenta o livro de resultados dos oito bens: na aprovação o estado
guarda nível e variante do produtor; ao sair da fila, nível maior conta como
concluído e nível igual ou menor como abandonado. A leitura é inferida, não
usa identidade de projeto, e pode ser distorcida por cancelamento seguido de
obra externa. Ferrovia e setor de construção ainda não têm registro. A captura
usa `b:<prédio>.level` como valor, forma presente no Advisor instalado.

A 0.6.9 estende o livro de resultados a ferrovia e setor de construção, com a
mesma inferência por fila e nível. Desativar limpa marcadores e contadores.

Os testes implementados ficam em `tests/test_planning.py`,
`tests/test_coordination.py` e na suíte anterior. As fontes e decisões de
política estão em [PLANNING.md](PLANNING.md). O roteiro de engine permanece em
[MANUAL_RUNTIME_TEST.md](MANUAL_RUNTIME_TEST.md).

A 0.7.2 estima duração e materiais do primeiro projeto e amplia a reserva
requerida conforme a duração, com teto de 56 semanas.

A 0.7.1 permite fundar a primeira ferrovia em estado com déficit e sem
ferrovia, com as mesmas guardas. Também corrige a pendência da fundação: sem
prédio, o pedido deixava de ser tratado como em andamento na leitura seguinte e
podia ser duplicado.

A 0.7.0 permite ao Automático fundar a indústria ausente que causa escassez.
Se o país não tem produtor verificado e algum estado incorporado aceita a
construção, esse estado entra no plano normal e a aprovação enfileira um nível
novo, com as guardas fiscais, de materiais, de fila e o limite mensal. Sem
estado apto, o objetivo 5 permanece e a obra não é forçada.

A 0.6.26 acrescenta o setor de construção ao dispatcher automático quando ele
lidera o plano, com as mesmas guardas fiscais, de materiais e de fila, além de
uma segunda revisão por mês após bloqueio pela fila privada ou pela pausa da
construção. A execução automática do setor usa a mesma elegibilidade da
aprovação manual; a diferença é o limite de uma tentativa mensal.

A 0.6.25 remove a exigência de fila pública vazia do executor próprio. O
Automático passa a poder enfileirar seu único nível mensal mesmo com obras de
outros construtores na fila; a fila privada continua bloqueando. O limite
mensal, a proteção fiscal, a referência de materiais e a checagem por prédio
permanecem. Custo incremental de uma fila longa e concorrência real ainda
precisam de observação em campanha.

A revisão de calendário, política fiscal e acompanhamento de variantes está
registrada em [REVIEW_2026-11-10.md](REVIEW_2026-11-10.md).
