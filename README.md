# robodriver-robot-booster-aio-ros2

## Get Start

### Clone the repository

```bash
git clone https://github.com/BAAI-EI-DATA/robodriver-robot-g1-aio-ros2.git && cd robodriver-robot-g1-aio-ros2
```

### Install the project to RoboDriver

```bash
conda activate RoboDriver
pip install -e .
```

---

## Configure the robot and topics

Before running, please check and configure the following items according to your environment:

- ROS2 domain/network settings
- Robot IP / SDK connection parameters
- ROS2 topic names (joint states / image / pose / gripper)
- Calibration parameters (if needed)
- Optional camera / teleoperation related parameters

If your project provides configuration files (e.g. `config.py`, YAML files, launch parameters), update them before starting data collection.

---

## Start collecting

### Activate environment

```bash
conda activate RoboDriver
```

### Launch RoboDriver

```bash
cd /path/to/your/RoboDriver
python robodriver/scripts/run.py \
  --robot.type=g1_aio_ros2
```

> If your registered robot type name is different, replace `g1_aio_ros2` with the actual type shown in your environment.



---

## Bug Fixes

### Plugin import failure (`No module named ...`)

If RoboDriver cannot import your plugin, check:

1. The package folder name and Python import path are consistent.
2. `pyproject.toml` package name is correct.
3. The plugin is installed in editable mode:
   ```bash
   pip install -e .
   ```
4. You are using the correct conda environment.

You can verify installation with:

```bash
pip list | grep robodriver
```

---


### ROS2 topic not received

Please check:

- ROS2 environment is sourced correctly
- Topic names match your code/config
- QoS settings are compatible
- Publisher and subscriber are in the same ROS domain/network

Useful commands:

```bash
ros2 topic list
ros2 topic echo /your/topic
ros2 topic hz /your/topic
```

---

## Data Information

Booster robot data is typically transmitted through ROS2 topics and/or SDK bridge nodes.

The exact observation/action fields depend on your RoboDriver adapter implementation. A common setup may include:

- **Joint states**
  - Arm joint angles
- **Gripper state**
  - Gripper width / position
- **End-effector pose (optional)**
  - Position `(x, y, z)`
  - Orientation `(quaternion or Euler angles)`
- **Head / camera related data (optional)**
  - RGB image stream
- **Teleoperation signals (optional)**
  - VR wrist pose
  - gripper command
  - Head pose command

When you need to modify the data schema, please update:

- RoboDriver adapter code (observation/action mapping)
- ROS2 topic parsing logic
- Related config files (e.g. `config.py`, YAML config)

---

## Project Structure (Example)

```text
robodriver-robot-booster-aio-ros2/
├── lerobot_robot_g1-aio_ros2/        # optional related dataset/adapter code
├── robodriver_robot_g1_aio_ros2/     # RoboDriver plugin package
├── README.md
└── pyproject.toml
```

---

## Notes

- Make sure the robot-side SDK service / ROS2 bridge is running before starting RoboDriver.
- If using camera streams, ensure device permissions and topic publishing are normal.
- If using calibration constants (e.g., wrist offsets), verify they are loaded correctly before teleoperation or collection.

---

## License

Apache-2.0 (recommended) or your chosen license.
