#/bin/bash

# Create Python virtualenv
PY_ENV=/home/sam/repos/env/py2


# Clone repos
# update and clone repos rather than submodules? 
# or clone non recurisce and update at this point

# Update python env
pip install -r /home/sam/repos/support/OasisLMF.github.io/modules/OasisPlatform/requirements.in
pip install -r requirements.txt

# script to extract / prase RELEASE.md / CHANGELOG.md  notes 

# Build docs
cd ./src/
make html SPHINXBUILD="python ${PY_ENV}/bin/sphinx-build"


# prompt for overwrite?
# Copy to root of dir
