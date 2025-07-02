import pybamm
import pickle
from pathlib import Path

def init_battery_model():
    """初始化电池模型并保存参数"""
    # 创建模型和参数
    model = pybamm.lithium_ion.DFN()
    param = model.default_parameter_values
    
    # 设置初始参数（可在运行时覆盖）
    param["Ambient temperature [K]"] = 298.15  # 25°C
    param["Current function [A]"] = 1.0 * param["Nominal cell capacity [A.h]"]
    
    # 保存初始状态
    initial_state = None
    
    # 确保目录存在
    Path("simulation_data").mkdir(exist_ok=True)
    
    # 保存模型和初始状态
    with open("simulation_data/model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    with open("simulation_data/params.pkl", "wb") as f:
        pickle.dump(param, f)
    
    with open("simulation_data/state.pkl", "wb") as f:
        pickle.dump(initial_state, f)
    
    # 创建空的结果文件
    with open("simulation_data/cycle_results.txt", "w") as f:
        f.write("cycle,discharge_capacity(Ah),min_voltage(V)\n")
    
    print("电池模型初始化完成。结果保存在 simulation_data/ 目录")

if __name__ == "__main__":
    init_battery_model()
