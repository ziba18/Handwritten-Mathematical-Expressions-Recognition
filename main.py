import logging
import math

import networkx as nx

from processors import image_processor
from processors.graph_processor import GraphProcessor
from transformers.scale_up_component import ComponentScaler
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
    for component in nx.connected_components(graph_processor.graph):
        component_graph: nx.Graph = graph_processor.graph.subgraph(component).copy()

        graph_size = component_graph.number_of_nodes()
        component_graph = graph_processor.reduce_graph_size(
            component_graph,
            (graph_size * config.min_keep_percentage) // 100,
            (graph_size * config.max_keep_percentage) // 100
        )
        component_graph = graph_processor.dfs_reduce_graph_size(component_graph)
        scaled_component = ComponentScaler(component_graph).scale()
        nx.write_adjlist(scaled_component, config.adjlist_output_path, delimiter="|")
        graph_processor.convert_graph_to_cv2_image_graph(scaled_component, color=(0, 0, 255), size=3)

    # graph_processor.plot_graph()
    # graph_processor.convert_graph_to_cv2_image()
