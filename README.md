# Smart Economy Director — Victoria 3 1.15

Versão de desenvolvimento **0.3.3 — diagnóstico, duas ações aprovadas e
explicação de bloqueios**. O mod tem diário próprio, leituras manuais ou mensais, recomendações
limitadas de infraestrutura e capacidade de construção, e botões para aprovar a
expansão de uma ferrovia elegível ou de um setor de construção operante. Quando
não há candidato, o painel decompõe os estados por motivo principal; quando o
botão de aprovação está bloqueado, o painel indica qual guarda falhou (pausa,
fila privada, inadimplência, saldo ou recomendação desatualizada). Não há
execução econômica automática.

O painel mostra finanças, PIB, população, padrão de vida, alfabetização,
capacidade de construção, filas e sinais de infraestrutura, abastecimento e
contratação. Os dados correspondem à última leitura indicada no painel.
O crescimento do PIB requer amostras em meses distintos.

**Estado: a interface, os indicadores, os estados vazios das seções, a
ocultação correta da decomposição de motivos, a atualização sob
solicitação, a desativação e a renderização do candidato de construção
foram confirmados em campanha (0.3.0/0.3.1). A execução dos botões
ferroviário e do setor de construção, a decomposição com déficit
presente e a linha de motivo do botão bloqueado da 0.3.2 ainda precisam
ser conferidas no jogo normal.** Compatibilidade
ampliada continua pendente. Não é uma versão de automação econômica pronta
para deixar uma campanha sozinha. A nova mensagem de recomendação desatualizada
ainda precisa ser conferida na engine.

## Instalação e uso

Consulte [instalação e geração do ZIP](docs/INSTALL.md). O pacote gerado em
`dist/smart-economy-director-0.3.3.zip` contém a pasta do mod e o descritor
externo. Ative no launcher e use a decisão **Ativar Smart Economy Director**.
Nenhum outro mod é obrigatório; nenhuma ativação econômica é automática.

## Desenvolvimento e verificação

```bash
python3 tools/build_mod.py
python3 tools/build_mod.py --check
python3 tools/validate.py --game "/caminho/Victoria 3/game"
python3 -m unittest discover -s tests -v
python3 tools/package_mod.py
```

Requer Python 3.10+ e somente a biblioteca padrão. Os scripts usam o prefixo
`sed_`, português brasileiro e fallback inglês. Não sobrescrevem arquivos
originais nem escrevem em variáveis de terceiros. Testes estáticos não
substituem a validação no motor do jogo.

## Documentação

- [Entrega, arquitetura implementada e limites da Fase 1](docs/PHASE1.md)
- [Requisitos originais completos](docs/PROJECT_BRIEF.md)
- [Pesquisa técnica](docs/RESEARCH.md)
- [Arquitetura por fases](docs/ARCHITECTURE.md)
- [Compatibilidade](docs/COMPATIBILITY.md)
- [Métricas e fontes](docs/METRICS.md)
- [Auditoria local de mods e saves](docs/LOCAL_AUDIT.md)
- [Relatório estruturado da auditoria](docs/ENVIRONMENT_AUDIT.json)
- [Inventário inicial de fontes](docs/SOURCE_INVENTORY.json)
- [Contexto para continuidade](docs/AI_CONTEXT.md)
- [Registro de fases](docs/PHASE_LOG.md)
- [Testes de campanha e da interface](docs/MANUAL_RUNTIME_TEST.md)
- [Resultado do teste de inicialização na engine](docs/RUNTIME_SMOKE.md)

A [pesquisa anterior na nuvem](docs/RESEARCH_CLOUD.md) e as
[instruções de continuidade local](docs/LOCAL_CODEX.md) foram preservadas.
PMs continuam sob responsabilidade dos outros mods. Os botões do Director só
adicionam um nível público após aprovação e checagens atuais; não ativam um
construtor periódico. A recomendação do setor de construção exige fila pública
com pelo menos três projetos e não promete contratação futura.
