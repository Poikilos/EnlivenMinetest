#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Purpose: View and cache issues in the EnlivenMinetest repo.
Author: 2020-2021 Jake Gustafson
License: See license file at https://github.com/Poikilos/EnlivenMinetest

This script caches issues (To
~/.cache/enissue/Poikilos/EnlivenMinetest/issues
by default).

Known issues:
- Get attachments from GitHub
- Get inline files from GitHub (such as pasted images)

Options:
--cache-base <dir>   Set the directory for cached files.
--verbose            Enable verbose mode.
--debug              Enable verbose mode (same as --debug).
--copy-meta-to <dbname> --db-type <db-type) --db-user <user> --db-password <password>
    Write database entries for the issue, timeline events, and reactions
    to each timeline event (overwrite ANY existing data if same id!).
    Only "PostgresQL" is implemented for db-type.
    The destination will be overwritten! Backup first:
    - PostgreSQL (su <dbusername> then):
    pg_dump dbname > outfile
--test               Run unit tests then exit (0) if passed.

## Partial API documentation:
This part covers the use of enissue itself as a Python API such as via
`import enissue` (For using a web API, you must view the API
documentation at the website of the specific web API).

### options keys:
- default_dt_parser: This must be a method that returns a python
    datetime object by accepting a single argument, which is a string
    from the style of the Repo's API.
- token: This should be set to a token that you've generated using the
  web interface of your repo. The token will cause you to "see your
  rate limit bumped to 5,000 requests an hour" on Github according to
  <https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api>
  2021-11-30.
'''
from __future__ import print_function
import sys
import json
import os
import platform
import copy
from datetime import datetime, timedelta
if sys.version_info.major >= 3:
    import urllib.request
    request = urllib.request
else:
    # python2
    print("* detected Python " + str(sys.version_info.major))
    import urllib2 as urllib
    request = urllib

if sys.version_info.major >= 3:
    from urllib.parse import urlparse
    # from urllib.parse import quote_plus
    from urllib.parse import urlencode
    from urllib.parse import quote
    from urllib.parse import unquote
    from urllib.error import HTTPError
    try:
        import requests
    except ImportError:
        sys.stderr.write("If you try to use a token, you must have the"
                         " requests package for python3 such as via:\n"
                         "    sudo apt-get install python3-requests")
        sys.stderr.flush()
else:
    # Python 2
    # See <https://docs.python.org/2/howto/urllib2.html>
    from urlparse import urlparse
    # from urlparse import quote_plus
    from urllib import urlencode
    from urllib import quote
    from urllib import unquote
    from urllib2 import HTTPError
    # ^ urllib.error.HTTPError doesn't exist in Python 2
    try:
        import requests
    except ImportError:
        sys.stderr.write("If you try to use a token, you must have the"
                         " requests package for python2 such as via:\n"
                         "    sudo apt-get install python-requests")
        sys.stderr.flush()



# see <https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python>
def echo0(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# https://api.github.com/repos/Poikilos/EnlivenMinetest/issues/475/timeline

verbose = False

for argI in range(1, len(sys.argv)):
    arg = sys.argv[argI]
    if arg.startswith("--"):
        if arg == "--debug":
            verbose = True
        elif arg == "--verbose":
            verbose = True

default_options = {
    # 'repo_url': "https://api.github.com/repos/Poikilos/EnlivenMinetest",
    'repo_url': "https://github.com/Poikilos/EnlivenMinetest",
}

sites_users_repos_meta = {
    'https://api.github.com': {
        'Poikilos': {
            'EnlivenMinetest': {
                'repository_id': "80873867"
            }
        }
    }
}
'''
# ^ Get repo metadata for known repos such as via:
site_users_repos_meta = sites_users_repos_meta.get(instance_url)
if site_users_repos_meta is not None:
    user_repos_meta = site_users_repos_meta.get(remote_user)
    if user_repos_meta is not None:
        repo_meta = user_repos_meta.get(repo_name)
        if repo_meta is not None:
            if repository_id is None:
                repository_id = repo_meta.get('repository_id')
