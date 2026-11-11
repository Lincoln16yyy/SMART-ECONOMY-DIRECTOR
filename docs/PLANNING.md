# Planejamento e coordenação — 0.6.8




## 0.7.6 — Compromissos da fila e retomada por reservas

O orçamento direto soma a construção de níveis pendentes nos tipos vanilla
verificados em `data/queued_building_costs.json`, incluindo fundações próprias
que ainda não têm prédio. A fila pública agregada limita a soma. Níveis sem
correspondência usam 6000 pontos, o maior custo vanilla verificado. A janela
estimada soma fila/capacidade nacional, duração do novo projeto e quatro
semanas, com piso de 26 semanas. O teto anterior de 56 semanas foi removido.

A referência semanal considera os pontos que os projetos públicos existentes
mais o novo podem consumir em paralelo, limitada pela capacidade nacional e
pelo material dos setores ocupados. A guarda de reservas usa essa referência
durante a janela estimada. O executor direto pode operar com déficit semanal
se o saldo operacional é não negativo, não há dívida e as duas guardas de
reservas e materiais são satisfeitas. Com coordenação, a prioridade própria
é avaliada antes da espera genérica por fila pública financiada por reservas.
Os caminhos específicos do Supply Chain mantêm suas guardas anteriores.

Os pontos da fila incluem o custo integral dos níveis pendentes e ignoram o
progresso já feito. Leituras por prédio podem incluir outro investidor e não
identificam projetos estrangeiros do país. O fallback cobre a falta de
correspondência na contagem agregada. Custos modificados por outros mods,
eficiência local, ordem exata, autoria e despesas operacionais futuras
continuam sem previsão precisa. A cobertura é uma referência de estresse.

## 0.7.5 — Despesa militar durante recuperação fiscal

O Automático passa a reduzir salários militares em crise/default com saldo
operacional negativo e despesas militares positivas. Cada mês permite um passo,
com piso baixo. Guerra, jogada diplomática ou formação mobilizada impedem o
corte. Déficit apenas de construção preserva essa despesa.

O primeiro corte captura o nível original. Com prontidão militar exigida,
a revisão pode recuperar um passo até médio, limitado ao original, mesmo
em crise. Acima de médio, ou na paz, a recuperação exige superávit,
saldo operacional não negativo, ausência de dívida, doze semanas de despesas
fixas em reservas e saldo de pelo menos metade da despesa militar observada.
Essa margem é um parâmetro conservador inicial, sem previsão exata do novo
salário. O limite mensal também vale para a recuperação de prontidão.

Sair do Automático ou desativar restaura o nível capturado. O marcador mensal
persiste para impedir cortes repetidos por troca de modo. Saves anteriores
sem snapshot capturam o nível no primeiro corte efetivo. A atualização de
diagnóstico continua sem executar políticas.

Fontes locais verificadas incluem o efeito `set_military_wage_level` e sua
assinatura no executável 1.15, a localização `SET_MILITARY_WAGE_LEVEL`, o
trigger `has_diplomatic_play` do executável e `any_military_formation` com
`is_mobilized` nos objetivos tutoriais vanilla. Aceitação e resultados em
campanha continuam pendentes. Recrutamento e modernização permanecem pendentes.

## 0.7.4 — Planejamento de insumos em vários elos

O Automático recalcula as prioridades a partir da escassez atual e propaga a
necessidade pelos fornecedores intermediários. Expansões e fundações podem
participar da cadeia. A propagação para quando encontra um fornecedor elegível
ou uma obra relacionada já enfileirada. Uma alternativa elegível em outro
estado evita priorizar os insumos de um produtor bloqueado.

Cada leitura limpa as prioridades anteriores. A propagação tem no máximo uma
passagem por bem de insumo suportado, encerrando antes quando nada muda. Isso
cobre os caminhos simples do catálogo e termina em dependências circulares.
O livro de fundações próprias passa a contar também na identificação de oferta
enfileirada, mesmo antes de existir prédio.

A execução continua limitada a uma tentativa por mês e ao catálogo atual.
Bens fora do catálogo, comércio, escolha de PMs e ciclos sem fornecedor viável
continuam pendentes. Nenhuma produção futura é creditada como oferta atual.
O plano volta a avaliar o gargalo após a mudança real da oferta.

## 0.7.2 — Duração e materiais do primeiro projeto

O orçamento direto continuava usando uma janela fixa de 26 semanas de déficit
para a reserva exigida e não estimava o tamanho do projeto escolhido. A 0.7.2
identifica a primeira prioridade do plano e lê a construção exigida por nível
na base vanilla: 200 pontos para fazendas, madeira e tecido; 400 para ferro e
carvão; 600 para ferramentas, alimentos, roupas e indústria bélica; 800 para
ferrovia, aço e munição; 25 para o setor de construção.

