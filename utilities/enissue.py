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
    from urllib.parse import quote
    from urllib.parse import unquote
except ImportError:
    from urlparse import urlparse
    from urllib import quote
    from urllib import unquote

import urllib


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
                     " Bucket_Game urgent"]
    },
    "labels": {
        "help": ("List all labels (just the labels themselves, not the"
                 " issues)."),
        "examples": [" labels"]
    },
    "page": {
        "help": ("GitHub only lists 30 issues at a time. Type page"
                 " followed by a number to see additional pages."),
        "examples": [" page 2"]
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
            page_size = 30,
            c_issues_name_fmt = "issues_page={p}{q}.json",
        ):
        '''
        Keyword arguments:
        remote_user -- The repo user may be used in api_repo_url_fmt.
        repo_name -- The repo name may be used in api_repo_url_fmt.
        api_repo_url_fmt -- a format string where {ru} is where a repo
                            user goes (if any), and {rn} is where a
                            repo name goes (if any).
        page_size -- This must be set to the page size that is
                     compatible with the URL in api_repo_url_fmt, such
                     as exactly 30 for GitHub.
        c_issues_name_fmt -- This is the format of the URL query tail
                             that shows a certain page by page number,
                             where {p} is the page number and {q} is any
                             additional query such as "&label=bug".
        '''
        self.page = None
        self.remote_user = remote_user
        self.repo_name = repo_name
        self.c_remote_user_path = os.path.join(Repo.caches_path,
                                               self.remote_user)
        self.c_repo_path = os.path.join(self.c_remote_user_path,
                                        self.repo_name)
        self.api_repo_url_fmt = api_repo_url_fmt
        self.repo_url = self.api_repo_url_fmt.format(
            ru=remote_user,
            rn=repo_name
        )
        self.issues_url = self.repo_url + "/issues"
        self.labels_url = self.repo_url + "/labels"
        self.page_size = page_size
        self.log_prefix = "@ "
        self.c_issues_name_fmt = c_issues_name_fmt

        self.label_ids = []  # all label ids in the repo
        self.labels = []  # all labels in the repo

    def get_issues(self):
        query_s = self.issues_url
        this_page = 1

        query_part = ""
        # TODO: IF longer API query is implemented, put something in
        #   query_part like "&label=Bucket_Game"
        if self.page is not None:
            this_page = self.page
        c_issues_name = self.c_issues_name_fmt.format(p=this_page,
                                                      q=query_part)
        c_issues_path = os.path.join(self.c_repo_path, c_issues_name)
        p = self.log_prefix
        if os.path.isfile(c_issues_path):
            # See <https://stackoverflow.com/questions/7430928/
            # comparing-dates-to-check-for-old-files>
            max_cache_delta = timedelta(hours=12)
            cache_delta = datetime.now() - max_cache_delta
            c_issues_mtime = os.path.getmtime(c_issues_path)
            filetime = datetime.fromtimestamp(c_issues_mtime)
            if filetime > cache_delta:
                print(p+"Loading cache: \"{}\"".format(c_issues_path))
                # print(p+"Cache time limit: {}".format(max_cache_delta)
                print(p+"Cache expires: {}".format(filetime
                                                   + max_cache_delta))
                with open(c_issues_path) as json_file:
                    results = json.load(json_file)
                # print(p+"The cache file has"
                #       " {} issue(s).".format(len(results)))
                max_issue = None
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
                print(p+"Cache time limit: {}".format(max_cache_delta))
                print(p+"The cache has expired: \"{}\"".format(
                    c_issues_path
                ))
        else:
            print(p+"There is no cache for \"{}\"".format(
                c_issues_path
            ))

        if self.page is not None:
            query_s = self.issues_url + "?page=" + str(self.page)
        try:
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
        print(p+"Saving issues cache: {}".format(c_issues_path))
        with open(c_issues_path, "w") as outs:
            outs.write(response_s)
        results = json.loads(response_s)
        return results


    def show_issue(self, issue):
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
        left_w = 10
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
        if issue_data["comments"] > 0:
            print("")
            print("")
            print("({}) comment(s):".format(issue_data["comments"]))
            this_cmts_json_url = issue_data["comments_url"]
            response = request.urlopen(this_cmts_json_url)
            cmts_data_s = decode_safe(response.read())
            cmts_data = json.loads(cmts_data_s)
            left_margin = "    "
            c_prop_fmt = (left_margin + "{: <" + str(left_w) + "}"
                          + spacer + "{}")
            for cmt in cmts_data:
                print("")
                print("")
                print(c_prop_fmt.format("from:", cmt["user"]["login"]))
                print(c_prop_fmt.format("updated_at:",
                                        cmt["updated_at"]))
                print("")
                print(left_margin + '"""')
                print(left_margin + cmt["body"])
                print(left_margin + '"""')
                print("")

        print("")
        print("")
        return True

    def load_issues(self):
        self.issues = self.get_issues()

    def get_match(self, mode, match_number=None, match_all_labels_lower=[]):
        '''
        Sequential arguments:
        mode -- This must be a valid mode
                (a key in the modes dictionary).

        Keyword arguments:
        match_number -- Match this issue number (None for multiple).
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
            elif (match_number is None) and (mode == "list"):
                # Show all since no criteria is set.
                match_count += 1
                print("#{} {}".format(issue["number"], issue["title"]))
            if match_number is not None:
                # INFO: match_number & issue["number"] are ints
                if match_number == issue["number"]:
                    matching_issue = issue
                    issue['lower_labels'] = this_issue_labels_lower
        return {'issue':matching_issue, 'count':match_count}


def main():
    mode = None
    repo = Repo()
    prev_arg = None
    match_number = None
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
                    match_number = i
            except ValueError:
                if (mode is None) and (modes.get(arg) is not None):
                    mode = arg
                else:
                    if arg != "page":
                        # print("* adding criteria: {}".format(arg))
                        mode = "list"
                        match_all_labels.append(arg)
        prev_arg = arg
    if mode is None:
        if len(match_all_labels) > 1:
            mode = "list"
        if match_number is not None:
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

    print("")
    # print("Loading...")

    # TODO: get labels another way, and make this conditional:
    # if mode == "list":
    repo.load_issues()
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
        match_number=match_number,
        match_all_labels_lower=match_all_labels_lower,
    )
    matching_issue = match['issue']

    if matching_issue is not None:
        repo.show_issue(matching_issue)

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
            print()
            print()
            print("To view details, type")
            print("    ./" + me)
            print("followed by a number.")
    print("")


if __name__ == "__main__":
    main()
