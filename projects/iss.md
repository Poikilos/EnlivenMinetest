# ISS Files
This file describes issues related to `*.iss` (Inno Setup projects).

## Working directory
(and main executable not in {app})

See setup-minetest-*.iss for running from {app}/bin and using that
as the working directory (remember to set that for both
Start Menu AND Desktop icons!).

The Inno Setup wizard doesn't seem to do a clear job of setting
the main executable. It sets it to an absolute path, but should
probably let you choose it after the file choosing step and let you
choose a relative path from there.
- See <https://groups.google.com/forum/#!topic/innosetup/pRa408kVOt4> to
  see if my feature request gets implemented to improve the GUI iss
  creator wizard in Inno Setup.
