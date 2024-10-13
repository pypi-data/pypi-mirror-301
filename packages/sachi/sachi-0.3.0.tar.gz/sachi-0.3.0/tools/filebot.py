#!/usr/bin/env python3
import csv
from pathlib import Path

import jinja2

TYPE_MAPPING = {
    "Episode": "str",
    "AudioTrack": "str",
    "[String:String]": "dict[str, str]",
    "Object": "Any",
    "ChannelCount": "str",
    "true | false": "bool",
    "String*": "list[str]",
    "[String:Any]": "dict[str, Any]",
    "Date": "datetime",
    "FrameRate": "str",
    "File*": "list[Path]",
    "Instant": "datetime",
    "Language": "str",
    "FileSize": "str",
    "Decimal": "float",
    "BitRate": "str",
    "Series": "dict[str, Any]",
    "[String:String]*": "list[dict[str, str]]",
    "String": "str",
    "Integer": "int",
    "Movie": "dict[str, Any]",
    "[String:Any]*": "list[dict[str, Any]]",
    "File": "Path",
    "Duration": "str",
    "Language*": "list[str]",
    "Integer*": "list[int]",
}

with open(Path(__file__).parent / "filebot.csv") as f:
    reader = csv.DictReader(f, delimiter=";")
    fields = list(reader)

for field in fields:
    field["Type"] = TYPE_MAPPING[field["Type"]]

template = jinja2.Template(
    r'''from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class FileBotContext:
    {%- for field in fields %}
    {{field.Name}}: {{field.Type}} | None = None
    """{{field.Description}} (`{{field.Example}}`)"""
    {% endfor %}
'''
)

print(template.render(fields=fields))
