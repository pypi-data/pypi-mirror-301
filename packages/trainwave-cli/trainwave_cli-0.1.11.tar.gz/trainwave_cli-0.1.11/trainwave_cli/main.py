import sys

import typer
from loguru import logger

from trainwave_cli.cli import auth, jobs, setup

app = typer.Typer()
app.add_typer(jobs.app, name="jobs", help="Manage training jobs")
app.add_typer(auth.app, name="auth", help="Authenticate with Trainwave")
app.add_typer(setup.app, name="config")


def entrypoint() -> None:
    logger.remove()
    logger.add(sys.stdout, colorize=True, format="<level>{message}</level>")
    app()


if __name__ == "__main__":
    app()
