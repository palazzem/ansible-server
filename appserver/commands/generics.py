import click

from subprocess import call

from appserver import VERSION
from ..conf import ANSIBLE_BOOK, ANSIBLE_TASK
from ..utils import write_hosts_inventory


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
