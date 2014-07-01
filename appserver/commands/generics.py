import click

from appserver import VERSION


def version(ctx, param, value):
    """
    Print current version
    """
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version: {}".format(VERSION))
    ctx.exit()
