# init_model.py
import pandas as pd
from pathlib import Path

def main():
    # 创建空数据文件
    data_path = Path("battery_data.csv")
    pd.DataFrame(columns=["cycle", "capacity", "voltage"]).to_csv(data_path, index=False)
    state_path = Path("simulation_data/state.pkl")
    state_path.parent.mkdir(exist_ok=True)
    if state_path.exists():
        state_path.unlink()
    print(f"Created empty data file at {data_path} and reset state at {state_path}")

if __name__ == "__main__":
    main()
