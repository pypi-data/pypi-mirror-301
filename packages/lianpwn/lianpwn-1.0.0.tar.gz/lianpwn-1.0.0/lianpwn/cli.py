# cli.py
import click
from lianpwn.template_gen import generate_template


@click.group()
def cli():
    pass


@cli.command()
def template():
    """Generate a template file"""
    generate_template()


@cli.command()
def nocli():
    """Generate a template file"""
    generate_template_nocli()


if __name__ == "__main__":
    cli()
