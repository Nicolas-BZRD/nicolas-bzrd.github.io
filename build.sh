#!/bin/bash
# Rebuilds the whole site from data/*.json, then rebuilds tailwind.css.
# Run after editing anything in data/. See README.md.
set -e
cd "$(dirname "$0")"

python3 build.py

BINARY="bin/tailwindcss"
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
[[ "$OS" == "darwin" ]] && OS="macos"
[[ "$ARCH" == "x86_64" ]] && ARCH="x64"

if [[ ! -x "$BINARY" ]]; then
    mkdir -p bin
    echo "Downloading Tailwind CLI (one-time)..."
    curl -sLo "$BINARY" "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-${OS}-${ARCH}"
    chmod +x "$BINARY"
fi

"$BINARY" -i tailwind.input.css -o tailwind.css --minify
echo "✓ tailwind.css rebuilt"
