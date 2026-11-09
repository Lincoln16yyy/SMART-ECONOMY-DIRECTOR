# Plano de teste da campanha — interface 0.5.3

Estado atual: [auditoria de 09/11/2026](AUDIT_2026-11-09.md). Os roteiros abaixo
não são resultados executados. Não iniciar novas funcionalidades até fechar
fila/reconciliação/opções do país. Usar cópia dedicada e registrar build, commit,
mods e opções. Uma tentativa simulada não confirma inclusão no jogo.
As capturas de junho/1839 confirmam modo Automático e texto de filas ocupadas;
ignorar/restaurar e detalhamento novo não foram conferidos na engine.


O jogador confirmou em campanha a interface e as leituras principais da 0.1.0,
a renderização das seções ferroviária e de capacidade de construção vazias na
0.3.0. A 0.3.1 teve os estados vazios conferidos; o candidato e a trava da fila
privada também apareceram em campanha. A aprovação, as linhas de motivo das
versões 0.3.2–0.3.4 e a convivência com o conjunto de mods continuam **não
testadas em campanha**. A suíte automatizada atual executa os scripts gerados
em um modelo restrito de país/estado/edifício e cobre filtros, ranking, travas,
contagens disjuntas de rejeição, confirmação/rejeição da fila e limpeza; ela
não é evidência de renderização ou de aceitação pela engine.

## Checklist específico da versão 0.1.0

| Ação | Resultado a conferir dentro do jogo |
| --- | --- |
| Carregar save novo/existente sem ativar | Nenhum diagnóstico ou automação aparece sozinho |
| Decisão Ativar Smart Economy Director | Uma única Journal Entry aparece com leitura inicial e mês/ano |
| Abrir o diário | Textos em português, sem chaves cruas ou números cortados; scroll permite ler todos os controles e indicadores |
| Comparar saldo, reservas, dívida e crédito | Valores correspondem ao país e data; estoque e fluxo semanal não estão confundidos |
| Comparar população, PIB, SoL e alfabetização | Conferir abrangência do indicador, principalmente população incorporada versus total |
| Comparar filas e infraestrutura | Projetos não são tratados como níveis; estados pertencem ao país jogador |
| Atualizar repetidamente no mesmo mês | Leituras mudam conforme o jogo, mas não surge uma falsa variação mensal de PIB |
| Avançar um mês | Uma atualização, sem duplicar diário; crescimento usa a primeira amostra-base do mês anterior registrado |
| Atualizar sob solicitação e avançar meses | Última leitura e indicadores ficam congelados até clicar em atualizar |
| Atualizar todo mês | Leitura imediata; leituras mensais voltam a acontecer |
| Desativar e avançar meses | Diário encerra e não volta sozinho; variáveis operacionais removidas, só schema retido |
| Reativar | Leituras novas; crescimento volta a indisponível até haver outra amostra mensal |
| Salvar e recarregar | Ativação, agenda e amostras pertencem ao país e permanecem coerentes |

Caso o diário esteja inacessível por um problema de interface, a decisão
**Desativar Smart Economy Director** continua sendo a saída de limpeza.

## Preparação

Registrar versão/build, commit do Director, DLCs, mods, ordem e opções de cada
automação. Com o jogo fechado, fazer backup do load order e usar cópia de save,
nunca o único arquivo da campanha. Não sobrescrever a cópia de teste do Smart
Government; preparar uma cópia própria do Haiti para o Director.

Executar primeiro vanilla + Director; depois adicionar os mods e, por fim,
testar o conjunto completo. Comparar logs antes/depois, guardando os novos
erros com arquivo e linha. Nenhum botão pode ser aprovado só por aparecer.

Registrar as flags efetivas no país: Economy Advisor (habilitação, construção,
mão de obra e balanceamento de PM), opções do Supply Chain, Auto-Apply e a
regra/flag de autobuild do ARoAI. O save Haiti encontrado é binário; a ocorrência
do nome de uma variável não comprova seu valor nem seu dono. Conferir as opções
na interface ou usar decodificação estruturada compatível.

