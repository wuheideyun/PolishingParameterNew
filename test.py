from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QStatusBar

class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 创建一个垂直布局
        layout = QVBoxLayout()

        # 创建一个标签控件并添加到布局中
        label = QLabel("这是扩展到整个布局的内容")
        layout.addWidget(label, stretch=1)  # 设置伸缩因子为 1

        # 创建一个状态栏并添加到布局中
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("状态栏")
        layout.addWidget(self.status_bar)  # 默认伸缩因子为 0

        # 设置布局到这个 widget
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建自定义 widget
        custom_widget = CustomWidget()

        # 设置为主窗口的中央控件
        self.setCentralWidget(custom_widget)

        # 设置窗口标题
        self.setWindowTitle("QWidget内容扩充示例")
        self.resize(400, 300)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
