types
--------
  pod
    java's types
    codepoint (32-bit number)
    unions
    pod types used to wrap C/C++ stuff
    
containers
--------------
  map
  list
  vector/array
  set
  queue
  stack
  trees
    red/black or AVL
    btree

interfaces
----------
numeric
  standard integers
  byte? (inherently unsigned)
  code point? (inherently unsigned)
  float, double, decimal
  currency
discrete
  integers but not floats
continuous
  floats but not integers
  dates
container (iterable)
  


in and out parameters aren't distinguished by marks but by section?
  func do_something:
    takes:
      x: bool
      y: int +range(1,30)
    returns:
      z: double
      err: exception

pre, post, invariant
  func clone_template:
    takes:
      template: +assert(it.is_valid)
      deep: bool
    returns:
      cloned: template
    pre:
      not this.template_list.is_full()
    post:
      cloned != null
      cloned in this.template_list



======
class bank_account:
  invariant:
    balance >= 0 and balance <= max_balance

  members:
    max_balance: +const money = 1e8 ; is this how I want to do const?
    balance: money = 0
    is_locked: bool = false

  func credit:
    takes:
      amount: money
    pre:
      amount > 0
      amount + balance <= max_balance, else "This would produce a balance > {1}." % max_balance
    post:
      new(balance) = old(balance) + amount
    body:
      balance += amount
  func debit:
    takes:
      amount: money
    pre:
      amount > 0
      amount - balance >= 0, else "This would produce a negative balance."
    post:
      new(balance) = old(balance) - amount
    body:
      balance -= amount
  func lock:
    takes:
      value: bool
    pre:
      value != is_locked
  func get_balance: +pure
    pre:
      !is_locked
      
======




Marks
---------
range<T>(min, max): tells acceptable range for a discrete  (for numbers or enums or )
    weekday: int +range(1,8) #do we want half-open? If so, how do we express beyond-the-end with enums?
    birth_month: +range(July, December)

variadic: tells compiler that this is a varargs/... parameter that takes 0 to N items

const: tells compiler that param doesn't change?

named: requires that a parameter be named when used; on by default for booleans

regex<str>(expr): specifies regex that must match a string param

text<str>(max_len=int.max, max_lines=int.max, min_len, min_lines): specifies that a string cannot contain unprintable chars

nullable<T>: specifies that null is a valid value for any reference type. Not present by default, so nullability is precluded unless you specify otherwise.

empty<T: is container>: allows empty containers on parameters

pure<T: is func>: has no side effects

threadsafe<T: is not pod>: asserts that class can be safely shared across multiple threads.
  Should be rare, because lect prefers the go approach to parallelism: share memory by communicating rather than communicating by sharing memory. Example that needs this is system-wide logger (if we implement one; but why not just have one logger per thread?)

  Do we want to implement atomics like this:

    ref_count: int +threadsafe

units<T: is quantifiable>: makes units of measurement explicit, automatically performs conversions, prevents incompatible units
  distance: float +units(kilometers)
  calendar "units" expressed with this? probably not, because the meaning/amount of "month" and "year" is variable

path.exists
path.is_folder
path.is_file
path.readable
path.writable

immutable: says that once created, a class doesn't change its state at all. On by default?

+assert(it.is_open)
  mark to assert that object has a particular internal state (e.g., file is open for write, socket is connected)
