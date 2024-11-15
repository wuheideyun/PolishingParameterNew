import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, \
    QGroupBox, QHBoxLayout, QSpacerItem, QSizePolicy

from JustifiedGridLayout import JustifiedGridLayout


class MotionInputOutputParamCombineWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("运动参数和输出参数设置")
        # self.setGeometry(100, 100, 400, 400)

        # 创建主布局
        main_layout = QVBoxLayout()
        param_label = QLabel("运动输入参数")
        param_label.setFixedHeight(35)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 16)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        param_label.setFont(param_font)
        param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        main_layout.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Fixed, QSizePolicy.Fixed))
        main_layout.addWidget(param_label)

        # 定义标签和编辑框的文本
        labels = [
            "产量大小：", "摆动速度：", "匀速摆动时间：", "边部停留时间：", "同粒度磨头数：", "加速度大小：", "进砖宽度：", "延时时间："
        ]

        # 定义编辑框的名称
        line_edit_names = [
            "lineEdit_production_volume", "lineEdit_beam_swing_speed", "lineEdit_beam_constant_time", "lineEdit_stay_time_input",
            "lineEdit_num_output", "lineEdit_accelerate", "lineEdit_ceramic_width", "lineEdit_delay_time"
        ]

        # 创建自定义的网格布局
        self.content_up_layout = JustifiedGridLayout(labels, line_edit_names,40)
        main_layout.addLayout(self.content_up_layout)

        main_layout.addStretch()

        param_middle_label = QLabel("运动输出参数")
        param_middle_label.setFixedHeight(30)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 16)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        param_middle_label.setFont(param_font)
        param_middle_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        main_layout.addWidget(param_middle_label)

        # 定义标签和编辑框的文本
        labels = [
            "主皮带速度：", "摆幅："
        ]

        # 定义编辑框的名称
        line_edit_names = [
            "lineEdit_belt_speed", "lineEdit_swing"
        ]

        # 创建自定义的网格布局
        self.content_middle_layout = JustifiedGridLayout(labels, line_edit_names)
        main_layout.addLayout(self.content_middle_layout)

        param_bottom_label = QLabel("产品质量参数")
        param_bottom_label.setFixedHeight(30)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 16)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        param_bottom_label.setFont(param_font)
        param_bottom_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        main_layout.addWidget(param_bottom_label)

        # 定义标签和编辑框的文本
        labels = [
            "均匀系数："
        ]

        # 定义编辑框的名称
        line_edit_names = [
            "lineEdit_coefficient"
        ]

        # 创建自定义的网格布局
        self.content_bottom_layout = JustifiedGridLayout(labels, line_edit_names)
        main_layout.addLayout(self.content_bottom_layout)
        main_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Fixed))

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