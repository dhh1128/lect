import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sandbox

def test_root():
  sb = sandbox.Sandbox('a/b/c/foo.sandbox/w/x/y')
  assert sb.root.endswith('a/b/c/foo.sandbox/')
