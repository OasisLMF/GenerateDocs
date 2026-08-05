"""Sphinx config for the aggregated Oasis documentation *landing* page.

GenerateDocs is now a version-pinned orchestrator (see ``orchestrate.py`` + ``modules.json``):
each component's documentation is built from its own repository and assembled under this
landing. This config therefore builds only the thin landing/index — it holds no component
content and needs none of the per-repo extensions (autoapi, redoc, jsonschema, …).
"""
import datetime

project = "Oasis LMF Documentation"
author = "Oasis LMF"
copyright = f"{datetime.date.today().year} Oasis LMF"

extensions = [
    "myst_parser",
    "sphinx_design",       # cards grid on the landing page
    "sphinx_copybutton",
    "sphinx.ext.intersphinx",
]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
master_doc = "index"
language = "en"
templates_path = ["_templates"]
exclude_patterns = ["_build", "**.ipynb_checkpoints"]

myst_enable_extensions = ["colon_fence", "deflist", "substitution"]

html_theme = "furo"
html_title = "Oasis LMF Documentation"

# Cross-links into the component sites. Each module publishes objects.inv at its sub-path in
# the assembled site; point intersphinx at the built inventories when cross-referencing.
# (Populated by CI from modules.json; left empty here so the landing builds standalone.)
intersphinx_mapping = {}
# -- Oasis shared branding (logo, palette, GitHub footer) -------------------
if globals().get("html_theme") == "furo":
    if "_static" not in (globals().get("html_static_path") or []):
        html_static_path = list(globals().get("html_static_path") or []) + ["_static"]
    try:
        html_theme_options
    except NameError:
        html_theme_options = {}
    html_theme_options.setdefault("light_logo", "OASIS_LMF_COLOUR.png")
    html_theme_options.setdefault("dark_logo", "OASIS_LMF_WHITE.png")
    _lcv = html_theme_options.setdefault("light_css_variables", {})
    _lcv.setdefault("color-brand-primary", "#862633")
    _lcv.setdefault("color-brand-content", "#d22630")
    _lcv.setdefault("font-stack", "Raleway, sans-serif")
    _dcv = html_theme_options.setdefault("dark_css_variables", {})
    _dcv.setdefault("color-brand-primary", "#e2919b")
    _dcv.setdefault("color-brand-content", "#ef8b93")
    # GitHub link — Furo's conventional spot is the footer icons (bottom of every page)
    html_theme_options.setdefault("footer_icons", [{
        "name": "GitHub", "url": "https://github.com/OasisLMF", "class": "",
        "html": '<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path></svg>',
    }])
    if "https://fonts.googleapis.com/css?family=Raleway" not in (globals().get("html_css_files") or []):
        html_css_files = list(globals().get("html_css_files") or []) + ["https://fonts.googleapis.com/css?family=Raleway"]
