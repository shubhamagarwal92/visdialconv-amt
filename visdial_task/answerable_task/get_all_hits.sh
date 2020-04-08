#!/usr/bin/env bash

export CURRENT_DIR=${PWD}  # get current directory - shell_scripts
# go to parent directory
export PARENT_DIR="$(dirname "$CURRENT_DIR")"
cd $PARENT_DIR

export TURK_DIR="$(dirname "$PARENT_DIR")"
cd $TURK_DIR


python get_all_hits.py \
  > visdial_task/results_answerable/all_results.txt
