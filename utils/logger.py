import logging
import os
import tempfile


def setup_logging():
    """
    Configures application-wide logging to a file under the OS temp directory.
    Needed because the packaged exe runs with console disabled
    (--windows-console-mode=disable in build.bat), so print() output is otherwise lost.
    """
    log_path = os.path.join(tempfile.gettempdir(), "converter.log")
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        encoding="utf-8",
    )
    return log_path
