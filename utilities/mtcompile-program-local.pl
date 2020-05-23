#!/usr/bin/env perl

#---------------------------------------------------------------------
#                          file information
#---------------------------------------------------------------------

# Name:     mtcompile-program.pl
# Purpose:  Linux Minetest build script
# License:  Creative Commons Attribution-NonCommercial-ShareAlike 4.0.
#           Attribution: OldCoder (Robert Kiraly).
# Revision: See program parameters section

#---------------------------------------------------------------------
#                           important note
#---------------------------------------------------------------------

# This software is provided on an  AS IS basis with ABSOLUTELY NO WAR-
# RANTY.  The  entire risk as to the  quality and  performance of  the
# software is with you.  Should the software prove defective,  you as-
# sume the cost of all necessary  servicing, repair or correction.  In
# no event will any of the developers,  or any other party, be  liable
# to anyone for damages arising out of use of the software, or inabil-
# ity to use the software.

#---------------------------------------------------------------------
#                              overview
#---------------------------------------------------------------------

                                # Label must be single-quoted here
my $USAGE_TEXT = << 'END_OF_USAGE_TEXT';
Usage: $PROGNAME --options --build

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
                # use the existing source tree,  if there is one,  and
                # doesn't deleted "build" files afterward.

                # The "--git*" and "--debug" switches  imply this swi-
                # tch.
                # Aliases: --notidy

--server        # Build server & not client unless --client also
--client        # Build client & not server unless --server also
                # Default: If neither  is set, both are implied
                #          If just one is set, the other is off

--postgresql    # Enable PostgreSQL (requires installed copy)
                # Aliases: --postgres

--redis         # Enable Redis      (requires installed copy)

--debug         # Build a "debug" version of the program  suitable for
                # use with "gdb".

--makeprod      # Build a  portable  production release  (ZIP file) of
                # Linux Minetest.  This is only needed  by  people who
                # wish to redistribute the program. The switch implies
                # --portable.  It isn't  compatible with  --noclean or
                # --debug.

--portable      # Build a portable version.  If this  isn't specified,
                # the copy of  Minetest built is tailored  to your ma-
                # chine and may only run on an identical machine (same
                # hardware,  distro, and distro release).  At the same
                # time,  non-portable versions may be slightly faster.

--gitreset      # Delete  any  existing source  tree and  try  to do a
                # fresh "git clone".

--gitpull       # Try  to  update the current  source tree using  "git
                # pull".  If there is no source  tree  or  it's not  a
                # "git" tree, this switch is the same as "--gitreset".

                # The "git" switches  require both the  "git" software
                # package and Internet access.

--safe          # Don't delete existing source trees automatically.

--edgy          # Build  EdgyTest instead of  Final Minetest.  Implies
                # "--fakemt4".

--fakemt4       # Pretend to be MT 4. Implies "--oldproto".

--oldproto      # Limit network protocol used to level 32. For the mo-
                # ment,  this is the default mode and  there is no way
                # to disable it.

--help          # Display usage text and exit.
                # Aliases: --usage

For full documentation, see "linux-minetest-kit.txt".
END_OF_USAGE_TEXT

#---------------------------------------------------------------------
#                            module setup
#---------------------------------------------------------------------

require 5.16.1    ;
use strict        ;
use Carp          ;
use warnings      ;
use Cwd;          ;
use Getopt::Long  ;
                                # Trap warnings
$SIG{__WARN__} = sub { die @_; };

#---------------------------------------------------------------------
#                           basic constants
#---------------------------------------------------------------------

use constant ZERO  => 0;        # Zero
use constant ONE   => 1;        # One
use constant TWO   => 2;        # Two

use constant FALSE => 0;        # Boolean FALSE
use constant TRUE  => 1;        # Boolean TRUE

#---------------------------------------------------------------------
#                         program parameters
#---------------------------------------------------------------------

