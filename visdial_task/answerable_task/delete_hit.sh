#!/usr/bin/env bash

export CURRENT_DIR=${PWD}  # get current directory - shell_scripts
# go to parent directory
export PARENT_DIR="$(dirname "$CURRENT_DIR")"
cd $PARENT_DIR

export TURK_DIR="$(dirname "$PARENT_DIR")"
cd $TURK_DIR


#python delete_hits.py \
#--hit_ids_file=visdial_task/results_tests/hit_ids_test_1.txt

python delete_hits.py \
--hit_ids_file=visdial_task/results_answerable/hit_ids_test_3.txt
