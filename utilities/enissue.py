#!/usr/bin/env python3
'''
Purpose: View and cache issues in the EnlivenMinetest repo.
Author: 2020-2021 Jake Gustafson
License: See license file at https://github.com/poikilos/EnlivenMinetest

This script caches issues (To
~/.cache/enissue/poikilos/EnlivenMinetest/issues
by default).
'''
from __future__ import print_function
import sys
import json
import os
import platform
from datetime import datetime, timedelta
python_mr = sys.version_info.major
try:
    import urllib.request
    request = urllib.request
except ImportError:
    # python2
    # python_mr = 2
    print("* detected Python " + str(python_mr))
    import urllib2 as urllib
    request = urllib

try:
    from urllib.parse import urlparse
    # from urllib.parse import quote_plus
    from urllib.parse import urlencode
    from urllib.parse import quote
    from urllib.parse import unquote
    from urllib.error import HTTPError
except ImportError:
    # Python 2
    # See <https://docs.python.org/2/howto/urllib2.html>
    from urlparse import urlparse
    # from urlparse import quote_plus
    from urllib import urlencode
    from urllib import quote
    from urllib import unquote
    from urllib2 import HTTPError
    # ^ urllib.error.HTTPError doesn't exist in Python 2



# see <https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python>
def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# https://api.github.com/repos/poikilos/EnlivenMinetest/issues/475/timeline

verbose = False


def debug(msg):
    if verbose:
        error("[debug] " + msg)

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
        "help": "Specify an issue number to see details.",
        "examples": [" 1"]
    },
}
# ^ The parent mode is the actual operating mode whereas the submodes
#   are only for documenting the keywords that apply to the parent mode.
modes["closed"] = modes["open"]

match_all_labels = []


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
    print("Options:")
    print("--cache-base <dir>   Set the directory for cached files.")
    print("--verbose            Enable verbose mode.")
    print("--debug              Enable verbose mode (same as --debug).")


