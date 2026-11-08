# PROJETO: SMART ECONOMY DIRECTOR
## Planejador e Coordenador Econômico Inteligente — Victoria 3 (versão 1.15)

Você será responsável por pesquisar, projetar, desenvolver, testar e documentar um novo mod para Victoria 3 chamado **Smart Economy Director**.

Não trate este projeto como um simples mod de recomendações econômicas. A intenção é desenvolver um sistema de planejamento econômico nacional, capaz de analisar o país como um todo, definir objetivos de longo prazo, coordenar decisões econômicas e, quando tecnicamente possível, executar ações automaticamente.

O jogador quer conseguir deixar seu país evoluir praticamente sozinho durante décadas, sem precisar administrar manualmente cada construção, método de produção ou decisão econômica.

O resultado precisa ser um mod funcional, integrado corretamente ao jogo e compatível com os outros mods utilizados pelo jogador.

---

# 1. CONTEXTO DO PROJETO E DO JOGADOR

O jogador está desenvolvendo um conjunto de mods para transformar a administração de países em Victoria 3 em uma experiência muito mais autônoma.

A campanha utilizada para testar o projeto é principalmente com o Haiti.

A intenção é conseguir deixar o país evoluir por 10, 20 ou 30 anos com o mínimo de intervenção possível.

O jogador não quer que o país apenas construa edifícios aleatoriamente. Ele quer um país economicamente desenvolvido, produtivo, financeiramente sustentável, com infraestrutura, população empregada, indústria diversificada e capacidade de financiar seus próprios objetivos.

O jogador deseja manter o controle de decisões importantes, especialmente:
- Declarar guerras.
- Aceitar ou iniciar conflitos diplomáticos importantes.
- Alterar objetivos nacionais importantes.
- Tomar decisões políticas e diplomáticas de grande impacto.

A economia, por outro lado, deve conseguir funcionar com bastante autonomia.

O jogador utiliza Victoria 3 versão 1.15, em Linux, através de uma instalação não Steam. Portanto:
- Não presuma que o jogo esteja instalado em uma localização padrão.
- Não presuma que os caminhos do Windows sejam os caminhos do ambiente atual.
- Não dependa de ferramentas exclusivas do Steam Workshop.
- Identifique a estrutura real da instalação.
- Considere os cuidados necessários com Wine e prefixos, caso sejam relevantes.

---

# 2. MOD JÁ DESENVOLVIDO PELO JOGADOR: SMART GOVERNMENT

Este projeto deve estudar obrigatoriamente o mod anterior do jogador:

https://github.com/Lincoln16yyy/Smart-Government-Victoria-3-1.15

Esse repositório é a principal referência de organização, qualidade, experiência de usuário e filosofia de desenvolvimento.

Não comece a programar antes de estudar o projeto.

Leia, no mínimo:

- README.md
- docs/AI_CONTEXT.md
- docs/PHASE_LOG.md
- docs/MANUAL_RUNTIME_TEST.md
- Estrutura de common/
- Scripted effects, triggers e values.
- Estrutura das interfaces de Journal Entry.
- Sistema de recomendações e pontuação.
- Geração dos dados.
- Sistema de atualização mensal.
- Sistema de diagnóstico.
- Testes automatizados.
- Localização.
- Metadados e arquivos de instalação.

Investigue como o Smart Government implementa:
- Recomendações contextualizadas.
- Análise de leis.
- Pontuação de benefícios, riscos e apoio político.
- Explicações das recomendações.
- Atualizações mensais.
- Ações manuais na interface.
- Ignorar e restaurar recomendações.
- Ativação e desativação.
- Limpeza de variáveis.
- Namespacing para evitar conflitos.
- Validação automatizada.
- Documentação de testes manuais.

## Filosofia que deve ser preservada

O Smart Government não tenta tomar todas as decisões políticas pelo jogador.

Ele analisa as leis disponíveis, calcula vantagens e riscos, apresenta recomendações e deixa o jogador iniciar a promulgação.

Seu sistema econômico deverá adotar a mesma filosofia de transparência, mas com níveis de automação apropriados ao domínio econômico.

