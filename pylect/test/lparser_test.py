import os, sys, tempfile, StringIO, time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import lparser

def test_process_handles_correct_files_in_correct_order():
  root = tempfile.mkdtemp()
  print(root)
  def fill(subdir):
    path = os.path.join(root, subdir)
    os.mkdir(path)
    for i in range(3):
      with open(os.path.join(path, 'file%d.l' % i), 'w'):
        pass
  for i in range(2):
    fill('subdir%d' % i)
  stdout = sys.stdout
  sys.stdout = StringIO.StringIO()
  try:
    lparser.process(root)
    txt = sys.stdout.getvalue()
    print ('here is what we wrote: %s' % txt)
    assert txt == 'x'
  finally:
    sys.stdout = stdout
    for i in range(2):
      path = os.path.join(root, 'subdir%d' % i)
      for f in os.listdir(path):
        os.remove(os.path.join(path, f))
      time.sleep(0.01)
      os.rmdir(path)
    time.sleep(0.01)
    os.rmdir(root)
