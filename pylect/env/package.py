import os, weakref

PACKAGE_SUFFIX = '.pkg'

class Component:
  '''
  A Package is a folder within a Component that directly contains source code.
  All Packages are siblings of one another; there is no nesting.
  '''
  def __init__(self, component, relpath):
    self.component = weakref.ref(component)
    if relpath.endswith('/') or relpath.endswith('\\'):
      relpath = relpath[0:-1]
    self.relpath = relpath
    self.modules = []