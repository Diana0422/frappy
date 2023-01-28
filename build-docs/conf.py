# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys, os
import sphinx_rtd_theme

sys.path.append(os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Frappy'
copyright = '2023, Mattia Antonangeli, Diana Pasquali'
author = 'Mattia Antonangeli, Diana Pasquali'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx_rtd_theme','sphinx.ext.autodoc']
autodoc_default_options = {"members": True, "undoc-members": True, "private-members": True}
autodoc_member_order = 'bysource'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output




html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
