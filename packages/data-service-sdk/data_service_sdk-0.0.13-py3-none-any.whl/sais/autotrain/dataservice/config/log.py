import logging

from sais.autotrain.dataservice.config.const import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)
logging.basicConfig(level=logging.INFO)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(name)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)