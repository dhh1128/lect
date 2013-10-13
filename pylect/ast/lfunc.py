class LFunc(lunit):
  '''
  Model a function in lect.
  '''
  def __init__(self):
    lunit.__init__(self)
    self.takes = []
    self.returns = []
    self.body = None