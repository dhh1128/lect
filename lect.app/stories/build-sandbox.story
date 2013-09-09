Story: Build a sandbox

As a PROGRAMMER,
I want to build a complete sandbox
so I can turn my code into a set of mutually compatible assemblies.

Scenario 1: successful shell build using cwd with no args

Given a shell where the current working directory is within sandbox A,
 and the sandbox is properly configured
 and the build has no reason to fail
when programmer types "lect build" and presses Enter
then an incremental build of the entire sandbox is performed
 and the build is performed in reverse dependency order (from leaves
     to root of the sandbox)
 and stdout contains status messages from the build process
 and stderr contains no error messages from the build process
 and the exit code is 0.
