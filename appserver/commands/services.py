import click

from subprocess import call

from ..conf import ANSIBLE_BOOK, ANSIBLE_TASK
from ..utils import write_hosts_inventory


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


@add.command("postgresql", short_help="add a strong, reliable and real DBMS")
@click.password_option('--psql-password', prompt="Set postgres user password (postgresql admin)")
@click.argument('ip')
def postgresql(ip, psql_password):
    """
    Add postgresql to chosen node
    """

    print("\n---\n")
    print("postgresql service is going to be installed for {}".format(ip))

    if click.confirm("Do you want to continue?"):
        inventory = write_hosts_inventory(ip)
        call(["ansible-playbook", ANSIBLE_BOOK, "-i", inventory, "--tags", ANSIBLE_TASK["postgres"],
              "-e", "psql_pass={}".format(psql_password)])
