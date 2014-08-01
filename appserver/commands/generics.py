import click
import json

from subprocess import call

from appserver import VERSION
from ..conf import ANSIBLE_BOOK, ANSIBLE_TASK, AVAILABLE_PYTHONZ
from ..utils import write_hosts_inventory, parser


def version(ctx, param, value):
    """
    Print current version
    """
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version: {}".format(VERSION))
    ctx.exit()


@click.command("prepare", short_help="fill a node with all required packages")
@click.argument('ip')
def prepare(ip):
    """
    Prepare basic server configuration via Ansible playbook
    """

    print("\n---\n")
    print("A basic configuration will be done for {}".format(ip))
    print("WARNING: if this server is already configured, probably, you don't want to do this!")

    if click.confirm("Do you want to continue?"):
        inventory = write_hosts_inventory(ip)
        call(["ansible-playbook", ANSIBLE_BOOK, "-i", inventory, "--tags", ANSIBLE_TASK["basic"]])


@click.command("deploy", short_help="prepare all components for application deployment")
@click.option('--app-name', prompt="Your application name")
@click.option('--server-name', prompt="FQDN for app server deployment")
@click.option('--python', type=click.Choice(AVAILABLE_PYTHONZ), prompt="Choose a Python version")
@click.password_option('--password', prompt="Set a password for the user")
@click.option('--createdb/--no-createdb', default=True, prompt="Create a user in PostgreSQL with a database (if available)?")
@click.argument('ip')
def deploy(ip, **kwargs):
    """
    Prepare all components for application deployment
    """

    print("\n---\n")
    print("'{}' will be configured to host {} as {}".format(ip, kwargs.get("app_name"), kwargs.get("server_name")))
    print("Running python version: {}".format(kwargs.get('python')))
    print("Database creation: {}".format(kwargs.get('createdb')))

    if click.confirm("Do you want to continue?"):
        ansible_param = parser(kwargs)
        inventory = write_hosts_inventory(ip)
        call(["ansible-playbook", ANSIBLE_BOOK, "-i", inventory, "--tags", ANSIBLE_TASK["application"],
              "-e", json.dumps(ansible_param)])
