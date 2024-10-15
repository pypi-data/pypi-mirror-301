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
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../../'))

import coalispr.bedgraph_analyze
import coalispr.count_analyze
import coalispr.resources
import coalispr.resources.share
import coalispr.coalispr

### for sphinx
### from docs folder
## `make html`

# -- Project information -----------------------------------------------------
project = 'coalispr'
author = 'Rob van Nues'
# ends up in footer
# https://github.com/pradyunsg/furo/discussions/248
# change coding via _templates/page.html
copyright = '2022-2024'
# with https://creativecommons.org/licenses/by/4.0/ Creative Commons Attribution License , permitting free reuse provided the work is properly cited.
# release

# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc', 
    'autoapi.extension',
    'sphinx.ext.autosectionlabel',
   # 'sphinx.ext.imgconverter', # converts svg to png with imagemagick for latex2pdf
   # 'sphinxcontrib.inkscapeconverter', #sphinxcontrib.rsvgconverter #for latex conversion svg 2 png
   # 'sphinx_tabs.tabs', #tabs for different images instead of long panel?
]
autosectionlabel_prefix_document = False #True 
autosectionlabel_maxdepth = 1

# do not replace constant names for their values
autodoc_preserve_defaults = True

### For api-doc (not needed for autoapi)
### from main folder; -o is target _source, searched by make; exclude tests
### 1 page per module; -e; 
## `sphinx-apidoc -f -e -o docs/_source coalispr "coalispr/tests*"`
# Napoleon settings, for processing numpy style doc-strings; also helps autoapi.
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
## keep Notes as flat text instead of directive
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# -- AutoApi configuration ---------------------------------------------------
# Add any paths that contain templates here, relative to this directory.
templates_path = ['../_templates']
autoapi_dirs = ['../../coalispr']
autoapi_type = "python"
#patterns to ignore when finding files
autoapi_ignore = [
    #'*constant_in*', # contains '.make_constant.py'
    '*constant_out*', # contains duplicate definitions 
    '*migrations*',
    '*test*', 
]

# Use work-around with coalispr.api.rst to include __main__ in api-doc:
# refer directly by relative html-links to pages in generated modules-index
autoapi_add_toctree_entry = True #False # replaced with 'coalispr.api'.
suppress_warnings = ["autoapi"] #["autoapi.python_import_resolution", "autoapi.not_readable"]

# For autoapi optimazation acc. to Antoine Beyeler
# https://bylr.info/articles/2022/05/10/api-doc-with-sphinx-autoapi/
autoapi_options = [
    "show-module-summary",
    "members",
    "undoc-members",
    "show-inheritance",
    "imported-members",
]

autoapi_keep_files = True # causes errors after python upgrade or when files are not available.
# delete build dictionary contents; run 'make html' in a new Python session, ie new terminal!
autodoc_typehints = "none" #"signature"
#autoapi_python_use_implicit_namespaces = True

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# The theme to use for HTML and HTML Help pages.  
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['../_static']
 
