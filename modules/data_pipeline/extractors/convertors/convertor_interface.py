#!/usr/bin/env python3

"""
Convertor Interface that subclasses would inherit from.

(c) 2023 Scintilla. All rights reserved.
Unauthorized reproduction, distribution, or disclosure of this material is strictly
prohibited without the express written permission of Scintilla.
"""

from typing import Any, Dict, List
from copy import deepcopy

class ConvertorInterface:
    def __init__(self, config: Dict[str, Any] = None):
        self.__config = config

    @property
    def header() -> List:
        raise NotImplementedError('Subclasses must implement the convert method.')

    @property
    def config(self) -> Dict[str, Any]:
        return deepcopy(self.__config)

    def convert(self, data: Any):
        raise NotImplementedError('Subclasses must implement the convert method.')
