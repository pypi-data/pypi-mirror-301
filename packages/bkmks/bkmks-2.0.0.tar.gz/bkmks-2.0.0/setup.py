from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="bkmks",
    version="2.0.0",
    description="Extendable browser bookmark exporter CLI tool",
    url="https://github.com/nico-i/bkmks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nico Ismaili",
    author_email="nico@ismaili.de",
    keywords="bookmark, browser, export",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.12, <4",
    include_package_data=True,
    install_requires=["pathspec", "questionary"],
    extras_require={
        "test": [
            "pytest",
        ],
        "dev": ["ruff", "pyinstaller"],
    },
    entry_points={
        "console_scripts": [
            "bkmks=presentation.cli.__main__:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/nico-i/bkmks/issues",
        "Funding": "https://www.paypal.com/paypalme/ismailinico",
        "Source": "https://github.com/nico-i/bkmks",
    },
)
