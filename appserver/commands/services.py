import click
import json

from subprocess import call

from .. import AVAILABLE_PYTHONZ
from ..utils import parser, write_hosts_inventory


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
