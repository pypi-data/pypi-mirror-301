# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="nasdaq-news-crawler",
    version="0.1.0",
    description="A tool for scraping and analyzing news and press releases from NASDAQ-listed companies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Norbert Nieżorawski",
    author_email="norbertnnn@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
    ],
    packages=["nasdaq_news_crawler"],
    include_package_data=True,
    install_requires=[
        "pandas",
        "beautifulsoup4",
        "requests",
        "tqdm",
        "selenium",
        "transformers",
        "torch",
        "python-dateutil"
    ],
    python_requires='>=3.10'
)