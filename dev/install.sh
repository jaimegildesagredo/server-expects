#!/bin/bash -e

python setup.py sdist
pip install dist/`python setup.py --name`-`python setup.py --version`.tar.gz
pip install --upgrade -r test-requirements.txt