class Repo:
    profile = None
    if platform.system() == "Windows":
        profile = os.environ['USERPROFILE']
    else:
        profile = os.environ['HOME']

    def __init__(
            self,
            remote_user = "poikilos",
            repo_name = "EnlivenMinetest",
            repository_id = "80873867",
            api_repo_url_fmt = "https://api.github.com/repos/{ru}/{rn}",
            api_issue_url_fmt = "{api_url}/issues/{issue_no}",
            search_issues_url_fmt = "https://api.github.com/search/issues?q=repo%3A{ru}/{rn}+",
            search_results_key="items",
            page_size = 30,
            c_issues_name_fmt = "issues_page={p}{q}.json",
            c_issue_name_fmt = "{issue_no}.json",
            default_query = {'state':'open'},
            hide_events = ['renamed', 'assigned'],
            caches_path=None,
            api_comments_url_fmt="{repo_url}/issues/comments",
        ):
        '''
        Keyword arguments:
        remote_user -- The repo user may be used in api_repo_url_fmt.
        repo_name -- The repo name may be used in api_repo_url_fmt.
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
        caches_path -- Store cached json files here: Specifically, in an
            "issues" directory or other directory under the user and
            repo directory. For example, if caches_path is None and uses
            the default ~/.cache/enissue, the numbered json files
            (and numbered folders containing timeline.json or other
            connected data) for issues will appear in
            "~/.cache/enissue/poikilos/EnlivenMinetest/issues". To set
            it later, use the setCachesPath method.
        '''
        self.rateLimitFmt = ("You may be able to view the issues"
                             " at the html_url, and a login may be"
                             " required. The URL \"{}\" is not"
                             " accessible, so you may have exceeded the"
                             " rate limit and be blocked temporarily")
        if caches_path is None:
            caches_path = os.path.join(Repo.profile, ".cache",
                                       "enissue")
        self.remote_user = remote_user
        self.repo_name = repo_name
        self.setCachesPath(caches_path)

        self.search_results_key = search_results_key
        self.page = None
        self.repository_id = repository_id
        self.c_issue_name_fmt = c_issue_name_fmt
        self.api_repo_url_fmt = api_repo_url_fmt
        self.api_issue_url_fmt = api_issue_url_fmt
        self.repo_url = self.api_repo_url_fmt.format(
            ru=remote_user,
            rn=repo_name,
        )
        self.search_issues_url = search_issues_url_fmt.format(
            ru=remote_user,
            rn=repo_name,
        )

        self.api_comments_url_fmt = api_comments_url_fmt
        self.comments_url = api_comments_url_fmt.format(
            repo_url=self.repo_url,
        )

        self.issues_url = self.repo_url + "/issues"
        self.labels_url = self.repo_url + "/labels"
        self.page_size = page_size
        self.log_prefix = "@ "
        self.c_issues_name_fmt = c_issues_name_fmt

        self.label_ids = []  # all label ids in the repo
        self.labels = []  # all labels in the repo
        self.default_query = default_query
        self.hide_events = hide_events
        self.issues = None

    def setCachesPath(self, caches_path):
        '''
        This directory will contain <remote_user>/<repo_name>/
        which will contain issues/ and potentially other directories
        that mimic the API web URL structure (See _get_issues code for
        subdirectories and files).
        '''
        self.caches_path = caches_path
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


        Keyword arguments:
        query -- Place keys & values in this dictionary directly into
            the query part of the URL.
        issue_no -- Match an exact issue number and convert the
            resulting json object into a list so it behaves like a list
            of matches (containing only 1 though). The query must be
            None when using issue_no or a ValueError is raised.
        search_terms -- Search for each of these terms.

        Returns:
        A 2-long tuple of: (results, error string (None if no error)).

        Raises:
        ValueError if query is not None and issue_no is not None.

        '''
        debug("get_issues...")
        debug("  options={}".format(options))
        debug("  query={}".format(query))
        debug("  issue_no={}".format(issue_no))
        debug("  search_terms={}".format(search_terms))
        p = self.log_prefix
        searchTermStr = ""
        if search_terms is None:
            search_terms = []
        for search_term in search_terms:
            searchTermStr += toSubQueryValue(search_term) + "+"
        refresh = options.get('refresh')
        if issue_no is not None:
            if query is not None:
                raise ValueError("You cannot do a query when getting"
                                 " only one issue because a single"
                                 " issue has its own URL with only"
                                 " one result (not a list).")
        query_s = self.issues_url  # changed below if issue_no
        this_page = 1

        query_part = ""
        and_query_part = ""
        if query is not None:
            '''
            for k,v in query.items():
                if v is not None:
                    # <https://stackoverflow.com/a/9345102/4541104>:
                    #query_s += (
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

        # print("c_issues_name: {}".format(c_issues_name))
        # print("query_part: {}".format(query_part))
        c_issues_path = os.path.join(self.c_repo_path, c_issues_name)
        make_list = False
        c_path = c_issues_path

        c_issue_name = self.c_issue_name_fmt.format(issue_no=issue_no)
        c_issues_sub_path = os.path.join(self.c_repo_path, "issues")
        results_key = None
        if issue_no is not None:
            if not os.path.isdir(c_issues_sub_path):
                os.makedirs(c_issues_sub_path)
            c_issue_path = os.path.join(c_issues_sub_path, c_issue_name)
            c_path = c_issue_path
            make_list = True
            # Change query_s to the issue url (formerly issue_url):
            query_s = self.api_issue_url_fmt.format(
                api_url=self.repo_url,
                issue_no=issue_no,
            )
        else:
            prev_query_s = query_s
            if len(searchTermStr) > 0:
                query_s = self.search_issues_url
                results_key = self.search_results_key
                if "?" not in query_s:
                    query_s += "?q=" + searchTermStr
                else:
                    query_s += searchTermStr
                debug("  changing query_s from {} to {}"
                      "".format(prev_query_s, query_s))
                debug("  (issues will be set to the content of the {}"
                      " element)".format(results_key))

        # Labels are NOT in the URL, but filtered later (See docstring).

        if self.page is not None:
            query_s = self.issues_url + "?page=" + str(self.page)
            query_s += and_query_part
            debug("  appended page query_part={} (c_path={})"
                  "".format(query_part, c_path))
        elif len(query_part) > 0:
            query_s += "?" + query_part
            debug("  appended custom query_part={} (c_path={})"
                  "".format(query_part, c_path))
        else:
            debug("  There was no custom query.")


        if os.path.isfile(c_path):
            # See <https://stackoverflow.com/questions/7430928/
            # comparing-dates-to-check-for-old-files>
            max_cache_delta = timedelta(hours=12)
            cache_delta = datetime.now() - max_cache_delta
            c_issues_mtime = os.path.getmtime(c_path)
            filetime = datetime.fromtimestamp(c_issues_mtime)

            if (refresh is not True) and (filetime > cache_delta):
                print(p+"Loading cache: \"{}\"".format(c_path))
                debug(p+"Cache time limit: {}".format(max_cache_delta))
                debug(p+"  for URL: {}".format(query_s))
                print(p+"Cache expires: {}".format(filetime
                                                   + max_cache_delta))
                with open(c_path) as json_file:
                    result = json.load(json_file)
                max_issue = None
                results = result
                if results_key is not None:
                    if hasattr(results, results_key):
                        debug("  loaded result[{}]"
                              "".format(results_key))
                        results = results[results_key]
                    else:
                        error("WARNING: expected {} in dict"
                              "".format(results_key))
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
                print("  The highest cached issue# is {}.".format(
                    max_issue
                ))
                debug("  returning {} issue(s)".format(len(results)))
                return results, None
            else:
                if refresh is True:
                    print(p+"Refreshing...".format(max_cache_delta))
                else:
                    print(p+"Cache time limit: {}".format(max_cache_delta))
                    print(p+"The cache has expired: \"{}\"".format(
                        c_path
                    ))
        else:
            print(p+"There is no cache for \"{}\"".format(
                c_path
            ))

        try:
            debug(p+"Query URL (query_s): {}".format(query_s))
            response = request.urlopen(query_s)
        except HTTPError as e:
            if "Error 410" in str(e):
                return None, "The issue was deleted."
            msg = str(e) + ": " + self.rateLimitFmt.format(query_s)
            return None, msg
        response_s = decode_safe(response.read())
        if not os.path.isdir(self.c_repo_path):
            os.makedirs(self.c_repo_path)
        print(p+"Saving issues cache: {}".format(c_path))
        with open(c_path, "w") as outs:
            outs.write(response_s)
        result = json.loads(response_s)

        if results_key is not None:
            result = result[results_key]

        if make_list:
            # If an issue URL was used, there will be one dict only, so
            # make it into a list.
            results = [result]
        else:
            results = result

        return results, None

    def getCachedJsonDict(self, url, refresh=False, quiet=False):
        '''
        This gets the cached page using the cache location
        cache directory specified in self.caches_path and further
        narrowed down to self.c_repo_path then narrowed down using the
        URL. For example, https://api.github.com/repos/poikilos/EnlivenMinetest/issues?q=page:1

        should become something like:
        ~/.cache/enissue/poikilos/EnlivenMinetest/
        which may contain files like "issues_page=1.json"
        and
        ~/.cache/enissue/poikilos/EnlivenMinetest/

        https://api.github.com/repos/poikilos/EnlivenMinetest/issues/515/timeline

        The reactions to a timeline event are from a URL such as:
        https://api.github.com/repos/poikilos/EnlivenMinetest/issues/comments/968357490/reactions

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
                    raise ValueError("Refusing to cache partial list.")
                subUrl += "index.json"
            if len(subUrl) == 0:
                raise ValueError("Refusing to cache partial list.")
            subParts = subUrl.split("/")
            c_path = os.path.join(self.c_repo_path, "labels")
            for subPart in subParts:
                c_path = os.path.join(c_path, subPart)
            fn = os.path.split(c_path)[1]
            if "." not in fn:
                fn += ".json"
                c_path += ".json"
        else:
            raise NotImplementedError("getCachedJsonDict doesn't"
                                      " have a cache directory for"
                                      " {}".format(url))

        if os.path.isfile(c_path):
            # See <https://stackoverflow.com/questions/7430928/
            # comparing-dates-to-check-for-old-files>
            max_cache_delta = timedelta(hours=12)
            cache_delta = datetime.now() - max_cache_delta
            c_issues_mtime = os.path.getmtime(c_path)
            filetime = datetime.fromtimestamp(c_issues_mtime)

            if (refresh is not True) and (filetime > cache_delta):
                shmsg(p+"Loading cache: \"{}\"".format(c_path))
                debug(p+"  for URL: {}".format(url))
                debug(p+"Cache time limit: {}".format(max_cache_delta))
                shmsg(p+"Cache expires: {}".format(filetime
                                                   + max_cache_delta))
                with open(c_path) as json_file:
                    try:
                        result = json.load(json_file)
                    except json.decoder.JSONDecodeError as ex:
                        error("")
                        error(p+"The file {} isn't valid JSON"
                              " and will be overwritten if loads"
                              "".format(c_path))
                        result = None
        if result is not None:
            return result

        res = request.urlopen(url)
        data_s = decode_safe(res.read())
        parent = os.path.split(c_path)[0]
        if not os.path.isdir(parent):
            os.makedirs(parent)
        data = json.loads(data_s)
        # Only save if loads didn't raise an exception.
        with open(c_path, 'w') as outs:
            outs.write(data_s)
            debug(p+"Wrote {}".format(c_path))

        return data


    def show_issue(self, issue, refresh=False):
        '''
        Display an issue dictionary as formatted text after getting the
        issue body and other data from the internet. Gather all of the
        additional metadata as well.
        '''
        p = self.log_prefix
        print("")
        debug("show_issue...")
        print("#{} {}".format(issue["number"], issue["title"]))
        # print(issue["html_url"])
        print("")
        issue_data = issue
        html_url = issue['html_url']
        if refresh:
            issue_data = self.getCachedJsonDict(issue["url"],
                                                refresh=refresh)
            '''
            this_issue_json_url = issue["url"]
            issue_data_bytes = None
            try:
                response = request.urlopen(this_issue_json_url)
                issue_data_bytes = response.read()
            except HTTPError as e:
                print(str(e))
                print(p+self.rateLimitFmt.format(this_issue_json_url))
                html_url = issue.get("html_url")
                print(p+"You may be able to view the issue on GitHub")
                print(p+"at the 'html_url', and a login may be required:")
                print(p+"html_url: {}".format(html_url))
                return False
            issue_data_s = decode_safe(issue_data_bytes)
            issue_data = json.loads(issue_data_s)
            '''

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
        print(line_fmt.format("html_url:",  issue["html_url"]))
        print(line_fmt.format("by:",  issue_data["user"]["login"]))
        print(line_fmt.format("state:",  issue_data["state"]))
        assignees = issue_data.get("assignees")
        if (assignees is not None) and len(assignees) > 1:
            assignee_names = [a["login"] for a in assignees]
            print(line_fmt.format("assignees:",
                                  " ".join(assignee_names)))
        elif issue_data.get("assignee") is not None:
            assignee_name = issue_data["assignee"]["login"]
            print(line_fmt.format("assignee:", assignee_name))
        labels_s = "None"
        if len(issue['lower_labels']) > 0:
            neat_labels = []
            for label_s in issue['lower_labels']:
                if " " in label_s:
                    neat_labels.append('"' + label_s + '"')
                else:
                    neat_labels.append(label_s)
            labels_s = ", ".join(neat_labels)
        print(line_fmt.format("labels:", labels_s))
        print("")
        if markdown is not None:
            print('"""')
            print(markdown)
            print('"""')
        else:
            print("(no description)")

        comments = issue_data.get("comments")
        if comments is None:
            comments = 0
        if comments > 0:
            print("")
            print("")
            print("({}) comment(s):".format(comments))

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
            # <https://api.github.com/repos/poikilos/EnlivenMinetest/
            # issues/202/events>
        '''
        this_tmln_json_url = issue_data.get('timeline_url')
        data = []
        if this_tmln_json_url is not None:
            tmln_data = self.getCachedJsonDict(
                this_tmln_json_url,
                refresh=refresh,
                quiet=True,
            )
            # Example:
            # <https://api.github.com/repos/poikilos/EnlivenMinetest/
            # issues/202/timeline>
            #
            data = tmln_data
        elif comments > 0:
            cmts_data = self.getCachedJsonDict(
                issue_data["comments_url"],
                refresh=refresh,
            )
            data = cmts_data

        for evt in data:
            user = evt.get('user')

            login = None
            if user is not None:
                print("")
                print("")
                login = user.get('login')
            if login is not None:
                print(c_prop_fmt.format("from:", login))
            updated_at = evt.get("updated_at")
            if updated_at is not None:
                print(c_prop_fmt.format("updated_at:",
                                        updated_at))
            body = evt.get("body")
            if body is not None:
                print("")
                print(left_margin + '"""')
                print(left_margin + body)
                print(left_margin + '"""')
                print("")
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
                    print(left_margin
                          +"cross-reference: {} referenced this issue"
                          " in {} {}."
                          "".format(login, source_type, source_number))
                elif event == "labeled":
                    label = evt.get('label')
                    if label is not None:
                        label_name = label.get('name')
                        label_color = label.get('color')
                    print(left_margin+"{}: {} by {} {}"
                          "".format(event, label_name, login,
                                    created_at))
                # elif (event == "closed") or (event == "reopened"):
                elif event == "unlabeled":
                    # Example:
                    # <https://api.github.com/repos/poikilos/
                    # EnlivenMinetest/issues/448/timeline>
                    label = evt.get('label')
                    if label is not None:
                        label_name = label.get('name')
                        label_color = label.get('color')
                    print(left_margin+"{}: {} by {} {}"
                          "".format(event, label_name, login,
                                    created_at))
                else:
                    print(left_margin+"{} {} by {}"
                          "".format(event.upper(), created_at, login))
            if (rename is not None) and ('renamed' not in ignore_events):
                # already said "RENAMED" above (evt.get('event'))
                # print(left_margin+"renamed issue")
                print(left_margin+"  from:{}".format(rename.get('from')))
                print(left_margin+"  to:{}".format(rename.get('to')))

            reactions = evt.get('reactions')
            reactions_url = None
            if reactions is not None:
                reactions_url = reactions.get('url')
            if reactions_url is not None:
                reac_data = None
                try:
                    debug(p+"  reactions_url: {}".format(reactions_url))
                    # Example: <https://api.github.com/repos/poikilos/
                    #   EnlivenMinetest/
                    #   issues/comments/968357490/reactions>
                    reac_data = self.getCachedJsonDict(
                        reactions_url,
                        refresh=refresh,
                        quiet=True,
                    )
                    '''
                    reactions_res = request.urlopen(reactions_url)
                    reac_data_s = decode_safe(reactions_res.read())
                    reac_data = json.loads(reac_data_s)
                    '''
                    # print(left_margin + "downloaded " + reactions_url)
                    for reac in reac_data:
                        reac_user = reac.get('user')
                        reac_login = None
                        if reac_user is not None:
                            reac_login = reac_user.get('login')
                        reac_content = reac.get('content')
                        print(left_margin + "- <{}> :{}:"
                              "".format(reac_login, reac_content))
                except HTTPError as e:
                    print(left_margin + "Error downloading {}:"
                          "".format(reactions_url))
                    print(left_margin + str(e))
                    print(left_margin + "{}".format(reac_data))

        closed_by = issue_data.get('closed_by')
        closed_at = issue_data.get('closed_at')
        if (closed_by is not None) or (closed_at is not None):
            # INFO: closed_by may be present even if reopened
            # (determine this by getting 'state').
            # The "REOPENED" and "CLOSED" events also appear in the
            # timeline (see this_tmln_json_url).
            print()
            state = issue_data.get('state')
            closet_at_str = ""
            if closed_at is not None:
                closet_at_str = " {}".format(closed_at)
            if state != "open":
                closed_by_login = closed_by.get("login")
                if closed_by_login is not None:
                    print("    (CLOSED{} by {})".format(
                        closet_at_str,
                        closed_by_login
                    ))
                else:
                    print("    (CLOSED{})".format(closet_at_str))
            if state == "open":
                print("    (REOPENED)")
            elif closed_at is None:
                print("    (The closing date is unknown.)")

        print("")
        print("")
        return True

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
        results, msg = self._get_issues(
            options,
            query=query,
            issue_no=issue_no,
            search_terms=search_terms,
        )
        self.issues = results
        return results, msg

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
                                     " start with '{}'"
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


