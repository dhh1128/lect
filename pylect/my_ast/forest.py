'''
A Forest is the container for all parsing that we do; it holds multiple Abstract Syntax Trees.
'''

class Forest:
  def __init__(self, sandbox):
    self.sandbox = sandbox
    self.trees = []
  def add(self, tree):
    self.trees.append(tree)