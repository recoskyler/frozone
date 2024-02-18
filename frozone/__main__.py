import click

from . import frozone

@click.group()
def cli():
    pass

cli.add_command(frozone.freeze)
cli.add_command(frozone.restore)
