# mtcompile-program-local.py

## Differences from mtcompile-program.pl

### Added
- Use $HOME/git/minetest if present INSTEAD of newline

### Removed
- EdgyTest options are mostly not present.
- FlagFakeMT4 options are mostly not present.
- FlagOldProto options are mostly not present.


## Known Issues
- [ ] Detect the number of cores instead of using `NUMJOBS = 3`
  (enforce a range of 1 to 3 like the original?)


## Code History
```
# $HOME/Downloads/git/felisPasseridae/Perl2Python/perl2python.pl $HOME/.config/EnlivenMinetest/linux-minetest-kit/mtcompile-program.pl > $HOME/git/locktopia/linux-minetest-kit-patched/mtcompile-program-local.py
# ^ won't work unless <https://github.com/felisPasseridae/Perl2Python/issues/3> is resolved.
#   (has many 'Use of uninitialized value $_ in pattern match (m//) at /home/owner/Downloads/git/felisPasseridae/Perl2Python/perl2python.pl line 179, <> line x.' where x is a line.
#if [ ! -d "$HOME/Downloads/git/Swati1910/Perl2Python-1" ]; then
#    mkdir -p $HOME/Downloads/git/Swati1910
#    git clone https://github.com/Swati1910/Perl2Python-1 $HOME/Downloads/git/Swati1910/Perl2Python-1
#    cd $HOME/Downloads/git/Swati1910/Perl2Python-1
#    git checkout patch-1
#fi
#$HOME/Downloads/git/Swati1910/Perl2Python-1/perl2python.pl $HOME/.config/EnlivenMinetest/linux-minetest-kit/mtcompile-program.pl > $HOME/git/locktopia/linux-minetest-kit-patched/mtcompile-program-local.py
#^ requires the CGI module for perl:
#  See comments at <https://github.com/felisPasseridae/Perl2Python/pull/4>.

if [ ! -d "$HOME/Downloads/git/uhayat/perl2python" ]; then
    mkdir -p $HOME/Downloads/git/uhayat
    git clone https://github.com/uhayat/perl2python $HOME/Downloads/git/uhayat/perl2python
    cd $HOME/Downloads/git/uhayat/perl2python
    git checkout patch-1
fi

python $HOME/Downloads/git/uhayat/perl2python/perl2python.py -i $HOME/.config/EnlivenMinetest/linux-minetest-kit/mtcompile-program.pl -o $HOME/git/locktopia/linux-minetest-kit-patched/mtcompile-program-local.py
```

Then manually fix functions:
- [x] pushd
- [x] popd
- [x] RunCmd
- [x] add `customExit` to replace `die`

Then manually fix uses of:
(errors caused by uhayat/perl2python)
- [x] `-f` perl feature
- [x] `-d` perl feature
- [ ] `segment` variable
- [x] Implement a `pushd` function
- [x] Implement a `popd` function
- [x] Implement a `GetOptions` function
- [x] (See new dict: `mapLongArgs`) Manually map argument aliases.
- [x] use triple quotes for instances of `END` or other self-defined
      stream end after `<<`
- [x] implement a `RunCmd` function
- [x] `die..if` (change to `if...customExit`)
- [x] `die..unless` (change to `if not...customExit`)
- [x] python2-style `print` without parenthesis
- [x] `TRUE` and `FALSE` (change to `True` and `False`)
- [ ] errant adding of spaces around equal signs within strings
- [x] errant use of `evalSed` without an input (`a =~ b` should become
      `a = evalSed(a, b)` not `evalSed(b)`)
- [x] commented `exit` statements (they should not be commented)
- [x] use of `str` as a variable (should only be used as a builtin
      Python function) (replace all with tmpStr)
- [ ] commented `open` commands
