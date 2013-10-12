import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ui

def test_wrap_with_indent():
  #print(('.........X' * 7) + '12345678')
  long_line = 'the quick1brown fox2jumped ov3r the laz4 red dogs ' * 10
  long_line = long_line.rstrip()
  assert ui.wrap_with_indent('') == ''
  assert ui.wrap_with_indent('abc') == 'abc'
  assert ui.wrap_with_indent(long_line) == '''the quick1brown fox2jumped ov3r the laz4 red dogs the quick1brown fox2jumped
ov3r the laz4 red dogs the quick1brown fox2jumped ov3r the laz4 red dogs the
quick1brown fox2jumped ov3r the laz4 red dogs the quick1brown fox2jumped ov3r
the laz4 red dogs the quick1brown fox2jumped ov3r the laz4 red dogs the
quick1brown fox2jumped ov3r the laz4 red dogs the quick1brown fox2jumped ov3r
the laz4 red dogs the quick1brown fox2jumped ov3r the laz4 red dogs the
quick1brown fox2jumped ov3r the laz4 red dogs'''
  assert ui.wrap_with_indent(long_line, 3) == '''      the quick1brown fox2jumped ov3r the laz4 red dogs the quick1brown
      fox2jumped ov3r the laz4 red dogs the quick1brown fox2jumped ov3r the
      laz4 red dogs the quick1brown fox2jumped ov3r the laz4 red dogs the
      quick1brown fox2jumped ov3r the laz4 red dogs the quick1brown fox2jumped
      ov3r the laz4 red dogs the quick1brown fox2jumped ov3r the laz4 red dogs
      the quick1brown fox2jumped ov3r the laz4 red dogs the quick1brown
      fox2jumped ov3r the laz4 red dogs the quick1brown fox2jumped ov3r the
      laz4 red dogs'''