Com a capacidade semanal (`country_construction_add`, limitada pelo progresso
máximo), o painel mostra pontos, semanas estimadas e materiais de referência do
projeto inteiro. A reserva exigida passa a usar a maior janela entre 26 e a
duração do projeto mais quatro semanas, limitada a 56 semanas. Projetos curtos
mantêm o piso anterior; ferrovias e munição, que duram mais, exigem mais ouro
sem bloquear obras de até um ano de déficit coberto. A estimativa assume o
maior custo entre métodos ativos e preços-base com 75% de estresse; fila
concorrente, salários, subsídios e modificadores ainda podem alongar o prazo.

247 testes sintéticos aprovados, incluindo o primeiro projeto de ferrovia com
800 pontos, 80 semanas e reserva de 56 semanas. Geração e validação estática
locais aprovadas. Sem engine ou campanha nesta etapa: a duração real depende da
fila e de efeitos que o script não observa.

## 0.7.1 — Primeira ferrovia e pedido de fundação persistente

Até a 0.7.0, ferrovia só entrava no plano quando já existia e estava operante.
Um estado com infraestrutura negativa e nenhuma ferrovia ficava apenas na
contagem "sem ferrovia" e nunca recebia obra. A 0.7.1 inclui o primeiro nível
como fundação: estado incorporado, déficit atual, sem `building_railway`, sem
pedido pendente e com `can_construct_building` aceito. O candidato mantém o
ranking por déficit, a aprovação (também no Assistido) e o livro de ferrovias;
a intenção registra nível 0 e a conclusão é inferida quando o prédio aparece.

A mesma entrega corrige a persistência da fundação. Sem prédio, a limpeza de
pendências tratava o pedido como abandonado na leitura seguinte, antes de a
obra concluir; isso liberava o gatilho e permitia fundar de novo. Agora o
pedido de fundação, de ferrovia ou de indústria, permanece pendente enquanto
houver níveis na fila pública e nenhum prédio; a pendência só é encerrada
quando o prédio aparece (conclusão) ou a fila esvazia (abandono).

246 testes sintéticos aprovados, incluindo fundação automática de ferrovia e
persistência do pedido após uma leitura intermediária. Geração e validação
estática locais aprovadas. Sem engine ou campanha nesta etapa: terra,
permissão e concorrência reais continuam pendentes de confirmação.

## 0.7.0 — Fundação da indústria ausente

Até a 0.6.26, um bem em escassez sem produtor no país entrava apenas no
objetivo 5: o Director registrava a ausência, mas a construção direta exigia
um produtor existente para expandir. A 0.7.0 fecha essa lacuna. Quando há
escassez de mercado, nenhum estado do país tem um dos produtores do bem e ao
menos um estado incorporado aceita `can_construct_building` para alguma
variante, esse estado entra no ranking normal como qualquer alvo de oferta.
O dirigente automático escolhe a primeira prioridade, e a aprovação enfileira
um nível do prédio novo com nível inicial 0.

A fundação não cria um caminho paralelo: usa o mesmo candidato, o mesmo plano
de até três prioridades, a mesma aprovação (também disponível no Assistido)
e as mesmas guardas fiscais, de materiais, de fila privada, de pausa e o
limite de uma tentativa por mês. Não inicia obra em estado que já tem a
variante; nesse caso a expansão normal continua valendo. Enquanto a fundação
está na fila ainda não há prédio no país, então o gatilho exige que nenhum
estado tenha pedido pendente daquele bem: só se funda uma base por país, e
revisões seguintes não duplicam a indústria em outro estado. O livro de resultados
passa a contar a fundação como pedido e infere a conclusão quando o nível sai
de 0 ao deixar a fila.

Quando nenhum estado pode hospedar o prédio, o objetivo 5 permanece e a
interface diz que o Director aguarda tecnologia, terra ou infraestrutura; a
construção não é forçada e a importação continua fora do escopo.

244 testes sintéticos aprovados à época, incluindo fundação automática,
ausência de estado apto, fundação única por país enquanto a obra está na fila e
as regressões anteriores. Geração e validação
estática locais aprovadas. Sem engine ou campanha nesta etapa: custo real,
terra disponível e comportamento de `can_construct_building` no jogo ainda
precisam de confirmação.

## 0.6.26 — Setor de construção e segunda revisão no Automático

O Automático passou a tratar o setor de construção como alvo do dispatcher,
como ferrovia e os onze bens. O setor só entra quando o plano o coloca em
primeiro lugar, o que exige ao menos três projetos públicos e um setor com
ocupação de 90%, sem falha de contratação, falta de insumos ou expansão já
enfileirada. As guardas fiscais, a referência de materiais e o limite de uma
tentativa por mês continuam valendo; sem orçamento de materiais conhecido o
setor não é enfileirado. A aprovação manual e Assistida do setor não mudou.

