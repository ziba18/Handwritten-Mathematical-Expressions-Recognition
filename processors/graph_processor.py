import cv2
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from utils.config import Config


class GraphProcessor:
    def __init__(self, skeleton):
        self.graph = nx.Graph()
        self.skeleton = skeleton
        self.rows = self.skeleton.shape[0]
        self.columns = self.skeleton.shape[1]
        self.graph_path = Config().graph_path

    def process_graph(self):
        for x, row in enumerate(self.skeleton):
            for y, value in enumerate(row):
                if value:
                    neighbors = [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
                    for neighbor in neighbors:
                        try:
                            if self.skeleton[neighbor]:
                                self.graph.add_edge((x, y), neighbor)
                        except IndexError:
                            continue

    def plot_graph(self):
        pos = {(x, y): (y, self.rows - x) for x, y in self.graph.nodes}

        nx.draw_networkx_nodes(self.graph, pos, node_size=1, node_color='red')
        plt.tight_layout()
        plt.show()

    def convert_graph_to_cv2_image(self):
        output = np.ones((self.rows, self.columns, 3), np.uint8) * 255

        for x, y in self.graph.nodes:
            cv2.circle(output, (y, x), 1, (0, 0, 0), -1)

        cv2.imwrite(self.graph_path, output)
        print(self.graph)
