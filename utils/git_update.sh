#!/bin/sh
echo "Pulling latest changes and updating submodules..."
git pull origin main --recurse-submodules
git submodule init
git submodule update --remote --merge

# If there are any changes, commit them
if [ -n "$(git status --porcelain)" ]; then
  git add .
  git commit -m "Update submodules"
  git push origin main
fi