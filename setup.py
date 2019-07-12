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
    package_data={"libkol": ["libkol.db"]},
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
)
