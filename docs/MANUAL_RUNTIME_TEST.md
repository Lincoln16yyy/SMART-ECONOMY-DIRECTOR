# Plano de teste da campanha — interface 0.5.3

## Evidência parcial recebida em 10/11/2026

Capturas da campanha de março–maio de 1842 mostram escassez de ferro, dois
estados produtores rejeitados por fila e ocupação, expansão de mina em Sinai
na fila, plano em acompanhamento e retorno a crescimento/diversificação após
fim do aviso de escassez. A autoria da obra e sua conclusão não foram
identificadas diretamente. O caminho direto coordenado permanece pendente.
Leitura manual corrigiu snapshot fiscal desatualizado. O controle por reservas
continuava ativo com déficit e fila pública, motivando a pausa da 0.6.16.


## Teste conjunto da 0.6.20

Realizar quando o jogador decidir retomar os testes. Registrar uma captura
inicial do orçamento, opções dos construtores e fila, e guardar um save.

1. País com superávit e reservas, Automático por seis a doze meses. Registrar
   objetivo, executor e última revisão. Comparar projetos novos e seus estados.
2. Se o objetivo for tributação, observar junho/dezembro. Se for capacidade de
   construção, fevereiro/agosto. Uma revisão do Director pode anteceder a
   execução da ferramenta externa.
3. Na política do Supply Chain, conferir estados incorporados, meta antecipada
   de instituições suspensa e limite numérico em um nível. Esses limites são
   por local da rotina externa, sem teto nacional de uma obra.
4. Em país deficitário, conferir ausência de novas autorizações externas e o
   registro fiscal. Comparar mês e níveis solicitados com impostos e salários
   no orçamento. Atualizar várias vezes no mesmo mês e verificar estabilidade.
5. Salvar/recarregar no Automático. Conferir continuidade da revisão, política e
   ausência de redefinição dos snapshots originais.
6. Voltar ao Assistido, depois testar desativar. Comparar as opções dos outros
   mods e níveis fiscais com a captura inicial. As opções originais podem
   reativar construtores que o jogador mantinha ligados antes da coordenação.

7. Com escassez ou falta de infraestrutura e expansão correspondente na fila,
   observar acompanhamento de obra quando não há outra prioridade elegível.
   Confirmar suspensão das opções externas e reavaliação após conclusão ou
   cancelamento. Uma obra em outro estado sem o gargalo não comprova resolução.

8. Comparar despesas militares do orçamento com a seção econômico-militar.
   Conferir a indicação de paz/guerra e avisos dos cinco bens no mercado.
   Em país com dívida ou reservas insuficientes, a diretriz não deve dizer que
   há condições para estudar modernização. Escassez militar deve manter o
   aviso de abastecimento mesmo se a diretriz geral for estabilizar finanças.

9. Se houver escassez de armas, artilharia ou munição e produtor existente,
   conferir o cartão, estado, ocupação e insumos. Em Assistido, aprovar uma
   expansão e conferir um nível na fila. Sem candidata, registrar o motivo.
   No Automático coordenado, oferta com primeira prioridade viável deve
   selecionar Director. Outras rotas ainda usam os filtros do executor externo.

10. Teste principal da 0.6.15. Com país solvente, filas livres e um produtor
    elegível para bem em escassez, fotografar a primeira prioridade e o executor.
    No Automático, aguardar a próxima revisão. Confirmar executor Director,
    opções verificadas dos outros construtores suspensas e um nível do prédio
    no estado da primeira prioridade na fila. Fotografar resultado da revisão.
    Repetir no mesmo mês para conferir ausência de uma segunda tentativa.
    Voltar ao Assistido e comparar as opções restauradas com a captura inicial.

11. Com déficit, reservas e obra pública na fila, atualizar o diagnóstico.
    Conferir seleção de espera por reservas e opções externas suspensas.
    Comparar piso, ouro disponível acima do piso e semanas de cobertura com
    orçamento. Após esvaziar a fila, atualizar e conferir nova seleção, sem
    inclusão de obra pelo clique. A última revisão automática deve conservar
    sua data e resultado anteriores até a revisão efetiva.

