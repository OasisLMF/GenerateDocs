#/bin/bash

DIR_BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR_ENV=$DIR_BASE/venv
DIR_MODULES=$DIR_BASE/modules


# Clone repos
# update and clone repos rather than submodules? 
# or clone non recurisce and update at this point


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
            git clone "git@github.com:OasisLMF/${module}.git"
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
        virtualenv2 $DIR_ENV
    fi 
    source ${DIR_ENV}/bin/activate

    # Update python env
    pip install -r requirements.txt
    pip install -r $DIR_BASE/modules/OasisPlatform/requirements.in
    pip install -r $DIR_BASE/modules/oasis_keys_server/requirements.txt 




# script to extract / prase RELEASE.md / CHANGELOG.md  notes 
#    git_modules=(
#        'OasisLMF/'
#        'OasisPlatform'
#        'Ktools'
#    )




# Build docs
cd $DIR_BASE
make html SPHINXBUILD="python ${DIR_ENV}/bin/sphinx-build"


# prompt for overwrite?
# Copy to root of dir
