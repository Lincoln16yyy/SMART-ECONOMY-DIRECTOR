# Auxiliar de inspeção das filas — 0.1.0

Ferramenta opcional de teste para fechar as lacunas de
[QUEUE_CONTRACT.md](QUEUE_CONTRACT.md). É um mod separado, chamado
**Smart Economy Queue Probe (test)**, sem dependência do Director habilitado.
O Director principal permanece na 0.4.1. Nenhuma instalação ou opção de campanha
foi alterada para entregar este auxiliar.

## O que implementa

- Ativação explícita por decisão, diário separado e leitura manual.
- Data da amostra; projetos e níveis públicos/privados em linhas distintas.
- Lista de edifícios dos dez tipos usados pelo Director, encontrados nos
  estados atuais do país. Para cada edifício: estado/nome, `level`,
  `level_after_queued_constructions` e diferença sem limitar o resultado a zero.
- Botão de atualizar e limpeza das variáveis próprias ao desativar.
- PT/EN, descritores próprios, pacote determinístico e namespace `sedqp_`.

Não possui on-actions, eventos, comandos de construção, troca de PM,
cancelamento, reordenação ou alteração de impostos/diplomacia. Escreve apenas
as suas próprias variáveis de medição/lista e cria sua própria Journal Entry.
Não altera opções de outros mods nem as guardas do Director.

**Estado: implementado e testado no harness, não verificado na engine.**
`is_building_type` foi conferido nos arquivos vanilla 1.15.0, incluindo
`common/tutorial_lessons/00_tutorial_lessons_market_access.txt:391,418`.
Iteração de buildings, nível após fila, variáveis/listas e padrão da Journal
Entry já têm referências no projeto. O binding de variáveis em Building,
renderização da lista e disponibilidade efetiva de cada prédio continuam
pendentes de confirmação no jogo. Não chamar o auxiliar de reconciliação completa.

## Gerar e localizar

```bash
python3 tools/build_queue_probe.py
```

Resultado local: `dist/smart-economy-queue-probe-0.1.0.zip`.
Também aceita `--output /caminho/probe.zip`. O workflow gera um artefato
**smart-economy-queue-probe**, separado do artefato principal do Director.
O ZIP principal não inclui os scripts do auxiliar.

O comando só grava o ZIP solicitado: não instala, não altera load order,
não abre o jogo e não lê o conteúdo de saves. Nenhum arquivo do jogo ou de
outros mods é incluído. O gerador usa a lista de tipos de prédio do Director,
mas o pacote gerado pode ser carregado separadamente.

## Instalação para um teste futuro

1. Fechar o jogo. Fazer backup da configuração e usar uma cópia de save
   dedicada; não sobrescrever a única campanha ou a cópia SG_TEST.
2. Extrair o pacote em `mod` dos dados do usuário. Deve haver
   `Smart Economy Queue Probe.mod` e `Smart Economy Queue Probe/descriptor.mod`.
   Se já existir outra versão, guardar sua pasta fora de `mod` primeiro.
3. Habilitar o auxiliar pelo launcher. Registrar build, versão do Director,
   mods, ordem e opções. O pacote não edita `content_load.json`.
4. Se o Director ou outro construtor estiver ativo, escolher explicitamente
   quem pode construir no save de teste; o auxiliar não os suspende sozinho.
5. Na campanha de teste, usar **Ativar inspeção de filas (teste)** e abrir o
   novo diário. Ele não inicia obras. Para novas amostras, clicar em
   **Ler filas agora**.

A instalação acima é um procedimento proposto, não executado nesta entrega.
O auxiliar não foi inserido na pasta de mods habitual nem habilitado.

## Conferência curta

Começar por uma obra pública existente, com o jogo pausado. Anotar/capturar:
data, estado, tipo do prédio, nível atual e projeto na fila nativa. Abrir o
diário auxiliar e conferir a linha equivalente. Registrar separadamente
projetos e níveis totais; uma quantidade não substitui a outra.

Em seguida, ainda na cópia, conferir um projeto privado e uma primeira
construção de nível zero, se existirem. Ausência de linha não significa ausência
do projeto: pode indicar que a iteração não expõe esse prédio. Registrar a
lacuna, sem concluir que a fila está vazia. Para cancelamento/conclusão e
save/reload, seguir a matriz de QUEUE_CONTRACT.md com amostras antes/depois.
Comparar logs; em caso de chave crua, linha ausente ou erro, registrar a leitura
como não verificada em vez de assumir zero.

| Campo do registro | Preencher com a observação real |
| --- | --- |
| Build / versões / mods / opções | Não preenchido |
| Data e estado / prédio / lado da fila | Não preenchido |
| Nível atual e após fila: script / tela nativa | Não preenchido |
| Projetos e níveis públicos/privados | Não preenchido |
| Prédio nível zero apareceu? | Não verificado |
| Resultado após cancelar/concluir/recarregar | Não verificado |
| Logs novos, arquivo/linha | Não verificado |

O auxiliar lê apenas os dez tipos do Director e não separa público/privado na
**diferença por prédio**. Os totais nacionais cobrem outra população; não se
deve exigir igualdade entre esses totais e a soma das linhas. Também não
identifica investidor, projeto individual ou causa da remoção. Não há atualização
mensal: valores permanecem congelados até outra leitura explícita.

## Remover

Usar **Desativar inspeção** ou a decisão de desativação; o efeito limpa apenas
`sedqp_` nos escopos atuais do país e seus edifícios. Não cancela obras.
Depois que o diário encerrar, salvar a cópia, fechar o jogo, desabilitar no
launcher e remover somente a pasta/descritor do auxiliar. Transferência de
território/destruição de prédio entre amostras pode retirar escopos do alcance
da limpeza; a limpeza não foi testada através desses eventos na engine.

## Verificação automatizada desta entrega

Seis testes em `tests/test_queue_probe.py`, além dos 61 existentes: todos
passaram, total 67. As fixtures exercitam projeções/níveis, prédio nível zero,
atualização/substituição da lista, diferença negativa visível, país não jogador,
limpeza independente, rejeição de mutação e pacote determinístico separado.
Nível zero na fixture não prova que a engine exponha a primeira construção.
O harness não renderiza GUI, não percorre projetos reais e não serializa saves.
