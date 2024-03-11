# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'eWaterCycle-HBV'
copyright = '2024, David Haasnoot'
author = 'David Haasnoot'

version = "1.4"
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
                'sphinx.ext.autodoc',
                "sphinx.ext.napoleon",
                "nbsphinx",
                "autoapi.extension",
                "sphinx_copybutton",
            ]

templates_path = ['_templates']

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

source_suffix = [".rst"]

html_sidebars = {
    "**": [
        "relations.html",  # needs 'show_related': True theme option to display
        "searchbox.html",
    ]
}

# Hacky way to 'remove' the cell count from the prompt.
# Inspired by https://github.com/spatialaudio/nbsphinx/issues/126
nbsphinx_prompt_width = "0"
nbsphinx_input_prompt = "%s         In:"
nbsphinx_output_prompt = "%s       Out:"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# -- Use autoapi.extension to run sphinx-apidoc -------
autoapi_dirs = ["../src"]
autoapi_python_class_content = "both"
autoapi_options = ["members", "undoc-members", "imported-members", "show-inheritance"]