# Plano de testes de campanha — execução pendente

Há uma primeira implementação executável, versão 0.1.0, somente de diagnóstico.
As interações e cenários em campanha continuam **não executados**. Os testes
automatizados e tentativas de inicialização constam em PHASE1.md; não são
resultados de campanha. Nenhum resultado foi simulado.

## Checklist específico da versão 0.1.0

| Ação | Resultado a conferir dentro do jogo |
| --- | --- |
| Carregar save novo/existente sem ativar | Nenhum diagnóstico ou automação aparece sozinho |
| Decisão Ativar Smart Economy Director | Uma única Journal Entry aparece com leitura inicial e mês/ano |
| Abrir o diário | Textos em português, sem chaves cruas ou números cortados; scroll permite ler todos os controles e indicadores |
| Comparar saldo, reservas, dívida e crédito | Valores correspondem ao país e data; estoque e fluxo semanal não estão confundidos |
| Comparar população, PIB, SoL e alfabetização | Conferir abrangência do indicador, principalmente população incorporada versus total |
| Comparar filas e infraestrutura | Projetos não são tratados como níveis; estados pertencem ao país jogador |
| Atualizar repetidamente no mesmo mês | Leituras mudam conforme o jogo, mas não surge uma falsa variação mensal de PIB |
| Avançar um mês | Uma atualização, sem duplicar diário; crescimento usa a primeira amostra-base do mês anterior registrado |
| Atualizar sob solicitação e avançar meses | Última leitura e indicadores ficam congelados até clicar em atualizar |
| Atualizar todo mês | Leitura imediata; leituras mensais voltam a acontecer |
| Desativar e avançar meses | Diário encerra e não volta sozinho; variáveis operacionais removidas, só schema retido |
| Reativar | Leituras novas; crescimento volta a indisponível até haver outra amostra mensal |
| Salvar e recarregar | Ativação, agenda e amostras pertencem ao país e permanecem coerentes |

Caso o diário esteja inacessível por um problema de interface, a decisão
**Desativar Smart Economy Director** continua sendo a saída de limpeza.

## Preparação

Registrar versão/build, commit do Director, DLCs, mods, ordem e opções de cada
automação. Com o jogo fechado, fazer backup do load order e usar cópia de save,
nunca o único arquivo da campanha. Não sobrescrever a cópia de teste do Smart
Government; preparar uma cópia própria do Haiti para o Director.

Executar primeiro vanilla + Director; depois adicionar os mods e, por fim,
testar o conjunto completo. Comparar logs antes/depois, guardando os novos
erros com arquivo e linha. Nenhum botão pode ser aprovado só por aparecer.

Registrar as flags efetivas no país: Economy Advisor (habilitação, construção,
mão de obra e balanceamento de PM), opções do Supply Chain, Auto-Apply e a
regra/flag de autobuild do ARoAI. O save Haiti encontrado é binário; a ocorrência
do nome de uma variável não comprova seu valor nem seu dono. Conferir as opções
na interface ou usar decodificação estruturada compatível.

Comparar também porto básico e administração com as definições carregadas:
ARoAI redefine PMs com dados diferentes da instalação vanilla 1.15.

## Ciclo de vida e interface

Verificar ativação por decisão, save existente, nova campanha, pulso mensal,
atualização manual, data, valores contra as telas do jogo, persistência após
recarregar e ausência de JE duplicada. Desativar, avançar meses e confirmar
que não reativa sozinho; reativar e testar limpeza/migração de variáveis.
Conferir português e fallback inglês, tooltip, ignorar/restaurar e estado vazio.

No Manual, confirmar ausência de ação econômica; no Assistido, ação só após
aprovação e revalidação; no Automático futuro, somente domínios autorizados.
Reordenar recomendações antes de clicar para verificar identidade do candidato.

## Cenários econômicos

| Cenário | Verificação e evidência exigida |
| --- | --- |
| Haiti pequeno | Emprego, orçamento, infraestrutura e insumos permitem as prioridades? Registrar motivos e candidatos rejeitados |
| País rico | Investimento aproveita capacidade sem expandir setor saturado? Comparar fila e custos recorrentes |
| Crise fiscal | Bloquear novas expansões inviáveis sem prometer cancelar custos já contratados; verificar reserva/dívida |
| Escassez | Distinguir preço alto de falta de insumo; impedir indústria dependente de abastecimento inexistente |
| Sem oportunidade | Até zero recomendações; fila vazia permitida; nenhum candidato artificial |
| Fila privada e pública | Mesmo edifício/estado em ambas, obra em andamento, primeira construção e cancelamento; nenhum pedido duplicado |
| Mods de PM | Mudança externa após análise invalida candidato e atualiza mão de obra/insumos; ausência de troca de volta pelo Director |
| Campanha longa | Amostras mensais e comparação em 1, 5, 10, 20 e 30 anos, com controle sem Director quando viável |

Registrar PIB, PIB per capita, padrão de vida, emprego, alfabetização,
infraestrutura, saldo, reservas, dívida, preços, produção e diversificação;
valor indisponível deve constar como indisponível. Guardar fila, ações,
modo e opções dos outros mods em cada marco. Crescimento do PIB isolado não
aprova o cenário. Medir tempo de atualização e tamanho do histórico/save.

Encerrar restaurando o load order de teste e preservando evidências separadas.
Testes automatizados futuros devem cobrir pontuação, restrições fiscais,
deduplicação, atualização, estados vazios, schema, localização e integridade GUI;
eles complementam esse roteiro, sem substituir os cliques na engine.
