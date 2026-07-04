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
