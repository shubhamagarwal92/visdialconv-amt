#!/usr/bin/env bash

export CURRENT_DIR=${PWD}  # get current directory - shell_scripts
# go to parent directory
export PARENT_DIR="$(dirname "$CURRENT_DIR")"
cd $PARENT_DIR

export TURK_DIR="$(dirname "$PARENT_DIR")"
cd $TURK_DIR

mkdir -p $TURK_DIR/visdial_task/rendered_templates

python render_template.py \
--html_template=visdial_task/hit_templates/verify_question_answer.html \
--rendered_html=visdial_task/rendered_templates/verify_question_answer.html
