#!/usr/bin/env python

import codecs

from setuptools import setup
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == 'mbcs'))

VERSION = '0.4.3'

setup(
    name='peerplays',
    version=VERSION,
    description='Python library for PEERPLAYS',
    long_description=open('README.md').read(),
    download_url='https://github.com/xeroc/python-peerplays/tarball/' + VERSION,
    author='Fabian Schuh',
    author_email='<Fabian@chainsquad.com>',
    maintainer='Fabian Schuh',
    maintainer_email='<Fabian@chainsquad.com>',
    url='http://www.github.com/xeroc/python-peerplays',
    keywords=['peerplays', 'library', 'api', 'rpc'],
    packages=[
        # "peerpays",
        # "peerplaysapi",
        # "peerplaysbase"
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial',
    ],
    install_requires=[
        "graphenelib",
        "scrypt==0.7.1",
        "appdirs==1.4.0",
        "pycrypto==2.6.1",
    ],
    dependency_links=[
        "git+https://github.com/xeroc/python-graphenelib@minimal#egg=graphenelib"
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
)