Comparar também porto básico e administração com as definições carregadas:
ARoAI redefine PMs com dados diferentes da instalação vanilla 1.15.

## Ciclo de vida e interface

Verificar ativação por decisão, save existente, nova campanha, pulso mensal,
atualização manual, data, valores contra as telas do jogo, persistência após
recarregar e ausência de JE duplicada. Desativar, avançar meses e confirmar
que não reativa sozinho; reativar e testar limpeza/migração de variáveis.
Conferir português e fallback inglês, tooltip, ignorar/restaurar e estado vazio.

Na 0.2.0, confirmar que a ação ocorre só após aprovação individual e
revalidação. A partir de 0.3.6, conferir também os modos abaixo. Reordenar as recomendações antes de clicar para verificar que
o botão continua ligado ao estado mostrado. A 0.3.0 mantém o mesmo contrato
para as duas seções e para a nova ação de capacidade de construção.

## Checklist da ação ferroviária 0.2.1

Use uma cópia do save. Para aparecer uma oportunidade, aplicam-se os filtros
estaduais abaixo. O país deve estar fora de inadimplência e a fila privada vazia para aprovar;
a pausa do jogo não é exigida. Saldo semanal negativo gera um alerta, mas não
bloqueia a aprovação desde a 0.3.4. A
recomendação requer uma ferrovia já construída, ocupação de pelo menos 80%, sem
falha de contratação ou falta de insumos, num estado incorporado com
infraestrutura negativa e sem expansão ferroviária já enfileirada.

| Ação | Resultado a conferir |
| --- | --- |
| Abrir a seção de oportunidades | Até três estados ordenados pelo maior déficit observado; sem candidato e sem déficit, explica que não há oportunidade de infraestrutura; com déficit mas sem candidato, explica que os filtros ferroviários rejeitaram os estados |
| Aprovar com jogo rodando e Assistido ativo | Revalidação segue normalmente; não há trava de pausa |
| Pausar, criar fila privada ou entrar em inadimplência | Botão desabilitado ao consultar de novo a elegibilidade |
| Manter saldo semanal negativo, com as outras travas liberadas | Alerta financeiro aparece e o botão continua clicável |
| Reordenar fila pública/privada antes do clique | Uma expansão pública para o estado mostrado, ou botão desabilitado se a ferrovia já estiver na fila |
| Aprovar uma oportunidade | Contador público aumenta em um nível; aviso confirma a inclusão; não há repetição automática |
| Atualizar diagnóstico depois de aprovar | Mesmo estado não volta a oferecer o nível enquanto a expansão estiver enfileirada |
| Cancelar a expansão e atualizar | A recomendação pode reaparecer se o déficit e os demais filtros persistirem |
| Salvar/recarregar após a aprovação | Fila normal do jogo persiste e a recomendação não duplica |

Registrar saldo, contador público antes/depois, estado, prédio, ocupação,
infraestrutura, filas, estado de pausa e flags dos outros construtores. A ação
não estima custo, uso de construção futuro, contratação ou retorno. Se não
houver candidato no save atual, isso não invalida o botão; significa que este
tipo de oportunidade não passou os filtros.

## Checklist da capacidade de construção 0.3.0

A recomendação exige uma fila pública com pelo menos três projetos. O estado
precisa ter um setor de construção já construído, ocupação de pelo menos 90%,
sem falha de contratação ou falta de insumos, sem expansão já enfileirada e
elegibilidade normal do jogo. Não é preciso pausar o jogo; o país deve estar fora de inadimplência e com
fila privada vazia. Saldo negativo gera apenas um alerta
desde a 0.3.4. Entre os
setores elegíveis, o Director mostra o estado mais populoso.

