#!/usr/bin/env bash
quarto render eia_backfill.qmd --to html

rm -rf docs/eia_backfill/
mkdir docs/eia_backfill
cp eia_backfill.html docs/eia_backfill/
cp -R ./eia_backfill_files ./docs/eia_backfill/

rm -rf ./eia_backfill_files
rm eia_backfill.html