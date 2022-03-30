#!/bin/bash
set -e

echo "Running black..."
python3 -m black . --exclude ".ipynb_checkpoints|.ipynb"
echo "success!"
echo

echo "Running pylint..."
find . -name "*.py" -not -path "*.ipynb_checkpoints" -not -path "*.ipynb" | \
	xargs python3 -m pylint --rcfile python-linter/.pylintrc
echo "success!"
echo

echo "Running mypy..."
python3 -m mypy --config-file python-linter/mypy.ini .
echo "success!"
echo

echo "Running yamllint..."
python3 -m yamllint -c python-linter/yamllint.yml .
echo "success!"
echo

echo "Running bandit..."
python3 -m bandit --recursive --quiet .
echo "success!"
