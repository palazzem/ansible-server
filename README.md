Server orchestration
====================

Ansible playbook to configure a generic CentOS node for Django applicationshosting. A python script is available.

Installed components
--------------------

* python interpreters
* supervisor
* postgresql
* nginx (serves static files)
* gunicorn
* redis

It takes care of some generic sysadmin tasks like firewall configuration and SELinux.

Requirements
------------

* Ansible 1.6+
* Click 2.2+

Installation
------------

Create a virtual env and install requirements:

    $ pip install -r requirements.txt

Command line interface
----------------------

`server-manager.py` exposes a really simple command line with `deploy` command:

    Usage: server-manager.py deploy [OPTIONS]
    Make a full server configuration via Ansible playbook

    Options:
      --version
      --name TEXT
      --app-server TEXT
      --password TEXT
      --psql-password TEXT
      --python [2.7.7|3.4.1]
      --help                  Show this message and exit.

If any of these options are missing, this script will ask you to complete all needed parameters:

    Your application name: evonove
    FQDN for app server deployment: evonove.it
    Set a password for a new user:
    Repeat for confirmation:
    Set postgres user password (postgresql admin):
    Repeat for confirmation:
    Choose a Python version: 3.4.1

    ---

    'evonove' will be deployed at 'evonove.it'
    'PostgreSQL' will be deployed at 'evonove.it'
    Chosen python version: 3.4.1

Send monkeys over the Internet
------------------------------

Just:

    $ python server-manager.py deploy
