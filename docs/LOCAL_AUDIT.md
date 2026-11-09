# Auditoria local de compatibilidade e saves

Data: 2026-11-08. Ferramenta: `tools/audit_environment.py`.
Resultado estruturado: [ENVIRONMENT_AUDIT.json](ENVIRONMENT_AUDIT.json).
Nenhuma instalação, opção, ordem de carregamento ou campanha foi alterada.

## Resultado da inspeção

Foram encontrados os dez diretórios listados no launcher. A auditoria identifica
blocos de primeiro nível, operações `INJECT`, `INJECT_OR_CREATE`, `TRY_INJECT`
e `REPLACE`, arquivos de mesmo caminho e diferenças de tokens nos campos de PM.
Ela não calcula a resolução final de merge do motor. Identificadores comuns,
especialmente namespaces de defines e on-actions, não são conflitos comprovados.

O único bloco compartilhado encontrado entre os dez mods foi
`on_monthly_pulse_country`: Economy Advisor, ARoAI e Smart Government.
Os dois Advisors usam dispatchers aditivos; ARoAI registra um evento.
Isso exige teste de despacho combinado, não remoção automática de nenhum deles.
Não foram encontrados caminhos idênticos aos arquivos vanilla em `common/`
ou `gui/` nesses mods. Isso não evita alterações de definições por ID.

Seis arquivos vanilla de DNA não passaram pelo leitor estrutural, por chaves
desbalanceadas. Os nomes estão no JSON; eles foram excluídos das comparações
de definições. Isso não é diagnóstico de erro econômico ou validação da engine.

## Alterações que afetam o planejamento econômico

### Controllable Private Construction

Foram identificadas 49 entradas com IDs também existentes no jogo original.
Em `zw_cpc_01_industry.txt`, `INJECT_OR_CREATE:building_food_industry` e os demais
edifícios acrescentam requisitos `can_build_government` e `can_build_private`.
Portanto, recurso natural e tecnologia não bastam para declarar uma construção
permitida. A execução deve consultar as regras atuais do jogo, no estado correto.

### Government Administration Auto Expand

`common/buildings/z0z_government.txt:1` usa
`REPLACE:building_government_administration`. A condição `should_auto_expand`
verifica ocupação igual a 1, déficit de capacidade tributária, ausência de
escassez e acesso ao mercado acima de 0,8. O arquivo também declara grupos
de PM e custo de construção. Não é apenas uma recomendação visual.
O Director deve observar expansões automáticas antes de pedir outra administração.

### ARoAI

O mod habilitado é Anbeeld's Revision of AI, uma identidade distinta do Kuromi.
Foram encontradas 18 redefinições de PM vanilla. O JSON registra quais campos
possuem sequências de tokens diferentes; isso inclui dados econômicos, além
de `ai_value`. A comparação ignora espaços e comentários, mas não prova
equivalência numérica nem identifica sozinha quais diferenças serão aplicadas.

Exemplo verificado nos arquivos: `pm_basic_port` em
`common/production_methods/aroai_government.txt:29` declara 3.000 laborers,
1.500 clerks e 500 bureaucrats por nível, infraestrutura 5 e saída de comboios.
O arquivo local vanilla `common/production_methods/11_private_infrastructure.txt`
declara 700/200/100 empregos, infraestrutura 3 e saída de `merchant_marine`.
Os nomes dos modificadores de insumo também diferem. O Director não pode usar
um perfil vanilla fixo e apresentá-lo como custo observado da campanha.

`common/scripted_triggers/aroai_preparation_triggers.txt` contém a condição
`aroai_is_construction_allowed`: para jogador, requer a regra
`aroai_autobuild_for_players_allowed` e a variável `aroai_autobuild`, além
das outras proteções. Existe uma decisão para abrir suas configurações.
Portanto, pode construir para o jogador quando habilitado dessa forma; a presença
do mod no launcher não demonstra que essa opção esteja ligada.

### Kuromi's AI

O ZIP local informa versão **8.0**, compatibilidade declarada **1.15.*** e ID
`kai.kuromi`. Foram lidos metadata, README, defines e injeções em buildings.
Ele modifica estratégia de IA, pesos de construção e PM, e usa `INJECT` em
administração, universidades e setores de construção. Não foi encontrado
arquivo `common/on_actions/` no pacote examinado.

