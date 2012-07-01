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


def get_user_info(github_user):
    """Get information about user and return as dictionary"""

    g = Github()

    # FIXME: Handle errors
    return g.users(github_user).response


def get_user_forks(github_user):
    """
    Generate list of repos from given user that are forks aka not their own
    """

    g = Github()
    user = getattr(g.users, github_user)

    # FIXME: Handle errors
    repos = user.repos().response

    for repo in repos:
        if not repo['fork']:
            continue

        g = Github()
        user_repos = getattr(g.repos, github_user)
        repo_details = user_repos(repo['name'])

        # FIXME: Handle errors
        yield repo_details.response['parent']['url']


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


def get_user_contributions(github_user):
    """Generate list of project urls and commit count given user contributed"""

    for url in get_user_forks(github_user):
        # Just use requests here since we already have the api url, no use in
        # re-parsing just to use frappy
        contributors_url = '%s/contributors' % (url)
        resp = requests.get(contributors_url)

        if resp.status_code != 200:
            print 'Error requesting %s fork from API' % (contributors_url)
            continue

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

    for url, cnt, commits_url in get_user_contributions(username):
        print '%s,%d,%s' % (url, cnt, commits_url)


if __name__ == "__main__":
    main()
