"""
The default group of operations that pyrelist has
"""
import sys
import json
import re
import pylogconf.core
from pytconf import register_endpoint, register_main, config_arg_parse_and_launch, get_free_args
from pyrelist.configs import ConfigMatch
from pyrelist.static import DESCRIPTION, APP_NAME, VERSION_STR


@register_endpoint(
    description="Match a collection of regexps against a file",
    configs=[
        ConfigMatch,
    ],
    allow_free_args=True,
    min_free_args=1,
)
def match() -> None:
    # read the regex patterns
    with open(ConfigMatch.patterns, "r", encoding="utf8") as stream:
        data = json.load(stream)
    elems = []
    for datum in data:
        elems.append(re.compile(datum))
    found = False
    for file in get_free_args():
        with open(file, "r", encoding="utf8") as stream:
            for line_number, line in enumerate(stream):
                for elem in elems:
                    if elem.search(line):
                        print(f"{file}:{line_number}: {line}", file=sys.stderr)
                        found = True
    if found:
        code = 1
    else:
        code = 0
    sys.exit(code)


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    pylogconf.core.setup()
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
