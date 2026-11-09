# Instalação e uso — versão 0.3.2

Requer Victoria 3 1.15.x. A versão 0.3.2 mantém o diagnóstico e os dois
protótipos de ação com aprovação individual — expansão ferroviária e ampliação
de um setor de construção quando a fila pública está sobrecarregada — e
acrescenta a decomposição dos motivos de rejeição quando não há candidato e
uma linha explicando por que o botão de aprovação está bloqueado. Não
executa ações econômicas automaticamente nem altera métodos de produção. Não
depende do Steam Workshop.

## Gerar o pacote

Na raiz do repositório, com Python 3.10 ou superior:

```bash
python3 tools/build_mod.py
python3 tools/validate.py --game "/caminho/Victoria 3/game"
python3 -m unittest discover -s tests -v
python3 tools/package_mod.py
```

O resultado fica em `dist/smart-economy-director-0.3.2.zip`. O pacote contém
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
6. Se houver recomendação ferroviária ou de capacidade de construção, confira o
   saldo, a fila pública e o tooltip; pause o jogo e aprove apenas se desejar
   adicionar um nível público. As ações não preveem custo nem retorno. Veja as
   travas em [MANUAL_RUNTIME_TEST.md](MANUAL_RUNTIME_TEST.md).
7. Use **Desativar** no diário ou a decisão de desativação para limpar leituras
   e histórico. Para voltar, use a decisão de ativação.

Quando não houver candidato, a seção mostra uma linha de motivos com contagens
por estado: sem ferrovia/setor, edifício não operante ou bloqueio por
incorporação/permissão. Cada estado entra em um único motivo principal, então as
contagens somam o total examinado.

Quando o botão de aprovar está desabilitado, uma linha indica a primeira
guarda que falha (jogo rodando, fila privada não vazia, inadimplência ou
saldo semanal negativo). O botão é seguro clicar quando nada aparece: a
revalidação do clique ainda impede a ação se alguma guarda falhar.

O Director é opcional: não se ativa sozinho em campanha nova ou save existente.
As opções de atualização controlam a frequência das leituras. Aprovar uma
recomendação executa somente aquela ação; não habilita um modo automático.

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
execução e conserva apenas `sed_schema_version`. Depois, feche o jogo,
desative no launcher e remova a pasta e o descritor externo.

A inclusão em saves existentes usa uma decisão e foi coberta estruturalmente;
a confirmação dentro da engine, incluindo salvar/recarregar e o ciclo do
diário, continua no roteiro [MANUAL_RUNTIME_TEST.md](MANUAL_RUNTIME_TEST.md).
