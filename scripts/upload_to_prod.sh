#! /bin/bash

pip install setuptools wheel twine

rm -rf dist build *.egg-info

python ./setup.py sdist
python ./setup.py bdist_wheel

twine upload -r pypi dist/*