Não há evidência nessa inspeção de um construtor independente comandando
automaticamente a fila pública do jogador. Existem mudanças em definições e
pesos da IA; o alcance efetivo deve ser confirmado pelo motor. O pacote não
aparece na lista atual do launcher. Se for reativado, compartilha alvos de
administração com Government Administration Auto Expand e o namespace `NAI`
com ARoAI. Isso requer comparar campos e ordem; namespace comum não significa
que todos os seus defines colidam.

## O que o save permite afirmar

`haiti_1836_06_30.v3` é um ZIP com prefixo próprio do jogo. `gamestate` e `meta`
contêm conteúdo binário. Todos os outros saves `.v3` encontrados também têm
gamestate binário, inclusive a cópia de teste Haiti.

O gamestate do Haiti contém o nome Kuromi's AI e uma ocorrência de cada um dos
quatro marcadores examinados do Economy Advisor: habilitação, construção,
automação de mão de obra e balanceamento de PMs. **Isso não determina o valor,
o país dono ou se a variável está ativa.** O relatório registra apenas contagens
e hash, sem publicar os bytes do save.

O autosave atual identifica outra campanha no início do conteúdo, portanto não
foi usado para inferir as opções do Haiti. A lista atual do launcher e a lista
histórica gravada no save precisam ser tratadas separadamente.

Falta uma leitura estruturada por país com decodificador compatível, ou consulta
das opções na interface do jogo. Nenhuma flag foi alterada para contornar isso.

## Fila pública e privada

No Advisor, `advisor_generated_candidate_effects.txt:324–326` percorre edifícios
e calcula `level_after_queued_constructions - level`; converte os níveis em
compromissos de insumos, empregos e infraestrutura. O contador privado também
participa da distribuição da capacidade. Isso comprova a estratégia de leitura
adotada pelo mod, mas não substitui um teste sobre a inclusão de toda a fila.

Pontos a verificar na 1.15: se uma primeira construção já possui escopo de
edifício mesmo com nível zero; se o valor inclui projetos privados e públicos;
como reage a cancelamentos; se reflete imediatamente uma adição de outro mod.
Não há permissão técnica para afirmar que essa primitiva resolva todos os casos.

`advisor_automation_effects.txt:398` também compara os níveis governamentais
antes/depois de despachar a construção. Uma tentativa só conta como sucesso
se a fila crescer. O comentário de confirmação em campanha pertence ao autor
do Advisor; essa sessão não repetiu a confirmação.

## Dados medidos e aproximações

O fator de qualificações em `advisor_generated_profiles.txt:41` é calculado
como `literacy_rate × 0.60 + 0.40`, limitado entre 0,40 e 1. Isso é uma
aproximação do Advisor, não uma leitura direta de qualificações por profissão.
Sua mão de obra disponível usa população × 0,25, desemprego e metade da fração
de camponeses. `advisor_state_wage_unit` também tem fallback e limites.
Esses modelos não devem aparecer no Director com o rótulo de dados observados.

## Testes executados

- Nove testes da ferramenta de auditoria passaram, incluindo comentários,
  strings, operações de injeção, diferenças de PM e recusa em tratar marcadores
  binários como flags ativas.
- Os 26 testes do Smart Government passaram novamente no checkout local.
- O validador completo do Smart Government, agora com o jogo disponível,
  terminou com **exit 1 e 178 erros**, incluindo chaves em
  `sg_research_rank.txt` e chamadas `sg_research_available_*` sem definição.
  São achados no módulo de pesquisa do outro projeto, não falhas introduzidas
  pelo Director. Nenhum arquivo desse projeto foi corrigido nesta tarefa.
- Não houve teste da engine, cliques na Journal Entry, desempenho ou campanha.

## Reproduzir

Exemplo local, com caminhos explícitos; a saída deve ficar fora da instalação
do jogo e dos dados do usuário:

```bash
python3 tools/audit_environment.py \
  --game "/caminho/Victoria 3/game" \
  --user-dir "/caminho/Paradox Interactive/Victoria 3" \
  --kuromi-zip "/caminho/3227982912_Kuromi__x27_s_AI.zip" \
  --save "/caminho/Paradox Interactive/Victoria 3/save games/haiti_1836_06_30.v3" \
  --output docs/ENVIRONMENT_AUDIT.json
python3 -m unittest discover -s tests -v
```

As opções `--save` e `--kuromi-zip` são opcionais. A ferramenta não depende de
Workshop, não extrai arquivos do ZIP para a instalação e não interpreta a
ausência de um mod como ausência de todos os seus efeitos históricos.