O novo mod deve possuir identidade própria.

Não copie cegamente a implementação do Smart Government. Reaproveite padrões arquiteturais quando fizer sentido e investigue separadamente os recursos técnicos do jogo para economia.

O Smart Government possui o prefixo `sg_`. O novo projeto deverá possuir um prefixo próprio, como `sed_`, em variáveis, efeitos, decisões, eventos e demais identificadores próprios.

Não sobrescreva arquivos originais do jogo sem necessidade.

Não altere o comportamento do Smart Government.

Os dois projetos devem continuar independentes, com possibilidade de integração futura.

---

# 3. MODS QUE JÁ FAZEM PARTE DO ECOSSISTEMA

O jogador utiliza ou está desenvolvendo sua campanha com os seguintes mods:

### Economy Advisor

É um dos mods mais importantes para este projeto.

O jogador informou que utiliza Economy Advisor, e não OGAS.

Sua implementação e compatibilidade exatas ainda precisam ser investigadas.

Não presuma suas funcionalidades apenas pelo nome ou pela descrição de uma página.

Localize os arquivos reais do mod instalado e examine:
- Scripts.
- Decisões.
- Eventos.
- Journal Entries.
- Scripted effects e triggers.
- Interface.
- Métodos de produção.
- Construção automática.
- Recomendações.
- Variáveis utilizadas.
- Frequência de atualização.
- Configurações e opções de automação.
- Compatibilidade declarada com Victoria 3 1.15.

Descubra precisamente o que ele já faz, o que consegue executar e o que apenas recomenda.

Verifique também se suas funções estão efetivamente habilitadas.

**Não desenvolva funcionalidades duplicadas sem uma justificativa técnica.**

### Supply Chain Semi-Auto Builder

Mod relacionado à construção e às cadeias produtivas.

Investigue o que ele efetivamente automatiza e como decide quais construções são necessárias.

O Smart Economy Director deverá evitar duplicar construções, criar filas conflitantes ou disputar o controle da fila de construção.

### Auto-Apply PMs

Mod de aplicação automática de métodos de produção.

Investigue seu funcionamento e como evitar que o Director recomende ou execute decisões incompatíveis com ele.

### Auto-Apply Automation PMs

Mod relacionado à automação da produção.

Investigue como ele considera mão de obra, produtividade e disponibilidade de insumos.

O Director deve considerar os efeitos dessas automações no planejamento econômico.

### Auto-Diplomacy and Advanced Subject Management

Mod que automatiza partes da diplomacia e da gestão de súditos.

Não é o foco do projeto, mas decisões econômicas devem considerar os efeitos de relações diplomáticas, comércio e súditos quando os dados estiverem disponíveis.

### Auto-Recruit & One-Click Recruit Commanders

Mod de automação militar.

O sistema econômico deve considerar que o país pode precisar financiar o exército, a indústria bélica e a marinha.

Não deve comprometer a sustentabilidade fiscal para financiar uma expansão militar desnecessária.

### Kuromi's AI

Investigue possíveis interações e conflitos, sem presumir que esse mod controle diretamente a economia do jogador.

### Regra de compatibilidade

Todos os mods acima devem ser tratados como parte de um ecossistema.

Crie um documento de compatibilidade indicando:
- O que cada mod controla.
- Quais sistemas podem ser compartilhados.
- Quais ações podem entrar em conflito.
- Quais integrações são tecnicamente possíveis.
- Quais integrações não foram testadas.

Não invente APIs ou interfaces de integração.

Se dois mods não possuem comunicação direta, procure formas seguras de coexistência usando os recursos reais do jogo.

Não crie dependências obrigatórias desnecessárias.

---

# 4. OBJETIVO PRINCIPAL DO SMART ECONOMY DIRECTOR

O Smart Economy Director deverá ser um planejador econômico nacional.

O Economy Advisor pode executar determinadas tarefas econômicas. O Director deve pensar estrategicamente.

Sua responsabilidade é responder continuamente:

