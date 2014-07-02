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
-----

None

nginx
-----

None

redis
-----

None

postgresql
----------

* psql_pass: password for a global postgres user

application
-----------

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

`manager.py` script, exposes a really simple command line tool:

    Usage: manager.py [OPTIONS] COMMAND [ARGS]...

      Deploy fast your Django app!

    Options:
      --version
      --help     Show this message and exit.

    Commands:
      add      add a specific service to your node
      deploy   prepare all components for application deployment
      prepare  fill a node with all required packages

Commands
--------

* `prepare`: when you create a new CentOS machine (VM, DigitalOcean, etc.) this should be the first running command.
 It installs all basic requirements like SELinux, firewall configuration, development tools (git, mercurial, etc.) and
 a global python version manager (pythonz)
* `add`: when a node is prepared, use this command to add some services like postgresql, redis or nginx
* `deploy`: after a node is configured with all required components, this command orchestrates them for a reverse proxy
 to a WSGI application server (gunicorn). Then you can start your first deploy via git, rsync or whatever you want

**WARNING**: even if all commands are idempotent, `prepare` should be executed only once per node because it could
 override your firewall settings.

Prepare
-------

    Usage: manager.py prepare [OPTIONS] IP

Options: none

Add
---

    Usage: manager.py add [OPTIONS] COMMAND IP

    Options:
      --help  Show this message and exit.

    Commands:
      nginx       add a web server with proxy capabilities
      postgresql  add a strong, reliable and real DBMS
      redis       add a fast and reliable data structure server

Options `postgresql`:

    --psql-password TEXT  choose a postgres user password

Deploy
------

    Usage: manager.py deploy [OPTIONS] IP

Options:

    --app-name TEXT             Set your application name. It's used even for username
    --password TEXT             Set your user password. It's used even for your database role
    --server-name TEXT          Used by nginx for reverse proxy
    --python [2.7.7|3.4.1]      Uses a global python version or installs a new one
    --createdb / --no-createdb  Creates a new role for postgresql database and a new database

Command line notes
------------------

If any of above options are missing, the script prompts you all needed parameters:

    Your application name: evonove
    Set a password for a new user:
    Repeat for confirmation:
    FQDN for app server deployment: evonove.it
    Choose a Python version: 3.4.1
    Do I need to create a user in postgres with a database? [Y/n]: Y

    ---

    '8.8.8.8' will be configured to host 'evonove' as 'evonove.it'
    Running python version: 3.4.1
    Database creation: True
    Do you want to continue? [y/N]: Y

**Note:** If you want to skip any wsgi configuration, `Your application name` should be your repository name.

Manage supervisor
-----------------

Log as your application user and:

    $ `workon supervisord`
    $ `supervisorctl -c ~/etc/supervisord_<application_name>.conf`

The day after deploy
--------------------

To finalize your deploy simply:

* clone your repository in user's `HOME` (it's your `application name`)
* install all requirements in your virtualenv (it already contains `gunicorn`)
* restart all supervisor services
* set environment vars for `postactivate` if required
* do further configurations if required (ex: add celery to supervisor, etc.)
