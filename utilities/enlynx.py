#!/usr/bin/env python3
'''
Specify a label or search term, optionally with a page #.

Examples:
# label:
    enlynx.py Bucket_Game
# Use a different binary name or path other than lynx:
    enlynx.py Bucket_Game --browser surfraw
# label and page number:
    enlynx.py Bucket_Game page 2
# multiple labels:
    enlynx.py Bucket_Game urgent
# closed issues only:
    enlynx.py Bucket_Game --closed
# both closed and open issues:
    enlynx.py Bucket_Game --closed --open
# search:
    enlynx.py find SIGSEGV
# search for 2 terms:
    enlynx.py find mobs find walk
    # or
    enlynx.py find mobs AND walk
# search for a closed issue:
    enlynx.py find SIGSEGV --closed
# label with search:
    enlynx.py Bucket_Game find mobs
# label with search, next page:
    enlynx.py Bucket_Game find node page 2


'''
me = "enlynx.py"
browserPath = "lynx"
sessionPath = "/tmp/enlynx.lynx-session"
import sys
import subprocess

enc = {}  # URL Encoded single characters
enc[':'] = '%3A'
# ^ Do this with urllib if there are many more

# see <https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python>
def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

verbose = True

def debug(msg):
    if not verbose:
        return
    sys.stderr.write("{}\n".format(msg))
    sys.stderr.flush()


def usage():
    error(__doc__)


def toSubQueryValue(value):
    '''
    Convert the value to one that will fit in a
    key+urlencoded(colon)+value string for GitHub queries.

    This function is copied to multiple scripts so they have no
    dependencies:
    - enissue.py
    - enlynx.py
    '''
    if " " in value:
        value = '"' + value.replace(" ", "+") + '"'
    return value


def toSubQuery(key, value):
    return key + enc[':'] + value


base_url = "https://github.com/poikilos/EnlivenMinetest"
query_url = base_url + "/issues"
open_q = "?q=" + toSubQuery("is", "issue") + '+' + toSubQuery("is", "open")
any_q = "?q=" + toSubQuery("is", "issue")
closed_q = "?q=" + toSubQuery("is", "issue") + '+' + toSubQuery("is", "closed")


if __name__ == "__main__":
    prev_arg = None
    findStrings = []
    base_q = open_q + "+"
    page_param = ""
    _closed = None
    _open = None
    labels_subqueries = ""
    for arg in sys.argv[1:]:
        # ^ skip arg 0 since it is self
        # Erase prev_arg in each case except "else" to turn off
        # context-sensitivity after the term after the command is found.
        if (prev_arg == "find") or (prev_arg == "AND"):
            findStrings.append(arg)
            prev_arg = None
        elif prev_arg == "--browser":
            browserPath = arg
        elif prev_arg == "page":
            page_param="&page=2"
            prev_arg = None
        else:
            if arg == "--closed":
                _closed = True
            elif arg == "--open":
                _open = True
            elif arg == "find":
                prev_arg = arg
            elif arg == "--browser":
                prev_arg = arg
            elif arg == "AND":
                if len(findStrings) == 0:
                    usage()
                    error("Error: You can only use AND after find"
                          " and after another keyword. To literally"
                          " search for the word \"AND\" itself,"
                          " say find before the word:\n"
                          "    {} find CREEPS find AND find WEIRDOS\n"
                          "".format(me))
                    exit(1)
                prev_arg = arg
            elif arg == "page":
                prev_arg = arg
            else:
                encArg = toSubQueryValue(arg)
                # if encArg != arg:
                #     debug("* encoding label as '{}'".format(encArg))
                # else:
                debug("* adding label {}".format(encArg))

                labels_subqueries += toSubQuery('label', encArg) + "+"

    # Ensure there aren't any dangling commands *after* the loop:
    if prev_arg is not None:
        usage()
        error("Error: You must specify a search term after {}."
              "".format(prev_arg))
        exit(1)

    if (_closed is True) and (_open is True):
        base_q = any_q + '+'
    elif _open is True:
        base_q = open_q + '+'  # This is the default
    elif _closed is True:
        base_q = closed_q + '+'



    for find_str in findStrings:
        base_q += find_str + "+"
    # else: (dangling '+' at the end when labels_subqueries=="" is ok)

    query = base_q + labels_subqueries + page_param
    url = query_url + query
    print("URL: {}".format(url))

    subprocess.call([browserPath, '-session=' + sessionPath, url])
