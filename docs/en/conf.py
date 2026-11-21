import moodle_docs_theme

project = "moodle-local_newplugin"
copyright = "{{YEAR}}, {{AUTHOR}}"
author = "{{AUTHOR}}"
release = "0.1.0"

extensions = [
    "sphinx.ext.githubpages",
    "moodle_docs_theme",
]

templates_path = []
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "en"

html_theme = "moodle_docs_theme"
html_theme_path = [moodle_docs_theme.get_html_theme_path()]

html_theme_options = {
    "primary_color": "#f98012",
    "secondary_color": "#6c336d",
    "project_name": "moodle-local_newplugin",
    "tagline": "{{DESCRIPTION}}",
    "github_url": "https://github.com/{{OWNER}}/moodle-local_newplugin",
    "github_repo": "{{OWNER}}/moodle-local_newplugin",
    "github_version": "main",
    "doc_path": "docs/en/",
    "show_edit_on_github": True,
    "enable_dark_mode": True,
    "navigation_links": "Home|index, Installation|installation, Usage|usage",
}

html_static_path = []
