import click
import json

from subprocess import call

from ..conf import AVAILABLE_PYTHONZ, ANSIBLE_BOOK, ANSIBLE_TASK
from ..utils import parser, write_hosts_inventory


@click.group(short_help="add a specific service to your node")
def add():
    pass


@add.command("nginx", short_help="add a web server with proxy capabilities")
@click.argument('ip')
def nginx(ip):
    """
    Add nginx proxy to chosen node
    """

    print("\n---\n")
    print("nginx service is going to be installed for {}".format(ip))

    if click.confirm("Do you want to continue?"):
        inventory = write_hosts_inventory(ip)
        call(["ansible-playbook", ANSIBLE_BOOK, "-i", inventory, "--tags", ANSIBLE_TASK["nginx"]])


@add.command("redis", short_help="add a fast and reliable data structure server")
@click.argument('ip')
def redis(ip):
    """
    Add redis to chosen node
    """

    print("\n---\n")
    print("redis service is going to be installed for {}".format(ip))

    if click.confirm("Do you want to continue?"):
        inventory = write_hosts_inventory(ip)
        call(["ansible-playbook", ANSIBLE_BOOK, "-i", inventory, "--tags", ANSIBLE_TASK["redis"]])


def full_configuration(param):
    ansible_param = parser(param)
    inventory = write_hosts_inventory(param.get("app_server"))
    call(["ansible-playbook", "djangoserver.yml", "-i", inventory, "-e", json.dumps(ansible_param)])


@click.command("deploy", short_help="make a full deploy")
@click.option('--name', prompt="Your application name")
@click.option('--app-server', prompt="FQDN for app server deployment")
@click.option('--python', type=click.Choice(AVAILABLE_PYTHONZ), prompt="Choose a Python version")
@click.password_option('--password', prompt="Set a password for a new user")
@click.password_option('--psql-password', prompt="Set postgres user password (postgresql admin)")
def deploy(*args, **kwargs):
    """
    Make a full server configuration via Ansible playbook
    """

    print("\n---\n")
    print("'{}' will be deployed at '{}'".format(kwargs.get("name"), kwargs.get("app_server")))
    print("'PostgreSQL' will be deployed at '{}'".format(kwargs.get("app_server")))
    print("Chosen python version: {}".format(kwargs.get('python')))

    if click.confirm("Do you want to continue?"):
        full_configuration(kwargs)
