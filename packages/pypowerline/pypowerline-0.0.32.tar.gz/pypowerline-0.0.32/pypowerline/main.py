"""
main
"""
import os
from typing import Dict, Any, List
from pytconf import register_endpoint, register_main, config_arg_parse_and_launch

from pypowerline.utils import execute_python_file
from pypowerline.segments import Segment
from pypowerline.colors import cprint, Color

from pypowerline.symbols import Symbol
from pypowerline.static import DESCRIPTION, APP_NAME, VERSION_STR


@register_endpoint(
    configs=[],
    description="print the location of pypowerlines config file",
)
def print_config_file() -> None:
    print(os.path.expanduser("~/.config/pypowerline/segments.py"))


@register_endpoint(
    configs=[],
    description="print a prompt for bash",
)
def bash() -> None:
    py_file = os.path.expanduser("~/.config/pypowerline/segments.py")
    vals: Dict[str, Any] = {}
    try:
        execute_python_file(py_file, vals=vals)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(e)
        print("cannot execute segments > ", end="")
        return
    if "segments" not in vals:
        print("segments not defined > ", end="")
        return
    segments: List[Segment] = vals["segments"]
    for segment in segments:
        text = ""
        if segment.icon is not None:
            # TODO: why the two spaces here? Is it because it's unicode?
            text += segment.icon.value + "  "
        text += segment.get_text()
        if segment.color is None or segment.background is None:
            print(text, end="")
        else:
            cprint(
                text,
                segment.color,
                segment.background,
            )
        if segment.separator is not None:
            text = segment.separator.value
            if segment.color is None or segment.background is None:
                print(text, end="")
            else:
                attrs: List[str] = []
                if segment.reverse_sep:
                    attrs.append("reverse")
                    attrs.append("reset")
                cprint(
                    text,
                    segment.color,
                    segment.background,
                    _attrs=attrs,
                )


@register_endpoint(
    configs=[],
    description="do some test printing on the terminal (development purposes)",
)
def test() -> None:
    cwd = os.getcwd()
    symbol = Symbol.SEPARATOR_B.value
    print(f"{cwd} > ", end="")
    cprint("cwd", Color.BLACK, Color.LIGHT_MAGENTA)
    cprint("cwd", Color.BLACK, Color.LIGHT_GREY)
    cprint("cwd", Color.BLACK, Color.GREY)
    cprint("cwd", Color.BLACK, Color.BLUE)
    cprint("cwd", Color.BLACK, Color.LIGHT_BLUE)
    cprint("cwd", Color.WHITE, Color.CYAN)
    cprint("cwd", Color.WHITE, Color.GREEN)
    cprint(f"{symbol}", Color.LIGHT_CYAN, Color.BLACK)
    print()


@register_endpoint(
    configs=[],
    description="do tmux",
)
def tmux() -> None:
    cwd = os.getcwd()
    print(f"{cwd} > ", end="")
    cprint(f"{cwd}", Color.RED, Color.LIGHT_MAGENTA)


@register_endpoint(
    configs=[],
    description="print special symbols (used for development)",
)
def dump_symbols() -> None:
    for symbol in Symbol:
        print(symbol, symbol.value)


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
