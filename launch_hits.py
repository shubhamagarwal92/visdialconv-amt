import argparse, json

import os
import simpleamt
import sys

if __name__ == '__main__':
  parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()])
  parser.add_argument('--hit_properties_file', type=argparse.FileType('r'))
  parser.add_argument('--html_template')
  parser.add_argument('--input_json_file', type=argparse.FileType('r'))
  parser.add_argument('--qual_questions', type=argparse.FileType('r'))
  parser.add_argument('--qual_answers', type=argparse.FileType('r'))
  parser.add_argument('--qual_test', action="store_true", help="If we want to have qualification test")
  parser.add_argument('--qual_id', type=str, default="", help="Qualification id if already created")
  parser.add_argument('--qual_name', type=str, default="", help="Name that we want to provide Qualification test")

  args = parser.parse_args()

  mtc = simpleamt.get_mturk_connection_from_args(args)

  hit_properties = json.load(args.hit_properties_file)
  hit_properties['Reward'] = str(hit_properties['Reward'])
  simpleamt.setup_qualifications(hit_properties, mtc)

  frame_height = hit_properties.pop('FrameHeight')
  env = simpleamt.get_jinja_env(args.config)
  template = env.get_template(args.html_template)

  if args.hit_ids_file is None:
    print('Need to input a hit_ids_file')
    sys.exit()
  if os.path.isfile(args.hit_ids_file):
    print('hit_ids_file already exists')
    sys.exit()

  if args.qual_test:
    if args.qual_id == "":
      questions = args.qual_questions.read()
      answers = args.qual_answers.read()

      # A QualificationType's name must be unique among
      # all of the QualificationTypes created by the same user.
      qual_response = mtc.create_qualification_type(
                    Name=args.qual_name,
                    Keywords=hit_properties['Description'],
                    Description=hit_properties['Keywords'],
                    QualificationTypeStatus='Active',
                    Test=questions,
                    AnswerKey=answers,
                    TestDurationInSeconds=300)

      qual_reponse_id = qual_response['QualificationType']['QualificationTypeId']
      print("New Qualification response id: ", qual_reponse_id )
    else:
      qual_reponse_id = args.qual_id
      print("Using qualification response id: ", qual_reponse_id )

    hit_properties['QualificationRequirements'].append({
        'QualificationTypeId': qual_reponse_id,
        'Comparator': 'EqualTo',
        'IntegerValues': [100],
    })

  with open(args.hit_ids_file, 'w') as hit_ids_file:
    for i, line in enumerate(args.input_json_file):
      hit_input = json.loads(line.strip())

      # In a previous version I removed all single quotes from the json dump.
      # TODO: double check to see if this is still necessary.
      template_params = { 'input': json.dumps(hit_input) }
      html_doc = template.render(template_params)
      html_question = '''
        <HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
          <HTMLContent>
            <![CDATA[
              <!DOCTYPE html>
              %s
            ]]>
          </HTMLContent>
          <FrameHeight>%d</FrameHeight>
        </HTMLQuestion>
      ''' % (html_doc, frame_height)
      hit_properties['Question'] = html_question

      # This error handling is kinda hacky.
      # TODO: Do something better here.
      launched = False
      while not launched:
        try:
          boto_hit = mtc.create_hit(**hit_properties)
          launched = True
        except Exception as e:
          print(e)
      hit_id = boto_hit['HIT']['HITId']
      hit_ids_file.write('%s\n' % hit_id)
      print('Launched HIT ID: %s, %d' % (hit_id, i + 1))
