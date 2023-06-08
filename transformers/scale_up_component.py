import math

import networkx as nx
import numpy as np

from utils.config import Config


class ComponentScaler:
    def __init__(self, component_graph: nx.Graph):
        config = Config()
        self.component_graph = component_graph
        self.default_canvas_size: int = config.default_canvas_size
        self.x1, self.y1 = np.inf, np.inf
        self.x2, self.y2 = -np.inf, -np.inf
        for x, y in component_graph.nodes:
            self.x1 = min(self.x1, x)
            self.y1 = min(self.y1, y)
            self.x2 = max(self.x2, x)
            self.y2 = max(self.y2, y)
        self.width = self.x2 - self.x1
        self.height = self.y2 - self.y1

        self.width_factor = 1
        self.height_factor = 1

        if math.isinf(self.width) or self.width == 0:
            self.width = 1
            self.x1 = 0
        if math.isinf(self.height) or self.height == 0:
            self.height = 1
            self.y1 = 0

        if self.width > self.height:
            self.width_factor = self.default_canvas_size / self.width
            self.height_factor = self.default_canvas_size / self.width
        else:
            self.width_factor = self.default_canvas_size / self.height
            self.height_factor = self.default_canvas_size / self.height

    def scale(self):
        mapping = dict()
        for x, y in self.component_graph.nodes():
            scaled_x = math.floor((x - self.x1) * self.width_factor)
            scaled_y = math.floor((y - self.y1) * self.height_factor)
            mapping.update({
                (x, y): (scaled_x, scaled_y)
            })
        self.component_graph = nx.relabel_nodes(self.component_graph, mapping)
        return self.component_graph
