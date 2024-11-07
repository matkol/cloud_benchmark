#!/bin/bash

# small setup script to be used in Make context which is setting a up a python virtual env

# set -x

source scripts/var.sh

if command -v pyenv 2>&1 >/dev/null; then
    echo "Using pyenv for installation virtual environment..."
    pyenv install 3.13.0 --skip-existing
    pyenv virtualenv 3.13.0 $virtual_env_name  # this will skip automatically if exists already
    pyenv local $virtual_env_name  # activate env
else
    echo "It is strongly recommended to install pyenv for managing virtual environments."
    echo "See https://github.com/pyenv/pyenv#installation or https://realpython.com/intro-to-pyenv/#install"
    echo "Using `virtualenv` now to setup an environment based on system python..."
    python -m pip install --user virtualenv
    python -m venv .venv  # here venv is an executable of virtualenv
    source .venv/bin/activate
fi

python -m pip install --upgrade pip
