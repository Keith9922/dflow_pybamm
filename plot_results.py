# plot_results.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib

# 设置中文字体（适配不同系统）
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False

def generate_report():
    data_path = Path("battery_data.csv")
    if not data_path.exists() or data_path.stat().st_size == 0:
        print("没有数据可绘制")
        return

    df = pd.read_csv(data_path)
    max_capacity = df['capacity'].max()
    max_cycle = df['capacity'].idxmax() + 1  # 循环编号从1开始
    if max_capacity == 0:
        degradation_rate = '无法计算（最大容量为0）'
    else:
        degradation_rate = f"{100 * (max_capacity - df['capacity'].iloc[-1]) / max_capacity:.2f}%"

    # 中文报告内容
    report = [
        "# 锂电池老化分析报告",
        f"## 仿真参数",
        f"- 总循环次数: {len(df)}",
        f"- 温度: 25°C",
        f"- 倍率: 1C",
        "",
        "## 容量衰减分析（以最大容量为基准）",
        f"- 最大容量: {max_capacity:.4f} Ah（出现在第{max_cycle}次循环）",
        f"- 最终容量: {df['capacity'].iloc[-1]:.4f} Ah",
        f"- 容量衰减率: {degradation_rate}",
        "",
        "## 电压变化分析",
        f"- 初始平均电压: {df['voltage'].iloc[0]:.3f} V",
        f"- 最终平均电压: {df['voltage'].iloc[-1]:.3f} V"
    ]

    # 画图
    plt.figure(figsize=(12, 15))

    # 1. 容量衰减曲线
    plt.subplot(3, 1, 1)
    plt.plot(df["cycle"], df["capacity"], "bo-")
    plt.title("锂电池容量衰减曲线")
    plt.xlabel("循环次数")
    plt.ylabel("容量 (Ah)")
    plt.grid(True)

    # 2. 电压变化曲线
    plt.subplot(3, 1, 2)
    plt.plot(df["cycle"], df["voltage"], "r^-")
    plt.title("放电平均电压变化曲线")
    plt.xlabel("循环次数")
    plt.ylabel("电压 (V)")
    plt.grid(True)

    # 3. 老化曲线（容量保持率，基于最大容量）
    plt.subplot(3, 1, 3)
    if max_capacity != 0:
        capacity_retention = df['capacity'] / max_capacity * 100
        plt.plot(df["cycle"], capacity_retention, "gs-")
        plt.title("容量保持率（基于最大容量）")
        plt.xlabel("循环次数")
        plt.ylabel("容量保持率 (%)")
        plt.ylim(0, 105)
        plt.grid(True)
    else:
        plt.text(0.5, 0.5, "最大容量为0，无法绘制老化曲线", ha='center', va='center', fontsize=14)
        plt.axis('off')

    plt.tight_layout()
    plt.savefig("degradation_curves_cn.png")

    # 保存中文报告
    with open("degradation_report_cn.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        f.write("\n\n![老化曲线](degradation_curves_cn.png)")

    print("报告已生成: degradation_report_cn.md")

if __name__ == "__main__":
    generate_report()
