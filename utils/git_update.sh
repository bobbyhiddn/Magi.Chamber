#!/bin/sh
echo "Pulling latest changes and updating submodules..."
git pull origin main --recurse-submodules
git submodule init
git submodule update --remote --merge