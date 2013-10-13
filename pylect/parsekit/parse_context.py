'''
A ParseContext keeps track of which file and which line we are currently processing.
'''

import os

class ParseContext:
  def __init__(self, sandbox, path, line=0, near=None):
    self.sandbox = sandbox
    path = os.path.normcase(os.path.abspath(path))
    assert path.startswith(self.sandbox.root)
    self.path = path
    self.line = line
    self.near = near
  @property
  def relpath(self):
    return os.path.relpath(self.path, self.sandbox.root)
