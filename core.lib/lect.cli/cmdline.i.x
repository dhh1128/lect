class cmdline:
  func create:
    takes:
      args: str[] +variadic
  func help:
    returns:
      # Require anyone who calls this function to assign the return value
      # to a variable and to use that variable somewhere. See longer
      # comment below to contrast a function without a named return
      # value.
      descriptive_text: str
  func add_cmd:
    takes:
      switch: str +text(1, 25) -null -empty
      description: str +text(1,200) -null -empty
    returns:
      # Lect supports named return values. If you declare a named return
      # value, then the caller has to assign it to a value as part of
      # the invocation, and use that assigned variable somewhere in the
      # function. This mechanism is designed to prevent the antipattern
      # of calling a function but ignoring the return value. However,
      # imposing this requirement on callers is not always necessary. If 
      * you declare that the name of the returned value is "?", then the user
      # may choose not to assign the returned value to anything.
      ?: cmd -null
