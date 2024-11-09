import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout

class HostParamSingleWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("主机参数(单头摆)设置")
        # self.setGeometry(100, 100, 300, 200)

        # 创建布局
        layout = QVBoxLayout()
        param_label = QLabel("主机参数")
        param_label.setFixedHeight(50)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 18)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        param_label.setFont(param_font)
        param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        layout.addWidget(param_label)
        # 创建表单布局
        form_layout = QFormLayout()

        # 添加横梁间距输入框
        self.lineEdit_beam_between = QLineEdit()
        form_layout.addRow(QLabel("横梁间距："), self.lineEdit_beam_between)

        # 添加磨头直径输入框
        self.lineEdit_diameter = QLineEdit()
        form_layout.addRow(QLabel("磨头直径："), self.lineEdit_diameter)

        # 添加磨块长度输入框
        self.lineEdit_grind_size = QLineEdit()
        form_layout.addRow(QLabel("磨块长度："), self.lineEdit_grind_size)

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
        beam_between = self.lineEdit_beam_between.text()
        diameter = self.lineEdit_diameter.text()
        grind_size = self.lineEdit_grind_size.text()

        # 打印参数（实际应用中可以保存到文件或数据库）
        print("横梁间距:", beam_between)
        print("磨头直径:", diameter)
        print("磨块长度:", grind_size)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = HostParamDoubleWidget()
    window.show()

    sys.exit(app.exec())