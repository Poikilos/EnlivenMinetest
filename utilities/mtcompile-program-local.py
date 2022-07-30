#!/usr/bin/env python3
"""
---------------------------------------------------------------------
                          file information
---------------------------------------------------------------------

 Name:     This program is based on mtcompile-program.pl
 Purpose:  Linux Minetest build script
 License:  Creative Commons Attribution-NonCommercial-ShareAlike 4.0.
           Attribution: OldCoder (Robert Kiraly)
                        and Poikilos (Jake Gustafson)
 Revision: See program parameters section

---------------------------------------------------------------------
                           important note
---------------------------------------------------------------------

 This software is provided on an  AS IS basis with ABSOLUTELY NO WAR-
 RANTY.  The  entire risk as to the  quality and  performance of  the
 software is with you.  Should the software prove defective,  you as-
 sume the cost of all necessary  servicing, repair or correction.  In
 no event will any of the developers,  or any other party, be  liable
 to anyone for damages arising out of use of the software, or inabil-
 ity to use the software.

---------------------------------------------------------------------
                              overview
---------------------------------------------------------------------
"""
import sys
import subprocess
import shutil
import re
import tarfile
import stat
from zipfile import ZipFile
import zipfile
import platform
import os


def echo0(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def customExit(msg):
    echo0(msg)
    sys.exit(1)


def isExecutableFile(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)


def which(prog):
    """
    Check for the given file within os.environ["PATH"], which contains
    paths separated by os.pathsep.
    NOTE: sys.path is NOT applicable, since it only has Python paths.
    """
    for thisPath in os.environ["PATH"].split(os.pathsep):
        sub_path = os.path.join(thisPath, prog)
        if os.path.isfile(sub_path):
            print("* using {} as {}".format(sub_path, prog))
            return sub_path
    return ""


def zipdir(path, ziph):
    """
    Zip an entire directory.
    See Mark Byers' Dec 6, 2009 answer edited by JosephH Feb 24, 2016
    on <https://stackoverflow.com/questions/1855095/how-to-create-a-zip-
    archive-of-a-directory-in-python>
    """
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def endsWithAny(haystack, needles):
    for needle in needles:
        if haystack.endswith(needle):
            return True
    return False


def containsAny(haystack, needles):
    for needle in needles:
        if needle in haystack:
            return True
    return False


def startsWithAny(haystack, needles):
    for needle in needles:
        if haystack.startswith(needle):
            return True
    return False


# Label must be single-quoted here
USAGE_TEXT = """
Usage: {PROGNAME} --options --build

The "--build" switch is required. It needs to be specified on the com-
mand line or you'll get this  usage text.  The other switches are opt-
ional.

The command-line argument "build", specified without dashes, will also
work.

----------------------------------------------------------------------

Background information related to "builds":

1. Minetest,  or this version,  uses a combined source and  production
tree.  I.e.,  a single tree can serve both purposes until it's cleaned
up for distribution.

2. The  production tree is portable in the sense  that it can be moved
to different directories on a given system and  the program will still
work.

3. The production tree  isn't  portable in the sense that it'll run on
different systems unless the  "--portable" or "--makeprod" option swi-
tch os used.

4. By default,  this script deletes the  source tree on each run,  un-
packs an  included source tarball,  and deletes unneeded "build" files
after a build is completed. The last step results in a pure production
as opposed to source tree.

Command-line  option switches  can be used  to modify  this  behavior.
Examples include "--noclean" and "--gitreset".

----------------------------------------------------------------------

Option switches:

--noclean       # If --noclean is specified,  this script tries to re-
 use the existing source tree,  if there is one,  and
 doesn't deleted "build" files afterward.

 The "--git*" and "--debug" switches  imply this swi-
 tch.
 Aliases: --notidy

--server        # Build server & not client unless --client also
--client        # Build client & not server unless --server also
 Default: If neither  is set, both are implied
          If just one is set, the other is off

--postgresql    # Enable PostgreSQL (requires installed copy)
 Aliases: --postgres

--redis         # Enable Redis      (requires installed copy)

--debug         # Build a "debug" version of the program  suitable for
 use with "gdb".

--makeprod      # Build a  portable  production release  (ZIP file) of
 Linux Minetest.  This is only needed  by  people who
 wish to redistribute the program. The switch implies
 --portable.  It isn't  compatible with  --noclean or
 --debug.

--portable      # Build a portable version.  If this  isn't specified,
 the copy of  Minetest built is tailored  to your ma-
 chine and may only run on an identical machine (same
 hardware,  distro, and distro release).  At the same
 time,  non-portable versions may be slightly faster.

--gitreset      # Delete  any  existing source  tree and  try  to do a
 fresh "git clone".

--gitpull       # Try  to  update the current  source tree using  "git
 pull".  If there is no source  tree  or  it's not  a
 "git" tree, this switch is the same as "--gitreset".

 The "git" switches  require both the  "git" software
 package and Internet access.

--safe          # Don't delete existing source trees automatically.

--edgy          # Build  EdgyTest instead of  Final Minetest.  Implies
 "--fakemt4".

--fakemt4       # Pretend to be MT 4. Implies "--oldproto".

--oldproto      # Limit network protocol used to level 32. For the mo-
 ment,  this is the default mode and  there is no way
 to disable it.

--help          # Display usage text and exit.
 Aliases: --usage
For full documentation, see "linux-minetest-kit.txt".

--MT_SRC=<minetest> # Set the minetest source path to a
                      # locally-modified copy, such as
                      # $HOME/git/minetest

Before using this script, please
see doc/mtcompile-program-local.md in EnlivenMinetest
for changes and progress on implementing features from
mtcompile-program.pl.
"""

# ----------------------------------------------------------------------
#                            module setup
# ----------------------------------------------------------------------

# TODO: Trap warnings to mimic the Perl version?
#SIG["__WARN__"] = sub { die @_; }

# ----------------------------------------------------------------------
#                         program parameters
# ----------------------------------------------------------------------

def streamEdit(inPath, replacements):
    """
    Replace parts similarly to sed ("stream editor").

    See David Miller's Dec 13, 2010 answer edited by dpb Jul 23, 2013
    on <https://stackoverflow.com/questions/4427542/how-to-do-sed-like-
    text-replace-with-python>

    Sequential arguments:
    inPath -- Edit then save the file at this path.
    replacements -- a replacements dict where the key is the string or
        regex, and the value is the new string to use in cases of]
        matches.

    """
    with open(inPath, "r") as sources:
        lines = sources.readlines()
    with open(inPath, "w") as sources:
        for rawLine in lines:
            line = rawLine
            for k, v in replacements.items():
                line = re.sub(k, v, line)
            sources.write(line)


def _UNUSED_evalSed(line, sedStr):
    """
    Mimic sed.
    Example:
    To mimic Perl `$str =~ s@\s+@ @gs;` do `evalSed(str, "s@\s+@ @gs")`.
    For m/, use re.findall() instead.
    """
    # - See <https://stackoverflow.com/questions/8903180/how-to-use-sed-
    #   without-a-file-with-an-env-var>
    # - See <https://stackoverflow.com/questions/3503879/assign-output-
    #   of-os-system-to-a-variable-and-prevent-it-from-being-displayed-
    #   on>
    return os.popen('echo "{}" | sed "{}"'.format(line, sedStr)).read()


PURPOSE = 'Linux Minetest build script'
REVISION = '200522'  # version of this script, not linux-minetest-kit
PROFILE_DIR = None
HOME_V = "HOME"
if platform.system() == "Windows":
    HOME_V = "USERPROFILE"
PROFILE_DIR = os.environ.get(HOME_V)

EXTRACTED_DIR = None
if os.path.isdir("mtsrc"):
    EXTRACTED_DIR = os.getcwd()
elif PROFILE_DIR is not None:
    EXTRACTED_DIR = os.path.join(PROFILE_DIR, ".config",
                                 "EnlivenMinetest",
                                 "linux-minetest-kit")
    if not os.path.isdir(EXTRACTED_DIR):
        print("You must run this from the directory of the extracted")
        print("linux-minetest-kit or have {}".format(EXTRACTED_DIR))
        exit(1)
else:
    if not os.path.isdir(EXTRACTED_DIR):
        print("You must run this from the directory of the extracted"
              "linux-minetest-kit or have a {} variable"
              "".format(HOME_V))
        exit(1)

GITURL = 'http://git.minetest.org/minetest/minetest.git'
IE = 'Internal error'
Flags = {}

# ----------------------------------------------------------------------
#                          global variables
# ----------------------------------------------------------------------

PROGNAME = None  # Program name without path
DirStack = [os.getcwd()]  # Directory stack

# ----------------------------------------------------------------------
#                        used by "--oldproto"
# ----------------------------------------------------------------------

segment = """
set(VERSION_MAJOR 0)
set(VERSION_MINOR 4)
set(VERSION_PATCH 17)
set(VERSION_TWEAK 1)
set(VERSION_EXTRA "" CACHE STRING "Stuff to append to version string")

# Change to false for releases
set(DEVELOPMENT_BUILD False)

set(VERSION_STRING "${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH}.${VERSION_TWEAK}")
if VERSION_EXTRA:
    set(VERSION_STRING ${VERSION_STRING}-${VERSION_EXTRA})
    elseif(DEVELOPMENT_BUILD)
    set(VERSION_STRING "${VERSION_STRING}-dev")
    endif()

    if CMAKE_BUILD_TYPE STREQUAL Debug:
"""

# ----------------------------------------------------------------------
#                     low-level utility routines
# ----------------------------------------------------------------------



def pushd(path):
    if not os.path.isdir(path):
        print("[pushd] ERROR: \"{}\" does not exist.".format(path))
        exit(1)
    os.chdir(path)
    DirStack.append(path)


def popd():
    if len(DirStack) < 2:
        print("[popd] ERROR: only the original path is on the stack")
        print("  (you popped more than you pushed).")
        exit(1)
    else:
        del DirStack[-1]
        os.chdir(DirStack[-1])


def execute(cmd, shell=True):
    """
    Iterate output of a command.

    See tokland's Dec 11, 2010 answer on <https://stackoverflow.com/
    questions/4417546/constantly-print-subprocess-output-while-
    process-is-running>
    """
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             universal_newlines=True,
                             shell=shell)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def RunCmd(cmdParts, shell=True):
    """
    :raises RuntimeError: The process returns a non-zero exit code.
    """
    # Popen can get confused when arguments contain quotes
    # (see <https://stackoverflow.com/questions/14928860/passing-double-
    # quote-shell-commands-in-python-to-subprocess-popen>) such as
    # in "-DCMAKE_CXX_FLAG="+XCFLAGS where XCFLAGS contains quotes.
    # child = subprocess.Popen(cmdParts, shell=shell,
    #                          stdout=subprocess.PIPE,
    #                          universal_newlines=True)
    # streamdata = child.communicate()[0]
    # rc = child.returncode
    # Instead of communicate, read the lines (See def execute)
    # if rc != 0:
    #     if exitOnFail:
    #         exit(rc)
    #     else:
    #         print("WARNING: {} failed".format(' '.join(cmdParts)))
    try:
        for line in execute(cmdParts, shell=shell):
            print(line, end="")
    except subprocess.CalledProcessError as ex:
        msg = ("The process '{}' failed with error code {}."
               "".format(" ".join(ex.cmd), ex.returncode))
        raise RuntimeError(msg)



