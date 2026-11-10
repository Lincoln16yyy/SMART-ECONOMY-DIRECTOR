# Contexto de continuidade

Entrega local 0.6.7 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.7_20261110_012225_626750`.

## Livro de resultados por alvo 0.6.7

Cada aprovação dos oito bens grava no estado `sed_<bem>_intent_level` (nível do
produtor antes da fila) e `sed_<bem>_intent_variant`. A confirmação incrementa
`sed_<bem>_intents`. Quando o pedido sai da fila, o nível atual é comparado à
linha de base: maior conta `sed_<bem>_completed`, igual ou menor conta
`sed_<bem>_abandoned`; `sed_<bem>_result` e `_result_month` guardam o último
desfecho. O plano mostra pedidos/concluídos/abandonados só quando há histórico.
É inferência por fila e nível, não identidade de projeto; cancelamento com obra
externa pode distorcer. Ferrovia e setor ainda sem registro. A captura usa
`b:<prédio>.level` como valor (forma do Advisor instalado,
`advisor_core_values.txt:1040`). 136 testes aprovados; sem confirmação na engine.

## Entrega local 0.6.6

Entrega local 0.6.6 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.6_20261110_011134_926784`.

## Salários do governo 0.6.6

`sed_apply_wage_policy` move o salário civil do governo um passo por revisão no
Automático: desce em crise/default (piso `low`) e sobe com classificação 1/5,
superávit, sem dívida e doze semanas de despesas fixas em ouro (teto `medium`).
`sed_gov_wage_saved` guarda o original e `sed_restore_wage_policy` o devolve ao
sair do Automático ou desativar. Cautela, Manual e Assistido não alteram
salários; militares e despesas ficam fora. O efeito
`set_government_wage_level` só aparece na localização vanilla, sem uso em
scripts: aceitação na engine é a principal incerteza. 135 testes aprovados.

## Entrega local 0.6.5

Entrega local 0.6.5 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.5_20261110_010449_284523`.

## Política fiscal própria 0.6.5

No Automático, `sed_apply_fiscal_policy` move o nível de imposto um passo por
revisão mensal: sobe em cautela, crise ou default (até `very_high`) e desce com
classificação 1/5, superávit, sem dívida e doze semanas de despesas fixas em
ouro (até `low`). `sed_tax_level_saved` guarda o nível original e
`sed_restore_fiscal_policy` o devolve ao sair do Automático ou desativar.
Mudanças manuais durante o Automático são substituídas na revisão seguinte.
O validador limita `set_tax_level` a esses dois efeitos e exige a guarda de modo.
Salários, despesas, impostos de consumo e leis não são alterados; efeito real na
receita e aceitação na engine não confirmados. 132 testes aprovados.

## Entrega local 0.6.4

Entrega local 0.6.4 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.4_20261110_005319_526047`.

## Metas industriais anuais 0.6.4

Escassez de mercado por três meses consecutivos define uma meta industrial
anual para o bem: `sed_<bem>_short_months` conta a sequência e
`sed_<bem>_meta_year` grava o ano. A meta vale até a virada do ano civil, recebe
25 pontos adicionais no plano e aparece em linha própria no diário. Não cria
candidato: elegibilidade, fila, insumos, trabalhadores, infraestrutura,
permissão e política fiscal continuam obrigatórias. Desativar limpa contadores
e marcadores. Três meses e 25 pontos são parâmetros iniciais sem calibração em
campanha. Metas plurianuais, cadeias completas e feedback por alvo continuam
pendentes. 129 testes aprovados; comportamento na engine não confirmado.

## Entrega local 0.6.3

Entrega local 0.6.3 instalada com jogo fechado, 14 outputs conferidos e
content_load.json preservado. Backup em
`sed_backups/mod_before_0.6.3_20261110_002209_786280`.

## Produtores alternativos 0.6.3

O catálogo deixou de assumir um prédio por bem. Cereais aceitam fazendas de
trigo, centeio, arroz, milho e milhete; tecido aceita plantação de algodão e
fazenda de gado. Cada variante tem trigger próprio `sed_<bem>_<prédio>_eligible`;
a elegibilidade é uma disjunção e a aprovação enfileira o primeiro produtor
elegível. O diagnóstico de produtor ausente e as rejeições usam as mesmas
variantes. Fontes vanilla e limites em PLANNING.md. 126 testes aprovados;
combinações novas ainda sem confirmação na engine.

## Entrega local 0.6.2

Instalada com jogo fechado, 14 outputs conferidos e content_load.json
preservado. Backup em `sed_backups/mod_before_0.6.2_20261109_235909_180351`.

## Construção financiada por reservas 0.6.2

A classificação fiscal 5 permite coordenação quando o déficit operacional é
coberto por reservas: receita fixa não negativa, déficit total observado, sem
dívida e ouro cobrindo doze semanas de despesas fixas mais 26 semanas do
déficit. `sed_coord_fiscal_safe` aceita a guarda antiga ou a 5 com Advisor
detectado; os ramos do Supply Chain continuam exigindo saldo não negativo. A
classificação 5 permite crescimento e não força estabilização. O limite
mensal automático passou a usar o script value `sed_live_month_key`, e o
validador rejeita aritmética embutida em igualdades `var:`. 124 testes
aprovados; instalação e comportamento em campanha ainda não confirmados.

