# init_model.py
import pandas as pd
from pathlib import Path

def main():
    # 创建空数据文件
    data_path = Path("battery_data.csv")
    pd.DataFrame(columns=["cycle", "capacity", "voltage"]).to_csv(data_path, index=False)
    print(f"Created empty data file at {data_path} ")

if __name__ == "__main__":
    main()
