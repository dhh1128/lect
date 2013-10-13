import os, sys

# Make it possible to import stuff relative to app root
_app_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not _app_root_path in sys.path:
  sys.path.insert(0, _app_root_path)

from env import sandbox
import context

# Make it possible to import stuff relative to app root
_app_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not _app_root_path in sys.path:
  sys.path.insert(0, _app_root_path)

from ast import forest
from util import ui, problems

def _create_forest_for_path(path):
  '''
  All processing has to be done in the context of a sandbox that configures the
  environment. Therefore, begin by discovering which sandbox this code belongs
  to.
  '''
  sb = sandbox.Sandbox(path)
  return forest.Forest(sb)

def _parse_compilation_unit(forest, ctx, lines):
  return
  for i in xrange(len(lines)):
    ctx.line_num = i
    line = lines[i].rstrip()
    if line:
      if line[0].isalpha():
        parse_top_noun(forest, ctx, lines, i)
  return None

def _parse_file(fname, forest=None):
  if not forest:
    forest = _create_forest_for_path(fname)
  exit_code = 0
  try:
    relpath = os.path.relpath(fname, forest.sandbox.root)
    ui.report(relpath)
    ctx = context.Context(forest.sandbox, fname)
    with open(fname, 'r') as f:
      lines = f.readlines()
    forest.add(parse_compilation_unit(forest, ctx, lines))
  except:
    exit_code = ui.complain(str(sys.exc_info()[1]))
  return exit_code, forest

def parse(path):
  sb = sandbox.Sandbox(path)
  ctx = context.Context(sb, '.')
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
          this_exit_code, ignored = _parse_file(os.path.join(root, f), forest)
          exit_code += this_exit_code
  return exit_code
