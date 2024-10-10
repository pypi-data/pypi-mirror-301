from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sum_test",
    version="0.2.3",
    description="A short description of your package",
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
)
