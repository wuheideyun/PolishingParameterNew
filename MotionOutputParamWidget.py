import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QGroupBox, QHBoxLayout

class MotionOutputParamWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("运动输出参数和产品质量参数设置")
        # self.setGeometry(100, 100, 400, 300)

        # self.setFixedSize(400,310)
        # 创建主布局
        main_layout = QVBoxLayout()
        param_label = QLabel("运动输出参数")
        param_label.setFixedHeight(50)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 18)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        param_label.setFont(param_font)
        param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        main_layout.addWidget(param_label)
        # 创建运动输出参数的组框
        motion_group_box = QGroupBox("运动输出参数")
        motion_layout = QFormLayout()

        # 添加主皮带速度输入框
        self.main_belt_speed_input = QLineEdit()
        motion_layout.addRow(QLabel("主皮带速度："), self.main_belt_speed_input)

        # 添加摆动速度输入框
        self.swing_speed_input = QLineEdit()
        motion_layout.addRow(QLabel("摆动速度："), self.swing_speed_input)

        # 添加匀速摆动时间输入框
        self.constant_swing_time_input = QLineEdit()
        motion_layout.addRow(QLabel("匀速摆动时间："), self.constant_swing_time_input)

        # 添加边部停留时间输入框
        self.edge_stay_time_input = QLineEdit()
        motion_layout.addRow(QLabel("边部停留时间："), self.edge_stay_time_input)

        # 添加摆幅输入框
        self.swing_amplitude_input = QLineEdit()
        motion_layout.addRow(QLabel("摆幅："), self.swing_amplitude_input)

        # 添加同粒度磨头数输入框
        self.same_grain_moto_count_input = QLineEdit()
        motion_layout.addRow(QLabel("同粒度磨头数："), self.same_grain_moto_count_input)

        # 将运动输出参数的布局添加到组框中
        motion_group_box.setLayout(motion_layout)

        # 将组框添加到主布局中
        main_layout.addWidget(motion_group_box)

        # 创建产品质量参数的组框
        quality_group_box = QGroupBox("产品质量参数")
        quality_layout = QFormLayout()

        # 添加均匀系数输入框
        self.uniformity_coefficient_input = QLineEdit()
        quality_layout.addRow(QLabel("均匀系数："), self.uniformity_coefficient_input)

        # 将产品质量参数的布局添加到组框中
        quality_group_box.setLayout(quality_layout)

        # 将组框添加到主布局中
        main_layout.addWidget(quality_group_box)


        # 设置主布局
        self.setLayout(main_layout)

    def save_parameters(self):
        # 获取输入的参数
        main_belt_speed = self.main_belt_speed_input.text()
        swing_speed = self.swing_speed_input.text()
        constant_swing_time = self.constant_swing_time_input.text()
        edge_stay_time = self.edge_stay_time_input.text()
        swing_amplitude = self.swing_amplitude_input.text()
        same_grain_moto_count = self.same_grain_moto_count_input.text()
        uniformity_coefficient = self.uniformity_coefficient_input.text()

        # 打印参数（实际应用中可以保存到文件或数据库）
        print("主皮带速度:", main_belt_speed)
        print("摆动速度:", swing_speed)
        print("匀速摆动时间:", constant_swing_time)
        print("边部停留时间:", edge_stay_time)
        print("摆幅:", swing_amplitude)
        print("同粒度磨头数:", same_grain_moto_count)
        print("均匀系数:", uniformity_coefficient)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())