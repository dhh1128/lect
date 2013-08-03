Lect Specification
==================

1. Introduction
----------------
Lect is a general-purpose, concurrent, object-oriented programming
language. It is compiled and memory-managed (but not garbage-collected). 

Lect borrows liberally from other modern programming languages--
notably, python, C++, java, C#, go, and D. Given the wide acceptance and
deep thought behind these languages, one might wonder why a new language
is needed. The answer is that cloud computing, pervasive network
connectivity, and the mobile revolution are changing the software
landscape. We need a language that is friendlier to massive parallelism,
that helps teams to communicate even though they're scattered across
the globe, that has a built-in immune system against bugs and
technical debt, that teaches correct mental models without being pedantic,
that facilitates distributed and organic architectures, that scales
well up down and out, that performs to the potential of hardware, and
that understands concepts such as fabrics and ecosystems.

In short, we need a better way to expand the software landscape.

Lect does not pretend to be all things to all programmers. Its features
are less compelling if your problem calls for quick-and-dirty scripting,
or if you are a one-person software shop. But it shines when problems
are complex, evolving, parallel, and network-centric. It shines when
testing is difficult, performance demands are high, and many people
will create and maintain the code.

2. How this spec is organized
------------------------------
This specification describes lect's grammar, 
