#!/usr/bin/env python3
from __future__ import print_function
import sys
import json
import os
from datetime import datetime, timedelta

try:
    import urllib.request
    request = urllib.request
except ImportError:
    # python2
    python_mr = 2
    import urllib2 as urllib
    request = urllib

try:
    from urllib.parse import urlparse
    # from urllib.parse import quote_plus
    from urllib.parse import urlencode
    from urllib.parse import quote
    from urllib.parse import unquote
except ImportError:
    # Python 2
    from urlparse import urlparse
    # from urlparse import quote_plus
    from urllib import urlencode
    from urllib import quote
    from urllib import unquote

import urllib


def error(msg):
    sys.stderr.write("{}\n".format(msg))
    sys.stderr.flush()

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
                 " not case sensitive."),
        "examples": ["list", " list Bucket_Game",
                     " list Bucket_Game urgent", " Bucket_Game",
                     " Bucket_Game urgent", " Bucket_Game --closed"]
    },
    "labels": {
        "help": ("List all labels (just the labels themselves, not the"
                 " issues)."),
        "examples": [" labels"]
    },
    "page": {
        "help": ("GitHub only lists 30 issues at a time. Type page"
                 " followed by a number to see additional pages."),
        "examples": [" page 2", " page 2 --closed"]
    },
    "<#>": {
        "help": "Specify an issue number to see details.",
        "examples": [" 1"]
    }
}
match_all_labels = []


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


