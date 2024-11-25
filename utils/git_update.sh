#!/bin/sh
echo "Pulling latest changes and updating submodules..."
git pull --recurse-submodules
git submodule update --remote --merge