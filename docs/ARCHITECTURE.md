# Arquitetura por fases

Atualização 0.5.3: há uma guarda persistente de uma tentativa automática por
mês, não uma reconciliação de projetos. Desativar remove runtime e conserva
schema + sed_auto_last_attempt_month quando existente, impedindo reinício
do limite por reativação. A política inclui tentativas sem confirmação;
Assistido mantém aprovação explícita. O mês corrente é lido diretamente, sem
depender da amostra do diagnóstico. Essa exceção de segurança substitui, para
a versão atual, descrições históricas de limpeza conservando somente schema.


Estado autoritativo em 09/11/2026: [auditoria](AUDIT_2026-11-09.md). O fluxo
estratégico desta proposta não está integralmente implementado: faltam objetivos,
ranking nacional, proteção fiscal incremental e reconciliação por projeto.
Atualmente existem filtros locais e executor experimental com modos. Ignorar/
restaurar foi acrescentado na 0.4.1, sem validação de cliques/persistência na engine.


A Fase 1 de diagnóstico foi confirmada em campanha na 0.1.0; ver
[PHASE1.md](PHASE1.md). A 0.2.0 começou a Fase 2 com até três candidatos
ferroviários e uma aprovação individual que enfileira uma expansão elegível. A
0.3.0 acrescenta uma segunda ação aprovada para ampliar um setor de construção
quando a fila pública tem pelo menos três projetos; a 0.3.1 explica os motivos de
rejeição quando não há candidato; a 0.3.2 mostra por que o botão de aprovação
está bloqueado; a 0.3.3 explica quando um cartão visível deixou de ser elegível
desde a última leitura; a 0.3.5 acrescenta expansão de produtores locais para
oito bens em escassez. A 0.3.6 introduz modos visíveis Manual/Assistido/
Automático e um executor mensal opt-in limitado a um nível. A 0.3.7 detalha o
resultado de cada revisão automática e as travas que impedem execução. Ranking
nacional completo e compatibilidade ampliada continuam por implementar.

## Responsabilidade

O objetivo proposto é o Director estabelecer objetivos e prioridades nacionais;
essa camada estratégica ainda não foi implementada. As ações em modo
Assistido exigem clique individual; o modo Automático pode enfileirar no máximo
um nível por revisão mensal. Usa namespace `sed_`, funciona sozinho
e não dependerá do Smart Government ou de identificadores internos de outro mod.
O jogador conserva decisões políticas, diplomáticas e militares importantes.

## Fluxo de dados

1. Coletar indicadores comprovados no escopo correto, com data e disponibilidade.
2. Classificar situação fiscal e gargalos; dados ausentes permanecem ausentes.
3. Formar candidatos por estado e tipo, usando recursos e tecnologias reais.
4. Aplicar restrições de emprego, insumos, infraestrutura, orçamento e fila.
5. Ordenar apenas candidatos viáveis e explicar até três prioridades.
6. Revalidar o candidato no clique ou antes da execução. Uma recomendação
   antiga não autoriza construir quando as condições já mudaram.
7. Registrar a intenção e observar conclusão, contratação e efeitos posteriores.

Uma recomendação econômica deverá ter um botão de aprovação que execute uma
ação real e identificada. No clique, o Director recalcula elegibilidade e
conflitos; aprovação antiga não deve executar um alvo diferente depois que a
lista mudar. Esse controle é independente dos botões de atualização da 0.1.0.
Leis permanecem fora do executor econômico: o jogador prefere que o Smart
Government Advisor só recomende promulgações.

## Módulos e arquivos previstos

| Camada | Arquivos previstos | Responsabilidade |
| --- | --- | --- |
| Catálogo | `tools/build_economy_data.py`, `data/` | Indexar IDs, grupos, tecnologias e modificadores de buildings/PMs com proveniência e camadas; sem resolver o merge da engine |
| Coleta | `common/script_values/sed_metrics.txt` | Somente primitivas verificadas; unidades e escopos documentados |
| Diagnóstico | `common/scripted_effects/sed_diagnostics.txt` | Indicadores, disponibilidade, data e estado econômico |
| Ciclo de vida | `common/on_actions/sed_on_actions.txt`, efeitos e decisões próprios | Ativação, migração e limpeza com marcador de schema |
| Planejamento | Valores e efeitos `sed_` separados | Objetivos, filtros, ranking e motivos de rejeição |
| Interface | Journal Entry, scripted GUIs e widget `sed_` | Situação, estratégia, três recomendações e ações efetivas |
| Execução inicial | `sed_run_railway_approval`, `sed_run_construction_approval` | Uma expansão pública aprovada e revalidada por clique; sem tentativa automática |
| Localização | `localization/braz_por/`, `localization/english/` | Português escrito de fato e fallback inglês; UTF-8 BOM |
| Verificação | `tests/`, `tools/validate.py` | Cenários e referências cruzadas; runtime separado |

