#!/usr/bin/env python
import argparse
from string import ascii_letters, digits
from datetime import datetime
from pathlib import Path

import matplotlib
from matplotlib import colors as mcolors

valid_chars = set(ascii_letters + digits + "_")


enum_template = """
class {name}(RgbTuple, Enum):
{vals}
""".strip()


def sanitise_name(s):
    s = s.strip().upper()
    if s[0] in digits:
        s = "_" + s
    s = s.replace('/', ' SLASH ')
    return "".join(c if c in valid_chars else "_" for c in s)


def make_key_fn(color_key_fn=mcolors.rgb_to_hsv):
    def fn(name_rgb):
        return tuple(color_key_fn(name_rgb[1])), name_rgb[0]
    return fn


def sort_color_mapping(mapping, key_fn=make_key_fn()):
    return {k: tuple(v) for k, v in sorted(mapping.items(), key=key_fn)}


def make_enum_code(name, mapping, name_fn=None):
    if name_fn is None:
        name_fn = lambda x: x

    rgb_mapping = {k: mcolors.to_rgb(v) for k, v in mapping.items()}

    vals = "\n".join(
        " " * 4 + f"{sanitise_name(name_fn(k))} = {v}"
        for k, v in sort_color_mapping(rgb_mapping).items()
    )
    return enum_template.format(name=name, vals=vals)


header_template = '''
"""Matplotlib's colors as enums. Generated automatically at {timestamp} with using Matplotlib v{version}"""
from enum import Enum
from .mixin import RgbTuple
'''.strip()


def grey_duplicates(mapping):
    out = dict()
    for k, v in mapping.items():
        out[k] = v
        if "grey" in k:
            out[k.replace("grey", "gray")] = v
        if "gray" in k:
            out[k.replace("gray", "grey")] = v
    return out


def make_module_code():
    elements = [
        header_template.format(
            timestamp=datetime.utcnow().isoformat(), version=matplotlib.__version__
        ),
        make_enum_code("BaseColor", mcolors.BASE_COLORS),
        make_enum_code("TableauColor", grey_duplicates(mcolors.TABLEAU_COLORS), lambda s: s[4:]),
        make_enum_code(
            "XkcdColor", grey_duplicates(mcolors.XKCD_COLORS), lambda s: s[5:]
        ),
        make_enum_code("Css4Color", mcolors.CSS4_COLORS),
        make_enum_code("Color", mcolors.get_named_colors_mapping()),
    ]
    return "\n\n\n".join(elements) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--stdout",
        action="store_true",
        help="Print output instead of writing to file (e.g. for dry runs)",
    )

    parsed = parser.parse_args()

    s = make_module_code()

    if parsed.stdout:
        print(s)
    else:
        tgt_path = Path(__file__).resolve().parent / "mpl_colors" / "generated.py"
        with open(tgt_path, "w") as f:
            f.write(s)


if __name__ == "__main__":
    main()