Quando a revisão mensal termina bloqueada pela fila privada (11) ou pela
construção pausada (12), o Director agenda uma segunda revisão sete dias
depois. O marcador `sed_auto_retry_month` permite no máximo uma segunda
revisão por mês de calendário, mesmo que a primeira volte a ser bloqueada. A
tentativa só é consumida se houver inclusão. A segunda revisão usa o mesmo
dispatcher e as mesmas guardas.

241 testes sintéticos aprovados, incluindo setor ranqueado, setor fora do
primeiro lugar, fila pública ocupada, fila privada bloqueando e a segunda
revisão única por mês. Geração e validação estática locais aprovadas. Nada foi
observado na engine: agenda real do evento, concorrência e custo incremental
seguem sem confirmação de campanha.

## 0.6.25 — Execução automática com fila pública ocupada

A revisão mensal deixava de agir sempre que a fila pública tinha qualquer
projeto, mesmo sendo obras de outros construtores. Em campanha, isso mantinha
o Automático parado. A guarda do executor próprio passa a exigir apenas a fila
privada vazia; a fila pública pode estar ocupada e recebe no máximo um nível
por revisão.

Continuam iguais: limite de uma tentativa por mês, inadimplência, construção
pausada, construtores conhecidos, proteção fiscal, referência de materiais,
elegibilidade do prédio e `level_after_queued_constructions` por prédio. O
status 11 agora descreve somente a fila privada. Aprovações manuais e
Assistidas não mudaram; o setor de construção foi incorporado ao dispatcher
automático na 0.6.26.

238 testes sintéticos aprovados nesta etapa, incluindo fila pública ocupada
com inclusão confirmada, bloqueio da segunda tentativa no mesmo mês e fila
privada ainda bloqueando. Geração e validação estática locais aprovadas. Nada
foi observado na engine: fila longa, custo incremental e concorrência real
continuam sem confirmação de campanha.

## 0.6.21–0.6.24 — Fornecedores de maior saída e prioridade de insumos

O Automático escolhe, entre produtores alternativos do mesmo bem, o de maior
saída estimada pelo registro `data/supplier_output_profiles.json`. Bloqueios
por insumo são exibidos nos cartões e o plano pode priorizar o bem em falta
para uma expansão bloqueada quando não existe fornecedor imediato. A segunda
passagem só roda no Automático e não cria candidato por si.

## 0.6.20 — Previsão de insumos das expansões de oferta

A recomendação e a aprovação dos onze bens agora verificam a demanda adicional
pelos PMs ativos do produtor. O registro `data/input_profiles.json` contém
coeficientes verificados para 18 tipos de prédio e 124 entradas de métodos.
A demanda de um nível completo recebe margem inicial de 25%.

O modelo mantém a oferta atual e desconta vagas e expansões enfileiradas dos
tipos conhecidos. Bens de mercado usam oferta/demanda agregadas e compromissos
dos estados do país, incluindo não incorporados. Eletricidade e transporte
usam produção/consumo e compromissos do próprio estado. A previsão aguarda
quando a nova demanda levaria a oferta/demanda abaixo de 50%, conforme o limiar
verificado nos defines vanilla locais. Na igualdade, a candidata é permitida.

As margens são calculadas por leitura e armazenadas, evitando varredura
nacional por candidata. A aprovação recalcula antes de validar. Métodos ativos
são lidos ao vivo. Falta de dados do insumo produz margem zero. Insumo com
quantidade ativa zero não exige margem. Desativar remove snapshots. Os
cartões usam ScriptValue, padrão verificado nos widgets vanilla, para mostrar
referências e margens por insumo; há motivo próprio de rejeição por previsão.

A oferta de projetos futuros não é creditada. Mudanças futuras de preços,
comércio, emprego, PMs, produção e modificadores de throughput/consumo ainda
podem alterar o resultado. Tipos e métodos fora do registro e compromissos de
outros países permanecem fora da projeção adicional. O modelo é uma referência
que precisa de calibração. Construtores externos mantêm seus próprios filtros.

O exemplo de autoconsumo de carvão citado durante o desenvolvimento foi
corrigido após conferir os arquivos. Os perfis atuais da mina de carvão usam
outros insumos conforme o PM, sem crédito especial de produção no modelo.
Nenhuma exceção de carvão foi incluída no código.

