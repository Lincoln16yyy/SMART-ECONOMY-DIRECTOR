# Fase 0 — Pesquisa e diagnóstico parcial

Data: 2026-11-08. **Fase aberta; implementação não iniciada.**

## Resultado técnico

O Smart Government oferece uma base arquitetural para apresentação, ciclo de vida e avaliação mensal. Seu código não comprova acesso completo à economia nem execução de construções. Antes de implementar o Director, é necessário examinar a instalação real 1.15 e os mods do jogador.

O checkout de referência foi estudado no commit `95b20870816b9ceabcaf0b7b9371a66c85dd8bf1`. As conclusões abaixo distinguem código observado, relatos do projeto anterior e hipóteses de arquitetura. Nenhuma ação econômica foi executada no jogo nesta pesquisa.

## Ambiente e fontes

- Repositório do Director: inicialmente apenas documentação.
- Referência clonada separadamente em `/workspace/Smart-Government-Victoria-3-1.15`, sem alterar arquivos rastreados.
- Busca por Victoria/Economy Advisor em `/workspace`, `/home/agent`, `/opt`, `/mnt` e `/media`: não encontrou instalação ou mods, além do próprio checkout de referência e nomes irrelevantes de bibliotecas Python.
- `/home/lincoln-ii` não existe neste executor. Os caminhos dessa máquina descritos no projeto anterior são pistas para uma sessão local, não caminhos válidos na nuvem.
- `docs/AI_CONTEXT.md` da referência relata Victoria 3 `1.15.0 (Ivan-Chai)` e Economy Advisor workshop `3778129206`. Isso não confirma a versão atualmente instalada pelo jogador nem a identidade de uma cópia nova.
- Não foi inspecionado `content_load.json`, save, executável, log ou fonte do Economy Advisor nesta entrega.

Documentos lidos: README, AI_CONTEXT, PHASE_LOG e MANUAL_RUNTIME_TEST. Código estudado: diretórios `common/`, geradores de leis e GUI, parser, instalação, validação, testes, localização e metadados. O checkout também contém artefatos de pesquisa tecnológica, inclusive `.common/scripted_guis/sg_research_sguis.txt`; sua presença não demonstra integração ou funcionamento. O Director não vai assumir controle de pesquisa com base nesses arquivos.

## Padrões comprovados no código da referência

| Área | Evidência | Consequência para o Director |
| --- | --- | --- |
| Inicialização | `common/on_actions/sg_on_actions.txt` usa despachantes aditivos, país jogador e marcador de esquema | Separar inicialização de atualização; nunca reativar após desativação deliberada |
| Journal Entry | `common/journal_entries/sg_journal_entries.txt` liga widget, avaliação, desativação e pulso mensal | Uma JE própria; confirmar os mesmos mecanismos na instalação alvo |
| Estado | `common/scripted_effects/sg_effects.txt` mantém esquema e limpa ranking, datas e ignoradas | `sed_` próprio, migração explícita e inventário de variáveis |
| Identidade | `data/law_ids.json` mantém IDs estáveis; ações geradas vinculadas à lei | Recomendação futura deve identificar ação, edifício e estado, não apenas posição no ranking |
| Revalidação | `sg_law_actions.txt` revalida disponibilidade antes de `start_enactment`, depois recalcula | Uma aprovação antiga não autoriza executar uma oportunidade já inválida |
| Ranking | `sg_law_rank.txt` inicializa sentinelas e contadores; mérito deve superar a lei atual | Aceitar zero recomendações e explicar filtros; não importar pesos de política para economia |
| Pontuação | `tools/build_law_data.py` deriva componentes de modificadores e ajustes situacionais | Mostrar componentes e fontes; validar pesos econômicos separadamente |
| Interface | `tools/build_gui.py` usa SGUI de visibilidade por candidato | Evitar cliques que mudam de alvo após recálculo; custo de muitos ramos exige medição |
| Idioma | `localization/braz_por` e `english`, arquivos com BOM | Português brasileiro e fallback inglês; validar chaves e codificação |
| Instalação | `descriptor.mod`, descritor externo e `.metadata/metadata.json` | Projetar instalação local portátil; não depender do Workshop |
| Diagnóstico | contadores por filtro, data da avaliação e logs condicionais | Diferenciar falta de dados, inviabilidade, ignoradas e ausência de oportunidade |

A referência relata erros reais com `autoresize` em widget, `HasVariable` na GUI, defines sem namespace e listas de grupos de interesse. Esses relatos justificam verificações preventivas, mas não substituem carregar o novo mod no jogo. Há trechos antigos no AI_CONTEXT que ainda citam alternativas corrigidas depois; priorizar o código do commit e o histórico mais recente.

