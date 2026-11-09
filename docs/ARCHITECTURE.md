# Arquitetura por fases

A Fase 1 de diagnóstico foi confirmada em campanha na 0.1.0; ver
[PHASE1.md](PHASE1.md). A 0.2.0 começa a Fase 2 com até três candidatos
ferroviários e uma aprovação individual que enfileira uma expansão elegível.
Ranking nacional completo, outros tipos de ação e automação periódica continuam
por implementar.

## Responsabilidade

O Director estabelece objetivos e prioridades nacionais. O primeiro executor
econômico é limitado a uma ação explícita por clique. Usa namespace `sed_`, funciona sozinho
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
| Execução inicial | `sed_run_railway_approval` | Uma expansão ferroviária pública, aprovada e revalidada; sem tentativa automática |
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
operantes em estados incorporados com infraestrutura abaixo de zero. Exige jogo
pausado, ausência de inadimplência, saldo semanal não negativo e fila privada
vazia; confere o nível ferroviário já enfileirado e a elegibilidade normal do
jogo no clique. Mesmo com essas travas, custo e retorno não são previstos. O
pedido cria um único nível na fila pública e sua inclusão é conferida pelo
contador de níveis públicos.

O modo automático futuro só habilitará domínios cujo executor seja o Director.
Uma aprovação manual não habilita sozinha ações periódicas. Quando outro mod
construir, o Director apresentará estratégia e verificará os resultados. Essa
cooperação é configuração do jogador, não API inventada. O Director não
escreverá flags de terceiros nem tentará desligá-los silenciosamente.

## Modos, ciclo e histórico

- Manual: diagnóstico e recomendações sob solicitação ou mensal; ação somente
  após o clique individual em uma recomendação.
- Assistido: análise periódica e aprovação individual de candidatos revalidados.
- Automático: apenas ações comprovadas, com limites, registro e suspensão em crise.

Esses são os futuros modos de execução. A versão 0.1.0 oferece somente agenda
de leitura mensal ou sob solicitação; não usa esses nomes para sugerir modos
de execução que ainda não existem.

A atualização deverá ter um único responsável para evitar execução em dobro
entre Journal Entry e on-action. Rotinas pesadas serão espaçadas e medidas;
não copiar o dia usado por outro mod como garantia de ausência de conflito.
Desativar limpa estado transitório, mantém somente marcador de versão/opt-out
documentado e não cancela construções já iniciadas pelo jogo.

Histórico será limitado, com amostras datadas de indicadores e resultado das
ações. Comparar antes/depois sem atribuir automaticamente a evolução ao Director.
Uma futura integração com Nation Controller exigirá contrato versionado;
nenhum controlador nacional será implementado agora.
