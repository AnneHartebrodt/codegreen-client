from setuptools import setup
from pathlib import Path
from setuptools import setup, find_packages

DESCRIPTION = (
    "Client code for web application"
)
AUTHOR = "Anne Hartebrodt"
AUTHOR_EMAIL = "anne.hartebrodt@fau.de"
PROJECT_URLS = {
    "Documentation": "https:",
    "Bug Tracker": "https:",
    "Source Code": "https:",
}
APP_ROOT = Path(__file__).parent
README = (APP_ROOT / "README.md").read_text()
INSTALL_REQUIRES = [
    "requests",
    "pandas",
    "numpy",
    "sphinx",
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
    ]
}

setup(
    name="carbonaware",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    version="0.1",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license="MIT",
    url="git@github.com:AnneHartebrodt/greenerai-client.git",
    project_urls=PROJECT_URLS,
    packages=['carbonaware'],
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
)
