func main(str[] args) => int:
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
