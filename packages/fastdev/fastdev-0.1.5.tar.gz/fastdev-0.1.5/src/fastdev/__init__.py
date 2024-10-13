import logging

import rich
from rich.logging import RichHandler

rich.reconfigure(log_path=False)

logger = logging.getLogger("fastdev")
logger.propagate = False
logger.setLevel("INFO")
logger.addHandler(RichHandler(console=rich.get_console(), show_path=False, log_time_format="[%X]"))
