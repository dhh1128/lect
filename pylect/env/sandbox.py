import os, sys

# Make it possible to import stuff relative to app root
_app_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not _app_root_path in sys.path:
  sys.path.insert(0, _app_root_path)

from util import problems, ui, helpers

problems.define('CantFindSandboxError', 1, 'Unable to find sandbox from %s. All code must be compiled relative to a sandbox to provide context.')

SUFFIX = '.sandbox'

def _get_root(path):
  '''
  A sandbox is always stored in a folder named .../foo.sandbox,
  where "foo" is any convenient name that the developer wants
  to use. It contains components -- each of which is a separately
  compilable project, possibly with interdependencies.
  '''
  i = path.find(SUFFIX)
  if i > -1:
    path = helpers.norm_folder(os.path.normcase(os.path.abspath(path[0:i+len(SUFFIX)])))
    return path
  raise CantFindSandboxError(path)

class Sandbox:
  '''
  A Sandbox is a unit of code management in lect, and corresponds
  to a single folder in the file system, where the folder name ends with
  ".sandbox". The sandbox contains zero or more component folders
  that are direct children. Typically, it is components rather than
  sandboxes that map onto repos in a dvcs.
  '''
  def __init__(self, path):
    self.root = _get_root(path)
    self.components = []
