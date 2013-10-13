import os, sys, unittest

# Make it possible to import stuff relative to app root
_app_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not _app_root_path in sys.path:
  sys.path.insert(0, _app_root_path)

from parsekit import parse_context, sandbox

class ParseContextTest(unittest.TestCase):
  def setUp(self):
    sb = sandbox.Sandbox('a.lsandbox')
    self.ctx = parse_context.ParseContext(sb, 'a.lsandbox/foo.llib/bar.lclass/make-func.l', 2)

  def test_relpath(self):
    self.assertEqual('foo.llib/bar.lclass/make-func.l', self.ctx.relpath)