12. Conferir o orçamento direto mostrado no plano. Comparar os métodos, níveis e ocupação dos
    setores ativos, os pontos potenciais e o teto material com a referência
    semanal. Conferir se um setor pequeno limita a referência, mesmo com
    capacidade nacional gratuita maior. Quando o
    orçamento não cobrir a referência, a revisão deve registrar bloqueio de
    materiais sem consumir tentativa. Com cobertura, filas livres e candidata
    viável, confirmar inclusão. Registrar casos em que a referência parece
    excessiva para calibrar o modelo. Métodos desconhecidos devem manter o
    aviso específico. Aprovação Assistida continua exigindo decisão do jogador.

13. Quando houver uma rodada significativa de teste, conferir os cartões e
    o novo motivo de rejeição por reserva estimada de trabalhadores. Comparar
    com desempregados/camponeses e obras do estado. Registrar exemplos de
    bloqueio excessivo, especialmente onde migração ou mudança de emprego
    permitiriam expansão. A referência não prevê qualificações. Conferir se
    liberar uma obra ou vagas altera a reserva na leitura seguinte.

14. Na próxima rodada significativa, conferir as referências de insumos nos
    cartões. Comparar PMs ativos, demanda adicional e margem ao limiar de
    escassez com o mercado. Testar um caso de nova demanda sem cobertura e um
    com cobertura. Conferir energia/transporte no estado específico e uma
    mudança de PM antes da aprovação. Registrar bloqueios excessivos. A
    projeção mantém a oferta atual, sem antecipar produção das obras da fila.

Guardar capturas de um caso saudável, um caso de crise e a restauração. Obras
existentes e investimentos privados não comprovam autoria do Director.


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

## Opções independentes do Supply Chain — 0.5.5 (pendente)

Em cópia dedicada, desligar cadeias e habilitar separadamente ferrovias,
energia e setores. Cada opção deve mostrar bloqueio atual no Automático e
registrar resultado de concorrência sem tentativa do Director. Desligar a
opção deve liberar a guarda, sujeito aos outros bloqueios. Registrar todas
as opções; não inferir inclusão ou reconciliação pelo total agregado da fila.
Este roteiro não foi executado e não solicita teste imediato ao jogador.

## Administração do Supply Chain — 0.5.6 (pendente)

Na mesma cópia de teste, verificar separadamente configuração geral e
tributária: ambas devem bloquear o Automático e registrar concorrência, sem
consumir tentativa mensal. Remover a configuração geral deixando apenas a meta
institucional deve liberar essa guarda; outros bloqueios continuam aplicáveis.
Não executado nesta etapa; sem solicitação de teste imediato ao jogador.

## Revalidação 0.5.7 (pendente)

Em cópia dedicada, confirmar que revisões automáticas bloqueadas por fila,
pausa ou configuração concorrente não incluem obra e não consomem o mês.
Confirmar que a aprovação Assistida mantém suas regras. Não executado nesta
etapa; nenhuma solicitação de teste imediato ao jogador.

## Autorização de modo 0.5.8 (pendente)

Em cópia dedicada, confirmar que trocar para Manual após exibir recomendação
não permite aprová-la nem executar evento automático pendente. Voltar para
Assistido deve permitir aprovação somente quando as guardas atuais passarem.
Testes sintéticos de chamadas diretas não substituem essa verificação de engine.
Não executado nesta etapa; sem solicitação imediata ao jogador.

## Lista externa 0.5.9 (pendente, ainda não instalada)

Quando houver instalação posterior com o jogo fechado, conferir a lista no
Automático com cada opção do Supply Chain e depois todas juntas; manter uma
fila ocupada para confirmar que a lista não some por prioridade do bloqueio.
Remover opções deve retirar suas linhas. Manual/Assistido/desativado ocultam
a lista. Verificar altura natural, legibilidade e ausência de cortes.
Não altera o teste em andamento da 0.5.8.

