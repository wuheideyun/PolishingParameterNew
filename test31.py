import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 生成一些随机数据
np.random.seed(0)
x = np.random.rand(50, 1)  # 50 个随机的 x 值
y = 2 + 3 * x + np.random.randn(50, 1)  # 对应的 y 值，带有一些噪声

# 创建线性回归模型并拟合数据
model = LinearRegression()
model.fit(x, y)

# 预测 y 值
y_pred = model.predict(x)

# 绘制原始数据点和线性回归曲线
plt.scatter(x, y, label='原始数据')
plt.plot(x, y_pred, color='red', linewidth=2, label='线性回归预测')
plt.xlabel('x')
plt.ylabel('y')
plt.title('线性回归预测示例')
plt.legend()
plt.show()