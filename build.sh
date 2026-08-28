#!/bin/bash
# Build the aggregated Oasis documentation site.
#
# GenerateDocs is a version-pinned orchestrator: it holds no component content. Each module's
# docs are built from its own repository at the ref pinned in modules.json, and assembled under
# build/html/<path>/ with a thin landing page at the root. See orchestrate.py + modules.json.
#
# Usage:
#   ./build.sh              # CI/release: clone each repo at its pinned ref, then build
#   ./build.sh --local      # dev: build from local checkouts next to this repo
set -e

DIR_BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR_ENV="$DIR_BASE/venv"
MODE="--clone"
[ "$1" == "--local" ] && MODE="--use-local"

# Python environment
if [ ! -f "${DIR_ENV}/bin/activate" ]; then
    printf "\n== Create Python virtualenv ==\n"
    python3 -m venv "$DIR_ENV"
fi
source "${DIR_ENV}/bin/activate"
pip install -q -r requirements.txt

# Build + assemble all modules and the landing
python "$DIR_BASE/orchestrate.py" $MODE --keep-going

# Package the assembled site
mkdir -p "$DIR_BASE/output"
tar -czf "$DIR_BASE/output/oasis_docs.tar.gz" -C "$DIR_BASE/build/html" .
printf "\n== Built build/html and output/oasis_docs.tar.gz ==\n"
