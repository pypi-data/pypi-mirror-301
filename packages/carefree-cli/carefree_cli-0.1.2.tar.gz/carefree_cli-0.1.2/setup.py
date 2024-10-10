from setuptools import setup
from setuptools import find_packages


VERSION = "0.1.2"
DESCRIPTION = "A `cli` that helps you manage your commands"
with open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="carefree-cli",
    version=VERSION,
    packages=find_packages(exclude=("tests",)),
    entry_points={"console_scripts": ["cfi = cfi:cli"]},
    install_requires=[
        "rich",
        "regex",
        "typer",
        "filelock",
        "pydantic",
    ],
    author="carefree0910",
    author_email="syameimaru.saki@gmail.com",
    url="https://github.com/carefree0910/carefree-cli",
    download_url=f"https://github.com/carefree0910/carefree-cli/archive/v{VERSION}.tar.gz",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="python cli",
)