def FixStr(s):
    if s is None:
        return ""
    s = re.sub("\s+", " ", s).strip()
    return s.strip()


def GetProgDir():
    """
    Set the PROGNAME global to this script's name and find the current
    working directory in terms of its real path (following symbolic
    links).

    This differs from mtcompile-program.pl in that this version gets
    the current directory, so that this script doesn't have to be in the
    linux-minetest-kit directory. However, due to that, the current
    directory must be linux-minetest-kit when running this function
    (when running this script).
    """
    global PROGNAME
    PROGNAME = os.path.basename(__file__)
    return os.path.realpath(os.getcwd())


def GetOptions(nonBoolNames=[], bareArgs=[]):
    """
    Convert command-line arguments to values in the global Flags dict.

    Keyword Arguments:
    nonBoolNames -- Specify which arguments can have values. All others
       are considered boolean, and will end the program if they contain
       '='.
    bareArgs -- allowed arguments without "--" at the beginning.

    Returns:
    false if arg has an equal sign and preceding part after "--" is not
      in nonBoolNames.
    """
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if (arg in bareArgs) or arg.startswith("--"):
            start = 0
            if arg.startswith("--"):
                start = 2
            signI = arg.find("=")
            name = arg[start:]
            val = True
            if signI > -1:
                name = arg[start:signI]
                if name not in nonBoolNames:
                    print("Only the following options can have values:"
                          " {}.".format(nonBoolNames))
                    return False
                val = arg[signI+1:]
            # if TitleCaseAndFlag:
            #     name = "Flag" + name.title()
            print("* {} = {}".format(name, val))
            Flags[name] = val
        else:
            print("The option is unknown: {}".format(arg))
            return False
    return True