## Entrega local 0.6.1

Instalada com jogo fechado, 13 outputs conferidos e content_load.json
preservado. Backup em `sed_backups/mod_before_0.6.1_20261109_222628_869777`.

## Objetivo e orçamento do Advisor 0.6.1

Integração de quatro opções verificadas do Advisor, além das sete de construção.
Ao escolher Advisor, o Director aplica crescimento, padrão de vida quando bens
essenciais lideram o plano ou retorno ao tesouro quando a dívida positiva chega
a 50% do crédito. A orientação financeira tem prioridade. Crescimento/social
usam orçamento equilibrado do Advisor, com sua reserva de doze semanas. Retorno
ao tesouro preserva reservas. A opção de endividamento do Advisor fica desligada
enquanto ele recebe essa orientação. O limiar de 50% é uma decisão inicial da
implementação com calibração em campanha pendente.

Snapshot e restauração incluem presença e valores das quatro opções. Migração
de uma coordenação 0.6.0 ativa captura antes da primeira escrita. Liberar antes
de capturar preserva as opções. Delegação ao Supply Chain mantém a política do
Advisor. A autorização de escrita do validador cobre apenas as onze opções nos
dois efeitos adaptadores existentes.

120 testes aprovados, geração atual, validação estática e ZIP aprovados.
A integração nova ainda aguarda confirmação de engine e save/reload. Fontes e
política em PLANNING.md. Instalação e publicação registradas na entrega abaixo.

## Entrega local 0.6.0

Instalada com jogo fechado. Os 13 outputs conferem byte a byte com o gerador,
e content_load.json foi preservado. Backup em
`sed_backups/mod_before_0.6.0_20261109_220347_442062`.
115 testes sintéticos aprovados, geração atual, validação estática contra
Victoria 3 1.15.0 e ZIP aprovados. A instalação substitui a 0.5.8.
Selecionar Automático novamente aplica os adaptadores em save da 0.5.x.
Coordenação, novo layout e save/reload ainda aguardam verificação na engine.

## Planejamento e coordenação 0.6.0

Direção confirmada pelo jogador em 09/11. O Director deve definir objetivos e
ativar somente caminhos necessários de Economy Advisor e Supply Chain. A versão
implementa plano nacional inicial, três prioridades globais e adaptadores
reversíveis de sete opções. Selecionar Automático guarda as opções de ferramentas
detectadas, escolhe executor por objetivo e impede construção própria em paralelo.
Sair para Manual/Assistido, liberar ou desativar restaura presença e valores.

Plano cobre infraestrutura, oferta e ausência de tipos de produtor atendidos,
capacidade, crescimento/diversificação, burocracia, tributos e energia local.
A classificação fiscal usa saldos, quatro semanas de despesas fixas em ouro e
dívida até 75% do crédito. São parâmetros iniciais escolhidos na implementação,
com testes por escala. Calibração em campanha e custo incremental ficam abertos.

A seleção interna do Advisor permanece sob sua política própria. O adaptador
controla autorização, sem transmitir estado/prédio. Os executores externos
conservam agendas e quantidades. O resultado 18 registra orientação aplicada.
ARoAI construtor detectado suspende a delegação. Autoexpansões nativas ainda
têm cobertura pendente. Impostos/gastos próprios, projeção futura de emprego e
insumos, reconciliação por projeto e estratégia plurianual continuam parciais.

Código em tools/planning.py e tools/coordination.py, integrado ao gerador.
O validador admite as sete opções externas apenas nos dois efeitos adaptadores
com guardas de jogador e coordenação ativa. Testes negativos cobrem escrita
fora desse limite. A política, fontes e roteiro estão em PLANNING.md e STATUS.md.
O relato dos testes anteriores foi pouca mudança visível enquanto outros mods
construíam. Ainda falta confirmação dos novos fluxos na engine e save/reload.

## Explicação das opções externas — 0.5.9

O painel Automático lista ao vivo as oito opções externas detectadas, com
nomes de mod e função, mesmo quando default, limite mensal, pausa ou fila
aparecem como primeiro bloqueio. Sem opções, em Manual/Assistido ou desativado,
a lista fica oculta. O texto explica que configuração ligada já suspende o
Director sem esperar obra, e orienta usar Assistido ou ajustar o outro mod.
Não altera opções externas, regras econômicas, dispatcher ou histórico.
Uma tabela no gerador alimenta guarda, linhas e traduções para manter cobertura
coerente. A meta institucional isolada continua fora da detecção.

91 testes aprovados, incluindo cada opção isolada, todas juntas, retirada ao
vivo, coexistência com fila ocupada, modos, desativação e leitura sem mutação.
Geração, validação estática local 1.15.0 e pacote aprovados. Layout novo não foi
verificado na engine. Preparada enquanto o jogador testa: NÃO instalada;
a instalação usada pelo jogador permanece 0.5.8. Não atualizar durante a
sessão nem interpretar capturas da 0.5.8 como confirmação da lista nova.

