#!/usr/bin/env python3
from __future__ import print_function
import sys
import json
import os
from datetime import datetime, timedelta

try:
    import urllib.request
    request = urllib.request
except:
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

cmd = None
# me = sys.argv[0]
me = os.path.basename(__file__)
cmds = {
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
    for name, command in cmds.items():
        hlp = command["help"]
        print(line_fmt.format(name, hlp))
        if len(command["examples"]) > 0:
            print(" "*(left_w+len(spacer)) + "Examples:")
            for s in command["examples"]:
                print(" "*(left_w+len(spacer)+2) + "./" + me + s)
        print("")
        print("")

page = None
prev_arg = None
match_number = None
for i in range(1, len(sys.argv)):
    arg = sys.argv[i]
    if arg.startswith("#"):
        arg = arg[1:]
    if (cmd is None) and (arg in cmds.keys()):
        # don't set the command to list unless the enclosing case is
        # true. If a label was specified, paging is handled in the
        # other case.
        if arg == "page":
            cmd = "list"
        else:
            cmd = arg
    else:
        try:
            i = int(arg)
            if prev_arg == "page":
                page = i
            else:
                match_number = i
        except ValueError:
            if (cmd is None) and (cmds.get(arg) is not None):
                cmd = arg
            else:
                if arg != "page":
                    print("* adding criteria: {}".format(arg))
                    cmd = "list"
                    match_all_labels.append(arg)
    prev_arg = arg
if cmd is None:
    if len(match_all_labels) > 1:
        cmd = "list"
    if match_number is not None:
        cmd = "issue"
valid_cmds = ["issue"]
for k, v in cmds.items():
    valid_cmds.append(k)

if cmd is None:
    print()
    print()
    usage()
    print()
    print()
    exit(0)
elif cmd not in valid_cmds:
    print()
    print()
    usage()
    print()
    print(cmd + " is not a valid command.")
    print()
    print()
    exit(0)

print("")
# print("Loading...")


caches_path = "/tmp/enissue"
remote_user = "poikilos"
repo_name = "EnlivenMinetest"
c_remote_user_path = os.path.join(caches_path, remote_user)
c_repo_path = os.path.join(c_remote_user_path, repo_name)
api_repo_url_fmt = "https://api.github.com/repos/{}/{}"
repo_url = api_repo_url_fmt.format(remote_user, repo_name)
issues_url = repo_url + "/issues"
labels_url = repo_url + "/labels"

def get_issues():
    query_s = issues_url
    c_issues_name_fmt = "issues_page={}{}.json"
    this_page = 1
    query_part = ""
    # TODO: IF longer API query is implemented, put something in
    #   query_part like "&label=Bucket_Game"
    if page is not None:
        this_page = page
    c_issues_name = c_issues_name_fmt.format(this_page, query_part)
    c_issues_path = os.path.join(c_repo_path, c_issues_name)
    if os.path.isfile(c_issues_path):
        # See <https://stackoverflow.com/questions/7430928/
        # comparing-dates-to-check-for-old-files>
        max_cache_delta = timedelta(hours=12)
        cache_delta = datetime.now() - max_cache_delta
        c_issues_mtime = os.path.getmtime(c_issues_path)
        filetime = datetime.fromtimestamp(c_issues_mtime)
        if filetime > cache_delta:
            print("Loading cache: \"{}\"".format(c_issues_path))
            # print("Cache time limit: {}".format(max_cache_delta)
            print("Cache expires: {}".format(filetime
                                             + max_cache_delta))
            with open(c_issues_path) as json_file:
                results = json.load(json_file)
            print("The cache has {} issue(s).".format(len(results)))
            return results
        else:
            print("Cache time limit: {}".format(max_cache_delta))
            print("The cache has expired: \"{}\"".format(c_issues_path))
    else:
        print("There is no cache for \"{}\"".format(c_issues_path))

    if page is not None:
        query_s = issues_url + "?page=" + str(page)
    try:
        response = request.urlopen(query_s)
    except urllib.error.HTTPError as e:
        print("You may be able to view the issues on GitHub")
        print("at the 'html_url', and a login may be required.")
        print("The URL \"{}\" is not accessible, so you may have"
              " exceeded the rate limit and be blocked"
              " temporarily:".format(query_s))
        print(str(e))
        return None
    response_s = decode_safe(response.read())
    if not os.path.isdir(c_repo_path):
        os.makedirs(c_repo_path)
    print("Saving issues cache: {}".format(c_issues_path))
    with open(c_issues_path, "w") as outs:
        outs.write(response_s)
    results = json.loads(response_s)
    return results

issues = get_issues()
if issues is None:
    exit(0)
label_ids = []
labels = []

match_all_labels_lower = []
for s in match_all_labels:
    # print("appending {} to match_all_labels_lower.".format(s.lower()))
    match_all_labels_lower.append(s.lower())

match_count = 0
total_count = len(issues)
matching_issue = None

matching_issue_labels = None

for issue in issues:
    this_issue_labels_lower = []
    for label in issue["labels"]:
        label_ids.append(label["id"])
        if label["url"].startswith(labels_url):
            start = len(labels_url) + 1  # +1 for "/"
            label_encoded = label["url"][start:]
            label_s = unquote(label_encoded)
            this_issue_labels_lower.append(label_s.lower())
            if label_s not in labels:
                labels.append(label_s)
        else:
            raise ValueError("The url '{}' does not start with"
                             " '{}'".format(label["url"], labels_url))
    if len(match_all_labels) > 0:
        this_issue_match_count = 0
        for try_label in match_all_labels_lower:
            if try_label in this_issue_labels_lower:
                this_issue_match_count += 1
            # else:
            #     print("#{} is not a match ({} is not in"
            #           " {})".format(issue["number"], try_label,
            #                         this_issue_labels_lower))
        if this_issue_match_count == len(match_all_labels):
            match_count += 1
            print("#{} {}".format(issue["number"], issue["title"]))
    elif (match_number is None) and (cmd == "list"):
        # Show all since no criteria is set.
        match_count += 1
        print("#{} {}".format(issue["number"], issue["title"]))
    if match_number is not None:
        # INFO: match_number & issue["number"] are ints
        if match_number == issue["number"]:
            matching_issue = issue
            matching_issue_labels = this_issue_labels_lower
issue = None


def show_issue(issue):
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
        print("The URL \"{}\" is not accessible, so you may have"
              " exceeded the rate limit and be blocked"
              " temporarily:".format(this_issue_json_url))
        html_url = issue.get("html_url")
        print("You may be able to view the issue on GitHub")
        print("at the 'html_url', and a login may be required:")
        print("html_url: {}".format(html_url))
        return False
    issue_data_s = decode_safe(issue_data_bytes)
    issue_data = json.loads(issue_data_s)
    markdown = issue_data["body"]
    markdown = markdown.replace("\\r\\n", "\n").replace("\\t", "\t")
    left_w = 10
    spacer = " "
    line_fmt = "{: <" + str(left_w) + "}" + spacer + "{}"
    print(line_fmt.format("html_url:",  issue["html_url"]))
    print(line_fmt.format("by:",  issue_data["user"]["login"]))
    print(line_fmt.format("state:",  issue_data["state"]))
    assignees = issue_data.get("assignees")
    if (assignees is not None) and len(assignees) > 1:
        assignee_names = [a["login"] for a in assignees]
        print(line_fmt.format("assignees:",  " ".join(assignee_names)))
    elif issue_data.get("assignee") is not None:
        assignee_name = issue_data["assignee"]["login"]
        print(line_fmt.format("assignee:", assignee_name))
    labels_s = "None"
    if len(matching_issue_labels) > 0:
        neat_labels = []
        for label_s in matching_issue_labels:
            if " " in label_s:
                neat_labels.append('"' + label_s + '"')
            else:
                neat_labels.append(label_s)
        labels_s = ", ".join(neat_labels)
    print(line_fmt.format("labels:", labels_s))
    print("")
    print('"""')
    print(markdown)
    print('"""')
    if issue_data["comments"] > 0:
        print("")
        print("")
        print("({}) comment(s):".format(issue_data["comments"]))
        this_cmts_json_url = issue_data["comments_url"]
        response = request.urlopen(this_cmts_json_url)
        cmts_data_s = decode_safe(response.read())
        cmts_data = json.loads(cmts_data_s)
        left_margin = "    "
        c_prop_fmt = (left_margin + "{: <" + str(left_w) + "}" + spacer
                      + "{}")
        for cmt in cmts_data:
            print("")
            print("")
            print(c_prop_fmt.format("from:", cmt["user"]["login"]))
            print(c_prop_fmt.format("updated_at:", cmt["updated_at"]))
            print("")
            print(left_margin + '"""')
            print(left_margin + cmt["body"])
            print(left_margin + '"""')
            print("")

    print("")
    print("")
    return True

if matching_issue is not None:
    show_issue(matching_issue)

if cmd == "labels":
    # print("Labels:")
    # print("")
    for label_s in labels:
        print(label_s)
    print("")
    print("The repo has {} label(s).".format(len(labels)))
elif cmd == "list":
    print()
    if len(match_all_labels) > 0:
        print("{} issue(s) matched {}".format(
            match_count,
            " + ".join("'{}'".format(s) for s in match_all_labels)
        ))
        if total_count >= 30:
            print("{} searched, which is the maximum number"
                  " per page.".format(total_count))
            next_page = 2
            if page is not None:
                next_page = page + 1
            print("    ./" + me + " " + " ".join(match_all_labels)
                  + " page " + str(next_page))
            print("to see additional pages.")

    else:
        if page is not None:
            print("{} issue(s) are showing for page"
                  " {}.".format(match_count, page))
        else:
            print("{} issue(s) are showing.".format(match_count))
        if match_count >= 30:
            print("That is the maximum number per page. Type")
            next_page = 2
            if page is not None:
                next_page = page + 1
            print("    ./" + me + " page " + str(next_page))
            print("to see additional pages.")
    if match_count > 0:
        print()
        print()
        print("To view details, type")
        print("    ./" + me)
        print("followed by a number.")
print("")

