from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="arranjo_combinacao",
    version="0.0.2",
    author="daniel_paes",
    author_email="daniel92.dev@gmail.com",
    description="Cálculo simples de arranjo e combinação",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DanielPaes/simple-package-template.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)