## Coordenação e plano 0.6.0

Usar cópia dedicada com opções e versões dos executores registradas. A anotação
de teste deve separar alteração de opção, execução externa e inclusão na fila.

1. Registrar presença e valores das sete opções descritas em PLANNING.md.
   Abrir o Director, atualizar diagnóstico e conferir data, situação fiscal,
   objetivo e até três prioridades. Conferir o painel com o país da campanha.
2. Selecionar Automático. Conferir executor escolhido e quais opções externas
   ficaram ligadas. Comparar PMs e outras opções com o registro inicial.
3. Conferir o caso de infraestrutura, depois burocracia, tributos e energia
   quando ocorrerem no save. Registrar o motivo e a ferramenta selecionada.
   Nenhuma alteração de campanha para fabricar candidatos foi realizada nesta entrega.
4. Avançar pela agenda normal da ferramenta e registrar a eventual inclusão de
   obra, alvo e quantidade. Status de orientação aplicada deve permanecer
   distinguível de sucesso de inclusão.
5. Conferir bloqueio fiscal em save apropriado. A suspensão limita autorizações
   futuras. Obras já existentes continuam na fila.
6. Alternar para Assistido ou Manual e comparar presença e valor das sete
   opções com o registro original. Repetir a seleção de Automático para conferir
   que o snapshot inicial de cada sessão permanece consistente.
7. Salvar e recarregar a cópia com coordenação ativa. Conferir o executor,
   snapshot, fila e restauração ao liberar ou desativar.
8. Registrar cortes, chaves cruas, erros de script e discrepâncias. Ainda faltam
   resultados desses casos na engine da 0.6.0.

No upgrade de 0.5.x, selecionar Automático novamente aplica a tomada de controle
pelos adaptadores. O modo salvo por si só preserva a escolha anterior até essa
seleção. Remover o mod exige restaurar opções antes de desabilitar seus arquivos.

## Objetivo e orçamento do Advisor 0.6.1

Registrar as quatro opções de objetivo/orçamento antes de escolher Automático.
Conferir o objetivo escolhido no Director e no Advisor nos cenários de
crescimento, bens essenciais e dívida entre 50% e 75% do crédito. Conferir
restauração ao sair e depois de salvar/recarregar. Em save 0.6.0 com coordenação
ativa, registrar a captura no primeiro uso do Advisor. A política social e a
financeira precisam ser comparadas à seleção real de candidatos do Advisor.
Os casos permanecem pendentes na engine.

## Conferência curta 0.6.9

Abrir o Director em cópia de save e selecionar Automático. Registrar uma
captura do modo, executor, situação fiscal e última revisão. Avançar até a
revisão do mês seguinte e registrar a mesma área, junto dos níveis de imposto
e salário civil no orçamento. Repetir Atualizar diagnóstico no mesmo mês
permite conferir que a idade das metas permanece estável. Ao voltar para
Assistido, conferir a restauração dos níveis originais.

O teste de inicialização já chegou ao menu com as rotinas carregadas. A
conferência acima verifica o comportamento em campanha e permanece pendente.

## Retorno com salários 0.7.17–0.7.19 (pendente)

Objetivo: confirmar na engine a unidade salarial observada, o retorno que
desconta folha e a pontuação de PMs. Guardar uma cópia do save antes de cada
passo e registrar data, país e estado.

1. Abrir o painel do Director com o mod ativo e o Automático ligado. Localizar
   a linha "Unidade salarial observada" acima da política do plano. Se não
   houver prédio saudável, deve aparecer a linha de ausência de amostra.
2. Escolher um produtor de madeira saudável (ocupação de ao menos 80%, sem
   escassez, sem contratação falha, não subsidiado). Anotar `earnings` e
   `weekly_profit` no painel do prédio. A unidade esperada é
   `(earnings − weekly_profit) ÷ (pesos de emprego × nível × ocupação)`.
   Comparar com o número mostrado no Director.