## Entrega local 0.5.8 — 2026-11-09

Instalada com jogo fechado. Backup:
`sed_backups/mod_before_0.5.8_20261109_212722_719786`.
Os 13 outputs foram conferidos byte a byte; `content_load.json` preservado.
A pasta antiga foi retirada antes de gerar a nova, sem arquivos remanescentes.
Isso atualiza as notas anteriores de instalação 0.5.4; engine e save/reload
continuam sem teste nesta etapa.

## Autorização explícita do modo no efeito — 0.5.8

Os dez efeitos mutantes exigem `sed_execution_mode_permits_approval` no país:
Assistido sem Automático, ou Automático com `sed_auto_executor_safe`.
Qualquer marca Manual impede a aprovação, inclusive em combinação inconsistente
de modos; ausência de modo também bloqueia. Antes, a condição aceitava qualquer
modo não automático, deixando chamadas diretas no Manual passarem. A interface
já exigia Assistido; a correção fecha o contrato dos efeitos internos sem
acrescentar execução, primitiva ou tipo ao dispatcher. Diagnóstico continua
podendo inicializar o modo padrão de saves antigos conforme regra existente.

90 testes aprovados. Novos cenários cobrem dez ações em Manual, sem modo e com
marcas conflitantes contendo Manual, sem construção, pendência ou consumo de
mês; cobrem também mudança de Assistido para Manual após análise e retorno ao
Assistido. O harness ganhou avaliação de bloco AND, usado para exigir Assistido
sem Automático. A sintaxe existe nos triggers vanilla locais de 1.15.0
(`common/scripted_triggers/00_scripted_triggers.txt:50`). Validação estática,
geração e pacote 0.5.8 aprovados. Isso não comprova execução/persistência na
engine. Nenhum jogo iniciado; instalação local permanece 0.5.4.
Reconciliação por projeto, save/reload e planejamento fiscal continuam pendentes.

## Revalidação no efeito de construção — 0.5.7

Os dez triggers de aprovação agora consultam `sed_auto_executor_safe` quando
o modo é Automático. Antes, somente o dispatcher checava fila pública vazia,
construção não pausada e configurações concorrentes; o efeito mutante
revalidava apenas elegibilidade, jogador/ativação, default, fila privada e
limite mensal. Chamadas diretas aos efeitos podiam escapar dessas três guardas.
Agora as mesmas condições são exigidas também pelo efeito que chama
`start_building_construction`, sem nova primitiva ou novo tipo no dispatcher.
Setor de construção continua fora da seleção automática. Assistido mantém
aprovação explícita sob as guardas anteriores, inclusive com fila pública,
construção pausada ou outro executor configurado. Isso não autoriza operações
novas na interface nem transforma aprovação em garantia fiscal.

88 testes aprovados. A nova matriz percorre dez ações e doze bloqueios,
valida elegibilidade antes da mudança e chama o efeito após a mudança.
Confere ausência de inclusão, marca mensal e pendência; depois verifica o
comportamento Assistido. Os testes mensais anteriores continuam aprovados.
É simulação dos scripts gerados, sem reprodução de concorrência na engine.
Validação estática local 1.15.0 e pacote 0.5.7 aprovados. Nenhum jogo iniciado;
instalação permanece 0.5.4. Reconciliação de projetos, persistência em save e
planejamento fiscal incremental continuam pendentes.

## Administração do Supply Chain — 0.5.6

A guarda de configuração agora inclui `zw_var_scsab_gov_admin` e
`zw_var_scsab_gov_admin_for_tax`. A primeira habilita a rotina geral, que pode
reagir à burocracia negativa mesmo sem meta institucional; a segunda habilita
uma rotina tributária independente. `zw_var_scsab_gov_admin_for_institution`
isolada não habilita nenhuma dessas rotinas e não bloqueia o Director.

Fontes locais: Supply Chain instalado, efeito
`common/scripted_effects/zw_scsab_effects_2_gov_admin.txt:1–185`, botões
`common/scripted_buttons/zw_scsab_buttons.txt:215–383` e pulso
`common/journal_entries/zw_scsab_je.txt:84–126`. O primeiro limite exige a
configuração geral; o alvo institucional só altera o cálculo interno.
O efeito tributário exige sua própria configuração e tecnologia; seleciona
estados com capacidade tributária insuficiente. Os botões removem as opções
ao desligar. A política do Director detecta configuração, sem reproduzir
calendário, tecnologia, burocracia, orçamento ou seleção estadual externos.
Isso pode suspender o Automático mesmo sem obra externa naquele mês.
Não comprova ativação do diário externo nem resolve reconciliação da fila.

87 testes aprovados: os casos das opções independentes agora incluem as duas
configurações administrativas; novo cenário confirma que uma meta institucional
isolada não bloqueia nem é alterada. Painel, resultado 13 e guarda de execução
continuam usando o mesmo trigger. Validação estática local 1.15.0 e pacote
0.5.6 aprovados. Nenhum jogo iniciado; engine e save/reload não verificados.
Pacote não instalado: instalação local permanece 0.5.4.

