# Smart Economy Director — Victoria 3 1.15

Na 0.7.32, o objetivo 9 (energia local 20% acima da base) ganha o mesmo
tratamento: sem Supply Chain detectado, o Automático amplia a usina elétrica um
nível por mês no estado com energia cara que aceite a obra, reservando 400
pontos e exigindo a tecnologia de geração elétrica pelo próprio jogo. Com a
ferramenta externa, o caminho dela continua sendo o usado.

Na 0.7.31, os objetivos 6 e 7 do plano (burocracia nacional negativa e estado
usando mais capacidade tributária do que tem) deixam de ficar só na mão do
Supply Chain: sem ferramenta externa detectada, o Automático amplia a
administração pública um nível por mês no estado que aceita a obra, sob as
mesmas guardas de fila privada, pausa, orçamento e uma tentativa por mês. O
objetivo 9 (energia) continua delegado.

Na 0.7.30, quando a escassez de um bem não tem produtor no país e nenhum
estado pode receber a fundação, o Automático amplia um Centro de Comércio
existente ou funda o primeiro para comprar capacidade de comércio. É o último
recurso do plano: não abre rota, não mexe em tarifa ou subvenção e não constrói
sob Isolacionismo nem em estado com infraestrutura negativa.

Na 0.7.29, o evento de escassez ensina o caminho de importação da 1.9+:
Centro de Comércio e capacidade de comércio, tarifa ou subvenção no painel do
bem, cláusula Transferência de Bens em tratado e o bloqueio do Isolacionismo.
Também corrige a localização em inglês, que era gerada em português desde que a
bandeira de idioma passou a ser reutilizada como rótulo de laço.

Na 0.7.28, a modernização de métodos de produção cede os prédios que o
Auto-Apply PMs já administra (botão do prédio ou do grupo ligado), em vez de
disputar o mesmo grupo de PM. A auditoria dos mods instalados está em
`docs/COMPATIBILITY.md`.

Na 0.7.27, o painel lê o Controllable Private Construction — o mod de controle
da construção privada que o jogador mantém ativo — e lista apenas quais
restrições estão ligadas. É leitura: o Director não altera essas opções, não
injeta regras `can_build_*` e não cancela obras. Quando a fila privada bloqueia
o Automático, o painel aponta o diário daquele mod como caminho para restringir
a autoexpansão.

Na 0.7.26, a unidade salarial usada no retorno é por família de prédio, com
queda para a média nacional quando a família não tem amostra saudável. O
jogo não expõe qualificação nem salário por profissão, então esses filtros
continuam aproximados por ocupação e contratações falhas.

Na 0.7.25, a meta de escassez que volta em anos consecutivos vira plurianual:
ganha prioridade extra, fica visível enquanto a falta persistir e reinicia se
passar um ano sem escassez (limite de cinco anos).

Na 0.7.24, o painel mostra quantos projetos do governo e quantos privados
estão na fila, ao lado dos níveis. O autor de cada item não é exposto pelo
script, então o Director não afirma quem enfileirou a obra.

Na 0.7.23, o painel compara a referência de semanas da fila com a duração
restante medida pela própria engine (`construction_queue_government_duration`,
arredondada para cima em faixas), sem trocar a reserva de ouro.

Na 0.7.22, o evento de escassez mostra os pedidos de compra e venda do bem no
mercado, para você medir a lacuna antes de abrir a importação. Os números vêm
direto do mercado; o Director não estima custo, frete nem comboios.

Na 0.7.21, quando a escassez de um bem não tem expansão local elegível nem
pedido pendente, o Director dispara um evento próprio com prazo e três opções:
reconhecer a importação (silêncio de 12 meses), recalcular o plano agora ou
adiar por 24 meses. O evento orienta; abrir rota comercial é ação do jogador,
porque o script não pode fazê-lo na 1.15.

Na 0.7.20, o painel declara que leis, imposto de consumo e gasto discricionário
ficam fora do Director e reconhece o Smart Government Advisor quando instalado,
sem repetir as recomendações de leis dele.