231 testes sintéticos aprovados, com 14 regressões adicionais de coeficientes,
limiar, ausência de insumo, filas, vagas, energia local, revalidação, retomada,
limpeza e proteção do validador. Geração e validação estática local aprovadas.
Interface, desempenho e decisões novas ainda aguardam campanha. Manter a
preferência do jogador por testes agrupados após mudanças relevantes.


## 0.6.19 — Reserva estimada de mão de obra nas expansões de oferta

As candidatas dos onze bens agora exigem reserva estimada de trabalhadores
para um nível adicional do produtor escolhido. O filtro aplica-se à
recomendação, aprovação Assistida e execução direta automática. Rotas externas
mantêm seus próprios critérios. Ferrovia e setor de construção entram no
cálculo de compromissos, mas seus filtros de candidatura permanecem anteriores.

A reserva demográfica usa população, referência de participação no trabalho
(0,25 mais modificador estadual, limitada entre 0,05 e 1), desemprego e metade
da participação de camponeses. Taxas são limitadas ao intervalo 0–1. Essa
fórmula é uma aproximação; não representa contagem direta de trabalhadores.
Não inclui qualificações, migração futura ou atração de empregados de outros
setores. Por isso pode rejeitar investimentos que seriam viáveis por esses
mecanismos.

A reserva é reduzida pelos compromissos conhecidos dos 18 tipos de prédio
registrados. Inclui vagas estimadas dos níveis atuais e os níveis adicionais
na fila, usando ocupação atual e coeficiente por nível. O coeficiente é a soma
dos maiores empregos de cada grupo de PMs vanilla do tipo, desconsiderando
economias de automação. O registro `data/labor_requirements.json` foi extraído
dos edifícios, grupos e métodos locais. Outros tipos de prédio e alterações
de emprego por outros mods continuam fora desse registro.

Os valores são calculados ao vivo nos filtros e registrados por estado na
leitura do plano. Cartões mostram reserva e compromissos; o diagnóstico de
rejeição tem motivo específico e coeficientes por produtor. Cancelar obra ou
liberar vagas muda a avaliação na próxima leitura. Desativar limpa snapshots.

217 testes sintéticos aprovados, incluindo oito regressões de referência,
fronteira, vagas, filas, camponeses, revalidação, variantes e limpeza. O harness
compara script values numéricos no lado esquerdo das condições. Geração e
validação estática local aprovadas. Novas leituras e bloqueios ainda aguardam
calibração e observação em campanha, junto do roteiro acumulado.

O jogador pediu testes apenas após mudanças relevantes. Acumular validações
locais e evitar solicitar capturas para cada alteração pequena.


## 0.6.18 — Limite material dos setores existentes

A referência da 0.6.17 podia aplicar o método ativo mais caro a pontos nacionais
que incluem construção gratuita. A origem da parcela gratuita é escalada pelo
PIB nos modificadores vanilla; não foi adotada uma dedução fixa de pontos.

A referência agora é limitada à soma de materiais dos setores existentes,
com seus níveis e ocupação atuais, mantendo preços-base acrescidos de 75%.
Cada estado soma os insumos de seu método reconhecido. A soma é recalculada em
cada leitura. O orçamento usa o menor valor entre essa soma e a referência
por pontos do próximo projeto. O limite semanal por projeto e as guardas
financeiras continuam iguais. A distribuição privada não introduz nova regra,
pois o executor direto já exige as duas filas vazias antes de construir.

Exemplo sintético com capacidade nacional 10 e um setor de madeira nível 1,
ocupação integral. Referência por pontos anterior de 17.500/semana passa a ser
limitada pelos materiais do setor em 3.500/semana. A reserva exigida para saldo
100 e despesas fixas 50 passa de 452.600 para 88.600. Esses valores são do
cenário de teste, sem confirmação de despesa real na campanha do jogador.

A referência continua sendo um cenário de materiais. Pode superestimar,
inclusive a parcela gratuita e os métodos mistos, e pode divergir do custo
real por preços locais, modificadores, emprego futuro e duração. Salários e
subsídios futuros permanecem fora do cálculo. O teto por ocupação atual não é
uma garantia contra crescimento futuro do consumo dos setores.

209 testes aprovados. Quatro regressões adicionais cobrem setor pequeno,
níveis/ocupação, soma entre estados e atualização, além do teto por projeto.
O harness suporta o iterador numérico de estados usado por scripts vanilla.
Geração e validação estática local aprovadas. Novos valores e comportamento
precisam de calibração em campanha.


## 0.6.17 — Referência de materiais para a execução direta

A proteção direta agora inclui referência conservadora de materiais para o
próximo projeto. Os quatro métodos de `13_construction.txt`, seus insumos,
pontos de construção e nove preços-base foram conferidos na instalação local.
O módulo `construction_budget.py` calcula materiais por ponto com preços-base
acrescidos de 75%, usando o maior custo entre métodos ativos dos setores.
O número de pontos é limitado pela capacidade nacional e pelo limite semanal
por projeto fornecido pelo jogo. Setor ativo com método desconhecido torna a
referência indisponível. Ausência de setores resulta em referência material
zero para a capacidade restante, sujeita às demais guardas.

