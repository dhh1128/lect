'''
Track errors and warnings emitted by the program.
'''
# A problem may or may not represent a condition that should concern the programmer.
WARNING = 1
# Code is definitely wrong. Compilation will continue where possible.
ERROR = 2
# Something is wrong that will prevent the program from
FATAL = 3

# Use inspection to map constants to labels.
_labels_by_severity = {}
x = None
x = [x for x in locals() if x[0].isalpha() and x[0].isupper() and isinstance(locals()[x], int)]
print x
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

def define(name, num, msg):
  assert name not in globals()
  print('name = %s; msg = %s' % (name, msg))
  severity = None
  for sev in _labels_by_severity:
    if name.endswith(_labels_by_severity[sev]):
      severity = sev
      break
  assert severity
  class X(Problem):
    def __init__(self, ctx, *args):
        Problem.__init__(self, ProblemDef(num, msg, severity), ctx, *args)
  globals()[name] = X

define('CantFindSandboxError', 1, 'Unable to find sandbox. All code must be compiled relative to a sandbox to provide context.')
define('CantFindSandboxWarning', 2, 'Unable to find sandbox. All code must be compiled relative to a sandbox to provide context.')

if __name__ == '__main__':
  print _labels_by_severity