| Ação | Resultado a conferir |
| --- | --- |
| Abrir a seção com fila pública curta | Explica que há menos de três projetos e não recomenda ampliar capacidade |
| Abrir a seção com fila pública de três ou mais projetos | Mostra no máximo um setor de construção, ou explica que nenhum passou pelos filtros |
| Aprovar com jogo rodando e Assistido ativo | Revalidação segue normalmente; não há trava de pausa |
| Pausar, criar fila privada ou entrar em inadimplência | Botão desabilitado na revalidação |
| Manter saldo semanal negativo com as outras travas liberadas | Alerta financeiro aparece e o botão continua clicável |
| Reduzir a fila pública para menos de três projetos antes do clique | Botão desabilitado ou candidato recusado |
| Aprovar o setor mostrado | Contador público aumenta em um nível; aviso confirma; nenhuma repetição automática |
| Atualizar o diagnóstico depois de aprovar | O mesmo estado não volta a oferecer o setor enquanto a expansão estiver enfileirada |
| Cancelar ou concluir a expansão e atualizar | A recomendação pode reaparecer se a fila e os demais filtros persistirem |
| Salvar/recarregar após a aprovação | Fila normal persiste; o pedido não duplica |

Registrar a fila pública antes/depois, o nível do setor, ocupação, insumos,
população do estado, pausa, saldo e flags dos outros construtores. A ação não
promete que o novo nível será contratado nem que reduzirá o prazo da fila.

## Checklist da decomposição de motivos 0.3.1

Quando não há candidato, cada seção mostra uma linha de motivos com contagens
por estado. Na seção ferroviária, o total de estados com déficit de
infraestrutura é dividido em sem ferrovia, ferrovia não operante e bloqueados
por incorporação ou permissão; na capacidade de construção, o total de
estados com setor é dividido em setor não operante e bloqueados. Cada estado
entra em um único motivo, e as contagens somam o total exibido. Os contadores
são zerados a cada leitura. A atualização, a agenda sob solicitação, a
desativação e a apresentação do candidato de construção foram confirmadas
em campanha; a linha de motivos visível e o clique de aprovação ainda não.

| Ação | Resultado a conferir |
| --- | --- |
| Abrir as seções sem candidato | Linha de motivos visível e valores coerentes com os estados do país; a soma das parcelas corresponde ao total |
| Atualizar duas vezes no mesmo mês | Contagens permanecem as mesmas, sem acumular entre leituras |
| Fazer um candidato aparecer (ou usar cópia de save com um) | Linha some e a recomendação aparece |
| Atualizar após a aprovação | O estado aprovado sai da lista e os contadores refletem o estado atual |
| Comparar com a telinha de estados do jogo | Estados sem ferrovia/setor e prédios parados correspondem às parcelas mostradas |

Registrar totais e parcelas de cada seção, data da leitura e se a linha
sumiu quando surgiu candidato. A decomposição descreve os filtros atuais;
não estima custo, prazo ou retorno.

## Checklist do motivo do botão bloqueado 0.3.4

Quando um candidato está listado, mas o botão de aprovar está
bloqueado, uma linha sob o botão nomeia a primeira guarda que falha: fila pública abaixo de três projetos (apenas construção), fila
privada não vazia ou inadimplência. O saldo semanal negativo não bloqueia mais
a aprovação: aparece como alerta para revisar o custo na fila. O jogador
clicou com fila privada de 2 projetos e apenas o tooltip com cadeado
indicou o bloqueio, sem dizer qual trava falhava; a 0.3.2 deve mostrar
“Botão bloqueado: há níveis na fila privada” nesse cenário.

| Ação | Resultado a conferir |
| --- | --- |
| Abrir o candidato com fila privada não vazia | Linha de motivo indica a fila privada |
| Esvaziar a fila privada, pausar e reabrir/atualizar | Linha some e o botão fica clicável |
| Testar com jogo rodando | Não deve aparecer bloqueio por falta de pausa |
| Testar em inadimplência | Linha indica inadimplência |
| Testar com saldo semanal negativo e demais travas liberadas | Alerta financeiro aparece, mas botão continua clicável |
| Na construção, reduzir a fila pública para menos de três | Linha indica a fila pública |
| Aprovar com fila privada vazia | Nível entra na fila pública; aviso confirma; sem repetição automática |

Depois dessa conferência, os pontos restantes são desativação (já uma vez
confirmada), save/recarregar e a convivência com os outros construtores
antes de ampliar os tipos de ação.

## Checklist de recomendação desatualizada e pendente 0.3.4

