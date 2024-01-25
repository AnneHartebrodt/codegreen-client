from setuptools import setup
from pathlib import Path
from setuptools import setup, find_packages

DESCRIPTION = (
    "Client code for code green web API"
)
AUTHOR = "Anne Hartebrodt"
AUTHOR_EMAIL = "anne.hartebrodt@fau.de"
PROJECT_URLS = {
    "Documentation": "https:",
    "Bug Tracker": "https://github.com/AnneHartebrodt/codegreen-client/issues",
    "Source Code": "https://github.com/AnneHartebrodt/codegreen-client",
}
APP_ROOT = Path(__file__).parent
README = (APP_ROOT / "README.md").read_text()
INSTALL_REQUIRES = [
    "requests",
    "pandas",
    "numpy",
    "codecarbon",
    "sphinx",
    "myst-parser" 
]
EXTRAS_REQUIRE = {
    "dev": [
        "black",
        "flake8==3.7.9",
        "pre-commit",
        "pydocstyle",
        "pytest",
        "pytest-black",
        "pytest-clarity",
        "pytest-dotenv",
        "pytest-flake8",
        "pytest-flask",
        "tox",
        "sphinx",
        "myst-parser"
    ]
}

setup(
    name="codegreen",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    version="0.1",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license="GPLv3",
    url="git@github.com:AnneHartebrodt/greenerai-client.git",
    project_urls=PROJECT_URLS,
    packages=['codegreen'],
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
)
