from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'readme.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name="base_class_package",
    version="0.2.0",
    author="Nodar",
    author_email="nodi3m@gmail.com",
    description="Counting normal point",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    # url="",
)