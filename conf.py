# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Micro_Python'
copyright = '2026, pf'
author = 'Peter Fabo'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_nb",
              "sphinx_copybutton",
              "sphinx_design",
              "sphinx_subfigure",
              "sphinxcontrib.plantuml",
              "sphinx.ext.graphviz",
              "sphinx_togglebutton",
              "sphinxcontrib.tikz"
              ]

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

myst_url_schemes = ("http", "https", "mailto")

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

numfig = True

numfig_format = {
    'code-block': 'Listing %s.',
    'figure': 'Obr. %s',
    'section': 'Section',
    'table': 'Tabulka %s',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
#html_static_path = ['_static']
html_logo = "logo_411.png"

plantuml = ["java", "-jar", "./plantuml/plantuml-1.2026.2.jar"]
