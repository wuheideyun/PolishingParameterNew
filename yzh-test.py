from random import random

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
import sys
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个画布
        self.canvas = FigureCanvas(Figure())
        self.ax = self.canvas.figure.add_subplot(111)  # 创建子图
        self.plot_initial_graph()  # 绘制初始图表

        # 创建按钮
        button = QPushButton("重新绘图")
        button.clicked.connect(self.redraw_plot)  # 连接按钮点击事件到重绘函数

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def plot_initial_graph(self):
        # 初始绘图
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.ax.plot(x, y)
        self.canvas.draw()  # 绘制到画布

    def redraw_plot(self):
        # 清除并重新绘制
        self.ax.clear()  # 清空画布
        x = np.linspace(0, 10, 100)
        y = np.random.uniform(0, 5, 100)
        self.ax.plot(x, y)
        self.canvas.draw()  # 更新显示新的绘图内容


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
