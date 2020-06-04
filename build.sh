#!/bin/bash

GH_TOKEN=$1
DIR_BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR_ENV=$DIR_BASE/venv
DIR_MODULES=$DIR_BASE/modules
DIR_RELEASE="${DIR_BASE}/src/releases/" 
URL_RELEASE_TAG='https://api.github.com/repos/oasislmf/OasisPlatform/releases/tags/<TAG>'
URL_RELEASE_LATEST='https://api.github.com/repos/oasislmf/OasisPlatform/releases/latest'

set -e 
## SETUP BUILD ENVIROMENT 
    git_modules=(
        'OasisLMF'
        'OasisPlatform'
        'Ktools'
    )
    for module in "${git_modules[@]}"; do
        cd $DIR_MODULES
        if [ ! -d $module ]; then
            printf "\n== Download %s ==\n" "${module}"
            git clone "https://github.com/OasisLMF/${module}.git"
        else 
            printf "\n== Update %s ==\n" "${module}"
            cd $module
            git pull
        fi 
    done

    # Create Python virtualenv
    cd $DIR_BASE
    if [ ! -f ${DIR_ENV}/bin/activate ]; then
        printf "\n == Create Python virtualenv =="
        virtualenv -p python3 $DIR_ENV 
    fi 
    source ${DIR_ENV}/bin/activate

# Update python env
    pip install -r requirements.txt
    pip install -r $DIR_BASE/modules/OasisPlatform/requirements.in

# Script to extract / prase RELEASE.md / CHANGELOG.md  notes 
    cat $DIR_MODULES/Ktools/CHANGELOG.rst > $DIR_RELEASE/ktools.md
    cat $DIR_MODULES/OasisLMF/CHANGELOG.rst > $DIR_RELEASE/oasislmf.rst
    cat $DIR_MODULES/OasisPlatform/CHANGELOG.rst > $DIR_RELEASE/oasis_platform.md

# Get the latest release notes
    if ! [ -x "$(command -v jq)" ]; then
        echo 'Error: jq is not installed.' >&2
    else    
        cd $DIR_MODULES/OasisPlatform
        curl -s $URL_RELEASE_LATEST | jq -r '{body} | .body' > latest_release.md
    fi

# Get Known issues 
    if [ ! -z "$GH_TOKEN" ]; then
        cd $DIR_BASE
        ./known_issues.py $GH_TOKEN > $DIR_MODULES/OasisPlatform/known_issues.md
        echo 'Witten known_issues list'
    else
        echo 'Missing GitHub token'
        exit 1
    fi 

# Build docs
    cd $DIR_BASE
    make html SPHINXBUILD="python ${DIR_ENV}/bin/sphinx-build"

# Create TAR
    if [[ ! -d "$DIR_BASE/output/" ]]; then 
        mkdir $DIR_BASE/output/
    fi 
    tar -czvf oasis_docs.tar.gz -C build/html/ .
    mv oasis_docs.tar.gz $DIR_BASE/output/
