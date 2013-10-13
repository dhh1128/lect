import os, weakref

class Context:
  '''
  Keep track of which folder/file/line we are currently processing, the outcome
  of our work, and how generated structures integrate to the big picture.
  '''
  def __init__(self, sandbox_or_parent, relpath, line_num=0, near=None):
    if isinstance(sandbox_or_parent, Context):
      self._parent = weakref.ref(sandbox_or_parent)
      self._parent.children.append(self)
      self._sandbox = None
    else:
      self._parent = None
      assert sandbox_or_parent
      self._sandbox = weakref.ref(sandbox_or_parent)
    self.relpath = relpath
    self.line_num = line_num
    self.near = near
    self.modules = {}
    self.children = []
    self.errors = []
    self.warnings = []

  def count_problems(self):
    error_count, warning_count = len(self.errors), len(self.warnings)
    for child in self.children:
      e, w = child.count_problems()
      error_count += e
      warning_count += w
    return error_count, warning_count

  @property
  def sandbox(self):
    if self._parent:
      return self.parent.sandbox
    else:
      return self._sandbox

  @property
  def parent(self):
    p = self._parent
    if p:
      return p()

  @property
  def abspath(self):
    return self.sandbox.root + self.relpath

  def __str__(self):
    if self.line_num:
      if self.near:
        return '%s, line %d, near "%s"' % (self.relpath, self.line_num, self.near)
      return '%s, line %d' % (self.relpath, self.line_num)
    return self.relpath
