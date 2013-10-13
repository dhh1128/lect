'''
Utility routines used in multiple modules.
'''

import os

def norm_folder(path):
  '''
  Put a path to a folder in canonical form, which means it's delimited by
  forward slashes and ends with a forward slash.
  '''
  if os.name == 'nt':
    path = path.replace('\\', '/')
  if not path.endswith('/'):
    path += '/'
  return path

