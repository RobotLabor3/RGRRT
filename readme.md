# MBM Benchmark & Labor3 Platform Test

---

## English Description

### MBM Benchmark

We acknowledge the contribution of KavrakiLab for providing the motion_bench_maker dataset. Built on OMPL, this benchmark enables systematic evaluation of sampling-based planners across different robots and complex environments.

Based on this framework, we implement the **RGRRT algorithm** within OMPL to address motion planning problems in cluttered, high-dimensional spaces. The algorithm is designed to achieve **asymptotic optimality** while maintaining strong performance.

The `MBM/ompl` directory includes configurations for four robots:

* baxter
* fetch
* panda
* ur5

along with parameter settings for eight benchmark scenarios. Most parameters follow default or MoveIt-recommended configurations.

Usage:

* Compile using the libraries in `algorithm/include` and `algorithm/lib`
* Replace the `config/ompl` directory in your MBM workspace
* Run benchmark experiments directly

Additionally:

* `MBM/mbm_data_process.py` is provided for statistical analysis
* It computes success rate, path length, and planning time metrics

All source code will be publicly released after naming standardization.

---

### Labor3 Platform

Labor3 is a laboratory-developed wheeled humanoid robot platform integrating multiple kinematic structures:

* Serial structure: dual-arm humanoid manipulators
* Parallel mechanism: 3-RPS structure
* Mobile base: omnidirectional mecanum wheels

The platform supports precise motion control within ±1.5 meters, achieving positioning accuracy within 1 mm.

Extensive experiments of the **RGRRT algorithm** are conducted on Labor3. The primary application scenario is agricultural harvesting, where the robot is required to reach targets inside dense tree canopies.

Due to the highly complex structure of branches, it is difficult to model the environment using simple geometric primitives. Therefore, 3D reconstruction techniques are employed to generate realistic point cloud environments.

Dataset and resources:

* Point clouds:
  `Labor3/labor3_pointcloud/`
  Contains 8 reconstructed scenes, with the coordinate system defined by the first reconstruction frame

* Goal configurations:
  Each scene includes 5 target configurations
  Stored in `Labor3/labor3_goal_config.yaml`

* Data analysis tool:
  `Labor3/labor3_data_process.py`
  Generates Excel reports including:

  * Success rate
  * Path length statistics
  * Planning time statistics

---

## 中文说明

### MBM Benchmark

感谢 KavrakiLab 提供的 motion_bench_maker 数据集(https://github.com/KavrakiLab/motion_bench_maker.git)。该数据集基于 OMPL，为不同机器人与复杂场景下的采样规划算法提供了统一的性能评估基准。

在此基础上，我们在 OMPL 框架内实现了 **RGRRT 算法**，用于解决高维空间中密集障碍环境下的路径规划问题，并具备渐进最优（asymptotic optimality）特性。

`MBM/ompl` 文件夹包含四种机器人模型：

* baxter
* fetch
* panda
* ur5

并提供了 motion_bench_maker 中 8 种典型场景的算法参数配置。大部分参数来源于默认设置或 MoveIt 推荐值。

使用方法如下：

* 使用 `algorithm/include` 与 `algorithm/lib` 中的算法库进行编译
* 替换自身 MBM 工作空间中的 `config/ompl` 文件夹
* 即可运行基准测试

此外：

* `MBM/mbm_data_process.py` 用于对实验结果进行统计分析
* 包括成功率、路径长度和规划时间等指标

所有源代码将在完成命名规范整理后开源发布。

---

### Labor3 平台

Labor3 是实验室自主研发的轮式仿人机器人平台，融合了多种机构形式：

* 串联结构：仿人双臂
* 并联结构：3-RPS 机构
* 移动底盘：全向麦克纳姆轮

该平台可在 ±1.5 米范围内实现高精度移动控制，位置误差小于 1 mm。

我们在 Labor3 平台上对 **RGRRT 算法**进行了大量实验验证。实验场景主要为农业采摘任务，目标是在树冠内部完成果实抓取。

由于树冠内部枝干结构复杂，难以使用简单几何体进行精确建模，因此采用三维重建技术，从多个视角对真实果树进行扫描，生成点云环境。

相关数据如下：

* 点云数据：
  `Labor3/labor3_pointcloud/`
  包含 8 个重建场景，坐标系基于重建的第一帧图像

* 目标构型：
  每个场景设置 5 个目标构型
  存储于 `Labor3/labor3_goal_config.yaml`

* 数据分析工具：
  `Labor3/labor3_data_process.py`
  可生成 Excel 文件，用于展示：

  * 成功率
  * 路径长度统计
  * 规划时间统计

---

