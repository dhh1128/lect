'''
A param is a named definition of particular input to a function.
'''

class lparam(lunit):
  def __init__(self):
    lunit.__init__(self)
    self.name = None
    self.ltype = None