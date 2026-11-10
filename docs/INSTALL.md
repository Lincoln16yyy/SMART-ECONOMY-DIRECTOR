# Instalação e uso — versão 0.6.20

Requer Victoria 3 1.15.x. A versão 0.6.20 mantém o diagnóstico e os protótipos
de expansão ferroviária e de capacidade de construção. Acrescenta recomendações
e botões de aprovação para expandir produtores locais de madeira, ferro,
carvão, cereais, tecido, ferramentas, mantimentos e roupas quando o mercado
registra escassez. O produtor precisa existir em estado incorporado, estar
operante, usar método de produção ativo que gere o bem, não ter falta de insumos
e não ter expansão já na fila. A operação continua limitada a um nível por
aprovação. Saldo semanal negativo gera um alerta, mas não impede aprovação. Os modos
Manual, Assistido e Automático têm botões visíveis no topo do diário. Automático é
opt-in. O executor próprio tenta no máximo um nível elegível por mês e os
executores externos seguem suas agendas e limites. Após cada revisão,
o diário informa se houve ação, faltou candidato ou uma trava bloqueou a fila. Não altera métodos
de produção nem leis.

## Gerar o pacote

Na raiz do repositório, com Python 3.10 ou superior:

```bash
python3 tools/build_mod.py
python3 tools/validate.py --game "/caminho/Victoria 3/game"
python3 tools/package_mod.py
```

O resultado fica em `dist/smart-economy-director-0.6.20.zip`. O pacote contém
somente os arquivos carregáveis; não inclui saves, fontes do jogo, pesquisa,
testes ou outro mod. A geração é determinística e não modifica a instalação.

## Instalar manualmente

Feche o jogo e use uma cópia de save para os testes. Extraia o ZIP na pasta
`mod` dos dados do usuário, de modo que existam estes dois caminhos:

```text
mod/Smart Economy Director.mod
mod/Smart Economy Director/descriptor.mod
```

Nesta máquina, a pasta encontrada foi:

```text
~/.config/hydralauncher/wine-prefixes/529340/drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3/mod
```

Esse caminho pertence ao prefixo Wine usado pelo jogo. Em outra máquina,
localize os dados efetivos do usuário. Não confunda com a pasta `game` da
instalação ou com a pasta Downloads.

Ative **Smart Economy Director** no launcher preservando os demais mods e
a ordem atual. O pacote não edita `content_load.json`. Se a pasta já existir,
guarde a versão anterior fora de `mod` e extraia uma pasta nova para evitar
scripts antigos remanescentes.

## Usar

1. Carregue a cópia de uma campanha ou inicie uma campanha nova.
2. Abra as decisões e escolha **Ativar Smart Economy Director**.
3. Abra o registro de diário **Smart Economy Director**.
4. Use **Atualizar diagnóstico** para uma nova leitura imediata.
5. Use **Atualizar sob solicitação** para suspender as leituras mensais,
   ou **Atualizar todo mês** para retomá-las e atualizar imediatamente.
6. Se houver uma recomendação ferroviária, de capacidade de construção ou de
   oferta, confira alvo e alerta financeiro; selecione Assistido e use o botão visível para
   enfileirar um nível público. As ações não preveem custo nem retorno.
   Para a oferta, confirme no jogo a escassez do bem e o método ativo do
   produtor. Veja as travas em [MANUAL_RUNTIME_TEST.md](MANUAL_RUNTIME_TEST.md).
7. Use **Desativar** no diário ou a decisão de desativação para limpar leituras
   e histórico. Para voltar, use a decisão de ativação.

Quando não houver candidato, a seção mostra uma linha de motivos com contagens
por estado: sem ferrovia/setor, edifício não operante ou bloqueio por
incorporação/permissão. Cada estado entra em um único motivo principal, então as
contagens somam o total examinado.

Quando o botão de aprovar está desabilitado, uma linha indica a primeira
guarda que falha (fila privada não vazia, inadimplência, fila pública curta ou estado desatualizado). O botão é seguro clicar quando nada aparece: a
revalidação do clique ainda impede a ação se alguma guarda falhar.

O Director é opcional: não se ativa sozinho em campanha nova ou save existente.
As opções de atualização controlam a frequência das leituras. Manual não aprova
ações; Assistido exige clique individual; Automático exige seleção explícita e
revalida filas, inadimplência, pausa da construção e flags conhecidas de outros
construtores antes de agir.

Todos os números do painel pertencem à última leitura, cuja data é mostrada.
A variação do PIB exige leituras em meses distintos e uma base positiva.
Cliques no mesmo mês não mudam a amostra-base. Após uma pausa de vários meses,
o painel mostra a variação acumulada e a distância entre os meses do calendário
registrados. Não é uma duração exata em dias, uma taxa mensal ou uma previsão.

Reservas divididas pelo déficit são uma razão condicional, sem uso do crédito
e mantendo o saldo observado. Não são uma previsão de falência ou uma garantia
de capacidade de investimento. As contagens de edifícios com contratação
incompleta não representam o número de desempregados.

