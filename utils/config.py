import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    _instance = None
    load_dotenv('.env')

    log_level: str = int(os.getenv('LOG_LEVEL', '10'))
    input_name: str = os.getenv('INPUT_NAME', '1')
    input_dir: str = os.getenv('INPUT_DIR', './input')
    output_dir: str = os.getenv('OUTPUT_DIR', './output')
    input_path: str = os.getenv('INPUT_PATH', f'{input_dir}/{input_name}.jpg')
    skeleton_path: str = os.getenv('SKELETON_PATH', f'{output_dir}/{input_name}-skeleton.png')
    graph_path: str = os.getenv('GRAPH_PATH', f'{output_dir}/{input_name}-graph.png')
    small_component_threshold: int = int(os.getenv('SMALL_COMPONENT_THRESHOLD', '30'))
    neighbor_component_min_size: int = int(os.getenv('NEIGHBOR_COMPONENT_MIN_SIZE', '50'))
    neighbor_component_max_distance: int = int(os.getenv('NEIGHBOR_COMPONENT_MAX_DISTANCE', '100'))
    large_component_max_size: int = int(os.getenv('LARGE_COMPONENT_MAX_SIZE', '1000'))
    default_canvas_size: int = int(os.getenv('DEFAULT_CANVAS_SIZE', '1000'))
    adjlist_output_path: str = os.getenv('ADJLIST_PATH', '1000')
    alpha: int = int(os.getenv('alpha', '5'))
    min_keep_percentage: int = int(os.getenv('NODES_MIN_PERCENTAGE_TO_KEEP', '3'))
    max_keep_percentage: int = int(os.getenv('NODES_MAX_PERCENTAGE_TO_KEEP', '5'))

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __str__(self):
        return f''' Config(
        log_level: {self.log_level},
        input_name: {self.input_name},
        input_dir: {self.input_dir},
        output_dir: {self.output_dir},
        input_path: {self.input_path},
        skeleton_path: {self.skeleton_path},
        graph_path: {self.graph_path},
        small_component_threshold: {self.small_component_threshold},
        neighbor_component_min_size: {self.neighbor_component_min_size},
        neighbor_component_max_distance: {self.neighbor_component_max_distance},
        large_component_max_size: {self.large_component_max_size},
        adjlist_output_path: {self.adjlist_output_path},
        min_keep_percentage:{self.min_keep_percentage},
        max_keep_percentage:{self.max_keep_percentage},
        )'''
