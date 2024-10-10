from typer import Argument
from typing_extensions import Annotated


template_argument = Annotated[
    str,
    Argument(
        help=(
            "The command template, or path to the command template (in which case it should end with `.txt`)\n\n"
            "There are two common formats:\n\n"
            "  * plain command, i.e. the direct command to run.\n\n"
            "  * placeholder template, which is a string with some '{}'s, and you can"
            "specify the values of these '{}'s later in the `load` command.\n\n"
            "> you can (and it is recommended) to provide a 'name' for each '{}' in"
            "the placeholder template, so identify them in `load` will be easier.\n\n"
            "> for example, 'echo {msg}' is preferred over 'echo {}'.\n\n"
            "> be aware that the 'name' should be 'formattable', i.e. it should be "
            "able to pass to `str.format`."
        )
    ),
]
hierarchy_argument = Annotated[
    str,
    Argument(
        help=(
            "Hierarchy of the template, use '/' to separate levels, and:\n\n"
            "  * at least 1 level should be provided.\n\n"
            "  * it is recommended to use at most 2 levels.\n\n"
            "  * the last level will be used as the template name."
        ),
    ),
]
