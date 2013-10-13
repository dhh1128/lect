import os, sys

import sandbox

# Make it possible to import stuff relative to app root
_app_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not _app_root_path in sys.path:
  sys.path.insert(0, _app_root_path)

from my_ast import forest
import ui

def create_forest_for_path(path):
  '''
  All processing has to be done in the context of a sandbox that configures the
  environment. Therefore, begin by discovering which sandbox this code belongs
  to.
  '''
  sb = sandbox.Sandbox(path)
  return forest.Forest(sb)

def process(path, forest=None):
  if not forest:
    forest = create_forest_for_path(path)
  exit_code = 0
  if os.path.isdir(path):
    # Iterate depth-first, because low-level classes are likely to
    # have less dependencies than high-level ones.
    for root, dirs, files in os.walk(path, topdown=False):
      # Iterate over folders and files in alphabetical order, to be
      # deterministic.
      dirs.sort()
      files.sort()
      for f in files:
        if f.endswith('.l'):
          this_exit_code, ignored = process_file(os.path.join(root, f), forest)
          if this_exit_code:
            exit_code = 1
  return exit_code, forest

def parse(lines, indent=0):
  return None

def process_file(fname, forest=None):
  if not forest:
    forest = create_forest_for_path(fname)
  exit_code = 0
  try:
    ui.report(fname)
    with open(fname, 'r') as f:
      lines = f.readlines()
    forest.add(parse(lines))
  except:
    exit_code = ui.complain(str(sys.exc_info()[1]))
  return exit_code, forest


