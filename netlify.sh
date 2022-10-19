#!/bin/bash
# This script is used by netlify
python3 -m pip install '.[docs]'
python3 -m sdk html
sphinx-build -W docs docs/build