A obra automática precisa de saldo cobrindo a referência semanal ou, sem
dívida, ouro cobrindo quatro semanas de despesas fixas mais 26 semanas da
diferença entre referência e saldo. As guardas fiscais anteriores continuam
obrigatórias. O cálculo é atualizado no plano, no executor direto e antes de
cada aprovação automática. Bloqueio de orçamento registra resultado 22 e
não consome tentativa. Assistido mantém aprovação explícita.

Esse cálculo é uma referência de estresse e pode superestimar o gasto. Ele
cobra todos os pontos potenciais pelo método ativo mais caro, inclusive quando
há capacidade gratuita ou métodos mistos. Não prevê duração, salários futuros,
subsídios, preços locais, modificadores de custo ou custos operacionais do
prédio concluído. Expansão de setores de construção ainda precisa de um modelo
separado de seu custo recorrente. Rotas externas continuam com seus orçamentos.

205 testes sintéticos aprovados. Nove regressões cobrem os perfis, capacidade,
limites de renda/reservas, dívida, método desconhecido, revalidação e limpeza.
A validação adversarial também verifica remoção da guarda de orçamento e da
atualização antes da execução. Geração e validação estática local aprovadas.
Referência e bloqueios precisam de calibração e observação em campanha.


## 0.6.16 — Ritmo de investimento por reservas e sincronização

O teste do jogador em março–maio de 1842 mostrou diagnóstico de ferro,
rejeição por expansão na fila e ocupação, acompanhamento de obra relacionada,
fim do aviso de escassez e retorno do objetivo para crescimento/diversificação.
A execução direta e a autoria da expansão ainda não foram comprovadas.
A leitura manual corrigiu uma divergência entre números registrados e a barra
atual do jogo. Leituras continuam representando snapshots.

Foi corrigida a sincronização após `sed_refresh_diagnostics`. O diagnóstico
atualiza o plano e, em coordenação ativa, reaplica a seleção de executor e as
opções autorizadas. Não enfileira obra, ajusta impostos/salários ou reescreve o
resultado arquivado da última revisão automática. Essa mudança pode alterar
as opções de construção externas durante o clique de diagnóstico.

Durante déficit financiado por reservas, níveis públicos já enfileirados
selecionam executor 12 e resultado 21. Novas opções externas ficam suspensas
nas revisões até a fila pública liberar. A fila privada sozinha não impõe essa
pausa. Com saldo não negativo, as rotas anteriores permanecem. O orçamento é
revalidado antes de liberar o Advisor; guardas de default e ARoAI prevalecem.
Obras existentes continuam; o mod não estima seu custo restante.

O painel mostra piso de doze semanas de despesas fixas, ouro acima desse piso,
cobertura em semanas do déficit atual e total exigido pela guarda de 26
semanas. Esses números explicam o limiar já existente, sem alterar seus fatores
ou prever custos incrementais. Casos de saldo zero e despesas negativas são
tratados para evitar divisão por zero e reservas mínimas negativas.

196 testes sintéticos aprovados. Sete regressões adicionais cobrem fila pública,
retomada, fila privada, sincronização sem execução/histórico alterado e contas
de reservas. Geração e validação estática local aprovadas. Novas transições e
layout ainda aguardam campanha.


## 0.6.15 — Execução direta da prioridade de oferta na coordenação

A coordenação agora escolhe o Director (executor 11) quando o objetivo de
oferta tem uma primeira prioridade elegível e passa pela guarda fiscal
normal. As sete opções verificadas de construção externa são suspensas antes
da execução. Infraestrutura e demais objetivos mantêm as rotas anteriores;
a delegação geral permanece para casos sem alvo direto viável.

O modo apenas seleciona a rota; a inclusão ocorre na revisão automática.
`sed_auto_run_direct` é compartilhado pelo Automático próprio e pelo novo
executor coordenado. Exige jogador, mod habilitado, Automático exclusivo,
filas pública e privada vazias, construção ativa, proteção fiscal e limite
mensal. Conflito com ARoAI ou outro switch conhecido impede execução.
A exceção de coordenação exige executor 11, objetivo 2 e primeira prioridade
atualmente elegível. Cada aprovação também exige o rank 1 daquele tipo/estado
quando a coordenação está ativa. Um candidato de outro tipo no mesmo estado
não pode aproveitar a autorização.

