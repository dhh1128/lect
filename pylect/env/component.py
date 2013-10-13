import os

LIB_SUFFIX = '.lib'
APP_SUFFIX = '.app'
VALID_SUFFIXES = [LIB_SUFFIX, APP_SUFFIX]

class Component:
  '''
  A Component is a separately compilable project in lect. Components
  are always siblings of one another and reside within a Sandbox. Typically,
  each Component corresponds to a different repo in a dvcs.
  '''
  def __init__(self, sandbox, relpath):
    self.sandbox = sandbox
    if relpath.endswith('/') or relpath.endswith('\\'):
      relpath = relpath[0:-1]
    self.relpath = relpath
    self.packages = []