1. Qual é a situação econômica atual do país?
2. Quais são seus principais problemas?
3. Quais setores precisam crescer?
4. Quais setores estão superdimensionados?
5. Onde existem oportunidades de desenvolvimento?
6. O país possui dinheiro e capacidade de construção?
7. Quais são as prioridades dos próximos anos?
8. As decisões atuais estão melhorando ou prejudicando o país?
9. Quando é melhor não construir nada?
10. Qual é o próximo passo mais importante para o desenvolvimento nacional?

O sistema precisa trabalhar com objetivos de curto, médio e longo prazo.

### Curto prazo
- Resolver escassez de bens.
- Reduzir gargalos produtivos.
- Evitar déficits perigosos.
- Aproveitar trabalhadores disponíveis.
- Melhorar a infraestrutura necessária.
- Evitar construções financeiramente inviáveis.

### Médio prazo
- Desenvolver cadeias produtivas.
- Diversificar a indústria.
- Melhorar a produtividade.
- Reduzir dependências externas estratégicas.
- Desenvolver estados com potencial econômico.
- Melhorar salários e padrão de vida.

### Longo prazo
- Aumentar PIB e PIB per capita.
- Modernizar a economia.
- Desenvolver setores de maior valor agregado.
- Melhorar educação e qualificação.
- Aumentar a capacidade de construção.
- Criar uma economia sustentável e resiliente.
- Preparar o país para objetivos futuros.

---

# 5. SISTEMA DE DIAGNÓSTICO ECONÔMICO

Antes de recomendar ou executar qualquer ação, o mod deve analisar o estado atual do país.

Investigue os dados realmente acessíveis pela versão 1.15 do jogo.

A análise deve incluir:

### Finanças públicas
- Saldo orçamentário.
- Receitas e despesas.
- Reservas de ouro.
- Dívida e juros, quando aplicáveis.
- Gastos com construção.
- Gastos militares.
- Gastos administrativos.
- Impostos e níveis de tributação.
- Capacidade de sustentar déficits temporários.

### Mercado
- Preços dos bens.
- Oferta e demanda.
- Importações.
- Exportações.
- Dependência de mercados externos.
- Escassez de produtos essenciais.
- Excesso de produção.
- Bens utilizados em cadeias produtivas.

### Produção
- Produção por setor.
- Produtividade.
- Rentabilidade.
- Métodos de produção.
- Necessidade de insumos.
- Capacidade instalada.
- Edifícios deficitários.
- Edifícios subutilizados.

### População
- Emprego e desemprego.
- Trabalhadores disponíveis.
- Qualificações.
- Salários.
- Padrão de vida.
- Migração, quando relevante.
- Distribuição populacional entre estados.

### Infraestrutura
- Infraestrutura disponível.
- Capacidade utilizada.
- Ferrovias.
- Portos.
- Construção.
- Serviços e gargalos regionais.

### Desenvolvimento nacional
- PIB.
- PIB per capita.
- Crescimento econômico.
- Alfabetização.
- Educação.
- Produtividade.
- Industrialização.
- Diversificação econômica.

Não presuma que todos esses dados podem ser lidos diretamente.

Para cada métrica:
1. Identifique a fonte real no jogo.
2. Verifique se pode ser consultada por scripts.
3. Verifique se pode ser exibida na interface.
4. Documente suas limitações.
5. Não crie valores fictícios para preencher dados ausentes.

---

# 6. SISTEMA DE PLANEJAMENTO ESTRATÉGICO

Esta é a parte mais importante do projeto.

O Director não deve olhar apenas para preços e lucros momentâneos.

Ele deverá construir uma estratégia econômica nacional a partir da situação do país.

### Exemplo: Haiti

Imagine um país com:
- Baixa capacidade de construção.
- Pouca produção de ferramentas.
- Dependência de importações.
- Trabalhadores disponíveis.
- Pouca infraestrutura.
- Orçamento limitado.

O sistema deverá avaliar se faz sentido desenvolver ferramentas, mineração, madeira, ferro ou outros setores necessários.

Mas não deve recomendar todos simultaneamente.

