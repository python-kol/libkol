import os
import sys

from setuptools import setup
from setuptools.command.install import install

def readme():
    with open("README.md", "r") as fh:
        return fh.read()

class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

setup(
    name="libkol",
    version=VERSION,
    author="",
    author_email="dan@heathmailbox.com",
    description="Python library for interacting with the Kingdom of Loathing ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/python-kol/libkol",
    packages=setuptools.find_packages(),
    install_requires=[
        "aiohttp",
        "beautifulsoup4",
        "multidict",
        "typing",
        "yarl",
        "tortoise-orm",
        "PuLP==1.6.10",
        "sympy==1.4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
