import json
import click

from tempfile import NamedTemporaryFile
from subprocess import call


__VERSION__ = "0.0.0"
AVAILABLE_PYTHONZ = [
    "2.7.7",
    "3.4.1",
]


def parser(param):
    return {
        "app_name": param.get("name"),
        "server_name": param.get("app_server"),
        "user_name": param.get("name"),
        "user_pass": param.get("password"),
        "psql_pass": param.get("psql_password"),
        "python_version": param.get("python"),
    }


def write_hosts_inventory(appserver):
    hosts_file = NamedTemporaryFile(delete=False)
    hosts = "[appservers]\n{0}\n\n[dbservers]\n{1}".format(appserver, appserver)

    hosts_file.write(hosts)
    hosts_file.close()
    return hosts_file.name


def version(ctx, param, value):
    """
    Print current version
    """
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version: {}".format(__VERSION__))
    ctx.exit()


def full_configuration(param):
    ansible_param = parser(param)
    inventory = write_hosts_inventory(param.get("app_server"))
    call(["ansible-playbook", "djangoserver.yml", "-i", inventory, "-e", json.dumps(ansible_param)])


@click.group()
def cli():
    """
    Deploy fast your Django app!
    """


@click.command("deploy", short_help="make a full deploy")
@click.option('--version', is_flag=True, callback=version, expose_value=False, is_eager=True)
@click.option('--name', prompt="Your application name")
@click.option('--app-server', prompt="FQDN for app server deployment")
@click.password_option('--password', prompt="Set a password for a new user")
@click.password_option('--psql-password', prompt="Set postgres user password (postgresql admin)")
@click.option('--python', type=click.Choice(AVAILABLE_PYTHONZ), prompt="Choose a Python version")
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

cli.add_command(deploy)

if __name__ == '__main__':
    cli()
