# Fase 1 — diagnóstico econômico 0.1.0

Implementação iniciada em 2026-11-08 por pedido explícito do jogador.
As lacunas da pesquisa sobre automação, fila detalhada e coexistência permanecem
documentadas. Elas não foram convertidas em permissões de executar ações.

## Implementado

- Journal Entry própria com widget, decisões de ativação/desativação e SGUIs.
- Ativação explícita para jogadores; nenhum auto-enable em novo jogo ou save.
- Um único dispatcher mensal aditivo; o diário não repete o mesmo trabalho.
- Atualização imediata e alternância entre leituras mensais e sob solicitação.
- Treze leituras nacionais com fontes registradas em `data/metrics.json`.
- PIB per capita, dívida/crédito e reserva/déficit com guardas de denominador.
- Contagens de estados com déficit de infraestrutura/acesso incompleto e
  edifícios ativos com insumos em falta, contratação incompleta ou falhas de
  contratação. Não há estimativa inventada de desemprego ou qualificações.
- Mensagens factuais de inadimplência e saldo negativo; saldo não negativo
  não é apresentado como diagnóstico de economia saudável.
- Histórico limitado de PIB: duas amostras-base datadas e leitura atual.
  A primeira leitura de cada mês registrado é a âncora. Repetições no mesmo mês
  não avançam a âncora. A variação informa a distância entre os meses de
  calendário amostrados, inclusive quando atravessa um ano ou há meses sem
  leitura. Isso não equivale à duração exata entre amostras ou a uma taxa mensal.
- Localização escrita em português brasileiro e inglês, metadados 1.15.* e
  pacote para instalação manual sem Workshop.

Não há pontuação de investimentos, três prioridades, aprovação/ignorar,
execução de construções ou PMs, modos de execução econômica ou integração por
API. Nenhum botão sugere uma ação inexistente.

## Organização e geração

`tools/build_mod.py` gera os scripts de `common/`, o widget, localizações e
descritores. Alterações nas fontes de métricas pertencem a `data/metrics.json`;
mudanças de ciclo de vida, interface e traduções pertencem ao gerador. Rode
`python3 tools/build_mod.py` depois de editar. `--check` verifica sem escrever.

`runtime_variables()` é o inventário de limpeza. A desativação remove todos
os indicadores, opções de atualização e histórico, conservando o schema.
Nenhuma variável de outro mod é alterada. O pacote usa o ícone de PIB existente
no jogo e não redistribui imagens ou fontes proprietárias.

## Verificação automatizada

`tools/validate.py` verifica geração atualizada, estrutura dos scripts,
referências próprias, localização, BOM, limpeza e o limite de ações da Fase 1.
Ele aceita `--game` para verificar a existência do ícone e caminhos que
sobrescreveriam arquivos originais. Não substitui os parsers da engine.

Os testes comportamentais executam os scripts gerados em um interpretador
restrito com leituras fornecidas pelo teste. Verificam crescimento, divisões
por zero, escalas de orçamento, contagens, atualização mensal/manual, limpeza,
estado desativado e pacote. Esse interpretador não valida nomes de primitivas,
semântica de listas da engine ou renderização. Não é um simulador econômico.

Comandos:

```bash
python3 tools/build_mod.py --check
python3 tools/validate.py --game "/caminho/Victoria 3/game"
python3 -m unittest discover -s tests -v
python3 tools/package_mod.py
git diff --check
```

Resultado inicial: **24 testes aprovados**, incluindo os nove de auditoria;
validação estática com a instalação local aprovada; pacote ZIP gerado.
Testes da referência Smart Government não contam como testes do Director.

## Aceitação dentro do jogo

A Fase 1 só será considerada funcionalmente validada após carregar uma cópia
de campanha, ativar a decisão, abrir o diário e comparar os indicadores,
atualizar, trocar a agenda, desativar/reativar e salvar/recarregar, conferindo
os logs. Ver o roteiro específico em MANUAL_RUNTIME_TEST.md.

Não foram alterados saves ou a lista habitual de mods do jogador. A inicialização
em dados de usuário temporários chegou ao menu com o mod reconhecido e sem
erros próprios identificados na execução limpa. A renderização lenta impediu
a validação do diário em campanha. Evidências e a recusa do save antigo por
uma regra de outro mod ausente estão em [RUNTIME_SMOKE.md](RUNTIME_SMOKE.md).
