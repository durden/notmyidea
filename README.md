# Not My Idea

Not My Idea is a micro 'application' that finds all the projects a given user
has contributed to that were not their own.

## Why

A developer's github profile can tell you a lot about the things they are
interested in and what their capable of.  However, I think another good bit of
information to know about a developer is how willing they are to contribute to
projects/ideas that are not their own.

You can also see how involved in a community and a rough idea of what other
developers think about each other by seeing how many other projects a
developer's code is accepted to.

###Install

This application can be installed simply by installing the requirements
designated in the
[requirements.txt](https://github.com/durden/notmyidea/blob/master/requirements.txt)
file.

    - git clone https://github.com/durden/notmyidea.git
    - pip install -r requirements.txt


###Usage

1. Command line

    - python notmyidea.py -h
    - python notmyidea.py -u <username>

2. Web

    - python app.py
    - Browse to 0.0.0.0:5000
