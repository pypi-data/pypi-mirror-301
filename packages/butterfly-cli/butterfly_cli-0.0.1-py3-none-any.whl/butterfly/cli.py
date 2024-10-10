import click
from .core import run as run_analysis

@click.group()
def cli():
    pass

@cli.command()
def run():
    """Run the Butterfly security analysis"""
    click.echo("Starting Butterfly security analysis...")
    results = run_analysis()
    click.echo("Analysis complete. Results:")
    click.echo(results)

if __name__ == '__main__':
    cli()