As listas são calculadas na última leitura, mas as travas são avaliadas ao
vivo. Se uma fila ou condição estadual mudar antes da leitura seguinte, o
cartão pode continuar visível com o botão desabilitado. A nova linha deve
explicar que a recomendação mudou ou já foi enfileirada. Cartão desatualizado
pede nova leitura e não executa a ação; cartão já enfileirado diz para não
aprovar de novo. Nenhuma ação deve ser executada pelo cartão antigo.

## Cenários econômicos

| Cenário | Verificação e evidência exigida |
| --- | --- |
| Haiti pequeno | Emprego, orçamento, infraestrutura e insumos permitem as prioridades? Registrar motivos e candidatos rejeitados |
| País rico | Investimento aproveita capacidade sem expandir setor saturado? Comparar fila e custos recorrentes |
| Crise fiscal | Exibir saldo, reservas e dívida; alerta financeiro acompanha o candidato, e a aprovação manual segue disponível fora de default quando as demais travas passam |
| Escassez | Distinguir preço alto de falta de insumo; impedir indústria dependente de abastecimento inexistente |
| Sem oportunidade | Até zero recomendações; fila vazia permitida; nenhum candidato artificial |
| Fila privada e pública | Mesmo edifício/estado em ambas, obra em andamento, primeira construção e cancelamento; nenhum pedido duplicado |
| Mods de PM | Mudança externa após análise invalida candidato e atualiza mão de obra/insumos; ausência de troca de volta pelo Director |
| Campanha longa | Amostras mensais e comparação em 1, 5, 10, 20 e 30 anos, com controle sem Director quando viável |

Registrar PIB, PIB per capita, padrão de vida, emprego, alfabetização,
infraestrutura, saldo, reservas, dívida, preços, produção e diversificação;
valor indisponível deve constar como indisponível. Guardar fila, ações,
modo e opções dos outros mods em cada marco. Crescimento do PIB isolado não
aprova o cenário. Medir tempo de atualização e tamanho do histórico/save.

Encerrar restaurando o load order de teste e preservando evidências separadas.
Testes automatizados futuros devem cobrir pontuação, restrições fiscais,
deduplicação, atualização, estados vazios, schema, localização e integridade GUI;
eles complementam esse roteiro, sem substituir os cliques na engine.

## Checklist de oferta por bem em escassez 0.3.5

Use um save em que o mercado registre escassez de pelo menos um dos bens da
lista. A leitura precisa mostrar a seção do bem mesmo se nenhum produtor local
passar pelos filtros; nesse caso, deve explicar que nenhum candidato foi
recomendado. A ação só considera prédio produtor já existente em estado
incorporado, com ocupação ≥80%, sem falha de contratação, sem falta de insumos,
sem expansão enfileirada e com um método ativo que produza positivamente o bem.

| Ação | Resultado a conferir |
| --- | --- |
| Mercado sem escassez dos oito bens | Nenhuma seção de oferta aparece |
| Escassez com produtor elegível | Seção identifica bem e estado, mostra prédio e botão explícito |
| Escassez sem produtor elegível | Mensagem explica por que não há recomendação; nenhum botão oculto ou automático |
| Método ativo que consome o bem ou não o produz | O estado não entra na lista |
| Tirar a pausa antes de clicar | Em Assistido, botão continua disponível quando as demais guardas passam (desde 0.3.6) |
| Enfileirar na fila privada ou entrar em inadimplência | Botão desabilitado com o motivo correspondente |
| Manter saldo semanal negativo, com as demais guardas liberadas | Alerta financeiro aparece; botão continua habilitado |
| Mudar a escassez ou estado do produtor depois da leitura | Cartão fica desatualizado e o clique não enfileira obra |
| Aprovar com as guardas liberadas | Apenas um nível público do prédio indicado é adicionado; linha confirma a inclusão |
| Atualizar após a aprovação | A mesma expansão permanece pendente e não pode ser duplicada |
| Cancelar ou concluir e atualizar | O marcador pendente limpa; a recomendação só volta se ainda elegível e o bem continuar escasso |