class Repo:

    caches_path = "/tmp/enissue"

    def __init__(
            self,
            remote_user = "poikilos",
            repo_name = "EnlivenMinetest",
            api_repo_url_fmt = "https://api.github.com/repos/{ru}/{rn}",
            api_issue_url_fmt = "{api_url}/issues/{issue_no}",
            page_size = 30,
            c_issues_name_fmt = "issues_page={p}{q}.json",
            c_issue_name_fmt = "issues_{issue_no}.json",
            default_query = {'state':'open'},
            hide_events = ['renamed', 'assigned'],
        ):
        '''
        Keyword arguments:
        remote_user -- The repo user may be used in api_repo_url_fmt.
        repo_name -- The repo name may be used in api_repo_url_fmt.
        api_repo_url_fmt -- a format string where {ru} is where a repo
                            user goes, and {rn} is where a
                            repo name goes.
        api_issue_url_fmt -- a format string where {issue_url} is
                             determined by api_repo_url_fmt and
                             {issue_no} is where an issue number goes.
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
        '''
        self.page = None
        self.remote_user = remote_user
        self.repo_name = repo_name
        self.c_remote_user_path = os.path.join(Repo.caches_path,
                                               self.remote_user)
        self.c_repo_path = os.path.join(self.c_remote_user_path,
                                        self.repo_name)
        self.c_issue_name_fmt = c_issue_name_fmt
        self.api_repo_url_fmt = api_repo_url_fmt
        self.api_issue_url_fmt = api_issue_url_fmt
        self.repo_url = self.api_repo_url_fmt.format(
            ru=remote_user,
            rn=repo_name,
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

    def _get_issues(self, options, query=None, issue_no=None):
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

        Sequential arguments:
        options -- This dictionary where all keys are optional may have:
        - 'refresh': Set to True to refresh the cache (load the data
          from the internet and re-save the cached data).

        Keyword arguments:
        query -- Place keys & values in this dictionary directly into
                 the query part of the URL.
        issue_no -- Match an exact issue number and convert the
                    resulting json object into a list so it behaves
                    like a list of matches (containing only 1
                    though). The query must be None when using
                    issue_no or a ValueError is raised.



        Keyword arguments:
        query -- Use keys & values in this dictionary to the URL query.
        issue_no -- Load only this issue (not compatible with query).

        Raises:
        ValueError if query is not None and issue_no is not None.

        '''
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
            query_part = urlencode(query)
            and_query_part = "&" + query_part

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

        p = self.log_prefix
        if os.path.isfile(c_path):
            # See <https://stackoverflow.com/questions/7430928/
            # comparing-dates-to-check-for-old-files>
            max_cache_delta = timedelta(hours=12)
            cache_delta = datetime.now() - max_cache_delta
            c_issues_mtime = os.path.getmtime(c_path)
            filetime = datetime.fromtimestamp(c_issues_mtime)

            if (refresh is not True) and (filetime > cache_delta):
                print(p+"Loading cache: \"{}\"".format(c_path))
                # print(p+"Cache time limit: {}".format(max_cache_delta)
                print(p+"Cache expires: {}".format(filetime
                                                   + max_cache_delta))
                with open(c_path) as json_file:
                    result = json.load(json_file)
                # print(p+"The cache file has"
                #       " {} issue(s).".format(len(results)))
                max_issue = None
                results = result
                if hasattr(results, 'keys'):
                    # It is an issue not a page, so convert to list:
                    results = [result]
                for issue in results:
                    issue_n = issue.get("number")
                    if issue_n is not None:
                        if (max_issue is None) or (issue_n > max_issue):
                            max_issue = issue_n
                print(p+"The highest cached issue# is {}.".format(
                    max_issue
                ))
                return results
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

        if self.page is not None:
            query_s = self.issues_url + "?page=" + str(self.page)
            query_s += and_query_part
        elif len(query_part) > 0:
            query_s += "?" + query_part
        try:
            debug(p+"Query URL (query_s): {}".format(query_s))
            response = request.urlopen(query_s)
        except urllib.error.HTTPError as e:
            print(p+"You may be able to view the issues on GitHub")
            print(p+"at the 'html_url', and a login may be required.")
            print(p+"The URL \"{}\" is not accessible, so you may have"
                  " exceeded the rate limit and be blocked"
                  " temporarily:".format(query_s))
            print(str(e))
            return None
        response_s = decode_safe(response.read())
        if not os.path.isdir(self.c_repo_path):
            os.makedirs(self.c_repo_path)
        print(p+"Saving issues cache: {}".format(c_path))
        with open(c_path, "w") as outs:
            outs.write(response_s)
        result = json.loads(response_s)
        if make_list:
            # If an issue URL was used, there will be one dict only, so
            # make it into a list.
            results = [result]
        else:
            results = result
        return results


    def show_issue(self, issue):
        '''
        Display an issue dictionary as formatted text after getting the
        issue body and other data from the internet.
        '''
        p = self.log_prefix
        print("")
        print("#{} {}".format(issue["number"], issue["title"]))
        # print(issue["html_url"])
        print("")
        this_issue_json_url = issue["url"]
        issue_data_bytes = None
        try:
            response = request.urlopen(this_issue_json_url)
            issue_data_bytes = response.read()
        except urllib.error.HTTPError as e:
            print(str(e))
            print(p+"The URL \"{}\" is not accessible, so you may have"
                  " exceeded the rate limit and be blocked"
                  " temporarily:".format(this_issue_json_url))
            html_url = issue.get("html_url")
            print(p+"You may be able to view the issue on GitHub")
            print(p+"at the 'html_url', and a login may be required:")
            print(p+"html_url: {}".format(html_url))
            return False
        issue_data_s = decode_safe(issue_data_bytes)
        issue_data = json.loads(issue_data_s)
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
            tmln_res = request.urlopen(this_tmln_json_url)
            tmln_data_s = decode_safe(tmln_res.read())
            tmln_data = json.loads(tmln_data_s)
            # Example:
            # <https://api.github.com/repos/poikilos/EnlivenMinetest/
            # issues/202/timeline>
            #
            data = tmln_data
        elif comments > 0:
            this_cmts_json_url = issue_data["comments_url"]
            response = request.urlopen(this_cmts_json_url)
            cmts_data_s = decode_safe(response.read())
            cmts_data = json.loads(cmts_data_s)
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

    def load_issues(self, options, query=None, issue_no=None):
        '''
        See _get_issues for documentation.
        '''
        if issue_no is not None:
            if query is not None:
                raise ValueError("You cannot do a query when getting"
                                 " only one issue because a single"
                                 " issue has its own URL with only"
                                 " one result (not a list).")
        self.issues = self._get_issues(
            options,
            query=query,
            issue_no=issue_no,
        )

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
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg.startswith("#"):
            arg = arg[1:]
        if (mode is None) and (arg in modes.keys()):
            # don't set the command to list unless the enclosing case is
            # true. If a label was specified, paging is handled in the
            # other case.
            if arg == "page":
                mode = "list"
            else:
                mode = arg
        else:
            try:
                i = int(arg)
                if prev_arg == "page":
                    repo.page = i
                else:
                    if issue_no is not None:
                        usage()
                        error("Error: Only one issue number can be"
                              " specified but you also specified"
                              " {}.".format(arg))
                        exit(1)
                    issue_no = i
            except ValueError:
                if (mode is None) and (modes.get(arg) is not None):
                    mode = arg
                else:
                    if arg == "--closed":
                        state = 'closed'
                    elif arg == "--refresh":
                        options['refresh'] = True
                    elif arg == "--verbose":
                        verbose = True
                    elif arg == "--help":
                        usage()
                        exit(0)
                    elif arg.startswith("--"):
                        usage()
                        error("Error: The argument \"{}\" is not valid"
                              "".format(arg))
                        exit(1)
                    elif arg != "page":
                        # print("* adding criteria: {}".format(arg))
                        mode = "list"
                        match_all_labels.append(arg)
        prev_arg = arg
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
    # print("Loading...")

    # TODO: get labels another way, and make this conditional:
    # if mode == "list":
    if (mode != "issue") and (state != repo.default_query.get('state')):
        query = {
            'state': state
        }
        repo.load_issues(options, query=query)
    else:
        repo.load_issues(options, issue_no=issue_no)

    if repo.issues is None:
        print("There were no issues.")
        sys.exit(0)

    match_all_labels_lower = []
    p = repo.log_prefix
    for s in match_all_labels:
        # print(p+"appending"
        #       " {} to match_all_labels_lower.".format(s.lower()))
        match_all_labels_lower.append(s.lower())

    total_count = len(repo.issues)
    match = repo.get_match(
        mode,
        issue_no=issue_no,
        match_all_labels_lower=match_all_labels_lower,
    )
    matching_issue = match['issue']

    if matching_issue is not None:
        repo.show_issue(matching_issue)
        if state != "open":
            print("(showing {} issue(s))".format(state.upper()))
            # ^ such as CLOSED
    else:
        # TODO: This code doesn't work since it isn't cached.
        if mode == 'issue':
            state = 'closed'
            repo.load_issues(options, query={'state':"closed"})
            total_count = len(repo.issues)
            match = repo.get_match(
                mode,
                issue_no=issue_no,
                match_all_labels_lower=match_all_labels_lower,
            )
            matching_issue = match['issue']
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
    print("")


if __name__ == "__main__":
    main()