O resultado mensal registra a inclusão observada na fila, falha, bloqueio de
fila ou limite mensal. Continua sendo uma tentativa por mês; falha consome a
tentativa. A política de restauração permanece intacta. Obras existentes,
construtores desconhecidos e autoexpansões nativas continuam fora do controle.
A guarda ainda usa a política fiscal inicial, sem previsão completa de custo
incremental, trabalhadores e insumos futuros.

189 testes sintéticos aprovados. Oito regressões exercitam execução direta,
restauração, limite, filas, revalidação, tipo/estado, finanças e ARoAI. Um teste
de validação adversarial rejeita autoridade ampliada, remoção da guarda e rank
menos restritivo. Validação estática e gerador aprovados. Inclusão real e UI
permanecem pendentes de campanha.


## 0.6.14 — Expansões da indústria bélica

O catálogo passa de oito para onze bens com armas leves, artilharia e munição.
Doze métodos ativos e seus outputs foram conferidos no `01_industry.txt`
vanilla local. Os novos alvos reutilizam elegibilidade, aprovação, limite
mensal, fila, histórico de resultado, ignorar/restaurar e metas anuais.

Candidatas militares exigem despesa militar positiva, demanda de mercado
positiva e escassez atual. O produtor deve existir, produzir o bem pelo método
ativo, estar em estado incorporado, com ocupação mínima de 80%, sem falha de
contratação, falta de insumos, déficit de infraestrutura ou expansão na fila.
Isso ainda usa despesa nacional como sinal parcial de necessidade. Demanda
do mercado compartilhado não identifica precisamente consumo das tropas.

A pontuação recebe bônus de 20 durante guerra. A regra é inicial e não foi
calibrada em campanha. Prioridades civis continuam concorrendo pela pontuação;
crise fiscal continua prevalecendo no objetivo macro e na proteção automática.

Assistido permite aprovar um nível de produtor militar elegível. Automático
próprio aplica os limites fiscais e de fila já existentes. Com coordenação
externa ativa, o Director preserva a delegação geral e não executa em paralelo.
O Advisor/Supply Chain ainda seleciona os próprios projetos, sem garantia de
executar o alvo militar específico. Navios continuam no diagnóstico; nova
fábrica, PMs das tropas e recrutamento seguem pendentes.

180 testes sintéticos aprovados. As oito novas regressões militares cobrem
aprovação, demanda, trabalhadores, insumos, ranking, proteção fiscal,
coordenação e livro de resultados. Geração, ZIP e validação estática local
aprovados. Inclusão real de obra e layout ainda exigem teste de campanha.


## 0.6.13 — Avaliação econômico-militar

O briefing inclui financiamento do exército, indústria bélica e marinha.
A nova avaliação é atualizada pela entrada normal do plano nacional e lê
`military_expenses`, `military_expenses_share` e `is_at_war`, verificados nos
scripts vanilla locais. A participação é apresentada como indicador do jogo,
sem presumir denominador diferente do fornecido pela engine.

Armas leves, artilharia, munição, navios de guerra à vela e blindados são
monitorados no mercado. Avisos exigem demanda positiva e escassez. Um mercado
compartilhado pode ter demanda de outros países; esses sinais ainda não
identificam o consumo das forças nacionais.

Diretrizes distinguem observar demanda, sustentar a força atual, investigar
abastecimento, estabilizar orçamento e estudar modernização. A última exige
saldo positivo, guarda fiscal de expansão, ausência de dívida e doze semanas
de despesas fixas em reservas, sem escassez militar detectada. Esse limiar é
inicial e não estima o custo de uma modernização específica. Crise/default ou
saldo operacional negativo têm precedência. Sem despesa militar positiva,
a escassez compartilhada não cria inferência de necessidade nacional.

A avaliação é informativa e não muda a seleção dos executores, recrutamento,
PMs, salários militares ou composição das forças. Construção militar dirigida,
consumo nacional, prontidão e coordenação do recrutador permanecem pendentes.

172 testes sintéticos aprovados. Sete novas regressões cobrem atualização
normal, escassez, ausência de demanda, limites fiscais, resolução e limpeza.
Geração, ZIP e validação estática local passaram. Novos dados e layout ainda
exigem observação na campanha, junto do roteiro acumulado.


## 0.6.12 — Acompanhamento de gargalos com obras na fila

Quando não há outra expansão elegível, o plano mantém o objetivo de
infraestrutura ou oferta se detectar expansão relacionada enfileirada.
Para oferta, exige escassez atual, estado incorporado e método de produção
verificado para o bem, incluindo produtores alternativos. Estados ignorados
pelo jogador não mantêm essa espera. Para administração, tributação e energia,
a espera exige expansão correspondente em estado incorporado afetado pelo
problema. Crise fiscal mantém precedência sobre acompanhamento de obra.

