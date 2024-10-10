from typer import Option
from pathlib import Path
from filelock import FileLock
from typing_extensions import Annotated

from .. import console
from ..utils import ask_with_warn
from ..utils import parse_hierarchy_path
from ..common import hierarchy_argument
from ..common import template_argument
from ..schema import Template


def add(
    template: template_argument,
    hierarchy: hierarchy_argument,
    *,
    is_plain: Annotated[
        bool,
        Option("--plain", help="Whether the template is a plain command."),
    ] = False,
    verbose: bool = True,
) -> None:
    template_path = parse_hierarchy_path(hierarchy)
    with FileLock(template_path.with_suffix(".lock")):
        if template_path.exists():
            if not ask_with_warn(
                f"Template '{template_path}' already exists, do you want to overwrite it?"
            ):
                console.error("Then please choose another hierarchy.")
                return None
        if template.endswith(".txt"):
            template = Path(template).read_text()
        cmd = Template(cmd=template, is_plain=is_plain)
        template_path.write_text(cmd.model_dump_json())
        if verbose:
            console.log(f"""[green]{template}[/green] is saved to '{template_path}'.""")