## Detecção de opções independentes do Supply Chain — 0.5.5

O Automático suspende tentativas quando encontra uma das configurações
`zw_var_more_construction_sectors`, `zw_var_scsab_construct_railway` ou
`zw_var_scsab_construct_power_plant`, mesmo sem `zw_var_expand_building`.
A presença configura a opção; os botões do mod externo removem a variável ao
desligá-la. Fonte: Supply Chain instalado, `zw_scsab_buttons.txt:90–153,
383–479, 483–547`; efeitos 1, 3 e 4, limites iniciais; JE, pulso mensal.

Política deliberadamente conservadora: detecta configuração, sem reproduzir
tecnologia, calendário, orçamento ou seleção estadual do outro executor.
Pode suspender o Director mesmo quando o outro mod não construiria neste mês.
Não confirma que o diário externo esteja ativo. Não escreve em variáveis
externas. Assistido preserva aprovação explícita com suas guardas existentes.
Executor, resultado 13 e painel ao vivo consultam um único trigger
`sed_competing_builder_configured`, evitando divergência entre UI e execução.

86 testes passam, incluindo opções independentes com cadeias desligadas,
bloqueio sem consumir o mês, liberação ao remover a opção, painel ao vivo e
aprovação Assistida sem alterar configuração externa. Validação estática
contra o jogo local 1.15.0 aprovada. Pacote 0.5.5 gerado; não instalado nesta
etapa. Instalação permanece 0.5.4. Nenhum jogo foi iniciado.
As opções de administração, reconciliação de projetos, save/reload e política
fiscal incremental continuam pendentes. Não cobrar novo teste do jogador agora.

## Proteção de infraestrutura — 0.5.4

Produtores dos oito bens atendidos e setores de construção exigem saldo atual
de infraestrutura maior ou igual a zero. A aprovação revalida essa condição;
um cartão antigo não autoriza expansão se o estado entrar em déficit.
Ferrovias mantêm a elegibilidade em déficit para tratar esse gargalo.
Cartões mostram o saldo ao vivo e o bloqueio, e os detalhes contam rejeições
por infraestrutura separadamente, respeitando a prioridade dos demais motivos.

84 testes automatizados aprovados: incluem invalidação de cartões antigos,
limite zero, exceção ferroviária, escolha de outro estado pelo Automático e
contadores sem dupla contagem. Validação estática contra os arquivos locais
1.15.0 aprovada. Isso não verifica execução na engine, save/reload ou campanha.
A guarda considera déficit atual, sem projetar consumo do próximo nível nem
reservar capacidade para projetos concorrentes. Reconciliação completa das
filas e planejamento fiscal incremental continuam pendentes.

## Continuação — limite mensal persistente de tentativas 0.5.3

Instalada sem jogo em execução; backup `mod_0.5.2_20261109_121259_782337`;
13 outputs conferidos e load order preservado.

O Automático agora admite uma tentativa por mês, gravando
sed_auto_last_attempt_month antes de construir. A guarda é consultada no
executor e nos dez efeitos de aprovação quando o modo é Automático; isso não
adiciona setor de construção ao dispatcher automático. Inclusão sem confirmação
consome o mês; sem candidato/operacionalmente bloqueado não consome.

Importante mudança de limpeza: PERSISTENT_VARIABLES declara schema e marcador
mensal. Desativar limpa runtime/leituras/pendências, mas preserva essa única
marca de segurança quando existe. Evita reiniciar limite por modo/desativação.
Validador foi ajustado para exigir a preservação e não aceitar outras sobras.
Assistido continua explícito e sem esse limite, sujeito às guardas existentes.
A comparação usa year/month atuais, não sed_month_key do diagnóstico.

81 testes passam (77 anteriores + quatro), incluindo dez tipos, fila esvaziada,
troca de modo, reativação, falha de inclusão, Assistido, virada de ano sem
refresh e regressão negativa de limpeza. O contador sintético não comprova
fila real; persistência de variáveis continua sem save/reload na engine.
Proteção não é reconciliação completa, nem calibração fiscal, e não recupera
um histórico completo de versões anteriores. Manter interface legível e não
cobrar teste do jogador agora.

## Continuação — status temporal do Automático 0.5.2

Instalada sem jogo em execução; backup `mod_0.5.1_20261109_115813_269189`;
13 outputs conferidos e load order preservado.

Captura enviada pelo jogador confirma renderização legível dos botões nativos,
modos, resumo e botão Abrir fila, compatível com a UI 0.5.x. Leitura 7/1839,
saldo £15.3K, reservas £2.36M, projetos públicos/privados 45/2 e ausência de
déficit de infraestrutura. Isso não comprova clique de aprovação nem abertura
da fila, só apresentação. Não exigir nova rodada de testes agora.

0.5.2 separa revisão agendada/aguardando pulso, bloqueios atuais (leitura live)
e último resultado registrado com mês/ano. Arquivo do resultado usa variáveis
próprias, não é apagado por trocar modo/atualizar diagnóstico. Desativar limpa.
Saves antigos sem data/arquivo mostram que ainda não há registro nesta versão,
sem inventar uma data. Não há mudança no agendamento, guardas ou execução.

