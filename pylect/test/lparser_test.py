import os, sys, tempfile, StringIO, time, unittest

# Make it possible to import stuff relative to app root
_app_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not _app_root_path in sys.path:
  sys.path.insert(0, _app_root_path)

from parsekit import lparser

class LParserTest(unittest.TestCase):

  def setUp(self):
    self.root = tempfile.mkdtemp()
    def fill(subdir):
      path = os.path.join(self.root, subdir)
      os.mkdir(path)
      # Create files in reverse alphabetical order, so we can
      # see whether we iterate in better order.
      for i in [3, 2, 1]:
        with open(os.path.join(path, 'f%d.l' % i), 'w'):
          pass
    for i in [2, 1]:
      fill('d%d' % i)
    self.old_stdout = sys.stdout
    sys.stdout = StringIO.StringIO()

  def tearDown(self):
    sys.stdout = self.old_stdout
    for subdir in os.listdir(self.root):
      path = os.path.join(self.root, subdir)
      for f in os.listdir(path):
        os.remove(os.path.join(path, f))
      time.sleep(0.01)
      os.rmdir(path)
    time.sleep(0.01)
    os.rmdir(self.root)

  def test_process_handles_correct_files_in_correct_order(self):
    lparser.process(self.root)
    items = sys.stdout.getvalue().split('\n')
    items = [l.strip() for l in items if (l.strip() and not l.startswith(' '))]
    items = ', '.join([l[len(self.root) + 1:] for l in items])
    #self.old_stdout.write('"%s"\n' % items)
    assert 'd1/f1.l, d1/f2.l, d1/f3.l, d2/f1.l, d2/f2.l, d2/f3.l' == items

  def test_sample_sandbox(self):
    pass