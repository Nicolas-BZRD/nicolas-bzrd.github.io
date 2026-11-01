#!/bin/bash
# Rebuilds the whole site from data/*.json. Run after editing anything in data/.
# See README.md.
set -e
cd "$(dirname "$0")"

python3 build.py