77 testes passam (73 anteriores + quatro do painel). Início com evento
pendente, consulta sem executar, exclusividade dos bloqueios, histórico versus
condição atual, troca de modo, virada do ano, limpeza e gravação pelo evento
cobertos no harness. Novos textos e passagem de tempo ainda não testados na
engine. A captura confirma a melhoria visual anterior, sem fechar a Fase 0.

## Continuação — cartões acionáveis 0.5.1

Instalada sem jogo em execução; backup `mod_0.5.0_20261109_114658_276092`,
13 outputs conferidos e load order preservado byte a byte.

O jogador pediu seguir construindo sem depender de testes seus agora. Mantida
a interface legível: cartões exibem aprovação disponível, Passar para Assistido
(sem construir) e Atualizar recomendações para cartão desatualizado. Guardas de
fila/default só aparecem como bloqueio da aprovação individual no Assistido;
fora dele, o cartão elegível oferece a troca de modo. Pendências/stale não
mostram troca de modo como se ela fosse resolver a elegibilidade.

Atalho Abrir fila de construção usa InformationPanelBar.OpenPanelTab com o
mesmo alvo production_methods/construction_queues do vanilla states_panel.gui.
Não é nova primitiva de construção. Os 73 testes passam (70 anteriores e três
novos cobrindo dez ações). Fluxos e atalhos ainda sem prova visual na engine;
sem teste oculto e sem solicitação de teste ao jogador nesta etapa.

## Direção atual do jogador e interface 0.5.0

0.5.0 instalada sem jogo em execução; backup `mod_0.4.1_20261109_113054_750010`,
load order preservado byte a byte. Auxiliar de teste não instalado.

O jogador não consegue testar enquanto botões não forem claramente visíveis
e os textos forem minúsculos. Pediu continuar construindo até melhorar isso;
não cobrar agora nova rodada de testes nem instalar auxiliar separado para ele.
A prioridade passou para a interface principal do Director.

Implementado 0.5.0: default_button da instalação nativa, texto principal 20,
títulos 26, botões 52 pixels. Recomendações antes dos indicadores completos;
controle Mostrar/Ocultar indicadores e detalhes, sem ação econômica. Cartões
agora usam flowcontainer/datamodel com altura natural, texto limitado à largura
e sem linhas fixas que cortam mensagens. Descrições repetidas encurtadas,
tooltips e dados mantidos. Nenhuma mudança nos filtros de construção.

70 testes passam (67 anteriores + três de controles/legibilidade/toggle).
Fontes vanilla conferidas: gui/shared/buttons.gui default_button;
gui/shared/defaults.gui fontsize_large=20 e fontsize_xxl=26;
great_game_widgets.gui usa flowcontainer/datamodel; tsarpoints_widgets.gui usa
background em flowcontainer. Validação estática não confirma renderização.
Nenhum jogo foi iniciado para teste oculto prolongado.

## Continuação — auxiliar de inspeção de filas

Criado `tools/build_queue_probe.py`: gera um mod auxiliar independente 0.1.0,
namespace sedqp_, com decisão/JE, leituras manuais de projetos e níveis por
lado, e nível atual/após fila/diferença por prédio dos dez tipos do Director.
Não tem mutações econômicas nem agenda. Não foi instalado/habilitado; runtime
do Director continua 0.4.1. Instruções e limitações em
[QUEUE_PROBE.md](QUEUE_PROBE.md). Não apresentar nível zero sintético, variáveis
Building ou listas no harness como confirmação da engine.

67 testes passam (61 anteriores + 6 do auxiliar). A entrega separa os dois
ZIPs; o principal não inclui scripts sedqp_. Próximo passo útil: conferir uma
linha pública, uma privada e primeira construção em cópia, registrando o que
foi realmente exposto. Ainda não há reconciliação por projeto, política fiscal
incremental ou inclusão real confirmada. Não iniciar teste oculto prolongado.

## Continuação — entrega CI e contrato de fila

A etapa seguinte corrigiu `.github/workflows/validate.yml`: publica o pacote
em caminho fixo `dist/smart-economy-director.zip`, sem versão duplicada, e
falha se o artefato não existir. O pacote continua contendo a versão atual em
seus descritores; CLI local sem --output mantém ZIP versionado. Sem mudança
no runtime/instalação 0.4.1.

Leia [QUEUE_CONTRACT.md](QUEUE_CONTRACT.md) para novas fontes da fila e a matriz
mínima ainda não executada. UI nativa expõe projetos/investidor/progresso, mas
isso não prova acesso por scripted effect. Supply Chain tem opções separadas
de ferrovia/energia/setores/admin que a flag geral de cadeias não protege.
61 testes e validação estática passaram; ZIP de CI conferido contra os 13
outputs. Nenhum jogo foi iniciado. O jogador enviou a auditoria para main;
o CI de `ada7c26` foi confirmado aprovado, sem inferir publicação de ZIP válido
pelo path antigo (upload-artifact pode só emitir warning).

## Orientação atual após auditoria — 2026-11-09