html_theme_options = {
## on furo only: https://pradyunsg.me/furo/customisation/
## logo replaces project name in side bar
    "navigation_with_keys": True,
    "sidebar_hide_name": True,
    ## change witdh and height of optimised svg to 200
    "light_logo": "../_static/coalispr_logo_light_ed.svg",
    "dark_logo": "../_static/coalispr_logo_light_ed.svg",
## imitate github-link 
    # from https://pradyunsg.me/furo/customisation/footer/#using-embedded-svgs
    # use the browser’s developer tools to get the SVG directly from the page: inspect element + copy svg element (ctrl+c) + paste.
    "footer_icons": [
## simplified EUPL-logo for use as button; by author based on lettering original logo.
    # original from https://upload.wikimedia.org/wikipedia/commons/9/91/Logo_EUPL.svg
        {
            "name": "EUPL-1.2",
         #   "url": "https://opensource.org/licenses/EUPL-1.2",
            "url": "https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12",
                  "html": """
                 <svg width="1 em" height="1em" fill="currentColor" stroke="currentColor" stroke-width="0" viewBox="0 0 244 244"><path d="m171.44 216.81-0.11615-83.232 17.426-0.0243 0.0974 69.764 44.658-0.0623 0.0188 13.468zm-12.319-56.869q0.0112 8.0338-3.6425 14.36-3.6536 6.3258-10.501 9.8206-6.7885 3.4356-16.181 3.4487l-20.675 0.0289 0.0409 29.3-17.426 0.0243-0.11616-83.232 37.393-0.0522q14.945-0.0209 22.989 6.8793 8.1025 6.841 8.12 19.423zm-17.544 0.31983q-0.0183-13.114-15.495-13.092l-18.017 0.0251 0.0377 26.996 18.49-0.0258q7.2068-0.0101 11.101-3.5598 3.8938-3.6088 3.8844-10.343zm-15.163-44.633q-17.19 0.024-26.358-8.3514-9.1088-8.3755-9.1305-23.97l-0.07263-52.042 17.426-0.02432 0.0707 50.684q0.0138 9.865 4.6876 14.998 4.7328 5.0736 13.83 5.0609 9.3333-0.013 14.347-5.3365 5.0136-5.3825 4.9996-15.366l-0.0699-50.093 17.426-0.02432 0.0714 51.156q0.0221 15.831-9.7716 24.588-9.7347 8.6972-27.456 8.7219zm-115.31-1.0205-0.11616-83.232 65.452-0.09135 0.0188 13.468-48.025 0.06702 0.02918 20.911 44.422-0.062 0.0188 13.468-44.422 0.062 0.03058 21.916 50.447-0.0704 0.0188 13.468z"></svg>
            """,
            "class":"",
        },
## codeberg-logo_special_fake.svg; 'official' alternative to codeberg icon, inspired by jakeg; 
## reduced by svgo (https://github.com/svg/svgo) to codeberg-logo_special_fake2.svg
## see https://codeberg.org/Codeberg/Community/issues/976
## derived from https://codeberg.org/Codeberg/Design/src/branch/main/logo/special/codeberg-logo_special_fake-transaprency.svg
## see https://codeberg.org/Codeberg/Design/issues/80#issuecomment-878178
        {
            "name": "Codeberg",
            "url": "https://codeberg.org/coalispr/coalispr/",
            "html": """
                <svg width="1em" height="1em" viewBox="0 0 4.233 4.233"><path fill="currentColor" d="M46.984 76.122a2.117 2.117 0 0 0-1.793 3.242l1.764-2.282c.013-.016.045-.016.058 0l.736.953h-.527l.011.042h.55l.155.2h-.648l.018.067h.68l.138.177h-.769l.024.085h.81l.123.158h-.889l.03.103h.939l.107.139h-1.008l.032.115h1.065l.099.128H47.56l.033.115h1.184a2.117 2.117 0 0 0-1.793-3.242zm.645 3.37.032.114h.94a2.24 2.24 0 0 0 .09-.114zm.068.243.031.114h.629a2.54 2.54 0 0 0 .125-.114zm.067.242.032.115h.212c.063-.036.121-.073.184-.115z" style="paint-order:markers fill stroke" transform="translate(-44.867 -75.991)"/></svg>
            """,
            "class": "",
        },
## creative commons-logos 'FaCreativeCommons', 'FaCreativeCommonsBy'
    # from https://react-icons.github.io/react-icons/search/#q=creative
        {
            "name": "CreativeCommons-4.0",
            "url": "https://creativecommons.org/licenses/by/4.0/",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 496 512" height="1em" width="1em"><path d="M245.83 214.87l-33.22 17.28c-9.43-19.58-25.24-19.93-27.46-19.93-22.13 0-33.22 14.61-33.22 43.84 0 23.57 9.21 43.84 33.22 43.84 14.47 0 24.65-7.09 30.57-21.26l30.55 15.5c-6.17 11.51-25.69 38.98-65.1 38.98-22.6 0-73.96-10.32-73.96-77.05 0-58.69 43-77.06 72.63-77.06 30.72-.01 52.7 11.95 65.99 35.86zm143.05 0l-32.78 17.28c-9.5-19.77-25.72-19.93-27.9-19.93-22.14 0-33.22 14.61-33.22 43.84 0 23.55 9.23 43.84 33.22 43.84 14.45 0 24.65-7.09 30.54-21.26l31 15.5c-2.1 3.75-21.39 38.98-65.09 38.98-22.69 0-73.96-9.87-73.96-77.05 0-58.67 42.97-77.06 72.63-77.06 30.71-.01 52.58 11.95 65.56 35.86zM247.56 8.05C104.74 8.05 0 123.11 0 256.05c0 138.49 113.6 248 247.56 248 129.93 0 248.44-100.87 248.44-248 0-137.87-106.62-248-248.44-248zm.87 450.81c-112.54 0-203.7-93.04-203.7-202.81 0-105.42 85.43-203.27 203.72-203.27 112.53 0 202.82 89.46 202.82 203.26-.01 121.69-99.68 202.82-202.84 202.82z"></path></svg>
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 496 512" height="1em" width="1em"><path d="M314.9 194.4v101.4h-28.3v120.5h-77.1V295.9h-28.3V194.4c0-4.4 1.6-8.2 4.6-11.3 3.1-3.1 6.9-4.7 11.3-4.7H299c4.1 0 7.8 1.6 11.1 4.7 3.1 3.2 4.8 6.9 4.8 11.3zm-101.5-63.7c0-23.3 11.5-35 34.5-35s34.5 11.7 34.5 35c0 23-11.5 34.5-34.5 34.5s-34.5-11.5-34.5-34.5zM247.6 8C389.4 8 496 118.1 496 256c0 147.1-118.5 248-248.4 248C113.6 504 0 394.5 0 256 0 123.1 104.7 8 247.6 8zm.8 44.7C130.2 52.7 44.7 150.6 44.7 256c0 109.8 91.2 202.8 203.7 202.8 103.2 0 202.8-81.1 202.8-202.8.1-113.8-90.2-203.3-202.8-203.3z"></path></svg>
            """,
            "class":"",
        },
## orcid logo plus link; 'LiaOrcid' adapted to fill all space
     # from https://react-icons.github.io/react-icons/search/#q=orcid
        {
            "name": "Orcid",
            "url": "https://orcid.org/0000-0003-0325-1481",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" height="1em" width="1em" viewBox="0 0 32 32"><path d="m16.026 0.95168c-8.3118 0-15.075 6.7629-15.075 15.075 0 8.3118 6.7629 15.075 15.075 15.075 8.3118 0 15.075-6.7629 15.075-15.075 0-8.3118-6.7629-15.075-15.075-15.075zm0 2.3192c7.0584 0 12.755 5.6971 12.755 12.755 0 7.0584-5.6971 12.755-12.755 12.755-7.0584 0-12.755-5.6971-12.755-12.755 0-7.0584 5.6971-12.755 12.755-12.755zm-5.7979 3.4788a1.1596 1.1596 0 0 0 0 2.3192 1.1596 1.1596 0 0 0 0 -2.3192zm-1.1596 3.4788v12.755h2.3192v-12.755zm4.6383 0v12.755h5.2181c3.5084 0 6.3777-2.8693 6.3777-6.3777 0-3.5084-2.8693-6.3777-6.3777-6.3777zm2.3192 2.3192h2.899c2.2547 0 4.0586 1.8038 4.0586 4.0586 0 2.2547-1.8038 4.0586-4.0586 4.0586h-2.899z"/></svg>
                """,
            "class":"",
        },
    ],
}

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "../_static/favicon.ico"

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
   'css/coalispr.css',
]

