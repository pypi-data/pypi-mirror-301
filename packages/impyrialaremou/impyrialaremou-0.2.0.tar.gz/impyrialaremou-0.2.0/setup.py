# Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author="Josue Afouda",
    description="A package for converting impyrial lengths and weights.",
    name="impyrialaremou",
    version="0.2.0",
    packages=find_packages(include=["impyrialaremou", "impyrialaremou.*"]),
    install_requires=[
        'numpy>=1.10',
        'pandas'
    ]
)