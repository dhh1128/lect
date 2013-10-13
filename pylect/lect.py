import os, sys
# todo: argparse

from parse import parser

def compile(args):
  switches = [arg for arg in args if arg.startswith('-')]
  targets = [arg for arg in args if not arg.startswith('-')]
  if not targets:
    targets = ['.']
  exit_code = 0
  for target in targets:
    exit_code += parser.parse(targets)
  return exit_code

if __name__ == '__main__':
  try:
    return compile(sys.argv)
  except FatalProblem as prob:
    ui.die(prob)