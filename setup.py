import os
import sys

from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install

VERSION = "0.5.15"

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
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/python-kol/libkol",
    #packages=setuptools.find_packages(),
    packages=find_packages(),
    install_requires=[
        "aioitertools==0.4.0",
        "aiohttp==3.5.4",
        "beautifulsoup4==4.7.1",
        "dataclasses==0.6",
        "multidict==4.5.2",
        "typing==3.6.6",
        "yarl==1.3.0",
        "aiosqlite==0.10.0",
        "tortoise-orm==0.12.2",
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