Na 0.7.19, o painel mostra a unidade salarial observada (ou o fallback
material) usada pelas decisões de oferta e pela pontuação de PMs.

Na 0.7.18, a pontuação de modernização e de recuperação de PMs desconta a
folha salarial da mudança. Um par materialmente positivo pode ser descartado
quando a troca adiciona emprego ponderado.

Na 0.7.17, a decisão de oferta desconta a folha salarial observada nos prédios
saudáveis. A elegibilidade, a preferência entre fornecedores e o plano usam o
retorno após salários, com a margem material como referência de reserva.

Na 0.7.16, as reservas e guardas fiscais usam receitas fixas menos saldo
operacional para medir despesas fixas. A proteção dos salários militares
reconhece os papéis diplomáticos no escopo de país.

Na 0.7.15, a fundação das indústrias próprias considera os insumos da
configuração básica verificada. Métodos avançados são avaliados na configuração
inicial do prédio conforme tecnologia, oferta e referência econômica.

Na 0.7.14, papel entra na construção própria e no planejamento de insumos.
O Automático pode fundar a primeira fábrica ou ampliar um produtor elegível.
A cadeia considera a disponibilidade de madeira e dos insumos de seus PMs.

Na 0.7.13, o Automático também avalia bens civis caros com demanda superior à
oferta. A obra própria exige margem material estimada positiva e os filtros
de trabalho, insumos e orçamento. O limiar inicial de preço é 20% acima da base.

Na 0.7.12, preços observados no mercado e faixas de preços locais passam a
influenciar a escolha de fornecedores para obras próprias. As referências
são renovadas no plano e na aprovação e incluem margem de incerteza.


Na 0.7.11, o Automático compara fornecedores do mesmo bem por oferta e margem
material estimada. A referência inclui subprodutos e insumos dos PMs ativos,
com preferência por margens não negativas e desempate econômico entre ofertas
iguais. Fornecedores com saída líquida zero do bem-alvo são excluídos.


Na 0.7.10, o Automático pode reduzir a dependência de insumos em falta nos
produtores existentes, inclusive em default e com expansão enfileirada. Ele
avalia métodos com menores entradas e preservação de pelo menos metade da
produção nominal estimada. Essa recuperação tem prioridade sobre modernizar
e pode reduzir a produção nominal em troca de menor dependência de insumos.


Na 0.7.9, o Automático moderniza produtores existentes de bens em falta ou
insumos prioritários. A escolha considera ganho material estimado e reserva
insumos adicionais, com uma tentativa mensal compartilhada com a construção
própria e intervalo de três meses por prédio. Gerentes de PMs ativos no
Advisor têm precedência. Lucro real e qualificações continuam pendentes.


Na 0.7.8, a escolha inicial de PMs compara saída e margem material de referência.
O Automático pode selecionar um método mais produtivo com insumos disponíveis,
ou iniciar com a configuração básica. A margem usa preços-base e estresse de
receitas e custos. As reservas de insumos das trocas são mantidas no mês civil.


Na 0.7.7, o Automático configura métodos básicos de produção nas indústrias
que fundou e acompanha. A configuração passa por verificações de insumos,
trabalho estimado e permissão do jogo. A escolha inicial de PMs está
implementada para o catálogo de produtores. Modernização e otimização
contínua seguem pendentes.


Na 0.7.6, o orçamento direto considera a fila existente e a nova obra na
cobertura por reservas, com referência para projetos simultâneos. O Automático
pode retomar investimentos com déficit semanal quando a operação, a dívida e
a cobertura estimada permitem. Custos e prazo continuam aproximados.


Na 0.7.5, a recuperação fiscal inclui salários militares na paz. Em crise com
déficit operacional, o Automático corta um nível por mês até baixo. Guerra,
jogada diplomática e mobilização impedem cortes. Os cortes feitos pelo
Director podem ser recuperados conforme prontidão militar e orçamento. Sair
do Automático restaura o nível original.


