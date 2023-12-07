#!/usr/bin/env python3

"""
Loads the convertor modules implemented by uers.

(c) 2023 Scintilla. All rights reserved.
Unauthorized reproduction, distribution, or disclosure of this material is strictly
prohibited without the express written permission of Scintilla.
"""

from data_pipeline.extractors.convertors.convertor_interface import ConvertorInterface
from typing import Any, Dict, List, Tuple
from copy import deepcopy
import numpy as np
from cv_bridge import CvBridge
import open3d as o3d
from ctypes import *

from sensor_msgs.msg import MagneticField, Imu, CameraInfo, FluidPressure, Temperature, Image, PointCloud2, PointField
from geometry_msgs.msg import PoseStamped, PoseWithCovariance, TwistWithCovariance, Pose, Twist, TransformStamped, PoseWithCovarianceStamped
from nav_msgs.msg import Path, Odometry
from tf2_msgs.msg import TFMessage
from visualization_msgs.msg import Marker
from diagnostic_msgs.msg import DiagnosticArray
from std_msgs.msg import String
from rcl_interfaces.msg import Log
from shape_msgs.msg import Mesh
from geometry_msgs.msg import Polygon
from stereo_msgs.msg import DisparityImage
from sensor_msgs_py import point_cloud2

from zed_interfaces.msg import PosTrackStatus, DepthInfoStamped, PlaneStamped

class MagneticFieldConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any]=None) -> None:
        super().__init__(config)
        self.__header = ['header/sec', 'header/nanosec', 'header/frame_id',
                         'magnetic_field/x', 'magnetic_field/y', 'magnetic_field/z',
                         'magnetic_field_covariance/0', 'magnetic_field_covariance/1', 'magnetic_field_covariance/2',
                         'magnetic_field_covariance/3', 'magnetic_field_covariance/4', 'magnetic_field_covariance/5',
                         'magnetic_field_covariance/6', 'magnetic_field_covariance/7', 'magnetic_field_covariance/8']

    @property
    def header(self) -> List:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: MagneticField) -> List:
        """
        Convert a MagneticField instance to a single-row list.

        :param data: MagneticField instance
        :return: List containing the converted data
        """
        # Check if data is of type MagneticField
        assert isinstance(data, MagneticField), "Input data must be of type MagneticField."

        header_data = [data.header.stamp.sec, data.header.stamp.nanosec, data.header.frame_id]
        magnetic_field_data = [data.magnetic_field.x, data.magnetic_field.y, data.magnetic_field.z]
        covariance_data = data.magnetic_field_covariance

        converted_data = list(header_data) + list(magnetic_field_data) + list(covariance_data)
        assert len(converted_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'
        
        return [converted_data]

class IMUConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = [
            "header/sec", "header/nanosec", "header/frame_id",
            "orientation/x", "orientation/y", "orientation/z", "orientation/w",
            "orientation_covariance/0", "orientation_covariance/1", "orientation_covariance/2",
            "orientation_covariance/3", "orientation_covariance/4", "orientation_covariance/5",
            "orientation_covariance/6", "orientation_covariance/7", "orientation_covariance/8",
            "angular_velocity/x", "angular_velocity/y", "angular_velocity/z",
            "angular_velocity_covariance/0", "angular_velocity_covariance/1", "angular_velocity_covariance/2",
            "angular_velocity_covariance/3", "angular_velocity_covariance/4", "angular_velocity_covariance/5",
            "angular_velocity_covariance/6", "angular_velocity_covariance/7", "angular_velocity_covariance/8",
            "linear_acceleration/x", "linear_acceleration/y", "linear_acceleration/z",
            "linear_acceleration_covariance/0", "linear_acceleration_covariance/1", "linear_acceleration_covariance/2",
            "linear_acceleration_covariance/3", "linear_acceleration_covariance/4", "linear_acceleration_covariance/5",
            "linear_acceleration_covariance/6", "linear_acceleration_covariance/7", "linear_acceleration_covariance/8",
        ]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: Imu) -> List:
        """
        Convert an IMU measurement instance to a single-row list.

        :param data: IMU measurement instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, Imu), "Input data must be of type Imu."

        header_data = [data.header.stamp.sec, data.header.stamp.nanosec, data.header.frame_id]

        orientation_data = [data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]
        orientation_covariance_data = data.orientation_covariance

        angular_velocity_data = [data.angular_velocity.x, data.angular_velocity.y, data.angular_velocity.z]
        angular_velocity_covariance_data = data.angular_velocity_covariance

        linear_acceleration_data = [data.linear_acceleration.x, data.linear_acceleration.y, data.linear_acceleration.z]
        linear_acceleration_covariance_data = data.linear_acceleration_covariance

        converted_data = (
            list(header_data) +
            list(orientation_data) +
            list(orientation_covariance_data) +
            list(angular_velocity_data) +
            list(angular_velocity_covariance_data) +
            list(linear_acceleration_data) +
            list(linear_acceleration_covariance_data)
        )

        # Use assert to check the length of converted_data
        assert len(converted_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [converted_data]


class PoseConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = [
            "header/sec", "header/nanosec", "header/frame_id",
            "pose/position/x", "pose/position/y", "pose/position/z",
            "pose/orientation/x", "pose/orientation/y", "pose/orientation/z", "pose/orientation/w"
        ]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: PoseStamped) -> List:
        """
        Convert a Pose message instance to a single-row list.

        :param data: Path message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, PoseStamped), "Input data must be of type Path."

        header_data = [data.header.stamp.sec, data.header.stamp.nanosec, data.header.frame_id]

        position_data = [data.pose.position.x, data.pose.position.y, data.pose.position.z]
        orientation_data = [data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w]

        converted_data = list(header_data) + list(position_data) + list(orientation_data)

        # Use assert to check the length of converted_data
        assert len(converted_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [converted_data]

class PathConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = [
            "header/sec", "header/nanosec", "header/frame_id",
            "poses/header/sec", "poses/header/nanosec", "poses/header/frame_id",
            "poses/pose/position/x", "poses/pose/position/y", "poses/pose/position/z",
            "poses/pose/orientation/x", "poses/pose/orientation/y", "poses/pose/orientation/z", "poses/pose/orientation/w"
        ]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: Path) -> List:
        """
        Convert a Path message instance to a single-row list.

        :param data: Path message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, Path), "Input data must be of type Path."

        header_data = list([data.header.stamp.sec, data.header.stamp.nanosec, data.header.frame_id])

        poses_data = []
        for pose_stamped in data.poses:
            pose_data = self._extract_pose_data(pose_stamped)
            poses_data.append(header_data + pose_data)

        converted_data = poses_data

        # Use assert to check the length of converted_data
        assert len(converted_data[0]) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return converted_data

    def _extract_pose_data(self, pose: PoseStamped) -> List:
        """
        Extract and return a list of data from a Pose message.

        :param pose: PoseStamped message instance
        :return: List containing the extracted pose data
        """
        header_data = [pose.header.stamp.sec, pose.header.stamp.nanosec, pose.header.frame_id]
        position_data = [pose.pose.position.x, pose.pose.position.y, pose.pose.position.z]
        orientation_data = [pose.pose.orientation.x, pose.pose.orientation.y, pose.pose.orientation.z, pose.pose.orientation.w]
        return list(header_data) + list(position_data) + list(orientation_data)


class OdometryConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = [
            "header/sec", "header/nanosec", "header/frame_id", "child_frame_id",
            "pose/pose/position/x", "pose/pose/position/y", "pose/pose/position/z",
            "pose/pose/orientation/x", "pose/pose/orientation/y", "pose/pose/orientation/z", "pose/pose/orientation/w",
            "pose/covariance/0", "pose/covariance/1", "pose/covariance/2", "pose/covariance/3",
            "pose/covariance/4", "pose/covariance/5", "pose/covariance/6", "pose/covariance/7",
            "pose/covariance/8", "pose/covariance/9", "pose/covariance/10", "pose/covariance/11",
            "pose/covariance/12", "pose/covariance/13", "pose/covariance/14", "pose/covariance/15",
            "pose/covariance/16", "pose/covariance/17", "pose/covariance/18", "pose/covariance/19",
            "pose/covariance/20", "pose/covariance/21", "pose/covariance/22", "pose/covariance/23",
            "pose/covariance/24", "pose/covariance/25", "pose/covariance/26", "pose/covariance/27",
            "pose/covariance/28", "pose/covariance/29", "pose/covariance/30", "pose/covariance/31",
            "pose/covariance/32", "pose/covariance/33", "pose/covariance/34", "pose/covariance/35",
            "twist/twist/linear/x", "twist/twist/linear/y", "twist/twist/linear/z",
            "twist/twist/angular/x", "twist/twist/angular/y", "twist/twist/angular/z",
            "twist/covariance/0", "twist/covariance/1", "twist/covariance/2", "twist/covariance/3",
            "twist/covariance/4", "twist/covariance/5", "twist/covariance/6", "twist/covariance/7",
            "twist/covariance/8", "twist/covariance/9", "twist/covariance/10", "twist/covariance/11",
            "twist/covariance/12", "twist/covariance/13", "twist/covariance/14", "twist/covariance/15",
            "twist/covariance/16", "twist/covariance/17", "twist/covariance/18", "twist/covariance/19",
            "twist/covariance/20", "twist/covariance/21", "twist/covariance/22", "twist/covariance/23",
            "twist/covariance/24", "twist/covariance/25", "twist/covariance/26", "twist/covariance/27",
            "twist/covariance/28", "twist/covariance/29", "twist/covariance/30", "twist/covariance/31",
            "twist/covariance/32", "twist/covariance/33", "twist/covariance/34", "twist/covariance/35",
        ]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: Odometry) -> List:
        """
        Convert a TransformStamped message instance to a single-row list.

        :param data: TransformStamped message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, Odometry), "Input data must be of type Odometry."

        header_data = [
            data.header.stamp.sec, data.header.stamp.nanosec, data.header.frame_id, data.child_frame_id
        ]

        pose_data = self._extract_pose_with_covariance_data(data.pose)
        twist_data = self._extract_twist_with_covariance_data(data.twist)

        converted_data = list(header_data) + list(pose_data) + list(twist_data)

        # Use assert to check the length of converted_data
        assert len(converted_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [converted_data]

    def _extract_pose_with_covariance_data(self, pose_with_covariance: PoseWithCovariance) -> List:
        """
        Extract and return a list of data from a PoseWithCovariance message.

        :param pose_with_covariance: PoseWithCovariance message instance
        :return: List containing the extracted pose data
        """
        pose_data = self._extract_pose_data(pose_with_covariance.pose)
        covariance_data = list(pose_with_covariance.covariance)
        return pose_data + covariance_data

    def _extract_pose_data(self, pose: Pose) -> List:
        """
        Extract and return a list of data from a Pose message.

        :param pose: Pose message instance
        :return: List containing the extracted pose data
        """
        position_data = [pose.position.x, pose.position.y, pose.position.z]
        orientation_data = [pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w]
        return position_data + orientation_data

    def _extract_twist_with_covariance_data(self, twist_with_covariance: TwistWithCovariance) -> List:
        """
        Extract and return a list of data from a TwistWithCovariance message.

        :param twist_with_covariance: TwistWithCovariance message instance
        :return: List containing the extracted twist data
        """
        twist_data = self._extract_twist_data(twist_with_covariance.twist)
        covariance_data = list(twist_with_covariance.covariance)
        return twist_data + covariance_data

    def _extract_twist_data(self, twist: Twist) -> List:
        """
        Extract and return a list of data from a Twist message.

        :param twist: Twist message instance
        :return: List containing the extracted twist data
        """
        linear_data = [twist.linear.x, twist.linear.y, twist.linear.z]
        angular_data = [twist.angular.x, twist.angular.y, twist.angular.z]
        return linear_data + angular_data


class CameraInfoConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = [
            "header/sec", "header/nanosec", "header/frame_id",
            "height", "width", "distortion_model",
            "d/0", "d/1", "d/2", "d/3", "d/4", "d/5", "d/6", "d/7", "d/8", "d/9",
            "k/0", "k/1", "k/2", "k/3", "k/4", "k/5", "k/6", "k/7", "k/8",
            "r/0", "r/1", "r/2", "r/3", "r/4", "r/5", "r/6", "r/7", "r/8",
            "p/0", "p/1", "p/2", "p/3", "p/4", "p/5", "p/6", "p/7", "p/8", "p/9", "p/10", "p/11",
            "binning_x", "binning_y",
            "roi/x_offset", "roi/y_offset", "roi/height", "roi/width", "roi/do_rectify"
        ]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: CameraInfo) -> List:
        """
        Convert a CameraInfo message instance to a single-row list.

        :param data: CameraInfo message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, CameraInfo), "Input data must be of type CameraInfo."

        header_data = [
            data.header.stamp.sec, data.header.stamp.nanosec, data.header.frame_id,
            data.height, data.width, data.distortion_model
        ]
        
        distortion_data = list(data.d)
        assert len(distortion_data) < 10, f'We assumed distortion parameters are at most 10.'
        distortion_data = distortion_data + [0.0] * (10-len(distortion_data))

        k_data = list(data.k)
        r_data = list(data.r)
        p_data = list(data.p)

        roi_data = [
            data.binning_x, data.binning_y,
            data.roi.x_offset, data.roi.y_offset, data.roi.height, data.roi.width, data.roi.do_rectify
        ]

        converted_data = list(header_data) + list(distortion_data) + list(k_data) + list(r_data) + list(p_data) + list(roi_data)

        # Use assert to check the length of converted_data
        assert len(converted_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [converted_data]

class TransformStampedConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = [
            "header/sec", "header/nanosec", "header/frame_id", "child_frame_id",
            "transform/translation/x", "transform/translation/y", "transform/translation/z",
            "transform/rotation/x", "transform/rotation/y", "transform/rotation/z", "transform/rotation/w"
        ]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: TransformStamped) -> List:
        """
        Convert a TransformStamped message instance to a single-row list.

        :param data: TransformStamped message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, TransformStamped), "Input data must be of type TransformStamped."

        header_data = [
            data.header.stamp.sec, data.header.stamp.nanosec, data.header.frame_id, data.child_frame_id
        ]

        translation_data = [data.transform.translation.x, data.transform.translation.y, data.transform.translation.z]
        rotation_data = [data.transform.rotation.x, data.transform.rotation.y, data.transform.rotation.z, data.transform.rotation.w]

        converted_data = list(header_data) + list(translation_data) + list(rotation_data)

        # Use assert to check the length of converted_data
        assert len(converted_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [converted_data]


class PosTrackStatusConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = ["status"]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: PosTrackStatus) -> List:
        """
        Convert a PosTrackStatus message instance to a single-row list.

        :param data: PosTrackStatus message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, PosTrackStatus), "Input data must be of type PosTrackStatus."

        status_data = [data.status]

        converted_data = list(status_data)

        # Use assert to check the length of converted_data
        assert len(converted_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [converted_data]


class MarkerConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = [
            "header/sec", "header/nanosec", "header/frame_id",
            "ns", "id", "type", "action",
            "pose/position/x", "pose/position/y", "pose/position/z",
            "pose/orientation/x", "pose/orientation/y", "pose/orientation/z", "pose/orientation/w",
            "scale/x", "scale/y", "scale/z",
            "color/r", "color/g", "color/b", "color/a",
            "lifetime/sec", "lifetime/nanosec",
            "frame_locked",
            "points",
            "colors",
            "text",
            "mesh_resource",
            "mesh_use_embedded_materials",
            "points_colors"
        ]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: Marker) -> List:
        """
        Convert a Marker message instance to a single-row list.

        :param data: Marker message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, Marker), "Input data must be of type Marker."

        header_data = [
            data.header.stamp.sec, data.header.stamp.nanosec, data.header.frame_id,
            data.ns, data.id, data.type, data.action
        ]

        pose_data = [
            data.pose.position.x, data.pose.position.y, data.pose.position.z,
            data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w
        ]

        scale_data = [data.scale.x, data.scale.y, data.scale.z]

        color_data = [data.color.r, data.color.g, data.color.b, data.color.a]

        lifetime_data = [data.lifetime.sec, data.lifetime.nanosec]

        points = ""
        for point in data.points:
            # Store points as strings in a single column
            points = points + f'{point.x},{point.y},{point.z};'

        colors = ""
        for color in data.colors:
            # Store colors as strings in a single column
            colors = colors + f'{color.r},{color.g},{color.b},{color.a};'

        text_data = [data.text] if data.text else [""]

        mesh_resource_data = [data.mesh_resource] if data.mesh_resource else [""]

        mesh_use_embedded_materials_data = [data.mesh_use_embedded_materials]

        converted_data = (
            list(header_data) +
            list(pose_data) +
            list(scale_data) +
            list(color_data) +
            list(lifetime_data) +
            [data.frame_locked] +
            [points] +
            [colors] +
            list(text_data) +
            list(mesh_resource_data) +
            list(mesh_use_embedded_materials_data)
        )

        # Use assert to check the length of converted_data
        assert len(converted_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [converted_data]

class TFMessageConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__transform_stamped_converter = TransformStampedConvertor(config=config)
        self.__header = [
            "transforms/header/sec", "transforms/header/nanosec", "transforms/header/frame_id", "transforms/child_frame_id",
            "transforms/transform/translation/x", "transform/translation/y", "transforms/transform/translation/z",
            "transforms/transform/rotation/x", "transforms/transform/rotation/y", "transforms/transform/rotation/z", "transforms/transform/rotation/w"
        ]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: TFMessage) -> List:
        """
        Convert a TFMessage message instance to a list of rows.

        :param data: TFMessage message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, TFMessage), "Input data must be of type TFMessage."

        converted_data = []
        for transform_stamped in data.transforms:
            # Use extend to add each transform as a separate row
            converted_data.extend(self.__transform_stamped_converter.convert(transform_stamped))

        # Use assert to check the length of converted_data
        assert len(converted_data[0]) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return converted_data


class DepthInfoStampedConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = ["header/sec", "header/nanosec", "header/frame_id", "min_depth", "max_depth"]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: DepthInfoStamped) -> List:
        """
        Convert a DepthInfoStamped message instance to a single-row list.

        :param data: DepthInfoStamped message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, DepthInfoStamped), "Input data must be of type DepthInfoStamped."

        header_data = [
            data.header.stamp.sec,
            data.header.stamp.nanosec,
            data.header.frame_id,
            data.min_depth,
            data.max_depth
        ]

        # Use assert to check the length of header_data
        assert len(header_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [header_data]


class FluidPressureConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = ["header/sec", "header/nanosec", "header/frame_id", "fluid_pressure", "variance"]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: FluidPressure) -> List:
        """
        Convert a FluidPressure message instance to a single-row list.

        :param data: FluidPressure message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, FluidPressure), "Input data must be of type FluidPressure."

        header_data = [
            data.header.stamp.sec,
            data.header.stamp.nanosec,
            data.header.frame_id,
            data.fluid_pressure,
            data.variance
        ]

        # Use assert to check the length of header_data
        assert len(header_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [header_data]


class PoseWithCovarianceStampedConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = [
            "header/sec", "header/nanosec", "header/frame_id",
            "pose/pose/position/x", "pose/pose/position/y", "pose/pose/position/z",
            "pose/pose/orientation/x", "pose/pose/orientation/y", "pose/pose/orientation/z", "pose/pose/orientation/w",
            "covariance/0", "covariance/1", "covariance/2", "covariance/3", "covariance/4", "covariance/5",
            "covariance/6", "covariance/7", "covariance/8", "covariance/9", "covariance/10", "covariance/11",
            "covariance/12", "covariance/13", "covariance/14", "covariance/15", "covariance/16", "covariance/17",
            "covariance/18", "covariance/19", "covariance/20", "covariance/21", "covariance/22", "covariance/23",
            "covariance/24", "covariance/25", "covariance/26", "covariance/27", "covariance/28", "covariance/29",
            "covariance/30", "covariance/31", "covariance/32", "covariance/33", "covariance/34", "covariance/35"
        ]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: PoseWithCovarianceStamped) -> List:
        """
        Convert a PoseWithCovarianceStamped message instance to a single-row list.

        :param data: PoseWithCovarianceStamped message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, PoseWithCovarianceStamped), "Input data must be of type PoseWithCovarianceStamped."

        header_data = [
            data.header.stamp.sec,
            data.header.stamp.nanosec,
            data.header.frame_id
        ]

        pose_data = [
            data.pose.pose.position.x,
            data.pose.pose.position.y,
            data.pose.pose.position.z,
            data.pose.pose.orientation.x,
            data.pose.pose.orientation.y,
            data.pose.pose.orientation.z,
            data.pose.pose.orientation.w
        ]

        covariance_data = data.pose.covariance

        # Combine header, pose, and covariance data
        converted_data = list(header_data) + list(pose_data) + list(covariance_data)

        # Use assert to check the length of converted_data
        assert len(converted_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [converted_data]


class TemperatureConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = ["header/sec", "header/nanosec", "header/frame_id", "temperature", "variance"]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: Temperature) -> List:
        """
        Convert a Temperature message instance to a single-row list.

        :param data: Temperature message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, Temperature), "Input data must be of type Temperature."

        header_data = [
            data.header.stamp.sec,
            data.header.stamp.nanosec,
            data.header.frame_id,
            data.temperature,
            data.variance
        ]

        # Use assert to check the length of header_data
        assert len(header_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [header_data]


class DiagnosticArrayConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = ["header/sec", "header/nanosec", "header/frame_id", "status/level", "status/name", "status/message", "status/hardware_id"]
        self.__status = [
            "status/values/key", "status/values/value"
        ]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header + self.__status)

    def convert(self, data: Any) -> List:
        """
        Convert a DiagnosticArray message instance to a single-row list.

        :param data: DiagnosticArray message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, DiagnosticArray), "Input data must be of type DiagnosticArray."

        converted_data = []
        for ind in range(len(data.status)):
            header_data = [
                data.header.stamp.sec,
                data.header.stamp.nanosec,
                data.header.frame_id,
                data.status[ind].level,
                data.status[ind].name,
                data.status[ind].message,
                data.status[ind].hardware_id
            ]

            for values in data.status[ind].values:
                status_data = list(header_data) + [values.key, values.value]
                converted_data.append(status_data)
        
        # Use assert to check the length of converted_data
        assert len(converted_data[0]) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return converted_data

class StringConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = ["data"]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: String) -> List:
        """
        Convert a String message instance to a single-row list.

        :param data: String message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, String), "Input data must be of type String."

        header_data = [
            data.data
        ]

        # Use assert to check the length of header_data
        assert len(header_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [header_data]


class LogConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = ["stamp/sec", "stamp/nanosec", "level", "name", "msg", "file", "function", "line"]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: Log) -> List:
        """
        Convert a Log message instance to a single-row list.

        :param data: Log message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, Log), "Input data must be of type Log."

        header_data = [
            data.stamp.sec,
            data.stamp.nanosec,
            data.level,
            data.name,
            data.msg,
            data.file,
            data.function,
            data.line
        ]

        # Use assert to check the length of header_data
        assert len(header_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [header_data]


class PlaneStampedConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = [
            "header/sec", "header/nanosec", "header/frame_id",
            "mesh/triangles", "mesh/vertices",
            "coefficients/coef/0", "coefficients/coef/1", "coefficients/coef/2", "coefficients/coef/3",
            "normal/x", "normal/y", "normal/z",
            "center/x", "center/y", "center/z",
            "pose/translation/x", "pose/translation/y", "pose/translation/z",
            "pose/rotation/x", "pose/rotation/y", "pose/rotation/z", "pose/rotation/w",
            "extents/0", "extents/1",
            "bounds/points"
        ]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: PlaneStamped) -> List:
        """
        Convert a PlaneStamped message instance to a single-row list.

        :param data: PlaneStamped message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, PlaneStamped), "Input data must be of type PlaneStamped."

        header_data = [
            data.header.stamp.sec,
            data.header.stamp.nanosec,
            data.header.frame_id
        ]

        mesh_data = self._extract_mesh_data(data.mesh)
        coefficients_data = data.coefficients.coef
        normal_data = [data.normal.x, data.normal.y, data.normal.z]
        center_data = [data.center.x, data.center.y, data.center.z]
        pose_data = [
            data.pose.translation.x,
            data.pose.translation.y,
            data.pose.translation.z,
            data.pose.rotation.x,
            data.pose.rotation.y,
            data.pose.rotation.z,
            data.pose.rotation.w
        ]
        extents_data = data.extents
        bounds_data = self._extract_polygon_data(data.bounds)

        # Combine all data
        converted_data = header_data + mesh_data + coefficients_data + normal_data + center_data + pose_data + extents_data + bounds_data

        # Use assert to check the length of converted_data
        assert len(converted_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return [converted_data]

    def _extract_mesh_data(self, mesh: Mesh) -> List:
        """
        Extract and return a list of data from a Mesh message.

        :param mesh: Mesh message instance
        :return: List containing the extracted mesh data
        """
        triangles_data = []
        vertices_data = []

        # Extract triangles and vertices data
        for triangle in mesh.triangles:
            triangles_data.append(f"{triangle.vertex_indices[0]},{triangle.vertex_indices[1]},{triangle.vertex_indices[2]}")
        for vertex in mesh.vertices:
            vertices_data.append(f"{vertex.x},{vertex.y},{vertex.z}")

        return [",".join(triangles_data), ",".join(vertices_data)]

    def _extract_polygon_data(self, polygon: Polygon) -> List:
        """
        Extract and return a list of data from a Polygon message.

        :param polygon: Polygon message instance
        :return: List containing the extracted polygon data
        """
        points_data = []

        # Extract points data
        for point in polygon.points:
            points_data.append(f"{point.x},{point.y},{point.z}")

        return [",".join(points_data)]


class ImageConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = [
            "header/sec", "header/nanosec", "header/frame_id",
            "height", "width", "encoding", "is_bigendian", "step"
        ]

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: Image) -> Tuple[List, np.ndarray]:
        """
        Convert a ROS2 Image message instance to a tuple with metadata and image.

        :param data: ROS2 Image message instance
        :return: Tuple containing metadata list and image
        """
        # Use assert to check the type of data
        assert isinstance(data, Image), "Input data must be of type Image."

        # Extract header data
        header_data = [
            data.header.stamp.sec,
            data.header.stamp.nanosec,
            data.header.frame_id,
            data.height,
            data.width,
            data.encoding,
            data.is_bigendian,
            data.step
        ]

        # Convert ROS Image to OpenCV Mat using cv_bridge
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data)

        # Combine metadata and image
        result_tuple = ([header_data], cv_image)
        # Use assert to check the length of converted_data
        assert len(header_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return result_tuple


class DisparityImageConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.__header = [
            "header/sec", "header/nanosec", "header/frame_id",
            "f", "t",
            "valid_window/x_offset", "valid_window/y_offset", "valid_window/height", "valid_window/width", "valid_windiw/do_rectify",
            "min_disparity", "max_disparity", "delta_d",
            "image/header/sec", "image/header/nanosec", "image/header/frame_id",
            "image/height", "image/width", "image/encoding", "image/is_bigendian", "image/step" 
        ]

        # ImageConvertor to convert the image part of DisparityImage
        image_config = deepcopy(config)
        image_config['num_output_columns'] = config['num_image_columns']
        self.image_convertor = ImageConvertor(config=image_config)

    @property
    def header(self) -> List[str]:
        """
        Return a list of field names for the header.

        :return: List of header field names
        """
        return deepcopy(self.__header)

    def convert(self, data: Any) -> Tuple[List, np.ndarray]:
        """
        Convert a DisparityImage message instance to a list.

        :param data: DisparityImage message instance
        :return: List containing the converted data
        """
        # Use assert to check the type of data
        assert isinstance(data, DisparityImage), "Input data must be of type DisparityImage."

        # Extract header data
        header_data = [
            data.header.stamp.sec,
            data.header.stamp.nanosec,
            data.header.frame_id,
            data.f,
            data.t,
            data.valid_window.x_offset,
            data.valid_window.y_offset,
            data.valid_window.height,
            data.valid_window.width,
            data.valid_window.do_rectify,
            data.min_disparity,
            data.max_disparity,
            data.delta_d
        ]

        # Convert the image part of DisparityImage using ImageConvertor
        image_data = self.image_convertor.convert(data.image)
        header_data.extend(image_data[0][0])

        # Combine metadata and image data
        result_list = ([header_data], image_data[1])

        # Use assert to check the length of converted_data
        assert len(header_data) == self.config.get('num_output_columns'), f'Converted data must have a length of {self.config.get("num_output_columns")}.'

        return result_list


class PointCloudConvertor(ConvertorInterface):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.__header = [
            "header/sec", "header/nanosec", "header/frame_id",
            "height", "width", "is_dense"
        ]

        # Color conversion lambdas
        self._convert_rgb_uint32_to_tuple = lambda rgb_uint32: (
            (rgb_uint32 & 0x00ff0000)>>16, (rgb_uint32 & 0x0000ff00)>>8, (rgb_uint32 & 0x000000ff)
        )
        self._convert_rgb_float_to_tuple = lambda rgb_float: self._convert_rgb_uint32_to_tuple(
            int(cast(pointer(c_float(rgb_float)), POINTER(c_uint32)).contents.value)
        )

    @property
    def header(self) -> List[str]:
        return deepcopy(self.__header)

    def convert(self, data: Any) -> Tuple[List, Any]:
        assert isinstance(data, PointCloud2), "Input data must be of type PointCloud2."

        header_data = [
            data.header.stamp.sec,
            data.header.stamp.nanosec,
            data.header.frame_id,
            data.height,
            data.width,
            data.is_dense
        ]

        o3d_cloud = self._convert_ros_pointcloud_to_o3d(data)

        return ([header_data], o3d_cloud)

    def _convert_ros_pointcloud_to_o3d(self, ros_cloud: PointCloud2) -> o3d.geometry.PointCloud:
        # RGB index
        RGB_COL = 3
        FIELDS = ['x', 'y', 'z', 'rgb']

        cloud_data = list(point_cloud2.read_points(ros_cloud, field_names=FIELDS, skip_nans=True))
        cloud_data = np.array([list(row) for row in cloud_data])

        rgb = [self._convert_rgb_float_to_tuple(row[RGB_COL]) for row in cloud_data]

        o3d_cloud = o3d.geometry.PointCloud()
        o3d_cloud.points = o3d.utility.Vector3dVector(cloud_data[:, :-1])
        o3d_cloud.colors = o3d.utility.Vector3dVector(np.array(rgb)/255.0)

        return o3d_cloud
