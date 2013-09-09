A programming language that improves collaboration is valuable.

Lect encourages collaboration by...
===================================

making assumptions explicit
--------------------------------

Problem
_______
Consider the following C++ function, taken almost at random from
a production codebase and tweaked to protect the innocent: ::

  bool Vehicle::SetCustomAttr(VAttrEnum which, char const * value, int sinceYear) {
      // implementation
  }

What assumptions of the coder are implicit here?

* Are all possible values of `VAttrEnum` valid for the `which` parameter?
* What is the function going to do if an arbitrary `int` is cast to `VAttrEnum`, and it's
  not a number that corresponds to a member of the enum?
* Is the null string or the empty string valid for the `value` parameter?
* What rules apply to `sinceYear`? If it's telling which model year began
  to exhibit the attribute, what happens if we pass in 1650? 2300?
* Is there any interaction among the parameters (e.g., `value` can only be `null` if
  `which` is an optional attribute)?
* Does the function do any synchronization to make itself thread-safe?
* Presumably, the function returns `true` if the attribute is successfully set.
  What happens if the attribute wasn't changed because the new value and the
  old value were identical?
* Does the function do any validation of `value`?

In most modern codebases, questions like these run rife, no matter which language
is in play. Here's a random prototype from a production python codebase: ::

  def get_section_info_from_file(section, file):
    # implementation

In this case, the function reads a section of an INI file from disk. Simple.
But we are still forced to study the body of the function to answer questions
like these:

* Is `section` a numeric constant, or a string? If it's a string, is it case-sensitive?
* What happens if the section is not found?
* Is `file` a path to a file, or an open file handle? If a path, can we pass a URL
  or other file-like objects, or only a path for a traditional file system?
* What happens if `file` is `None` or is a file opened in the wrong mode? Do we get an
  exception, or an empty return value?

**When answers to these questions differ in the minds of the producer and consumer of the
code, bugs result. This discourages collaboration. **

You might say that if doc comments were used with discipline, these assumptions
would be far less likely to cause problems--and you'd be right. But consider this:

* Compilers typically don't enforce use of doc strings--or if they do, they only enforce
  a few key ingredients, such as a comment for every parameter. What developers choose
  to put in comments can be useful or a total waste of time.
* Even if comments explain the coder's intentions effectively, they only explain them
  to other human beings--not to the compiler. As a result, the compiler cannot sanity
  check usage of the code in other places.

Lect's solution
_______________
First of all, lect is aware of all of these possible questions, and for each, it
explicitly defines a default answer:

* Whenever an enum is used as a parameter, any pre-defined value of the enum is
  valid unless the coder specifies otherwise.
* Numeric and date parameters can carry any value in their range, by default.
* Null args are invalid unless the coder specifies otherwise.
* Parameters are considered independent unless the coder specifies otherwise.
* Classes are either thread-safe, or (by default) they are not. Individual methods
  must conform to their class threading strategy.

Other programming languages might give these same answers, but the answers are
implicit and permissive; the compiler doesn't use these answers to validate correctness
of the code. On the other hand, lect's compiler will test whether the logic of the
function reflects these assumptions. If it doesn't, you get a compile error, which
you can fix by being more explicit.

This brings us to lect's second innovation: lect makes it exceedingly easy to declare
custom semantics. Let's rewrite the first function in lect, and be clearer about
what we intend: ::

  class vehicle +threadsafe:
    func set_attr:
      takes:
        which: vehicle_attr +customizable
        value: str +text(1, 25)
        since_year: int +range(this.first_year, 2100)
      returns: bool +ifstatechange
      # impl

Custom semantics in this example are declared using lect's "marks" feature, which is
similar to annotations in java or attributes in .NET. The marks are visible as
tokens preceded by - or +:

* `threadsafe` is a pre-defined mark in lect, and the + in front of it adds the mark
  to this class. The `threadsafe` mark means that the coder intends for
  a class to usable from multiple threads at the same time. This is *not* the same
  thing as java's `synchronized` keyword. It doesn't implement any locking. But it
  tells the lect compiler to verify that every public or protected method on the
  class is threadsafe, and it tells consumers of the code that it's safe to use
  a reference to a `vehicle` from more than one thread at the same time. If the
  implementation of the `set_attr` function modifies the object's state in a way
  that's not thread-safe, the code won't compile.
* `customizable` is a user-defined mark that tells the compiler that whenever
  a `vehicle_attr` value is passed as the `which` parameter, it must be a `vehicle_attr`
  that carries the `customizable` mark. Adding marks to enums is trivial and common
  in lect.
* `text` is another pre-defined mark. It requires that strings consist of printable
  characters only. Its first parameter is a max line count, and its second is a max
  length. This coder is requiring `value` to consist of a single line of at most 25
  characters.
* `range` tells what numbers are acceptable values for `since_year`. Consistent with
  ranges everywhere else in lect, this is a half-open range.
* `ifstatechange` says that the bool's value depends on whether the state of the object
  actually changes.

Look at how long it took us to explain these semantics in prose, versus how tersely
we expressed them in lect.
