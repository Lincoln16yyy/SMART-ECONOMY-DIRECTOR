# Arquitetura proposta — sem implementação

## Responsabilidade

O Director estabelece objetivos e prioridades nacionais. A primeira entrega
executável será somente diagnóstico. Usará namespace `sed_`, funcionará sozinho
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

## Módulos e arquivos previstos

| Camada | Arquivos previstos | Responsabilidade |
| --- | --- | --- |
| Catálogo | `tools/build_economy_data.py`, `data/` | Extrair buildings, PMs, bens e custos da instalação informada por argumento |
| Coleta | `common/script_values/sed_metrics.txt` | Somente primitivas verificadas; unidades e escopos documentados |
| Diagnóstico | `common/scripted_effects/sed_diagnostics.txt` | Indicadores, disponibilidade, data e estado econômico |
| Ciclo de vida | `common/on_actions/sed_on_actions.txt`, efeitos e decisões próprios | Ativação, migração e limpeza com marcador de schema |
| Planejamento | Valores e efeitos `sed_` separados | Objetivos, filtros, ranking e motivos de rejeição |
| Interface | Journal Entry, scripted GUIs e widget `sed_` | Situação, estratégia, três recomendações e ações efetivas |
| Execução futura | Efeitos de ações `sed_` | Construção normal, proteções e confirmação da fila |
| Localização | `localization/braz_por/`, `localization/english/` | Português escrito de fato e fallback inglês; UTF-8 BOM |
| Verificação | `tests/`, `tools/validate.py` | Cenários e referências cruzadas; runtime separado |

Esses caminhos são propostas; não foram criados arquivos vazios para simulá-los.

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

O modo automático futuro só habilitará domínios cujo executor seja o Director.
Quando outro mod construir, o Director apresentará estratégia e verificará os
resultados. Essa cooperação é configuração do jogador, não API inventada.
O Director não escreverá flags de terceiros nem tentará desligá-los silenciosamente.

## Modos, ciclo e histórico

- Manual: diagnóstico/recomendações sob solicitação, nenhuma ação econômica.
- Assistido: análise periódica e aprovação individual de candidatos revalidados.
- Automático: apenas ações comprovadas, com limites, registro e suspensão em crise.

A atualização deverá ter um único responsável para evitar execução em dobro
entre Journal Entry e on-action. Rotinas pesadas serão espaçadas e medidas;
não copiar o dia usado por outro mod como garantia de ausência de conflito.
Desativar limpa estado transitório, mantém somente marcador de versão/opt-out
documentado e não cancela construções já iniciadas pelo jogo.

Histórico será limitado, com amostras datadas de indicadores e resultado das
ações. Comparar antes/depois sem atribuir automaticamente a evolução ao Director.
Uma futura integração com Nation Controller exigirá contrato versionado;
nenhum controlador nacional será implementado agora.
