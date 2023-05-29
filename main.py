import logging
import os

from dotenv import load_dotenv

from utils.config import Config

if __name__ == '__main__':
    load_dotenv('.env')
    config = Config()

    logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(funcName)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=config.log_level)
    logger = logging.getLogger(__name__)

    logger.info(f"Loaded configurations:{config}")
