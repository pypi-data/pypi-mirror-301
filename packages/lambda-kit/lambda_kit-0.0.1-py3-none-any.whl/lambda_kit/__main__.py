"""
This module contains the CLI tool for packaging Python Lambda functions.
"""

import click


@click.group()
def cli() -> None:
    """CLI tool for packaging Python Lambda components."""


@cli.command("func")
@click.option("-n", "--name", required=True, help="Name of the Lambda function.")
@click.option(
    "--source-dir",
    required=True,
    type=click.Path(exists=True),
    help="Path to the source directory.",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(),
    help="Path to the output directory.",
)
def package_function(function_name: str, source_dir: str, output_dir: str) -> None:
    """Package Lambda functions."""
    click.echo(f"Packaging Lambda function: {function_name}")
    click.echo(f"Source directory: {source_dir}")
    click.echo(f"Output directory: {output_dir}")
    # Add your packaging logic here


def main() -> None:
    """
    Entry point for the CLI tool.

    :return:
    """
    cli()


if __name__ == "__main__":
    main()
