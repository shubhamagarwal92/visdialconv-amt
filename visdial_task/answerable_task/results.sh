#!/usr/bin/env bash

export CURRENT_DIR=${PWD}  # get current directory - shell_scripts
# go to parent directory
export PARENT_DIR="$(dirname "$CURRENT_DIR")"
cd $PARENT_DIR

export TURK_DIR="$(dirname "$PARENT_DIR")"
cd $TURK_DIR

mkdir -p $TURK_DIR/visdial_task/results_answerable

# To deploy on prod
python get_results.py \
  --prod \
  --hit_ids_file=visdial_task/results_answerable/hit_ids_batch_1_launched.txt \
  > visdial_task/results_answerable/results_batch_1.txt


#python get_results.py \
#  --hit_ids_file=visdial_task/results_answerable/hit_ids_test_1.txt \
#  > visdial_task/results_answerable/results_test_1.txt
