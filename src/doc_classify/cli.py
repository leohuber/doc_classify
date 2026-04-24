"""Doc-classify command-line interface."""

from importlib.metadata import version

import click

from doc_classify.config import get_config


@click.group(invoke_without_command=True)
@click.version_option(version=version("doc-classify"), prog_name="doc-classify")
@click.pass_context
def main(ctx: click.Context) -> None:
    """Doc-classify command-line interface."""
    config = get_config()  # noqa: F841
    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())
