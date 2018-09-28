#!/bin/bash

DIR_BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR_ENV=$DIR_BASE/venv
DIR_MODULES=$DIR_BASE/modules
DIR_RELEASE="${DIR_BASE}/src/releases/" 

## SETUP BUILD ENVIROMENT 
    git_modules=(
        'OasisLMF'
        'OasisPlatform'
        'oasis_keys_server'
        'Ktools'
    )
    for module in "${git_modules[@]}"; do
        cd $DIR_MODULES
        if [ ! -d $module ]; then
            printf "\n== Download %s ==\n" "${module}"
            git clone --depth 1 "https://github.com/OasisLMF/${module}.git"
        else 
            printf "\n== Update %s ==\n" "${module}"
            cd $module
            git pull
        fi 
    done

# Update python env
    pip install -r $DIR_BASE/requirements.txt
    pip install -r $DIR_BASE/modules/OasisPlatform/requirements.in
    pip install -r $DIR_BASE/modules/oasis_keys_server/requirements.txt 

# script to extract / prase RELEASE.md / CHANGELOG.md  notes 
    cat $DIR_MODULES/Ktools/CHANGE.md > $DIR_RELEASE/ktools.md
    cat $DIR_MODULES/OasisLMF/CHANGELOG.rst > $DIR_RELEASE/oasislmf.rst
    cat $DIR_MODULES/OasisPlatform/RELEASE.md > $DIR_RELEASE/oasis_platform.md

# Build docs
    cd $DIR_BASE
    make html

# Create TAR
    tar -czvf oasis_docs.tar.gz -C build/html/ .
    mv oasis_docs.tar.gz $DIR_BASE/output/
