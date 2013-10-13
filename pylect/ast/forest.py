class Forest:
  '''
  Contain all parsing results as a list of Abstract Syntax Trees.
  '''
  def __init__(self, sandbox):
    self.sandbox = sandbox
    self.trees = []

  def add(self, tree):
    self.trees.append(tree)