// A .i.x file defines an interface. It can't have any impl in it,
// or compiler will complain.

type cmdline:
  // Not sure whether I like python's doc string convention, because
  // it has to follow the line it describes.

  # Define semantics for lect's unique cmdline.
  
  extends: core.cmdline
  // Do these func decls need a colon or something?
  // Do I want ctor to be named "ctor" or "cmdline"?
  func cmdline(args: str[])

  // Allow more than one returned value from func?
  // Allow named return vals?
  // What about exceptions?

  func compile(targets: str[]) => int
    
