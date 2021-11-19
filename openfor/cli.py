import click
from openfor.core.engine import Engine
from openfor import settings

@click.command()
@click.option(
    "-e",
    "--extractor",
    multiple=True,
    metavar="EXTRACTOR_NAME",
    help="Activate an extractor.",
)
@click.option("--files", "-f", multiple=True, required=True, help="Input files.")
@click.option("--output", "-o", help="Output folder.")
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
def cli(extractor, files, output, verbose):
    """yoyooyoyo
    """
    e = Engine()
    if extractor:
        e.extractors = extractor
    
    if not output:
        output = settings.output_folder
    e.run(files, output)

if __name__ == "__main__":
    cli()