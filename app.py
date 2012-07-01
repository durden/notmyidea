#!/usr/bin/env python

"""
Tiny web interface around notmyidea.py
"""

from flask import Flask, render_template, request

from notmyidea import get_user_contributions, get_user_info

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

        user_info = get_user_info(username)

        contributions = []
        for url, cnt, commits_url in get_user_contributions(username):
            # Just get username and project name for pretty display
            short_url = '/'.join(url.split('/')[-2:])

            contributions.append({'url': url,
                                  'short_url': short_url,
                                  'commit_cnt': cnt,
                                  'commits_url': commits_url})

        contributions = sorted(contributions, key=lambda x: x['commit_cnt'],
                               reverse=True)
        return render_template('contributions.html', user_info=user_info,
                               contributions=contributions)


def run_web(host, port):
    """Run web interface"""

    app.run(host=host, port=port)


if __name__ == "__main__":
    import os

    port = int(os.environ.get('PORT', 5000))
    run_web(host='0.0.0.0', port=port)
