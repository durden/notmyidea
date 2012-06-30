#!/usr/bin/env python

"""
Tiny web interface around notmyidea.py
"""

from flask import Flask, render_template, request

from notmyidea import get_user_forks, get_user_contributions

app = Flask(__name__)
app.debug = True


@app.route('/')
def home():
    """homepage"""

    return render_template('index.html')


@app.route('/about')
def about():
    """about"""

    return render_template('about.html')


@app.route('/lookup')
def lookup():
    """Lookup github user's contributions"""

    # FIXME: Handle errors

    if request.method == 'GET':
        username = request.args.get('github_user', None)
        if username is None:
            return None

        fork_urls = get_user_forks(username)

        contributions = []
        for url, cnt, commits_url in get_user_contributions(username, fork_urls):
            # Just get username and project name for pretty display
            short_url = '/'.join(url.split('/')[-2:])

            contributions.append({'url': url,
                                  'short_url': short_url,
                                  'commit_cnt': cnt,
                                  'commits_url': commits_url})

        return render_template('contributions.html', user=username,
                               contributions=contributions)


def run_web(host, port):
    """Run web interface"""

    app.run(host=host, port=port)


if __name__ == "__main__":
    import os

    port = int(os.environ.get('PORT', 5000))
    run_web(host='0.0.0.0', port=port)
