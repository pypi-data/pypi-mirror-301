from setuptools import setup, find_packages

# Nom du package PyPI ('pip install NAME')
NAME = "Orange-All-Dependencies"

# Version du package PyPI
VERSION = "0.0.4"  # la version doit être supérieure à la précédente sinon la publication sera refusée

# Facultatif / Adaptable à souhait
AUTHOR = "Orange community"
AUTHOR_EMAIL = ""
URL = ""
DESCRIPTION = "Install all the addons at once for Orange Data Mining !!"
LICENSE = ""

# 'orange3 add-on' permet de rendre l'addon téléchargeable via l'interface addons d'Orange 
KEYWORDS = ["orange3 add-on",]

# Dépendances
INSTALL_REQUIRES = ["AAIT>=0.0.4.19", "gpt4all-pypi-part-011",
                    "aait-store-cut-part-016", "all-mpnet-base-v2-pypi-part-005",
                    "Orange3-Associate",
                    "Orange3-Bioinformatics",
                    "Orange3-Educational",
                    "Orange3-Explain",
                    "Orange3-Fairness",
                    "Orange3-Geo",
                    "Orange3-ImageAnalytics",
                    "Orange3-Network",
                    "Orange3-Prototypes",
                    "Orange3-SingleCell",
                    "Orange-Spectroscopy",
                    "Orange3-Survival-Analysis",
                    "Orange3-Text",
                    "Orange3-Textable",
                    "Orange3-Timeseries",
                    "Orange3-WorldHappiness"]

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
