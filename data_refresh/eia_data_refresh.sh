#!/usr/bin/env bash
source /opt/$VENV_NAME/bin/activate 

rm -rf ./eia_data_refresh_files
rm eia_data_refresh.html
quarto render eia_data_refresh.qmd --to html

rm -rf docs/eia_data_refresh/
mkdir docs/eia_data_refresh
cp eia_data_refresh.html docs/eia_data_refresh/
cp -R ./eia_data_refresh_files ./docs/eia_data_refresh/

rm -rf ./eia_data_refresh_files
rm eia_data_refresh.html



echo "Finish"

p=$(pwd)
git config --global --add safe.directory $p

if [[ "$(git status --porcelain)" != "" ]]; then
    git config --global user.name 'RamiKrispin'
    git config --global user.email 'ramkrisp@umich.edu'
    git add docs/*
    git add data/*
    git commit -m "Auto update of the data"
    git push origin main
else
echo "Nothing to commit..."
fi