## Capacidades e evidência disponível

Classificações finais exigidas pelo briefing: executável, observável, parcial ou não suportado. **Pendente** abaixo significa que não existe evidência suficiente para atribuir uma dessas classificações; não significa que a engine não suporte o recurso.

| Recurso | Estado nesta pesquisa | Evidência / verificação necessária |
| --- | --- | --- |
| Ativar, desativar, ignorar, restaurar e atualizar JE | Parcial: implementação de referência observada | Código e testes estáticos; repetir interações em campanha para o Director |
| Atualização mensal | Parcial: padrão de referência observado | JE e on-actions; medir custo e confirmar um ciclo por mês |
| Saldo e risco fiscal | Parcial: uso em condições da referência | `net_total_income` e `weeks_until_bankruptcy` em `dynamic_benefit`/`dynamic_risk`; validar semântica, unidades, escopo e leitura numérica |
| Padrão de vida e alfabetização | Parcial: uso em condições da referência | `average_sol`, `average_expected_sol`, `literacy_rate`; validar consulta e exibição na instalação |
| Pressão burocrática | Parcial: condição da referência | `approaching_bureaucracy_shortage`; não equivale a valor monetário de despesa |
| Reservas, dívida, juros e composição das despesas | Pendente | Localizar funções/valores reais; distinguir saldo semanal de estoque e de limite de crédito |
| Preços, ordens de compra/venda, escassez e comércio | Pendente | Investigar mercado nacional/local, unidades e contexto do bem; distinguir preço alto de escassez efetiva |
| Produção, rentabilidade, utilização e salários | Pendente | Determinar leitura por edifício, estado e país; não inferir lucro futuro do preço atual |
| Emprego, desemprego, camponeses, qualificações e migração | Pendente | Distinguir categorias e mobilidade; trabalhador disponível não é contratação garantida |
| Infraestrutura, acesso ao mercado, portos e ferrovias | Pendente | Mapear valores regionais e efeitos concretos na versão alvo |
| PIB, PIB per capita e crescimento | Pendente | Confirmar valores e agregações; crescimento requer histórico comparável |
| Fila pública, privada e construção em andamento | Pendente crítico | Identificar leitura, dono e identidade dos projetos antes de permitir automação |
| Adicionar/priorizar/cancelar construção | Pendente crítico | Efeito real, escopo, limites e coexistência; não usar `start_enactment` como prova de ação econômica |
| Consultar e alterar PMs | Pendente | Inspecionar grupos, métodos e mods de PM; preferir coexistência sem escrita |
| Tecnologia desbloqueada e restrições de edifícios | Pendente | Ler definições e requisitos efetivos; não assumir controle da pesquisa |
| Histórico e adaptação durante campanha | Pendente | Confirmar persistência e custo de amostras; descrever associação, não causalidade ou previsão garantida |

## Arquitetura proposta, ainda não implementada

1. **Catálogo de capacidades:** cada métrica registra fonte, versão, escopo, unidade, disponibilidade, limitações e teste de confirmação. Ausência de valor é desconhecido, nunca zero.
2. **Diagnóstico:** avaliação mensal e manual gera estado fiscal/produtivo com motivos e data. Métricas insuficientes produzem diagnóstico incompleto; não classificam automaticamente a economia como saudável.
3. **Objetivos:** curto/médio/longo prazo e objetivo escolhido pelo jogador. Prioridades não assumem política, guerra ou diplomacia.
4. **Elegibilidade:** filtrar oportunidade por tecnologia, recursos, mão de obra, insumos, infraestrutura, finanças e projetos existentes antes de pontuar. Campo crítico desconhecido bloqueia execução.
5. **Planejamento:** decompor necessidade, benefício e risco; comparar com a opção de esperar. Não fixar fórmula ou limiares antes de conhecer unidades e dados acessíveis. Calibrar com cenários e registrar versões dos pesos.
6. **Apresentação:** até três recomendações, identidade estável, estado alvo, motivos, restrições, componentes e confiança baseada em dados disponíveis. Custos/previsões só aparecem quando calculáveis.
7. **Execução futura:** revalidar modo, identidade, dados atuais, fila e proteções imediatamente antes de agir. Bloquear se outro controlador disputa a fila. Registrar ação pendente e reconciliar com o mundo antes de repetir; cooldown sozinho não comprova conclusão.
8. **Observação posterior:** comparar amostras com mesma unidade e contexto de mercado; registrar mudanças de PM, guerra e comércio como fatores concorrentes. Não prometer aprendizado preditivo sem dados adequados.

