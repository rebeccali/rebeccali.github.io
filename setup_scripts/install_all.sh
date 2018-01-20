#!/usr/bin/env bash

# This script installs all necessary apt packages

# exit on errors
set -e

./setup_scripts/install_packages.sh

./setup_scripts/install_gems.sh
