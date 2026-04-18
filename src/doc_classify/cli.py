"""Doc-classify command-line interface."""

from importlib.metadata import version

import click


@click.group(invoke_without_command=True)
@click.version_option(version=version("doc-classify"), prog_name="doc-classify")
@click.pass_context
def main(ctx: click.Context) -> None:
    """Doc-classify command-line interface."""
    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())
