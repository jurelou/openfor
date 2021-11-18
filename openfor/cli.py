import click
from openfor.core.engine import Engine

@click.command()
@click.option(
    "-e",
    "--extractor",
    multiple=True,
    metavar="EXTRACTOR_NAME",
    help="Activate an extractor.",
)
@click.option("--files", "-f", multiple=True, required=True, help="Input files.")
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
def cli(extractor, files, verbose):
    """yoyooyoyo
    """
    e = Engine()
    if extractor:
        e.extractors = extractor
    e.run(files)

if __name__ == "__main__":
    cli()