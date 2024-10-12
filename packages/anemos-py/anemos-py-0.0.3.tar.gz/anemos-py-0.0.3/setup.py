# Author: Kengo Handa <kengo.handa@solufit.net>
# Copyright (c) 2024 Kengo Handa and Solufit
# License: MIT License

from setuptools import setup

DESCRIPTION = "anemos-py: A Python library for Anemos API"
NAME = 'anemos-py'
AUTHOR = 'Kengo Handa'
AUTHOR_EMAIL = 'kengo.handa@solufit.net'
URL = 'https://github.com/solufit/anemos-py'
LICENSE = 'MIT License'
DOWNLOAD_URL = 'https://github.com/solufit/anemos-py'
VERSION = '0.0.3'
PYTHON_REQUIRES = ">=3.10"

INSTALL_REQUIRES = [
    'requests>=2.32.3',
    'pydantic>=2.9.2',
]

EXTRAS_REQUIRE = {
    'tutorial': [
    ]
}

PACKAGES = [
    'anemos'
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Scientific/Engineering',
]

with open('README.md', 'r') as fp:
    readme = fp.read()
long_description = readme

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/markdown',
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,
      packages=PACKAGES,
      classifiers=CLASSIFIERS
    )
