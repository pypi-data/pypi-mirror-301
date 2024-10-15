# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import logging
from pathlib import Path
from typing import Iterable, List

from fm_weck.engine import RESERVED_LOCATIONS


def mountable_absolute_paths_of_command(command: List[str]) -> Iterable[Path]:
    """
    Iterate over all arguments in command and find those that are paths.
    The paths are returned as absolute paths, that already exist on the host.
    """

    no_mount = {"/", "/dev", "/proc", "/sys"}

    command_iter = (arg for arg in command if arg not in no_mount)
    for arg in command_iter:
        if arg in RESERVED_LOCATIONS:
            logging.warning("Ignoring reserved path %s. This path is internally used and mounted by fm-weck.", arg)

        path = Path(arg)
        if path.exists() and path.is_absolute():
            yield path
