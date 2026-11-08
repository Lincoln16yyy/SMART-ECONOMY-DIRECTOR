# Plano de validação dentro do jogo

**Planejado; nenhum cenário executado.** Ainda não há mod instalável do Director. Este roteiro define evidências a coletar quando as fases correspondentes forem implementadas.

## Preparação

Confirmar versão/build efetiva, caminhos reais de jogo e dados do usuário, versões dos mods, ordem e opções ativas. Fazer cópia do save e backup da configuração antes de alterá-la; não substituir a campanha original. Identificar o log da sessão nova para não atribuir erros antigos ao mod.

## Fase 0 e 1: leitura e ciclo de vida

Comparar cada indicador com a interface nativa na mesma data, país, estado, mercado e unidade. Registrar fonte e divergência. Validar ausentes explicitamente; nenhum ausente pode aparecer como zero.

Abrir JE, atualizar, avançar um mês, desativar e reativar. Verificar data, ausência de JE duplicada, limpeza do estado e ausência de reativação inesperada. Conferir localização pt-BR/inglês, textos longos e logs. Medir tempo das avaliações em país pequeno e grande.

## Fases 2 e 3: prioridades e execução

| Cenário | Comportamento a demonstrar |
| --- | --- |
| Haiti, orçamento limitado | Prioridades viáveis; considerar trabalhadores, insumos e infraestrutura; permitir esperar |
| País rico | Investir com justificativa, evitar excesso e concentração injustificada |
| Crise fiscal | Suspender expansão inadequada e explicar recuperação proposta |
| Escassez de insumos | Considerar a cadeia; não expandir indústria inviável |
| Filas pública e privada existentes | Não duplicar projetos; reconhecer andamento e conclusão |
| Alteração entre recomendar e aprovar | Revalidar ação/estado/custos; rejeitar ação antiga inviável |
| Outro mod executor ativo | Coexistência comprovada ou bloqueio da execução do Director |
| Desativação e save/reload | Não repetir ação pendente nem reativar automaticamente |

Testar separadamente manual, assistido e automático quando existirem. Nenhuma guerra ou decisão diplomática importante pode ser iniciada pelo Director.

## Fases 4 e 5: convivência e campanha longa

Rodar baseline sem execução do Director, combinações relevantes e conjunto completo de mods. Registrar opções e fatores externos. Comparar campanhas de 10, 20 e 30 anos conforme viabilidade: PIB, PIB per capita, padrão de vida, emprego, alfabetização, infraestrutura, saldo, reservas, dívida, preços, produção, filas e diversidade industrial. Medir desempenho e estabilidade também.

Uma comparação isolada não prova causalidade. PIB maior não basta para aprovar o sistema.

## Registro de resultados

Cada execução deve ter commit do Director, versão/build do jogo, mods/opções, cópia de save usada, datas da campanha, ação, esperado, observado, métricas antes/depois, logs relevantes e resultado (passou, falhou, bloqueado ou não executado). Não marcar um cenário como aprovado com apenas carregamento inicial ou validação estática.
