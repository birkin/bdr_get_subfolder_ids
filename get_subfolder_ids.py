# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
- Purpose: creates a listing of subfolder names and ids
- Usage (from shell):
    - source the env
    - python ./get_subfolder_ids.py
"""

import json, pprint, os
import requests

FOLDER_API_URL = unicode( os.environ['FLDR_IDS__FOLDER_API_URL'] )
FOLDER_API_AUTH_NAME = unicode( os.environ['FLDR_IDS__FOLDER_API_AUTH_NAME'] )
FOLDER_API_AUTH_KEY = unicode( os.environ['FLDR_IDS__FOLDER_API_AUTH_KEY'] )
PARENT_FOLDER_DCT = json.loads( os.environ['FLDR_IDS__PARENT_FOLDER_INFO'] )  # format: { 'name': 'the name', 'id': 'the id string' }


def runCode():
  ## get data
  payload = { 'folder_id': PARENT_FOLDER_DCT['id'] }
  r = requests.get( FOLDER_API_URL, params=payload, auth=(FOLDER_API_AUTH_NAME, FOLDER_API_AUTH_KEY) )
  json_string = r.content.decode( 'utf-8' )
  jdict = json.loads( json_string )
  print( 'jdict, ```{}```'.format(pprint.pformat(jdict)) )
  ## check for correct folder
  returned_json_name = jdict['result']['folder_name']
  if not returned_json_name == PARENT_FOLDER_DCT['name']:
    return 'ERROR: expected folder name ```{expected}```; got folder name ```{received}```'.format( expected=PARENT_FOLDER_DCT['name'], received=returned_json_name )
  ## build output
  output = {
    'parent_folder': { 'name': PARENT_FOLDER_DCT['name'], 'id': PARENT_FOLDER_DCT['id'] },
    'subfolders': []
    }
  for entry in jdict['result']['folder_subfolders']:
    output['subfolders'].append( entry['subfolder'] )
  pprint.pprint( output )
  print '\n-- END OF SCRIPT --'


if __name__ == "__main__":
  runCode()
