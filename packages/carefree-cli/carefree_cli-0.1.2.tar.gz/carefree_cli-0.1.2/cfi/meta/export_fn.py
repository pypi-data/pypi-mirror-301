import json

from typer import Argument
from typing import List
from pathlib import Path
from typing_extensions import Annotated

from .. import console
from ..utils import load_settings_or_error
from ..schema import TemplatePack
from ..constants import CFI_SUFFIX


def export_fn(
    target: Annotated[
        str,
        Argument(
            help=(
                "Path to export the templates to. "
                "It is recommended to use a '.cfi' file extension."
            )
        ),
    ] = "templates.cfi",
) -> None:
    def _walk(parent: Path) -> None:
        for child in parent.iterdir():
            if child.is_dir():
                _walk(child)
            elif child.suffix == CFI_SUFFIX:
                templates.append(
                    TemplatePack(
                        cmd=json.loads(child.read_text()),
                        hierarchy=child.relative_to(root),
                    )
                )

    root = load_settings_or_error().data_dir
    templates: List[TemplatePack] = []
    _walk(root)
    templates_json = [t.model_dump(mode="json") for t in templates]
    target_path = Path(target)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("w") as f:
        json.dump(templates_json, f)
    console.log(f"exported {len(templates)} templates to '{target_path}'!")