A coordenação mostra executor 10 e resultado mensal 20 enquanto aguarda.
Nesse estado, as opções externas de novas obras permanecem suspensas.
Cancelamento, conclusão, fim da escassez ou surgimento de outra prioridade
provocam reavaliação pelos filtros normais. A detecção usa nível atual e nível
após fila, sem atribuir autoria, identidade ou impacto previsto ao projeto.

A espera é conservadora. Uma obra relacionada pode suspender a autorização
nacional da rotina enquanto não houver outra prioridade elegível. A versão
acompanha expansões de prédios reconhecidos pelas leituras existentes; novos
prédios ainda não expostos nessas leituras podem ficar fora da detecção.

165 testes sintéticos aprovados, geração e validação estática local aprovadas.
Sete novas regressões cobrem fila, cancelamento, resolução, prioridade
alternativa, métodos produtivos, localização da energia e precedência fiscal.
Novas mensagens e transições ainda aguardam o teste conjunto em campanha.


## 0.6.11 — Política e acompanhamento da delegação

O Director guarda e controla três opções adicionais do Supply Chain. Expansões
ficam restritas a estados incorporados pelas opções verificadas
`zw_var_develop_incorporated_states` e `zw_var_ip_incorporated`. A meta de
instituições `zw_var_scsab_gov_admin_for_institution` fica suspensa durante a
coordenação para que administração responda à burocracia atual. Os valores e
a ausência originais são restaurados ao sair do Automático ou desativar.
Snapshots são capturados uma vez antes da primeira alteração, inclusive em
coordenações salvas por versões anteriores. Sair de um save antigo sem uma nova
sincronização preserva as opções ainda não capturadas.

Limites numéricos de administração, tributação, energia, ferrovia e setores
passam a um nível por local selecionado pela rotina externa. A soma nacional
pode superar um nível. Advisor e cadeias gerais mantêm a semântica anterior.
Essa escolha é um ritmo inicial conservador, ainda sem calibração de campanha.

O painel informa a agenda verificada no `zw_scsab_je.txt` instalado. A rotina
tributária roda nos meses de script 5/11 (junho/dezembro), e setores em 1/7
(fevereiro/agosto). Agenda e algoritmo continuam pertencendo ao Supply Chain.

Impostos e salários civis mostram o último comando do Director, com mês,
ano e níveis anterior/solicitado. Esse registro comprova a passagem pelo efeito,
mas o resultado deve ser conferido no orçamento. Reavaliações sem alteração
não criam histórico; restauração de modo não reescreve o último comando
automático; desativar remove o histórico e preserva as travas mensais.

158 testes sintéticos aprovados, gerador e validação estática local aprovados.
A nova interface, o efeito das opções externas e save/reload continuam pendentes
do teste conjunto do jogador. Nenhuma nova inicialização de engine nesta etapa.


## 0.6.10 — Objetivo e executor

Capturas do jogador confirmaram revisão automática de outubro a dezembro de
1837 no Uruguai. No teste otomano, o objetivo de capacidade tributária coexistia
com orientação geral de crescimento ao Advisor. Obras novas foram observadas,
mas sua autoria e relação causal com o Director não foram comprovadas.

Administração, tributação e energia agora exigem os adaptadores específicos do
Supply Chain. Sem ferramenta disponível ou sem a proteção fiscal específica,
a coordenação suspende novas opções e mostra execução pendente. O Advisor
continua recebendo orientação geral para os demais objetivos compatíveis.
A rotina específica de setores de construção tem preferência sobre o Advisor.
O diagnóstico tributário só considera estados incorporados. Isso não altera os
filtros internos do Supply Chain, incluindo sua seleção de estados.

A última revisão distingue delegação, falta de executor específico, bloqueio
fiscal e conflito com ARoAI. Snapshots e restauração permanecem cobertos por
regressões. Cinco testes novos, 151 testes aprovados no total, geração e
validação estática contra os arquivos locais 1.15 aprovadas. A UI e as novas
transições ainda aguardam confirmação na campanha. A fila nativa e os níveis
fiscais foram vistos em capturas anteriores, sem comprovação causal das mudanças.


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

## Salários do governo na 0.6.6

O controle de gastos começa pelo salário civil do governo, com a mesma
reversibilidade dos impostos:

- Crise ou default (classificações 3 e 4): desce um nível, com piso `low`.
- Classificação 1 ou 5 com superávit, sem dívida e doze semanas de despesas
  fixas em ouro: sobe um nível, com teto `medium`.
- Cautela (2), Manual e Assistido não alteram salários.

