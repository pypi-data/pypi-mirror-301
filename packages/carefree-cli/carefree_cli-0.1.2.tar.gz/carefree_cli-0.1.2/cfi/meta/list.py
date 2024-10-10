from typer import Argument
from typing import Optional
from pathlib import Path
from typing_extensions import Annotated

from .. import console
from ..utils import parse_hierarchy_path
from ..utils import load_settings_or_error
from ..constants import CFI_SUFFIX


def list(
    hierarchy: Annotated[
        Optional[str],
        Argument(
            help=(
                "Hierarchy of the template to list, use '/' to separate levels.\n\n"
                "  * 'level1/level2' will list all templates under 'level1 -> level2'.\n\n"
                "  * `None` will list all existing templates.\n\n"
            ),
        ),
    ] = None,
) -> None:
    from rich.text import Text
    from rich.tree import Tree
    from rich.markup import escape
    from rich.filesize import decimal

    def _list(parent: Path, tree: Tree) -> None:
        paths = sorted(
            parent.iterdir(),
            key=lambda path: (not path.is_file(), path.name.lower()),
        )
        for child in paths:
            if child.is_dir():
                style = "dim" if child.name.startswith("__") else ""
                branch = tree.add(
                    f"[bold magenta]:open_file_folder: [link file://{child}]{escape(child.name)}",
                    style=style,
                    guide_style=style,
                )
                _list(child, branch)
            elif child.suffix == CFI_SUFFIX:
                text_filename = Text(child.stem, "green")
                text_filename.stylize(f"link file://{child}")
                file_size = child.stat().st_size
                text_filename.append(f" ({decimal(file_size)})", "blue")
                tree.add(Text("📄 ") + text_filename)

    if hierarchy is None:
        parent = load_settings_or_error().data_dir
    else:
        path = parse_hierarchy_path(hierarchy)
        if path.is_file():
            parent = path.parent
        else:
            parent = path.with_suffix("")
    parent = parent.absolute()
    if not parent.is_dir():
        parent.mkdir(parents=True, exist_ok=True)
    tree = Tree(
        f":open_file_folder: [link file://{parent}]{parent}",
        guide_style="bold bright_blue",
    )
    _list(parent, tree)
    console.log(tree)
