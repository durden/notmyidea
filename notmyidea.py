#!/usr/bin/env python

"""
Simple script to find all github projects a given user has committed to that
are not their own, i.e. find all open source repos user has 'helped' out.
"""


try:
    from frappy.services.github import Github
except ImportError:
    raise ImportError('Frappy required, install it via requirements.txt')


def get_user_forks(github_user):
    """Get a list of repos from given user that are forks aka not their own"""

    g = Github()
    user = getattr(g.users, github_user)
    repos = user.repos().response

    for repo in repos:
        if not repo['fork']:
            continue

        g = Github()
        user_repos = getattr(g.repos, github_user)
        repo_details = user_repos(repo['name'])
        print repo_details.response['parent']['url']


def main():
    """start"""

    get_user_forks('durden')


if __name__ == "__main__":
    main()
