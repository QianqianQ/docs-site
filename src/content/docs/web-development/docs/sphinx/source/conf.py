#!/usr/bin/env python3
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'docs'
copyright = 'TEST'  # pylint: disable=W0622
author = 'tester'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.duration',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'myst_parser'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}
html_theme_options = {
    'logo_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': 'white',
    'flyout_display': 'hidden',
    'version_selector': False,
    'language_selector': False,
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': -1,
    'titles_only': False,
}
# myst_parser configuration
myst_heading_anchors = 6

rst_prolog = """
.. role:: raw-html(raw)
   :format: html
"""

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
html_css_files = ["custom.css"]
html_logo = "_static/images/xxx.png"
html_favicon = '_static/images/xxx.png'
html_show_sphinx = False
