# Copyright 2023 Marimo. All rights reserved.
import os
import subprocess
import sys
from typing import Optional

if sys.version_info < (3, 9):
    from importlib_resources import files as importlib_files
else:
    from importlib.resources import files as importlib_files

from marimo import _loggers

LOGGER = _loggers.marimo_logger()


def start_lsp(port: int) -> Optional[subprocess.Popen[bytes]]:
    lsp_process: Optional[subprocess.Popen[bytes]] = None
    lsp_bin = os.path.join(
        str(importlib_files("marimo").joinpath("_lsp")),
        "index.js",
    )
    cmd = f"node {lsp_bin} --port {port}"
    try:
        lsp_process = subprocess.Popen(
            cmd.split(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
    except Exception as e:
        LOGGER.error(
            "When starting language server (%s), got error: %s", cmd, e
        )

    return lsp_process
