---
name: vic3-modding
description: Fluxo obrigatório para criar, alterar, validar e testar mods de Victoria 3 (script Paradox/Jomini - common, events, gui, localization, scripted effects/triggers/values, on_actions, journal entries). Use SEMPRE que a tarefa envolver o mod Smart Economy Director ou qualquer arquivo .txt/.gui/.yml/.mod de Victoria 3, mesmo que o usuário só diga "continua o mod", "adiciona X", "corrige esse erro" ou "testa isso". Evita suposições e retrabalho - primeiro verifica no jogo e nos docs, depois escreve.
---

# Victoria 3 — fluxo de modding (verificar, não supor)

## Regra de ouro

**Nenhum efeito, trigger, escopo, modificador ou ID entra no mod sem evidência.**
Evidência = (a) aparece em arquivo do jogo base (`game/`), (b) aparece na
documentação exportada pelo próprio jogo (`docs/`), ou (c) o `vic3-tiger`
aceita. Se nenhuma das três confirma, o item é **NÃO VERIFICADO**: registre
isso no `docs/STATUS.md`, não finja que está pronto e crie um passo de teste
na engine. Perder tempo chutando sintaxe é o erro mais caro deste projeto.

## 0. Ritual de início de sessão (5 minutos, sempre)

1. Leia `references/ambiente-local.md`. Se estiver vazio, descubra e preencha
   (caminho do jogo, pasta de dados, pasta `docs/` exportada, caminho do
   tiger). **Nunca redescubra o que já está anotado.**
2. Leia o **bloco de estado no topo** de `docs/AI_CONTEXT.md` (últimas ~40
   linhas de resumo). Não leia o arquivo inteiro: ele é longo; o histórico
   fica em `docs/PHASE_LOG.md`.
3. Rode `git status` e `git log --oneline -5`. Não sobrescreva trabalho sem commit.
4. Rode `python3 tools/build_mod.py --check`. Se falhar, os arquivos gerados
   estão fora de sincronia: resolva antes de qualquer coisa nova.
5. Declare ao usuário em 3 linhas: onde paramos, o que vai fazer agora, o que
   NÃO está verificado.

## 1. Como um mod de Victoria 3 é estruturado

```
Smart Economy Director.mod        # arquivo na pasta mod/ (aponta para a pasta)
Smart Economy Director/           # pasta do mod
  descriptor.mod                  # version, name, tags, supported_version
  .metadata/metadata.json         # metadados (mantenha a versão sincronizada)
  common/<tipo>/*.txt             # lógica: script_values, scripted_effects,
                                  #   scripted_triggers, scripted_guis, on_actions,
                                  #   journal_entries, decisions ...
  events/*.txt                    # eventos (namespace próprio)
  gui/…/*.gui                     # interface (widgets de journal entry)
  localization/<idioma>/*.yml     # textos (UTF-8 com BOM, cabeçalho l_<idioma>:)
```

- O caminho dentro do mod **espelha** o do jogo base (`game/common/...`). O
  jogo carrega por pasta; arquivo errado = é ignorado ou gera erro no log.
- **Prefixe tudo** (`sed_`, `je_sed_`). Nunca crie arquivo com o mesmo nome de
  um arquivo do jogo base nem sobrescreva IDs de outros mods.
- `on_actions` são aditivos: várias mods podem se pendurar em
  `on_monthly_pulse_country` sem brigar. Prefira isso a substituir arquivos.
- Scripts e localização: **UTF-8 com BOM** (o `validate.py` exige).
- Localização: `l_english:` / `l_braz_por:` na primeira linha, chaves
  `chave:0 "texto"`. Toda chave usada em GUI/JE/decision precisa existir.
- Pastas de dados do usuário (Linux nativo costuma ser
  `~/.local/share/Paradox Interactive/Victoria 3/`; confirme e anote em
  `ambiente-local.md`): `mod/` (mods), `logs/error.log` (erros do script),
  `docs/` (documentação exportada pelo jogo).

## 2. Protocolo "nunca suponha" — verificar qualquer primitiva

Antes de usar um efeito/trigger/escopo **novo** (que ainda não aparece no mod):

1. **Procure no jogo base** (leitura apenas):
   `grep -rn "nome_do_efeito" "<game>/common" "<game>/events" | head`
   Veja em qual escopo (país, estado, prédio...) ele é usado e com quais
   parâmetros. Copie a *forma* de uso real, não invente.
2. **Procure na documentação exportada** (`docs/` do usuário; o jogo gera com
   o comando `script_docs` no console em modo debug; `dump_data_types` gera os
   tipos de dados). Liste a pasta e use `grep`; os nomes dos arquivos variam
   por versão. Confirme escopo de entrada e argumentos.
3. **Rode o `vic3-tiger`** no mod. Ele lê o jogo base + o mod e acusa itens
   inexistentes, escopo errado e localização faltando
   (`vic3-tiger "<pasta do mod>"`; opções `--game <pasta do jogo>`,
   `--config vic3-tiger.conf`, `--suppress baseline.json`). Ele é mais novo
   que o ck3-tiger e pode dar falso positivo: um aviso do tiger se confronta
   com o jogo base, não se obedece às cegas.
