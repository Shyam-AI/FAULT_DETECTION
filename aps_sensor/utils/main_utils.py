from aps_sensor.logger import logging
from aps_sensor.exception import SensorException
import yaml
import os, sys


def read_yaml(filepath:str)->dict:
    try:
        with open(filepath, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e, sys)


def write_yaml_file(file_path: str, content: str, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove()
        
        os.makedirs(os.path.dirname(file_path), exist_ok = True)

        with open(file_path, "w") as f:
            yaml.dump(content, f)

    except Exception as e:
        raise SensorException(e, sys)
