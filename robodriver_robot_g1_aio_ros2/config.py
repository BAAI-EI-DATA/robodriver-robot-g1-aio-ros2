from typing import Dict
from dataclasses import dataclass, field

from lerobot.robots.config import RobotConfig
from lerobot.cameras import CameraConfig
from lerobot.cameras.opencv import OpenCVCameraConfig
from lerobot.motors import Motor, MotorNormMode


@RobotConfig.register_subclass("g1_aio_ros2")
@dataclass
class G1AioRos2RobotConfig(RobotConfig):
    use_degrees = True
    norm_mode_body = (
        MotorNormMode.DEGREES if use_degrees else MotorNormMode.RANGE_M100_100
    )

    leader_motors: Dict[str, Dict[str, Motor]] = field(
        default_factory=lambda norm_mode_body=norm_mode_body: {
            "leader_left_wrist": {
                "leader_left_wrist_x": Motor(1, "robot_motor", norm_mode_body),
                "leader_left_wrist_y": Motor(2, "robot_motor", norm_mode_body),
                "leader_left_wrist_z": Motor(3, "robot_motor", norm_mode_body),
                "leader_left_wrist_roll": Motor(4, "robot_motor", norm_mode_body),
                "leader_left_wrist_pitch": Motor(5, "robot_motor", norm_mode_body),
                "leader_left_wrist_yaw": Motor(6, "robot_motor", norm_mode_body),
            },
            "leader_right_wrist": {
                "leader_right_wrist_x": Motor(1, "robot_motor", norm_mode_body),
                "leader_right_wrist_y": Motor(2, "robot_motor", norm_mode_body),
                "leader_right_wrist_z": Motor(3, "robot_motor", norm_mode_body),
                "leader_right_wrist_roll": Motor(4, "robot_motor", norm_mode_body),
                "leader_right_wrist_pitch": Motor(5, "robot_motor", norm_mode_body),
                "leader_right_wrist_yaw": Motor(6, "robot_motor", norm_mode_body),
            },
            "leader_head": {
                "leader_head_x": Motor(1, "robot_motor", norm_mode_body),
                "leader_head_y": Motor(2, "robot_motor", norm_mode_body),
                "leader_head_z": Motor(3, "robot_motor", norm_mode_body),
                "leader_head_roll": Motor(4, "robot_motor", norm_mode_body),
                "leader_head_pitch": Motor(5, "robot_motor", norm_mode_body),
                "leader_head_yaw": Motor(6, "robot_motor", norm_mode_body),
            },

            
            "leader_left_hand": {
                "left_hand_thumb_0_joint":  Motor(1, "robot_motor", norm_mode_body),
                "left_hand_thumb_1_joint":  Motor(2, "robot_motor", norm_mode_body),
                "left_hand_thumb_2_joint":  Motor(3, "robot_motor", norm_mode_body),
                "left_hand_middle_0_joint": Motor(4, "robot_motor", norm_mode_body),
                "left_hand_middle_1_joint": Motor(5, "robot_motor", norm_mode_body),
                "left_hand_index_0_joint":  Motor(6, "robot_motor", norm_mode_body),
                "left_hand_index_1_joint":  Motor(7, "robot_motor", norm_mode_body),
            },

            
            "leader_right_hand": {
                "right_hand_thumb_0_joint":  Motor(1, "robot_motor", norm_mode_body),
                "right_hand_thumb_1_joint":  Motor(2, "robot_motor", norm_mode_body),
                "right_hand_thumb_2_joint":  Motor(3, "robot_motor", norm_mode_body),
                "right_hand_middle_0_joint": Motor(4, "robot_motor", norm_mode_body),
                "right_hand_middle_1_joint": Motor(5, "robot_motor", norm_mode_body),
                "right_hand_index_0_joint":  Motor(6, "robot_motor", norm_mode_body),
                "right_hand_index_1_joint":  Motor(7, "robot_motor", norm_mode_body),
            },
        }
    )

    follower_motors: Dict[str, Dict[str, Motor]] = field(
        default_factory=lambda norm_mode_body=norm_mode_body: {
            "follower_body_joint_states": {
                # legs
                "left_hip_pitch_joint":      Motor(1,  "robot_motor", norm_mode_body),
                "left_hip_roll_joint":       Motor(2,  "robot_motor", norm_mode_body),
                "left_hip_yaw_joint":        Motor(3,  "robot_motor", norm_mode_body),
                "left_knee_joint":           Motor(4,  "robot_motor", norm_mode_body),
                "left_ankle_pitch_joint":    Motor(5,  "robot_motor", norm_mode_body),
                "left_ankle_roll_joint":     Motor(6,  "robot_motor", norm_mode_body),

                "right_hip_pitch_joint":     Motor(7,  "robot_motor", norm_mode_body),
                "right_hip_roll_joint":      Motor(8,  "robot_motor", norm_mode_body),
                "right_hip_yaw_joint":       Motor(9,  "robot_motor", norm_mode_body),
                "right_knee_joint":          Motor(10, "robot_motor", norm_mode_body),
                "right_ankle_pitch_joint":   Motor(11, "robot_motor", norm_mode_body),
                "right_ankle_roll_joint":    Motor(12, "robot_motor", norm_mode_body),

                # waist
                "waist_yaw_joint":           Motor(13, "robot_motor", norm_mode_body),
                "waist_roll_joint":          Motor(14, "robot_motor", norm_mode_body),
                "waist_pitch_joint":         Motor(15, "robot_motor", norm_mode_body),

                # left arm
                "left_shoulder_pitch_joint": Motor(16, "robot_motor", norm_mode_body),
                "left_shoulder_roll_joint":  Motor(17, "robot_motor", norm_mode_body),
                "left_shoulder_yaw_joint":   Motor(18, "robot_motor", norm_mode_body),
                "left_elbow_joint":          Motor(19, "robot_motor", norm_mode_body),
                "left_wrist_roll_joint":     Motor(20, "robot_motor", norm_mode_body),
                "left_wrist_pitch_joint":    Motor(21, "robot_motor", norm_mode_body),
                "left_wrist_yaw_joint":      Motor(22, "robot_motor", norm_mode_body),

                # right arm
                "right_shoulder_pitch_joint": Motor(23, "robot_motor", norm_mode_body),
                "right_shoulder_roll_joint":  Motor(24, "robot_motor", norm_mode_body),
                "right_shoulder_yaw_joint":   Motor(25, "robot_motor", norm_mode_body),
                "right_elbow_joint":          Motor(26, "robot_motor", norm_mode_body),
                "right_wrist_roll_joint":     Motor(27, "robot_motor", norm_mode_body),
                "right_wrist_pitch_joint":    Motor(28, "robot_motor", norm_mode_body),
                "right_wrist_yaw_joint":      Motor(29, "robot_motor", norm_mode_body),
            },

            "follower_hand_joint_states": {
                # left hand
                "left_hand_thumb_0_joint":   Motor(1,  "robot_motor", norm_mode_body),
                "left_hand_thumb_1_joint":   Motor(2,  "robot_motor", norm_mode_body),
                "left_hand_thumb_2_joint":   Motor(3,  "robot_motor", norm_mode_body),
                "left_hand_middle_0_joint":  Motor(4,  "robot_motor", norm_mode_body),
                "left_hand_middle_1_joint":  Motor(5,  "robot_motor", norm_mode_body),
                "left_hand_index_0_joint":   Motor(6,  "robot_motor", norm_mode_body),
                "left_hand_index_1_joint":   Motor(7,  "robot_motor", norm_mode_body),

                # right hand
                "right_hand_thumb_0_joint":  Motor(8,  "robot_motor", norm_mode_body),
                "right_hand_thumb_1_joint":  Motor(9,  "robot_motor", norm_mode_body),
                "right_hand_thumb_2_joint":  Motor(10, "robot_motor", norm_mode_body),
                "right_hand_index_0_joint":  Motor(11, "robot_motor", norm_mode_body),
                "right_hand_index_1_joint":  Motor(12, "robot_motor", norm_mode_body),
                "right_hand_middle_0_joint": Motor(13, "robot_motor", norm_mode_body),
                "right_hand_middle_1_joint": Motor(14, "robot_motor", norm_mode_body),
            },
        }
    )

    cameras: Dict[str, CameraConfig] = field(
        default_factory=lambda: {
            "image_top": OpenCVCameraConfig(
                index_or_path=0, fps=30, width=640, height=480
            ),
        }
    )

    use_videos: bool = False

    microphones: Dict[str, int] = field(
        default_factory=lambda: {}
    )