3. Repetir com um prédio subsidiado ou com escassez de insumos: a unidade não
   deve mudar por causa dele.
4. Avançar um mês sem alterar prédios: a unidade deve ficar estável. Subsidiar
   um prédio que estava na amostra e avançar um mês: a unidade deve mudar na
   revisão seguinte.
5. Oferta: numa escassez com margem material pequena, comparar o fornecedor
   escolhido antes e depois de a unidade salarial subir. Registrar a unidade,
   a margem e o cartão da prioridade. Mudança de fornecedor aqui é o sinal que
   a 0.7.17 tenta produzir.
6. PMs: com prédio elegível (ocupação ≥ 90%, sem escassez, insumo e tecnologia
   ok), observar a modernização. Se a troca aumenta emprego ponderado e a
   folha estimada zera a pontuação, a revisão deve registrar método mantido.
   Anotar o método antes e depois e a mensagem da revisão.
7. Salvar e recarregar no Automático: a unidade deve ser recalculada na próxima
   revisão. Conferir `logs/error.log` sem erro novo citando `sed_`.
8. Desativar o Director: as duas linhas novas somem do painel e as variáveis
   `sed_investment_wage_*` não devem sobrar (conferir no save, se possível).
9. Devolver: trecho do `logs/error.log`, captura do painel nas duas revisões,
   captura do cartão da prioridade, método antes/depois e o save.

Limites conhecidos: a unidade é média por emprego ponderado, não salário por
profissão; `earnings` semanal está documentado apenas pela localização vanilla;
o painel mostra a média nacional, não a leitura por estado. Divergência grande
deve ser registrada para calibragem, não ajustada sem evidência.

## Leis delegadas 0.7.20 (pendente)

Com o Smart Government Advisor ativo e o Director no Automático, abrir o painel
do Director e conferir a linha "Smart Government Advisor detectado". Sem o
outro mod, deve aparecer apenas a linha de escopo das leis. Clicar "Atualizar
diagnóstico" e avançar um mês não pode alterar leis, nem criar diário duplicado.
Devolver captura do painel com e sem o mod e o trecho do `logs/error.log`.

## Evento de importação 0.7.21–0.7.22 (pendente)

Com o Director ativo e uma escassez real sem expansão local possível (por
exemplo, nenhum produtor do bem com insumos, trabalho e fila liberados):

1. Avançar um mês. Deve aparecer um evento com ícone industrial, prazo de
   leitura e três opções: "Vou abrir a rota de importação", "Recalcular o plano
   agora" e "Só me avise em 2 anos". Conferir que a descrição cita o bem certo
   e que os pedidos de compra e venda aparecem como números (desde a 0.7.22),
   batendo com a aba de mercado do bem no mesmo mês; se aparecer texto cru do
   tipo `GetValue` ou a chave da variável, o formato de loc do evento está
   errado — reportar.
2. Escolher "Vou abrir a rota de importação": o mesmo evento não pode reaparecer
   nos 12 meses seguintes. Abrir a rota é ação sua na interface de comércio; o
   Director não deve criar rota, nem registrar erro no `logs/error.log`.
3. Sem responder, deixar expirar: o evento deve resolver sozinho na opção
   padrão (recalcular o plano) e não alterar impostos, salários ou obras.
4. Clicar "Só me avise em 2 anos" e avançar 24 meses: o aviso pode voltar se a
   escassez continuar.
5. Desativar o Director: nenhum aviso novo deve aparecer, e as variáveis
   `sed_import_notice_*` não devem sobrar na próxima leitura.
6. Devolver captura do evento, o texto do `logs/error.log` e o save.

Limites conhecidos: o prazo do evento em meses e a escolha automática ao
expirar seguem NÃO VERIFICADO; as três opções são inofensivas por desenho.

## Duração real da fila 0.7.23 (pendente)

1. Com o Director ativo e alguma obra pública na fila, abrir o painel e ler a
   linha do orçamento direto: deve aparecer "a engine mede até N semanas
   restantes na fila do governo", ao lado da referência do plano.
