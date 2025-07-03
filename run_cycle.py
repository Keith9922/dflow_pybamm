import pybamm
import pandas as pd
from pathlib import Path
import numpy as np
import sys


def simulate_cycle(cycle_num, temperature=25, c_rate=1.0):
    # 转换为开尔文
    temp_k = temperature + 273.15

    # 初始化模型
    model = pybamm.lithium_ion.DFN()
    param = model.default_parameter_values

    # 设置参数
    param["Ambient temperature [K]"] = temp_k
    param["Current function [A]"] = c_rate * param["Nominal cell capacity [A.h]"]
    param["Lower voltage cut-off [V]"] = 2.5  # 匹配放电终止电压
    param["Upper voltage cut-off [V]"] = 4.2  # 匹配充电终止电压
    # 修正实验步骤格式（关键修改）
    experiment = pybamm.Experiment([
        # 放电步骤：使用逗号分隔终止条件（电压和容量耗尽）
        "Discharge at 1.0C until 2.5V",  # 修正点1：移除多余空格和"until"
        # 充电阶段
        "Charge at 0.5C until 4.2V",
        "Hold at 4.2V until 20mA",
        "Rest for 1 hour"
    ])

    # 运行模拟
    sim = pybamm.Simulation(
        model,
        parameter_values=param,
        experiment=experiment,
        solver=pybamm.CasadiSolver(
            mode="safe",
            atol=1e-7,
            rtol=1e-5,
        )
    )
    solution = sim.solve()

    # 提取关键数据
    if len(solution.cycles) > 0 and len(solution.cycles[0].steps) > 0:
        discharge_step = solution.cycles[0].steps[0]
        capacity = abs(np.trapz(discharge_step["Current [A]"].data,
                                discharge_step["Time [s]"].data)) / 3600
        avg_voltage = np.mean(discharge_step["Terminal voltage [V]"].data)
    else:
        capacity = 0.0
        avg_voltage = 0.0
        print(f"Warning: No discharge data for cycle {cycle_num}")

    return {
        "cycle": cycle_num,
        "capacity": capacity,
        "voltage": avg_voltage
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_cycle.py <cycle_number>")
        sys.exit(1)

    cycle_num = int(sys.argv[1])
    data_path = Path("battery_data.csv")

    # 执行仿真
    result = simulate_cycle(cycle_num)

    # 保存结果
    if data_path.exists() and data_path.stat().st_size > 0:
        df = pd.read_csv(data_path)
        df = pd.concat([df, pd.DataFrame([result])], ignore_index=True)
    else:
        df = pd.DataFrame([result])

    df.to_csv(data_path, index=False)
    print(f"Cycle {cycle_num} completed. Capacity: {result['capacity']:.4f} Ah")


if __name__ == "__main__":
    main()
