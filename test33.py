import pandas as pd
import numpy as np


def dynamic_prediction():
    # 文件路径配置
    file_path = r'D:\360data\重要数据\桌面\申报补充资料\SizeTest1_240703_184616.CSV'

    try:
        # 读取CSV文件第5列（E列）
        df = pd.read_csv(file_path, usecols=[4], header=None)
        data_stream = df[4].tolist()
    except Exception as e:
        print(f"文件读取失败：{str(e)}")
        return

    history = []  # 动态数据窗口
    counter = 0  # 数据点计数器

    for current_value in data_stream:
        counter += 1
        prediction = None
        error = None

        # 当有足够历史数据时进行预测
        if len(history) >= 2:
            # 构造回归矩阵
            x = np.arange(1, len(history) + 1)
            y = np.array(history)

            # 最小二乘法解线性方程组
            A = np.vstack([x, np.ones(len(x))]).T
            a, b = np.linalg.lstsq(A, y, rcond=None)[0]

            # 预测下一个点（当前值的预测）
            next_x = len(history) + 1
            prediction = a * next_x + b
            error = current_value - prediction

        # 输出格式化
        pred_str = f"{prediction:.2f}" if prediction is not None else "-"
        err_str = f"{error:+.2f}" if error is not None else "-"
        print(f"[第{counter:02d}行] 当前值：{current_value:.2f} | 预测值：{pred_str} | 差值：{err_str}")

        # 维护动态窗口
        history.append(current_value)
        if len(history) > 100:
            history.pop(0)


if __name__ == "__main__":
    dynamic_prediction()