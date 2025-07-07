# dflow_pybamm
# 锂电池老化仿真与分析工作流（PyBaMM + Python）

本项目基于 [PyBaMM](https://www.pybamm.org/) 电化学建模库，模拟锂离子电池在多次充放电循环下的容量衰减过程，并自动生成老化分析报告和图表。适用于科研、教学或电池寿命预测相关应用。

## 目录结构

```
├── init_model.py           # 初始化数据文件
├── run_cycle.py            # 多循环仿真主脚本（一次性完成所有循环）
├── plot_results.py         # 结果分析与可视化（中文报告+图表）
├── battery_data.csv        # 仿真结果数据（自动生成）
├── degradation_report_cn.md# 中文分析报告（自动生成）
├── degradation_curves_cn.png # 中文图表（自动生成）
└── README.md               # 项目说明
```

## 依赖环境

- Python 3.7+
- pybamm
- pandas
- matplotlib

安装依赖：
```bash
pip install pybamm pandas matplotlib
```

## 脚本说明与用法

### 1. 初始化数据文件

```bash
python init_model.py
```
- 作用：创建空的 `battery_data.csv`，为仿真做准备。

### 2. 多循环仿真（主脚本）

```bash
python run_cycle.py           # 默认仿真50次循环
python run_cycle.py 20        # 仿真20次循环
```
- 作用：基于 PyBaMM 的 DFN+SEI 模型，一次性完成指定次数的充放电循环仿真。
- 结果：每一循环的放电容量和平均电压会被记录到 `battery_data.csv`。

### 3. 结果分析与可视化

```bash
python plot_results.py
```
- 作用：读取仿真结果，生成中文分析报告和三合一图表：
  - 容量衰减曲线
  - 放电平均电压变化曲线
  - 容量保持率（老化曲线，基于最大容量）
- 结果：
  - `degradation_report_cn.md`：中文分析报告
  - `degradation_curves_cn.png`：中文图表

## 结果说明

- **容量衰减分析**：以所有循环中的最大容量为基准，计算最终容量的衰减率，更符合实际电池寿命测试标准。
- **容量保持率（老化曲线）**：反映每一循环后电池容量相对于最大容量的保持百分比。
- **电压变化分析**：展示循环过程中平均放电电压的变化趋势。

## 常见问题

- 仿真过程中如出现数值警告（如 corrector convergence failed），只要最终结果正常输出即可。
- 容量保持率略超100%通常为数值误差，已通过最大容量基准法避免。
- 如需自定义温度、倍率等参数，可在 `run_cycle.py` 中修改。

## 参考
- [PyBaMM 官方文档](https://docs.pybamm.org/en/latest/)
- [电池老化与寿命测试标准](https://www.sciencedirect.com/science/article/pii/S0378775319306237)

---

如有问题或建议，欢迎提交 issue 或 PR！ 
