import logging
from loguru import logger
from pathlib import Path
from primitive_pal import process_vcd

logger.enable("primitive")
FORMAT = "%(asctime)-15s | %(levelname)s %(name)s | %(filename)s:%(lineno)d %(message)s"
logging.basicConfig(format=FORMAT)
logging.getLogger().setLevel(logging.INFO)
