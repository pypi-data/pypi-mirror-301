# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath(os.sep.join(['..','..','src','KiMoPack'])))
sys.path.insert(0, os.path.abspath(os.sep.join(['src','KiMoPack'])))
sys.path.insert(0, os.path.abspath(os.sep.join([os.getcwd(),'src','KiMoPack'])))

# -- Project information -----------------------------------------------------

project = 'KiMoPack'
copyright = '2022, Jens Uhlig'
author = 'Jens Uhlig'

# The full version, including alpha/beta/rc tags
release = '7.4.9'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.napoleon','sphinx.ext.autosectionlabel','sphinx.ext.autodoc','sphinx.ext.viewcode','sphinx.ext.autosummary']
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
autosummary_generate = True
numpydoc_show_class_members = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ['custom.css',]
html_logo = '_static/KiMoPack_logo.png'
html_theme_options = {
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': 'white',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
    'logo_only': False,
}