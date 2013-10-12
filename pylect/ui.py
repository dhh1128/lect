import sys, os

INDENT = '  '

if os.name == 'nt':
  EOL = '\r\n'
else:
  EOL = '\n'

def wrap_with_indent(txt, indent=0, width=80):
  '''
  Figure out how to render a string within a given width,
  indenting as needed.
  '''
  assert width >= 10
  if indent:
    indent = INDENT * indent
  else:
    indent = ''
  width -= len(EOL)
  wrapped = ''
  if txt:
    if indent:
      txt = indent + txt
    while len(txt) > width:
      i = width
      last_reasonable_wrap = max(10, width - 20)
      last_punc = -1
      while i > last_reasonable_wrap:
        if txt[i] == ' ':
          wrapped += txt[0:i] + EOL
          txt = indent + txt[i + 1:]
          break
        elif (last_punc == -1) and not txt[i].isalnum():
          last_punc = i
        i -= 1
      if i == -1:
        if last_punc > -1:
          wrapped += txt[0:last_punc + 1] + EOL
          txt = indent + txt[last_punc + 1:]
        else:
          wrapped = txt[0:width - 1] + '-' + EOL
          txt = indent + txt[width - 1:]
  wrapped += txt
  return wrapped

def complain(msg, indent=0, width=80):
  sys.stderr.write(wrap_with_indent(msg, indent, width) + '\n')
  return 1

def report(msg, indent=0, width=80):
  sys.stdout.write(wrap_with_indent(msg, indent, width) + '\n')
