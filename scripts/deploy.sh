#!/usr/bin/env bash

set -e  # Exit with non-zero exit code if anything fails.
set -x  # Trace everything that the script executes.

if [ "${TRAVIS_PULL_REQUEST}" = "false" ] && [ "${TRAVIS_BRANCH}" = "master" ] && [ `ls ${TRAVIS_BUILD_DIR}/bin/* 2>/dev/null | wc -l` = "2" ]; then
    echo -e "Starting to update revelation-bins.\n"

    # Configure git.
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "Travis CI"

    # Clone revelation binaries repository.
    cd ${HOME}
    git clone --quiet --branch=master https://${GH_PUSH_BIN_TOKEN}@github.com/futurecore/revelation-bins.git  revelation-bins > /dev/null

    # Copy binary simulators into new repository.
    cd revelation-bins
    cp ${TRAVIS_BUILD_DIR}/bin/pydgin-revelation* .

    # Add, commit and push binary files.
    git add pydgin-revelation*
    git commit -m "Travis build ${TRAVIS_BUILD_NUMBER} pushed to master"
    git push -fq origin master > /dev/null

    echo -e "Finished pushing to revelation-bins.\n"
fi