`sed_gov_wage_saved` guarda o nível original na primeira alteração e
`sed_restore_wage_policy` o devolve ao sair do Automático ou desativar. A
revisão mensal aplica no máximo um passo de imposto e um de salário. Salários
militares, despesas discricionárias, subsídios e impostos de consumo continuam
fora do controle; não há estimativa do efeito de um passo no orçamento nem na
burocracia.

Fonte vanilla 1.15: `set_government_wage_level` em
`common/effect_localization/00_country_effects_loc.txt:279`, trigger
`government_wage_level` em
`common/trigger_localization/00_trigger_localization.txt:3269` e níveis
`very_low`–`very_high` em `common/static_modifiers/00_code_static_modifiers.txt:366–393`.
O efeito aparece apenas na localização de efeitos, sem uso nos scripts e
históricos vanilla; por isso a aceitação na engine é a principal incerteza
desta etapa, mais do que no `set_tax_level`, que é usado no histórico.

O validador permite `set_government_wage_level` somente em
`sed_apply_wage_policy` e `sed_restore_wage_policy`, com valores do enum, e
exige guarda explícita de modo Automático. 135 testes sintéticos aprovados
incluem corte até o piso, subida até o teto, ausência de mudança em cautela e
restauração por troca de modo e desativação.

## Livro de resultados por alvo na 0.6.7

O Director registrava apenas que uma obra foi enfileirada, sem medir o que
acontecia depois. A 0.6.7 relaciona cada pedido confirmado dos oito bens
estratégicos a um desfecho observado:

- Na aprovação, o estado guarda `sed_<bem>_intent_level` (nível do produtor
  antes da fila) e `sed_<bem>_intent_variant` (qual variante foi enfileirada).
- A confirmação incrementa `sed_<bem>_intents` no país.
- Quando o pedido sai da fila, o nível atual é comparado com a linha de base.
  Nível maior conta `sed_<bem>_completed`; nível igual ou menor conta
  `sed_<bem>_abandoned`; `sed_<bem>_result` guarda 1 ou 2 e
  `sed_<bem>_result_month` registra o mês civil pelo `sed_live_month_key`.
- A leitura é exibida no plano somente depois do primeiro pedido, com pedidos,
  concluídos e abandonados por bem.

A conclusão é **inferida** pela saída da fila e pelo nível do produtor, não por
uma identidade de projeto. Cancelamento seguido de obra externa no mesmo estado
e prédio, rebaixamento ou remoção podem distorcer a contagem. O livro cobre os
oito bens; ferrovia e setor de construção continuam sem esse registro.

A captura de nível usa `b:<prédio>.level` como valor de script, forma presente
no Advisor instalado (`common/script_values/advisor_core_values.txt:1040` e
`:1579–1580`), além das comparações de nível já usadas pelo Director.

136 testes sintéticos aprovados incluem captura de linha de base e variante,
conclusão quando o nível sobe, abandono quando a fila esvazia sem novo nível e
contagem acumulada de dois pedidos. Nada foi observado na engine: a leitura de
`b:<prédio>.level` em valor e a ordem exata entre conclusão, cancelamento e
limpeza mensal ainda não foram confirmadas.

### Ferrovia e setor de construção na 0.6.8

O mesmo livro passou a cobrir os dois tipos restantes. A aprovação grava
`sed_railway_intent_level` ou `sed_construction_intent_level` no estado; a
confirmação incrementa `sed_<tipo>_intents`. Quando o pedido sai da fila, nível
maior conta `sed_<tipo>_completed`; nível igual ou menor, ou prédio ausente,
conta `sed_<tipo>_abandoned`. `sed_<tipo>_result` e `_result_month` guardam o
último desfecho, e o plano mostra pedidos/concluídos/abandonados após o
primeiro pedido de cada tipo.

A mesma inferência por fila e nível se aplica: não há identidade de projeto, e
cancelamento seguido de obra externa no mesmo estado pode contar como
conclusão. Desativar limpa os marcadores estaduais e os contadores nacionais.
137 testes sintéticos aprovados incluem ferrovia concluída e setor abandonado
no mesmo cenário. Continua sem confirmação na engine.

## Calendário e limites corrigidos na 0.6.9

Metas exigem três observações em meses consecutivos de calendário. Atualizações
no mesmo mês preservam a idade. Um mês sem observação reinicia a sequência.
Contadores legados sem data são reiniciados para reconstruir a evidência.

Imposto e salário civil permitem um ajuste automático por mês, cada qual com
marcador próprio que persiste após sair do modo ou desativar. As restaurações
explícitas devolvem o nível original. A redução de imposto termina em baixo.
O livro acompanha a variante solicitada e verifica presença do produtor antes
de inferir o resultado. Fontes, defeitos corrigidos e limites da verificação
estão em [REVIEW_2026-11-10.md](REVIEW_2026-11-10.md).
