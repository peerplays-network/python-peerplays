#!/usr/bin/env python3

from setuptools import setup
import re

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs

try:
    codecs.lookup("mbcs")
except LookupError:
    ascii = codecs.lookup("ascii")
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == "mbcs"))

VERSION = "0.5.0"

# Strip some stuff from README for PyPI description:
long_desc = open("README.md").read()
long_desc = re.sub(
    '<!-- EXCLUDE_FROM_PYPI -->?(.*?)<!-- END_EXCLUDE_FROM_PYPI -->',
    '',
    long_desc,
    flags=re.DOTALL
)

setup(
    name="peerplays",
    version=VERSION,
    description="Python library for PEERPLAYS",
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author="PBSA and contributors. Original by Fabian Schuh.",
    author_email="info@pbsa.info",
    maintainer="PBSA",
    maintainer_email="info@pbsa.info",
    url="https://gitlab.com/PBSA/tools-libs/python-peerplays",
    keywords=["peerplays", "library", "api", "rpc"],
    packages=["peerplays", "peerplays.cli", "peerplaysapi", "peerplaysbase"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Games/Entertainment",
    ],
    entry_points={"console_scripts": ["peerplays = peerplays.cli.cli:main"]},
    install_requires=open("requirements.txt").readlines(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
)
