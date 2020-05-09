# General Test Documentation
This documentation covers how to generate testing procedures. For an
example of actual test documentation designed using this document, see
[mapgen.md](mapgen.md).

NOTICE: I originally created this document for my Software Development
II class. I didn't do it here first nor plagiarize.

## Overview
Implementing each manual test document’s "Instructions for testers" as
a web form where they can enter results is the most efficient way to
implement the tests. Choosing the web form from a list of test forms
should reset the test environment and start the server. Each result
area should contain a radio group where the user can choose "pass" or
"fail" and enter an optional comment. The user should only be able to
run the test once until a new git commit appears in the branch on git
or administrators manually reset the test. Resetting the test includes
restoring everything backed up in the "Backup" step(s) of the General
Test Design section.

The tests can either integrate with GitHub or use another issue tracker
with a network API. If the issue exists, the issue will receive the new
comment from the given user. If the test fails for a closed issue, the
issue will reopen.


## General Test Design Guide
This section is a template for the "Test Design Guide" section of each
test document.
1. Set the configuration.
2. Backup the configuration.
3. Setup the world (this will only include entering the world and
   changing it in the case of non-mapgen test documents).
4. Backup the world (for comparison with the original or for other kinds
   of analysis).