## Desativar e remover

Desative pelo Director, avance o tempo suficiente para o diário processar a
desativação e salve a cópia de teste. A limpeza remove suas variáveis de
execução, mas conserva `sed_schema_version` e, quando existente,
`sed_auto_last_attempt_month`, a marca de segurança do limite mensal. Depois, feche o jogo,
desative no launcher e remova a pasta e o descritor externo.

A inclusão em saves existentes usa uma decisão e foi coberta estruturalmente;
a confirmação dentro da engine, incluindo salvar/recarregar e o ciclo do
diário, continua no roteiro [MANUAL_RUNTIME_TEST.md](MANUAL_RUNTIME_TEST.md).


Desde a 0.4.0, uma escassez sem candidato mostra os estados com produtor e sua
rejeição principal na última leitura: expansão pendente/enfileirada, estado
não incorporado, nível zero/ocupação abaixo de 80%, falha de contratação,
falta de insumos, método sem produção confirmada ou construção não permitida.
As regras de aprovação permanecem iguais. Atualize o diagnóstico após instalar.


Em um cartão elegível, **Ignorar esta expansão neste estado** remove apenas
aquele tipo de expansão naquele estado das recomendações e da automação.
No topo, **Restaurar recomendações ignoradas** remove todas as escolhas atuais
e atualiza a análise. Ignorar vale nos três modos e não cancela obras;
restaurar não aprova obras. Desativar o Director limpa essas preferências.


Interface 0.6.9: fonte principal 20, títulos 26 e botões nativos de 52 pixels,
com fundo/borda. As recomendações vêm primeiro e os indicadores completos
podem ser abertos com Mostrar indicadores e detalhes. As listas de cartões
crescem com o conteúdo em vez de usar uma altura de linha fixa. Os critérios
econômicos, modos e travas de aprovação permanecem iguais.


Na 0.6.9, cada cartão indica quando a aprovação está disponível. Em outro modo,
Passar para Assistido muda apenas o modo; depois o jogador decide se aprova.
Atualizar recomendações aparece no cartão desatualizado e pode removê-lo da
lista sem executar obras. Abrir fila de construção leva ao painel nativo.
A fonte e os botões maiores da 0.5.0 foram mantidos.


O painel Automático 0.6.9 mostra se há evento pendente e o bloqueio atual,
mesmo antes da próxima revisão. Registra o último resultado com mês/ano,
separadamente dos indicadores. Atualizar diagnóstico não executa a revisão;
trocar modo preserva esse registro e desativar limpa. Em save antigo sem dados
da revisão, a versão informa ausência de registro em vez de atribuir data.


Na 0.6.9 o executor próprio permite uma tentativa por mês, registrada antes da chamada
de construção. Uma inclusão não confirmada também consome o limite; revisão
bloqueada antes de tentar ou sem candidato não consome. O marcador não é
apagado por atualizar, trocar modo, cancelar projeto ou desativar/reativar.
No próximo mês, o calendário atual libera outra tentativa, se elegível.
Assistido não usa esse limite; mantém revalidação e demais guardas.

O marcador mensal é uma exceção intencional à limpeza total do diagnóstico:
sem preservá-lo, reativar permitiria outra tentativa no mesmo mês. Ele não
agenda ações, não guarda projetos e não interfere com o mod desabilitado.
Não reconstrói tentativas antigas sem registro nem comprova persistência na
engine; save/reload ainda exige verificação em cópia de campanha.

## Atualização 0.6.9

Ao selecionar Automático com executores detectados, o Director guarda sete
opções de construção e escolhe uma rota externa conforme o plano. Use
Restaurar opções ou saia para Assistido/Manual para devolver as configurações.
Restaure antes de remover o mod. Consulte PLANNING.md para as regras, limites
e efeitos sobre configurações alteradas manualmente durante a coordenação.

O instalador local atualiza uma instalação existente com jogo fechado, guarda
a pasta anterior e confere os 14 outputs. O caminho é obrigatório.

```bash
python3 tools/install_mod.py --user-data "/caminho/dos/dados/Victoria 3" --dry-run
python3 tools/install_mod.py --user-data "/caminho/dos/dados/Victoria 3"
```

Em save da 0.5.x, selecione Automático novamente para assumir a coordenação.

Na 0.6.9, o Automático também coordena objetivo e orçamento do Advisor.
O painel mostra a orientação aplicada. Restauração inclui essas quatro opções.
Em coordenação 0.6.0 já ativa, a primeira seleção do Advisor captura as opções
atuais antes de aplicar a política nova.

A política fiscal permite um ajuste de imposto e um de salário civil por mês
de calendário. Os marcadores mensais permanecem após troca de modo ou
desativação. Metas antigas sem amostragem datada são recontadas. A revisão
completa está em REVIEW_2026-11-10.md.
