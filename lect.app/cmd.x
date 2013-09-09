class cmd:
  func add_positional_token:
    takes:
      # I'd like to use lect's "alias" mechanism (akin to typedefs, but more powerful
      # because it can include marks and be parameterized) to make defining the
      # semantics of str params less repetitive. For example, I'd like to define
      # a "sentence" alias that is a single non-null, non-empty line with no CRLF.
      token: str +text(1, 25) 
      description: str +text(1,200) 
  func add_flag:
    # The "resembles" statement says that add_flag will take the same parameters and
    # have the same preconditions and postconditions and return values as
    # add_positional_token -- unless/until it overrides something. Typically it
    # will override the impl, but this saves a lot of redundant code. In fact, it
    # is possible to define a hidden function with no impl, and just use it as a
    # pattern to save code later. A "resembles" relationship is not visible in an
    # external interface -- only in internal impl.
    resembles: add_positional_token
  func add_value:
    resembles: add_positional_token
  func copy_syntax:
    takes:
      from: cmd
    
