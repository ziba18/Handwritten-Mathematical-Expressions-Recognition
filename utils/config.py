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
        )'''