Precisa avaliar:
- Custo de construção.
- Tempo necessário.
- Disponibilidade de trabalhadores.
- Disponibilidade de insumos.
- Efeito esperado nos preços.
- Efeito sobre outras indústrias.
- Sustentabilidade fiscal.
- Prioridade nacional.

Se a construção de uma indústria depender de insumos importados que o país não consegue obter, isso deverá afetar sua pontuação.

### Priorização

Desenvolva um sistema de pontuação que classifique oportunidades considerando:

- Necessidade nacional.
- Impacto econômico.
- Redução de escassez.
- Aumento de produtividade.
- Potencial de lucro.
- Emprego.
- Impacto no padrão de vida.
- Segurança de abastecimento.
- Custo de construção.
- Tempo para obter retorno.
- Capacidade financeira.
- Infraestrutura.
- Qualificações.
- Risco de excesso de produção.

Não utilize uma fórmula arbitrária sem explicação.

Documente os pesos, os critérios e as limitações.

Quando possível, compare o resultado previsto com os resultados efetivamente observados depois da construção.

O sistema deverá aprender com os resultados durante a campanha, mas não inventar previsões que os dados do jogo não permitem calcular.

---

# 7. COORDENAÇÃO DAS CONSTRUÇÕES

O Director deve decidir quais construções são estrategicamente necessárias.

Considere:
- Construções existentes.
- Construções em andamento.
- Construções enfileiradas.
- Construções privadas.
- Oferta e demanda.
- Trabalhadores disponíveis.
- Insumos.
- Infraestrutura.
- Rentabilidade.
- Custo de manutenção.
- Necessidades futuras da economia.

### Regras obrigatórias

1. Nunca adicionar repetidamente a mesma construção porque o sistema ainda não observou o resultado da anterior.
2. Considerar a fila existente antes de recomendar novos edifícios.
3. Não criar fábricas sem trabalhadores suficientes, salvo justificativa estratégica documentada.
4. Não expandir setores que já apresentam excesso estrutural de produção sem uma razão clara.
5. Não construir edifícios que o país não consiga abastecer.
6. Não comprometer toda a capacidade de construção com um único setor.
7. Não ignorar construções privadas.
8. Não tratar lucro de curto prazo como único critério.
9. Não construir apenas para manter a fila ocupada.
10. Permitir que o sistema recomende não fazer novas construções.

### Estados e localização

O Director deve analisar onde construir.

Considere:
- Disponibilidade de trabalhadores.
- Qualificações.
- Recursos naturais.
- Infraestrutura.
- População.
- Potencial produtivo.
- Custos e bônus regionais.
- Cadeias produtivas existentes.

Não escolha estados aleatoriamente.

---

# 8. GESTÃO FINANCEIRA E PROTEÇÃO ECONÔMICA

A automação precisa ser responsável.

O Director não pode destruir a economia do país por tentar crescer rápido demais.

Crie proteções para:

- Preservar reservas de ouro.
- Evitar déficits persistentes.
- Considerar juros e endividamento.
- Controlar o ritmo de construção.
- Avaliar despesas recorrentes.
- Evitar gastos militares excessivos.
- Considerar custos de métodos de produção.
- Evitar que o país dependa de uma economia artificialmente sustentada por dívida.

O sistema deverá identificar diferentes situações:

**Expansão saudável:** o país possui recursos e pode investir.

**Expansão cautelosa:** o país pode investir, mas deve preservar reservas.

**Estagnação:** não há investimento claramente vantajoso.

**Crise fiscal:** prioridade é recuperar sustentabilidade financeira.

**Emergência:** existem problemas graves que exigem ação imediata.

Não implemente uma política fixa de orçamento que funcione mal para países pequenos e grandes.

Os limites precisam ser proporcionais à economia do país.

O Haiti deve ser um caso importante de teste.

---

# 9. COORDENAÇÃO COM MÉTODOS DE PRODUÇÃO

O Director precisa entender que a produção pode ser modernizada por outros mods.

Considere o funcionamento de:
- Auto-Apply PMs.
- Auto-Apply Automation PMs.
- Economy Advisor.