Os caminhos de catálogo e planejamento são propostas; não há arquivos vazios
para simulá-los. O diagnóstico atual usa `data/metrics.json`, o gerador
`tools/build_mod.py` e `common/scripted_effects/sed_effects.txt`, sem camada de
script values desnecessária para apenas copiar as leituras identificadas.
`tools/audit_environment.py` já existe como ferramenta de pesquisa, sem scripts
de jogo. A auditoria encontrou PMs redefinidos pelo ARoAI e regras de construção
injetadas pelo Controllable Private Construction. O catálogo futuro precisa
registrar origem e versão dos dados, detectar sobreposição e recusar projeção
com catálogo incompatível. Ler só vanilla não reproduz o ecossistema ativo.
`tools/build_economy_data.py` agora produz esse índice local para buildings,
PMs e grupos de PM. Ele mantém cada definição em camada separada; não chama o
relatório de “catálogo efetivo” enquanto as operações de merge não forem
reproduzidas ou confirmadas no motor.

## Priorização e segurança

Aplicar restrições antes de somar benefícios. Uma fábrica sem insumos ou sem
trabalhadores não se torna segura por receber muitos pontos estratégicos.
O ranking deve separar: urgência do gargalo; ganho nacional mensurável;
contribuição ao objetivo; custo de construção e manutenção; risco de excesso.
Pesos e normalização dependem das métricas verificadas e de cenários comparáveis.
Nenhuma fórmula foi calibrada nesta fase; não apresentar retorno previsto em
libras sem modelo validado. Usar desempate determinístico por ID de candidato.

Limites fiscais devem ser relativos: cobertura das despesas em semanas, saldo
operacional, dívida/crédito e custo incremental. Definir limiares a partir dos
testes Haiti/país rico/crise, incluindo receita zero e crédito zero. Diferenciar
expansão saudável, cautelosa, estagnação, crise fiscal e emergência, mostrando
quais critérios levaram à classificação. Não construir é um resultado válido.

## Fila e coexistência

Uma ação será identificada por estado, edifício e objetivo. Consultar fila
pública e privada antes de recomendar e novamente antes de executar. Guardar
intenção pendente e aguardar conclusão e estabilização antes de repetir.
Um cooldown isolado não evita duplicação de projetos privados ou de outros mods.
Se essa consulta não for confiável, a construção automática permanecerá bloqueada.

Na 0.2.0, o primeiro recorte considera apenas ferrovias já existentes e
operantes em estados incorporados com infraestrutura abaixo de zero. Na implementação atual exige modo Assistido, ausência de inadimplência e fila privada vazia; confere o nível
ferroviário já enfileirado e a elegibilidade normal do jogo no clique. Saldo
semanal negativo gera um alerta junto ao candidato, mas não bloqueia a aprovação.
Mesmo com essas travas, custo e retorno não são previstos. O
pedido cria um único nível na fila pública e sua inclusão é conferida pelo
contador de níveis públicos.

Na 0.3.0, a segunda ação só aparece quando a fila pública tem pelo menos três
projetos. Entre os setores de construção operantes, sem falta de insumos, sem
falha de contratação e sem expansão enfileirada, o Director mostra o estado mais
populoso. A aprovação repete as travas fiscais e de fila, enfileira um único
nível e confere o mesmo contador público. Saldo semanal negativo é alerta, não
bloqueio. O recorte não calcula custo, prazo nem
garante que o novo nível será contratado; a localização no estado mais populoso
não é uma projeção de retorno.

Na 0.3.1, quando nenhum candidato passa pelos filtros, o painel decompõe os
estados por motivo principal. Para ferrovias, o total de estados com
infraestrutura negativa é dividido em sem ferrovia, ferrovia não operante
(nível, ocupação, insumos, contratação ou expansão já enfileirada) e bloqueados
por incorporação ou permissão de construção. Para capacidade de construção, o
total de estados com setor é dividido em setor não operante e bloqueados. As
categorias são exclusivas: cada estado entra em um único motivo, e as contagens
somam o denominador exibido. A decomposição descreve filtros atuais, não uma
previsão de custo ou retorno.

Na 0.3.6, Automático é opt-in e pode enfileirar no máximo um nível mensal de
ferrovia ou produtor local de bens em escassez. A rotina exige filas pública e
privada vazias, país fora de inadimplência, construção não pausada e ausência
de três flags de construtores conhecidos. A lista de flags não cobre todos os
mods; o modo permanece protótipo. O Director não escreve flags de terceiros.

## Modos, ciclo e histórico

- Manual: diagnóstico e recomendações sob solicitação ou mensal; nenhuma
  aprovação ou execução econômica. Aprovação por clique pertence ao Assistido.
- Assistido: análise periódica e aprovação individual de candidatos revalidados.
- Automático: apenas ações comprovadas, com limites, registro e suspensão em crise.

A 0.3.6 implementa esses três modos: Manual suspende ações, Assistido habilita
aprovação por botões individuais, e Automático agenda uma revisão mensal com
limite de uma construção. O primeiro modo ao ativar um save sem escolha é
Assistido; ativar Automático exige clique explícito.

A atualização deverá ter um único responsável para evitar execução em dobro
entre Journal Entry e on-action. Rotinas pesadas serão espaçadas e medidas;
não copiar o dia usado por outro mod como garantia de ausência de conflito.
Desativar limpa estado transitório, mantém somente marcador de versão/opt-out
documentado e não cancela construções já iniciadas pelo jogo.

Histórico será limitado, com amostras datadas de indicadores e resultado das
ações. Comparar antes/depois sem atribuir automaticamente a evolução ao Director.
Uma futura integração com Nation Controller exigirá contrato versionado;
nenhum controlador nacional será implementado agora.

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
