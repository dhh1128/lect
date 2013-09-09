func main:
  takes:
    args: str[] +variadic
  returns:
    # Here we are assigning a return value when we declare what we'll
    # be returning. If the function exits without overriding, then
    # 0 is what we'll return. To override, we assign a new value to
    # the special variable named "returned".
    ?: int = 0
  impl:
    cl: cmdline = args
    if not cl:
      print(cl.errors)
      return 1
    switch cl.op:
      case "help":
        print(cl.help())
      case "version":
        print(cl.version())
      default:
        compile(cl.targets)