def main():
    global verbose
    mode = None
    repo = Repo()
    prev_arg = None
    issue_no = None
    state = repo.default_query.get('state')
    options = {}
    search_terms = []
    SEARCH_COMMANDS = ['find', 'AND']
    caches_path = None
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        isValue = False
        if arg.startswith("#"):
            arg = arg[1:]
        if (mode is None) and (arg in modes.keys()):
            # don't set the command to list unless the enclosing case is
            # true. If a label was specified, paging is handled in the
            # other case.
            parent = modes[arg].get('parent')
            if parent is not None:
                mode = parent
            else:
                mode = arg
        else:
            is_text = False
            try:
                i = int(arg)
                if prev_arg == "page":
                    repo.page = i
                    isValue = True
                else:
                    if issue_no is not None:
                        usage()
                        error("Error: Only one issue number can be"
                              " specified but you also specified"
                              " {}.".format(arg))
                        exit(1)
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
                    elif arg == "--refresh":
                        options['refresh'] = True
                    elif arg == "--verbose":
                        verbose = True
                    elif arg == "--debug":
                        verbose = True
                    elif arg == "--help":
                        usage()
                        exit(0)
                    elif arg == "--cache-base":
                        pass
                        # options['caches_path'] = None
                    elif arg.startswith("--"):
                        usage()
                        error("Error: The argument \"{}\" is not valid"
                              "".format(arg))
                        exit(1)
                    elif prev_arg in SEARCH_COMMANDS:
                        search_terms.append(arg)
                        isValue = True
                    elif prev_arg == "--cache-base":
                        caches_path = arg
                    elif arg == "find":
                        # print("* adding criteria: {}".format(arg))
                        mode = "list"
                    elif (arg == "AND"):
                        # print("* adding criteria: {}".format(arg))
                        if len(search_terms) < 1:
                            usage()
                            error("You can only specify \"AND\" after"
                                  " the \"find\" command. To literally"
                                  " search for the word \"AND\", place"
                                  " the \"find\" command before it."
                                  " Examples:")
                            for andI in modes['find']['AND_EXAMPLES']:
                                error(me
                                      + modes['find']['examples'][andI])
                            exit(1)
                        mode = "list"
                    elif arg != "page":
                        mode = "list"
                        match_all_labels.append(arg)
        prev_arg = arg
        if isValue:
            # It is not a command that will determine meaning for the
            # next var.
            prev_arg = None
    if mode is None:
        if len(match_all_labels) > 1:
            mode = "list"
        if issue_no is not None:
            mode = "issue"

    valid_modes = ["issue"]
    for k, v in modes.items():
        valid_modes.append(k)

    if mode is None:
        print()
        print()
        usage()
        print()
        print()
        sys.exit(0)
    elif mode not in valid_modes:
        print()
        print()
        usage()
        print()
        print(mode + " is not a valid command.")
        print()
        print()
        sys.exit(0)
    elif mode == "list":
        if issue_no is not None:
            print("Error: You must specify either an issue number"
                  " or query criteria, not both.")
            sys.exit(1)

    print("")
    if caches_path is not None:
        repo.setCachesPath(caches_path)
        debug("The cache is now at {}"
              "".format(repo.c_repo_path))
    # print("Loading...")

    # TODO: get labels another way, and make this conditional:
    # if mode == "list":
    msg = None
    if (mode != "issue") and (state != repo.default_query.get('state')):
        query = {
            'state': state
        }
        results, msg = repo.load_issues(options, query=query,
                                   search_terms=search_terms)
        debug("* done load_issues for list")
    else:
        results, msg = repo.load_issues(options, issue_no=issue_no,
                                   search_terms=search_terms)
        debug("* done load_issues for single issue")
    if msg is not None:
        error(msg)
        if "deleted" in msg:
            sys.exit(0)
        else:
            sys.exit(1)

    if repo.issues is None:
        print("There were no issues.")
        sys.exit(0)

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

    if matching_issue is not None:
        debug("* showing matching_issue...")
        refresh = options.get('refresh') is True
        repo.show_issue(
            matching_issue,
            refresh=False,
        )
        # ^ Never refresh, since that would already have been done.
        if state != "open":
            print("(showing {} issue(s))".format(state.upper()))
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
        # print("Labels:")
        # print("")
        for label_s in repo.labels:
            print(label_s)
        print("")
        print("The repo has {} label(s).".format(len(repo.labels)))
        print("")
        if total_count >= repo.page_size:
            print("The maximum issue count per page was reached.")
            next_page = 2
            if repo.page is not None:
                next_page = repo.page + 1
            print("    ./" + me + " labels page " + str(next_page))
            print("to see labels on additional pages.")


    elif mode == "list":
        print()
        if len(match_all_labels) > 0:
            print("{} issue(s) matched {}".format(
                match['count'],
                " + ".join("'{}'".format(s) for s in match_all_labels)
            ))
            if total_count >= repo.page_size:
                print("{} searched, which is the maximum number"
                      " per page.".format(total_count))
                next_page = 2
                if repo.page is not None:
                    next_page = repo.page + 1
                print("    ./" + me + " " + " ".join(match_all_labels)
                      + " page " + str(next_page))
                print("to see additional pages.")

        else:
            if repo.page is not None:
                print("{} issue(s) are showing for page"
                      " {}.".format(match['count'], repo.page))
            else:
                print("{} issue(s) are showing.".format(match['count']))
            if total_count >= repo.page_size:
                print("That is the maximum number per page. Type")
                next_page = 2
                if repo.page is not None:
                    next_page = repo.page + 1
                print("    ./" + me + " page " + str(next_page))
                print("to see additional pages.")
        if match['count'] > 0:
            # Note that if a label and issue number are both provided,
            # the mode is still "list".
            if issue_no is not None:
                print()
                print()
                print("Warning: The issue number was ignored since you"
                      " used an option that lists multiple issues.")
            else:
                print()
                print()
                print("To view details, type")
                print("    ./" + me)
                print("followed by a number.")
    else:
        debug("There is no summary output due to mode={}".format(mode))
    print("")


if __name__ == "__main__":
    main()