Leia [AUDIT_2026-11-09.md](AUDIT_2026-11-09.md) antes de continuar. Código auditado:
`ccf5c2ba325203faad9d704a1f139e21b8ce3261`, main, 0.4.1. Não houve alteração de
funcionalidade na auditoria. 61 testes do Director passaram agora; 26 da
referência passaram separadamente e seu validador tem 178 erros. A instalação
corresponde aos 13 outputs; isso não é comprovação de execução econômica.

Fase 0 parcial, diagnóstico parcialmente verificado, planejamento nacional
não implementado e executor experimental. Próximo bloco: contrato de fila,
reconciliação e opções dos outros executores, antes de novos tipos de obra ou
ranking. Sem leitura confiável dos projetos relevantes, não certificar
construção automática como segura. Não iniciar jogo oculto prolongado nem
alterar a campanha para obter candidatos.

Aprovação manual atual não exige pausa nem saldo positivo; exige Assistido,
elegibilidade, fora de default e fila privada vazia. Automático existe opt-in,
com guardas limitadas e sem teste de inclusão bem-sucedida na engine. Ignorar/
restaurar e diagnósticos 0.4.0/0.4.1 estão implementados e testados no harness,
mas sem cliques ou save/reload comprovados. As capturas de junho/1839 confirmam
texto do modo e bloqueio por fila ocupada, sem identificar commit da sessão.

GitHub main consultada pelo conector: `9366277…`; os dois commits de recursos
0.4.0/0.4.1 estavam locais no início da auditoria. Fetch/push por Git no shell
falham por DNS; o conector consegue ler. Não reescrever histórico para contornar.
Relatório/JSON publicados pelo conector no PR em rascunho #1:
https://github.com/Lincoln16yyy/SMART-ECONOMY-DIRECTOR/pull/1
A branch de auditoria usa a main remota 0.3.9 e não inclui os recursos locais
0.4.x; não confundir essa publicação documental com envio do código.

## Registros anteriores — consultar sua data e versão

Os resumos abaixo são históricos. Números de testes, exigência de pausa,
“sem modos” e próximos passos antigos não substituem a orientação da auditoria.
Referências a comportamento de pendências descrevem o script/harness, salvo
quando um teste de engine estiver explicitamente registrado.


O usuário solicitou seguir `Texto colado.txt` e ir publicando no GitHub
`Lincoln16yyy/SMART-ECONOMY-DIRECTOR`. O conteúdo original está preservado
integralmente em PROJECT_BRIEF.md. Leia-o antes de trabalhar.

Fase atual: ignorar e restaurar recomendações 0.4.1.
Instalada; backup `mod_0.4.0_20261109_103945_594880`; load order preservado. Cada cartão elegível tem
botão para ignorar apenas o tipo de expansão no estado. A variável estadual
permanece nas leituras e modos, bloqueia lista, aprovação e seleção automática.
O topo oferece restauração de todas as escolhas nos estados atuais do país,
com aviso enquanto existir escolha. Desativar limpa tudo. Obras enfileiradas
não são canceladas e restaurar não enfileira obras. Marcadores de pendência
continuam separados. Motivos de rejeição agora incluem escolhas ignoradas.
Os 61 testes passam; validação estática e conferência na engine seguem sendo
coisas distintas. Confirmar os novos botões, recarga com escolhas e layout no
jogo normal; não iniciar testes gráficos prolongados.

Estado anterior de referência: Fase atual: diagnóstico de rejeição de produtores locais 0.4.0.
Instalada localmente; backup `mod_0.3.9_20261109_102912_254983`; load order preservado. Quando um bem
está escasso e não há candidato, mostra quantidade de estados com produtor e
sete motivos principais disjuntos, da última leitura. Cada produtor estadual
entra no primeiro motivo aplicável: expansão pendente/enfileirada, incorporação,
nível/ocupação, contratação, insumos, método ativo e permissão. Não acrescenta
ações nem altera guardas. 57 testes passam, incluindo todos os bens, cascata,
reset e visibilidade; validação estática contra o jogo local passou.
As capturas enviadas pelo jogador mostram Império Otomano em 13 e 18/06/1839:
modo Automático e mensagem de filas ocupadas renderizados; última leitura
6/1839, 45 projetos públicos/2 privados, infraestrutura negativa zero, dois
setores de construção não operantes e ferro escasso sem produtor elegível.
Isso confirma apresentação do bloqueio, não inclusão de obra ou revisão neste
dia específico. Modo sob solicitação estava selecionado. Não iniciar teste
gráfico prolongado. Detalhamento novo e inclusão real seguem pendentes.

Continuação em 2026-11-09: a suíte foi retomada e os **51 testes passaram**.
O harness agora modela mercado/bens ausentes, métodos ativos, existência de
estado elegível e registro de eventos agendados. Foram atualizados cenários
históricos que ainda exigiam pausa/saldo positivo e ignoravam as oito marcas
estaduais de oferta. Novos cenários cobrem exclusividade dos modos, agendamento
sem duplicata, razões de bloqueio, máximo de uma ação com revalidação da fila,
e elegibilidade/expansão sem duplicata dos oito produtores. Esses resultados
são simulação dos scripts gerados, não confirmação da engine. Nenhum arquivo
carregável ou instalação foi alterado. Os números e regras das seções abaixo
são históricos; a conferência da revisão mensal em campanha segue pendente.

