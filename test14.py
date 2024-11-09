import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QStackedWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("主机参数设置")
        self.setGeometry(100, 100, 300, 200)

        # 创建布局
        layout = QVBoxLayout()

        # 创建表单布局
        form_layout = QFormLayout()

        # 添加磨头间距输入框
        self.moto_spacing_input = QLineEdit()
        form_layout.addRow(QLabel("磨头间距："), self.moto_spacing_input)

        # 添加横梁间距输入框
        self.beam_spacing_input = QLineEdit()
        form_layout.addRow(QLabel("横梁间距："), self.beam_spacing_input)

        # 添加磨头直径输入框
        self.moto_diameter_input = QLineEdit()
        form_layout.addRow(QLabel("磨头直径："), self.moto_diameter_input)

        # 添加磨块长度输入框
        self.grinding_block_length_input = QLineEdit()
        form_layout.addRow(QLabel("磨块长度："), self.grinding_block_length_input)

        # 将表单布局添加到主布局中
        layout.addLayout(form_layout)

        # 添加保存按钮
        self.save_button = QPushButton("参数保存")
        self.save_button.clicked.connect(self.save_parameters)
        layout.addWidget(self.save_button)

        # 设置主布局
        self.setLayout(layout)

    def save_parameters(self):
        # 获取输入的参数
        moto_spacing = self.moto_spacing_input.text()
        beam_spacing = self.beam_spacing_input.text()
        moto_diameter = self.moto_diameter_input.text()
        grinding_block_length = self.grinding_block_length_input.text()

        # 打印参数（实际应用中可以保存到文件或数据库）
        print("磨头间距:", moto_spacing)
        print("横梁间距:", beam_spacing)
        print("磨头直径:", moto_diameter)
        print("磨块长度:", grinding_block_length)

class AnotherPage(QWidget):
    def __init__(self, main_window):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("另一个页面")
        self.setGeometry(100, 100, 300, 200)

        # 创建布局
        layout = QVBoxLayout()

        # 添加一个标签
        self.label = QLabel("这是另一个页面")
        layout.addWidget(self.label)

        # 添加一个按钮，用于返回到主页面
        self.back_button = QPushButton("返回主页面")
        self.back_button.clicked.connect(lambda: self.switch_page(main_window))
        layout.addWidget(self.back_button)

        # 设置主布局
        self.setLayout(layout)

    def switch_page(self, main_window):
        # 切换到主页面
        main_window.stacked_widget.setCurrentWidget(main_window)

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("多页面应用")
        self.setGeometry(100, 100, 300, 200)

        # 创建 QStackedWidget
        self.stacked_widget = QStackedWidget()

        # 创建主页面
        self.main_window = MainWindow()
        self.stacked_widget.addWidget(self.main_window)

        # 创建另一个页面
        self.another_page = AnotherPage(self.main_window)
        self.stacked_widget.addWidget(self.another_page)

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)

        # 设置主布局
        self.setLayout(layout)

        # 默认显示主页面
        self.stacked_widget.setCurrentWidget(self.main_window)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_app = MainApp()
    main_app.show()

    sys.exit(app.exec())