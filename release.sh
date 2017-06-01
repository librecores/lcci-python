#!/bin/bash

if [ $# -lt 1 ]; then
  echo "Usage: release.sh <version>"
  exit 1
fi

rm -rf dist/
git tag $1
git push origin $1

python setup.py sdist bdist_wheel --universal
twine upload dist/*