Na 0.7.4, o Automático percorre vários elos de fornecedores para chegar a uma
expansão ou fundação viável. Ele considera alternativas disponíveis, espera
obras relacionadas e encerra a análise de dependências circulares. As
prioridades são recalculadas em cada leitura conforme a oferta observada.


Na 0.7.3, fundações de indústrias e ferrovias passam a exigir reserva estimada
de trabalhadores e insumos. Para prédios ausentes, os insumos usam o maior
consumo por grupo de PM entre os métodos tecnologicamente disponíveis. Esse
limite conservador pode adiar uma fundação que funcionaria com um PM simples.
Pedidos próprios ainda sem prédio reservam trabalhadores e insumos, sem dupla
contagem quando o prédio aparece. Um fornecedor ausente pode ser fundado para
abastecer uma indústria bloqueada por insumos.

Na 0.7.2, o orçamento direto estima a duração e os materiais do primeiro projeto
pelo tipo de prédio, sua construção exigida e a capacidade semanal. A reserva
exigida acompanha essa duração, até 56 semanas, em vez de usar só a janela fixa
de 26 semanas.

Na 0.7.1, um estado com déficit de infraestrutura e sem ferrovia pode receber
a primeira ferrovia pelo Automático, com as mesmas guardas de orçamento,
materiais e fila. O pedido continua pendente enquanto a obra está na fila,
mesmo antes de existir prédio, e não é duplicado em outro estado.

Na 0.7.0, o Automático pode fundar a indústria ausente que causa escassez: se
um bem está em falta, o país não tem produtor verificado e algum estado
incorporado pode hospedar a construção, o Director enfileira um nível do
prédio novo sob as mesmas guardas fiscais, de materiais, de fila e o limite
de uma tentativa por mês. Sem estado apto, o objetivo 5 registra o bloqueio e
nada é forçado.

Na 0.6.26, o Automático age com a fila pública ocupada, pode expandir o setor
de construção quando ele é a primeira prioridade do plano e agenda uma segunda
revisão no mesmo mês quando a fila privada bloqueia a primeira. A expansão
automática do setor continua sujeita às guardas fiscais e de materiais, e o
resultado não é explicado na interface além do status mensal.

Na 0.6.23, ao construir para suprir um insumo prioritário, o Automático
seleciona o fornecedor elegível de maior produção-base por nível, estimada
pelos métodos de produção ativos do jogo base.

Na 0.6.22, o painel identifica o estado, a expansão bloqueada e o insumo
necessário, exibindo até três estados por insumo.

Na 0.6.21, um insumo pode ganhar prioridade quando sua oferta limita uma
expansão para atender à escassez. A prioridade considera dependências diretas
entre bens cobertos e respeita os filtros de construção do produtor do insumo.

Na 0.6.20, expansões de oferta projetam insumos adicionais e compromissos
conhecidos, com tratamento estadual de energia e transporte. A suíte atual
tem 236 testes aprovados. A calibração em campanha segue pendente.

A versão 0.6.23 acrescenta planejamento nacional inicial e coordenação de
construção com Economy Advisor e Supply Chain Semi-Auto Builder. O diário
mostra objetivo atual, situação fiscal, executor escolhido e até três
prioridades entre estados e setores.

Ao selecionar **Automático**, o Director guarda as opções de construção dos
executores detectados e habilita o caminho escolhido pelo plano. Infraestrutura,
capacidade administrativa, energia, oferta e crescimento/diversificação têm
rotas próprias. Sair para **Assistido** ou **Manual**, restaurar opções ou
desativar devolve os valores originais aos outros mods.

Os adaptadores controlam sete opções de construção e quatro opções de objetivo
e orçamento do Advisor, verificadas nos arquivos instalados.
O Director escolhe entre crescimento, padrão de vida e retorno ao tesouro,
e aplica orçamento equilibrado ou preservação das reservas. O Economy Advisor
avalia prédios e estados usando o objetivo configurado. O Supply Chain mantém suas categorias e filtros internos. Revisões
ocorrem no pulso mensal e no evento agendado do Director. O painel distingue
orientação aplicada de inclusão de obra.

