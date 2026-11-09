# Inicialização na engine — 0.1.0

Registro histórico: a continuação no topo ocorreu depois da primeira execução
descrita nas seções inferiores. Para o estado atual, consulte a
[auditoria de 09/11/2026](AUDIT_2026-11-09.md); nenhuma nova sessão de jogo foi
realizada durante a auditoria e estes resultados não certificam a 0.4.1.


**Atualização da continuação:** o uso de Gamescope headless com DXVK nativo
permitiu entrar numa campanha nova da França. Foram confirmados a decisão de
ativação, criação e abertura do diário, atualização manual, alteração da agenda
para leitura sob solicitação e manutenção das leituras de janeiro ao avançar
até 16 de fevereiro. A atualização manual em fevereiro mostrou PIB de £21,2M,
SoL 11,2 e alfabetização 48,3%, correspondentes aos indicadores exibidos pelo
jogo. A variação acumulada de PIB foi 4,1%, com distância de um mês de calendário
entre as bases. Rolagem e leitura da parte inferior do widget foram conferidas.

O saldo do script é uma leitura observada e diferiu da previsão do orçamento:
em 16 de fevereiro, £−4,71K no diagnóstico e £−4,68K na barra. A diferença inicial
em 1 de janeiro foi maior. Não equiparar a leitura ao valor previsto da GUI sem
investigar essa semântica. Não foi alterada a fórmula com base nessa diferença.

A sessão oculta foi encerrada após o jogador preferir realizar a conferência
diretamente. Não houve confirmação completa de desativação/reativação,
salvar/recarregar, ciclo mensal retomado ou convivência do conjunto completo.
Esses pontos permanecem pendentes. As limitações abaixo descrevem a primeira
execução, anterior a essa continuação.

Data: 2026-11-08. Executável local: Victoria 3 1.15.0,
build `6338547985dbc271523e149f362a6fd93dc62975`.

## Isolamento do teste

O jogo foi iniciado em tela virtual Xvfb, pelo Wine, com `-debug_mode` e
`-userdir` apontando para dados temporários em `/tmp`. Essa opção foi confirmada
pelos arquivos e logs criados no destino temporário. O `content_load.json`
temporário habilitou apenas o Director diretamente do checkout.

Nenhum mod foi instalado na pasta habitual e nenhum save original ou load order
habitual foi alterado. Uma cópia do Haiti e uma cópia de cache gráfico foram
usadas somente em `/tmp`. Não foram publicadas no repositório.

## Resultados observados

1. A primeira tentativa parou em erros do compilador de shaders do Wine, antes
   de chegar à leitura completa dos scripts. Foi usada a DLL de compilação
   já fornecida pelo jogo, por override de processo `d3dcompiler_47=n`.
   Não foi baixado ou instalado um compilador diferente.
2. Com o compilador nativo e cache gráfico temporário, a engine chegou ao
   menu principal. O log reconheceu `Smart Economy Director` com ID
   `sed.smart_economy_director` e correspondência com Victoria 3 1.15.0.
3. A leitura inicial apontou um aviso de `sed_schema_version` definido sem
   leitura. O enable passou a consultar a existência do marcador antes de
   criá-lo. A correção foi regenerada, testada e verificada numa inicialização
   limpa; o aviso não voltou nessa inicialização.
4. Na inicialização limpa, não foram encontrados erros de scripts,
   localização ou GUI atribuídos aos arquivos do Director no `error.log`.
   Existem erros do conteúdo base, incluindo localização de tooltips de bens,
   monumentos, escape de texto em português e conquistas. Eles não foram
   removidos ou atribuídos ao Director.
5. A cópia `sed_haiti_test.v3` não carregou com apenas o Director: a engine
   recusou a regra `zw_rule_adnasm_advanced_subject_management_on`, gravada
   pelo ecossistema anterior e ausente nesse conjunto de teste. Isso exige
   repetir com as dependências originais; não comprova falha ou compatibilidade
   do Director com aquele save.
6. Foi aberta a seleção de objetivo Sandbox e selecionada a França em uma
   campanha nova. O início avançou para a transição de mapa. A tela virtual
   apresentou aproximadamente 1–2 FPS e não permitiu concluir de forma
   confiável a abertura da Journal Entry. O teste foi encerrado pelo processo
   de teste, preservando os dados do usuário.

Os registros locais dessa execução ficam em
`/tmp/sed-runtime-ds73tnj_/logs`. Esses arquivos temporários não são necessários
para instalar o mod e podem desaparecer ao reiniciar a máquina.

## Limite da primeira execução — antes da continuação descrita no topo

**Confirmado:** descoberta do mod, correspondência de versão, inicialização
até o menu e ausência de erros próprios de carregamento identificados na
execução limpa. A suíte automatizada da 0.1.0 (24 testes) passava; a suíte
atual, já ampliada para as ações 0.2.1 e 0.3.0, tem 40 testes aprovados, e a
validação estática também passa.

**Não confirmado:** ativação por decisão numa campanha, renderização do widget,
correspondência dos números com as telas, atualização mensal, limpeza observada
na engine, salvar/recarregar e coexistência com os demais mods. O interpretador
dos testes cobre as regras dos scripts, mas não substitui essas interações.

A versão 0.1.0 deve ser apresentada como implementação inicial para testes,
sem declarar encerrada a validação funcional da Fase 1. Próximo roteiro:
[MANUAL_RUNTIME_TEST.md](MANUAL_RUNTIME_TEST.md).
