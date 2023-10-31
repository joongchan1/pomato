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
import os, sys
sys.path.insert(0, os.path.abspath('../'))
# sys.path.append('C:/Users/riw/tubCloud/Uni/Market_Tool/pomato/')

# -- Project information -----------------------------------------------------
project = 'POMATO'
copyright = '2023, riw'
author = 'riw, rom'

# The full version, including alpha/beta/rc tags
release = '0.5.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autosummary", "sphinx.ext.autodoc", "numpydoc"]
autosummary_generate = False
autosummary_imported_members = True
numpydoc_show_inherited_class_members = False 
numpydoc_show_class_members = False 

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
master_doc = 'index'
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# exclude_patterns = ["code_trunk*"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'searchbox.html',
        'donate.html',
    ]
}
html_title = 'POMATO'
html_short_title = 'POMATO'
html_theme_options = {
    'logo': 'graphics/pomato_space.png',
    'logo_name': False,
    "sidebar_width": "220px",
    "page_width": "1080px",
    "extra_nav_links": {
    	"Github": "https://github.com/richard-weinhold/pomato"},
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']