Fase anterior: protótipo da Fase 2 em 0.3.4. O jogador confirmou em campanha a
interface, os indicadores e a seção vazia de oportunidades. A 0.2.0 acrescentou
até três recomendações ferroviárias e um botão para aprovar uma por vez; a
0.2.1 explica se não há déficit de infraestrutura ou se há déficit sem
candidato elegível. A 0.3.0 acrescenta uma ação de capacidade de construção:
quando a fila pública tem pelo menos três projetos, mostra no máximo um setor
de construção operante no estado mais populoso e permite enfileirar um nível
após revalidação. A 0.3.1 acrescenta a decomposição dos motivos de rejeição por
estado quando não há candidato; a 0.3.2 mostra sob o botão a primeira
guarda que falha quando ele está bloqueado; a 0.3.3 explica quando um cartão
antigo deixou de passar os filtros ou já foi enfileirado. Em 0.3.4, saldo
semanal negativo é um alerta, não uma trava, e ação já enfileirada tem mensagem
própria. A execução dos botões e a coexistência com mods ainda não foram
validadas. Não há automação periódica. A versão 0.3.4 está instalada localmente.
A suíte reportou 46 testes para os dois fluxos existentes; ela não cobre as
mensagens novas nem a remoção da trava de saldo, e não foi executada nesta
alteração. Na captura mais recente do Haiti (11/01/1836), o saldo era -£4,27K,
reservas £0, dívida £268K de crédito £850K, 2 estados, nenhum com déficit de
infraestrutura, fila pública/privada 0/0 e capacidade 10. Como não há déficit de
infraestrutura nem fila pública de três projetos, os dois protótipos atuais
continuam sem candidato; remover a trava financeira não cria candidatos por si
só. Próxima prioridade: pesquisar um tipo de recomendação aplicável ao Haiti,
usando escassez específica de bens, mercado, produção e emprego sem presumir que
o contador agregado de escassez indica qual prédio construir. Em
2026-11-08, o jogador enviou capturas das seções vazias em campanha
(0.3.0 e 0.3.1, Império Otomano, 1/1836): estados vazios corretos nas duas
seções e, na 0.3.1, a linha de motivos corretamente oculta sem déficit/fila
suficiente. Depois, o jogador confirmou atualização (inclusive sob
solicitação) e desativação na engine: os botões clicáveis somem ao
ao desativar. Em leitura posterior, a seção de construção
renderizou o candidato Baixo Egito com o botão de aprovar, e a variação
mensal de PIB funcionou (6,4%). O jogador clicou no botão e nada
aconteceu: o tooltip mostrava o botão Bloqueado, e a fila privada tinha
2 projetos, satisfazendo corretamente a trava da fila privada. Para
confirmar a aprovação, será preciso fila privada vazia. Execução com
clique permitido, linha de motivos com déficit presente, recarga e
coexistência seguem pendentes.

Atualização histórica: a continuação conseguiu entrar na França com
Gamescope headless/DXVK e confirmou ativação por decisão, abertura/rolagem do
diário, atualização manual, agenda sob solicitação e congelamento das leituras
ao avançar de janeiro para fevereiro. PIB, SoL e alfabetização corresponderam
à barra do jogo; saldo observado e previsão da GUI diferiram (RESEARCH/RUNTIME
devem preservar essa distinção). Os demais testes interativos ainda estão
pendentes. O jogador reclamou da demora dos testes ocultos e preferiu abrir
o jogo pessoalmente: não voltar a iniciar testes gráficos prolongados sem
necessidade ou novo pedido. A sessão oculta foi encerrada.

A versão 0.1.0 foi então instalada em `mod/Smart Economy Director` no prefixo
Wine já identificado e adicionada ao final de `content_load.json`, preservando
as dez entradas anteriores. Backup:
`sed_backups/content_load_20261108_222107_956307.json`, nos dados do usuário.
O jogador enviou captura do jogo normal com o diário aberto e os indicadores
visíveis em 27/02/1846; a instalação, ativação e renderização estão confirmadas.
Ainda faltam limpeza/desativação, save/reload e teste dos demais mods em conjunto.

Observação do jogador em 2026-11-08: o diário e os indicadores apareceram na
campanha. Direção de produto confirmada: este projeto deve permitir executar,
por botões, recomendações econômicas dentro do escopo do briefing. O jogador
mantém o Smart Government Advisor separado e prefere que ele apenas recomende
leis. Não confundir aprovação de ações econômicas do Director com alterar leis,
nem tratar os botões de agenda/atualização da 0.1.0 como execução econômica.
Planejamento e ações continuam por fases: cada ação precisa de escopo,
viabilidade técnica, explicação, confirmação por clique e revalidação antes de
executar; automação em segundo plano só entra depois das proteções e pesquisas
previstas no briefing.

