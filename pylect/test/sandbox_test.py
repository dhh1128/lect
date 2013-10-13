import os, sys

# Make it possible to import stuff relative to app root
_app_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not _app_root_path in sys.path:
  sys.path.insert(0, _app_root_path)

from parsekit import sandbox

def test_root():
  sb = sandbox.Sandbox('a/b/c/foo.lsandbox/w/x/y')
  assert sb.root.endswith('a/b/c/foo.lsandbox/')
