import time
import logging_mp
import numpy as np

from functools import cached_property
from typing import Any

from lerobot.cameras import make_cameras_from_configs
from lerobot.utils.errors import DeviceNotConnectedError, DeviceAlreadyConnectedError
from lerobot.robots.robot import Robot

from .config import G1AioRos2RobotConfig
from .node import G1AioRos2Node


logger = logging_mp.get_logger(__name__)


class G1AioRos2Robot(Robot):
    config_class = G1AioRos2RobotConfig
    name = "g1_aio_ros2"

    def __init__(self, config: G1AioRos2RobotConfig):

        super().__init__(config)
        self.config = config
        self.robot_type = self.config.type
        self.use_videos = self.config.use_videos
        self.microphones = self.config.microphones


        self.leader_motors = config.leader_motors
        self.follower_motors = config.follower_motors
        self.cameras = make_cameras_from_configs(self.config.cameras)

        self.connect_excluded_cameras = ["image_pika_pose"]


        self.robot_ros2_node = G1AioRos2Node()

        self.connected = False
        self.logs = {}

    def _ensure_ros2_node(self):
        if getattr(self.robot_ros2_node, "_destroyed", False):
            self.robot_ros2_node = G1AioRos2Node()

    # ========= features =========

    @property
    def _follower_motors_ft(self) -> dict[str, type]:
        return {
            f"follower_{motor}.pos": float
            for _comp_name, joints in self.follower_motors.items()
            for motor in joints.keys()
        }
    

    @property
    def _leader_motors_ft(self) -> dict[str, type]:
        return {
            f"leader_{joint}.pos": float
            for _comp_name, joints in self.leader_motors.items()
            for joint in joints.keys()
        }



    @property
    def _cameras_ft(self) -> dict[str, tuple]:
        return {
            cam: (
                self.config.cameras[cam].height,
                self.config.cameras[cam].width,
                3,
            )
            for cam in self.cameras
        }

    @cached_property
    def observation_features(self) -> dict[str, Any]:
        return {**self._follower_motors_ft, **self._cameras_ft}

    @cached_property
    def action_features(self) -> dict[str, Any]:
        return self._leader_motors_ft

    @property
    def is_connected(self) -> bool:
        return self.connected

    @staticmethod
    def _joint_value_from_map(joint_map: dict[str, Any], joint_name: str) -> Any | None:
        if joint_name in joint_map:
            return joint_map[joint_name]

        short_name = joint_name
        side_prefix = None
        other_side_prefix = None
        side_prefixes = ("left_hand_", "right_hand_")
        for prefix in side_prefixes:
            other_prefix = "right_hand_" if prefix == "left_hand_" else "left_hand_"
            if joint_name.startswith(prefix):
                side_prefix = prefix
                other_side_prefix = other_prefix
                short_name = joint_name[len(prefix):]
                if short_name in joint_map:
                    return joint_map[short_name]
                break

        for key, value in joint_map.items():
            if joint_name in key:
                return value
            if key in joint_name and (other_side_prefix is None or other_side_prefix not in key):
                return value
            if short_name != joint_name and short_name in key:
                if other_side_prefix is not None and other_side_prefix in key:
                    continue
                if side_prefix is not None and side_prefix in key:
                    return value
                if not any(prefix in key for prefix in side_prefixes):
                    return value

        return None

    def _component_is_ready(
        self,
        cache: dict[str, Any],
        comp_name: str,
        joints: dict[str, Any],
    ) -> bool:
        data = cache.get(comp_name)
        if data is None:
            return False

        if isinstance(data, dict):
            return all(
                self._joint_value_from_map(data, joint_name) is not None
                for joint_name in joints
            )

        return hasattr(data, "__len__") and len(data) >= len(joints)

    def _missing_component_joints(
        self,
        cache: dict[str, Any],
        comp_name: str,
        joints: dict[str, Any],
    ) -> list[str]:
        data = cache.get(comp_name)
        joint_names = list(joints.keys())
        if data is None:
            return joint_names

        if isinstance(data, dict):
            return [
                joint_name
                for joint_name in joint_names
                if self._joint_value_from_map(data, joint_name) is None
            ]

        if not hasattr(data, "__len__"):
            return joint_names

        return joint_names[len(data):]

    def _component_joint_value(
        self,
        data: Any,
        joint_name: str,
        index: int,
    ) -> Any | None:
        if data is None:
            return None
        if isinstance(data, dict):
            return self._joint_value_from_map(data, joint_name)
        if hasattr(data, "__len__") and index < len(data):
            return data[index]
        return None

    # ========= connect / disconnect =========

    def connect(self):
        timeout = 5
        start_time = time.perf_counter()

        if self.connected:
            raise DeviceAlreadyConnectedError(f"{self} already connected")

        self._ensure_ros2_node()
        self.robot_ros2_node.start()

        # 约定：node 里有 recv_images / recv_follower / recv_leader
        conditions = [
            # 摄像头图像
            (
                lambda: all(
                    name in self.robot_ros2_node.recv_images
                    for name in self.cameras
                    if name not in self.connect_excluded_cameras
                ),
                lambda: [
                    name
                    for name in self.cameras
                    if name not in self.robot_ros2_node.recv_images
                    and name not in self.connect_excluded_cameras
                ],
                "等待摄像头图像超时",
            ),
            (
                lambda: all(
                    self._component_is_ready(
                        self.robot_ros2_node.recv_leader,
                        comp_name,
                        joints,
                    )
                    for comp_name, joints in self.leader_motors.items()
                ),
                lambda: sorted([
                    joint_name
                    for comp_name, joints in self.leader_motors.items()
                    for joint_name in self._missing_component_joints(
                        self.robot_ros2_node.recv_leader,
                        comp_name,
                        joints,
                    )
                ]),
                "等待主臂数据超时",
            ),



            # 从臂
            (
                lambda: all(
                    self._component_is_ready(
                        self.robot_ros2_node.recv_follower,
                        comp_name,
                        joints,
                    )
                    for comp_name, joints in self.follower_motors.items()
                ),
                lambda: [
                    joint_name
                    for comp_name, joints in self.follower_motors.items()
                    for joint_name in self._missing_component_joints(
                        self.robot_ros2_node.recv_follower,
                        comp_name,
                        joints,
                    )
                ],
                "等待从臂数据超时",
            ),
        ]

        completed = [False] * len(conditions)

        while True:
            for i, (cond, _get_missing, _msg) in enumerate(conditions):
                if not completed[i] and cond():
                    completed[i] = True

            if all(completed):
                break

            if time.perf_counter() - start_time > timeout:
                failed_messages = []
                for i, (cond, get_missing, base_msg) in enumerate(conditions):
                    if completed[i]:
                        continue

                    missing = get_missing()
                    if cond() or not missing:
                        completed[i] = True
                        continue

                    if i == 0:
                        received = [
                            name
                            for name in self.cameras
                            if name not in missing
                        ]
                    elif i == 1:
                        received = [
                            comp_name
                            for comp_name, joints in self.leader_motors.items()
                            if self._component_is_ready(
                                self.robot_ros2_node.recv_leader,
                                comp_name,
                                joints,
                            )
                        ]
                    else:
                        received = [
                            comp_name
                            for comp_name, joints in self.follower_motors.items()
                            if self._component_is_ready(
                                self.robot_ros2_node.recv_follower,
                                comp_name,
                                joints,
                            )
                        ]

                    msg = (
                        f"{base_msg}: 未收到 [{', '.join(missing)}]; "
                        f"已收到 [{', '.join(received)}]"
                    )
                    failed_messages.append(msg)

                if not failed_messages:
                    break

                try:
                    raise TimeoutError(
                        f"连接超时，未满足的条件: {'; '.join(failed_messages)}"
                    )
                finally:
                    self.robot_ros2_node.stop()


            time.sleep(0.01)

        # 成功日志
        success_messages = []

        if conditions[0][0]():
            cam_received = [
                name
                for name in self.cameras
                if name in self.robot_ros2_node.recv_images
                and name not in self.connect_excluded_cameras
            ]
            success_messages.append(f"摄像头: {', '.join(cam_received)}")

        if conditions[1][0]():
            leader_received = []
            for comp_name, joints in self.leader_motors.items():
                if self._component_is_ready(
                    self.robot_ros2_node.recv_leader,
                    comp_name,
                    joints,
                ):
                    leader_received.append(comp_name)

            success_messages.append(f"主臂数据: {', '.join(leader_received)}")

        if conditions[2][0]():
            follower_received = [
                comp_name
                for comp_name, joints in self.follower_motors.items()
                if self._component_is_ready(
                    self.robot_ros2_node.recv_follower,
                    comp_name,
                    joints,
                )
            ]
            success_messages.append(f"从臂数据: {', '.join(follower_received)}")

        log_message = "\n[连接成功] 所有设备已就绪:\n"
        log_message += "\n".join(f"  - {msg}" for msg in success_messages)
        log_message += f"\n  总耗时: {time.perf_counter() - start_time:.2f} 秒\n"
        logger.info(log_message)

        self.connected = True
    
    def get_node(self):
        self._ensure_ros2_node()
        return self.robot_ros2_node

    def disconnect(self):
        if not self.connected:
            raise DeviceNotConnectedError()
        self.connected = False
        self.robot_ros2_node.stop()

    def __del__(self):
        try:
            if hasattr(self, "robot_ros2_node"):
                self.robot_ros2_node.stop()
        except Exception:
            pass

    # ========= calibrate / configure =========

    def calibrate(self):
        pass

    def configure(self):
        pass

    @property
    def is_calibrated(self):
        return True

    # ========= obs / action =========

    def get_observation(self) -> dict[str, Any]:
        if not self.connected:
            raise DeviceNotConnectedError(f"{self} is not connected.")

        start = time.perf_counter()
        obs_dict: dict[str, Any] = {}

        # for name in self.follower_motors:
        #     for _follower_name, follower in self.robot_ros2_node.recv_follower.items():
        #         for key, value in follower.items():
        #             if name == key:
        #                 obs_dict[f"follower_{name}.pos"] = float(value)

        missing = []
        for comp_name, joints in self.follower_motors.items():
            data = self.robot_ros2_node.recv_follower.get(comp_name)
            joint_names = list(joints.keys())

            for index, joint_name in enumerate(joint_names):
                val = self._component_joint_value(data, joint_name, index)
                if val is None:
                    missing.append(joint_name)
                    obs_dict[f"follower_{joint_name}.pos"] = float("nan")
                else:
                    obs_dict[f"follower_{joint_name}.pos"] = float(val)

        if missing:
            logger.warning(f"Missing follower joints in ROS state topics: {missing[:8]}"
                        + (f" (+{len(missing)-8} more)" if len(missing) > 8 else ""))

        dt_ms = (time.perf_counter() - start) * 1e3
        logger.debug(f"{self} read follower state: {dt_ms:.1f} ms")

        # ---- 摄像头图像保持不变 ----
        for cam_key, _cam in self.cameras.items():
            start = time.perf_counter()
            for name, val in self.robot_ros2_node.recv_images.items():
                if cam_key == name or cam_key in name:
                    obs_dict[cam_key] = val
                    break
            dt_ms = (time.perf_counter() - start) * 1e3
            logger.debug(f"{self} read {cam_key}: {dt_ms:.1f} ms")

        return obs_dict
    
    def get_action(self) -> dict[str, Any]:
        if not self.connected:
            raise DeviceNotConnectedError(f"{self} is not connected.")

        start = time.perf_counter()
        act_dict: dict[str, Any] = {}

        # for name in self.leader_motors:
        #     for _leader_name, leader in self.robot_ros2_node.recv_leader.items():
        #         for key, value in leader.items():
        #             if name == key:
        #                 act_dict[f"leader_{name}.pos"] = float(value)

        # ---- 逐组件展开，然后逐 joint 填入 ----
        for comp_name, joints in self.leader_motors.items():

            data = self.robot_ros2_node.recv_leader.get(comp_name)
            joint_names = list(joints.keys())

            for idx, joint in enumerate(joint_names):
                val = self._component_joint_value(data, joint, idx)
                if val is not None:
                    act_dict[f"leader_{joint}.pos"] = float(val)

        dt_ms = (time.perf_counter() - start) * 1e3
        logger.debug(f"{self} read action: {dt_ms:.1f} ms")

        return act_dict

    # ========= send_action =========

    def send_action(self, action: dict[str, Any]) -> dict[str, Any]:
        """The provided action is expected to be a vector."""
        if not self.is_connected:
            raise DeviceNotConnectedError(
                f"{self} is not connected. You need to run `robot.connect()`."
            )

        # goal_joint = [val for _key, val in action.items()]
        # goal_joint_numpy = np.array(goal_joint, dtype=np.float32)

        # Extract motor names from keys like 'leader_elbow.pos' -> 'elbow'
        cleaned_action = {}
        for key, value in action.items():
            if key.startswith("leader_") and key.endswith(".pos"):
                motor = key[len("leader_"):-len(".pos")]
                cleaned_action[motor] = value
            else:
                raise ValueError(f"Unexpected action key format: {key}. Expected 'leader_{{motor}}.pos'.")

        # Send the cleaned action to the ROS 2 node
        self.robot_ros2_node.ros2_send(cleaned_action)

        return {f"{arm_motor}.pos": val for arm_motor, val in action.items()}
