import numpy as np


def calculate_least_squares_parameters(x, y):
    """
    使用最小二乘法计算一元线性回归的最佳权重 w 和偏差 b。

    一元线性回归模型：
        y_pred = w * x + b

    最小二乘法的目标：
        找到一条直线，让所有样本的“实际值 y”和“预测值 y_pred”
        之间的平方误差之和最小。

    参数：
        x:
            输入特征数据，例如学习小时数。
            可以传入 Python 列表、元组或 numpy 数组。

        y:
            真实目标值，例如考试分数。
            可以传入 Python 列表、元组或 numpy 数组。

    返回：
        (w, b):
            w 是权重，也叫斜率，控制直线的倾斜程度。
            b 是偏差，也叫截距，控制直线整体上下移动。

    使用公式：
        w = Σ((x - x均值) * (y - y均值)) / Σ((x - x均值)^2)
        b = y均值 - w * x均值

    注意：
        这个函数只负责计算最小二乘法参数，不负责生成数据、
        计算 MAE/MSE，也不负责绘图。
    """

    # 转成 numpy 数组，方便进行均值、求和、逐元素相减等数学运算。
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    # 最小二乘法要求 x 和 y 一一对应，所以两个数组长度必须相同。
    if x.shape != y.shape:
        raise ValueError("x 和 y 的形状必须相同，每个 x 都要对应一个 y。")

    # 至少需要两个样本点，才有意义去拟合一条直线。
    if x.size < 2:
        raise ValueError("至少需要两个数据点才能计算线性回归参数。")

    # x 如果全部相同，说明所有点都在同一个竖直位置。
    # 这种情况下无法用 y = w*x + b 表示唯一的最佳直线。
    if np.all(x == x[0]):
        raise ValueError("x 不能全部相同，否则无法计算唯一的权重 w。")

    # 计算 x 和 y 的平均值。
    # x_mean 表示所有输入特征的中心位置。
    # y_mean 表示所有真实目标值的中心位置。
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    # 分子衡量 x 和 y 一起变化的程度。
    # 如果 x 增大时 y 通常也增大，分子通常为正，w 也通常为正。
    # 如果 x 增大时 y 通常减小，分子通常为负，w 也通常为负。
    numerator = np.sum((x - x_mean) * (y - y_mean))

    # 分母衡量 x 自身的变化程度。
    # x 变化越大，分母越大；x 完全不变时，分母为 0。
    denominator = np.sum((x - x_mean) ** 2)

    # 权重 w，也就是最佳拟合直线的斜率。
    w = numerator / denominator

    # 偏差 b，也就是当 x = 0 时，预测线在 y 轴上的截距。
    # 这个公式保证最佳拟合线会经过数据的中心点：(x_mean, y_mean)。
    b = y_mean - w * x_mean

    return w, b
