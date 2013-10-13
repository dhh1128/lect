'''
Track errors and warnings emitted by the program.
'''
# A problem may or may not represent a condition that should concern the programmer.
WARNING = 1

# Code is definitely wrong. Compilation will continue where possible.
ERROR = 2

# Something is wrong that will prevent the program from
FATAL = 3

# Use reflection to map constants to labels.
_labels_by_severity = {}
x = None
x = [x for x in locals() if x[0].isalpha() and x[0].isupper() and isinstance(locals()[x], int)]
for lbl in x:
  _labels_by_severity[locals()[lbl]] = lbl[0].upper() + lbl[1:].lower()
del lbl
del x

class ProblemDef:
  def __init__(self, number, msg, severity):
    assert severity in _labels_by_severity
    self.number = number
    self.msg = msg
    self.severity = severity
  @property
  def label(self):
    return _labels_by_severity[self.severity]

class Problem(Exception):
  def __init__(self, pdef, ctx, *args):
    self.args = args
    self.pdef = pdef
    self.ctx = ctx
    self.args = args
  def __str__(self):
    return '%s %d at %s: %s' % (self.pdef.label, self.pdef.number, self.ctx, self.pdef.msg % self.args)

class FatalProblem(Problem):
  def __init__(self, pdef, ctx, *args):
    assert pdef.severity == FATAL
    Problem.__init__(self, pdef, ctx, *args)

def define(name, num, msg):
  assert name not in globals()
  severity = None
  for sev in _labels_by_severity:
    if name.endswith(_labels_by_severity[sev]):
      severity = sev
      break
  assert severity
  base_class = Problem
  if severity == FATAL:
    base_class = FatalProblem
  class X(base_class):
    def __init__(self, ctx, *args):
        Problem.__init__(self, ProblemDef(num, msg, severity), ctx, *args)
  globals()[name] = X
