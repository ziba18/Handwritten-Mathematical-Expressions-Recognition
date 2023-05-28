from __future__ import annotations

import math

import networkx as nx
from scipy.spatial import KDTree

from utils.config import Config


class ComponentBounds:
    def __init__(self, component: set[tuple[int, int]]):
        self.size = len(component)
        self.x1 = self.y1 = math.inf
        self.x2 = self.y2 = -math.inf
        for x, y in component:
            self.x1 = min(self.x1, x)
            self.y1 = min(self.y1, y)
            self.x2 = max(self.x2, x)
            self.y2 = max(self.y2, y)


class ComponentRemover:
    def __init__(self, graph: nx.Graph):
        config = Config()
        self.graph = graph
        self.bounds = [ComponentBounds(comp) for comp in nx.connected_components(self.graph)]
        self._small_component_threshold = config.small_component_threshold
        self._neighbor_component_min_size = config.neighbor_component_min_size
        self._neighbor_component_max_distance = config.neighbor_component_max_distance
        self._large_component_max_size = config.large_component_max_size

    def _remove_bound(self, component):
        target = ComponentBounds(component)
        for bound in self.bounds:
            if bound.x1 == target.x1 and bound.x2 == target.x2 and \
                    bound.y1 == target.y1 and bound.y2 == target.y2:
                self.bounds.remove(bound)

    def _find_nearest_component(self, component) -> ComponentBounds | None:
        target_bound = ComponentBounds(component)
        target_point = (target_bound.x1, target_bound.y1, target_bound.x2, target_bound.y2)
        points = [(bound.x1, bound.y1, bound.x2, bound.y2) for bound in self.bounds]
        tree = KDTree(points)
        distances, indexes = tree.query(target_point, k=8, distance_upper_bound=self._neighbor_component_max_distance)
        for distance, index in zip(distances, indexes):
            if distance == 0 or distance == float('inf'):
                continue
            bound = self.bounds[index]
            if bound.size >= self._neighbor_component_min_size:
                return bound

        return None

    def remove_large_components(self):
        large_components = [comp for comp in nx.connected_components(self.graph) if
                            len(comp) > self._large_component_max_size]
        for large_component in large_components:
            self._remove_bound(large_component)
            nodes = set.union(*large_components)
            self.graph.remove_nodes_from(nodes)

    def remove_small_components(self):
        small_components = [comp for comp in nx.connected_components(self.graph) if
                            len(comp) < self._small_component_threshold]
        if small_components:
            for small_component in small_components:
                neighbor = self._find_nearest_component(small_component)
                if not neighbor:
                    self.graph.remove_nodes_from(small_component)
                self._remove_bound(small_component)
