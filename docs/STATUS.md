# Estado dos requisitos — 0.6.5

Esta matriz acompanha o briefing e os esclarecimentos do jogador sobre um
coordenador que define objetivos e orienta Economy Advisor e Supply Chain.
Implementação, teste sintético e confirmação de campanha são evidências separadas.

| Requisito | Código e teste sintético | Verificação de campanha e trabalho restante |
| --- | --- | --- |
| Diagnóstico econômico e diário | Implementados, com métricas, data e atualização manual/mensal | Indicadores e UI de versões anteriores tiveram confirmação visual parcial |
| Objetivo nacional atual | Implementado para gargalos, fiscal, crescimento/diversificação e meta industrial anual por escassez persistente | Validar seleção, expiração anual e transições na 0.6.4 |
| Até três prioridades nacionais | Implementado sobre pares estado/tipo elegíveis | Validar layout e dados das novas prioridades na engine |
| Setores estratégicos ausentes | Oito bens; cereais cobrem cinco tipos de fazenda e tecido cobre plantação e pecuária | Demais bens ainda têm um único produtor; considerar importações e objetivos industriais |
| Emprego e insumos | Filtros atuais de ocupação, falha de contratação e escassez do prédio | Projetar disponibilidade futura de trabalhadores, qualificações e insumos |
| Reserva, dívida e ritmo | Guarda proporcional inicial, classificações 1–4 e construção financiada por reservas (5) | Calibrar limiares, estimar custo incremental e serviço da dívida |
| Impostos e gastos | Nível de imposto próprio no Automático, com um passo mensal, snapshot e restauração | Calibrar limiares e confirmar na engine; salários, despesas e impostos de consumo permanecem pendentes |
| Coordenação Advisor/Supply Chain | Adaptadores de sete opções de construção e quatro de objetivo/orçamento, com restauração | Verificar efeitos reais, save/reload e compatibilidade das versões instaladas |
| Ativar somente caminho necessário | Automático assume controle de ferramentas detectadas e configura um caminho | A seleção interna de alvos permanece sob o algoritmo da ferramenta escolhida |
| Construção própria automática | Consome a primeira prioridade, revalida guardas e limita tentativa mensal | Inclusão real e persistência ainda exigem evidência de engine |
| Evitar executor próprio em paralelo | Bloqueio explícito durante coordenação | ARoAI detectado suspende delegação, autoexpansões nativas continuam sem controle |
| Desativar e devolver opções | Restaura presença e valor original das onze opções, com testes de idempotência | Confirmar restauração após save/reload e atualização de versão |
| Manual e Assistido | Autorizações e trocas de modo testadas | Restauração pode reativar opções externas originalmente ligadas |
| Histórico | Resultado mensal datado e status de orientação externa | Acrescentar livro de intenções e resultados por alvo |
| Fila sem duplicação | Guardas agregadas, nível após fila e marcas por tipo/estado | Identidade, lado, investidor, conclusão/cancelamento e reconciliação completa |
| Planejamento de longo prazo | Direção atual, reavaliação periódica e meta anual de oferta para escassez persistente | Metas plurianuais, cadeias completas, diversificação medida e feedback de resultados |
| Leis, guerra e diplomacia | Fora das mutações econômicas implementadas | Mantidas sob responsabilidade dos módulos e decisões previstos pelo briefing |
| Haiti, país rico e crise | Cenários sintéticos fiscais e de seleção | Campanhas registradas e comparáveis permanecem pendentes |
| Crescimento em campanha longa | Ainda sem evidência | Medir PIB, SoL, emprego, dívida, reservas e diversificação durante vários anos |
| Entrega | Gerador, validador, testes, ZIP e instalador com backup | Instalação 0.6.5 com backup e 14 outputs conferidos. Publicação segue por PR |

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

Os testes implementados ficam em `tests/test_planning.py`,
`tests/test_coordination.py` e na suíte anterior. As fontes e decisões de
política estão em [PLANNING.md](PLANNING.md). O roteiro de engine permanece em
[MANUAL_RUNTIME_TEST.md](MANUAL_RUNTIME_TEST.md).