Antes de implementar qualquer sistema próprio de troca de métodos de produção, verifique se outro mod já executa essa função.

O Director deve avaliar:
- Disponibilidade de trabalhadores.
- Custo dos insumos.
- Aumento de produtividade.
- Alteração dos salários.
- Desemprego causado.
- Efeito sobre a lucratividade.
- Impacto sobre o mercado.

Uma modernização não é automaticamente boa apenas porque aumenta a produtividade.

Se uma mudança provocar escassez de insumos, demissões excessivas ou prejuízo generalizado, isso deve ser considerado.

---

# 10. TECNOLOGIA E DESENVOLVIMENTO INDUSTRIAL

Embora exista a possibilidade de um futuro Smart Technology separado, o Director deve considerar a tecnologia disponível.

Não precisa assumir o controle da pesquisa tecnológica.

Entretanto, deve identificar:
- Tecnologias que estão limitando a produção.
- Métodos de produção indisponíveis.
- Tecnologias que podem aumentar a produtividade.
- Tecnologias relevantes para infraestrutura.
- Tecnologias que podem melhorar o desenvolvimento nacional.

Quando a pesquisa não for controlável pelo mod, apresente uma recomendação fundamentada.

---

# 11. POPULAÇÃO, EMPREGO E PADRÃO DE VIDA

O objetivo não é criar um país com PIB elevado e população miserável.

O Director deve avaliar o desenvolvimento social junto com o crescimento econômico.

Considere:
- Desemprego.
- Empregos disponíveis.
- Salários.
- Qualificações.
- Padrão de vida.
- Custo dos bens essenciais.
- Migração.
- Crescimento populacional.
- Efeitos de novas construções.

Evite expandir setores que não conseguem contratar trabalhadores.

Considere a necessidade de educação e qualificação como parte do desenvolvimento de longo prazo.

Não tente controlar diretamente todas as políticas sociais se isso duplicar o Smart Government.

---

# 12. MODOS DE OPERAÇÃO

O sistema deverá possuir três modos:

### AUTOMÁTICO

Executa automaticamente ações econômicas seguras e tecnicamente suportadas.

Exemplos:
- Adicionar construções.
- Ajustar prioridades econômicas.
- Executar ações de gestão que o jogo permita.
- Corrigir problemas produtivos dentro dos limites configurados.

Não pode iniciar guerras ou tomar decisões diplomáticas importantes.

### ASSISTIDO

Analisa a economia, define prioridades e apresenta recomendações.

O jogador aprova ou rejeita as ações.

### MANUAL

Não executa ações econômicas.

Apresenta apenas diagnóstico, indicadores e recomendações quando solicitado.

A mudança entre modos deve ser simples pela interface.

---

# 13. INTERFACE — JOURNAL ENTRY

Utilize como referência visual e funcional a interface do Smart Government.

Crie uma Journal Entry própria para o Smart Economy Director.

A interface deverá mostrar:

### Situação econômica
- Estado atual da economia.
- PIB e crescimento.
- Orçamento.
- Reservas.
- Capacidade de construção.
- Emprego.
- Padrão de vida.
- Principais problemas.

### Estratégia nacional
- Objetivo econômico atual.
- Prioridades de curto prazo.
- Prioridades de médio prazo.
- Prioridades de longo prazo.
- Setores que precisam crescer.
- Setores que precisam de atenção.

### Recomendações

Mostrar até três recomendações prioritárias.

Cada uma deve explicar:
- O que fazer.
- Por que fazer.
- Benefício esperado.
- Custo estimado, se disponível.
- Riscos.
- Urgência.
- Consequência provável de não agir.

### Controle
- Modo de operação.
- Ativar e desativar.
- Atualizar análise manualmente.
- Aprovar recomendações.
- Ignorar recomendações.
- Restaurar recomendações ignoradas.
- Visualizar histórico.
- Consultar última atualização.

A interface deve ser clara, organizada e compatível com o padrão de Victoria 3.

Não crie botões decorativos ou que não executam ações reais.

---

