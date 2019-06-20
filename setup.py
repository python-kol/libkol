import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libkol",
    version="0.9.0",
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
)
