'''
A func models a function in lect.
'''

class lfunc(lunit):
  def __init__(self):
    lunit.__init__(self)
    self.takes = []
    self.returns = []
    self.body = None