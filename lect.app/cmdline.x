class cmdline:
  inherits: core.cli.cmdline
  # ctor is how we specify a constructor
  # ctors can call other constructors
  ctor:
    takes:
      args: str[] +variadic
    impl:
      # The ~'...' notation for strings mean that they are localizable.
      help = add_cmd('help', ~'Display help, possibly for a specific sub-command.')
      help.add_positional_token('topic': +optional, ~'specific topic')
      version = add_cmd('version', ~'Display the version of this program.')
      interact = add_cmd('interact', ~'Enter interactive mode.')
      make = add_cmd('make', ~'Create one or more targets.')
      make.add_flag('verbose', ~'Emit more information.')
      make.add_value('define': +token(50) +optional +repeatable)
      # variadic is the equiv of C#'s "paramarray"
      # exists demands that file/folder must exist
      make.add_positional_token('target': path[] +variadic +exists)
      stub = add_cmd('expand', ~'Expand code where functionality is implied or stubbed.')
      stub.copy_syntax(make)
      
  