# 14. COORDENAÇÃO COM O FUTURO SMART NATION CONTROLLER

O Smart Economy Director deve ser desenvolvido como um módulo independente.

No futuro, poderá existir um Smart Nation Controller, responsável por coordenar:

- Smart Government.
- Smart Economy Director.
- Smart Technology.
- Smart Military.
- Smart Population.
- Smart Crisis Manager.

Não implemente o Smart Nation Controller agora.

Entretanto, organize o código para permitir integração futura.

Evite dependências rígidas e variáveis globais desnecessárias.

O Director deve conseguir funcionar sozinho, sem depender do Smart Government.

---

# 15. PESQUISA TÉCNICA OBRIGATÓRIA

Antes de implementar qualquer recurso, investigue a versão 1.15 do Victoria 3.

Não confie exclusivamente em documentação antiga, vídeos ou mods de versões anteriores.

Examine os arquivos reais do jogo e os mods instalados.

Investigue:
- Estrutura de buildings.
- Construction queue.
- Journal Entries.
- Decisions.
- Events.
- On actions.
- Scripted effects.
- Scripted triggers.
- Scripted values.
- GUI.
- Localization.
- Variáveis de país e estado.
- Métodos de produção.
- Acesso a informações de mercado.
- Ações econômicas executáveis por scripts.
- Limitações da interface.
- Frequência segura de atualização.

Para cada funcionalidade pretendida, classifique:

1. **Executável:** existe mecanismo comprovado para executar a ação.
2. **Observável:** o jogo fornece os dados necessários, mas não permite executar a ação automaticamente.
3. **Parcial:** existe uma implementação limitada.
4. **Não suportado:** não existe mecanismo confiável identificado.

Não invente comandos, funções, efeitos ou APIs.

Se uma funcionalidade não puder ser automatizada, implemente uma recomendação honesta e documente a limitação.

---

# 16. TESTES OBRIGATÓRIOS

Não considere o projeto pronto apenas porque os arquivos passaram na validação estática.

Crie testes automatizados para:
- Pontuação.
- Priorização.
- Identificação de escassez.
- Controle de construções duplicadas.
- Análise orçamentária.
- Atualizações.
- Estados sem recomendações.
- Ativação e desativação.
- Limpeza de variáveis.
- Consistência de localization.
- Compatibilidade dos identificadores.
- Integridade da interface.

Crie também testes manuais com cópias de saves.

### Cenário A — Haiti

Teste com país pequeno e orçamento limitado.

Verifique:
- Se escolhe prioridades realistas.
- Se evita expansão exagerada.
- Se considera trabalhadores e insumos.
- Se consegue aumentar a capacidade produtiva.
- Se não gera déficits insustentáveis.

### Cenário B — País rico

Teste se o sistema aproveita a capacidade de investimento sem desperdiçar dinheiro.

### Cenário C — Crise econômica

Teste se interrompe expansões inadequadas e prioriza a recuperação.

### Cenário D — País com escassez de insumos

Teste se considera a cadeia produtiva completa e evita construções inviáveis.

### Cenário E — Campanha longa

Deixe o país evoluir por vários anos.

Observe:
- PIB.
- PIB per capita.
- Padrão de vida.
- Emprego.
- Alfabetização.
- Infraestrutura.
- Orçamento.
- Reservas.
- Dívida.
- Produção.
- Construções.
- Preços.
- Diversificação econômica.

Compare o estado inicial e o final.

Não afirme que o país está se desenvolvendo bem apenas porque o PIB cresceu.

---

# 17. QUALIDADE E ORGANIZAÇÃO DO CÓDIGO

Siga os padrões do Smart Government sempre que apropriado.

Requisitos:
- Código organizado.
- Identificadores próprios.
- Namespacing consistente.
- Localização em português brasileiro.
- Fallback em inglês.
- Comentários úteis.
- Documentação.
- Validação automatizada.
- Testes reproduzíveis.
- Instalação simples.
- Compatibilidade com saves existentes, se tecnicamente possível.
- Nenhuma modificação desnecessária nos arquivos originais.

