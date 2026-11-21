#!/usr/bin/env python3
"""Inicializa um repositório gerado a partir do template-moodle-plugin.

Troca os marcadores ({{OWNER}}, {{TITLE}}...) e o componente de exemplo ``local_newplugin`` pelos valores
do novo plugin, renomeia os arquivos e, por fim, apaga este script.

Uso (na raiz do repositório recém-criado):

    python template_init.py                      # pergunta o que não conseguir deduzir
    python template_init.py --component tool_meuplugin --title "Meu plugin" --description "..." --yes
    python template_init.py --dry-run            # mostra o que mudaria, sem alterar nada

Sem dependências externas: só a biblioteca padrão do Python 3.10+.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SELF = Path(__file__).resolve()
SKIP_DIRS = {".git", "node_modules", "vendor", ".venv", "venv", "__pycache__", "_build", "_site", "dist"}
TEMPLATE_BLOCK = re.compile(r"<!-- template:start -->.*?<!-- template:end -->\n*", re.S)
RST_UNDERLINE = re.compile(r"^([=\-~^\"'`#*+])\1+$")

EXAMPLE_COMPONENT = "local_newplugin"
COMPONENT_RE = re.compile(r"^[a-z][a-z0-9]*_[a-z][a-z0-9_]*[a-z0-9]$")

# Pasta de instalação de cada tipo de plugin (relativa à raiz do Moodle, ou a public/ no Moodle 5.1+).
INSTALL_DIRS = {
    "antivirus": "lib/antivirus",
    "assignfeedback": "mod/assign/feedback",
    "assignsubmission": "mod/assign/submission",
    "auth": "auth",
    "availability": "availability/condition",
    "block": "blocks",
    "customfield": "customfield/field",
    "datafield": "mod/data/field",
    "editor": "lib/editor",
    "enrol": "enrol",
    "filter": "filter",
    "format": "course/format",
    "gradeexport": "grade/export",
    "gradereport": "grade/report",
    "local": "local",
    "media": "media/player",
    "message": "message/output",
    "mod": "mod",
    "profilefield": "user/profile/field",
    "qbank": "question/bank",
    "qtype": "question/type",
    "quizaccess": "mod/quiz/accessrule",
    "report": "report",
    "repository": "repository",
    "theme": "theme",
    "tiny": "lib/editor/tiny/plugins",
    "tool": "admin/tool",
}


def git(*args: str) -> str:
    """Executa um comando git na raiz e devolve a saída (vazia se o git falhar)."""
    try:
        result = subprocess.run(  # noqa: S603 - argumentos fixos, git do PATH do desenvolvedor
            ["git", *args],  # noqa: S607
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return ""
    return result.stdout.strip()


def remote_owner_repo() -> tuple[str, str]:
    """Deduz dono e nome do repositório pela URL do remoto ``origin``."""
    match = re.search(r"[:/]([^/:]+)/([^/]+?)(?:\.git)?/?$", git("remote", "get-url", "origin"))
    return (match.group(1), match.group(2)) if match else ("", "")


def ask(label: str, default: str, interactive: bool) -> str:
    """Pergunta um valor no terminal, usando o padrão quando não houver resposta."""
    if not interactive:
        return default
    answer = input(f"{label} [{default}]: ").strip() if default else input(f"{label}: ").strip()
    return answer or default


def iter_paths() -> list[Path]:
    """Lista arquivos e pastas do repositório, ignorando .git, dependências e saídas de build."""
    paths = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts) or path == SELF:
            continue
        paths.append(path)
    return paths


def fix_rst_underlines(text: str) -> str:
    """Ajusta o sublinhado dos títulos reStructuredText ao novo tamanho do título."""
    lines = text.split("\n")
    for i in range(1, len(lines)):
        title = lines[i - 1]
        if title.strip() and not RST_UNDERLINE.match(title) and RST_UNDERLINE.match(lines[i]):
            lines[i] = lines[i][0] * max(len(title), 3)
    return "\n".join(lines)


def apply(replacements: dict[str, str], dry_run: bool) -> None:
    """Troca os marcadores no conteúdo e nos nomes dos arquivos."""
    ordered = sorted(replacements.items(), key=lambda item: -len(item[0]))
    for path in iter_paths():
        if not path.is_file():
            continue
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            continue  # binário (imagens, fontes...)
        new = text
        for old, value in ordered:
            new = new.replace(old, value)
        new = TEMPLATE_BLOCK.sub("", new)
        if path.suffix == ".rst":
            new = fix_rst_underlines(new)
        if new != text:
            print(f"  editado:   {path.relative_to(ROOT).as_posix()}")
            if not dry_run:
                path.write_bytes(new.encode("utf-8"))
    for path in sorted(iter_paths(), key=lambda p: len(p.parts), reverse=True):
        name = path.name
        for old, value in ordered:
            name = name.replace(old, value)
        if name != path.name:
            print(f"  renomeado: {path.relative_to(ROOT).as_posix()} -> {name}")
            if not dry_run:
                path.rename(path.with_name(name))


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    owner, repo = remote_owner_repo()
    default_component = repo.removeprefix("moodle-") if COMPONENT_RE.match(repo.removeprefix("moodle-")) else ""

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--component", default=default_component, help="ex.: tool_meuplugin (padrão: nome do repo)")
    parser.add_argument("--owner", default=owner, help="organização ou usuário do GitHub (padrão: remoto origin)")
    parser.add_argument("--title", default="", help="nome legível do plugin (pluginname)")
    parser.add_argument("--description", default="", help="descrição curta, em inglês")
    parser.add_argument("--author", default=git("config", "user.name"))
    parser.add_argument("--email", default=git("config", "user.email"))
    parser.add_argument("--yes", action="store_true", help="não pergunta nada; usa argumentos e padrões")
    parser.add_argument("--dry-run", action="store_true", help="só mostra o que mudaria")
    args = parser.parse_args()

    interactive = not args.yes and sys.stdin.isatty()
    component = ask("Componente (tipo_nome)", args.component, interactive)
    if not COMPONENT_RE.match(component):
        print(f"erro: componente inválido {component!r}; use o formato tipo_nome, ex.: tool_meuplugin", file=sys.stderr)
        return 2
    plugintype, name = component.split("_", 1)
    if plugintype not in INSTALL_DIRS:
        print(
            f"erro: tipo de plugin desconhecido {plugintype!r}; tipos aceitos: {', '.join(INSTALL_DIRS)}",
            file=sys.stderr,
        )
        return 2
    values = {
        "{{OWNER}}": ask("Dono no GitHub", args.owner, interactive),
        "{{TITLE}}": ask("Nome legível", args.title or name.replace("_", " ").capitalize(), interactive),
        "{{DESCRIPTION}}": ask("Descrição curta (inglês)", args.description or "Moodle plugin.", interactive),
        "{{AUTHOR}}": ask("Autor", args.author, interactive),
        "{{EMAIL}}": ask("E-mail do autor", args.email, interactive),
        "{{YEAR}}": str(date.today().year),
        "{{INSTALL_PATH}}": f"{INSTALL_DIRS[plugintype]}/{name}",
    }
    missing = [key for key, value in values.items() if not value]
    if missing:
        print(f"erro: informe {', '.join(missing)} (veja --help)", file=sys.stderr)
        return 2
    values[EXAMPLE_COMPONENT] = component

    print(f"Inicializando {component} ({values['{{INSTALL_PATH}}']}){' [dry-run]' if args.dry_run else ''}")
    apply(values, args.dry_run)
    if not args.dry_run:
        SELF.unlink()
        steps = ["Revise as mudanças com `git status` e `git diff`."]
        if plugintype not in ("local", "tool"):
            steps.append(
                f"Plugins do tipo {plugintype} exigem arquivos próprios (lib.php, db/access.php...): "
                "veja https://moodledev.io/docs/apis/plugintypes"
            )
        steps.append("Ative o GitHub Pages (Settings > Pages > Source: GitHub Actions) para publicar a documentação.")
        steps.append("Faça o commit inicial do plugin.")
        print("\nPronto. Próximos passos:")
        for number, step in enumerate(steps, 1):
            print(f"  {number}. {step}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
