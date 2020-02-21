#!/usr/bin/env python3
from __future__ import print_function
import sys
import json
import os

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


repo_url = "https://api.github.com/repos/poikilos/EnlivenMinetest"
url = repo_url + "/issues"
labels_url = repo_url + "/labels"
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
match_number = None
for i in range(1, len(sys.argv)):
    arg = sys.argv[i]
    if arg.startswith("#"):
        arg = arg[1:]
    if (cmd is None) and (arg in cmds.keys()):
        cmd = arg
        print("* mode set to {}".format(cmd))
    else:
        try:
            match_number = int(arg)
        except ValueError:
            if (cmd is None) and (cmds.get(arg) is not None):
                cmd = arg
            else:
                match_all_labels.append(arg)
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
response = request.urlopen(url)
d_s = response.read()
d = json.loads(d_s)
label_ids = []
labels = []

match_all_labels_lower = []
for s in match_all_labels:
    # print("appending {} to match_all_labels_lower.".format(s.lower()))
    match_all_labels_lower.append(s.lower())

match_count = 0
matching_issue = None
for issue in d:
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
    elif match_number is None:
        # Show all since no criteria is set.
        match_count += 1
        print("#{} {}".format(issue["number"], issue["title"]))
    if match_number is not None:
        # INFO: match_number & issue["number"] are ints
        if match_number == issue["number"]:
            matching_issue = issue
if matching_issue is not None:
    print("")
    print("#{} {}".format(issue["number"], issue["title"]))
    # print(matching_issue["html_url"])
    print("")
    this_issue_json_url = matching_issue["url"]
    response = request.urlopen(this_issue_json_url)
    issue_data_s = response.read()
    issue_data = json.loads(issue_data_s)
    markdown = issue_data["body"]
    markdown = markdown.replace("\\r\\n", "\n").replace("\\t", "\t")
    left_w = 10
    spacer = " "
    line_fmt = "{: <" + str(left_w) + "}" + spacer + "{}"
    print(line_fmt.format("html_url:",  matching_issue["html_url"]))
    print(line_fmt.format("by:",  issue_data["user"]["login"]))
    print(line_fmt.format("state:",  issue_data["state"]))
    assignees = issue_data["assignees"]
    if len(assignees) > 1:
        print(line_fmt.format("assignees:",  " ".join(assignees)))
    else:
        print(line_fmt.format("assignee:",  issue_data["assignee"]))
    print(markdown)
    if issue_data["comments"] > 0:
        print("")
        print("")
        print("({}) comment(s):".format(issue_data["comments"]))
        this_cmts_json_url = issue_data["comments_url"]
        response = request.urlopen(this_cmts_json_url)
        cmts_data_s = response.read()
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
            print(left_margin + cmt["body"])
            print("")

    print("")
    print("")


if cmd == "labels":
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
    else:
        print("{} issue(s) are showing.".format(match_count))
    if match_count > 0:
        print()
        print()
        print("To view details, type")
        print("    ./" + me)
        print("followed by a number.")
print("")

