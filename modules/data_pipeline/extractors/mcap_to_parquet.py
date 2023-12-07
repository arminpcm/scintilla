#!/usr/bin/env python3

"""
Convert .mcap files to parquet files.

(c) 2023 Scintilla. All rights reserved.
Unauthorized reproduction, distribution, or disclosure of this material is strictly
prohibited without the express written permission of Scintilla.
"""

import argparse
import yaml
from common.oslibs import info
from typing import Dict, Union, List, Any, Tuple
import os
import shutil
import open3d as o3d
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import cv2

import rosbag2_py
from sensor_msgs.msg import Image, PointCloud2
from stereo_msgs.msg import DisparityImage
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message


from data_pipeline.extractors.convertors.convertor_loader import load_convertors


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


def read_messages(input_bag: str, topics: List[str]) -> List[Tuple[str, Any, str, int]]:
    """
    Read messages from a ROS bag file for specified topics.

    Parameters:
        input_bag (str): Path to the ROS bag file.
        topics (List[str]): List of topic names to read.

    Yields:
        Tuple[str, Any, str, int]: A tuple containing topic name, message, message type, and timestamp.

    Raises:
        ValueError: If the specified topic is not found in the bag.

    Example:
        >>> for topic, msg, msg_type, timestamp in read_messages('example.bag', ['topic1', 'topic2']):
        ...     print(f"Topic: {topic}, Type: {msg_type}, Timestamp: {timestamp}")
        ...     print(f"Message: {msg}")
    """
    reader = rosbag2_py.SequentialReader()
    reader.open(
        rosbag2_py.StorageOptions(uri=input_bag, storage_id="mcap"),
        rosbag2_py.ConverterOptions(
            input_serialization_format="cdr", output_serialization_format="cdr"
        ),
    )

    topic_types = reader.get_all_topics_and_types()

    def typename(topic_name: str) -> str:
        """
        Get the message type for a specified topic.

        Parameters:
            topic_name (str): Name of the topic.

        Returns:
            str: The message type.

        Raises:
            ValueError: If the specified topic is not found in the bag.
        """
        for topic_type in topic_types:
            if topic_type.name == topic_name:
                return topic_type.type
        raise ValueError(f"topic {topic_name} not in bag")

    while reader.has_next():
        topic, data, timestamp = reader.read_next()
        if topic in topics:
            msg_type = get_message(typename(topic))
            msg = deserialize_message(data, msg_type)
            yield topic, msg, msg_type, timestamp
    del reader


def create_topic_directories(output_directory, topics) -> None:
    # Delete the entire directory if it exists
    try:
        shutil.rmtree(output_directory)
    except FileNotFoundError:
        pass  # Ignore if the directory doesn't exist
    for topic in topics:
        # Create the output directory if it doesn't exist
        topic_directory = os.path.join(output_directory, topic.lstrip('/').replace('/', os.path.sep))
        info(f'Deleting and creating directory: {topic_directory}')

        # Create the directory
        os.makedirs(topic_directory, exist_ok=True)



def save_as_parquet(topic, metadata, converted_message, output_directory):
    topic_directory = os.path.join(output_directory, topic.lstrip('/').replace('/', os.path.sep))

    # Load the converted_message into a DataFrame
    converted_message_df = pd.DataFrame(converted_message, columns=metadata)

    # Create or append to the Parquet file
    parquet_file_path = os.path.join(topic_directory, 'data.parquet')
    header_written = False

    if os.path.exists(parquet_file_path):
        # Append to existing Parquet file
        existing_table = pq.read_table(parquet_file_path)

        # Check if the schema matches
        if existing_table.schema.equals(pa.Table.from_pandas(converted_message_df).schema):
            new_table = pa.Table.from_pandas(converted_message_df)
            new_table = pa.concat_tables([existing_table, new_table])
            header_written = True
        else:
            raise ValueError('Schema for the message has changed!')
    else:
        # Create a new Parquet file
        new_table = pa.Table.from_pandas(converted_message_df)
        header_written = True

    # Write the table to the Parquet file
    pq.write_table(new_table, parquet_file_path, write_statistics=not header_written)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert mcap files to parquet')
    parser.add_argument('mcap', help='Path to the mcap file.')
    parser.add_argument('-c', '--config', help='Path to the mcap file.', default='data/config/mcap_to_parquet.yaml')
    args = parser.parse_args()

    config_file = args.config
    config = load_config(config_file)

    output_directory = config.get('output_directory')
    log_name = os.path.basename(os.path.dirname(args.mcap))
    output_directory = os.path.join(output_directory, log_name)

    topics = config.get('extracted_topics', [])

    stats_dict: Dict = {}
    topic_dict: Dict = {}
    counter = 0

    info('Loading message convertors')
    convertor_config_file = config.get('convertors')
    convertors = load_convertors(convertor_config_file)
    info(convertors)

     # Create all topic directories first
    create_topic_directories(output_directory, topics)

    for topic, msg, msg_type, timestamp in read_messages(args.mcap, topics):
        if topic in convertors.keys():
            info(f'Converting {topic} ({msg_type}): @ stamp [{timestamp}]')
            converted_message = convertors[topic].convert(msg)
            try:
                stats_dict[topic] = stats_dict[topic] + 1
            except:
                stats_dict[topic] = 1
            counter = counter + 1
            info(f'couter: {counter}')

            metadata = convertors[topic].header

            if msg_type == PointCloud2:
                # Save as a PCD
                o3d.io.write_point_cloud(os.path.join(output_directory, f'{topic.lstrip("/")}/{timestamp}.pcd'), converted_message[1])
                save_as_parquet(topic, metadata, converted_message[0], output_directory)
            elif msg_type == Image or msg_type == DisparityImage:
                # Save as an image
                cv2.imwrite(os.path.join(output_directory, f'{topic.lstrip("/")}/{timestamp}.png'), converted_message[1])
                save_as_parquet(topic, metadata, converted_message[0], output_directory)
            else:
                # Save parquet
                save_as_parquet(topic, metadata, converted_message, output_directory)

        else:
            info(f'No extractors are provided for {topic}:{msg_type}')
    

