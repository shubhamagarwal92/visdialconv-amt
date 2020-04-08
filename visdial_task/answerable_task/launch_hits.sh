#!/usr/bin/env bash

export CURRENT_DIR=${PWD}  # get current directory - shell_scripts
# go to parent directory
export PARENT_DIR="$(dirname "$CURRENT_DIR")"
cd $PARENT_DIR

export TURK_DIR="$(dirname "$PARENT_DIR")"
cd $TURK_DIR

# TODO: See the automation steps below
#export QUAL_ID=""
export QUAL_NAME='Very small qualification test to see if you understand the task'

mkdir -p $TURK_DIR/visdial_task/results_answerable

## Testing here -- sandbox
python launch_hits.py \
  --html_template=visdial_task/hit_templates/verify_question_answer.html \
  --hit_properties_file=visdial_task/hit_properties/image_question_answer_test.json \
  --input_json_file=visdial_task/data/data.txt \
  --hit_ids_file=visdial_task/results_answerable/tests/hit_ids_test_acl.txt \
  --qual_questions=visdial_task/hit_templates/qual_questions.xml \
  --qual_answers=visdial_task/hit_templates/qual_answers.xml \
  --qual_test \
  --qual_name "$QUAL_NAME"

## To launch on prod
#python launch_hits.py \
#  --html_template=visdial_task/hit_templates/verify_question_answer.html \
#  --hit_properties_file=visdial_task/hit_properties/image_question_answer.json \
#  --input_json_file=visdial_task/data/data.txt \
#  --hit_ids_file=visdial_task/results_answerable/hit_ids_batch_1.txt \
#  --qual_questions=visdial_task/hit_templates/qual_questions.xml \
#  --qual_answers=visdial_task/hit_templates/qual_answers.xml \
#  --qual_test \
#  --qual_name "$QUAL_NAME" \
#  --prod

# TODO: Automate this process!
# will be printed on console
# New Qualification response id:
# Then use this flag above
#--qual_id "$QUAL_ID" \

