'''
A Sandbox is a unit of code management in lect, and corresponds
to a single folder in the file system. It consists of multiple
components that are all direct children of the sandbox folder.
Typically, it is components rather than sandboxes that map onto
repos in a dvcs.
'''

import os

def _normpath(path):
  if os.name == 'nt':
    path = path.replace('\\', '/')
  if not path.endswith('/'):
    path += '/'
  return path

def _get_root(path):
  '''
  A sandbox is always stored in a folder named .../foo.sandbox,
  where "foo" is any convenient name that the developer wants
  to use.
  '''
  i = path.find('.sandbox')
  if i > -1:
    path = _normpath(os.path.abspath(path[0:i+8]))
    return path

class Sandbox:
  def __init__(self, path):
    self.root = _get_root(path)
