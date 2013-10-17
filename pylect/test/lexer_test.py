import os, sys, unittest

# Make it possible to import stuff relative to app root
_app_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not _app_root_path in sys.path:
  sys.path.insert(0, _app_root_path)

from parse import lexer

class LexerTest(unittest.TestCase):

  def test_simple(self):
    txt = '''
use module

foo: class +threadsafe
  extends: bar
  make: func
    takes:
      - name: str +nullable
    returns:
      - error_code: int
'''
    lex = lexer.Lexer()
    types = [v for t, u, v in lex(txt)]
    self.assertEqual('[13, 97, 32, 97, 13, 13, 97, 58, 32, 97, 32, -1, 97, 13, 32, 97, 58, 32, 97, 13, 32, 97, 58, 32, 97, 13, 32, 97, 58, 13, 32, -1, 32, 97, 58, 32, 97, 32, -1, 97, 13, 32, 97, 58, 13, 32, -1, 32, 97, 58, 32, 97, 13]', str(types))
