class lect:
  # The 'app' base class supports a cmdline and an exit code.
  inherits: app
`
cal = calendar.get_gregorian()
base_date = date.parse('2013-08-01')
'
  version:
    build_date: "`cal.format(date.now())`"
    build_id: `guid.new()`
    cvs_revision: `cvs.revision()`
    # This next line shows how lect code can run at compile time.
    # Anything between backticks is scanned and expanded
    # before the code is parsed.
    major: 1
    minor: 0
    revision: 'date.now() - base_date' +units(dateunits.days)
