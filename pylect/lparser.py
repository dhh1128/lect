import os

import ui

def process(path):
  exit_code = 0
  if os.path.isdir(path):
    for root, dirs, files in os.walk(path):
      for f in files:
        if f.endswith('.l'):
          if process_file(os.path.join(root, f)):
            exit_code = 1
  return exit_code

def parse(code):
  return None

def process_file(fname):
  exit_code = 0
  try:
    ui.report(fname)
    with open(fname, 'r') as f:
      txt = f.read()
    ast = parse(txt)
    return 0
  except:
    exit_code = ui.complain(str(sys.exc_info[0]))
  return exit_code


