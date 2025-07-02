import pybamm
import pickle
import numpy as np
from pathlib import Path
import argparse

def run_cycle(cycle_num: int, temperature: float = 25.0, c_rate: float = 1.0):
    """执行单个充放电循环并记录结果"""
    # 加载模型和参数
    with open("simulation_data/model.pkl", "rb") as f:
        model = pickle.load(f)
    
    with open("simulation_data/params.pkl", "rb") as f:
        param = pickle.load(f)
    
    with open("simulation_data/state.pkl", "rb") as f:
        initial_state = pickle.load(f)
    
    # 更新参数
    param["Ambient temperature [K]"] = temperature + 273.15
    param["Current function [A]"] = c_rate * param["Nominal cell capacity [A.h]"]
    
    # 创建实验：一个充放电循环
    experiment = pybamm.Experiment([
        f"Discharge at {c_rate}C until 2.5 V",
        f"Charge at {c_rate}C until 4.2 V",
    ])
    
    # 运行模拟
    sim = pybamm.Simulation(
        model, 
        parameter_values=param,
        experiment=experiment
    )
    
    # 使用前一次的状态（如果有）
    solution = sim.solve(initial_solution=initial_state)
    
    # 保存当前状态供下一次使用
    with open("simulation_data/state.pkl", "wb") as f:
        pickle.dump(solution, f)
    
    # 提取结果数据
    discharge_step = solution.cycles[0].steps[0]
    discharge_capacity = np.trapz(
        discharge_step["Current [A]"].data, 
        discharge_step["Time [s]"].data
    ) / 3600  # 转换为Ah
    
    min_voltage = np.min(discharge_step["Terminal voltage [V]"].data)
    
    # 追加结果到文件
    with open("simulation_data/cycle_results.txt", "a") as f:
        f.write(f"{cycle_num},{abs(discharge_capacity):.6f},{min_voltage:.3f}\n")
    
    print(f"循环 {cycle_num} 完成: 放电容量={abs(discharge_capacity):.4f}Ah, 最低电压={min_voltage:.3f}V")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="执行电池充放电循环")
    parser.add_argument("cycle_num", type=int, help="当前循环编号")
    parser.add_argument("--temperature", type=float, default=25.0, help="温度(摄氏度)")
    parser.add_argument("--c_rate", type=float, default=1.0, help="充放电倍率")
    
    args = parser.parse_args()
    
    run_cycle(
        cycle_num=args.cycle_num,
        temperature=args.temperature,
        c_rate=args.c_rate
    )
