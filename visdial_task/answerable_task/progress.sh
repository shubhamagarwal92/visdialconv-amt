#!/usr/bin/env bash

export CURRENT_DIR=${PWD}  # get current directory - shell_scripts
# go to parent directory
export PARENT_DIR="$(dirname "$CURRENT_DIR")"
cd $PARENT_DIR

export TURK_DIR="$(dirname "$PARENT_DIR")"
cd $TURK_DIR

# On prod
#python show_hit_progress.py \
#--hit_ids_file=visdial_task/results_answerable/hit_ids_batch_1.txt \
#--prod

python show_hit_progress.py \
--hit_ids_file=visdial_task/results_answerable/hit_ids_batch_1.txt
