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


def get_user_contributions(github_user, fork_urls):
    """Generate list of project urls that given user has contributed to"""

    for url in fork_urls:
        # Just use requests here since we already have the api url, no use in
        # re-parsing just to use frappy
        contributors_url = '%s/contributors' % (url)
        resp = requests.get(contributors_url)

        if resp.status_code != 200:
            print 'Error requesting %s fork from API' % (contributors_url)
            yield None

        users = json.loads(resp.content)
        if github_user in [user['login'] for user in users]:
            yield url


def main():
    """start"""

    fork_urls = get_user_forks('durden')
    for contrib in get_user_contributions('durden', fork_urls):
        print contrib


if __name__ == "__main__":
    main()
