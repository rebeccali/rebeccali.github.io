#!/usr/bin/env bash

# This script installs all necessary apt packages

# exit on errors
set -e

sudo apt update

# internal packages
APT_PKGS="ruby-full rubygems"

# imagemagick 
APT_PKGS="${APT_PKGS} imagemagick libmagickcore-dev libmagickwand-dev"

echo "Installing/updating: ${APT_PKGS}"

sudo apt-get install -y ${APT_PKGS}
