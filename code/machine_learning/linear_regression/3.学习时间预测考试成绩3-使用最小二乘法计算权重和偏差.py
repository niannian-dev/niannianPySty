import numpy as np
import matplotlib.pyplot as plt


DATA_COUNT = 200
OUTLIER_COUNT = 12
RANDOM_SEED = 42


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


def create_data():
    rng = np.random.default_rng(RANDOM_SEED)

    x = np.linspace(0.5, 10, DATA_COUNT)
    noise = rng.normal(loc=0, scale=3, size=DATA_COUNT)
    y_actual = 5 * x + 50 + noise

    outlier_indices = rng.choice(DATA_COUNT, OUTLIER_COUNT, replace=False)
    outlier_offsets = rng.choice([-1, 1], OUTLIER_COUNT) * rng.uniform(
        18, 35, OUTLIER_COUNT
    )
    y_actual[outlier_indices] += outlier_offsets

    is_outlier = np.zeros(DATA_COUNT, dtype=bool)
    is_outlier[outlier_indices] = True

    return x, y_actual, is_outlier


def calculate_least_squares_parameters(x, y):
    """Calculate the best w and b for y = w * x + b by ordinary least squares."""
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean) ** 2)

    w = numerator / denominator
    b = y_mean - w * x_mean

    return w, b


def mean_absolute_error(actual, predicted):
    return np.mean(np.abs(actual - predicted))


def mean_squared_error(actual, predicted):
    return np.mean((actual - predicted) ** 2)


def print_metrics(title, actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    mse = mean_squared_error(actual, predicted)
    print(f"{title} MAE: {mae:.2f}")
    print(f"{title} MSE: {mse:.2f}")
    return mae, mse


def main():
    configure_chinese_font()

    x, y_actual, is_outlier = create_data()

    best_w, best_b = calculate_least_squares_parameters(x, y_actual)
    y_predicted = best_w * x + best_b

    print("最小二乘法计算结果：")
    print(f"最佳权重 w = {best_w:.4f}")
    print(f"最佳偏差 b = {best_b:.4f}")
    print()

    overall_mae, overall_mse = print_metrics("全部数据", y_actual, y_predicted)
    print_metrics("普通数据", y_actual[~is_outlier], y_predicted[~is_outlier])
    print_metrics("离群点", y_actual[is_outlier], y_predicted[is_outlier])

    plt.figure(figsize=(12, 7))

    plt.scatter(
        x[~is_outlier],
        y_actual[~is_outlier],
        color="#2563eb",
        alpha=0.72,
        s=38,
        label="普通实际值",
    )
    plt.scatter(
        x[is_outlier],
        y_actual[is_outlier],
        color="#f97316",
        edgecolor="#7c2d12",
        linewidth=0.8,
        s=90,
        marker="X",
        label="离群点实际值",
    )
    plt.plot(
        x,
        y_predicted,
        color="#dc2626",
        linewidth=2.7,
        label=f"最小二乘法拟合线: y = {best_w:.2f}x + {best_b:.2f}",
    )

    for hour, actual, predicted in zip(
        x[is_outlier], y_actual[is_outlier], y_predicted[is_outlier]
    ):
        plt.plot(
            [hour, hour],
            [actual, predicted],
            color="#f97316",
            linestyle="--",
            linewidth=1.2,
            alpha=0.85,
        )

    plt.text(
        0.03,
        0.97,
        (
            f"最小二乘法结果\n"
            f"w = {best_w:.4f}\n"
            f"b = {best_b:.4f}\n"
            f"MAE = {overall_mae:.2f}\n"
            f"MSE = {overall_mse:.2f}"
        ),
        transform=plt.gca().transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox={
            "boxstyle": "round,pad=0.5",
            "facecolor": "#f8fafc",
            "edgecolor": "#64748b",
            "alpha": 0.95,
        },
    )

    plt.title("线性回归第三版：用最小二乘法自动计算最佳 w 和 b", fontsize=16)
    plt.xlabel("学习小时数")
    plt.ylabel("考试分数")
    plt.grid(True, linestyle="--", alpha=0.32)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
