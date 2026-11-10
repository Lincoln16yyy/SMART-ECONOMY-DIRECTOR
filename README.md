# Smart Economy Director — Victoria 3 1.15

Na 0.6.13, o plano inclui avaliação econômico-militar, custos e escassez de
cinco bens militares. A execução de modernização dirigida permanece pendente.
A suíte atual tem 172 testes aprovados; os novos dados aguardam campanha.

A versão 0.6.13 acrescenta planejamento nacional inicial e coordenação de
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

O plano compara infraestrutura e produtores existentes de madeira, ferro,
carvão, cereais, tecido, ferramentas, mantimentos e roupas. Também identifica
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

O pacote fica em `dist/smart-economy-director-0.6.13.zip`. A instalação local
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