my $PURPOSE  = 'Linux Minetest build script';
my $REVISION = '191130';
my $USE_LESS = TRUE;            # Flag: Use "less" for usage text

my $GITURL   = 'http://git.minetest.org/minetest/minetest.git';
my $IE       = 'Internal error';

#---------------------------------------------------------------------
#                          global variables
#---------------------------------------------------------------------

my $PROGNAME;                   # Program name without path
my @DirStack = ();              # Directory stack

#---------------------------------------------------------------------
#                        used by "--oldproto"
#---------------------------------------------------------------------

my $segment = << 'END';
set(VERSION_MAJOR 0)
set(VERSION_MINOR 4)
set(VERSION_PATCH 17)
set(VERSION_TWEAK 1)
set(VERSION_EXTRA "" CACHE STRING "Stuff to append to version string")

# Change to false for releases
set(DEVELOPMENT_BUILD FALSE)

set(VERSION_STRING "${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH}.${VERSION_TWEAK}")
if(VERSION_EXTRA)
	set(VERSION_STRING ${VERSION_STRING}-${VERSION_EXTRA})
elseif(DEVELOPMENT_BUILD)
	set(VERSION_STRING "${VERSION_STRING}-dev")
endif()

if (CMAKE_BUILD_TYPE STREQUAL Debug)
END

#---------------------------------------------------------------------
#                     low-level utility routines
#---------------------------------------------------------------------

sub pushd
{
    my ($dir) = @_;             # Relative or absolute directory path
    die unless -d $dir;
    push (@DirStack, getcwd());
    die unless chdir ($dir);
    undef;
}

#---------------------------------------------------------------------

sub popd
{
    my $dir = pop (@DirStack);
    die unless defined $dir;
    die unless -d $dir;
    die unless chdir ($dir);
    undef;
}

#---------------------------------------------------------------------

sub RunCmd
{
    my ($cmd) = @_;
    my $status = system $cmd;
       $status = ($status >> 8) & 0x0F;
    exit $status if $status;
    undef;
}

#---------------------------------------------------------------------

sub FixStr
{
    my ($str) = @_;
    $str = "" unless defined $str;
    $str =~ s@\s+@ @gs;
    $str =~ s@\s+\z@@s;
    $str =~ s@^\s+@@s;
    $str;
}

#---------------------------------------------------------------------

sub GetProgDir
{
    $PROGNAME    = $0;
    my $ProgTemp = $0;

    $PROGNAME =~ s@^.*/@@;

    while (defined (my $r = readlink ($ProgTemp)))
    {
        while ($r =~ s@^\./@@) {}
        die "$IE #203494\n" if $r =~ m@^\.\./@;
        $ProgTemp = $r;
    }

    while ($ProgTemp =~ s@^\./@@) {}

    if ($ProgTemp =~ m@/@)
    {
        die "$IE #595033: $ProgTemp\n" unless $ProgTemp =~ m@^/@;

        die "$IE #024839: $ProgTemp\n"
            unless $ProgTemp =~ s@/[^/]+\z@@;
    }
    else
    {
        $ProgTemp = ".";
    }

    my $cwd     = getcwd();
    chdir ($ProgTemp) || die;
    my $ProgDir = getcwd();
    chdir ($cwd) || die "$IE #048837\n";
    $ProgDir;
}

#---------------------------------------------------------------------
#                         usage-text routine
#---------------------------------------------------------------------

# "UsageText" prints usage text for the current program,  then termin-
# ates the program with exit status one.

#---------------------------------------------------------------------

