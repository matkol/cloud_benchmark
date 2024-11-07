#!/bin/bash

source scripts/var.sh

pyenv uninstall -f $virtual_env_name 2>/dev/null; true
rm .python-version 2>/dev/null; true
rm -rf .venv 2>/dev/null; true
