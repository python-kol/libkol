import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pykollib",
    version="0.9.4.5",
    author="",
    author_email="dan@heathmailbox.com",
    description="Python library for interacting with the Kingdom of Loathing ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danheath/pykollib",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "pickledb",
        "aiohttp",
        "aspy.yaml",
        "beautifulsoup4",
        "certifi",
        "cfgv",
        "chardet",
        "identify",
        "idna",
        "importlib-metadata",
        "importlib-resources",
        "multidict",
        "nodeenv",
        "peewee",
        "pickleDB",
        "pre-commit",
        "PyYAML",
        "requests",
        "six",
        "toml",
        "typing",
        "urllib3",
        "virtualenv",
        "yarl",
        "zipp",
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
