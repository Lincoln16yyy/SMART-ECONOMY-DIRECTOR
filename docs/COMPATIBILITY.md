# Compatibilidade — matriz inicial

Estado: investigação parcial em 2026-11-08. Nenhum teste de convivência foi executado. Nomes e funções esperadas dos mods vêm do briefing do jogador; somente o código do Smart Government foi inspecionado.

| Mod | Controle comprovado ou ainda a investigar | Risco a verificar | Estratégia proposta |
| --- | --- | --- | --- |
| Smart Government | Código inspecionado: recomenda leis; inicia promulgação por ação do jogador; ciclo mensal e namespace `sg_` | Mudança de lei altera premissas econômicas; custo combinado dos ciclos | `sed_` independente; recalcular sem alterar leis ou variáveis do Government |
| Economy Advisor | Arquivos ausentes; referência anterior identifica workshop `3778129206` | Duplicação de diagnóstico, construção e eventual controle econômico | Inspecionar opções realmente ativas, efeitos e fila antes de escolher quem executa |
| Supply Chain Semi-Auto Builder | Construção/cadeias informadas pelo jogador; implementação não inspecionada | Projetos duplicados e disputa da fila | Enquanto coexistência não for comprovada, Director sem escrita na fila |
| Auto-Apply PMs | Aplicação de PMs informada; implementação não inspecionada | Mudança de insumos e rentabilidade após avaliação | Não implementar troca própria; revalidar condições após mudança |
| Auto-Apply Automation PMs | Automação de PMs informada; implementação não inspecionada | Desemprego, nova demanda de insumos e alteração de contratação | Investigar critérios e frequência; manter execução própria desabilitada |
| Auto-Diplomacy and Advanced Subject Management | Diplomacia/súditos informados; implementação não inspecionada | Alterações de mercado e comércio invalidam planos | Ler efeitos disponíveis, sem assumir diplomacia |
| Auto-Recruit & One-Click Recruit Commanders | Automação militar informada; implementação não inspecionada | Custos e demanda militar tornam investimento inviável | Revalidar capacidade fiscal sem financiar expansão militar por iniciativa do Director |
| Kuromi's AI | Escopo desconhecido | Possível alteração de IA, economia, preços ou on-actions | Examinar arquivos e configuração; não presumir controle do país jogador |

## Inspeção necessária por mod

Registrar versão/ID, origem, hash dos arquivos relevantes, diretórios sobrescritos, dependências, load order e opções efetivamente habilitadas. Mapear JE, decisões, eventos, on-actions, SGUIs, triggers, effects, values, PMs, variáveis, frequência de avaliação e todas as escritas em construção e economia.

Comparar caminhos e identificadores para colisões; arquivo com nome diferente não comprova ausência de conflito comportamental. Examinar escopos e efeito final. Prefixos diferentes não impedem dois mods de enfileirarem o mesmo prédio.

## Limites de integração

Nenhuma API de integração foi identificada. Não chamar efeitos externos nem escrever variáveis de outro mod sem contrato real e teste. Coexistência sem comunicação pode exigir que apenas um mod execute ações por domínio, deixando o Director no diagnóstico/assistido. Detecção de mod e leitura de fila também dependem de mecanismos comprovados; não prometer detecção automática.

Testar baseline, cada par relevante e conjunto completo em cópias de save. Registrar versões, ordem, opções, data inicial/final, fila pública/privada e logs. Se ocorrer duplicação, interromper a execução do Director e investigar antes de reativar. Ver o [plano de testes](MANUAL_RUNTIME_TEST.md).
