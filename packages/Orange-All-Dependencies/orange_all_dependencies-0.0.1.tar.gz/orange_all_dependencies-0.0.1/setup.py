from setuptools import setup, find_packages

# Nom du package PyPI ('pip install NAME')
NAME = "Orange-All-Dependencies"

# Version du package PyPI
VERSION = "0.0.1"  # la version doit être supérieure à la précédente sinon la publication sera refusée

# Facultatif / Adaptable à souhait
AUTHOR = "Orange community"
AUTHOR_EMAIL = ""
URL = ""
DESCRIPTION = "Install all the addons at once for Orange Data Mining !!"
LICENSE = ""

# 'orange3 add-on' permet de rendre l'addon téléchargeable via l'interface addons d'Orange 
KEYWORDS = ["orange3 add-on",]

# Dépendances
INSTALL_REQUIRES = ["AAIT>=0.0.4.16", "gpt4all-pypi-part-011",
                    "aait-store-cut-part-016", "all-mpnet-base-v2-pypi-part-005"]

setup(name=NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      description=DESCRIPTION,
      license=LICENSE,
      keywords=KEYWORDS,
      install_requires=INSTALL_REQUIRES,
      )
