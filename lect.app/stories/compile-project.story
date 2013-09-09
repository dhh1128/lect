As a PROGRAMMER,
I want to comppile a complete sandbox
so I can turn my code into a set of mutually compatible assemblies.

Scenario: use current working directory with no switches

From any folder within a sandbox (that is, with the current working directory
set to anywhere inside a sandbox), the user types "lect build" and presses
Enter.

The lect tool performs an incremental build. The rough algorithm for the
build is:

1. Determine the correct build order based on the graph of compile-time dependencies.
2. Spawn worker threads with the goal of keeping the I/O and CPU 100% busy, but
   run the threads at below-normal priority, so that the rest of the system
   remains responsive.
3. Traverse the graph from leaves to root, building one component at a time.
4. For each component:
   a. Find any backtick sequences in source code. These are used to embed
      values or generate code at compile-time. Replace backtick sequences
      with their expansion and write a new version of the file, without the
      backtick sequence.
   b. Traverse the component in depth-first alphabetical order. For each class:
      i. Assemble partial classes into a set of files that define the class fully.
      ii. Generate a public interface for the class, and load its public interface
          into RAM.
      iii. Compile the class's implementation.
