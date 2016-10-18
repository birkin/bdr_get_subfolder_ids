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
TARGET_FOLDER_LST = json.loads( os.environ['FLDR_IDS__TARGET_FOLDER_INFO'] )  # format: [ {'folder_a': 1}, {'folder_b': 2} ]


def runCode( target_folder_dct ):
    print 'starting runCode()'
    ## get data
    ( target_name, target_id ) = ( target_folder_dct.items()[0][0], target_folder_dct.items()[0][1] )  # single item dct
    payload = { 'folder_id': target_id }
    r = requests.get( FOLDER_API_URL, params=payload, auth=(FOLDER_API_AUTH_NAME, FOLDER_API_AUTH_KEY) )
    json_string = r.content.decode( 'utf-8' )
    jdict = json.loads( json_string )
    print( 'jdict, ```{}```'.format(pprint.pformat(jdict)) )
    ## check for correct folder
    returned_folder_name = jdict['name']
    returned_folder_id = jdict['id']
    if not returned_folder_name == target_name:
        print 'ERROR: expected folder name ```{expected}```; got folder name ```{received}```'.format( expected=target_name, received=returned_folder_name )
        return
    if not returned_folder_id == target_id:
        print 'ERROR: expected folder id ```{expected}```; got folder name ```{received}```'.format( expected=target_id, received=returned_folder_id )
        return
    print 'name and id ok'
    ## build output
    output = {
        'target_folder': { 'name': returned_folder_name, 'id': returned_folder_id },
        'subfolders': []
        }
    for child_folder in jdict['child_folders']:
        subfolder = ( child_folder['name'], child_folder['id'] )
        output['subfolders'].append( subfolder )
    output['subfolders'].sort()
    print 'output, ```{}```'.format( pprint.pformat(output) )


if __name__ == "__main__":
    for target_folder_dct in TARGET_FOLDER_LST:
        runCode( target_folder_dct )
    print '\n-- END OF SCRIPT --'
