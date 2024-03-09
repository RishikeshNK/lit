from typing import List
import click
import os
from lit.constants import REPO_NAME

from lit.models.workspace import Workspace
from lit.models.database import Database
from lit.models.blob import Blob
from lit.models.entry import Entry
from lit.models.tree import Tree


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
    root_path = os.getcwd()
    lit_path = os.path.join(root_path, REPO_NAME)
    db_path = os.path.join(lit_path, "objects")

    workspace = Workspace(pathname=root_path)
    database = Database(pathname=db_path)

    entries: List[Entry] = []

    for file in workspace.list_files():
        data = workspace.read_file(file)
        blob = Blob(data=data)

        database.store(blob)

        # TODO: Handle nested directories
        entries.append(
            Entry(name=os.path.basename(file).split("/")[-1], oid=blob.object_id)
        )

    tree = Tree(entries=entries)
    database.store(tree)

    click.echo(f"Tree: {tree.object_id}")


if __name__ == "__main__":
    cli()
