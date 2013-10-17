import os, sys, unittest

# Make it possible to import stuff relative to app root
_app_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not _app_root_path in sys.path:
  sys.path.insert(0, _app_root_path)

from parse import lexer

def tokenize(txt):
  lex = lexer.Lexer()
  tokens = [tuple for tuple in lex(txt)]
  return tokens

class LexerTest(unittest.TestCase):

  def test_unique_tokens(self):
    tokens = [t for t in dir(lexer) if t.startswith('t_')]
    dups = []
    numbers = {}
    for t in tokens:
      n = getattr(lexer, t)
      if n in numbers:
        dups.append((t, n))
        original = (numbers[n], n)
        if original not in dups:
          dups.append(original)
      else:
        numbers[n] = t
    if dups:
      self.fail('Duplicate tokens: %s' % ', '.join([str(x) for x in dups]))

  def assert_token(self, start, end, token_type, token):
    self.assertEqual(start, token[0])
    self.assertEqual(end, token[1])
    self.assertEqual(token_type, token[2])

  def test_quote(self):
    token = tokenize('"abc"')[0]
    self.assert_token(0, 5, lexer.t_quote, token)

  def test_mark(self):
    token = tokenize('x: +nullable abc')[3]
    self.assert_token(3, 12, lexer.t_mark, token)

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
    code:
      # This is a comment
      x := 3
      y: double = (x / 6)
      x += 4
      y -= 6
      x /= 4
      y *= 3
      y = x.get_avg_rainfall("peru", "summer") * (9 + 2)
      txt := ~"a translated string"

'''
    lex = lexer.Lexer()
    types = [token_type for start, end, token_type in lex(txt)]
    tokens = [(t, getattr(lexer, t)) for t in dir(lexer) if t.startswith('t_')]
    missing = []
    for t in tokens:
      if t[1] not in types and t[1] != lexer.t_invalid:
        missing.append(t)
    if missing:
      self.fail('Tokens not exercised by test: %s' % ', '.join([str(t) for t in missing]))
    self.assertEqual(
      '[13, 97, 32, 97, 13, 13, 97, 58, 32, 97, 32, 1, 13, 9, 97, 58, 32, 97, 13, 9, 97, 58, 32, 97, 13, 9, 97, 58, 13, 9, 45, 32, 97, 58, 32, 97, 32, 1, 13, 9, 97, 58, 13, 9, 45, 32, 97, 58, 32, 97, 13, 9, 97, 58, 13, 9, 35, 13, 9, 97, 32, 58, 61, 32, 48, 13, 9, 97, 58, 32, 97, 32, 61, 32, 40, 97, 32, 47, 32, 48, 41, 13, 9, 97, 32, 104, 32, 48, 13, 9, 97, 32, 106, 32, 48, 13, 9, 97, 32, 108, 32, 48, 13, 9, 97, 32, 103, 32, 48, 13, 9, 97, 32, 61, 32, 97, 46, 97, 40, 34, 44, 32, 34, 41, 32, 42, 32, 40, 48, 32, 43, 32, 48, 41, 13, 9, 97, 32, 58, 61, 32, 126, 34, 13, 13]',
      str(types))

