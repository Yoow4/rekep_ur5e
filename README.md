# Rekep_ur5e

待修改的地方

1. `real_camera.py`修改`target_serial`, 取消保存内参和图像的注释,按's'键保存图片和npy深度数据

2. `real_vision.py`修改`D435_Intrinsics`参数，修改输入的`instruction`

3. `real_action.py`修改`_setup_environment_state`函数包含环境设置，`_transform_keypoints_to_world`中修改`_load_camera_extrinsics`中的`extrinsics_path`以及确定`_get_ee_pose`这里得到的是否为真实的末端执行器位置。

   `ur5_env.py`修改机器人IP地址，修改`control_gripper`为当前夹爪的功能函数。

4. `visualization.py`修改`extrinsics`的默认值，修改`_get_test_ee_pose`的数值

5. `ur5_action.py`修改`_load_camera_extrinsics`，修改`_apply_grasp_offset`中的夹爪偏差，增加ur5e的`UR5eIKSolver`，修改`reset_joint_pos`

   `_update_current_state`没有实际作用,`sdf_voxels`和`collision_points`都是mock。`_update_keypoint_movable_mask`也没有实际功能，全都会被标记成可动。





整体流程：

1. 图像获取保存

2. DINOX分割获得物体掩码，DINOv2提取特征点，GPT4o/Qwenvl根据关键点图生成约束,约束函数在`./vlm_query`保存。
3. `_run_stage`主入口，读取`metadata.json`信息(与操作的关键点和阶段有关)，读取约束函数和运行阶段，将输出保存为`./outputs/action.json`同时保存阶段动作到`./vlm_query`。
4. 画出base,EE,camera的坐标，画出运动轨迹
5. 读取约束函数,初始化可移动关键掩码和动作序列，获取关键点，`_generate_subgoal`和`_generate_path`优化器求解，moveL执行动作，验证是否执行完成。

# Development Log

Reproduce [Rekep](https://arxiv.org/abs/2409.01652) in real robotic arm (UR5e) and one camera (D435)

# Actual Operating (locked end-effector pose)

<img  src="media/pen-in-holder.gif" width="480">

# Steps Breakingdown

## Environment Setup

```bash
Ubuntu22.04
Cuda: 12.8
```

[hand-on-eye Camera Calibration](https://github.com/heyjiacheng/hand-eye-calibration) (Optional)

Obtain an [OpenAI API](https://openai.com/blog/openai-api) key and set it up as an environment variable:

```Shell
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

Obtain an [Dino-X API](https://cloud.deepdataspace.com/playground/dino-x?referring_prompt=0) key and set it up as an environment variable:

```Shell
export Dino_X_API_KEY="YOUR_Dino_X_API_KEY"
```

## Installation

1. First, install [pixi](https://pixi.sh/latest/#installation)
2. Then build the dependencies:

```bash
pixi install
```

## Take photo（use D435, available at ./data/realsense_captures）

```bash
python real_camera.py
```

## Run [Dino-X](https://arxiv.org/abs/2411.14347) model to do image segementation. Clustering and flitering keypoints from 2D mask (generatede by Dino-X)

```bash
python real_vision.py
```

## Transfer keypoint position from camera coordinate to world coordinate (robot base coordinate). Generate robotic arm action, based on optimizer (Dual Annealing and SLSQP)

```bash
python real_action.py
```

## Visualization robot coordinate and sequence of end-effector trajectory.

```bash
python visualization.py
```

## Conduct action on UR5 robotic arm

```bash
python ur5_action.py
```

# Original Work

## ReKep: Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation

#### [[Project Page]](https://rekep-robot.github.io/) [[Paper]](https://rekep-robot.github.io/rekep.pdf) [[Video]](https://youtu.be/2S8YhBdLdww)

改自

https://github.com/heyjiacheng/Rekep-ur5/tree/main?tab=readme-ov-file







