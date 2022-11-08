#!/bin/sh

git pull

python -m pipenv install
python -m pipenv run python main.py