'''


def github_ts_to_dt(timestamp_s):
    '''
    Use "%Y-%m-%dT%H:%M:%SZ" for GitHub.
    GitHub example (Z for UTC): 2018-09-13T16:59:38Z
    '''
    return datetime.strptime(timestamp_s, "%Y-%m-%dT%H:%M:%SZ")


giteaSanitizedDtFmt = "%Y-%m-%dT%H:%M:%S%z"
giteaDtExampleS = "2021-11-25T12:00:13-05:00"
sanitizedDtExampleS = "2021-11-25T12:00:13-0500"
giteaExtraColonAt = giteaDtExampleS.rfind(":")
giteaColonNegI = -3
if giteaExtraColonAt - len(giteaDtExampleS) != giteaColonNegI:
    raise RuntimeError("The Gitea timestamp format description wasn't"
                       " prepared correctly.")

def gitea_ts_to_dt(timestamp_s):
    '''
    Use giteaSanitizedDtFmt BUT last ':' must be removed before
    parsing (but: datetime still does it right somehow either way)
    or added after formatting.
    Gitea example: "2021-11-25T12:00:13-05:00"
    '''
    giteaSanitizedDtFmt = "%Y-%m-%dT%H:%M:%S%z"
    if len(timestamp_s) != len(giteaDtExampleS):
        raise ValueError("Gitea {} is not like the expected {}"
                         "".format(timestamp_s, giteaDtExampleS))
    timestamp_s_raw = timestamp_s
    colonNegI = giteaColonNegI
    timestamp_s = timestamp_s[:colonNegI] + timestamp_s[colonNegI+1:]
    '''
    Remove the non-python-like : from %z
    %z is "+0000 UTC offset in the form ?HHMM[SS[.ffffff]] (empty
    string if the object is naive)." where '?' is +/-
    - <https://strftime.org/>
    '''
    return datetime.strptime(timestamp_s, giteaSanitizedDtFmt)

# See:
# - labels: <https://docs.github.com/en/rest/issues/labels
#   #list-labels-for-a-repository>
github_defaults = {
    # 'repository_id': "",  # Use sites_users_repos_meta instead.
    'instance_url': "https://api.github.com",
    'api_repo_url_fmt': "{instance_url}/repos/{ru}/{rn}",
    'api_issue_url_fmt': "{instance_url}/repos/{ru}/{rn}/issues/{issue_no}",
    'search_issues_url_fmt': "{instance_url}/search/issues?q=repo%3A{ru}/{rn}+",
    # 'base_query_fmt': "?q=repo%3A{ru}/{rn}+",
    'search_results_key': "items",
    'api_labels_url_fmt': "{instance_url}/repos/{ru}/{rn}/labels",
    'page_size': 30,
    'c_issues_name_fmt': "issues_page={p}{q}.json",
    'c_issue_name_fmt': "{issue_no}.json",
    'default_query': {'state':'open'},
    'hide_events': ['renamed', 'assigned'],
    'api_comments_url_fmt': "{instance_url}/repos/{ru}/{rn}/issues/comments",
    'known_issue_keys': {
        'created_at': 'created_at',
        'updated_at': 'updated_at',
        'closed_at': 'closed_at',
        'body': 'body',
        'title': 'title',
    },
    'default_dt_parser': github_ts_to_dt,
}

# See:
# - labels: <https://any-api.com/gitea_io/gitea_io/docs
#   /_repos_owner_repo_labels?query=labels>
gitea_defaults = {
    # 'repository_id': None,  # Use sites_users_repos_meta instead.
    'api_repo_url_fmt': "{instance_url}/api/v1/repos/{ru}/{rn}",
    'api_issue_url_fmt': "{instance_url}/api/v1/repos/{ru}/{rn}/issues/{issue_no}",
    'search_issues_url_fmt': "{instance_url}/api/v1/search/issues?q=repo%3A{ru}/{rn}+",
    # 'base_query_fmt': "?q=repo%3A{ru}/{rn}+",  # TODO: Change for Gitea ??
    'search_results_key': "items", # TODO: Change for Gitea ??
    'api_labels_url_fmt': "{instance_url}/repos/{ru}/{rn}/labels",
    'page_size': 30,  # TODO: Change for Gitea ??
    'c_issues_name_fmt': "issues_page={p}{q}.json",
    'c_issue_name_fmt': "{issue_no}.json",
    'default_query': {'state':'open'},  # TODO: Change for Gitea ??
    'hide_events': ['renamed', 'assigned'],
    'api_comments_url_fmt': "{instance_url}/api/v1/repos/{ru}/{rn}/issues/comments",
    'known_issue_keys': {
        'created_at': 'created_at',
        'updated_at': 'updated_at',
        'closed_at': 'closed_at',
        'body': 'body',
        'title': 'title',
    },
    'default_dt_parser': gitea_ts_to_dt,
}

# API documentation:
# https://docs.gitea.io/en-us/api-usage/ says:
# > API Reference guide is auto-generated by swagger and available on: https://gitea.your.host/api/swagger or on [gitea demo instance](https://try.gitea.io/api/swagger)
# > The OpenAPI document is at: https://gitea.your.host/swagger.v1.json


apis = {}
apis["GitHub"] = github_defaults
apis["Gitea"] = gitea_defaults


def tests():
    for name, options in apis.items():
        if options.get('default_query') is None:
            raise AssertionError("There must be a 'default_query'"
                                 " in apis['{}']."
                                 "".format(name))
        if not isinstance(options.get('default_query'), dict):
            raise AssertionError(" apis['{}']['default_query']"
                                 " must be a dict."
                                 "".format(name))
        for k,v in options['default_query']:
            if v is None:
                raise AssertionError("{} is None".format(k))


def debug(*args, **kwargs):
    msg = ""
    if verbose:
        if len(args) > 0:
            msg = args[0]
        echo0("[debug] " + msg)


def set_verbose(on):
    global verbose
    if on is True:
        verbose = True
    elif on is False:
        verbose = True
    else:
        raise ValueError("on must be True or False.")


def decode_safe(b):
    try:
        s = b.decode()
    except UnicodeDecodeError:
        s = b.decode('utf-8')
    return s


# me = sys.argv[0]
me = os.path.basename(__file__)
modes = {
    "list": {
        "help": ("List all issues. Provide one or more labels to narrow"
                 " down the list. Alternatively, provide a label only."
                 " Labels with spaces require quotes. The matching is"
                 " not case sensitive. The \"list\" command can be"
                 " implied by not using a label (any word that isn't a"
                 " command will select a label) and no command."),
        "examples": ["list", " list Bucket_Game",
                     " list Bucket_Game urgent", " Bucket_Game",
                     " Bucket_Game urgent", " Bucket_Game --closed"]
    },
    "labels": {
        "help": ("List all labels (just the labels themselves, not the"
                 " issues)."),
        "examples": [" labels"]
    },
    "find": {
        "parent": "list",
        "help": ("To search using a keyword, say \"find\" or \"AND\""
                 " before each term."),
        "examples": [
            " find mobs  # term=mobs",
            " find mobs find walk  # term[0]=mobs, term[1]=walk",
            " find mobs AND walk  # ^ same: term[0]=mobs, term[1]=walk",
            " find \"open doors\"  # term=\"open doors\"",
            " find mobs Bucket_Game  # term=mobs, label=Bucket_Game",
            " find mobs # term=mobs",
            (" find CREEPS find AND find WEIRDOS"
             "  # specifies (3) terms = [CREEPS, AND, WEIRDOS]"),
            (" find CREEPS AND AND AND WEIRDOS "
             " # ^ same: specifies (3) terms = [CREEPS, AND, WEIRDOS]"),
            (" find CREEPS AND WEIRDOS"
             "  # specifies (2) terms = [CREEPS, WEIRDOS]"),
        ],
        "AND_EXAMPLES": [6, 7],  # indices in ['find']['examples'] list
    },
    "open": {
        "parent": "list",
        "help": ("Only show a closed issue, or show closed & open"
                 " (The default is open issues only)"),
        "examples": [
            " --closed",
            " --closed --open",
            " Bucket_Game --closed  # closed, label=Bucket_Game",
            " Bucket_Game --closed open  # open, label=Bucket_Game",
        ]
    },
    "page": {
        "parent": "list",
        "help": ("GitHub only lists 30 issues at a time. Type page"
                 " followed by a number to see additional pages."),
        "examples": [" page 2", " page 2 --closed"]
    },
    "<#>": {
        "parent": "issue",
        "help": "Specify an issue number to see details.",
        "examples": [" 1"]
    },
}
# ^ The parent mode is the actual operating mode whereas the submodes
#   are only for documenting the keywords that apply to the parent mode.
modes["closed"] = modes["open"]

match_all_labels = []

trues = ["true", "on", "yes"]
falses = ["false", "off", "no"]

# TODO: Consider from pycodetool import to_syntax_error
#  (to replace instances of {}:{}: formatted by `path, line` below).

def str_to_value(valueStr, typeName=None, lineN=-1, path="(generated)"):
    '''
    Convert a string such as from a conf file to a value that may be of
    a different type than string. The type will be detected by the
    content of the string as follows (in order):
    - If it is the string "None" then it will become None.
    - It is int if it converts to int without ValueError.
    - It is float if it converts to float without ValueError.
    - It is bool if the string is (case insensitively) in the trues or
      falses list.
    - It is a string in all other cases.    typeStr = None

    Keyword arguments:
    typeName -- Force it to be this type, otherwise raise ValueError.
        If typeName is "bool", a number 0 or 1 will be converted to
        False or True, respectively. Otherwise, the value has to be in
        the global trues or falses list (case-insensitive). The typeName
        must be: int, str, float, or bool, such as obtained via
        `type(anotherValue).__name__`.
    path -- The file (used for error reporting only).
    lineN -- The line number in the file (used for error reporting only).
    '''
    valueL = None
    if valueStr is not None:
        valueL = valueStr.lower()
    else:
        raise RuntimeError("A symbolic value is extracted from code or"
                           " a conf file, so it should never be None."
                           " If it were None in the source, it should"
                           " be an empty string or the string \"None\"")

    if typeName is not None:
        if valueStr == "None":
            echo0("{}:{}: WARNING: The program expected a(n) '{}' but"
                                 " the value was 'None' and will become"
                                 " None."
                                 "".format(conf_path, lineN, typeName))
            return None
        elif typeName == "bool":
            moreTrues = ['1'] + trues
            moreFalses = ['0'] + falses
            if valueL in moreTrues:
                return True
            elif valueL in moreFalses:
                return False
            else:
                raise ValueError("{}:{}: A bool value is expected:"
                                 " {} or {} (case insensitive) and if"
                                 " the typeName is defined by the"
                                 " program as 'bool' (which it is in"
                                 " this case) then '0' or '1'"
                                 " are also ok)."
                                 "".format(conf_path, lineN, trues,
                                           falses))
        elif typeName == 'int':
            try:
                return int(valueStr)
            except ValueError:
                raise ValueError("{}:{}: An int value is expected:"
                                 " the typeName is defined by the"
                                 " program as 'int'."
                                 "".format(conf_path, lineN, trues,
                                           falses))
        elif typeName == 'float':
            try:
                return float(valueStr)
            except ValueError:
                raise ValueError("{}:{}: A float value is expected:"
                                 " the typeName is defined by the"
                                 " program as 'float'."
                                 "".format(conf_path, lineN, trues,
                                           falses))
        elif typeName == "str":
            if valueStr.startswith("'") and valueStr.endswith("'"):
                return valueStr[1:-1]
            if valueStr.startswith('"') and valueStr.endswith('"'):
                return valueStr[1:-1]
            return valueStr
        else:
            raise NotImplementedError("The type {} isn't implemented"
                                      " in str_to_value."
                                      "".format(typeName))

    if valueStr == "None":
        return None
    try:
        return int(valueStr)
    except ValueError:
        pass
    try:
        return float(valueStr)
    except ValueError:
        pass
    if valueL in trues:
        return True
    elif valueL in falses:
        return False
    if valueStr.startswith("'") and valueStr.endswith("'"):
        return valueStr[1:-1]
    if valueStr.startswith('"') and valueStr.endswith('"'):
        return valueStr[1:-1]
    return valueStr


def modify_dict_by_conf(options, conf_path, always_lower=False,
                        no_file_error=True, no_value_error=True,
                        quiet=True):
    '''
    Set values in the options dict using conf assignment operations
    in the file at conf_path. If the key is in the dict, that will
    determine the type. Otherwise, the type will be detected by
    str_to_value. If there is nothing after the equal sign on the line,
    the value will be None (or if no_value_error is True it will be
    ignored and an error will be displayed).

    Keyword arguments:
    always_lower -- If True, options in the conf file won't be added
        if they aren't lowercase.
    no_file_error -- Show an error if the file doesn't exist.
    no_value_error -- Show an error if the value is blank. If False,
        set the value to None.
    quiet -- Do not show when a value is set.
    '''
    conf_name = os.path.basename(conf_path)
    lineN = 0
    if os.path.isfile(conf_path):
        with open(conf_path, 'r') as ins:
            for rawL in ins:
                lineN += 1  # Counting numbers start at 1.
                line = rawL.strip()
                if len(line) == 0:
                    continue
                if line.startswith("#"):
                    continue
                signI = line.find("=")
                if signI < 1:
                    echo0("{}:{}: A value is expected before '='."
                          "".format(conf_path, lineN))
                name = line[:signI].strip()
                valueStr = line[signI+1:].strip()
                value = None
                if valueStr == "":
                    value = None
                if always_lower:
                    if name.lower() != name:
                        echo0("{}:{}: A lowercase name is expected."
                              "".format(conf_path, lineN))
                        continue
                if (valueStr is None) and no_value_error:
                    echo0("{}:{}: A value is expected."
                              "".format(conf_path, lineN))
                else:
                    typeName = None
                    oldValue = options.get(name)
                    if oldValue is not None:
                        typeName = type(oldValue).__name__
                    value = str_to_value(valueStr, typeName=typeName,
                                         path=conf_path, lineN=lineN)
                    options[name] = value
                    if not quiet:
                        echo0("[settings] {}: Set {} to {}"
                              "".format(conf_name, name, value))
    else:
        if no_file_error:
            echo0("Error: \"{}\" Doesn't exist"
                  "".format(conf_path, lineN))


def toSubQueryValue(value):
    '''
    Convert the value to one that will fit in a
    key+urlencoded(colon)+value="+" string (can end in plus, so leave
    it on the end to easily add more terms later) for GitHub queries.

    This function is copied to multiple scripts so they have no
    dependencies:
    - enissue.py
    - enlynx.py
    '''
    if " " in value:
        value = '"' + value.replace(" ", "+") + '"'
    return value


def to_error(results):
    if hasattr(results, 'items'):
        if results.get('documentation_url') is not None:
            msg = results.get('message')
            if msg is None:
                msg = "There is nothing at the address."
            return {
                'code': 404,  # Silly GitHub, I will force a 404 of course since you didn't.
                'reason': msg,
            }
    return None


def usage():
    print("")
    print("Commands:")
    left_w = 10
    spacer = " -- "
    line_fmt = "{: <" + str(left_w) + "}" + spacer + "{}"
    for name, command in modes.items():
        hlp = command["help"]
        print(line_fmt.format(name, hlp))
        if len(command["examples"]) > 0:
            print(" "*(left_w+len(spacer)) + "Examples:")
            for s in command["examples"]:
                print(" "*(left_w+len(spacer)+2) + "./" + me + s)
        print("")
        print("")
    print("")
    print(__doc__)


class Repo:
    profile = None
    os_user = None
    AppDatas = None
    if platform.system() == "Windows":
        profile = os.environ['USERPROFILE']
        os_user = os.environ.get('USERNAME')
        AppDatas = os.environ.get('APPDATA')
    else:
        profile = os.environ['HOME']
        os_user = os.environ.get('USER')
        AppDatas = os.path.join(profile, ".config")

    def __init__(
            self,
            options
        ):
        '''
        Keyword arguments:
        options -- Set self.options. Any that aren't set will be
                detected based on the URL, otherwise from
                options['api_id'] (if there is an api name that
                corresponds to your site's API in the apis global dict).
                The options dict may have any of the following keys:
            repo_url -- This is required. It can be an API or web URL
                as long as it ends with username/reponame (except where
                there is no username in the URL).
            remote_user -- The repo user is used in api_repo_url_fmt,
                and cache path if caches is not on single_cache mode
                (If present, remote_user overrides the one detected from
                the repo_url).
            repo_name -- The repo name is used in api_repo_url_fmt,
                and cache path if caches is not on single_cache mode
                (If present, repo_name overrides the one detected from
                the repo_url).
            api_repo_url_fmt -- The format string where {ru} is where a repo
                                user goes, and {rn} is where a repo name
                                goes, is used for the format of
                                self.repo_url.
            api_issue_url_fmt -- a format string where {issue_url} is
                                 determined by api_repo_url_fmt and
                                 {issue_no} is where an issue number goes.
            api_comments_url_fmt -- Set the comments URL format (see the
                default for an example).
            page_size -- This must be set to the page size that is
                         compatible with the URL in api_repo_url_fmt, such
                         as exactly 30 for GitHub.
            c_issues_name_fmt -- This converts a URL to a cache filename,
                                 where {p} is the page number and {q} is any
                                 additional query such as "&state=closed".
            c_issue_name_fmt -- This converts a URL to a cache filename,
                                where {issue_no} is the issue number.
            default_query -- This dictionary must contain all URL query
                             parameters that the API assumes and that don't
                             need to be provided in the URL.
            hide_events -- Do not show these event types in an issue's
                           timeline.
            search_results_key -- If the URL described by
                search_issues_url_fmt returns a dict, specify the key in
                the dict that is a list of issues.
            caches_path -- Store cached json files here: Specifically,
                in an "issues" directory or other directory under the
                user and repo directory. For example, if caches_path is
                None and uses the default ~/.cache/enissue, the
                numbered json files (and numbered folders containing
                timeline.json or other connected data) for issues will
                appear in
                "~/.cache/enissue/Poikilos/EnlivenMinetest/issues". To
                set it later, use the setCachesPath method.
                This is the default behavior, and  the default is
                os.path.join(userprofile, ".cache").
            single_cache -- Store all issue data in one flat directory
                structure (except for issues and other subdirectories
                which mimic the web API routes). Only use this option
                if you set a different single_cache for each repo!
            api_id -- a key in the global apis dict which determines the
                defaults for accessing the web API.
        '''

        if options is None:
            raise ValueError("options cannot be None.")
        repo_url = options.get('repo_url')
        debug("* using URL {}".format(repo_url))
        if repo_url is None:
            raise ValueError("repo_url is required (API or web URL).")
        if repo_url.endswith(".git"):
            repo_url = repo_url[:-4]
        urlParts = repo_url.split("/")
        self.remote_user = urlParts[-2]
        self.api_id = options.get('api_id')
        if urlParts[-2] == "repo.or.cz":
            self.remote_user = "almikes@aol.com"  # Wuzzy2
            if self.api_id is not None:
                if self.api_id != 'git_instaweb':
                    echo0("WARNING: URL has [] but self.api_id was {}"
                          "".format(urlParts[-2], self.api_id))
            self.api_id = "git_instaweb"
            # Such as https://repo.or.cz/minetest_treasurer.git
            # - locally, git instaweb is controlled via:
            #   git instaweb --httpd=webrick --start
            #   git instaweb --httpd=webrick --stop

        remote_user = options.get('remote_user')
        if remote_user is not None:
            self.remote_user = remote_user
        del remote_user

        self.repo_name = urlParts[-1]

        repo_name = options.get('repo_name')
        if repo_name is not None:
            self.repo_name = repo_name
        del repo_name

        if self.api_id is None:
            if len(urlParts) > 2:
                if "github.com" in urlParts[2]:
                    # [0] is https:
                    # [1] is '' (because of //)
                    self.api_id = "GitHub"
                    debug("* detected GitHub in {}".format(urlParts))
                else:
                    debug("* no api detected in {}[2]".format(urlParts))
            else:
                debug("* no generic urlParts were found in "
                      "".format(urlParts))
        else:
            debug("* using specified API: {}".format(self.api_id))
        if self.api_id is None:
            self.api_id = "Gitea"
            if "github.com" in repo_url.lower():
                echo0("WARNING: assuming Gitea but URL has github.com.")
            echo0("  * assuming API is {} due to non-GitHub URL {}"
                  "".format(self.api_id, repo_url))
        if self.api_id is None:
            raise RuntimeError("api_id is not set")
        api_meta = apis.get(self.api_id)
        if api_meta is None:
            raise NotImplementedError("{} api_id is not implemented"
                                      "".format(self.api_id))
        for k, v in api_meta.items():
            # Set it to the default if it is None:
            if options.get(k) is None:
                options[k] = v

        debug("* constructing {} Repo".format(self.api_id))
        debug("  * detected remote_user \"{}\" in url"
              "".format(self.remote_user))
        debug("  * detected repo_name \"{}\" in url"
              "".format(self.repo_name))
        if self.api_id == "Gitea":
            instance_url = "/".join(urlParts[:-2])
            debug("  * detected Gitea url " + instance_url)
        else:
            instance_url = options.get('instance_url')
            if instance_url is None:
                raise NotImplementedError("Detecting the instance_url"
                                          " is not implemented for"
                                          " {}".format(self.api_id))
            debug("  * detected instance_url " + instance_url)
        # NOTE: self.instance_url is set by super __init__ below.
        # base_query_fmt = options['base_query_fmt']
        # search_issues_url_fmt = \
        #     "{instance_url}/api/v1/repos/issues/search"+base_query_fmt
        self.repository_id = options.get('repository_id')
        site_users_repos_meta = sites_users_repos_meta.get(instance_url)
        if site_users_repos_meta is not None:
            user_repos_meta = site_users_repos_meta.get(self.remote_user)
            if user_repos_meta is not None:
                repo_meta = user_repos_meta.get(self.repo_name)
                if repo_meta is not None:
                    if self.repository_id is None:
                        self.repository_id = \
                            repo_meta.get('repository_id')

        self.instance_url = instance_url

        self.rateLimitFmt = ("You may be able to view the issues"
                             " at the html_url, and a login may be"
                             " required. The URL \"{}\" is not"
                             " accessible, so you may have exceeded the"
                             " rate limit and be blocked temporarily")

        _caches_path = options.get('caches_path')
        _single_cache = options.get('single_cache')
        if _caches_path is not None:
            if _single_cache is not None:
                raise ValueError("You can't set both caches_path and"
                                 " single_cache. The caches_path option"
                                 " creates a"
                                 " <caches_path>/<user>/<repo>/"
                                 " structure.")
            self.setCachesPath(_caches_path, flat=False)
        elif _single_cache is not None:
            self.setCachesPath(_single_cache, flat=True)
        else:
            _caches_path = os.path.join(Repo.profile, ".cache",
                                        "enissue")
            self.setCachesPath(_caches_path, flat=False)
        del _caches_path
        del _single_cache

        self.search_results_key = options.get('search_results_key')
        self.page = options.get('page')
        self.c_issue_name_fmt = options['c_issue_name_fmt']
        self.api_repo_url_fmt = options['api_repo_url_fmt']
        self.api_issue_url_fmt = options['api_issue_url_fmt']
        self.api_labels_url_fmt = options['api_labels_url_fmt']
        # ^ All of these are guaranteed not to be None due to
        # "Set it to the default if it is None" further up.
        self.repo_url = self.api_repo_url_fmt.format(
            instance_url=instance_url,
            ru=self.remote_user,
            rn=self.repo_name,
        )
        self.search_issues_url_fmt = \
            options.get('search_issues_url_fmt')
        self.search_issues_url = self.search_issues_url_fmt.format(
            instance_url=instance_url,
            ru=self.remote_user,
            rn=self.repo_name,
        )

        self.api_comments_url_fmt = options['api_comments_url_fmt']
        self.comments_url = self.api_comments_url_fmt.format(
            instance_url=instance_url,
            ru=self.remote_user,
            rn=self.repo_name,
        )

        self.issues_url = self.repo_url + "/issues"
        # self.labels_url = self.repo_url + "/labels"
        self.labels_url = self.api_labels_url_fmt.format(
            instance_url=instance_url,
            ru=self.remote_user,
            rn=self.repo_name,
        )

        self.page_size = options['page_size']
        self.log_prefix = "@ "
        self.c_issues_name_fmt = options['c_issues_name_fmt']

        self.label_ids = []  # all label ids in the repo
        self.labels = []  # all labels in the repo (string only)
        self.label_metas = None
        self.default_query = options['default_query']
        self.hide_events = options['hide_events']
        self.issues = None
        self.last_url = None
        self.options = copy.deepcopy(options)

    def getKnownKey(self, name):
        '''
        Get an API-specific key that matches the given name. The name
        variable will only be considered valid if it exists in
        self.options['known_issue_keys'].

        Sequential arguments:
        name -- a well-known issue key such as 'body' that will be
                translated to an API-specific key.
        '''
        known_issue_keys = self.options.get('known_issue_keys')
        if known_issue_keys is None:
            raise RuntimeError("known_issue_keys shouldn't be None.")
        key = known_issue_keys.get(name)
        if key is None:
            raise KeyError("{} is not a well-known key in"
                           " known_issue_keys. Try _getIssueValue to"
                           " forcefully get a value but only if you"
                           " ran load_issues first--otherwise use"
                           " getKnown.")
        return key

    def _getIssueValue(self, index, key):
        '''
        Sequential arguments:
        index -- an index in self.issues
        key -- a key in self.options['known_issue_keys']
        '''
        return self.issues[index][key]

    def _getKnownAt(self, index, name):
        '''
        Sequential arguments:
        index -- an index in self.issues
        name -- a well-known issue key such as 'body' that will be
                translated to an API-specific key.
        '''
        if self.issues is None:
            raise RuntimeError("You cannot use _getKnownAt when there"
                               " no issues loaded (try getKnown).")
        key = self.getKnownKey(name)
        if key is None:
            raise RuntimeError("getKnownKey should not be None.")
        return self._getIssueValue(index, key)

    def getKnown(self, issue, name):
        '''
        Sequential arguments:
        issue -- a full issue dict such as obtained via get_issue
        name -- a well-known issue key such as 'body' that will be
                translated to an API-specific key.
        '''
        if issue is None:
            raise ValueError("issue is None but must be an issue dict"
                             " such as obtained via get_issue.")
        if not isinstance(issue, dict):
            raise ValueError("issue must be an issue dict such as"
                             " obtained via get_issue.")
        key = self.getKnownKey(name)
        return issue[key]

    def setCachesPath(self, path, flat=True):
        '''
        This repo cache directory will be <remote_user>/<repo_name>/
        unless flat is True, in which case it will be path.

        The repo cache will contain issues/ and potentially other
        directories that mimic the API web URL structure (See
        _get_issues code for subdirectories and files).
        '''
        if self.remote_user is None:
            raise RuntimeError("self.remote_user must be initialized"
                               " before calling self.setCachesPath")
        if path is None:
            raise ValueError("path must not be None")
        self.caches_path = path
        if flat:
            self.c_remote_user_path = self.caches_path
            self.c_repo_path = self.caches_path
        else:
            self.c_remote_user_path = os.path.join(self.caches_path,
                                                   self.remote_user)
            self.c_repo_path = os.path.join(self.c_remote_user_path,
                                            self.repo_name)

    def _get_issues(self, options, query=None, issue_no=None,
                    search_terms=[]):
        '''
        Load the issues matching the query into self.issues, or load
        one issue (len(self.issues) is 1 in that case). Only one or the
        other keyword argument can be specified. This method is used
        for both purposes so that the caching code only has to be
        written once. The cached copy of the issue or result list will
        be loaded if the cache has not expired (unless 'refresh' is
        True in options, then the data will always be from the
        internet).

        This method is used internally by load_issues and the result is
        placed in self.issues.

        The consumer of this method must manually filter by label! The
        page is cached regardless of label(s) because the page is the
        same unless there is a query.

        Sequential arguments:
        options -- This dictionary where all keys are optional may have:
            - 'refresh': Set to True to refresh the cache (load the data
              from the internet and re-save the cached data).
            - 'never_expire': Never download unless 'refresh' is set
              or there is no cache file.
            - 'token': The token such as generated by the web GUI of
              your repo management system mitigates rate limiting to a
              level that is probably not noticeable (5000/hr according
              to GitHub API docs 2021-11-30).


        Keyword arguments:
        query -- Place keys & values in this dictionary directly into
            the query part of the URL.
        issue_no -- Match an exact issue number and convert the
            resulting json object into a list so it behaves like a list
            of matches (containing only 1 though). The query must be
            None when using issue_no or a ValueError is raised.
        search_terms -- Search for each of these terms.

        Returns:
        A 2-long tuple of: (results, error_dict) where error_dict is
        None if there is no error, otherwise contains a 'reason',
        possibly a 'code' (standard website error code), and possibly a
        'url'.

        Raises:
        ValueError if query is not None and issue_no is not None.

        '''
        quiet = options.get('quiet') is True
        debug("get_issues...")
        # debug("  options={}".format(options))
        # ^ By now, options is populated with defaults as well.
        debug("  query={}".format(query))
        if query is not None:
            for k,v in query.items():
                if v is None:
                    raise ValueError("{} is None.".format(k))
        debug("  issue_no={}".format(issue_no))
        debug("  search_terms={}".format(search_terms))
        p = self.log_prefix
        searchTermStr = ""
        if search_terms is None:
            search_terms = []
        for search_term in search_terms:
            searchTermStr += toSubQueryValue(search_term) + "+"
        refresh = options.get('refresh')
        never_expire = options.get('never_expire') is True
        if issue_no is not None:
            if query is not None:
                raise ValueError("You cannot do a query when getting"
                                 " only one issue because a single"
                                 " issue has its own URL with only"
                                 " one result (not a list).")
        url = self.issues_url  # changed below if issue_no
        this_page = 1

        query_part = ""
        and_query_part = ""
        if query is not None:
            '''
            for k,v in query.items():
                if v is not None:
                    # <https://stackoverflow.com/a/9345102/4541104>:
                    #url += (
                    #    "&{}={}".format(quote_plus(k), quote_plus(v))
                    #)
                    #
                    # <https://stackoverflow.com/a/5607708/4541104>:
            '''
            query_part = urlencode(query)  # urlencode takes a dict
            and_query_part = "&" + query_part
            and_query_part += searchTermStr
        elif len(searchTermStr) > 0:
            debug("  searchTermStr=\"{}\"".format(searchTermStr))
            and_query_part = "&" + "q=" + searchTermStr
            # NOTE: using urlencode(searchTermStr) causes
            #  "TypeError: not a valid non-string sequence or mapping
            #  object"
            # - It should already be formed correctly by
            #   toSubQueryValue anyway, so don't filter it here.

        debug("  and_query_part:{}".format(and_query_part))
        if self.page is not None:
            this_page = self.page
        c_issues_name = self.c_issues_name_fmt.format(p=this_page,
                                                      q=and_query_part)

        # echo0("c_issues_name: {}".format(c_issues_name))
        # echo0("query_part: {}".format(query_part))
        if self.c_repo_path is None:
            raise RuntimeError("self.c_repo_path must not be None."
                               " The __init__ method should call"
                               " setCachesPath so this should never"
                               " happen!")
        c_issues_path = os.path.join(self.c_repo_path, c_issues_name)
        make_list = False
        c_path = c_issues_path

        c_issue_name = self.c_issue_name_fmt.format(issue_no=issue_no)
        c_issues_sub_path = os.path.join(self.c_repo_path, "issues")
        results_key = None
        url = None
        if issue_no is not None:
            if not os.path.isdir(c_issues_sub_path):
                os.makedirs(c_issues_sub_path)
            c_issue_path = os.path.join(c_issues_sub_path, c_issue_name)
            c_path = c_issue_path
            make_list = True
            # Change url to the issue url (formerly issue_url):
            url = self.api_issue_url_fmt.format(
                instance_url=self.instance_url,
                ru=self.remote_user,
                rn=self.repo_name,
                issue_no=issue_no,
            )
        else:
            prev_query_s = url
            if len(searchTermStr) > 0:
                url = self.search_issues_url
                results_key = self.search_results_key
                if "?" not in url:
                    url += "?q=" + searchTermStr
                else:
                    url += searchTermStr
                debug("  changing url from {} to {}"
                      "".format(prev_query_s, url))
                debug("  (issues will be set to the content of the {}"
                      " element)".format(results_key))
            # else:
            #     raise ValueError(
            #         "The url is unknown for the action."
            #         " Maybe the code is trying to get labels instead"
            #         " of issues and should call _get_labels."
            #     )
            # else issues list, it seems

        # Labels are NOT in the URL, but filtered later (See docstring).

        if self.page is not None:
            url = self.issues_url + "?page=" + str(self.page)
            url += and_query_part
            debug("  appended page query_part={} (c_path={})"
                  "".format(query_part, c_path))
        elif len(query_part) > 0:
            if url is None:
                url = self.issues_url
                # raise RuntimeError("url is None")
            if query_part is None:
                raise RuntimeError("query_part is None")
            url += "?" + query_part
            debug("  appended custom query_part={} (c_path={})"
                  "".format(query_part, c_path))
        else:
            debug("  There was no custom query.")

        self.last_url = url
        # ^ Differs from self.last_src, which can be a file.

        if os.path.isfile(c_path):
            # See <https://stackoverflow.com/questions/7430928/
            # comparing-dates-to-check-for-old-files>
            max_cache_delta = timedelta(hours=12)
            cache_delta = datetime.now() - max_cache_delta
            c_issues_mtime = os.path.getmtime(c_path)
            filetime = datetime.fromtimestamp(c_issues_mtime)
            is_fresh = filetime > cache_delta
            max_cache_d_s = "{}".format(max_cache_delta)
            expires_s = "{}".format(filetime + max_cache_delta)
            self.last_src = c_path  # Changed later if doesn't return
            if never_expire:
                max_cache_d_s = "never_expire"
                expires_s = "never_expire"
            if (refresh is not True) and (is_fresh or never_expire):
                if not quiet:
                    echo0(p+"Loading cache: \"{}\"".format(c_path))
                debug(p+"Cache time limit: {}".format(max_cache_delta))
                debug(p+"  for URL: {}".format(url))
                if not quiet:
                    echo0(p+"Cache expires: {}".format(expires_s))
                with open(c_path) as json_file:
                    result = json.load(json_file)
                max_issue = None
                results = result
                err = to_error(result)
                if err is not None:
                    echo0("WARNING: a website error was saved"
                          " as an issue, so it will be deleted:"
                          " \"{}\""
                          "".format(c_path))
                    result = None
                    os.remove(c_path)
                    err = None
                elif results_key is not None:
                    if hasattr(results, results_key):
                        debug("  loaded result[{}]"
                              "".format(results_key))
                        results = results[results_key]
                    else:
                        echo0("WARNING: expected {} in dict"
                              "".format(results_key))
                if result is not None:
                    if hasattr(results, 'keys'):
                        debug("  issue not page: converting to list")
                        results = [result]
                    debug(p+"The cache file has"
                          " {} issue(s).".format(len(results)))
                    for issue in results:
                        issue_n = issue.get("number")
                        # debug("issue_n: {}".format(issue_n))
                        if issue_n is not None:
                            if (max_issue is None) or (issue_n > max_issue):
                                max_issue = issue_n
                    if issue_no is None:
                        # Only mention this if more than one issue
                        debug("  The highest cached issue# (this run)"
                              " is {}.".format(max_issue))
                    debug("  returning {} issue(s)".format(len(results)))
                    return results, None
                # else load from URL (See os.remove() above for why)
            else:
                if refresh is True:
                    if not quiet:
                        echo0(p+"Refreshing...".format(max_cache_delta))
                else:
                    if not quiet:
                        echo0(p+"Cache time limit: {}".format(max_cache_delta))
                        echo0(p+"The cache has expired: \"{}\"".format(
                            c_path
                        ))
        else:
            if not quiet:
                echo0(p+"There is no cache for \"{}\"".format(
                    c_path
                ))

        self.last_src = url
        # ^ If didn't return yet, the source is a URL.
        req_is_complex = False
        try:
            debug(p+"Query URL (url): {}".format(url))
            headers = {}
            token = self.options.get('token')
            if token is not None:
                headers['Authorization'] = "token " + token
            if len(headers) > 0:
                req_is_complex = True
                res = requests.get(url, headers=headers)
                # res = req.urlopen(url)
                res_text = res.text
                # NOTE: In python3, res.content is in bytes
                # (<https://stackoverflow.com/a/18810889/4541104>).
            else:
                res = request.urlopen(url)
                res_text = decode_safe(res.read())
        except HTTPError as ex:
            msg = ex.reason
            if ex.code == 410:
                msg = ("The issue was apparently deleted ({})."
                               "".format(ex.reason))
                return (
                    None,
                    {
                        'code': ex.code,
                        'reason': msg,
                        'headers': ex.headers,
                        'url': url,
                    }
                )
            # msg = str(ex) + ": " + self.rateLimitFmt.format(url)
            return (
                None,
                {
                    'code': ex.code,
                    'reason': msg,
                    'headers': ex.headers,
                    'url': url,
                }
            )

        if not os.path.isdir(self.c_repo_path):
            os.makedirs(self.c_repo_path)
        # if not quiet:
        #     echo0(p+"Saving issues cache: {}".format(c_path))
        # with open(c_path, "w") as outs:
        #     outs.write(res_text)
        result = json.loads(res_text)
        err = to_error(result)
        if err is not None:
            return None, err
        with open(c_path, "w") as outs:
            json.dump(result, outs, indent=2)
            debug(p+"Wrote {}".format(c_path))

        if results_key is not None:
            result = result[results_key]

        if make_list:
            # If an issue URL was used, there will be one dict only, so
            # make it into a list.
            results = [result]
        else:
            results = result

        return results, None

    def _get_url(self, url, c_path=None, comment_prefix=""):
        '''
        Keyword arguments:
        c_path -- If not None, save the results as JSON to this path.
        '''
        p = comment_prefix
        self.last_src = url
        try:
            headers = {}
            token = self.options.get('token')
            if token is not None:
                headers['Authorization'] = "token " + token
            if len(headers) > 0:
                res = requests.get(url, headers=headers)
                # res = req.urlopen(url)
                res_text = res.text
                # NOTE: In python3, res.content is in bytes
                # (<https://stackoverflow.com/a/18810889/4541104>).
            else:
                res = request.urlopen(url)
                res_text = decode_safe(res.read())
            if c_path is not None:
                parent = os.path.split(c_path)[0]
                if not os.path.isdir(parent):
                    os.makedirs(parent)
            data = json.loads(res_text)
            err = to_error(data)
            if err is not None:
                return None, err
            # Only save if loads didn't raise an exception.
            if c_path is not None:
                with open(c_path, 'w') as outs:
                    # outs.write(res_text)
                    json.dump(data, outs, indent=2)
                    debug(p+"Wrote {}".format(c_path))
        except HTTPError as ex:
            return (
                None,
                {
                    'code': ex.code,
                    'reason': ex.reason,
                    'headers': ex.headers,
                    'url': url,
                }
            )
        err = to_error(data)
        if err is not None:
            return None, err
        return data, None

    def _get_labels(self, options):
        '''
        Get labels.

        Sequential arguments:
        options -- The following options are checked:
            page -- This is added to the query.
            refresh -- Always re-download the page of results.
            never_expire -- Ignore the age of results and read the
                cache if present instead of downloading data.
        '''
        query_part = ""
        page = options.get('page')
        if page is not None:
            query_part = "?page={}".format(page)
        else:
            debug("* In _get_labels there is no page in"
                  " options.")
        query_url = self.labels_url + query_part
        refresh = False
        if options.get('refresh') is True:
            refresh = True
        never_expire = False
        if options.get('never_expire') is True:
            never_expire = True
        quiet = False
        '''
        debug("* requesting cached URL: {}".format(query_url))
        results, err = self.getCachedJsonDict(
            query_url,
            refresh=refresh,
            never_expire=never_expire,
            quiet=quiet,
        )
        '''
        result, err = self._get_url(query_url, comment_prefix="  * ")
        return result, err

    def getCachedJsonDict(self, url, refresh=False, never_expire=False,
                          quiet=False):
        '''
        Get a cached page, unless the 2nd returned param is not None in
        which case that will contain a standard web response 'code'
        (RFC 2616) number and 'reason' string.

        The cached page is obtained using the cache location
        cache directory specified in options['caches_path'] and further
        narrowed down to self.c_repo_path then narrowed down using the
        URL. For example,
        https://api.github.com/repos/Poikilos/EnlivenMinetest/issues?q=page:1

        should become something like:
        ~/.cache/enissue/Poikilos/EnlivenMinetest/
        which may contain files like "issues_page=1.json"
        and
        ~/.cache/enissue/Poikilos/EnlivenMinetest/

        ...unless options['single_path'] is set: then there will be no
        automatically-created subdirectories (except for the usual
        "issues" and other directories below that one described below).

        https://api.github.com/repos/Poikilos/EnlivenMinetest/issues/515/timeline

        The reactions to a timeline event are from a URL such as:
        https://api.github.com/repos/Poikilos/EnlivenMinetest/issues/comments/968357490/reactions

        This method uses the following options from self.options:
        token -- If set, then the header gets a new line like:
            "Authorization: token ghp_16C7e42F292c6912E7710c838347Ae178B4a"
            where ghp_16C7e42F292c6912E7710c838347Ae178B4a is just an
            example from the GitHub documentation but you must set a
            real token you've generated.

        Keyword arguments:
        quiet -- Set to True to hide messages (verbose mode will
            override this).

        Raises:
        - ValueError: If the issues list itself is tried, it will be
          refused since self.issues_url is known to only show a partial
          list in the GitHub API (denoted by a list that is the same
          length as the max results count). Therefore, this method
          refuses to handle such URLs.
        '''
        if self.options is None:
            raise RuntimeError("You must set options before running"
                               "getCachedJsonDict")
        token = self.options.get('token')
        result = None
        p = self.log_prefix
        # The known API URLs are already set as follows:
        # self.issues_url = self.repo_url + "/issues"
        # self.labels_url = self.repo_url + "/labels"
        shmsg = print
        if quiet:
            shmsg = debug

        c_path = None
        if "?" in url:
            raise NotImplementedError("getCachedJsonDict can't query")
            # If this is implemented, use:
            # c_issues_name_fmt
            # Since even the first page should have "page" or something
            # to denote there are potentially multiple pages.
        '''
        elif url.startswith(self.comments_url):
            # This code is not necessary since it startswith
            # self.issues_url and that case creates any subdirectories
            # necessary such as issues/comments/<#>/reactions
            subUrl = url[len(self.comments_url):]
            if subUrl.startswith("/"):
                subUrl = subUrl[1:]
            if subUrl.endswith("/"):
                if len(subUrl) == 0:
                    raise ValueError("Refusing to cache partial list.")
                subUrl += "index.json"
            if len(subUrl) == 0:
                raise ValueError("Refusing to cache partial list.")
            subParts = subUrl.split("/")
            c_path = os.path.join(self.c_repo_path, "issues")
            for subPart in subParts:
                c_path = os.path.join(c_path, subPart)
            fn = os.path.split(c_path)[1]
            if "." not in fn:
                fn += ".json"
                c_path += ".json"
        '''
        if url.startswith(self.issues_url):
            subUrl = url[len(self.issues_url):]
            if subUrl.startswith("/"):
                subUrl = subUrl[1:]
            if subUrl.endswith("/"):
                if len(subUrl) == 0:
                    raise ValueError("Refusing to cache partial list.")
                subUrl += "index.json"
            if len(subUrl) == 0:
                raise ValueError("Refusing to cache partial list.")
            subParts = subUrl.split("/")
            c_path = os.path.join(self.c_repo_path, "issues")
            for subPart in subParts:
                c_path = os.path.join(c_path, subPart)
            fn = os.path.split(c_path)[1]
            if "." not in fn:
                fn += ".json"
                c_path += ".json"
        elif url.startswith(self.labels_url):
            subUrl = url[len(self.labels_url):]
            if subUrl.startswith("/"):
                subUrl = subUrl[1:]
            if subUrl.endswith("/"):
                if len(subUrl) == 0:
                    raise ValueError(
                        "Refusing to cache partial list (labels url"
                        " {} has no page so the cache page would be"
                        " unmarked and seem to be the whole list but it"
                        " usually isn't due to the web API's page size"
                        " limit."
                        "".format(url)
                    )
                subUrl += "index.json"
            if len(subUrl) == 0:
                raise ValueError(
                    "Refusing to cache partial list (labels url"
                    " {} has no page so the cache page would be"
                    " unmarked and seem to be the whole list but it"
                    " usually isn't due to the web API's page size"
                    " limit."
                    "".format(url)
                )
            subParts = subUrl.split("/")
            c_path = os.path.join(self.c_repo_path, "labels")
            for subPart in subParts:
                c_path = os.path.join(c_path, subPart)
            fn = os.path.split(c_path)[1]
            if "." not in fn:
                fn += ".json"
                c_path += ".json"
        else:
            echo0("url: {}".format(url))
            echo0("self.labels_url: {}".format(self.labels_url))
            echo0("self.issues_url: {}".format(self.issues_url))
            raise NotImplementedError("getCachedJsonDict"
                                      " doesn't have a cache directory"
                                      " for {}. Try --refresh"
                                      " if you changed repos."
                                      "".format(url))

        if os.path.isfile(c_path):
            self.last_src = c_path  # changed later if doesn't return
            # See <https://stackoverflow.com/questions/7430928/
            # comparing-dates-to-check-for-old-files>
            max_cache_delta = timedelta(hours=12)
            cache_delta = datetime.now() - max_cache_delta
            c_issues_mtime = os.path.getmtime(c_path)
            filetime = datetime.fromtimestamp(c_issues_mtime)
            is_fresh = filetime > cache_delta
            max_cache_d_s = "{}".format(max_cache_delta)
            expires_s = "{}".format(filetime + max_cache_delta)
            if never_expire is True:
                max_cache_d_s = "never_expire"
                expires_s = "never_expire"
            if (refresh is not True) and (is_fresh or never_expire):
                shmsg(p+"Loading cache: \"{}\"".format(c_path))
                debug(p+"  for URL: {}".format(url))
                debug(p+"Cache time limit: {}".format(max_cache_d_s))
                shmsg(p+"Cache expires: {}".format(filetime
                                                   + max_cache_delta))
                with open(c_path) as json_file:
                    try:
                        result = json.load(json_file)
                    except json.decoder.JSONDecodeError as ex:
                        echo0("")
                        echo0(p+"The file {} isn't valid JSON"
                              " and will be overwritten if loads"
                              "".format(c_path))
                        result = None
                        # Do NOT set err NOR set to a tuple (A result
                        # of None means it will load from the web
                        # below)!
                err = to_error(result)
                if err is not None:
                    result = None
                    echo0("Error: An error was saved as an issue"
                          " so it will be deleted: {}"
                          "".format(c_path))
                    os.remove(c_path)
        if result is not None:
            return result, None

        result, err = self._get_url(
            url,
            c_path=c_path,
            comment_prefix="  * ",
        )
        return result, err

    def show_issue(self, issue, refresh=False, never_expire=False,
                   quiet=False):
        '''
        Display an issue dictionary as formatted text after getting the
        issue body and other data from the internet. Gather all of the
        additional metadata as well.

        Sequential arguments:
        issue -- Provide a partial issue dict such as from a list result
            page that can be used to identify and obtain the full issue.

        Returns:
        (full_issue_dict, None)
        or
        (full_issue_dict, error_dict) (where error_dict is something
        non-fatal such as missing timeline)
        or
        (None, error_dict)
        where (in both cases) error_dict contains a 'reason' key
        and possibly a 'code' key (standard website error number, or
        else 'code' is not present).
        '''
        p = self.log_prefix
        shmsg = print
        if quiet:
            shmsg = debug

        shmsg("")
        debug("show_issue...")
        shmsg("#{} {}".format(issue["number"], issue["title"]))
        # shmsg(issue["html_url"])
        shmsg("")
        issue_data = issue
        html_url = issue['html_url']
        issue_data, err = self.getCachedJsonDict(
            issue["url"],
            refresh=refresh,
            never_expire=never_expire,
            quiet=quiet,
        )

        if err is not None:
            return None, err

        markdown = issue_data.get("body")
        # ^ It is (always?) present but allowed to be None by GitHub!
        if markdown is not None:
            markdown = markdown.replace("\\r\\n", "\n").replace(
                "\\t",
                "\t"
            )
        left_w = 11
        # ^ left_w must be >=11 or "updated_at:" will push the next col.
        spacer = " "
        line_fmt = "{: <" + str(left_w) + "}" + spacer + "{}"
        shmsg(line_fmt.format("html_url:",  issue["html_url"]))
        shmsg(line_fmt.format("by:",  issue_data["user"]["login"]))
        shmsg(line_fmt.format("state:",  issue_data["state"]))
        assignees = issue_data.get("assignees")
        if (assignees is not None) and len(assignees) > 1:
            assignee_names = [a["login"] for a in assignees]
            shmsg(line_fmt.format("assignees:",
                                  " ".join(assignee_names)))
        elif issue_data.get("assignee") is not None:
            assignee_name = issue_data["assignee"]["login"]
            shmsg(line_fmt.format("assignee:", assignee_name))
        labels_s = "None"
        ll = None
        if issue.get('labels') is not None:
            if issue.get('lower_labels') is None:
                issue['lower_labels'] = []
                for oldL in issue.get('labels'):
                    labelURL = oldL.get('url')
                    if labelURL is not None:
                        lastSlashI = labelURL.rfind('/')
                        if lastSlashI > -1:
                            ll = labelURL[lastSlashI+1:]
                            issue['lower_labels'].append(ll)
            lls = issue.get('lower_labels')
        if (lls is not None) and (len(issue['lower_labels']) > 0):
            neat_labels = []
            for label_s in lls:
                if " " in label_s:
                    neat_labels.append('"' + label_s + '"')
                else:
                    neat_labels.append(label_s)
            labels_s = ", ".join(neat_labels)
        # moved further down: shmsg(line_fmt.format("labels:", labels_s))
        shmsg("")
        if markdown is not None:
            shmsg('"""')
            shmsg(markdown)
            shmsg('"""')
        else:
            shmsg("(no description)")

        comments = issue_data.get("comments")
        if comments is None:
            comments = 0
        if comments > 0:
            shmsg("")
            shmsg("")
            shmsg("({}) comment(s):".format(comments))

        left_margin = "    "
        c_prop_fmt = (left_margin + "{: <" + str(left_w) + "}"
                      + spacer + "{}")
        # ^ Ensure that the second column is justified
        #   (in a Terminal using a monospaced font).

        # NOTE: Timeline is nicer than events because it has both
        #       comments and events.
        '''
        this_evts_json_url = issue_data.get('events_url')
        if this_evts_json_url is not None:
            evts_res = request.urlopen(this_evts_json_url)
            evts_data_s = decode_safe(evts_res.read())
            evts_data = json.loads(evts_data_s)
            # Example:
            # <https://api.github.com/repos/Poikilos/EnlivenMinetest/
            # issues/202/events>
        '''
        this_tmln_json_url = issue_data.get('timeline_url')
        data = []
        msg = None
        if this_tmln_json_url is not None:
            tmln_data, err = self.getCachedJsonDict(
                this_tmln_json_url,
                refresh=refresh,
                quiet=True,
                never_expire=never_expire,
            )
            if err is not None:
                msg = ("Accessing the timeline URL failed: {}"
                       "".format(err.get('reason')))
            # Example:
            # <https://api.github.com/repos/Poikilos/EnlivenMinetest/
            # issues/202/timeline>
            #
            data = tmln_data
        elif comments > 0:
            comments_url = issue_data.get("comments_url")
            if comments_url is None:
                # if self.api_id == "Gitea":
                comments_url = self.api_comments_url_fmt.format(
                    instance_url = self.instance_url,
                    ru=self.remote_user,
                    rn=self.repo_name,
                )
            if comments_url is not None:
                cmts_data, err = self.getCachedJsonDict(
                    comments_url,
                    refresh=refresh,
                    quiet=True,
                    never_expire=never_expire,
                )
                if err is not None:
                    msg = ("Accessing the timeline URL failed: {}"
                           "".format(err.get('reason')))
                    return (
                        issue_data,
                        {
                            'code': err.code,
                            'reason': msg,
                            'headers': err.headers,
                        }
                    )
                data = cmts_data
            else:
                msg = ("WARNING: comments={} but there is no"
                       " comments_url in:"
                       "".format(comments))
                # echo0(msg)
                # echo0(json.dumps(issue_data, indent=4, sort_keys=True))

        for evt in data:
            user = evt.get('user')

            login = None
            if user is not None:
                shmsg("")
                shmsg("")
                login = user.get('login')
            if login is not None:
                shmsg(c_prop_fmt.format("from:", login))
            updated_at = evt.get("updated_at")
            if updated_at is not None:
                shmsg(c_prop_fmt.format("updated_at:",
                                        updated_at))
            body = evt.get("body")
            if body is not None:
                shmsg("")
                shmsg(left_margin + '"""')
                shmsg(left_margin + body)
                shmsg(left_margin + '"""')
                shmsg("")
            rename = evt.get('rename')
            event = evt.get('event')

            ignore_events = ['commented']
            if self.hide_events:
                ignore_events.extend(self.hide_events)
            if event is not None:
                actor = evt.get('actor')
                if actor is not None:
                    login = actor.get('login')
                created_at = evt.get('created_at')
                if event in ignore_events:
                    pass
                elif event == "cross-referenced":
                    source = evt.get('source')
                    source_type = source.get('type')
                    source_issue = source.get('issue')
                    if source_issue is not None:
                        source_number = source_issue.get('number')
                    shmsg(left_margin
                          +"cross-reference: {} referenced this issue"
                          " in {} {}."
                          "".format(login, source_type, source_number))
                elif event == "labeled":
                    label = evt.get('label')
                    if label is not None:
                        label_name = label.get('name')
                        label_color = label.get('color')
                    shmsg(left_margin+"{}: {} by {} {}"
                          "".format(event, label_name, login,
                                    created_at))
                # elif (event == "closed") or (event == "reopened"):
                elif event == "unlabeled":
                    # Example:
                    # <https://api.github.com/repos/Poikilos/
                    # EnlivenMinetest/issues/448/timeline>
                    label = evt.get('label')
                    if label is not None:
                        label_name = label.get('name')
                        label_color = label.get('color')
                    shmsg(left_margin+"{}: {} by {} {}"
                          "".format(event, label_name, login,
                                    created_at))
                else:
                    shmsg(left_margin+"{} {} by {}"
                          "".format(event.upper(), created_at, login))
            if (rename is not None) and ('renamed' not in ignore_events):
                # already said "RENAMED" above (evt.get('event'))
                # shmsg(left_margin+"renamed issue")
                shmsg(left_margin+"  from:{}".format(rename.get('from')))
                shmsg(left_margin+"  to:{}".format(rename.get('to')))

            reactions = evt.get('reactions')
            reactions_url = None
            if reactions is not None:
                reactions_url = reactions.get('url')
            if reactions_url is not None:
                reac_data = None
                debug(p+"  reactions_url: {}".format(reactions_url))
                # Example: <https://api.github.com/repos/Poikilos/
                #   EnlivenMinetest/
                #   issues/comments/968357490/reactions>
                reac_data, err = self.getCachedJsonDict(
                    reactions_url,
                    refresh=refresh,
                    quiet=True,
                    never_expire=never_expire,
                )
                if err is not None:
                    echo0("Accessing the reactions URL failed: {}"
                          "".format(err.get('reason')))
                if reac_data is not None:
                    for reac in reac_data:
                        reac_user = reac.get('user')
                        reac_login = None
                        if reac_user is not None:
                            reac_login = reac_user.get('login')
                        reac_content = reac.get('content')
                        shmsg(left_margin + "- <{}> :{}:"
                              "".format(reac_login, reac_content))
        shmsg("")
        shmsg(left_margin+"labels: {}".format(labels_s))
        closed_by = issue_data.get('closed_by')
        closed_at = issue_data.get('closed_at')
        if (closed_by is not None) or (closed_at is not None):
            # INFO: closed_by may be present even if reopened
            # (determine this by getting 'state').
            # The "REOPENED" and "CLOSED" events also appear in the
            # timeline (see this_tmln_json_url).
            shmsg()
            state = issue_data.get('state')
            if state is None:
                state = options['default_query'].get('state')
            closet_at_str = ""
            if closed_at is not None:
                closet_at_str = " {}".format(closed_at)
            if state != "open":
                closed_by_login = None
                if closed_by is not None:
                    closed_by_login = closed_by.get("login")
                if closed_by_login is not None:
                    shmsg("    (CLOSED{} by {})".format(
                        closet_at_str,
                        closed_by_login
                    ))
                else:
                    shmsg("    (CLOSED{})".format(closet_at_str))
            if state == "open":
                shmsg("    (REOPENED)")
            elif closed_at is None:
                shmsg("    (The closing date is unknown.)")

        shmsg("")
        shmsg("")
        err = None
        if msg is not None:
            err = {
                'reason': msg,
            }
        return issue_data, err

    def load_labels(self, options):  # query=None
        '''
        See _get_labels for documentation.
        '''
        debug("load_labels...")
        results, err = self._get_labels(
            options,
            # query=query,
        )
        if err is None:
            self.label_metas = results
            for label in self.label_metas:
                if label['name'] not in self.labels:
                    self.labels.append(label['name'])

        return results, err

    def load_issues(self, options, query=None, issue_no=None,
                    search_terms=None):
        '''
        See _get_issues for documentation.
        '''
        debug("load_issues...")
        if issue_no is not None:
            if query is not None:
                raise ValueError("You cannot do a query when getting"
                                 " only one issue because a single"
                                 " issue has its own URL with only"
                                 " one result (not a list).")
        results, err = self._get_issues(
            options,
            query=query,
            issue_no=issue_no,
            search_terms=search_terms,
        )
        self.issues = results
        return results, err

    def get_match(self, mode, issue_no=None, match_all_labels_lower=[]):
        '''
        Show a summary of matching issues in list mode or get a single
        issue that will instead by shown by the show_issue method. In
        single issue mode, this method can be skipped since load_issues
        would have placed only one issue in self.issues in that case.

        Sequential arguments:
        mode -- This must be a valid mode
                (a key in the modes dictionary).

        Keyword arguments:
        issue_no -- Match this issue number (None for multiple).
        match_all_labels_lower -- Only match where all of these labels
                                  are on the issue.
        '''
        matching_issue = None
        match_count = 0
        p = self.log_prefix
        # TODO: get labels another way, and make this conditional:
        # if mode == "list":
        for issue in self.issues:
            this_issue_labels_lower = []
            try:
                labels = issue["labels"]
            except KeyError as ex:
                dumpPath = os.path.join(Repo.profile,
                                        "dump-issues.json")
                with open(dumpPath, 'w') as outs:
                    json.dump(self.issues, outs, indent=2)
                    print("Error: dumped self.issues as {}"
                          "".format(dumpPath))
                raise ex
            for label in issue["labels"]:
                self.label_ids.append(label["id"])
                if label["url"].startswith(self.labels_url):
                    start = len(self.labels_url) + 1  # +1 for "/"
                    label_encoded = label["url"][start:]
                    label_s = unquote(label_encoded)
                    this_issue_labels_lower.append(label_s.lower())
                    if label_s not in self.labels:
                        self.labels.append(label_s)
                else:
                    raise ValueError(p+"ERROR: The url '{}' does not"
                                     " start with '{}'. Try refresh"
                                     " if you've changed the"
                                     " repository URL after a cached"
                                     " page was saved"
                                     "".format(label["url"],
                                     self.labels_url))
            if len(match_all_labels) > 0:
                this_issue_match_count = 0
                for try_label in match_all_labels_lower:
                    if try_label in this_issue_labels_lower:
                        this_issue_match_count += 1
                    # else:
                    #     print(p+"{} is not a match ({} is not in"
                    #           " {})".format(issue["number"], try_label,
                    #                         this_issue_labels_lower))
                if this_issue_match_count == len(match_all_labels):
                    match_count += 1
                    print("#{} {}".format(issue["number"], issue["title"]))
            elif (issue_no is None) and (mode == "list"):
                # Show all since no criteria is set.
                match_count += 1
                print("#{} {}".format(issue["number"], issue["title"]))
            if issue_no is not None:
                # INFO: issue_no & issue["number"] are ints
                if issue_no == issue["number"]:
                    matching_issue = issue
                    issue['lower_labels'] = this_issue_labels_lower
        if (mode == 'issue') and (matching_issue is None):
            raise RuntimeError("You must first call load_issues with"
                               " the issue_no option to ensure that"
                               " the single issue is loaded.")
            # TODO: Do not use this method for getting a single issue
            # since the page must be cached or it fails (use improved
            # show_issue method instead).

        return {'issue':matching_issue, 'count':match_count}

    def create_issue(self, src_issue, src_repo):
        '''
        Remotely create a new issue using the web API.

        Sequential arguments:
        src_issue -- The issue dictionary for one issue in the format of
            the src_repo.
        src_repo -- Provide the Repo object that originated the data
            for the purpose of translating the issue format.
        '''
        raise NotImplementedError("create_issue")

    def update_issue(self, src_issue, src_repo):
        '''
        Remotely update an existing issue using the web API.

        Sequential arguments:
        src_issue -- The issue dictionary for one issue in the format of
            the src_repo.
        src_repo -- Provide the Repo object that originated the data
            for the purpose of translating the issue format.
        '''
        raise NotImplementedError("update_issue")

    def get_issue(self, issue_no):
        '''
        Get a tuple of single issue dict and None, or if the second
        value is not None, it is an error dict such as containing
        'reason' and possibly 'code' (standard website error number)
        and possibly 'url'.
        '''
        if self.options is None:
            raise RuntimeError("options is not initialized.")
        results, err = self.load_issues(
            self.options,
            issue_no=issue_no,
        )
        if err is None:
            never_expire = self.options.get('never_expire') is True
            result, err = self.show_issue(
                results[0],
                never_expire=never_expire,
                quiet=True,
            )
            '''
            ^ show_issue gets all of the attached data such as timeline
              (issues/#/timeline.json) and reactions to comments
              (issues/comments/<comment_id>/reactions.json) if present
              online.
            '''
            results = [result]
        if results is None:
            if err is not None:
                if err.get('code') == 410:
                    # echo0("The issue was deleted")
                    pass
                elif err.get('code') == 404:
                    # echo0("The issue doesn't exist")
                    pass
                return None, err
            else:
                msg = ("Unknown error: Results should not be None unless"
                       " there is an error (issue_no={})."
                       "".format(issue_no))
                return (
                    None,
                    {
                        'reason': msg,
                    }
                )
        elif not isinstance(results, list):
            raise RuntimeError("Results must be a list even if there is"
                               " only one result.")
        elif len(results) > 1:
            raise RuntimeError("Results should have"
                               " only one result.")
        issue = results[0]
        '''
        match = self.get_match(
            mode,
            issue_no=issue_no,
            match_all_labels_lower=match_all_labels_lower,
        )
        matching_issue = match['issue']
        if matching_issue is not None:
            self.show_issue(
                matching_issue,
                refresh=False,
                never_expire=self.options.get('never_expire') is True,
            )
        '''
        return issue, None


def main(custom_args=None):
    if custom_args is None:
        custom_args = sys.argv
    global verbose
    mode = None
    prev_arg = None
    issue_no = None
    state = None
    options = {}
    for k,v in default_options.items():
        options[k] = v
    myAppData = os.path.join(Repo.AppDatas, "enissue")
    conf_path = os.path.join(myAppData, "source.conf")
    if os.path.isfile(conf_path):
        modify_dict_by_conf(options, conf_path, always_lower=True,
                            no_file_error=False, quiet=False)
    search_terms = []
    SEARCH_COMMANDS = ['find', 'AND']  # CLI-only commands
    caches_path = None
    logic = {}  # CLI-only values
    save_key = None
    save_option = None
    test_only = False
    assume_values = {
        'never_expire': True,
        'refresh': True,
    }
    collect_options = ['--repo-url', '--never-expire', '--refresh']
    # ^ Repo init data
    # ^ These CLI arguments override default_options. For example:
    #   - repo_url is initially set to default_options['repo_url']
    collect_logic = ['--copy-meta-to', '--db-type', '--db-user',
                     '--db-password', '--cache-base']
    for i in range(1, len(custom_args)):
        arg = custom_args[i]
        isValue = False
        if arg.startswith("#"):
            arg = arg[1:]
        if (mode is None) and (arg in modes.keys()):
            # don't set the command to list unless the enclosing case is
            # true. If a label was specified, paging is handled in the
            # other case.
            parent = modes[arg].get('parent')
            if parent is not None:
                if mode is None:
                    echo0("* setting mode to {} for {}"
                          "".format(parent, mode))
                    mode = parent
                # else the mode is already set explicitly. Example:
                # enissue.py labels page 2
            else:
                mode = arg
        else:
            is_text = False
            try:
                i = int(arg)
                if prev_arg == "page":
                    options['page'] = i
                    isValue = True
                else:
                    if issue_no is not None:
                        usage()
                        echo0("Error: Only one issue number can be"
                              " specified but you also specified"
                              " {}.".format(arg))
                        return 1
                    issue_no = i
                is_text = False
            except ValueError:
                is_text = True
                # It is not a number, so put all other usual code in
                # this area
            if is_text:
                if (mode is None) and (modes.get(arg) is not None):
                    mode = arg
                else:
                    if arg == "--closed":
                        state = 'closed'
                    elif arg == "--test":
                        tests()
                        echo0("All tests passed.")
                        return 0
                    elif arg == "--verbose":
                        verbose = True
                    elif arg == "--debug":
                        verbose = True
                    elif arg == "--help":
                        usage()
                        return 0
                    elif arg in collect_logic:
                        save_key = arg.strip("-").replace("-", "_")
                    elif arg in collect_options:
                        save_option = arg.strip("-").replace("-", "_")
                        assume_value = assume_values.get(save_option)
                        if assume_value is not None:
                            options[save_option] = assume_value
                            save_option = None
                        # else: the next arg will be the value.
                    elif arg.startswith("--"):
                        usage()
                        echo0("Error: The argument \"{}\" is not valid"
                              "".format(arg))
                        return 2
                    elif prev_arg in SEARCH_COMMANDS:
                        search_terms.append(arg)
                        isValue = True
                    elif arg == "find":
                        # echo0("* adding criteria: {}".format(arg))
                        mode = "list"
                    elif (arg == "AND"):
                        # echo0("* adding criteria: {}".format(arg))
                        if len(search_terms) < 1:
                            usage()
                            echo0("You can only specify \"AND\" after"
                                  " the \"find\" command. To literally"
                                  " search for the word \"AND\", place"
                                  " the \"find\" command before it."
                                  " Examples:")
                            for andI in modes['find']['AND_EXAMPLES']:
                                echo0(me
                                      + modes['find']['examples'][andI])
                            return 3
                        mode = "list"
                    elif save_key is not None:
                        logic[save_key] = arg
                        save_key = None
                    elif save_option is not None:
                        options[save_option] = arg
                        save_option = None
                    elif arg != "page":
                        mode = "list"
                        match_all_labels.append(arg)
        prev_arg = arg
        if isValue:
            # It is not a command that will determine meaning for the
            # next var.
            prev_arg = None

    debug("options: {}".format(options))
    repo = Repo(options)

    if mode is None:
        if issue_no is not None:
            mode = "issue"
        elif len(match_all_labels) > 1:
            mode = "list"
        else:
            mode = "list"
            debug("* defaulting to list mode (no command)")
            # raise RuntimeError(
            #     "The command combination is not implemented"
            #     " (The mode couldn't be determined)."
            # )
    if save_key is not None:
        raise ValueError("--{} requires a space then a value."
                         "".format(save_key))
    if save_option is not None:
        raise ValueError("--{} requires a space then a value."
                         "".format(save_option))
    caches_path = logic.get('cache-base')
    valid_modes = ["issue"]
    debug("command metadata: {}".format(logic))
    for k, v in modes.items():
        valid_modes.append(k)

    if mode is None:
        print()
        print()
        usage()
        print()
        print()
        return 0
    elif mode not in valid_modes:
        print()
        print()
        usage()
        print()
        print(mode + " is not a valid command.")
        print()
        print()
        return 0
    elif mode == "list":
        if issue_no is not None:
            print("Error: You must specify either an issue number"
                  " or query criteria, not both.")
            return 4

    echo0("")
    if caches_path is not None:
        repo.setCachesPath(caches_path)
        debug("The cache is now at {}"
              "".format(repo.c_repo_path))
    # echo0("Loading...")

    # TODO: get labels another way, and make this conditional:
    # if mode == "list":
    msg = None

    if mode == "labels":
        debug(" * load_labels...")
        # query = None
        # if repo.default_labels_query is not None:
        #     query = copy.deepcopy(repo.default_labels_query)
        # if options.get('page') is None
        # echo0("* query: {}".format(query))
        results, msg = repo.load_labels(
            options,
            # query=query,
        )
        debug(" * done load_labels")
    elif mode == "issue":
        debug(" * load_issues for single issue...")

        results, msg = repo.load_issues(options, issue_no=issue_no,
                                   search_terms=search_terms)
        debug("* done load_issues for single issue")
    else:
        debug("* load_issues for list...")
        query = None
        if repo.default_query is not None:
            if (state != repo.default_query.get('state')):
                if state is not None:
                    query = {
                        'state': state
                    }
                else:
                    query = copy.deepcopy(repo.default_query)
        results, msg = repo.load_issues(options, query=query,
                                   search_terms=search_terms)
        debug(" * done load_issues for list")
    dstRepoUrl = logic.get('copy-meta-to')
    if dstRepoUrl is not None:
        if mode != "issue":
            raise ValueError("Only rewriting one Gitea issue at a time"
                             " is implemented. Specify a number.")
        db_type = logic.get('db-type')
        if db_type is None:
            db_type = "PostgresQL"
            echo0("WARNING: No db-type was specified, so db-type was"
                  " set to the default: {}".format(db_type))
        db_u = logic.get("db-user")
        if db_u is None:
            db_u = Repo.os_user
            echo0("WARNING: No db-type was specified, so db-user was"
                  " set to the default: {}".format(db_u))
            pass
        db_p = logic.get('db-password')
        is_deleted = False
        if msg is not None:
            if "deleted" in msg:
                is_deleted = True
        if db_p is None:
            echo0("WARNING: No db-password was specified, so the db"
                  " operation will be attempted without it."
                  " Success will depend on your database type and"
                  " settings.")
        dstRepo = Repo({
            'repo_url': dstRepoUrl,
        })
        # echo0("* rewriting Gitea issue {}...".format(issue_no))
        return 5  # TODO: Change based on return of the method.

    if msg is not None:
        echo0(msg)
        if "deleted" in msg:
            return 0
        else:
            return 6
    total_count = 0
    echo0()
    # ^ This blank line goes after "@ Cache" messages and before
    #   the list items or other output.
    if mode == "labels":
        if repo.labels is None:
            print("There were no labels.")
            return 0
    else:
        if repo.issues is None:
            print("There were no issues.")
            return 0

        match_all_labels_lower = []
        p = repo.log_prefix
        for s in match_all_labels:
            debug(p+"appending"
                  " {} to match_all_labels_lower.".format(s.lower()))
            match_all_labels_lower.append(s.lower())

        total_count = len(repo.issues)
        match = repo.get_match(
            mode,
            issue_no=issue_no,
            match_all_labels_lower=match_all_labels_lower,
        )
        matching_issue = match['issue']
        never_expire = options.get('never_expire') is True

        if matching_issue is not None:
            debug("* showing matching_issue...")
            refresh = options.get('refresh') is True
            repo.show_issue(
                matching_issue,
                refresh=False,
                never_expire=never_expire,
            )
            # ^ Never refresh, since that would already have been done.
            state_msg = repo.default_query.get('state')
            if state_msg is None:
                state_msg = repo.last_url
            if state_msg != "open":
                print("(showing {} issue(s))".format(state_msg.upper()))
                # ^ such as CLOSED
        else:
            debug("* There is no matching_issue; matching manually...")
            # TODO: This code doesn't work since it isn't cached.
            if mode == 'issue':
                debug("mode:issue...")
                state = 'closed'
                repo.load_issues(options, query={'state':"closed"},
                                 search_terms=search_terms)
                total_count = len(repo.issues)
                match = repo.get_match(
                    mode,
                    issue_no=issue_no,
                    match_all_labels_lower=match_all_labels_lower,
                )
                matching_issue = match['issue']
            else:
                debug("mode:{}...".format(mode))
        if matching_issue is None:
            if mode == "issue":
                print("")
                # print("mode: {}".format(mode))
                # print("issue_no: {}".format(issue_no))
                # print("match_all_labels_lower: {}"
                #       "".format(match_all_labels_lower))
                print("{}".format(match))
                print("(the issue wasn't visible)")

    if mode == "labels":
        print("Labels:")
        print("")
        total_count = 0
        for label_s in repo.labels:
            total_count += 1
            # print(label_s)
            # Each item in repo.label_metas is formatted like:
            # {'id': 1285230160, 'node_id': 'MDU6TGFiZWwxMjg1MjMwMTYw',
            # 'url': 'https://api.github.com/repos/Poikilos/
            # EnlivenMinetest/labels/
            # 2016-2018%20unconfirmed%20on%20minetest.org',
            # 'name': '2016-2018 unconfirmed on minetest.org',
            # 'color': 'e2a353', 'default': False, 'description': ''}
            # caption = label_s
            print("{}".format(label_s))
        print("")
        print("* got {} label(s)".format(len(repo.labels)))
        print("")
        if total_count >= repo.page_size:
            print("The maximum issue count per page was reached.")
            next_page = 2
            if repo.page is not None:
                next_page = repo.page + 1
            echo0("    ./" + me + " labels page " + str(next_page))
            echo0("to see labels on additional pages.")

    elif mode == "list":
        echo0()
        if len(match_all_labels) > 0:
            if total_count >= repo.page_size:
                print("{} found but only {} searched, which is the"
                      " maximum number per page."
                      "".format(match['count'], total_count))
                next_page = 2
                if repo.page is not None:
                    next_page = repo.page + 1
                echo0("    ./" + me + " " + " ".join(match_all_labels)
                      + " page " + str(next_page))
                echo0("to see additional pages.")

            else:
                pageMsg = "."
                if repo.page is not None:
                    pageMsg = " (There are no more pages)."
                echo0("{} issue(s) matched {}{}".format(
                    match['count'],
                    " + ".join("'{}'".format(s) for s in match_all_labels),
                    pageMsg,
                ))

        else:
            if repo.page is not None:
                echo0("{} issue(s) are showing for page"
                      " {}.".format(match['count'], repo.page))
            else:
                echo0("{} issue(s) are showing.".format(match['count']))
            if total_count >= repo.page_size:
                echo0("That is the maximum number per page. Type")
                next_page = 2
                if repo.page is not None:
                    next_page = repo.page + 1
                echo0("    ./" + me + " page " + str(next_page))
                echo0("to see additional pages.")

        if match['count'] > 0:
            # Note that if a label and issue number are both provided,
            # the mode is still "list".
            if issue_no is not None:
                echo0()
                echo0()
                print("Warning: The issue number was ignored since you"
                      " used an option that lists multiple issues.")
            else:
                echo0()
                echo0()
                echo0("To view details of one of these issues, type")
                echo0("    ./" + me)
                # print("    {}".format(custom_args[0]))
                # ^ Doesn't help: changes to full path including $PATH
                echo0("followed by a number.")
        elif total_count >= repo.page_size:
            echo0("* There were {} matches by the end of the page so"
                  " page {} will appear automatically..."
                  "".format(match['count'], next_page))
            new_args = []
            prevArg = None
            pageDone = False
            for arg in custom_args:
                if prevArg == "page":
                    pageDone = True
                    new_args.append(str(next_page))
                else:
                    new_args.append(arg)
                prevArg = arg
            if not pageDone:
                new_args.append("page")
                new_args.append(str(next_page))
            debug("* constructed new_args {} from {}"
                  "".format(new_args, custom_args))
            ret = main(custom_args=new_args)
            echo0("")
            return ret
    else:
        debug("There is no summary output due to mode={}".format(mode))
    echo0("")
    return 0


if __name__ == "__main__":
    sys.exit(main())
