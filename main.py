import logging

from processors import image_processor
from processors.graph_processor import GraphProcessor
from utils.config import Config

if __name__ == '__main__':
    config = Config()
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(funcName)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=config.log_level)
    logger = logging.getLogger(__name__)
    logger.info(f"Loaded configurations:{config}")

    skeleton = image_processor.process_image()
    graph_processor = GraphProcessor(skeleton)
    graph_processor.process_graph()
    graph_processor.plot_graph()
    graph_processor.convert_graph_to_cv2_image()
