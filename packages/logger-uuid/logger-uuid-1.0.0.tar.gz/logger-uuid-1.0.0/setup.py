import pathlib

from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = "1.0.0"
PACKAGE_NAME = "logger-uuid"
AUTHOR = "Anddy Agudelo"
AUTHOR_EMAIL = "andiagudelo@gmail.com"
URL = "https://github.com/anddyagudelo/logger-uuid"

LICENSE = "MIT"
DESCRIPTION = "Implement logs with unique uuid identifier."
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = []

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    url=URL,
)
