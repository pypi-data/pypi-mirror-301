import logging
import sys

# Set logger with proper format for backend parsing to status page
from .constants import LOGGER_NAME

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
log = logging.Logger(LOGGER_NAME)

logger_handler = logging.StreamHandler()
logger_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(logger_handler)

# Import the methods
from .DatalakeHandler import *
from .TaskHandler import *
from .StatusHandler import *
from .Timeseries import *
from .ExceptionHandler import *
