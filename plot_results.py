# plot_results.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# 完全使用英文的版本
def generate_report():
    # 不需要特殊字体设置
    data_path = Path("battery_data.csv")
    if not data_path.exists() or data_path.stat().st_size == 0:
        print("No data to plot")
        return

    df = pd.read_csv(data_path)

    # 创建报告
    report = [
        "# Battery Degradation Analysis Report",
        f"## Simulation Parameters",
        f"- Total Cycles: {len(df)}",
        f"- Temperature: 25°C",
        f"- C-rate: 1C",
        "",
        "## Capacity Degradation Analysis",
        f"- Initial Capacity: {df['capacity'].iloc[0]:.4f} Ah",
        f"- Final Capacity: {df['capacity'].iloc[-1]:.4f} Ah",
        f"- Capacity Degradation Rate: {100 * (df['capacity'].iloc[0] - df['capacity'].iloc[-1]) / df['capacity'].iloc[0]:.2f}%",
        "",
        "## Voltage Change Analysis",
        f"- Initial Average Voltage: {df['voltage'].iloc[0]:.3f} V",
        f"- Final Average Voltage: {df['voltage'].iloc[-1]:.3f} V"
    ]

    # 创建图表
    plt.figure(figsize=(12, 10))

    # 容量衰减曲线
    plt.subplot(2, 1, 1)
    plt.plot(df["cycle"], df["capacity"], "bo-")
    plt.title("Battery Capacity Degradation Curve")
    plt.xlabel("Cycle Number")
    plt.ylabel("Capacity (Ah)")
    plt.grid(True)

    # 电压变化曲线
    plt.subplot(2, 1, 2)
    plt.plot(df["cycle"], df["voltage"], "r^-")
    plt.title("Discharge Average Voltage Change")
    plt.xlabel("Cycle Number")
    plt.ylabel("Voltage (V)")
    plt.grid(True)

    # 保存结果
    plt.tight_layout()
    plt.savefig("degradation_curves.png")

    # 保存报告
    with open("degradation_report.md", "w") as f:
        f.write("\n".join(report))
        f.write("\n\n![Degradation Curves](degradation_curves.png)")

    print("Report generated: degradation_report.md")


if __name__ == "__main__":
    generate_report()
