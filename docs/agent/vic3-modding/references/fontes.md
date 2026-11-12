# Fontes de consulta para modding de Victoria 3

Ordem de confiança: **jogo base e `docs/` exportado > tiger > wiki/fórum > mods de terceiros**.

## 1. Verdade absoluta (sempre local)
- Pasta `game/` do Victoria 3 instalado (só leitura): exemplos reais de tudo.
  `grep -rn "<nome>" "<game>/common" "<game>/events" "<game>/gui"`
- Documentação exportada pelo jogo (comando `script_docs` no console em modo
  debug; `dump_data_types` para tipos de dados). Cai na pasta `docs/` dos
  dados do usuário. Lista efeitos, triggers, escopos e modificadores válidos.
- `logs/error.log` dos dados do usuário: erros reais de carregamento.

## 2. Validador
- **vic3-tiger** (amtep/tiger, também empacotado junto do ck3-tiger):
  https://github.com/amtep/tiger — baixe o release ou compile com
  `cargo build --release -p vic3-tiger`. Uso: `vic3-tiger "<pasta do mod>"`.
  Opções: `--game <pasta>`, `--config <arquivo.conf>`, `--suppress baseline.json`.
  Mais novo que o ck3-tiger; pode dar falso positivo.
- Extensão VS Code do Tiger (unLomTrois/ck3tiger-for-vscode) e GitHub Action
  (kaiser-chris/tiger-action-public) para rodar no CI.
- paradox-modding-toolkit (JDeffner): https://github.com/JDeffner/paradox-modding-toolkit
  — extensão de editor que integra o vic3-tiger e usa schema derivado do jogo.
- cwtools-vic3-config (kaiser-chris): configuração do CWTools para Victoria 3.

## 3. Documentação e tutoriais
- Wiki oficial de modding: https://vic3.paradoxwikis.com (pode estar
  desatualizada em páginas de modifiers; cruze com o `docs/` exportado).
- Dev Diary #60 (Modding): estrutura de pastas e uso do `error.log`
  https://paradoxinteractive.com/games/victoria-3/news/victoria-3-dev-diary-60-modding
- Dev Diary #120 (novidades de script no 1.7): exportação de documentação,
  modifiers e widgets scriptados.
- Skill de terceiros para agentes (qualidade não avaliada, leia antes de usar):
  https://smithery.ai/skills/trotsky1997/victoria3-mod-dev

## 4. Mods abertos para ler como exemplo
- Tópico `victoria3` no GitHub: https://github.com/topics/victoria3
- dragon-archer/vic3-mods (MIT; economia, PMs automáticos, UI).
- Mods que o Director integra (Economy Advisor, Supply Chain Semi-Auto
  Builder): leia os arquivos instalados do Workshop antes de mexer na integração.

## 5. Como usar
Antes de pesquisar na web, procure localmente (item 1). Só vá à wiki/fórum
quando o jogo base não tiver exemplo. Qualquer coisa tirada de fonte externa
vale como **hipótese** até passar pelo protocolo da seção 2 do SKILL.md.
