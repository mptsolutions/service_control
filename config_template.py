from logging import INFO
from pathlib import Path

# Log settings
LOG_LEVEL = INFO
LOG_FILE_PATH = Path(__file__).parents[1] / "service_control.log"
LOG_FILE_MODE = "w"

SERVICES = [
    ""
]
