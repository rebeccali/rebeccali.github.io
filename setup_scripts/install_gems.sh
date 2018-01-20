#!/usr/bin/env bash

# This script installs all necessary gem packages

# exit on errors
set -e

GEMS="jekyll bundler"

echo "Installing/updating: ${GEMS}"

sudo gem install ${GEMS}

bundle install 