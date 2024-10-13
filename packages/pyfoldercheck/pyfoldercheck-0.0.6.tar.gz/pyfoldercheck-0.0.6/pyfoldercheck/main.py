import json
import os

import pylogconf.core
from pytconf import register_endpoint, register_main, config_arg_parse_and_launch

from pyfoldercheck.configs import ConfigRepository, ConfigNames, Authorized
from pyfoldercheck.static import APP_NAME, VERSION_STR, DESCRIPTION
from pyfoldercheck.utils import is_ascii, add_non_ascii


def scan_files():
    bad_characters = set()
    count = 0
    for root, directories, files in os.walk(ConfigRepository.folder):
        for file in files:
            if 'á' in file:
                full = os.path.join(root, file)
                print(file, full)
                count += 1
            if not is_ascii(file, Authorized.chars_ok_for_files):
                # full = os.path.join(root, file)
                # print(file, full)
                add_non_ascii(bad_characters, file)
        for directory in directories:
            if not is_ascii(directory, Authorized.chars_ok_for_folders):
                full = os.path.join(root, directory)
                print(f"folder [{full}]")
    return bad_characters, count


@register_endpoint(
    description="Scan the folder",
    configs=[
        ConfigRepository,
    ],
)
def scan() -> None:
    bad_characters, count = scan_files()
    print(bad_characters)
    print(f"found [{count}] appearances")


@register_endpoint(
    description="Authorize words with non ascii in them",
    configs=[
        ConfigRepository,
        ConfigNames,
    ],
)
def review_not_ascii() -> None:
    """
    Only checks for name not previously authorized
    """
    # read the previous repository
    with open(ConfigNames.repository) as f:
        repository = json.load(f)
    scan_files()
    # write the repository back
    with open(ConfigNames.repository, "w") as f:
        json.dump(repository, f)


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    pylogconf.core.setup()
    config_arg_parse_and_launch()


if __name__ == '__main__':
    main()
