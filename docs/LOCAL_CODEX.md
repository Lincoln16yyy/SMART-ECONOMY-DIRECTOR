# Continuar no computador local — CachyOS

**Documento histórico de transição da nuvem.** Os caminhos abaixo foram
confirmados localmente depois desta instrução. Para continuar hoje, use
[AUDIT_2026-11-09.md](AUDIT_2026-11-09.md), especialmente o mapa de diretórios e
o próximo bloco de pesquisa. O código atual é 0.4.1, com limitações de fila e
validação de execução; não está mais no estado “sem implementação”. As
instruções antigas abaixo foram preservadas como registro.


A sessão na nuvem não acessa automaticamente os discos do computador. O Codex CLI abre uma sessão local separada, capaz de trabalhar com os arquivos que você autorizar. Login não transfere esta conversa; o contexto está versionado neste repositório.

## Instalar e abrir

Se ainda não houver Node.js, npm e Git:

```bash
sudo pacman -S nodejs npm git
```

Instale o CLI e inicie:

```bash
npm install -g @openai/codex
codex
```

Faça login pela opção oferecida pelo aplicativo. Se o npm reclamar de permissão no diretório global, não use `sudo npm`: configure um prefixo do seu usuário:

```bash
mkdir -p "$HOME/.local"
npm install -g --prefix "$HOME/.local" @openai/codex
export PATH="$HOME/.local/bin:$PATH"
codex
```

O `export` vale para esse terminal; para uso futuro, adicione o diretório ao PATH pela configuração do seu shell. Projeto oficial do CLI: https://github.com/openai/codex . Não cole tokens em conversas.

## Abrir o projeto

Se ainda não tiver uma cópia local:

```bash
mkdir -p "$HOME/Projetos"
cd "$HOME/Projetos"
git clone https://github.com/Lincoln16yyy/SMART-ECONOMY-DIRECTOR.git
cd SMART-ECONOMY-DIRECTOR
codex
```

Se já tiver uma cópia, use-a e confira `git status` antes de atualizar; preserve alterações locais. Execute o Codex dentro da pasta do projeto. O acesso de leitura e escrita depende das permissões da sessão local; mantenha as aprovações e conceda acesso somente aos diretórios necessários quando solicitado. Não precisa executar o Codex como root.

## Mensagem para a sessão local

Copie este pedido para o Codex local:

> Continue a Fase 0 do Smart Economy Director. Leia README.md, docs/PROJECT_BRIEF.md, docs/AI_CONTEXT.md, docs/RESEARCH.md, docs/COMPATIBILITY.md e docs/PHASE_LOG.md. O Smart Government foi estudado no commit 95b20870816b9ceabcaf0b7b9371a66c85dd8bf1; 26 testes estáticos dele passaram na nuvem, mas o jogo e os mods não estavam disponíveis lá. Localize no meu computador a instalação real do Victoria 3 1.15, os dados do usuário e os mods instalados, principalmente Economy Advisor. Os caminhos históricos abaixo são apenas pistas. Inspecione os scripts e a configuração ativa, documente evidências, unidades, escopos e capacidades, e apresente o diagnóstico consolidado antes de implementar. Não altere o jogo, saves ou load order nesta pesquisa; não publique arquivos proprietários ou dados pessoais no GitHub. Continue atualizando a documentação do Director no GitHub com os resultados verificados.

Pistas históricas, registradas no Smart Government e ainda não confirmadas nesta entrega:

- Jogo: `/home/lincoln-ii/Games/Victoria 3`
- Prefixo: `/home/lincoln-ii/.config/hydralauncher/wine-prefixes/529340`
- Dados: subdiretório `drive_c/users/steamuser/Documents/Paradox Interactive/Victoria 3` desse prefixo.
- Economy Advisor: `/home/lincoln-ii/Downloads/3778129206_Economy_Advisor/3778129206 Economy Advisor/`

A sessão local deve verificar os caminhos em vez de assumi-los. Não envie a instalação inteira para o GitHub.
