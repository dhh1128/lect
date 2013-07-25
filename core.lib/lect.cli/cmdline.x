import lect.containers.list

type cmdline:
  // All members are automatically private.
  members:
    // A handle is the equivalent of a c++ unique_ptr.
    args: handle<list<str>>

  // All functions in an implementation unit are automatically private.

  // Begin functions with a capital letter to make range till paren easier
  // to find? Eh. Constants will begin with capitals as well...
  // Would really like either pep8 or spaces in func names.
  func is flag(arg: str) => bool:
    // As with python, len function for all containers instead of
    // a .length() method
    return str[0] == '-' && len(str) > 1 

  func cmdline(args: str[]):
    // We use the this pointer as in C++ and java -- although we never use ->
    // because the difference between ptr and ref is hidden.
    // We use "new" as operator for heap.
    this.args = new list<str>()
    // for loop as in python
    for arg in args:
      if is flag(arg):
        
      
    