USAGE_FMT = """
#{PROGNAME} {REVISION} - {PURPOSE}

#{USAGE_TEXT}
"""


def UsageText(msg=""):
    """
    "UsageText" prints usage text for the current program,  then termin-
    ates the program with exit status one.
    """
    # NOTE: PROGNAME is this script's name, NOT the engine name.
    THIS_USAGE = USAGE_FMT.format(PROGNAME=PROGNAME,
                                  REVISION=REVISION,
                                  PURPOSE=PURPOSE,
                                  USAGE_TEXT=USAGE_TEXT.format(
                                      PROGNAME=PROGNAME
                                  ))
    # USAGE_TEXT = evalSed('s@\s*\z@\n@s')
    print(THIS_USAGE)
    print("")
    print(msg)
    print("")
    print("")
    exit(1)


def main():

    # ------------------------------------------------------------------
    # Misc. variables.

    #my $cmd;                    # Shell command string
    #my $tmpStr;                    # Scratch

    # ------------------------------------------------------------------
    # Mode flags.

    # These may be modified, indirectly, by command-line switches.

    MAKEDEBUG = False
    PORTABLE = False
    TIDYUP = True
    MAKEPROD = False

    #---------------------------------------------------------------------
    # Command-line option flags.

    Flags["build"] = False
    Flags["client"] = False
    Flags["debug"] = False
    Flags["edgy"] = False
    Flags["gitpull"] = False
    Flags["gitreset"] = False
    Flags["help"] = False
    Flags["makeprod"] = False
    Flags["fakemt4"] = False
    Flags["noclean"] = False
    Flags["portable"] = False
    Flags["postgres"] = False
    Flags["redis"] = False
    Flags["safe"] = False
    Flags["server"] = False

    Flags["oldproto"] = True

    # ------------------------------------------------------------------
    # Initial setup.

    #select STDERR; $| = ONE;    # Force STDERR flush on write
    #select STDOUT; $| = ONE;    # Force STDOUT flush on write

    # ------------------------------------------------------------------
    # Get absolute path for script directory.

    # As a side effect, this function call initializes the global variable
    # "$PROGNAME". Note that this must be done before "UsageText" is call-
    # ed.

    THISDIR = GetProgDir()

    # ------------------------------------------------------------------
    # Parse command-line arguments.

    if not GetOptions(nonBoolNames=["MT_SRC"], bareArgs=["build"]):
        UsageText()
    mapLongArgs = {}
    mapLongArgs["edgytest"] = "edgy"
    mapLongArgs["notidy"] = "noclean"
    mapLongArgs["oldprotocol"] = "oldproto"
    mapLongArgs["postgresql"] = "postgres"
    mapLongArgs["usage"] = "help"
    for k, v in mapLongArgs.items():
        old_v = Flags.get(k)
        if old_v is not None:
            Flags[v] = old_v
            del Flags[k]


    # Handle usage-text exit
    if (not Flags["build"]) or Flags["help"]:
        if not Flags["build"]:
            msg = ("You did not specify build or --build (got:{})."
                   "".format(Flags))
        UsageText(msg=msg)

    # ------------------------------------------------------------------
    # Handle misc. flag issues.
    if Flags["edgy"]:
        Flags["fakemt4"] = True
    if Flags["edgy"] or Flags["fakemt4"]:
        Flags["oldproto"] = True
    if Flags["edgy"] and Flags["gitpull"]:
        customExit("Error: Can't use both --edgy and --gitpull")

    # ------------------------------------------------------------------
    # Confirm that script is running in the right place.

    if not os.path.isdir('mtsrc'):
        echo0("""
Error:  This script should be stored,  and executed,  in the directory
which contains the "mtsrc" directory.
""")
        exit(1)

    # ------------------------------------------------------------------
    # Additional directory paths.

    BALLDIR = os.path.join(THISDIR, "mtsrc", "newline")
    PRODDIR = os.path.join(THISDIR, "minetest")
    TOOLS_PREFIX = os.path.join(THISDIR, "toolstree")

    BINDIR = os.path.join(TOOLS_PREFIX, "bin")
    INCDIR = os.path.join(TOOLS_PREFIX, "include")
    LIBDIR = os.path.join(TOOLS_PREFIX, "lib")
    LIB64DIR = os.path.join(TOOLS_PREFIX, "lib64")

    # ------------------------------------------------------------------
    # Misc. setup.
    if not BINDIR in os.environ["PATH"]:
        os.environ["PATH"] = BINDIR + os.pathsep + os.environ["PATH"]
    which("g++")
    # ------------------------------------------------------------------
    # Handle some of the option flags.
    if Flags["debug"]:
        MAKEDEBUG = True
    if Flags["makeprod"]:
        MAKEPROD = True
    if Flags["noclean"]:
        TIDYUP = False

    if MAKEPROD:
        MAKEDEBUG = False
        PORTABLE = True
        TIDYUP = True

    # ------------------------------------------------------------------
    # Handle "--gitreset".

    if Flags["gitreset"]:
        if Flags["gitpull"]:
            customExit("Error: Can't use both --gitreset and --gitpull\n")

        if Flags["safe"] and os.path.isdir('minetest'):
            print("""
Error:  "minetest" directory exists and  "--gitreset" needs  to delete
it.  But can't because "--safe" was specified. If you wish to proceed,
move or rename the directory.
""")
            exit(1);

        TIDYUP = False
        print("""
* --gitreset specified and --safe not specified
* Removing any existing "minetest" directory
""")
        shutil.rmtree("minetest")
        print("* Attempting a git clone...")
        cmdParts = ["git", "clone", GITURL, "minetest"]
        print("  " + " ".join(cmdParts))
        RunCmd(cmdParts);

    # ------------------------------------------------------------------
    # Handle "--gitpull".

    if Flags["gitpull"]:
        if Flags["gitreset"]:
            customExit("Error: Can't use both --gitreset and --gitpull\n")

        TIDYUP = False

        if os.path.isdir('minetest'):
            if not os.path.isdir('minetest/.git'):
                print("""
Error: "--gitpull" specified  and I see a  "minetest" directory but no
"minetest/.git" directory.
If you'd like to use "--gitpull",  delete, rename,  or move the "mine-
test" directory.

Or  you can use  "--gitreset" instead.  This will delete the directory
automatically.
""")
                exit(1)

        if not os.path.isdir('minetest'):
            print("""
* "--gitpull" specified but I don't see a "minetest" directory
* Attempting a git clone
""")
            cmdParts = ["git", "clone", GITURL, "minetest"]
            print("cmd " + " ".join(cmdParts))
            RunCmd(cmdParts)
        else:
            if not os.path.isdir(os.path.join("minetest", ".git")):
                customExit(IE + "#250458")

            print("""
* --gitpull specified and I see "minetest/.git"
* Attempting a git pull
""")
            pushd('minetest');
            cmdParts = ["git", "pull"]
            RunCmd(cmdParts, exit_on_fail=false)
            popd();

    # ------------------------------------------------------------------
    # Handle "--client" and "--server".

    client_line = "-DBUILD_CLIENT=1"
    server_line = "-DBUILD_SERVER=1"

    if Flags["client"] and not Flags["server"]:
        client_line = "-DBUILD_CLIENT=1"
        server_line = "-DBUILD_SERVER=0"

    if not Flags["client"] and Flags["server"]:
        client_line = "-DBUILD_CLIENT=0"
        server_line = "-DBUILD_SERVER=1"

    # ------------------------------------------------------------------
    # Status messages.

    NUBDF = "not used by default in this version"

    print("""
* leveldb (by default)
* sqlite3 (by default)
""")

    # ------------------------------------------------------------------
    # Handle "--postgres".

    postgres_line = "-DENABLE_POSTGRESQL=0"

    if Flags["postgres"]:
        print("* postgres (due to --postgresql)")
        postgres_line = "-DENABLE_POSTGRESQL=1"
    else:
        print("(skipping postgresql --"+NUBDF)

    # ------------------------------------------------------------------
    # Handle "--redis".

    redis_line = "-DENABLE_REDIS=0"

    if Flags["redis"]:
        print("* redis (due to --redis)")
        redis_line = "-DENABLE_REDIS=1"
    else:
        print("(skipping redis --"+NUBDF)

    # ------------------------------------------------------------------
    # "--portable" requires the bootstrapped "gcc".

    if PORTABLE and not os.path.isfile(os.path.join(BINDIR, "gcc")):
        print("""
Error: For Linux portable mode (--portable), you need to build the in-
cluded  "gcc" 8 compiler.  To do so, run "mtcompile-libraries.sh" with
gcc-bootstrap mode enabled.
""")
        exit(1)

    # ------------------------------------------------------------------
    # Identify "gcc" major release number.

    #my ($GCCVER) = $tmpStr =~ m@\ngcc.* (\d+)*\.\d+\.@
    tmpStr = subprocess.check_output(["gcc", "--version"]).decode()
    tmpParts = re.findall("gcc.* (\d+)*\.\d+\.", tmpStr)
    GCCVER = None
    if len(tmpParts) > 0:
        GCCVER = tmpParts[0]
    else:
        customExit("Error: Not able to identify gcc release")

    # ------------------------------------------------------------------
    # Replace existing "minetest" directory.

    RESETDIR = (not os.path.isdir(PRODDIR)) or TIDYUP

    if RESETDIR:
        if Flags["safe"] and os.path.isdir('minetest'):
            print("""

Error:  We  need  to delete  the  existing "minetest"  directory,  but
"--safe" is  specified.  If you'd like to preserve the directory, move
or rename it. Otherwise, drop the "--safe" switch.
""")
            exit(1)
        # PRODDIR is THISDIR/minetest
        print("* cleaning " + os.getcwd())
        for sub in os.listdir(THISDIR):
            sub_path = os.path.join(THISDIR, sub)
            if sub.startswith("."):
                continue
            if os.path.isfile(sub_path):
                continue
            if sub_path == PRODDIR:
                # ^ sub_path must be generated the same way as
                #   PRODDIR (from THISDIR) for this to work (to
                #   remove the linux-minetest-kit/minetest directory).
                print("* removing old \"{}\"".format(sub_path))
                shutil.rmtree(sub_path)
            elif sub.startswith("minetest-newline"):
                shutil.rmtree(sub_path)
        print("* extracting in " + os.getcwd())
        mtNewLine = "minetest-newline"
        if Flags["edgy"]:
            mtNewLine = "minetest-newline"
        if Flags.get("MT_SRC") is not None:
            if not os.path.isdir(Flags["MT_SRC"]):
                customExit("{} does not exist.".format(Flags["MT_SRC"]))
            print("* using custom MT_SRC \"{}\" (copying to \"{}\")"
                  "".format(Flags["MT_SRC"], PRODDIR))
            shutil.copytree(Flags["MT_SRC"], PRODDIR,
                            copy_function=shutil.copy2)
        else:
            tarPath = os.path.join(BALLDIR, mtNewLine + ".tar.bz2")
            tar = tarfile.open(tarPath)
            tar.extractall(path=THISDIR)
            tar.close()
        for sub in os.listdir(THISDIR):
            sub_path = os.path.join(THISDIR, sub)
            if sub.startswith(mtNewLine):
                print("* using {} as minetest".format(sub_path))
                shutil.move(sub_path, PRODDIR)
                break

    os.chdir(PRODDIR)
    # or die "$IE #505850\n";

    # ------------------------------------------------------------------
    # Sanity check.

    if not os.path.isfile('CMakeLists.txt'):
        print("""
Error: You're trying to build using a "minetest" directory that's mis-
sing a "CMakeLists.txt".  The directory was probably tidied up after a
previous build.

To  rebuild, delete, move, or  rename the "minetest" directory and try
again.
""")
        exit(1)

    # ------------------------------------------------------------------
    # Delete leftover temporary files.
    tmpFileNames = [
        "C.includecache",
        "CXX.includecache",
        "CMakeCache.txt",
        "CMakeCCompiler.cmake",
        "CMakeCXXCompiler.cmake",
        "CMakeDirectoryInformation.cmake",
        "CMakeRuleHashes.txt",
        "CPackConfig.cmake",
        "CPackSourceConfig.cmake",
        "DependInfo.cmake",
        "Makefile2",
        "TargetDirectories.txt",
        "build.make",
        "depend.make",
        "depend.internal",
        "cmake_config.h",
        "cmake_install.cmake",
        "flags.make",
        "link.txt",
        "progress.make",
        "relink.txt"
    ]
    tmpFilePaths = [
        "textures/base/pack/menu_header_old.png"
    ]
    tmpExtensions = [
        ".a",
        ".log",
        ".o"
    ]
    androidSub = os.path.join("build", "android")
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            subPath = os.path.join(root, name)
            if name in tmpFileNames:
                os.remove(subPath)
            elif (name == "Makefile") and (androidSub in subPath):
                os.remove(subPath)
            elif endsWithAny(subPath, tmpFilePaths + tmpExtensions):
                os.remove(subPath)

    # ------------------------------------------------------------------
    # Define paths for some ".a" library files.

    IRRLICHT_LIBRARY = os.path.join(LIBDIR, "libIrrlicht.a")
    LEVELDB_LIBRARY = os.path.join(LIBDIR, "libleveldb.a")
    LUA_LIBRARY = os.path.join(LIBDIR, "libluajit-5.1.a")
    SQLITE3_LIBRARY = os.path.join(LIBDIR, "libsqlite3.a")

    # ------------------------------------------------------------------
    # Set "$XCFLAGS" (extra compiler flags).

    XCFLAGS = "-O2 -I" + INCDIR
    if MAKEDEBUG:
        XCFLAGS += " -g"
    if not PORTABLE:
        XCFLAGS = "-march=native " + XCFLAGS
    XCFLAGS += " -Wl,-L" + LIBDIR + " -Wl,-R" + LIBDIR
    if os.path.isdir(LIB64DIR):
        XCFLAGS += " -Wl,-L" + LIB64DIR + " -Wl,-R" + LIB64DIR

    print("XCFLAGS="+XCFLAGS)

    # ------------------------------------------------------------------
    # Get pathnames for "gcc" and "g++" compilers.

    WHICH_GCC = which("gcc")
    WHICH_GPP = which("g++")
    if not isExecutableFile(WHICH_GCC):
        if WHICH_GCC is not None:
            print("gcc: {}".format(WHICH_GCC))
        customExit("gcc is not present or not executable in {}."
                   "".format(os.environ["PATH"]))
    if not isExecutableFile(WHICH_GPP):
        if WHICH_GPP is not None:
            print("g++: {}".format(WHICH_GPP))
        customExit("g++ is not present or not executable in {}."
                   "".format(os.environ["PATH"]))

    # ------------------------------------------------------------------
    # Handle another "--edgy step".

    if Flags["edgy"]:
        CM = 'src/defaultsettings.cpp'
        # TODO: finish converting this from perl
        print("edgy changing {} is not yet implemented."
              "".format(CM))
        data = None
        try:
            with open(CM, 'r') as IFD:
                pass
                #SS = $/
                #undef $/;
                #data = <IFD>
                #data = ""unless defined  + data
                #/ = SS
                # - secure.enable_security to false by default
        except FileNotFoundError:
            customExit("Internal error 0766")
        # try:
        #     with open(CM) as OFD:
        #         OFD.write(data)
        # except FileNotFoundError:
        #     customExit("Internal error 0777")
    # ------------------------------------------------------------------
    # Handle "--fakemt4".

    if Flags["fakemt4"]:

        CM = 'CMakeLists.txt'
        print("fakemt4 changing {} is not yet implemented."
              "".format(CM))
        # TODO: handle fakemt4
        # data = None
        # with open(CM, 'r') as IFD:  # or die "Internal error 0789\n";
        #     SS = $/
        #     undef $/;
        #     data = <IFD>
        #     data = ""unless defined  + data
        #     / = SS

        # pat = << 'END'
        # set\(VERSION_MAJOR \d+\)
        # .*?
        # if \(CMAKE_BUILD_TYPE STREQUAL Debug\)
        # END
        # pat = evalSed('s@\s+\z@@s')
        # pat = evalSed('s@\s*\n\s*@@gs')
        # TODO: Use the segment variable here
        # data = evalSed('s@\s*$pat\s*@\n$segment@is')
        # with open(CM, 'w') as OFD:  # or die "Internal error 0806\n";
        #     OFD.write(data)
        #     OFD.close()  # or die "Internal error 0808\n";

    # ------------------------------------------------------------------
    # Handle "--oldproto".

    if Flags["oldproto"]:
        CM = 'src/network/networkprotocol.h'
        print("oldproto changing {} is not yet implemented."
              "".format(CM))
        # TODO: change protocol in CM:
        # data = None
        # with open(CM, 'r') as IFD:  #or die "Internal error 0714\n";
        #     SS = $/
        #     undef $/;
        #     data = <IFD>
        #     data = ""unless defined  + data
        #     / = SS
        #     data = evalSed('s@(#define\s+LATEST_PROTOCOL_VERSION)\s+3\d\b@$1 32@')
        # with open("CM", 'w') as OFD:  # or  die "Internal error 0715\n";
        #     OFD.write(data)

    # ------------------------------------------------------------------
    # Run "cmake".
    cmdParts = ["cmake"]
    cmdParts.append("-DCMAKE_BUILD_TYPE=release")
    cmdParts.append("-DCMAKE_C_COMPILER="+WHICH_GCC)
    cmdParts.append("-DCMAKE_CXX_COMPILER="+WHICH_GPP)
    cmdParts.append("-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=1")
    cmdParts.append("-DCMAKE_SKIP_INSTALL_RPATH=0")
    cmdParts.append("-DCMAKE_SKIP_RPATH=0")
    cmdParts.append(client_line)
    cmdParts.append(server_line)
    cmdParts.append("-DENABLE_LEVELDB=1")
    cmdParts.append(postgres_line)
    cmdParts.append(redis_line)
    cmdParts.append("-DENABLE_SOUND=1")
    cmdParts.append("-DENABLE_SPATIAL=0")
    # ^ TODO: WHY 0 in linux-minetest-kit?
    cmdParts.append("-DENABLE_SYSTEM_JSONCPP=0")
    cmdParts.append("-DRUN_IN_PLACE=1")
    cmdParts.append("-DIRRLICHT_INCLUDE_DIR={}/irrlicht".format(INCDIR))
    cmdParts.append("-DIRRLICHT_LIBRARY="+IRRLICHT_LIBRARY)
    cmdParts.append("-DLEVELDB_INCLUDE_DIR={}/leveldb".format(INCDIR))
    cmdParts.append("-DLEVELDB_LIBRARY="+LEVELDB_LIBRARY)
    cmdParts.append("-DLUA_INCLUDE_DIR={}/luajit-2.1".format(INCDIR))
    cmdParts.append("-DLUA_LIBRARY="+LUA_LIBRARY)
    cmdParts.append("-DSQLITE3_INCLUDE_DIR="+INCDIR)
    cmdParts.append("-DSQLITE3_LIBRARY="+SQLITE3_LIBRARY)
    cmdParts.append("-DCMAKE_C_FLAGS=\"{}\"".format(XCFLAGS))
    cmdParts.append("-DCMAKE_CXX_FLAGS=\"{}\"".format(XCFLAGS))
    cmdParts.append("-DCMAKE_C_FLAGS_RELEASE=\"{}\"".format(XCFLAGS))
    cmdParts.append("-DCMAKE_CXX_FLAGS_RELEASE=\"{}\"".format(XCFLAGS))
    cmdParts.append(".")
    print("")
    print("")
    print("* running cmake in {}:".format(os.getcwd()))
    print(" ".join(cmdParts))
    print("")
    print("")
    # RunCmd(cmdParts, shell=True)
    # ^ fails due to excessive automatic quotes around params by python
    # RunCmd(cmdParts[:1] + [" ".join(cmdParts[1:])], shell=False)
    # ^ must be false to avoid inserting quotes automatically
    # ^ still has problems
    os.system(" ".join(cmdParts))

    # TODO: use some absolute pathnames as the Perl version does
    # ------------------------------------------------------------------
    # Replace some "-l..." switches with absolute pathnames.

    replacements = {
        "-lIrrlicht": IRRLICHT_LIBRARY,
        "-lleveldb": LEVELDB_LIBRARY,
        "-lluajit-5.1": LUA_LIBRARY,
        "-lsqlite3": SQLITE3_LIBRARY,
    }
    for root, dirs, files in os.walk(PRODDIR):
        for name in files:
            subPath = os.path.join(root, name)
            if name == "link.txt":
                streamEdit(subPath, replacements)

    # ------------------------------------------------------------------
    # Build the program.
    NUMJOBS = 3
    print("* running make in {}...".format(os.getcwd()))
    RunCmd(["make", "clean"])
    RunCmd("make", "-j{}".format(NUMJOBS))
    serverlistDir = os.path.join(PRODDIR, "client", "serverlist")
    os.makedirs(serverlistDir, exist_ok=True)
    os.makedirs("games", exist_ok=True)
    os.makedirs("worlds", exist_ok=True)
    dstAKPath = os.path.join(PRODDIR, "arrowkeys.txt")
    shutil.copy(os.path.join(BALLDIR, "arrowkeys.txt"), dstAKPath)

    # ------------------------------------------------------------------
    # Add preloaded cache.
    thisCache = os.path.join(PRODDIR, "cache")
    if os.path.isdir(thisCache):
        shutil.rmtree(thisCache)
    tarPath = os.path.join(BALLDIR, "cachemedia.tar.bz2")
    tar = tarfile.open(tarPath)
    tar.extractall(path=PRODDIR)
    tar.close()

    # ------------------------------------------------------------------
    # Add "_games".

    pushd('games');
    cmd = ""
    gameNames = ["minimal", "amhi_game"]
    if not Flags["edgy"]:
        # TODO: What does Flags["edgy"] do here? Does it leave the old
        # Bucket_Game and do nothing else differently?
        # See mtcompile-program.pl
        gameNames.append("Bucket_Game")
    # gamePaths = [os.path.join(PRODDIR, gName) for gName in gameNames]
    # print("* purging gamepaths: {}".format(gamePaths))
    for gameName in gameNames:
        gamePath = os.path.join(PRODDIR, gameName)
        if os.path.isdir(gamePath):
            print("* replacing {}".format(gamePath))
            shutil.rmtree(gamePath)
        else:
            print("* adding {}".format(gamePath))
        zipPath = os.path.join(BALLDIR, gameName + ".zip")
        if os.path.isfile(zipPath):
            zf = ZipFile(zipPath)
            zf.extractall(gamePath)  # pwd means password in this case
    popd();

    # ------------------------------------------------------------------
    # Add worlds.

    # pushd('worlds');
    WORLDS_PATH = os.path.join(PRODDIR, "worlds")
    for worldName in ["Bucket_City", "Wonder_World"]:
        worldPath = os.path.join(WORLDS_PATH, worldName)
        tarPath = os.path.join(BALLDIR, worldName + ".taz.bz2")
        if os.path.isdir(worldPath):
            if os.path.isfile(tarPath):
                # Only remove the old one if there is a new one.
                shutil.rmtree(worldPath)
        if Flags["edgy"]:
            continue
        if os.path.isfile(tarPath):
            tar = tarfile.open(tarPath)
            tar.extractall(path=WORLDS_PATH)
            tar.close()
        else:
            print("WARNING: \"{}\" is missing.".format(tarPath))
    # popd();

    # ------------------------------------------------------------------
    # Strip the executable(s).

    if not MAKEDEBUG:
        prodBinDir = os.path.join(PRODDIR, "bin")
        for sub in os.listdir(prodBinDir):
            if sub.startswith("."):
                continue
            sub_path = os.path.join(prodBinDir, sub)
            if not os.path.isfile(sub_path):
                continue
            if sub.startswith("minetest"):
                try:
                    RunCmd(["strip", sub_path])
                except RuntimeError:
                    print("strip (optimizing the executable size)"
                          " failed for {}".format(sub_path))

    # ------------------------------------------------------------------
    # Additional cleanup.

    if TIDYUP:
        tmpNames = ["MakeFile", "build", "debug.txt", "lib", "src"]
        tmpEndsWith = ["cmake"]
        tmpStartsWith = ["CMake"]
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                subPath = os.path.join(root, name)
                if name in tmpNames:
                    if os.path.isfile(subPath):
                        os.remove(subPath)
                    else:
                        shutil.rmtree(subPath)
                elif endsWithAny(subPath, tmpEndsWith):
                    if os.path.isfile(subPath):
                        os.remove(subPath)
                    else:
                        shutil.rmtree(subPath)
                elif startsWithAny(subPath, tmpStartsWith):
                    if os.path.isfile(subPath):
                        os.remove(subPath)
                    else:
                        shutil.rmtree(subPath)

        keepWith = [" ", ".dummy"]

        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                subPath = os.path.join(root, name)
                if containsAny(name, keepWith):
                    continue
                if not name.startswith("."):
                    continue
                if name[1:2].upper() != name[1:2]:
                    # .[a-z]\*
                    os.remove(subPath)

        # --------------------------------------------------------------
        # Finish required "--portable" operations.

    if PORTABLE:
        M = os.uname().machine
        BITS = 32 if (M == "i686") else 64
        solibPath = os.path.join(PRODDIR, "solib")
        if os.path.isdir(solibPath):
            shutil.rmtree(solibPath)

        tarPath = os.path.join(BALLDIR, "solib{}.tar.bz2".format(BITS))
        if os.path.isfile(tarPath):
            tar = tarfile.open(tarPath)
            tar.extractall(path=PRODDIR)
            if not os.path.isdir(solibPath):
                customExit("ERROR: extracting \"{}\" did not result in"
                           " \"{}\"".format(tarPath, solibPath))
            tar.close()
        else:
            customExit("ERROR: \"{}\" is missing.".format(tarPath))
        # pushd('bin');
        for prog in ["minetest", "minetestserver"]:
            srcWrapPath = os.path.join(BALLDIR, prog+".wrapper")
            progWrapPath = os.path.join(PRODDIR, "bin", prog)
            progBinPath = os.path.join(PRODDIR, "bin", prog+".bin")
            if os.path.isfile(progBinPath):
                os.remove(progBinPath)
            shutil.move(progWrapPath, progBinPath)
            # copy2 mimics `cp -p` (preserve attributes)
            shutil.copy2(srcWrapPath, progWrapPath)
            os.chmod(progWrapPath, 0o755)

        # popd()
        # --------------------------------------------------------------

        if MAKEPROD:
            # os.chdir(THISDIR)  # or die "$IE #505833\n";
            ZIPDIR = "minetest-linux" + BITS
            ZIPDIR_PATH = os.path.join(THISDIR, ZIPDIR)
            ZIPFILE = ZIPDIR + ".zip"
            ZIPFILE_PATH = os.path.join(THISDIR, ZIPFILE)
            if os.path.isdir(ZIPDIR_PATH):
                shutil.rmtree(ZIPDIR_PATH)
            if os.path.isfile(ZIPFILE_PATH):
                os.remove(ZIPFILE_PATH)
            shutil.move(PRODDIR_PATH, ZIPDIR_PATH)
            zf = zipfile.ZipFile(ZIPFILE_PATH, 'w',
                                 zipfile.ZIP_DEFLATED, compresslevel=9)
            zipdir(ZIP_PATH, zf)
            zf.close()
            # originally zip -ro9q
            # r: recurse into subdirectories (done by zipdir)
            # o: make zipfile as old as latest entry (handled below)
            # 9: compress better
            # q: quiet
            latestStamp = None
            for root, dirs, files in os.walk(ZIPDIR_PATH):
                for name in files:
                    subPath = os.path.join(root, name)
                    stamp = os.stat("ideas.md").st_mtime
                    if (latestStamp is None) or (stamp > latestStamp):
                        latestStamp = stamp
            st = os.stat(ZIPFILE_PATH)
            # See <https://www.gubatron.com/blog/2007/05/29/how-to-
            # update-file-timestamps-in-python/>
            atime = st[stat.ST_ATIME]
            mtime = st[stat.ST_MTIME]
            shutil.rmtree(ZIPDIR_PATH)
            os.utime(ZIPFILE_PATH, (atime, latestStamp))

    print("Done\n")
    # end main
    return 0


if __name__ == "__main__":
    sys.exit(main())