Não remova funcionalidades do jogo base.

Não crie arquivos vazios apenas para aparentar que uma funcionalidade existe.

Não apresente uma funcionalidade como concluída se ela apenas exibe uma mensagem ou simula uma ação.

---

# 18. METODOLOGIA DE DESENVOLVIMENTO

Trabalhe em fases.

Não tente implementar todo o sistema de uma só vez.

### Fase 0 — Pesquisa e diagnóstico

- Estudar o Smart Government.
- Localizar e estudar o Economy Advisor.
- Estudar os demais mods.
- Investigar Victoria 3 1.15.
- Mapear capacidades e limitações.
- Criar documento de arquitetura.
- Identificar conflitos potenciais.

Entregável: `docs/RESEARCH.md`.

Não iniciar a implementação antes de concluir essa fase e apresentar suas conclusões.

### Fase 1 — Diagnóstico econômico

Implementar a leitura dos indicadores e a apresentação da situação econômica.

Nenhuma ação automática ainda.

Entregável: primeira Journal Entry funcional.

### Fase 2 — Planejamento estratégico

Implementar pontuação, objetivos econômicos e recomendações.

Entregável: sistema que consegue identificar as três prioridades mais importantes do país.

### Fase 3 — Execução controlada

Implementar as ações automáticas comprovadamente suportadas pelo jogo.

Entregável: modo Automático com proteções econômicas.

### Fase 4 — Compatibilidade

Testar convivência com Economy Advisor e os demais mods.

Corrigir duplicações, conflitos e comportamentos inesperados.

### Fase 5 — Testes de campanha

Executar os cenários definidos anteriormente.

Registrar resultados reais.

### Fase 6 — Documentação e entrega

Atualizar:
- README.md
- docs/AI_CONTEXT.md
- docs/PHASE_LOG.md
- docs/MANUAL_RUNTIME_TEST.md
- docs/RESEARCH.md
- Documentação de compatibilidade.

---

# 19. REGRAS DE TRABALHO COM O JOGADOR

O jogador está desenvolvendo seus conhecimentos de programação e utiliza agentes de IA para ajudar na criação dos mods.

Portanto:

- Explique o que está fazendo.
- Não esconda decisões arquiteturais.
- Divida mudanças grandes em etapas pequenas.
- Apresente os arquivos que serão alterados.
- Explique os motivos de cada implementação.
- Mostre limitações técnicas.
- Não faça refatorações desnecessárias.
- Preserve o trabalho que já funciona.
- Não substitua funcionalidades por protótipos simplificados.
- Não declare sucesso sem evidência.

Antes de cada fase:
1. Apresente o objetivo.
2. Explique o plano.
3. Liste os arquivos que pretende alterar.
4. Identifique riscos.

Depois de cada fase:
1. Informe o que foi implementado.
2. Informe os testes executados.
3. Informe os resultados.
4. Liste o que ainda não foi testado.
5. Atualize a documentação.

Se uma ação depender de confirmação do jogador, aguarde.

---

# 20. CRITÉRIO FINAL DE SUCESSO

O Smart Economy Director estará cumprindo seu objetivo quando for capaz de:

- Entender a situação econômica nacional.
- Identificar os problemas mais importantes.
- Definir uma estratégia coerente de desenvolvimento.
- Priorizar investimentos com justificativa.
- Evitar construções improdutivas.
- Considerar trabalhadores, insumos e infraestrutura.
- Preservar a sustentabilidade financeira.
- Coordenar-se com as automações existentes, quando possível.
- Executar as ações suportadas pelo jogo.
- Explicar o que fez e por que fez.
- Reconhecer quando não é necessário fazer nada.

O objetivo não é construir o máximo possível.

O objetivo é desenvolver um país economicamente forte, produtivo, estável e sustentável ao longo de décadas.

**Comece pela FASE 0. Não programe o mod ainda. Primeiro investigue o Smart Government, o Economy Advisor instalado, os demais mods e os recursos reais de Victoria 3 1.15. Depois apresente o diagnóstico técnico e a arquitetura proposta.**