Conferir oito pares bem/prédio (madeira, ferro, carvão, cereais, tecido,
ferramentas, mantimentos e roupas), método de produção ativo, escassez no
mercado, estado, filas, saldo, pausa e status de inadimplência. Esta fase não
prevê custos, preços futuros, retorno ou emprego do novo nível; a expansão
apenas acrescenta um nível à fila normal do jogo.

## Modos e automação opt-in 0.3.7

| Ação | Resultado esperado |
| --- | --- |
| Abrir diário ativado | Botões Manual, Assistido e Automático visíveis no topo; Assistido aparece como modo inicial em save sem escolha |
| Clicar Manual | Status visível; botões individuais permanecem visíveis e indisponíveis |
| Clicar Assistido | Botões individuais podem ser aprovados; não é exigido pausar o jogo; confirmar que fila e estado são revalidados no clique |
| Clicar Automático | Status e limite de uma ação mensal visíveis; nenhum nível é enfileirado imediatamente ao trocar modo |
| Avançar até revisão automática | No máximo um nível entra na fila pública no mês; conferir qual candidato foi escolhido |
| Fila ocupada | Revisão não enfileira e mostra que as filas pública/privada já estão ocupadas |
| Inadimplência | Revisão não enfileira e mostra a suspensão fiscal |
| Construção pausada | Revisão não enfileira e mostra a pausa da fila |
| Automação concorrente conhecida | Revisão não enfileira e identifica outro construtor ativo |
| Nenhum candidato elegível | Mostra status de ausência de candidato, sem confundir com trava operacional |
| Outro construtor conhecido ativo | Automação do Director fica bloqueada; confirmar variáveis no save/mod ativo |
| Voltar de Automático para Assistido/Manual | A próxima revisão não executa ação automática |
| Save antigo sem variável de modo | Migra para Assistido, sem ligar Automático sozinho |
| Desativar com evento pendente | Evento não executa ação depois da desativação |

A 0.3.6 removeu a exigência de pausa dos botões individuais após a falsa
mensagem observada na captura do Egito. A fila de construção pausada só bloqueia
o executor automático. Fazer esses passos em uma cópia de save e parar se houver
erro de script ou um clique duplicar construção.


## Regressões de integridade 0.3.8

- Com filas vazias e dois estados ferroviários elegíveis de déficits distintos,
  comparar a primeira recomendação com o estado escolhido na revisão automática:
  ambos devem priorizar o maior déficit.
- No mesmo estado, manter uma expansão de produtor pendente e concluir/cancelar
  uma expansão de setor de construção. Atualizar: a marca do produtor deve
  persistir enquanto seu próprio nível permanece enfileirado.
- Desativar: todas as marcas estaduais do Director devem ser removidas.

Esses casos passaram no harness; a confirmação na engine permanece pendente.


## Revisão com inclusão não confirmada 0.3.9

Se a revisão selecionar candidato mas não confirmar aumento na fila pública,
o diário deve informar inclusão não confirmada, pedir conferência da fila e
explicar que não tentou outra expansão nessa revisão. Não deve informar
"sem ação elegível". Esse caminho foi verificado por inserção recusada no
harness; não foi identificado um método seguro para forçar a recusa na engine.

Com evento já agendado, trocar para Manual/Assistido ou desativar antes de sua
execução deve impedir a ação. Em Automático, a execução deve permitir agendar
novamente no pulso mensal seguinte. Conferir também save/reload com evento
pendente; persistência e passagem de tempo não são simuladas pelos testes.


## Motivos dos produtores rejeitados 0.4.0

Em uma escassez sem candidato, atualizar e conferir os estados com produtor e
os sete motivos da última leitura. Se um estado falhar em mais de um filtro,
conta apenas no primeiro motivo da ordem exibida. Estados sem o prédio não
entram na contagem. Se o total de produtores for zero, nenhuma expansão é
proposta. Conferir incorporação, ocupação, falha de contratação, insumos, método
ativo e fila no painel do produtor. Atualizar após mudanças: contadores devem
ser recalculados. Com candidato elegível ou escassez resolvida, o detalhamento
fica oculto. Desativar e reativar não deve reter contagens da leitura anterior.


## Ignorar e restaurar 0.4.1

