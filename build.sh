#!/bin/bash

DIR_BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR_ENV=$DIR_BASE/venv
DIR_MODULES=$DIR_BASE/modules
DIR_RELEASE="${DIR_BASE}/src/releases/" 

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
# requires a log in for the show command, hangs in docker, download directy?  
#    cd $DIR_MODULES/OasisPlatform
#    hub release show `git tag | tail -1` > latest_release.md

# Build docs
    cd $DIR_BASE
    make html SPHINXBUILD="python ${DIR_ENV}/bin/sphinx-build"

# Create TAR
    if [[ ! -d "$DIR_BASE/output/" ]]; then 
        mkdir $DIR_BASE/output/
    fi 
    tar -czvf oasis_docs.tar.gz -C build/html/ .
    mv oasis_docs.tar.gz $DIR_BASE/output/
