# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import tomllib

base_path = os.path.realpath(os.path.sep.join([".." for _ in range(2)]))
src_path = os.path.join(base_path, "src")
sys.path.insert(
    0,
    src_path
)

project = 'etautil'
copyright = '2023, Ella Jameson'
author = 'Ella Jameson'

with open(os.path.join(base_path, "pyproject.toml"), "rb") as f:
    pyproject_toml = tomllib.load(f)
version = pyproject_toml["project"]["version"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'autoapi.extension',
    'sphinx_rtd_theme'
]
autoapi_dirs = [src_path]
autoapi_options = [
    'members',
    'undoc-members',
    #'private-members'
    'show-inheritance',
    'show-module-summary',
    'special-members',
    'imported-members'
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'display_version': True
}
html_static_path = ['_static']