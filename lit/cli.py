import click
import os
from lit.constants import REPO_NAME
from lit.models.workspace import Workspace


@click.group()
def cli():
    pass


@cli.command("init")
@click.argument(
    "path", type=click.Path(exists=True, file_okay=False), required=False, default="."
)
def init(path: str) -> None:
    """
    Initialize a new Lit repository.

    :param path: Path where the repository will be initialized.
    """
    try:
        repo_path = os.path.abspath(os.path.join(path, REPO_NAME))
        for directory in ("objects", "refs"):
            dir_path = os.path.join(repo_path, directory)
            os.makedirs(dir_path, exist_ok=True)

        click.echo(f"Initialized empty Lit repository in {repo_path}")
    except OSError as e: 
        click.echo(f"{repo_path}: {e.strerror}", err=True)

@cli.command("commit")
def commit() -> None:
    """
    Record changes to the repository.
    """
    workspace = Workspace(pathname=os.getcwd())
    click.echo(workspace.list_files())
    


if __name__ == "__main__":
    cli()
