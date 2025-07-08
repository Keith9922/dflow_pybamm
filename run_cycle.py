import pybamm
import pandas as pd
import numpy as np
from pathlib import Path
import sys

def main():
        # 检查文件是否存在
    if not Path("battery_data.csv").exists():
        print("鸡你太美")
        return
    num_cycles = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    model = pybamm.lithium_ion.DFN(options={"SEI": "ec reaction limited"})
    param = model.default_parameter_values
    param["Ambient temperature [K]"] = 25 + 273.15
    param["Lower voltage cut-off [V]"] = 2.5
    param["Upper voltage cut-off [V]"] = 4.2

    experiment = pybamm.Experiment([
        "Discharge at 1.0C until 2.5V",
        "Charge at 0.5C until 4.2V",
        "Hold at 4.2V until 20mA",
        "Rest for 1 hour"
    ] * num_cycles)

    sim = pybamm.Simulation(
        model,
        parameter_values=param,
        experiment=experiment,
        solver=pybamm.CasadiSolver(mode="safe", atol=1e-7, rtol=1e-5)
    )
    solution = sim.solve()

    # 提取每个循环的容量和电压
    results = []
    for i, cycle in enumerate(solution.cycles):
        if len(cycle.steps) > 0:
            discharge_step = cycle.steps[0]
            capacity = abs(np.trapz(discharge_step["Current [A]"].data, discharge_step["Time [s]"].data)) / 3600
            avg_voltage = np.mean(discharge_step["Terminal voltage [V]"].data)
        else:
            capacity = 0.0
            avg_voltage = 0.0
        results.append({"cycle": i+1, "capacity": capacity, "voltage": avg_voltage})

    df = pd.DataFrame(results)
    df.to_csv("battery_data.csv", mode='w', index=False)
    print("All cycles completed. Results saved to battery_data.csv")

if __name__ == "__main__":
    main()
