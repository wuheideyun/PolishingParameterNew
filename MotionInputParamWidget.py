import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QGroupBox, QHBoxLayout

class MotionInputParamWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("运动输入参数设置")
        # self.setGeometry(100, 100, 400, 300)
        # self.setFixedSize(400,310)

        # 创建主布局
        main_layout = QVBoxLayout()
        param_label = QLabel("运动输入参数")
        param_label.setFixedHeight(50)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 18)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        param_label.setFont(param_font)
        param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        main_layout.addWidget(param_label)
        # 创建表单布局
        form_layout = QFormLayout()

        # 添加产量大小输入框
        self.lineEdit_production_volume = QLineEdit()
        form_layout.addRow(QLabel("产量大小："), self.lineEdit_production_volume)

        # 添加进砖宽度输入框
        self.lineEdit_ceramic_width = QLineEdit()
        form_layout.addRow(QLabel("进砖宽度："), self.lineEdit_ceramic_width)

        # 添加加速度大小输入框
        self.lineEdit_accelerate = QLineEdit()
        form_layout.addRow(QLabel("加速度大小："), self.lineEdit_accelerate)

        # 添加轨迹重叠量输入框
        self.lineEdit_overlap = QLineEdit()
        form_layout.addRow(QLabel("轨迹重叠量："), self.lineEdit_overlap)

        # 将表单布局添加到主布局中
        main_layout.addLayout(form_layout)

        # 创建自定义修正方案的组框
        custom_group_box = QGroupBox("以下参数仅在自定义修正方案使用")
        custom_layout = QFormLayout()

        # 添加单组覆盖磨头数输入框
        self.single_group_moto_input = QLineEdit()
        custom_layout.addRow(QLabel("单组覆盖磨头数："), self.single_group_moto_input)

        # 添加叠加组数输入框
        self.lineEdit_num_input = QLineEdit()
        custom_layout.addRow(QLabel("叠加组数："), self.lineEdit_num_input)

        # 添加边部停留时间输入框
        self.lineEdit_stay_time_output = QLineEdit()
        custom_layout.addRow(QLabel("边部停留时间："), self.lineEdit_stay_time_output)

        # 将自定义修正方案的布局添加到组框中
        custom_group_box.setLayout(custom_layout)

        # 将组框添加到主布局中
        main_layout.addWidget(custom_group_box)

        # 添加保存按钮
        self.save_button = QPushButton("参数保存")
        self.save_button.clicked.connect(self.save_parameters)
        main_layout.addWidget(self.save_button)

        # 设置主布局
        self.setLayout(main_layout)

    def save_parameters(self):
        # 获取输入的参数
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())