from typing import Optional

import latitude_cli.modules.templates as templates
import typer
from latitude_cli.libs.version import getVerison


app = typer.Typer()

app.add_typer(
    templates.app,
    name="templates",
    help="Utils for bootstrapping new apps"
)


def _version_callback(value: bool) -> None:
    if value:
        __version__ = getVerison()
        typer.echo(f"v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )

) -> None:
    return


def run() -> None:
    """Run commands."""
    # getLatestPyPiVersion()
    app()
