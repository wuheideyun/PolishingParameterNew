import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QGroupBox, QHBoxLayout

class MotionInputOutputParamCombineWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("运动参数和输出参数设置")
        # self.setGeometry(100, 100, 400, 400)

        # 创建主布局
        main_layout = QVBoxLayout()
        param_label = QLabel("运动输入参数")
        param_label.setFixedHeight(50)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 18)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        param_label.setFont(param_font)
        param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        main_layout.addWidget(param_label)
        # 创建运动参数的组框
        motion_group_box = QGroupBox("运动参数")
        motion_layout = QFormLayout()

        # 添加主皮带速度输入框
        self.lineEdit_belt_speed = QLineEdit()
        motion_layout.addRow(QLabel("主皮带速度："), self.lineEdit_belt_speed)

        # 添加横梁摆动速度输入框
        self.lineEdit_beam_swing_speed = QLineEdit()
        motion_layout.addRow(QLabel("横梁摆动速度："), self.lineEdit_beam_swing_speed)

        # 添加横梁匀速摆动时间输入框
        self.lineEdit_beam_constant_time = QLineEdit()
        motion_layout.addRow(QLabel("横梁匀速摆动时间："), self.lineEdit_beam_constant_time)

        # 添加边部停留时间输入框
        self.lineEdit_stay_time_input = QLineEdit()
        motion_layout.addRow(QLabel("边部停留时间："), self.lineEdit_stay_time_input)

        # 添加同款度磨头数输入框
        self.lineEdit_num_output = QLineEdit()
        motion_layout.addRow(QLabel("同粒度磨头数："), self.lineEdit_num_output)

        # 添加加速度大小输入框
        self.lineEdit_accelerate = QLineEdit()
        motion_layout.addRow(QLabel("加速度大小："), self.lineEdit_accelerate)

        # 添加进砖宽度输入框
        self.lineEdit_ceramic_width = QLineEdit()
        motion_layout.addRow(QLabel("进砖宽度："), self.lineEdit_ceramic_width)

        # 添加延时时间输入框
        self.lineEdit_delay_time = QLineEdit()
        motion_layout.addRow(QLabel("延时时间："), self.lineEdit_delay_time)

        # 将运动参数的布局添加到组框中
        motion_group_box.setLayout(motion_layout)

        # 将组框添加到主布局中
        main_layout.addWidget(motion_group_box)

        # 创建输出参数的组框
        output_group_box = QGroupBox("输出参数")
        output_layout = QFormLayout()

        # 添加摆幅输入框
        self.lineEdit_swing = QLineEdit()
        output_layout.addRow(QLabel("摆幅："), self.lineEdit_swing)

        # 添加产量大小输入框
        self.lineEdit_production_volume = QLineEdit()
        output_layout.addRow(QLabel("产量大小："), self.lineEdit_production_volume)

        # 添加均匀系数输入框
        self.lineEdit_coefficient = QLineEdit()
        output_layout.addRow(QLabel("均匀系数："), self.lineEdit_coefficient)

        # 将输出参数的布局添加到组框中
        output_group_box.setLayout(output_layout)

        # 将组框添加到主布局中
        main_layout.addWidget(output_group_box)


        # 设置主布局
        self.setLayout(main_layout)

    def output_report(self):
        # 获取输入的参数
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())