O executor próprio permanece disponível quando ferramentas externas estão
ausentes. Revalida as guardas e tenta a primeira expansão do plano, com limite
persistente de uma tentativa mensal. Esse limite pertence ao executor próprio.
Os executores externos seguem suas quantidades e agendas.

## Modos

| Modo | Comportamento |
| --- | --- |
| Manual | Consulta diagnóstico e recomendações. Ao sair do Automático, restaura opções externas originais |
| Assistido | Permite aprovação individual de expansões elegíveis |
| Automático | Coordena executores detectados ou usa o executor próprio quando estão ausentes |

A interface usa botões nativos, corpo de texto de 20 pontos, títulos de 26 e
cartões com altura natural. **Mostrar indicadores e detalhes** abre métricas,
motivos de rejeição e listas completas de candidatos. O plano principal contém
até três prioridades.

## Política inicial e cobertura

A guarda básica exige saldos semanal e operacional não negativos, ouro
cobrindo quatro semanas de despesas fixas e
dívida até 75% do crédito, quando houver dívida. Inadimplência e pausa suspendem
a coordenação de construção. Esses limiares são parâmetros iniciais avaliados
em cenários sintéticos e ainda precisam de calibração em campanha. O caminho
do Advisor admite também financiamento por reservas com a cobertura descrita
em PLANNING.md. Impostos e salários civis têm um ajuste automático por mês
de calendário e restauração dos níveis anteriores ao sair do modo.

O plano compara infraestrutura e produtores existentes de doze bens — madeira,
ferro, carvão, cereais, tecido, ferramentas, mantimentos, roupas, armas leves,
artilharia, munição e papel —, além de ferrovia e do setor de construção. Também identifica
escassez desses bens sem o tipo de produtor atendido e objetivos administrativos
ou de energia. A autorização do executor externo permite que ele avalie
investimentos além do escopo das expansões próprias do Director.

O desenvolvimento está parcial. Custo incremental completo, projeção de
trabalhadores e insumos futuros, outras despesas, identidade de projetos,
avaliação causal dos resultados e estratégia plurianual seguem
pendentes. As integrações e o layout 0.6.9 ainda precisam de verificação na
engine e de save/reload. ARoAI construtor é detectado e suspende a delegação
pelos dois adaptadores. Autoexpansões nativas têm cobertura pendente.

## Desenvolvimento e entrega

```bash
python3 tools/build_mod.py
python3 tools/build_mod.py --check
python3 tools/validate.py --game "/caminho/Victoria 3/game"
python3 -m unittest discover -s tests -v
python3 tools/package_mod.py
```

O pacote fica em `dist/smart-economy-director-0.7.32.zip`. A instalação local
pode ser atualizada com jogo fechado, backup e conferência dos arquivos pelo
comando documentado em [INSTALL.md](docs/INSTALL.md).

Consulte a [matriz viva de requisitos](docs/STATUS.md), a [política de planejamento
e coordenação](docs/PLANNING.md), os [testes de campanha](docs/MANUAL_RUNTIME_TEST.md)
e o [contexto de continuidade](docs/AI_CONTEXT.md). O briefing original está em
[PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md). A [auditoria de 09/11](docs/AUDIT_2026-11-09.md)
registra o estado histórico da 0.4.1.

A 0.6.9 foi instalada localmente com backup, 14 outputs conferidos e ordem
dos mods preservada. Os 146 testes sintéticos e a validação estática passaram.
A leitura das rotinas foi verificada até o menu da engine. Alterações fiscais
em campanha e restauração após save/reload seguem pendentes.

A revisão 0.6.9 corrige amostragem mensal de metas, limite fiscal por mês,
piso de imposto e acompanhamento da variante solicitada. Contadores antigos
sem data são reconstruídos com novas observações. A suíte tem 146 testes
aprovados e a inicialização da engine chegou ao menu com as rotinas carregadas.
O relatório está em [REVIEW_2026-11-10.md](docs/REVIEW_2026-11-10.md).
