from setuptools  import setup, find_packages

# Leer el contenido del archivo README.md

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="Spectro1",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Spectro1",
    description="Una biblioteca para consultar los cursos del tito savitar",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://Spectro1.io",
)