Organização prevista: `common/` para ciclo de vida, valores, triggers, GUIs e efeitos `sed_`; `gui/journal_entry_widgets/` para JE; `localization/` para idiomas; `data/` para catálogo e IDs; `tools/` para geração/validação; `tests/` para regras e fixtures; `docs/` para evidência. São destinos planejados, não arquivos fictícios já criados.

Fase 1 terá apenas diagnóstico. Modos assistido e automático só poderão executar ações após a Fase 3; a interface não deve oferecer botões sem implementação real. Propor início manual na primeira versão é uma medida de projeto, sujeita à validação da arquitetura.

## Proteções de projeto a demonstrar

- Sem leitura confiável das filas pública e privada, nenhuma execução automática de construção.
- Nenhuma capacidade econômica suposta a partir do nome de um mod.
- Um controlador por domínio; nenhuma escrita em variáveis `sg_` ou de outros mods.
- Estado fiscal deve considerar despesas recorrentes e escala do país; percentuais e janelas ainda precisam de calibração.
- Desativar remove estado operacional `sed_`, preservando somente marcadores necessários e documentados; não cancela construções já iniciadas sem decisão explícita.
- Desempenho: começar pelo país jogador, evitar varredura diária global, limitar candidatos e medir antes/depois em país pequeno e grande. Frequência mensal é referência, não garantia de custo aceitável.

## Validação executada

No checkout da referência, sem gerar novamente os dados:

```bash
python3 -m unittest discover -s tests -v
# 26 testes executados, 26 passaram.
python3 tools/validate.py
# Exit 1: Could not find Victoria 3 automatically.
```

Os 26 testes verificam artefatos e regras do Smart Government. Não são testes econômicos do Director nem confirmação da engine. A validação dependente dos arquivos originais ficou bloqueada por instalação ausente. Não houve teste de GUI, campanha, compatibilidade ou economia.

## Critério para encerrar a Fase 0

- [x] Estudar documentos e implementação do Smart Government em revisão fixa.
- [x] Propor separação arquitetural e registrar riscos.
- [x] Criar matriz inicial de compatibilidade com lacunas explícitas.
- [ ] Confirmar instalação, versão, caminhos e lista efetiva de mods.
- [ ] Inspecionar Economy Advisor e demais mods instalados.
- [ ] Preencher capacidades com fontes reais 1.15, unidades, escopos e limites.
- [ ] Demonstrar dados mínimos da Fase 1 e definir testes de leitura/exibição.
- [ ] Apresentar diagnóstico consolidado antes de implementar o mod.

Próxima ação: continuar em uma sessão local do Codex no computador do jogador ou disponibilizar privadamente os arquivos necessários. Não publicar arquivos proprietários do jogo ou saves neste repositório.

## Fontes fixadas

- [Contexto e mecanismos relatados](https://github.com/Lincoln16yyy/Smart-Government-Victoria-3-1.15/blob/95b20870816b9ceabcaf0b7b9371a66c85dd8bf1/docs/AI_CONTEXT.md)
- [Histórico e correções de runtime](https://github.com/Lincoln16yyy/Smart-Government-Victoria-3-1.15/blob/95b20870816b9ceabcaf0b7b9371a66c85dd8bf1/docs/PHASE_LOG.md)
- [Procedimento manual](https://github.com/Lincoln16yyy/Smart-Government-Victoria-3-1.15/blob/95b20870816b9ceabcaf0b7b9371a66c85dd8bf1/docs/MANUAL_RUNTIME_TEST.md)
- [Ciclo de vida](https://github.com/Lincoln16yyy/Smart-Government-Victoria-3-1.15/blob/95b20870816b9ceabcaf0b7b9371a66c85dd8bf1/common/scripted_effects/sg_effects.txt)
- [JE](https://github.com/Lincoln16yyy/Smart-Government-Victoria-3-1.15/blob/95b20870816b9ceabcaf0b7b9371a66c85dd8bf1/common/journal_entries/sg_journal_entries.txt)
- [Gerador e sinais econômicos](https://github.com/Lincoln16yyy/Smart-Government-Victoria-3-1.15/blob/95b20870816b9ceabcaf0b7b9371a66c85dd8bf1/tools/build_law_data.py)
- [GUI](https://github.com/Lincoln16yyy/Smart-Government-Victoria-3-1.15/blob/95b20870816b9ceabcaf0b7b9371a66c85dd8bf1/tools/build_gui.py)
- [Validação](https://github.com/Lincoln16yyy/Smart-Government-Victoria-3-1.15/blob/95b20870816b9ceabcaf0b7b9371a66c85dd8bf1/tools/validate.py)
- [Testes executados](https://github.com/Lincoln16yyy/Smart-Government-Victoria-3-1.15/blob/95b20870816b9ceabcaf0b7b9371a66c85dd8bf1/tests/test_advisor_generation.py)
