import click

from appserver.commands.generics import version, prepare, deploy
from appserver.commands.services import add


@click.group()
@click.option('--version', is_flag=True, callback=version, expose_value=False, is_eager=True)
def cli():
    """
    Deploy fast your Django app!
    """

# Available subcommands
cli.add_command(add)
cli.add_command(deploy)
cli.add_command(prepare)


if __name__ == '__main__':
    cli()
