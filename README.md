<!-- template:start -->
# template-moodle-plugin

Template de repositório para plugins Moodle (4.5 LTS e 5.3 LTS), com CI (`moodle-plugin-ci` em PostgreSQL e
MariaDB), documentação bilíngue (Sphinx + `moodle-docs-theme`, publicada no GitHub Pages), release em rascunho
verificada e envio opcional ao Moodle Marketplace.

## Como usar

1. Clique em **Use this template > Create a new repository**. Nomeie o repositório no padrão do Marketplace:
   `moodle-{tipo}_{nome}`, por exemplo `moodle-tool_meuplugin`.
2. Clone o repositório novo e rode o inicializador (só biblioteca padrão do Python 3.10+):

   ```bash
   python template_init.py
   ```

   Ele deduz o componente e o dono pelo remoto `origin`, pergunta nome, descrição e autor, troca os marcadores
   (`local_newplugin`, `{{OWNER}}`, `{{TITLE}}`...), renomeia os arquivos e se apaga. Use `--dry-run` para
   conferir antes e `--help` para ver todas as opções.
3. Ative o GitHub Pages em *Settings > Pages > Source: GitHub Actions*.
4. Para publicar no Marketplace depois da aprovação, crie a variável `MARKETPLACE_ENABLED=true`, o secret
   `MOODLE_MARKETPLACE_TOKEN` e o environment `marketplace` (veja `.github/workflows/moodle-release.yml`).

O exemplo é um plugin `local` mínimo e funcional (privacy provider e teste PHPUnit). Tipos como `mod`, `block`
e `tiny` exigem arquivos próprios: veja <https://moodledev.io/docs/apis/plugintypes>.

## Workflows

| Workflow | Quando | O que faz |
|---|---|---|
| `ci.yml` | push na `main` e PR | `moodle-plugin-ci`: phplint, phpcs, phpdoc, validate, savepoints, mustache, grunt e PHPUnit |
| `docs.yml` | push na `main` e PR | Gera `docs/en` e `docs/pt_BR` e publica no GitHub Pages |
| `release.yml` | manual | Confere versão, CHANGELOG e CI verde, monta o ZIP e cria a release em **rascunho** |
| `release-check.yml` | release publicada | Confere tag × `version.php`, ZIP idêntico ao código e CI verde |
| `moodle-release.yml` | tag `v*` | Envia ao Moodle Marketplace (desligado até `MARKETPLACE_ENABLED=true`) |

---
<!-- template:end -->
# moodle-local_newplugin

{{DESCRIPTION}}

[![CI](https://github.com/{{OWNER}}/moodle-local_newplugin/actions/workflows/ci.yml/badge.svg)](https://github.com/{{OWNER}}/moodle-local_newplugin/actions/workflows/ci.yml)

Documentation / Documentação: <https://{{OWNER}}.github.io/moodle-local_newplugin/>

## Requirements / Requisitos

- Moodle 4.5 LTS or 5.3 LTS
- PHP 8.1 or later

## Installation / Instalação

Download the ZIP from the [releases](https://github.com/{{OWNER}}/moodle-local_newplugin/releases) and install it at
*Site administration > Plugins > Install plugins*, or clone it into `{{INSTALL_PATH}}`
(`public/{{INSTALL_PATH}}` in Moodle 5.1+).

Baixe o ZIP nas [releases](https://github.com/{{OWNER}}/moodle-local_newplugin/releases) e instale em
*Administração do site > Plugins > Instalar plugins*, ou clone em `{{INSTALL_PATH}}`
(`public/{{INSTALL_PATH}}` no Moodle 5.1+).

## Release

1. Update `$plugin->version` and `$plugin->release` in `version.php` and add the section to `CHANGELOG.md`.
2. Run the **Prepare release** workflow: it creates a draft release with the ZIP.
3. Review the draft and click **Publish release**. **Verify published release** checks the result.

## License / Licença

[GNU GPL v3 or later](LICENSE).
