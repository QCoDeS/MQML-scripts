# MQML

[![PyPi version](https://badge.fury.io/py/mqml.svg)](https://badge.fury.io/py/mqml)
[![PyPI python versions](https://img.shields.io/pypi/pyversions/mqml.svg)](https://pypi.python.org/pypi/mqml/)

Packages for measurement and analysis for the Microsoft Quantum Materials Lyngby lab.

# Description

This repository holds all packages, docs and tests for measurement and analysis running at Microsoft Quantum Materials Lyngby lab.
This repository is built on top of QCoDeS and depends on it.

# Installation

Installing from Pypi: pip install mqml
Installing developing version: Clone the repository from [![MQML_scripts github](https://github.com/QCoDeS/MQML-scripts)]. Navigate to the cloned directory on your PC and install it:
```bash
$ pip install -e .
```

# Usage

It is mainly designed for usage at Microsoft Quantum Materials Lyngby lab. However, anybody who has the access to this repository can use it for his/ her experiments.

## Running the tests

If you have gotten 'mqml' from source, you may run the tests locally.

Install `mqml` along with its test dependencies into your virtual environment by executing the following in the root folder

```bash
$ pip install -r test_requirements.txt
```

Then run `pytest` in the `tests` folder.

## Building the documentation

If you have gotten `mqml` from source, you may build the docs locally.

Install `mqml` along with its documentation dependencies into your virtual environment by executing the following in the root folder

```bash
$ pip install -r docs_requirements.txt
```

Then run `make html` in the `docs` folder. This generate a webpage, index.html, in docs/_build/html with the rendered html. The next time you build the documentation, remember to run `make clean` before you run `make html`.
