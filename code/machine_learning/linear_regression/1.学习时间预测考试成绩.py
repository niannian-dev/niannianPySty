import numpy as np
import matplotlib.pyplot as plt


# 你可以先只修改这两个参数，观察预测线和 MSE 如何变化。
w = 4
b = 50


def configure_chinese_font():
    """Configure common Chinese fonts on Windows and fix minus sign display."""
    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei",
        "SimHei",
        "KaiTi",
        "FangSong",
        "Arial Unicode MS",
    ]
    plt.rcParams["axes.unicode_minus"] = False


def mean_squared_error(actual, predicted):
    return np.mean((actual - predicted) ** 2)


def main():
    configure_chinese_font()

    # x 表示学习小时数，y 表示实际考试分数。
    x = np.array([1, 2, 3, 4, 5, 6])
    y_actual = np.array([52, 55, 61, 66, 70, 74])

    y_predicted = w * x + b
    mse = mean_squared_error(y_actual, y_predicted)

    print("学习小时数:", x)
    print("实际值:", y_actual)
    print("预测值:", y_predicted)
    print(f"MSE: {mse:.2f}")

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y_actual, color="#2563eb", s=90, label="实际值")
    plt.plot(
        x,
        y_predicted,
        color="#dc2626",
        linewidth=2.5,
        marker="o",
        label=f"预测线: y = {w}x + {b}",
    )

    for hour, actual, predicted in zip(x, y_actual, y_predicted):
        plt.annotate(
            f"实际: {actual}\n预测: {predicted}",
            xy=(hour, actual),
            xytext=(8, 10),
            textcoords="offset points",
            fontsize=9,
            bbox={
                "boxstyle": "round,pad=0.3",
                "facecolor": "#f8fafc",
                "edgecolor": "#cbd5e1",
                "alpha": 0.95,
            },
        )

        # 竖向虚线表示该点的误差大小。
        plt.plot(
            [hour, hour],
            [actual, predicted],
            color="#94a3b8",
            linestyle="--",
            linewidth=1,
        )

    plt.text(
        0.04,
        0.95,
        f"当前参数\nw = {w}\nb = {b}\nMSE = {mse:.2f}",
        transform=plt.gca().transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox={
            "boxstyle": "round,pad=0.5",
            "facecolor": "#fff7ed",
            "edgecolor": "#fb923c",
            "alpha": 0.95,
        },
    )

    plt.title("线性回归练习：用学习小时数预测考试分数", fontsize=15)
    plt.xlabel("学习小时数")
    plt.ylabel("考试分数")
    plt.xticks(x)
    plt.grid(True, linestyle="--", alpha=0.35)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
