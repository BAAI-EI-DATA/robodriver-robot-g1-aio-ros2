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

    # 按组件分组：{ comp_id: { joint_name: Motor, ... }, ... }
    leader_motors: Dict[str, Dict[str, Motor]] = field(
        default_factory=lambda norm_mode_body=norm_mode_body: {
            "leader_joint_states": {
                "leader_left_hip_pitch_joint":      Motor(1,  "robot_motor", norm_mode_body),
                "leader_left_hip_roll_joint":       Motor(2,  "robot_motor", norm_mode_body),
                "leader_left_hip_yaw_joint":        Motor(3,  "robot_motor", norm_mode_body),
                "leader_left_knee_joint":           Motor(4,  "robot_motor", norm_mode_body),
                "leader_left_ankle_pitch_joint":    Motor(5,  "robot_motor", norm_mode_body),
                "leader_left_ankle_roll_joint":     Motor(6,  "robot_motor", norm_mode_body),

                "leader_right_hip_pitch_joint":     Motor(7,  "robot_motor", norm_mode_body),
                "leader_right_hip_roll_joint":      Motor(8,  "robot_motor", norm_mode_body),
                "leader_right_hip_yaw_joint":       Motor(9,  "robot_motor", norm_mode_body),
                "leader_right_knee_joint":          Motor(10, "robot_motor", norm_mode_body),
                "leader_right_ankle_pitch_joint":   Motor(11, "robot_motor", norm_mode_body),
                "leader_right_ankle_roll_joint":    Motor(12, "robot_motor", norm_mode_body),

                "leader_waist_yaw_joint":           Motor(13, "robot_motor", norm_mode_body),
                "leader_waist_roll_joint":          Motor(14, "robot_motor", norm_mode_body),
                "leader_waist_pitch_joint":         Motor(15, "robot_motor", norm_mode_body),

                "leader_left_shoulder_pitch_joint": Motor(16, "robot_motor", norm_mode_body),
                "leader_left_shoulder_roll_joint":  Motor(17, "robot_motor", norm_mode_body),
                "leader_left_shoulder_yaw_joint":   Motor(18, "robot_motor", norm_mode_body),
                "leader_left_elbow_joint":          Motor(19, "robot_motor", norm_mode_body),
                "leader_left_wrist_roll_joint":     Motor(20, "robot_motor", norm_mode_body),
                "leader_left_wrist_pitch_joint":    Motor(21, "robot_motor", norm_mode_body),
                "leader_left_wrist_yaw_joint":      Motor(22, "robot_motor", norm_mode_body),

                "leader_right_shoulder_pitch_joint": Motor(23, "robot_motor", norm_mode_body),
                "leader_right_shoulder_roll_joint":  Motor(24, "robot_motor", norm_mode_body),
                "leader_right_shoulder_yaw_joint":   Motor(25, "robot_motor", norm_mode_body),
                "leader_right_elbow_joint":          Motor(26, "robot_motor", norm_mode_body),
                "leader_right_wrist_roll_joint":     Motor(27, "robot_motor", norm_mode_body),
                "leader_right_wrist_pitch_joint":    Motor(28, "robot_motor", norm_mode_body),
                "leader_right_wrist_yaw_joint":      Motor(29, "robot_motor", norm_mode_body),
            },
            "leader_left_hand": {
                "leader_left_hand_thumb_0_joint":  Motor(1, "robot_motor", norm_mode_body),
                "leader_left_hand_thumb_1_joint":  Motor(2, "robot_motor", norm_mode_body),
                "leader_left_hand_thumb_2_joint":  Motor(3, "robot_motor", norm_mode_body),
                "leader_left_hand_middle_0_joint": Motor(4, "robot_motor", norm_mode_body),
                "leader_left_hand_middle_1_joint": Motor(5, "robot_motor", norm_mode_body),
                "leader_left_hand_index_0_joint":  Motor(6, "robot_motor", norm_mode_body),
                "leader_left_hand_index_1_joint":  Motor(7, "robot_motor", norm_mode_body),
            },
            "leader_right_hand": {
                "leader_right_hand_thumb_0_joint":  Motor(1, "robot_motor", norm_mode_body),
                "leader_right_hand_thumb_1_joint":  Motor(2, "robot_motor", norm_mode_body),
                "leader_right_hand_thumb_2_joint":  Motor(3, "robot_motor", norm_mode_body),
                "leader_right_hand_middle_0_joint": Motor(4, "robot_motor", norm_mode_body),
                "leader_right_hand_middle_1_joint": Motor(5, "robot_motor", norm_mode_body),
                "leader_right_hand_index_0_joint":  Motor(6, "robot_motor", norm_mode_body),
                "leader_right_hand_index_1_joint":  Motor(7, "robot_motor", norm_mode_body),
            },
        }
    )

    follower_motors: Dict[str, Dict[str, Motor]] = field(
        default_factory=lambda norm_mode_body=norm_mode_body: {
            "follower_joint_states": {
                "follower_left_hip_pitch_joint":      Motor(1,  "robot_motor", norm_mode_body),
                "follower_left_hip_roll_joint":       Motor(2,  "robot_motor", norm_mode_body),
                "follower_left_hip_yaw_joint":        Motor(3,  "robot_motor", norm_mode_body),
                "follower_left_knee_joint":           Motor(4,  "robot_motor", norm_mode_body),
                "follower_left_ankle_pitch_joint":    Motor(5,  "robot_motor", norm_mode_body),
                "follower_left_ankle_roll_joint":     Motor(6,  "robot_motor", norm_mode_body),

                "follower_right_hip_pitch_joint":     Motor(7,  "robot_motor", norm_mode_body),
                "follower_right_hip_roll_joint":      Motor(8,  "robot_motor", norm_mode_body),
                "follower_right_hip_yaw_joint":       Motor(9,  "robot_motor", norm_mode_body),
                "follower_right_knee_joint":          Motor(10, "robot_motor", norm_mode_body),
                "follower_right_ankle_pitch_joint":   Motor(11, "robot_motor", norm_mode_body),
                "follower_right_ankle_roll_joint":    Motor(12, "robot_motor", norm_mode_body),

                "follower_waist_yaw_joint":           Motor(13, "robot_motor", norm_mode_body),
                "follower_waist_roll_joint":          Motor(14, "robot_motor", norm_mode_body),
                "follower_waist_pitch_joint":         Motor(15, "robot_motor", norm_mode_body),

                "follower_left_shoulder_pitch_joint": Motor(16, "robot_motor", norm_mode_body),
                "follower_left_shoulder_roll_joint":  Motor(17, "robot_motor", norm_mode_body),
                "follower_left_shoulder_yaw_joint":   Motor(18, "robot_motor", norm_mode_body),
                "follower_left_elbow_joint":          Motor(19, "robot_motor", norm_mode_body),
                "follower_left_wrist_roll_joint":     Motor(20, "robot_motor", norm_mode_body),
                "follower_left_wrist_pitch_joint":    Motor(21, "robot_motor", norm_mode_body),
                "follower_left_wrist_yaw_joint":      Motor(22, "robot_motor", norm_mode_body),

                "follower_right_shoulder_pitch_joint": Motor(23, "robot_motor", norm_mode_body),
                "follower_right_shoulder_roll_joint":  Motor(24, "robot_motor", norm_mode_body),
                "follower_right_shoulder_yaw_joint":   Motor(25, "robot_motor", norm_mode_body),
                "follower_right_elbow_joint":          Motor(26, "robot_motor", norm_mode_body),
                "follower_right_wrist_roll_joint":     Motor(27, "robot_motor", norm_mode_body),
                "follower_right_wrist_pitch_joint":    Motor(28, "robot_motor", norm_mode_body),
                "follower_right_wrist_yaw_joint":      Motor(29, "robot_motor", norm_mode_body),
            },
            "follower_left_hand": {
                "follower_left_hand_thumb_0_joint":  Motor(1, "robot_motor", norm_mode_body),
                "follower_left_hand_thumb_1_joint":  Motor(2, "robot_motor", norm_mode_body),
                "follower_left_hand_thumb_2_joint":  Motor(3, "robot_motor", norm_mode_body),
                "follower_left_hand_middle_0_joint": Motor(4, "robot_motor", norm_mode_body),
                "follower_left_hand_middle_1_joint": Motor(5, "robot_motor", norm_mode_body),
                "follower_left_hand_index_0_joint":  Motor(6, "robot_motor", norm_mode_body),
                "follower_left_hand_index_1_joint":  Motor(7, "robot_motor", norm_mode_body),
            },
            "follower_right_hand": {
                "follower_right_hand_thumb_0_joint":  Motor(1, "robot_motor", norm_mode_body),
                "follower_right_hand_thumb_1_joint":  Motor(2, "robot_motor", norm_mode_body),
                "follower_right_hand_thumb_2_joint":  Motor(3, "robot_motor", norm_mode_body),
                "follower_right_hand_middle_0_joint": Motor(4, "robot_motor", norm_mode_body),
                "follower_right_hand_middle_1_joint": Motor(5, "robot_motor", norm_mode_body),
                "follower_right_hand_index_0_joint":  Motor(6, "robot_motor", norm_mode_body),
                "follower_right_hand_index_1_joint":  Motor(7, "robot_motor", norm_mode_body),
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