2. Comparar N com a barra de obras do jogo (tempo restante da fila do governo).
   A leitura é arredondada **para cima** na faixa seguinte (2, 4, 6, 8, 12, 16,
   20, 26, 32, 40, 52, 78, 104, 156, 208 ou 260), então N pode ser maior que o
   valor exato da barra, nunca menor.
3. Pausar/cancelar todas as obras públicas e atualizar o diagnóstico: N deve
   voltar a 0, e nenhuma obra deve ser enfileirada por causa disso.
4. Conferir que a reserva de ouro exigida não mudou de fórmula — ela continua
   baseada na referência do plano, não na leitura da engine.
5. Devolver captura do painel, o `logs/error.log` e o save.

## Meta plurianual 0.7.25 (pendente)

1. Provocar escassez de um bem por três meses consecutivos e conferir a linha
   "Meta industrial anual" no painel.
2. Avançar para o ano seguinte e repetir a escassez por três meses: a linha da
   meta deve continuar visível em janeiro (sem esperar os três meses) enquanto a
   falta persistir, e o bem deve manter prioridade no plano.
3. Deixar a escassez sumir e passar um ano inteiro sem meta para o bem: ao
   reaparecer, a meta deve voltar como primeira ocorrência (sem bônus
   plurianual).
4. Desativar o Director e conferir que `sed_<bem>_goal_streak`, `meta_since` e
   `meta_year` não sobram.

## Unidade salarial por família 0.7.26 (pendente)

1. Com o Director ativo, abrir o painel e conferir a linha "Unidade salarial
   observada".
2. Comparar a escolha de fornecedor de um bem com duas opções de prédio (ex.:
   cereais em fazenda de trigo vs. arroz) com e sem prédios saudáveis de cada
   família: quando existir amostra da família, o retorno dela deve usar essa
   amostra, não a média nacional.
3. Conferir que prédios subsidiados, com escassez de insumos, contratações
   falhas ou ocupação abaixo de 80% continuam fora da amostra.
4. Desativar o Director e verificar que as variáveis `sed_investment_wage_*_
   <prédio>` não sobram.

## Controle de construção privada 0.7.27 (pendente)

Pré-requisito: Controllable Private Construction ativo e o Director ligado.
Anote a versão dos dois mods. Save de teste antes de mexer nos botões.

1. Abra o diário *Private Constructions Management* do outro mod e confira quais
   botões estão ligados. Abra o painel do Director: a seção
   *Controle de construção privada detectado* deve listar exatamente as mesmas
   restrições, uma linha por botão ligado.
2. Ligue um botão novo no diário do outro mod e atualize o Director. A linha
   correspondente deve aparecer; desligue e ela deve sumir. Esperado: leitura,
   sem nenhuma mensagem de erro no `logs/error.log`.
3. Desative o Controllable Private Construction (jogo fechado, mudar o playset)
   e carregue o save. A seção deve sumir por completo e o Director deve
   continuar funcionando; nenhuma variável `zw_var_*` deve aparecer no save.
4. Com a fila privada ocupada e o Automático ativo, confira o aviso
   *A fila privada ocupada conta para os guardas do Director mesmo com o
   controle ativo*. Ele deve apontar o diário do outro mod, sem botão novo.
5. Se a intervenção no investimento estrangeiro estiver ligada, tente aprovar
   uma obra pública que o Director pediria e registre se a recusa aparece como
   falha de ação. Devolver: trecho do `error.log`, captura da seção antes/depois
   de ligar o botão e o save se a recusa ocorrer.

## Cessão de PM ao Auto-Apply PMs 0.7.28 (pendente)

Pré-requisito: Auto-Apply PMs ativo, Director em Automático, país com escassez
de um bem do catálogo (ex.: madeira) e um prédio operante do tipo.

1. No diário do Auto-Apply PMs, ligue o botão do prédio (ex.: serraria). No
   painel do Director deve aparecer a linha *Auto-Apply PMs detectado*.
