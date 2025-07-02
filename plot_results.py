import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_results():
    """可视化电池老化结果并生成报告"""
    # 确保目录存在
    Path("results").mkdir(exist_ok=True)
    
    # 加载数据
    results_path = "simulation_data/cycle_results.txt"
    df = pd.read_csv(results_path)
    
    # 创建容量衰减图
    plt.figure(figsize=(10, 6))
    plt.plot(df["cycle"], df["discharge_capacity(Ah)"], "bo-")
    plt.title("电池容量衰减曲线")
    plt.xlabel("循环次数")
    plt.ylabel("放电容量 (Ah)")
    plt.grid(True)
    plt.savefig("results/capacity_degradation.png")
    
    # 创建电压变化图
    plt.figure(figsize=(10, 6))
    plt.plot(df["cycle"], df["min_voltage(V)"], "ro-")
    plt.title("放电最低电压变化")
    plt.xlabel("循环次数")
    plt.ylabel("最低电压 (V)")
    plt.grid(True)
    plt.savefig("results/voltage_degradation.png")
    
    # 生成文本报告
    report = [
        "电池老化模拟报告",
        "=" * 40,
        f"总循环次数: {len(df)}",
        f"初始容量: {df['discharge_capacity(Ah)'].iloc[0]:.4f} Ah",
        f"最终容量: {df['discharge_capacity(Ah)'].iloc[-1]:.4f} Ah",
        f"容量衰减率: {100 * (1 - df['discharge_capacity(Ah)'].iloc[-1]/df['discharge_capacity(Ah)'].iloc[0]):.2f}%",
        "",
        "循环数据摘要:",
        df.describe().to_string()
    ]
    
    # 保存报告
    with open("results/simulation_report.txt", "w") as f:
        f.write("\n".join(report))
    
    print("结果可视化完成。报告保存在 results/ 目录")
    print("\n".join(report[:7]))  # 打印摘要

if __name__ == "__main__":
    plot_results()
