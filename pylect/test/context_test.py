import os, sys, unittest

# Make it possible to import stuff relative to app root
_app_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not _app_root_path in sys.path:
  sys.path.insert(0, _app_root_path)

from env import context, sandbox

class ContextTest(unittest.TestCase):
  def setUp(self):
    sb = sandbox.Sandbox('a' + sandbox.SUFFIX)
    self.ctx = context.Context(sb, 'foo.lib/bar.cls/make-func.l', 2)

  def test_relpath(self):
    self.assertEqual('foo.lib/bar.cls/make-func.l', self.ctx.relpath)

