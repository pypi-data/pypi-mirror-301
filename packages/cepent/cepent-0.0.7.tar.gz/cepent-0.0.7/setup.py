from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

LICENSE = 'MIT' #Tipo de licencia
VERSION = '0.0.7'
DESCRIPTION = 'Catch error pentaho'
LONG_DESCRIPTION = 'A package for capturing errors encountered during the data extraction process in ETL workflows using Pentaho'


INSTALL_REQUIRES = [
      'psycopg2'
      ]
# Setting up
setup(
    name="cepent",
    version=VERSION,
    author="Ysis Longart (Biwiser)",
    author_email="ysisl@biwiser.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/biwiser-com/cepent",
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    include_package_data=True,
    keywords=['python', 'psycopg2', 'catch', 'pentaho'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)