# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/stable/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import datetime
from sphinx.ext import autodoc
from recommonmark.parser import CommonMarkParser

sys.path.insert(0, os.path.abspath('../modules/OasisLMF'))
sys.path.insert(0, os.path.abspath('../modules/OasisPlatform'))

#import src.server.app

# -- Project information -----------------------------------------------------

project = u'Oasis LMF'
author = u'Oasis LMF'
year_now = datetime.date.today().year
# copyright = u'2023, Oasis LMF'
copyright = str(year_now) + ' Oasis LMF'

# # The short X.Y version
# version = u''
# # The full version, including alpha/beta/rc tags
# release = u'1.0.0'


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinxcontrib.httpdomain',
    # 'sphinxcontrib.autohttp.flask',
    # 'sphinxcontrib.autohttp.flaskqref',
    'sphinx-jsonschema',
    'nbsphinx',
    'sphinx.ext.mathjax',
    "sphinxcontrib.youtube",
    # 'm2r',
    # 'autoapi.extension',
    # 'recommonmark'
    'sphinx-jsonschema',
]

autoapi_dirs = [
    '../modules/OasisLMF/oasislmf',
    '../modules/OasisPlatform/src',
    ]
autoapi_add_toctree_entry = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates/layout.html']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
# source_parsers = {
#     '.md': CommonMarkParser,
# }
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ['_build', '**.ipynb_checkpoints']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'friendly'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'
html_logo = 'images/OASIS_LMF_COLOUR.png'
html_static_path = ['_static']
html_title = "Oasis LMF Documentation"

html_css_files = [
    'https://fonts.googleapis.com/css?family=Raleway',
]


# -- Options for JSON table output in settings sections -------------------------------------------------

jsonschema_options = {
    'lift_title': False,
}


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'logo_only': True,
    'display_version': False,
    'logo_link': '<https://github.com/OasisLMF>',

    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/OasisLMF",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"></path>
                </svg>
            """,
            "class": "",
        },
    ],

    "light_css_variables": {
        "color-brand-primary": " #862633",
        "color-brand-content": "#d22630",
        "font-stack": "Raleway, sans-serif",
        "font-stack--monospace": "Courier, monospace",
    }
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}
# html_sidebars = {
#     '**': {
#         'layout.html',
#         "sidebar/scroll-start.html",
#         "sidebar/brand.html",
#         "sidebar/search.html",
#         "sidebar/navigation.html",
#         "sidebar/ethical-ads.html",
#         "sidebar/scroll-end.html",
#         "sidebar/variant-selector.html",
#     }
# }


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'OasisLMFdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'OasisLMF.tex', u'Oasis LMF Documentation',
     u'Oasis LMF', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'oasislmf', u'Oasis LMF Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'OasisLMF', u'Oasis LMF Documentation',
     author, 'OasisLMF', 'One line description of project.',
     'Miscellaneous'),
]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


class CliDocumenter(autodoc.ClassDocumenter):
    objtype = "cli"

    #do not indent the content
    content_indent = ""

    #do not add a header to the docstring
    def add_directive_header(self, sig):
        pass


def setup(app):
    app.add_autodocumenter(CliDocumenter)
