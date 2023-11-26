#!/usr/bin/env python3

"""
Log ROS2 topics.

(c) 2023 Scintilla. All rights reserved.
Unauthorized reproduction, distribution, or disclosure of this material is strictly
prohibited without the express written permission of Scintilla.
"""


import os
from typing import Dict

# ANSI Escape Code Colors
COLORS: Dict[str, str] = {
    'RESET': '\033[0m',
    'BLACK': '\033[0;30m',
    'RED': '\033[0;31m',
    'GREEN': '\033[0;32m',
    'YELLOW': '\033[0;33m',
    'BLUE': '\033[0;34m',
    'PURPLE': '\033[0;35m',
    'CYAN': '\033[0;36m',
    'WHITE': '\033[0;37m',
}


def get_environment_variable(variable_name: str) -> str:
    """
    Get the value of an environment variable.

    Args:
        variable_name (str): Name of the environment variable.

    Returns:
        str: Value of the environment variable, or an empty string if not found.
    """
    try:
        variable_value = os.environ[variable_name]
        return variable_value
    except KeyError:
        print(f"Environment variable '{variable_name}' not found.")
        return ""

def error(message: str) -> None:
    """
    Print an error message in red.

    Args:
        message (str): The error message.

    Returns:
        None
    """
    print(f"{COLORS['RED']}[Error]: {message}{COLORS['RESET']}")

def warning(message: str) -> None:
    """
    Print a warning message in yellow.

    Args:
        message (str): The warning message.

    Returns:
        None
    """
    print(f"{COLORS['YELLOW']}[Warning]: {message}{COLORS['RESET']}")

def info(message: str) -> None:
    """
    Print an info message in light blue.

    Args:
        message (str): The info message.

    Returns:
        None
    """
    print(f"{COLORS['CYAN']}[Info]: {message}{COLORS['RESET']}")