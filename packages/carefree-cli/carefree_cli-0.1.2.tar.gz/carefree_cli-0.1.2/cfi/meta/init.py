import json

from typer import Option
from typing import Any
from typing import Dict
from typing import Optional
from pathlib import Path
from filelock import FileLock
from typing_extensions import Annotated

from .. import console
from ..utils import ask_with_warn
from ..constants import CFI_SETTINGS_PATH


def _ask_existing_data_dir(data_dir: str) -> bool:
    return ask_with_warn(
        f"Directory '{data_dir}' already exists, do you still want to use it as `data_dir`?"
    )


def _set_data_dir(d: Dict[str, Any], ddir: Path) -> None:
    ddir.mkdir(parents=True, exist_ok=True)
    data_dir = str(ddir)
    d["data_dir"] = data_dir
    with CFI_SETTINGS_PATH.open("w") as f:
        json.dump(d, f, indent=2)
    console.log(f"`data_dir` is set to '{data_dir}'")


def _init(data_dir: Optional[str]) -> None:
    if not CFI_SETTINGS_PATH.is_file():
        d = {}
    else:
        with CFI_SETTINGS_PATH.open("r") as f:
            d = json.load(f)
    existing_data_dir = d.get("data_dir")
    if existing_data_dir is None:
        if data_dir is None:
            console.rule("Enter the Directory to Store Your Templates")
            data_dir = console.ask("[cyan]`data_dir`")
        ddir = Path(data_dir).absolute()
        if ddir.is_dir():
            if not _ask_existing_data_dir(data_dir):
                console.error("Then please choose another directory.")
                return None
        _set_data_dir(d, ddir)
        return None
    if data_dir is None:
        console.log(f"`data_dir` is already set to '{existing_data_dir}'")
        return None
    ddir = Path(data_dir).absolute()
    existing_ddir = Path(existing_data_dir).absolute()
    if ddir == existing_ddir:
        console.log(f"`data_dir` is already set to '{existing_data_dir}'")
        return None
    if ddir.is_dir():
        if _ask_existing_data_dir(data_dir):
            _set_data_dir(d, ddir)
        else:
            console.error("Then please choose another directory.")
        return None
    migrate = console.ask(
        f"[yellow]Current `data_dir` is '{existing_data_dir}', do you want to migrate to '{data_dir}'?",
        ["y", "n"],
        default="n",
    )
    if migrate == "n":
        console.log(f"`data_dir` is still set to '{existing_data_dir}'")
        return None
    existing_ddir.rename(ddir)
    _set_data_dir(d, ddir)


def init(
    data_dir: Annotated[
        Optional[str],
        Option("--data_dir", "-d", help="Directory to store your templates."),
    ] = None,
) -> None:
    with FileLock(CFI_SETTINGS_PATH.with_suffix(".lock")):
        _init(data_dir)
