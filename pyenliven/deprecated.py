#!/usr/bin/env python3
class Repo:
    '''
    WARNING: The real Repo class is in enliven.py
    '''
    print(__doc__)
    pass


class GiteaRepo(Repo):
    '''
    This class is deprecated since the "options" sequential argument
    replaces all of the keyword arguments, and the API and its defaults
    are detected from the URL (See enissue.py).
    '''
    def __init__(
            self,
            repo_url,
            # instance_url="https://api.github.com",
            # repository_id="80873867",
            # api_repo_url_fmt="{instance_url}/repos/{ru}/{rn}",
            # api_issue_url_fmt="{instance_url}/repos/{ru}/{rn}/issues/{issue_no}",
            # search_issues_url_fmt="{instance_url}/search/issues?q=repo%3A{ru}/{rn}+",
            # search_results_key="items",
            # page_size=30,
            # c_issues_name_fmt="issues_page={p}{q}.json",
            # c_issue_name_fmt="{issue_no}.json",
            # default_query={'state':'open'},
            # hide_events=['renamed', 'assigned'],
            caches_path=None,
            # api_comments_url_fmt="{instance_url}/repos/{ru}/{rn}/issues/comments",
            ):
        print(GiteaRepo.__doc__)
        if repo_url.endswith(".git"):
            repo_url = repo_url[:-4]
        urlParts = repo_url.split("/")
        remote_user = urlParts[-2]
        repo_name = urlParts[-1]
        debug("* constructing GiteaRepo")
        debug("  * detected remote_user \"{}\" in url"
              "".format(remote_user))
        debug("  * detected repo_name \"{}\" in url"
              "".format(repo_name))
        instance_url = "/".join(urlParts[:-2])
        debug("  * detected Gitea url " + instance_url)
        # NOTE: self.instance_url is set by super __init__ below.
        # base_query_fmt = "?q=repo%3A{ru}/{rn}+"
        # search_issues_url_fmt = \
        #     "{instance_url}/api/v1/repos/issues/search"+base_query_fmt