RESEARCH.md contém fontes e lacunas; ARCHITECTURE.md descreve propostas, não
funções concluídas. COMPATIBILITY.md diferencia instalação, habilitação no
launcher e automação ativa no país. SOURCE_INVENTORY.json registra commit da
referência, hash do briefing e exemplos com linhas para reproduzir buscas.

O ambiente real é Linux com instalação Windows via Hydra/Wine. Não alterar
instalação, saves ou load order na pesquisa. O Economy Advisor correto é
3778129206, já possui construção e PMs. Kuromi não aparece habilitado; ARoAI sim.
Não usar o nome OGAS como sinônimo do Advisor.

Continuação local: METRICS.md registra a matriz por indicador/GUI;
LOCAL_AUDIT.md e ENVIRONMENT_AUDIT.json registram o exame do Kuromi 8.0,
redefinições e nomes históricos do save. A ferramenta de pesquisa
`tools/audit_environment.py` tem nove testes aprovados e não é código do mod.
ARoAI redefine 18 PMs e pode construir para o jogador sob configuração.
Não copiar modelos aproximados de mão de obra/salários do Advisor como medidas.

Continuação Fase 2: `tools/build_economy_data.py` cria um índice local de
building/PM/PMG com proveniência por camada, sem resolver merge. Foi gerado em
`data/economy_catalog.local.json` (ignorado pelo Git): 122 buildings, 450 PMs,
203 grupos, 67 IDs em mais de uma camada e 0 erros de parsing. As sobreposições
incluem CPC em 48 buildings, Government Administration Auto Expand em um e
ARoAI em 18 PMs; o arquivo local não é fonte efetiva para recomendações.
Próximo: usar o relatório para escolher dados/candidatos cuja semântica final
possa ser confirmada no jogo e expor incertezas.

Fontes da implementação: `data/metrics.json` e `tools/build_mod.py`. Não editar
à mão os arquivos gerados em common/gui/localization e descritores. O schema
atual é 1, ativação sempre explícita por decisão. Só o dispatcher atualiza
mensalmente; a Journal Entry não tem segundo pulso. Desativar limpa tudo, menos
schema. A agenda pode ser mensal ou sob solicitação; não há modos de execução
econômica. O histórico mantém duas amostras-base mensais de PIB e leitura atual.

Comandos de desenvolvimento permanecem: `python3 tools/build_mod.py --check`,
`python3 tools/validate.py --game "/caminho/Victoria 3/game"`,
`python3 -m unittest discover -s tests -v`, `python3 tools/package_mod.py`.
**46 testes passam** (nove de auditoria e 37 da implementação). O
interpretador de testes modela escopos de país/estado/edifício, listas,
ordenação e construção simulada, cobrindo filtros, ranking, mensagens de estado
vazio, contagens disjuntas de rejeição, linhas de motivo do botão bloqueado,
travas, confirmação/rejeição de fila e limpeza dos dois fluxos. Ele não
confirma primitivas, datamodel nem GUI na engine.

Próximos passos: pedir ao jogador uma conferência breve dos dois botões e das
linhas explicativas, em cópia de save, com o jogo pausado, seguindo os checklists
da 0.3.0–0.3.4 em MANUAL_RUNTIME_TEST.md. Registrar se os estados aparecem, se
as travas desabilitam os botões e se a fila pública ganha um único nível em
cada tipo. Conferir também a linha de motivo sob o botão bloqueado. Não iniciar
testes gráficos ocultos prolongados. Depois
verificar desativação, recarga e coexistência antes de ampliar os tipos de ação.
O comportamento real das pendências é: a marca permanece enquanto a expansão
está enfileirada e some quando ela é concluída ou cancelada.


Houve teste de inicialização isolado em Xvfb/Wine, descrito em RUNTIME_SMOKE.md:
o mod foi reconhecido e chegou ao menu sem erros próprios na execução limpa.
O save Haiti exige uma regra do Auto-Diplomacy ausente no teste só com Director.
A campanha nova chegou à seleção da França e início da transição, mas a tela
virtual em 1–2 FPS impediu validar o diário. Não apresentar esses resultados
como teste de métricas, botões, desempenho de campanha ou compatibilidade.
Os 26 testes de leis da referência passaram localmente, mas seu validador
completo encontrou 178 erros de pesquisa tecnológica. Não corrigir o outro
projeto no escopo do Director. Validação documental não comprova script aceito
pela engine.

A etapa anterior na nuvem executou 26 testes da referência com sucesso; o
validador não localizou o jogo naquele executor. O registro histórico foi
preservado em PHASE_LOG.md e RESEARCH_CLOUD.md. LOCAL_CODEX.md mantém as
instruções de transição originais; seus caminhos já foram confirmados aqui.

Instalação local 0.5.4: jogo fechado, backup `mod_0.5.3_20261109_122756_131472`, 13 arquivos conferidos com o pacote; configuração de carregamento preservada.

Conferência final da 0.6.0 inclui ocultação das listas vazias do plano,
115 testes aprovados e reinstalação dos 13 outputs com jogo fechado.
Backup dessa conferência em
`sed_backups/mod_before_0.6.0_20261109_220620_787220`.
O backup inicial `mod_before_0.6.0_20261109_220347_442062` conserva a 0.5.8.
