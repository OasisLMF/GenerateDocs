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
# -- Oasis shared branding (logo, palette, home link) -----------------------
import os as _os_brand
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
    _home = _os_brand.environ.get("OASIS_DOCS_HOME", "https://oasislmf.github.io/index.html")
    html_theme_options.setdefault(
        "announcement",
        '<a href="' + _home + '" style="color:inherit;font-weight:600;text-decoration:none">'
        '&#8962; Oasis documentation home</a>')
    if "https://fonts.googleapis.com/css?family=Raleway" not in (globals().get("html_css_files") or []):
        html_css_files = list(globals().get("html_css_files") or []) + ["https://fonts.googleapis.com/css?family=Raleway"]
