# Jinja2 Templating with JSON files
#
# This software is marked with CC0 1.0. To view a copy of this license, visit:
#   https://creativecommons.org/publicdomain/zero/1.0/
# (In other words, public domain.)


import argparse
import builtins
import json
from importlib import import_module
from io import TextIOBase
from os import PathLike
from typing import Any, Union

import jinja2


__all__ = ["__version__", "jjtemplate", "main"]
__version__ = "0.9.0"


ENCODING = "utf-8"


def jjtemplate(
    template_file: Union[str, PathLike, TextIOBase],
    json_files: Union[list[str], list[PathLike], list[TextIOBase]] = [],
    /,
    import_names: list[str] = [],
) -> str:

    loader = jinja2.FileSystemLoader(".")
    env = jinja2.Environment(keep_trailing_newline=True, loader=loader)

    if isinstance(template_file, (str, PathLike)):
        template_file = open(template_file, "r", encoding=ENCODING)
    template = env.from_string(template_file.read())

    context: dict[str, Any] = {}
    context.update(
        {k: v for k, v in builtins.__dict__.items() if not k.startswith("_")}
    )
    for json_file in json_files:
        if isinstance(json_file, (str, PathLike)):
            json_file = open(json_file, "r", encoding=ENCODING)
        obj = json.load(json_file)
        if isinstance(obj, dict):
            context.update(obj)
    for import_name in import_names:
        context[import_name] = import_module(import_name)

    return template.render(context)


def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--import",
        action="append",
        default=[],
        help="import Python module to the context (can be put multiple times)",
        metavar="IMPORT_NAME",
        dest="import_names",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="-",
        type=argparse.FileType("w", encoding=ENCODING),
        help="output file name",
    )
    parser.add_argument(
        "template_file",
        default="-",
        type=argparse.FileType("r", encoding=ENCODING),
        help="Jinja2 template file",
    )
    parser.add_argument(
        "json_files",
        nargs="*",
        type=argparse.FileType("r", encoding=ENCODING),
        help="JSON files loaded to the context (top-level "
        "object must be a dictionary)",
    )
    args = parser.parse_args()

    import_names: list[str] = args.import_names
    output_file: TextIOBase = args.output
    template_file: TextIOBase = args.template_file
    json_files: list[TextIOBase] = args.json_files

    output_file.write(jjtemplate(template_file, json_files, import_names=import_names))


if __name__ == "__main__":
    main()
