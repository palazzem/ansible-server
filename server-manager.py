import click

from appserver.commands.generics import version
from appserver.commands.services import deploy


@click.group()
@click.option('--version', is_flag=True, callback=version, expose_value=False, is_eager=True)
def cli():
    """
    Deploy fast your Django app!
    """

cli.add_command(deploy)


if __name__ == '__main__':
    cli()