sub UsageText
{
    $USAGE_TEXT =~ s@^\s+@@s;
    $USAGE_TEXT =~ s@\$PROGNAME@$PROGNAME@g;

    $USAGE_TEXT = << "END";     # "END" must be double-quoted here
$PROGNAME $REVISION - $PURPOSE

$USAGE_TEXT
END
    $USAGE_TEXT =~ s@\s*\z@\n@s;

    if ($USE_LESS && (-t STDOUT) && open (OFD, "|/usr/bin/less"))
    {
                                # "END" must be double-quoted here
        $USAGE_TEXT = << "END";
To exit this "help" text, press "q" or "Q".  To scroll up or down, use
PGUP, PGDN, or the arrow keys.

$USAGE_TEXT
END
        print OFD $USAGE_TEXT;
        close OFD;
    }
    else
    {
        print "\n", $USAGE_TEXT, "\n";
    }

    exit ONE;
}

#---------------------------------------------------------------------
#                            main routine
#---------------------------------------------------------------------

sub Main
{

#---------------------------------------------------------------------
# Misc. variables.

    my $cmd;                    # Shell command string
    my $str;                    # Scratch

#---------------------------------------------------------------------
# Mode flags.

# These may be modified, indirectly, by command-line switches.

    my $MAKEDEBUG = FALSE ;
    my $PORTABLE  = FALSE ;
    my $TIDYUP    = TRUE  ;
    my $MAKEPROD  = FALSE ;

#---------------------------------------------------------------------
# Command-line option flags.

    my $FlagBuild    = FALSE ;
    my $FlagClient   = FALSE ;
    my $FlagDebug    = FALSE ;
    my $FlagEdgy     = FALSE ;
    my $FlagGitPull  = FALSE ;
    my $FlagGitReset = FALSE ;
    my $FlagHelp     = FALSE ;
    my $FlagMakeProd = FALSE ;
    my $FlagFakeMT4  = FALSE ;
    my $FlagNoClean  = FALSE ;
    my $FlagPortable = FALSE ;
    my $FlagPostgres = FALSE ;
    my $FlagRedis    = FALSE ;
    my $FlagSafe     = FALSE ;
    my $FlagServer   = FALSE ;

    my $FlagOldProto = TRUE  ;

#---------------------------------------------------------------------
# Initial setup.

    select STDERR; $| = ONE;    # Force STDERR flush on write
    select STDOUT; $| = ONE;    # Force STDOUT flush on write

#---------------------------------------------------------------------
# Get absolute path for script directory.

# As a side effect, this function call initializes the global variable
# "$PROGNAME". Note that this must be done before "UsageText" is call-
# ed.

    my $THISDIR = &GetProgDir();

#---------------------------------------------------------------------
# Parse command-line arguments.

    for (@ARGV) { s@^build\z@--build@; }
    Getopt::Long::Configure ("bundling");

    exit ONE unless GetOptions
    (
        "build"         => \$FlagBuild      ,
        "client"        => \$FlagClient     ,
        "debug"         => \$FlagDebug      ,
        "edgy"          => \$FlagEdgy       ,
        "edgytest"      => \$FlagEdgy       ,
        "fakemt4"       => \$FlagFakeMT4    ,
        "gitpull"       => \$FlagGitPull    ,
        "gitreset"      => \$FlagGitReset   ,
        "help"          => \$FlagHelp       ,
        "makeprod"      => \$FlagMakeProd   ,
        "noclean"       => \$FlagNoClean    ,
        "notidy"        => \$FlagNoClean    ,
        "oldproto"      => \$FlagOldProto   ,
        "oldprotocol"   => \$FlagOldProto   ,
        "portable"      => \$FlagPortable   ,
        "postgres"      => \$FlagPostgres   ,
        "postgresql"    => \$FlagPostgres   ,
        "redis"         => \$FlagRedis      ,
        "safe"          => \$FlagSafe       ,
        "server"        => \$FlagServer     ,
        "usage"         => \$FlagHelp       ,
    );
                                # Handle usage-text exit
    &UsageText() if !$FlagBuild || $FlagHelp || scalar (@ARGV);

#---------------------------------------------------------------------
# Handle misc. flag issues.

    $FlagFakeMT4  = TRUE if $FlagEdgy;
    $FlagOldProto = TRUE if $FlagEdgy || $FlagFakeMT4;

    die "Error: Can't use both --edgy and --gitpull\n"
        if $FlagEdgy && $FlagGitPull;

#---------------------------------------------------------------------
# Confirm that script is running in the right place.

    if (!-d 'mtsrc')
    {
        print STDERR << 'END';
Error:  This script should be stored,  and executed,  in the directory
which contains the "mtsrc" directory.
END
        exit ONE;
    }

#---------------------------------------------------------------------
# Additional directory paths.

    my $BALLDIR      = "$THISDIR/mtsrc/newline" ;
    my $PRODDIR      = "$THISDIR/minetest"      ;
    my $TOOLS_PREFIX = "$THISDIR/toolstree"     ;

    my $BINDIR       = "$TOOLS_PREFIX/bin"      ;
    my $INCDIR       = "$TOOLS_PREFIX/include"  ;
    my $LIBDIR       = "$TOOLS_PREFIX/lib"      ;
    my $LIB64DIR     = "$TOOLS_PREFIX/lib64"    ;

#---------------------------------------------------------------------
# Misc. setup.

    $ENV {'PATH'} = "$BINDIR:" . $ENV {'PATH'};
    system "which g++";

#---------------------------------------------------------------------
# Handle some of the option flags.

    $MAKEDEBUG = TRUE  if $FlagDebug    ;
    $MAKEPROD  = TRUE  if $FlagMakeProd ;
    $TIDYUP    = FALSE if $FlagNoClean  ;

    if ($MAKEPROD)
    {
        $MAKEDEBUG = FALSE ;
        $PORTABLE  = TRUE  ;
        $TIDYUP    = TRUE  ;
    }

#---------------------------------------------------------------------
# Handle "--gitreset".

    if ($FlagGitReset)
    {
        die "Error: Can't use both --gitreset and --gitpull\n"
            if $FlagGitPull;

        if ($FlagSafe && (-d 'minetest'))
        {
            print << 'END';

Error:  "minetest" directory exists and  "--gitreset" needs  to delete
it.  But can't because "--safe" was specified. If you wish to proceed,
move or rename the directory.
END
            exit ONE;
        }

        $TIDYUP = FALSE;

        print << 'END';
* --gitreset specified and --safe not specified
* Removing any existing "minetest" directory
END
        $cmd = "rm -fr minetest";
        &RunCmd ($cmd);

        print "* Attempting a git clone\n";
        $cmd = "git clone $GITURL minetest";
        print "  $cmd\n";
        &RunCmd ($cmd);
    }

#---------------------------------------------------------------------
# Handle "--gitpull".

    if ($FlagGitPull)
    {
        die "Error: Can't use both --gitreset and --gitpull\n"
            if $FlagGitReset;

        $TIDYUP = FALSE;

        if (-d 'minetest' && !-d 'minetest/.git')
        {
            print << 'END';

Error: "--gitpull" specified  and I see a  "minetest" directory but no
"minetest/.git" directory.

If you'd like to use "--gitpull",  delete, rename,  or move the "mine-
test" directory.

Or  you can use  "--gitreset" instead.  This will delete the directory
automatically.
END
            exit ONE;
        }

        if (!-d 'minetest')
        {
            print << 'END';
* "--gitpull" specified but I don't see a "minetest" directory
* Attempting a git clone
END
            $cmd = "git clone $GITURL minetest";
            print "  $cmd\n";
            &RunCmd ($cmd);
        }
        else
        {
            die "$IE #250458\n" unless -d 'minetest/.git';

            print << 'END';
* --gitpull specified and I see "minetest/.git"
* Attempting a git pull
END
            &pushd ('minetest');
            $cmd = << 'END';
git pull || exit 1
END
            &RunCmd ($cmd);
            &popd();
        }
    }

#---------------------------------------------------------------------
# Handle "--client" and "--server".

    my  $client_line = "-DBUILD_CLIENT=1" ;
    my  $server_line = "-DBUILD_SERVER=1" ;

    if ( $FlagClient && !$FlagServer)
    {
        $client_line = "-DBUILD_CLIENT=1" ;
        $server_line = "-DBUILD_SERVER=0" ;
    }

    if (!$FlagClient &&  $FlagServer)
    {
        $client_line = "-DBUILD_CLIENT=0" ;
        $server_line = "-DBUILD_SERVER=1" ;
    }

#---------------------------------------------------------------------
# Status messages.

    my $NUBDF = "not used by default in this version";

    print << 'END';
* leveldb (by default)
* sqlite3 (by default)
END

#---------------------------------------------------------------------
# Handle "--postgres".

    my $postgres_line = "-DENABLE_POSTGRESQL=0";

    if ($FlagPostgres)
    {
        print "* postgres (due to --postgresql)\n";
        $postgres_line =~ s@0\z@1@;
    }
    else
    {
        print "  (skipping postgresql -- $NUBDF)\n";
    }

#---------------------------------------------------------------------
# Handle "--redis".

    my $redis_line = "-DENABLE_REDIS=0";

    if ($FlagRedis)
    {
        print "* redis (due to --redis)\n";
        $redis_line =~ s@0\z@1@;
    }
    else
    {
        print "  (skipping redis -- $NUBDF)\n";
    }

#---------------------------------------------------------------------
# "--portable" requires the bootstrapped "gcc".

    if ($PORTABLE && !-f "$BINDIR/gcc")
    {
        print << 'END';

Error: For Linux portable mode (--portable), you need to build the in-
cluded  "gcc" 8 compiler.  To do so, run "mtcompile-libraries.sh" with
gcc-bootstrap mode enabled.
END
        exit ONE;
    }

#---------------------------------------------------------------------
# Identify "gcc" major release number.

    $str = "\n" . &FixStr (`gcc --version 2>&1`);
    my ($GCCVER) = $str =~ m@\ngcc.* (\d+)*\.\d+\.@;
    die "Error: Not able to identify gcc release\n"
        unless defined $GCCVER;

#---------------------------------------------------------------------
# Replace existing "minetest" directory.

    my  $RESETDIR = (!-d $PRODDIR) || $TIDYUP;

    if ($RESETDIR)
    {
        if ($FlagSafe && (-d 'minetest'))
        {
            print << 'END';

Error:  We  need  to delete  the  existing "minetest"  directory,  but
"--safe" is  specified.  If you'd like to preserve the directory, move
or rename it. Otherwise, drop the "--safe" switch.
END
            exit ONE;
        }

        $cmd = << "END";
rm -fr  $PRODDIR minetest-newline*              || exit 1
mkdir   $PRODDIR minetest-newline               || exit 1
rmdir   $PRODDIR minetest-newline               || exit 1
END
        $cmd = << "END" if     $FlagEdgy;
tar jxf $BALLDIR/minetest-edgytest.tar.bz2      || exit 1
mv               minetest-edgytest* $PRODDIR    || exit 1
END
        $cmd = << "END" unless $FlagEdgy;
tar jxf $BALLDIR/minetest-newline.tar.bz2       || exit 1
mv               minetest-newline*  $PRODDIR    || exit 1
END
        &RunCmd ($cmd);
    }

#---------------------------------------------------------------------

    chdir ($PRODDIR) || die "$IE #505850\n";

#---------------------------------------------------------------------
# Sanity check.

    if (!-f 'CMakeLists.txt')
    {
        print << 'END';
Error: You're trying to build using a "minetest" directory that's mis-
sing a "CMakeLists.txt".  The directory was probably tidied up after a
previous build.

To  rebuild, delete, move, or  rename the "minetest" directory and try
again.
END
        exit ONE;
    }

#---------------------------------------------------------------------
# Delete leftover temporary files.

    $cmd = << 'END';
for x in \
    C.includecache                  \
    CXX.includecache                \
    CMakeCache.txt                  \
    CMakeCCompiler.cmake            \
    CMakeCXXCompiler.cmake          \
    CMakeDirectoryInformation.cmake \
    CMakeRuleHashes.txt             \
    CPackConfig.cmake               \
    CPackSourceConfig.cmake         \
    DependInfo.cmake                \
    Makefile2                       \
    TargetDirectories.txt           \
    build.make                      \
    depend.make                     \
    depend.internal                 \
    cmake_config.h                  \
    cmake_install.cmake             \
    flags.make                      \
    link.txt                        \
    progress.make                   \
    relink.txt
do
    rm -fr `find . -name $x` || exit 1
done
END
    &RunCmd ($cmd);

#---------------------------------------------------------------------
# Delete more temporary files.

    $cmd = << 'END';
rm -fr textures/base/pack/menu_header_old.png           || exit 1
rm -fr `find . -name Makefile | grep -v build/android`  || exit 1
rm -fr `find . -name \*.a`                              || exit 1
rm -fr `find . -name \*.log`                            || exit 1
rm -fr `find . -name \*.o`                              || exit 1
END
    &RunCmd ($cmd);

#---------------------------------------------------------------------
# Define paths for some ".a" library files.

    my $IRRLICHT_LIBRARY = "$LIBDIR/libIrrlicht.a"   ;
    my $LEVELDB_LIBRARY  = "$LIBDIR/libleveldb.a"    ;
    my $LUA_LIBRARY      = "$LIBDIR/libluajit-5.1.a" ;
    my $SQLITE3_LIBRARY  = "$LIBDIR/libsqlite3.a"    ;

#---------------------------------------------------------------------
# Set "$XCFLAGS" (extra compiler flags).

    my $XCFLAGS = "-O2 -I$INCDIR";
       $XCFLAGS = "$XCFLAGS -g" if $MAKEDEBUG;
       $XCFLAGS = "-march=native $XCFLAGS" unless $PORTABLE;
       $XCFLAGS = "$XCFLAGS -Wl,-L$LIBDIR -Wl,-R$LIBDIR";

       $XCFLAGS = "$XCFLAGS -Wl,-L$LIB64DIR -Wl,-R$LIB64DIR"
           if -d $LIB64DIR;

    print "XCFLAGS=$XCFLAGS\n";

#---------------------------------------------------------------------
# Get pathnames for "gcc" and "g++" compilers.

    my $WHICH_GCC = &FixStr (`which gcc` );
    my $WHICH_GPP = &FixStr (`which g++` );

    die unless -f $WHICH_GCC && -x $WHICH_GCC;
    die unless -f $WHICH_GPP && -x $WHICH_GPP;

#---------------------------------------------------------------------
# Handle another "--edgy step".

    if ($FlagEdgy)
    {
        my $CM = 'src/defaultsettings.cpp';

        open (IFD, "<$CM")  || die "Internal error 0766\n";
        my $SS   = $/;
        undef $/;
        my $data = <IFD>;
           $data = "" unless defined $data;
        $/       = $SS;
        close (IFD);

        my $ses = 'secure.enable_security';
        $data =~ s@"$ses", "true"@"$ses", "false"@;

        open (OFD, ">$CM")  || die "Internal error 0777\n";
        print OFD $data;
        close (OFD)         || die "Internal error 0779\n";
    }

#---------------------------------------------------------------------
# Handle "--fakemt4".

    if ($FlagFakeMT4)
    {
        my $CM = 'CMakeLists.txt';

        open (IFD, "<$CM")  || die "Internal error 0789\n";
        my $SS   = $/;
        undef $/;
        my $data = <IFD>;
           $data = "" unless defined $data;
        $/       = $SS;
        close (IFD);

        my $pat = << 'END';
set\(VERSION_MAJOR \d+\)
.*?
if \(CMAKE_BUILD_TYPE STREQUAL Debug\)
END
        $pat  =~ s@\s+\z@@s;
        $pat  =~ s@\s*\n\s*@@gs;
        $data =~ s@\s*$pat\s*@\n$segment@is;

        open (OFD, ">$CM")  || die "Internal error 0806\n";
        print OFD $data;
        close (OFD)         || die "Internal error 0808\n";
    }

#---------------------------------------------------------------------
# Handle "--oldproto".

    if ($FlagOldProto)
    {
        my $CM = 'src/network/networkprotocol.h';

        open (IFD, "<$CM")  || die "Internal error 0714\n";
        my $SS   = $/;
        undef $/;
        my $data = <IFD>;
           $data = "" unless defined $data;
        $/       = $SS;
        close (IFD);

        $data =~ s@(#define\s+LATEST_PROTOCOL_VERSION)\s+3\d\b@$1 32@;

        open (OFD, ">$CM")  || die "Internal error 0715\n";
        print OFD $data;
        close (OFD)         || die "Internal error 0716\n";
    }

#---------------------------------------------------------------------
# Run "cmake".

    $cmd = << "END";
cmake
-DCMAKE_BUILD_TYPE=release
-DCMAKE_C_COMPILER=$WHICH_GCC
-DCMAKE_CXX_COMPILER=$WHICH_GPP

-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=1
-DCMAKE_SKIP_INSTALL_RPATH=0
-DCMAKE_SKIP_RPATH=0

$client_line
$server_line

-DENABLE_LEVELDB=1

$postgres_line
$redis_line

-DENABLE_SOUND=1
-DENABLE_SPATIAL=0
-DENABLE_SYSTEM_JSONCPP=0
-DRUN_IN_PLACE=1

-DIRRLICHT_INCLUDE_DIR=$INCDIR/irrlicht
-DIRRLICHT_LIBRARY=$IRRLICHT_LIBRARY

-DLEVELDB_INCLUDE_DIR=$INCDIR/leveldb
-DLEVELDB_LIBRARY=$LEVELDB_LIBRARY

-DLUA_INCLUDE_DIR=$INCDIR/luajit-2.1
-DLUA_LIBRARY=$LUA_LIBRARY

-DSQLITE3_INCLUDE_DIR=$INCDIR
-DSQLITE3_LIBRARY=$SQLITE3_LIBRARY

-DCMAKE_C_FLAGS="$XCFLAGS"
-DCMAKE_CXX_FLAGS="$XCFLAGS"
-DCMAKE_C_FLAGS_RELEASE="$XCFLAGS"
-DCMAKE_CXX_FLAGS_RELEASE="$XCFLAGS"
.
END
    $cmd = &FixStr ($cmd);
    &RunCmd ($cmd);

#---------------------------------------------------------------------
# Replace some "-l..." switches with absolute pathnames.

    $cmd = << "END";
sed -e "s:-lIrrlicht:$IRRLICHT_LIBRARY:g"
    -e "s:-lleveldb:$LEVELDB_LIBRARY:g"
    -e "s:-lluajit-5.1:$LUA_LIBRARY:g"
    -e "s:-lsqlite3:$SQLITE3_LIBRARY:g"
END
    $cmd .= << 'END';
    -i `find . -type f -name link.txt`
END
    $cmd = &FixStr ($cmd);
    &RunCmd ($cmd);

#---------------------------------------------------------------------
# Build the program.

    my $NUMJOBS = &FixStr (`getconf _NPROCESSORS_ONLN`);
    die "$IE #458310\n" unless $NUMJOBS =~ m@^\d{1,3}\z@;

    $cmd = << "END";            # "END" must be double-quoted here
make clean
make -j $NUMJOBS
mkdir -p client/serverlist
mkdir -p games worlds
cp -p $BALLDIR/arrowkeys.txt .
END
    &RunCmd ($cmd);

#---------------------------------------------------------------------
# Add preloaded cache.

    $cmd = << "END";            # "END" must be double-quoted here
rm -fr cache                        || exit 1
tar jxf $BALLDIR/cachemedia.tar.bz2 || exit 1
END
    &RunCmd ($cmd);

#---------------------------------------------------------------------
# Add "_games".

    &pushd ('games');
    $cmd = "";

    $cmd .= << "END";           # "END" must be double-quoted here
rm -fr minimal                      || exit 1
END
    $cmd .= << "END";
rm -fr             Bucket_Game      || exit 1
END
    $cmd .= << "END" unless $FlagEdgy;
rm -fr             Bucket_Game      || exit 1
mkdir              Bucket_Game      || exit 1
rmdir              Bucket_Game      || exit 1
unzip -qo $BALLDIR/Bucket_Game.zip  || exit 1
END

    $cmd .= << "END";
rm -fr             amhi_game        || exit 1
mkdir              amhi_game        || exit 1
rmdir              amhi_game        || exit 1
unzip -qo $BALLDIR/amhi_game.zip    || exit 1
END

    &RunCmd ($cmd);
    &popd();

#---------------------------------------------------------------------
# Add worlds.

    &pushd ('worlds');

    for my $world (qw (Bucket_City Wonder_World))
    {
        system "rm -fr $world";
        next if $FlagEdgy;

        $cmd = << "END";        # "END" must be double-quoted here
mkdir   $world                      || exit 1
rmdir   $world                      || exit 1
tar jxf $BALLDIR/$world.tar.bz2     || exit 1
END
        &RunCmd ($cmd);
    }
    &popd();

#---------------------------------------------------------------------
# Strip the executable(s).

    if (!$MAKEDEBUG)
    {
        $cmd = << 'END';
strip bin/minetest*
END
        &RunCmd ($cmd);
    }

#---------------------------------------------------------------------
# Additional cleanup.

    if ($TIDYUP)
    {
        $cmd = << 'END';        # 'END' must be single-quoted here
rm -fr CMake* *cmake Makefile
rm -fr build *.md debug.txt lib src
rm -fr `find . -name .[a-z]\* | grep -v " " | grep -v '\.dummy'`
END
        &RunCmd ($cmd);
    }

#---------------------------------------------------------------------
# Finish required "--portable" operations.

    if ($PORTABLE)
    {
        my $M    = &FixStr (`uname -m`)     ;
        my $BITS = ($M eq "i686") ? 32 : 64 ;

        $cmd = << "END";        # "END" must be double-quoted here
rm -fr solib                        || exit 1
tar jxf $BALLDIR/solib$BITS.tar.bz2 || exit 1
END
        &RunCmd ($cmd);
        &pushd ('bin');

        for my $prog (qw (minetest minetestserver))
        {
            $cmd = << "END";    # "END" must be double-quoted here
rm -fr   $prog.bin                  || exit 1
mv $prog $prog.bin                  || exit 1
cp -p $BALLDIR/$prog.wrapper $prog  || exit 1
chmod 755                    $prog  || exit 1
END
            &RunCmd ($cmd);
        }

        &popd();

#---------------------------------------------------------------------

        if ($MAKEPROD)
        {
            chdir ($THISDIR) || die "$IE #505833\n";
            my $ZIPDIR  = "minetest-linux$BITS" ;
            my $ZIPFILE = "$ZIPDIR.zip"         ;

            $cmd = << "END";    # "END" must be double-quoted here
rm -fr      $ZIPDIR  $ZIPFILE   || exit 1
mv $PRODDIR $ZIPDIR             || exit 1
zip -ro9q   $ZIPFILE $ZIPDIR    || exit 1
rm -fr               $ZIPDIR    || exit 1
ls -l       $ZIPFILE            || exit 1
END
            &RunCmd ($cmd);
        }
    }

    print "Done\n";
    undef;
}

#---------------------------------------------------------------------
#                            main program
#---------------------------------------------------------------------

&Main();                        # Call the main routine
exit ZERO;                      # Normal exit
