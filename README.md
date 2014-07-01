Server orchestration
====================

Ansible playbook to configure a generic CentOS node for Django applications hosting. A python script is also available.

Requirements
------------

* Ansible 1.6+
* Click 2.2+

Create a virtualenv and install above requirements:

    $ pip install -r requirements.txt

Available tasks
---------------

The Ansible playbook exposes the following tasks:

* Prepare a node for basic functions (`basic`)
* Add nginx service (`nginx`)
* Add redis service (`redis`)
* Add postgresql service (`postgresql`)
* Prepare for application deployment (`application`)

To use a particular task, use `--tags` options like:

    $ ansible orchestration.yml -i hosts --tags basic

*Note:* `hosts` file should exists in your folder. Check how to create an [inventory][1].

[1]: http://docs.ansible.com/intro_inventory.html

Required parameters
-------------------

These parameters are required in order to let Ansible works like expected:

basic
~~~~~

None

nginx
~~~~~

None

redis
~~~~~

None

postgresql
~~~~~~~~~~

* psql_pass: password for a global postgres user

application
~~~~~~~~~~~

* user_name: user that will host the application and all configurations files including static files
* user_pass: password for above user
* app_name: the name of your application
* createdb: should be `True` if it's required to create a user and a database inside postgresql instance
* python_version: choose a python version for your application

To pass a parameter, simply:

    $ ansible orchestration.yml -i hosts --tags postgresql -e {"psql_pass" : "123456"}

Notes
-----

`nginx` serves all static files inside your `user_name` home directory. If the file is not available, it does a
reverse proxy to your wsgi application server (ATM it's `gunicorn`). Otherwise its a 404 error page.

`application` configures all other components to host your new wsgi application. It uses a global installation of
python if available otherwise a new version of interpreter is installed with `pythonz`.

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

**Note:** If you want to skip any wsgi configuration, `Your application name` should be your repository name.

Send monkeys over the Internet
------------------------------

Just:

    $ python server-manager.py deploy

The day after deploy
--------------------

To finalize your deploy simply:

* clone your repository in user folder (it's your `application name`)
* `workon` virtualenv and install your app requirements
* `workon supervisord` and use `supervisorctl -c ~/etc/supervisord_<application_name>.conf`
* `restart all`
* set environ vars inside `postactivate` if required
* do further configurations if required (ex: add celery to supervisor)