Em cópia de save, abrir candidato elegível e clicar em Ignorar: o cartão deve
sumir após a leitura e o aviso/restauração deve aparecer no topo. Atualizar e
trocar de modo não deve trazer a expansão de volta. Conferir outro estado e
outro tipo de produtor no mesmo estado: a preferência não deve bloqueá-los.
No Automático, a revisão não pode selecionar a expansão ignorada.

Salvar/recarregar antes de restaurar: a escolha deve permanecer. Restaurar no
topo: candidato só volta se ainda elegível, nenhuma obra é adicionada pelo
botão e expansões já pendentes permanecem na fila. Desativar/reativar deve
limpar as preferências. Conferir altura dos cartões, tooltips e novo motivo
"ignorado por você" nos diagnósticos vazios. Esse fluxo ainda não foi testado
na engine; os testes locais executam os scripts gerados em harness.


## Interface 0.5.0 — conferência futura, sem pedido de teste nesta entrega

Quando o jogador estiver pronto, conferir fundo/borda e texto dos modos,
Atualizar, Desativar, Mostrar/Ocultar e botões nos cartões. Corpo 20/títulos 26,
controles 52 pixels; textos devem quebrar dentro do painel. Conferir cartão
com motivo de bloqueio e alerta financeiro simultâneos sem sobreposição.
Mostrar detalhes não deve executar obras; recolher não deve remover cartões.
Critérios de aprovação e limitações da auditoria permanecem iguais.


## Cartões acionáveis 0.5.1 — roteiro futuro

Conferir que Passar para Assistido muda apenas o modo, mantendo o prédio e
estado apresentados, sem adicionar obra. Somente o botão Aprovar deve iniciar
a inclusão. Conferir mensagem disponível com guardas satisfeitas; fila privada
e default devem retirar a disponibilidade. Em Manual/Automático, as mensagens
devem orientar a troca de modo antes de apresentar guardas operacionais.

Um cartão desatualizado oferece atualização; ela recalcula a lista e não
constrói. Um cartão pendente não deve tratar a troca de modo ou atualização
como aprovação de outra expansão. Abrir fila de construção deve abrir a janela
nativa sem modificar a fila. Esses testes visuais ainda não foram executados.


## Painel Automático 0.5.2 — roteiro futuro

Antes da primeira revisão, conferir agendamento e ausência de registro, sem
uma data inventada. Com filas ocupadas, o motivo atual deve aparecer mesmo
sem nova revisão. Após o evento, conferir mês/ano e resultado. Alterar a fila
e consultar o painel: motivo atual muda, resultado datado anterior permanece.
Trocar modo e atualizar diagnóstico não devem apagar esse resultado nem
executar uma obra. Desativar limpa o arquivo. Passagem de tempo/save-reload
continuam pendentes de teste na engine; não foram simulados como aprovados.


## Limite mensal de tentativas 0.5.3 — roteiro futuro

Em cópia, registrar uma tentativa automática e verificar a mensagem de limite.
Cancelar a obra de teste, se apropriado, e manter o mês: outra revisão não deve
adicionar uma expansão. Trocar modo e desativar/reativar não devem reiniciar o
limite. Assistido deve continuar sujeito às guardas de aprovação e pode operar
por clique explícito. No mês seguinte, sem depender de refresh manual, a guarda
mensal deve liberar avaliação de outro candidato. Conferir save/reload com a
marca presente; esse caminho não foi verificado na engine. Inclusão recusada
também consome o mês; revisão sem candidato não consome. Não presumir uma
história de tentativas anterior à instalação da 0.5.3.

## Casos pendentes — infraestrutura 0.5.4

Em cópia de save: comparar saldo do cartão com interface nativa; gerar cartão
de produtor/setor com saldo não negativo, criar déficit antes de aprovar e
confirmar bloqueio sem inclusão. Atualizar deve remover candidato e contar
o motivo. Saldo exatamente zero permanece permitido; isso não garante margem
para o próximo nível. Verificar ferrovia em déficit e seleção automática de
outro produtor em estado elegível. Estes casos ainda não foram executados
na engine nesta revisão.
