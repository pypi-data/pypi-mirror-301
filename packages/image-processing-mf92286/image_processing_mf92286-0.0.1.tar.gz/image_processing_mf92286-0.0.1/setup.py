from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image-processing-mf92286",
    version="0.0.1",
    author="Marcio Fernando",
    author_email="marcio-fernando@dominio.com",
    description="Pacote criado para fins de estudo",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Marcio-Balivo",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.0',
)
