# Author: Kenta Nakamura <c60evaporator@gmail.com>
# Copyright (c) 2020-2021 Kenta Nakamura
# License: BSD 3 clause

from setuptools import setup
import PayNexus

DESCRIPTION = "PayNexus: PythonからPayPayを操作できる非公式モジュールです。"
NAME = 'PayNexus'
AUTHOR = 'Haruki Kodama'
AUTHOR_EMAIL = 'tp-link-z490@outlook.jp'
URL = 'https://github.com/harumaki4649/PayNexus'
LICENSE = 'BSD 3-Clause'
DOWNLOAD_URL = 'https://github.com/harumaki4649/PayNexus'
VERSION = PayNexus.__version__
PYTHON_REQUIRES = ">=3.9"
# Readmeのファイルパス指定
readme_path = r'C:\Users\msi-z\OneDrive\ドキュメント\GitHub\PayNexus\README.md'

with open("./PayNexus/requirements.txt", "r", encoding="utf-8") as f:
    INSTALL_REQUIRES = f.readlines()

EXTRAS_REQUIRE = {
}

PACKAGES = [
    'paynexus'
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Multimedia :: Graphics',
    'Framework :: Matplotlib',
]

with open(readme_path, 'r', encoding="utf-8") as fp:
    readme = fp.read()
long_description = readme

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description_content_type="text/markdown",
      long_description=long_description,
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
