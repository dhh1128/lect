Design By Contract
------------------
Lect requires programmers to communicate clearly about expectations. All of the following topics
can be addressed in a function prototype, and many of them are mandatory:

* Acceptable and unacceptable input values or types, and their meanings
* Return values or types, and their meanings
* Error and exception condition values or types that can occur, and their meanings
* Side effects
* Preconditions
* Postconditions
* Invariants
* (more rarely) Performance guarantees, e.g. for time or space used, big-O claims

.. note:: TODO

   Presumably, most dbc ideas will be expressed as simple label:expr pairs.
   However, we need to understand how to do more complex preconditions, where
   if two of the parameters have such and such values, then a third parameter
   has this range.
