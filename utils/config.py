import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    _instance = None

    log_level: str = int(os.getenv('LOG_LEVEL', '10'))

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __str__(self):
        return f''' Config(
        LOG_LEVEL: {self.log_level}
        )'''

