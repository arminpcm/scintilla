#!/usr/bin/env python3

"""
Log ROS2 topics.

(c) 2023 Scintilla. All rights reserved.
Unauthorized reproduction, distribution, or disclosure of this material is strictly
prohibited without the express written permission of Scintilla.
"""

import subprocess
import sys
import os
import signal
import argparse
import yaml
from datetime import datetime
from pathlib import Path
import threading
from typing import List, Dict, Union

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from common.oslibs import info, error, get_environment_variable

class UserDescriptionPublisherNode(Node):
    def __init__(
        self,
        config: Dict[str, Union[str, List[str], float, int]],
        condition: threading.Condition,
        operator_name: str,
        description: str
    ) -> None:
        """
        Initialize the UserDescriptionPublisherNode.

        Args:
            config (dict): Configuration settings loaded from YAML file.
            condition (threading.Condition): Condition object for synchronization.
            operator_name (str): Name of the operator.
            description (str): Description of the rosmcap collection.

        Returns:
            None
        """
        super().__init__('user_description_publisher_node')

        self.operator_name = operator_name
        self.description = description

        self.config = config
        self.topic_name = self.config.get('description_topic', '/user_description')
        self.queue_length = self.config.get('topic_queue_length')
        self.description_publisher = self.create_publisher(String, self.topic_name, self.queue_length)

        self.timer_period = self.config.get('topic_frequency')  # seconds
        self.timer = self.create_timer(self.timer_period, self.publish_user_info)

        self.condition = condition

    def publish_user_info(self) -> None:
        """
        Publish user information on a specified ROS topic.

        Returns:
            None
        """
        if rclpy.ok():
            with self.condition:
                msg = String()
                msg.data = f"Operator: {self.operator_name}, Description: {self.description}"
                self.description_publisher.publish(msg)
        else:
            self.destroy_node()


def record_topics(config: Dict[str, Union[str, List[str], float, int]], condition: threading.Condition) -> None:
    """
    Record specified ROS2 topics.

    Args:
        config (dict): Configuration settings loaded from YAML file.
        condition (threading.Condition): Condition object for synchronization.

    Returns:
        None
    """
    with condition:
        # Configure the log file name
        base_file_name = config.get('base_file_name', 'output')
        log_directory = config.get('log_directory', 'output')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        root_dir = Path(get_environment_variable("SCINTILLA_ROOT"))

        mcap_file = root_dir / log_directory / f"{base_file_name}_{timestamp}"

        topics = config.get('recorded_topics', [])
        if not topics:
            error("No topics specified in the configuration file. Exiting.")
            sys.exit(1)

        command = ['ros2', 'bag', 'record', '-s', 'mcap', '--output', mcap_file]
        command.extend(topics)

        mcap_process = subprocess.Popen(command)
        info(f"Recording topics {topics} to {mcap_file}. Press Ctrl+C to stop recording.")

    try:
        mcap_process.wait()
    except KeyboardInterrupt:
        stop_record(mcap_process)


def stop_record(process: subprocess.Popen) -> None:
    """
    Stop the recording process.

    Args:
        process (subprocess.Popen): Recording process.

    Returns:
        None
    """
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGINT)
    except ProcessLookupError:
        # Process has already terminated, ignore the error
        pass
    process.communicate()


def show_mcap_info(mcap_file: str) -> None:
    """
    Display information about a recorded rosmcap.

    Args:
        mcap_file (str): Path to the recorded rosmcap file.

    Returns:
        None
    """
    subprocess.run(['ros2', 'mcap', 'info', mcap_file])


def load_config(config_file: str) -> Dict[str, Union[str, List[str], float, int]]:
    """
    Load configuration settings from a YAML file.

    Args:
        config_file (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration settings.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config


def check_config(config: Dict[str, Union[str, List[str], float, int]]) -> bool:
    """
    Check if the configuration file has all the required arguments.

    Args:
        config (dict): Configuration settings loaded from YAML file.

    Returns:
        bool: True if all required arguments are present, False otherwise.
    """
    required_keys = ['base_file_name', 'log_directory', 'recorded_topics', 'topic_frequency', 'topic_queue_length', 'description_topic']

    for key in required_keys:
        if key not in config:
            error(f"'{key}' is missing in the configuration file.")
            return False

    return True


def spin_in_thread(node: Node) -> None:
    """
    Spin a ROS2 node in a separate thread.

    Args:
        node (Node): The ROS2 node.

    Returns:
        None
    """
    while rclpy.ok():
        try:
            rclpy.spin_once(node)
        except Exception:
            info("Shutting down")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record ROS2 topics and manage recordings")
    parser.add_argument("config", help="Path to the YAML configuration file.")

    args = parser.parse_args()
    config_file = args.config

    config = load_config(config_file)

    if not check_config(config=config):
        error("Config file is missing important fields")
        sys.exit(1)

    rclpy.init()
    operator_name = input("Enter your name as the operator: ")
    description = input("Enter a description of what the rosmcap is being collected for: ")

    condition = threading.Condition()
    user_description_node = UserDescriptionPublisherNode(config, condition, operator_name, description)

    thread = threading.Thread(target=spin_in_thread, args=(user_description_node,), daemon=True)
    thread.start()

    try:
        with condition:
            input("Press Enter to start recording topics...")

        record_topics(config, condition)

    except KeyboardInterrupt:
        pass

    try:
        # Join but wait for 5 minutes before timing out
        thread.join(timeout=300)
        if rclpy.ok():
            rclpy.shutdown()
    except:
        pass