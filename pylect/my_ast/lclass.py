class lclass(lunit):
  # Models a class in the lect ecosystem
  def __init__(self):
    lunit.__init__(self)
    self.fqname = None
    self.methods = {}
    self.properties = {}