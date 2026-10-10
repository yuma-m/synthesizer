# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from importlib.metadata import version as get_version

# -- Project information -----------------------------------------------------

project = "synthesizer"
author = "Yuma Mihira"
copyright = "2017, Yuma Mihira"
release = get_version("synthesizer")
version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]

root_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
language = "en"

autodoc_member_order = "bysource"
todo_include_todos = True

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
