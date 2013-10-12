import sys
# todo: argparse

def compile(args):
  switches = [arg for arg in args if arg.startswith('-')]
  targets = [arg for arg in args if not arg.startswith('-')]
  if not targets:
    targets = ['.']
  for target in targets:
    compiler.

if __name__ == '__main__':
  compile(sys.argv)