#!/usr/bin/env python

"""
Tiny web interface around notmyidea.py
"""

from flask import Flask, abort, render_template, request

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

    # Using slightly bad practice for handling errors by not specifying the
    # error we are catching.  However, we truly want to hide all errors from
    # user and just give them general 404.  So any resulting error should be
    # have the same way.

    if request.method == 'GET':
        username = request.args.get('github_user', None)
        if username is None:
            return None

        try:
            user_info = get_user_info(username)
        except:
            abort(404)

        contributions = []

        try:
            user_contribs = list(get_user_contributions(username))
        except:
            abort(404)

        for url, cnt, commits_url in user_contribs:
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


@app.errorhandler(404)
def page_not_found(error):
    if request.method == 'GET':
        username = request.args.get('github_user', None)

    return render_template('404.html', username=username), 404


def run_web(host, port):
    """Run web interface"""

    app.run(host=host, port=port)


if __name__ == "__main__":
    import os

    port = int(os.environ.get('PORT', 5000))
    run_web(host='0.0.0.0', port=port)