2. Avance um mês. Esperado: o Director não troca o método principal daquele
   prédio; o `sed_pm_upgrade_status` não deve indicar modernização confirmada.
   Confira que o outro mod aplicou a mudança dele (ou nenhuma).
3. Desligue o botão do Auto-Apply PMs e avance um mês. Esperado: o Director
   volta a modernizar aquele tipo e a linha do painel some.
4. Repita com o botão de grupo de fazendas ligado e uma fazenda de trigo: a
   linha deve aparecer, e a cessão deve valer para trigo, centeio, arroz, milho e
   milhete. Devolver: captura do painel nos dois estados e trecho do
   `error.log`.

## Evento de importação 0.7.29 (pendente)

1. Com escassez de papel e sem candidata local, avance o mês até o evento
   `sed_pulse` de papel aparecer. A descrição deve listar os quatro passos
   (Centro de Comércio, tarifa/subvenção, Transferência de Bens, Isolacionismo)
   com parágrafos separados.
2. Confira o botão de opção: "Vou tentar importar pelo Mercado Mundial"; ao
   clicar, o aviso de papel não deve voltar por 12 meses.
3. Troque o jogo para inglês e confirme que o texto está em inglês (antes da
   0.7.29 o arquivo inglês saía em português).

## Administração pública 0.7.31 (pendente)

1. Save de teste **sem** Economy Advisor e **sem** Supply Chain ativos, com
   burocracia nacional negativa (objetivo 6) e um estado incorporado com
   infraestrutura ≥ 0. Automático por um mês. Esperado: um nível de
   `building_government_administration` na fila do governo, seção
   "Administração pública" no painel com o pedido enfileirado. Devolver:
   captura do painel e da fila.
2. Burocracia ≥ 0 e um estado com `tax_capacity_usage > tax_capacity`
   (objetivo 7): a obra deve ir para esse estado, não para o mais populoso.
3. Com o prédio já tendo um nível na fila, avance um mês: nada novo deve ser
   enfileirado (espera a fila andar).
4. Com fila privada ocupada, avance um mês: status 11 e nenhuma obra; a segunda
   revisão deve ocorrer 7 dias depois, se a fila privada esvaziar.
5. Confira que o custo na fila corresponde a 100 pontos por nível e que a
   reserva de orçamento do painel cobre esse projeto.
6. Salve e recarregue no Automático: o pedido pendente deve continuar
   reconhecido e, ao concluir, `sed_admin_completed` deve subir.
7. Com Supply Chain ativo, confirme que o caminho externo (opção
   `zw_var_scsab_gov_admin`) continua sendo o usado e que o Director não
   enfileira obra própria em paralelo.

## Centro de Comércio 0.7.30 (pendente)

1. Save de teste com um bem do catálogo em escassez real e **sem produtor** no
   país (ex.: papel sem fábrica de papel), estado incorporado com infraestrutura
   ≥ 0 e que aceite a obra. Automático por um mês. Esperado: um nível de
   `building_trade_center` na fila do governo, linha "Centro de Comércio" no
   painel com o pedido enfileirado. Devolver: captura do painel e da fila.
2. Confirme que o nível aparece no prédio existente quando já há um Centro de
   Comércio no estado (caso de expansão), e que nada é enfileirado de novo no
   mês seguinte enquanto a obra está na fila.
3. Com um produtor do bem presente mas parado por falta de trabalhadores, o
   Director deve esperar (status 2) e **não** comprar capacidade.
4. Ligue Isolacionismo (`law_isolationism`) e repita o passo 1: nada deve ser
   enfileirado e a linha do painel não deve aparecer.
5. Estado com `infrastructure_delta` negativo: nenhuma obra ali; com outro
   estado saudável, a obra deve ir para o estado saudável.
6. Salve e recarregue no Automático: o pedido pendente deve continuar
   reconhecido e, ao concluir a obra, o contador `sed_trade_center_completed`
   deve subir (inferência por nível, como na ferrovia).
