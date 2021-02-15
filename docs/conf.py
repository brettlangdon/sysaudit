import datetime

import sphinx_rtd_theme

year = datetime.datetime.now().year
project = "sysaudit"
copyright = "2020-{}, brettlangdon".format(year)
author = "brettlangdon <me@brett.is>"


extensions = ["sphinx_rtd_theme"]
templates_path = []
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "sphinx_rtd_theme"
html_static_path = []
html_theme_options = {}
