import cv2
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from processors.component_remover import ComponentRemover
from utils.config import Config
from utils.degree_difference import calculate_degree_difference


class GraphProcessor:
    def __init__(self, skeleton):
        self.graph = nx.Graph()
        self.skeleton = skeleton
        self.rows = self.skeleton.shape[0]
        self.columns = self.skeleton.shape[1]
        self._graph_path = Config().graph_path
        self.canvas_size = Config().default_canvas_size

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
        component_remover = ComponentRemover(self.graph)
        component_remover.remove_large_components()
        component_remover.remove_small_components()

    @staticmethod
    def dfs_reduce_graph_size(g):
        graph = g.copy()
        nodes_to_remove = set()
        dfs_edges = list(nx.dfs_edges(graph))
        base_edge = None
        for edge in dfs_edges:
            if base_edge is None:
                base_edge = edge
                continue

            if calculate_degree_difference(base_edge, edge) > 15.0:
                base_edge = edge
                continue

            nodes_to_remove.add(edge[0])

        for node in nodes_to_remove:
            neighbors = list(graph.neighbors(node))
            if len(neighbors) == 2:
                graph.add_edge(neighbors[0], neighbors[1])
                graph.remove_node(node)
        return graph

    def dfs_reduce_size(self):
        self.dfs_reduce_graph_size(self.graph)

    @staticmethod
    def reduce_graph_size(g, min_lower_bound_size: int, desired_upper_bound_size: int):
        graph = g.copy()
        if min_lower_bound_size < 25:
            min_lower_bound_size = 25
        if desired_upper_bound_size < min_lower_bound_size:
            desired_upper_bound_size = min_lower_bound_size * 2

        if graph.number_of_nodes() <= desired_upper_bound_size:
            return graph

        degree_2_nodes = {node for node, degree in graph.degree() if degree == 2}

        while graph.number_of_nodes() > desired_upper_bound_size:
            candidates = degree_2_nodes.copy()
            if len(candidates) == 0:
                break
            nodes_to_remove = set()
            while len(candidates) > 0:
                node = candidates.pop()
                neighbors = list(graph.neighbors(node))
                graph.add_edge(neighbors[0], neighbors[1])
                nodes_to_remove.add(node)
                degree_2_nodes.remove(node)
                candidates.difference_update(neighbors)
            if graph.number_of_nodes() - len(nodes_to_remove) < min_lower_bound_size:
                break
            graph.remove_nodes_from(nodes_to_remove)

        return graph

    def reduce_size(self, min_lower_bound_size: int, desired_upper_bound_size: int):
        return self.reduce_graph_size(self.graph, min_lower_bound_size, desired_upper_bound_size)

    def plot_graph(self):
        pos = {(x, y): (y, self.rows - x) for x, y in self.graph.nodes}

        nx.draw_networkx_nodes(self.graph, pos, node_size=1, node_color='red')
        plt.tight_layout()
        plt.show()

    def convert_graph_to_cv2_image_graph(self, graph: nx.Graph, color=(0, 0, 0), size: int = 1):
        output = np.ones((self.canvas_size, self.canvas_size, 3), np.uint8) * 255

        for x, y in graph.nodes:
            cv2.circle(output, (y, x), size, color, -1)

        for u, v in graph.edges:
            x1, y1 = u
            x2, y2 = v
            cv2.line(output, (y1, x1), (y2, x2), (0, 0, 0), 1)

        cv2.imwrite(self._graph_path, output)

    def convert_graph_to_cv2_image(self):
        output = np.ones((self.rows, self.columns, 3), np.uint8) * 255

        for x, y in self.graph.nodes:
            cv2.circle(output, (y, x), 1, (0, 0, 0), -1)

        cv2.imwrite(self._graph_path, output)