4. Só então escreva. Se 1–3 não confirmam: marque **NÃO VERIFICADO**,
   implemente atrás de teste de engine e anote em `docs/STATUS.md`.
5. **Depois de carregar no jogo**, leia `logs/error.log`. Erro do script
   aparece lá. Sem erro no log ≠ funciona; só significa que carregou.

**Limite de tentativas:** se duas hipóteses seguidas falharem, PARE de
tentar variações. Colete evidência (error.log, docs, exemplo do jogo base) ou
peça ao usuário uma checagem rápida no jogo. Não gaste uma sessão inteira
adivinhando.

## 3. Ciclo de trabalho deste repositório (Smart Economy Director)

**Os arquivos de `common/`, `events/` e `gui/` são GERADOS por
`tools/build_mod.py`. Nunca edite esses arquivos à mão** — o validador acusa
"Generated file differs". Edite o gerador (e `data/*.json`, quando for o caso),
depois regenere.

```bash
python3 tools/build_mod.py                      # gera os arquivos do mod
python3 tools/build_mod.py --check              # confirma sincronia
python3 tools/validate.py --game "<pasta game>" # validação estática local
vic3-tiger "<pasta do mod>"                     # validação contra o vanilla
python3 -m unittest discover -s tests -v        # ~2 min, centenas de testes
python3 tools/package_mod.py                    # zip em dist/
# instalar: jogo FECHADO + backup; ver docs/INSTALL.md (tools/install_mod.py)
```

Regras:
- Uma mudança lógica por vez. Gere, valide e teste antes da próxima.
- Mudou comportamento ⇒ escreva/ajuste teste em `tests/` **no mesmo commit**.
- `tests/script_harness.py` roda a lógica aritmética/controle do script em
  Python. **Não emula o jogo e não valida nomes de primitivas.** Teste
  passando = lógica coerente, não = aceito pela engine.
- Dados do jogo (coeficientes, PMs, custos) vêm do vanilla local 1.15 via
  `tools/build_economy_data.py`/`data/`. Não digite números de memória.
- Mexeu na versão ⇒ sincronize `descriptor.mod`, `.metadata/metadata.json`,
  nome do pacote (`dist/…`), README e docs. Versões divergentes já aconteceram.
- Um commit/PR por entrega, mensagem dizendo o que mudou e o que ficou
  não verificado.

## 4. Categorias de evidência (use estas palavras exatas nos docs)

| Rótulo | Significa |
| --- | --- |
| Código | implementado no gerador |
| Teste sintético | passa no `script_harness`/unittest |
| Estático | passa `validate.py` e/ou `vic3-tiger` |
| Carregou | jogo iniciou e o `error.log` não cita o mod |
| Campanha | observado funcionando num save real (descreva qual save/data) |

Nunca escreva "funciona" para algo que só chegou em "Teste sintético".

## 5. Armadilhas comuns

- **Escopo errado.** Efeito de estado dentro de escopo de país (ou o
  contrário) falha em silêncio ou vira erro no log. Confirme o escopo na doc.
- Variáveis: ler com `var:nome`, gravar com `set_variable`/`change_variable`.
  Variável ausente precisa de `has_variable` antes.
- Efeitos fiscais/de efeito colateral (impostos, salários, leis) exigem
  snapshot + restauração + teste de save/reload. Nunca altere sem caminho de volta.
- Mexer na fila de construção: grave o valor antes, aplique, confira se
  subiu depois. Só então registre a ação como feita.
- Arquivo sem BOM, chave de localização faltando ou ID duplicado.
- Editar arquivo gerado à mão (será sobrescrito e quebra o `--check`).
- Confiar em mod de terceiro sem ler o que ele faz: leia os arquivos dele
  (pasta do Workshop) antes de integrar.
- Documentação da wiki pode estar desatualizada: o `docs/` exportado e os
  arquivos do jogo base têm prioridade.

## 6. Teste na engine (quando o usuário puder rodar)

Peça sempre **um roteiro curto e específico**, não "testa aí". Use
`docs/MANUAL_RUNTIME_TEST.md` como base. Formato:
1. Save de teste (cópia), jogo com o mod, modo debug se necessário.
2. Passos numerados com resultado esperado em cada um.
3. Quais arquivos devolver: trecho do `logs/error.log`, captura da tela do
   diário, e o save se for preciso inspecionar variáveis.
Prioridade de teste: **save/reload no modo Automático** > restauração de
opções ao sair do modo > efeitos fiscais > o resto.

## 7. Ritual de fim de sessão (obrigatório)

1. Atualize o **bloco de estado no topo** de `docs/AI_CONTEXT.md`
   (máx. ~40 linhas): versão, o que foi feito, o que está NÃO VERIFICADO,
   próximo passo exato, armadilhas descobertas hoje.
2. Histórico detalhado vai para `docs/PHASE_LOG.md`, não para o topo.
3. Atualize `docs/STATUS.md` com os rótulos da seção 4.
4. Se descobriu algo sobre o ambiente (caminho, comando, comportamento do
   jogo), grave em `references/ambiente-local.md` para não redescobrir.
5. Commit com tudo isso junto.

## 8. Fontes de consulta

Ver `references/fontes.md` (wiki, dev diaries, tiger, mods abertos para ler).
