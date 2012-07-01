#!/usr/bin/env python

"""
Simple script to find all github projects a given user has committed to that
are not their own, i.e. find all open source repos user has 'helped' out.

Keep in mind that this script requires Python >= 2.6 for json support.
"""

import json

try:
    from frappy.services.github import Github
except ImportError:
    raise ImportError('Frappy required, install it via requirements.txt')

try:
    import requests
except ImportError:
    raise ImportError('Requests required, install it via requirements.txt')


def get_user_forks(github_user):
    """Get a list of repos from given user that are forks aka not their own"""

    g = Github()
    user = getattr(g.users, github_user)
    repos = user.repos().response

    fork_urls = []

    for repo in repos:
        if not repo['fork']:
            continue

        g = Github()
        user_repos = getattr(g.repos, github_user)
        repo_details = user_repos(repo['name'])
        fork_urls.append(repo_details.response['parent']['url'])

    return fork_urls


def _api_url_to_commits_url(api_url, github_user):
    """
    Take url used by API for a repo's information and return url to all commits
    from given user on that repo
    """

    # Example api url: https://api.github.com/repos/saltycrane/trace-tools
    # Example commit url:
        # https://github.com/saltycrane/trace-tools/commits?author=durden

    url_parts = api_url.split('/')
    repo = url_parts[-1]
    repo_owner = url_parts[-2]
    return 'https://github.com/%s/%s/commits?author=%s' % (repo_owner, repo,
                                                           github_user)


def get_user_contributions(github_user, fork_urls):
    """Generate list of project urls and commit count given user contributed"""

    for url in fork_urls:
        # Just use requests here since we already have the api url, no use in
        # re-parsing just to use frappy
        contributors_url = '%s/contributors' % (url)
        resp = requests.get(contributors_url)

        if resp.status_code != 200:
            print 'Error requesting %s fork from API' % (contributors_url)
            yield (None, None, None)

        users = json.loads(resp.content)
        for user in users:
            if github_user == user['login']:
                yield url, user['contributions'], _api_url_to_commits_url(
                                                            url, github_user)


def _parse_args():
    """Parse arguments and return username"""

    import argparse

    desc = 'Show projects a github user has contributed to besides their own'
    parser = argparse.ArgumentParser(prog='notmyidea.py', description=desc)

    parser.add_argument('-u', '--username', action='store', required=True,
                        default=None, help='Github username to lookup')

    args = parser.parse_args()
    return args.username


def main():
    """start"""

    username = _parse_args()

    fork_urls = get_user_forks(username)
    for url, cnt, commits_url in get_user_contributions(username, fork_urls):
        print '%s,%d,%s' % (url, cnt, commits_url)


if __name__ == "__main__":
    main()
