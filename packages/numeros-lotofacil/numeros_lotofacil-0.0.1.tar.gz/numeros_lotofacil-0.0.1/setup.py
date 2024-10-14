from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="numeros_lotofacil",
    version="0.0.1",
    author="Thais Mendes",
    author_email="thaisppmendes@hotmail.com",
    description="Sorteia numeros da lotofacil",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MendesTatah",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)