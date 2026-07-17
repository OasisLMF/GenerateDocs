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
