#!/usr/bin/env python3

"""
Loads the convertor modules implemented by uers.

(c) 2023 Scintilla. All rights reserved.
Unauthorized reproduction, distribution, or disclosure of this material is strictly
prohibited without the express written permission of Scintilla.
"""

from importlib import import_module
import yaml
from typing import Dict
from data_pipeline.extractors.convertors.convertor_interface import ConvertorInterface

def load_convertors(config_file: str) -> Dict[str, ConvertorInterface]:
    """
    Load convertors based on a YAML configuration file.

    :param config_file: The path to the YAML configuration file.
    :return: A dictionary of instantiated conversion classes.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    convertors = {}

    for convertor_config in config.get('convertors', []):
        convertor_class_path = convertor_config.get('name')

        module_name, class_name = convertor_class_path.rsplit('.', 1)
        module = import_module(module_name)
        convertor_class = getattr(module, class_name)

        # Ensure the class implements the ConvertorInterface
        if issubclass(convertor_class, ConvertorInterface):
            convertor_instance: ConvertorInterface = convertor_class(convertor_config)
            for topic in convertor_config.get('topics'):
                convertors[topic] = convertor_instance
        else:
            raise ValueError(f"{convertor_class_path} must implement ConvertorInterface.")

    return convertors
