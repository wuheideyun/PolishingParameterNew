import sys

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QGroupBox, QHBoxLayout

from ImageChangeButton import ImageChangeButton
from JustifiedGridLayout import JustifiedGridLayout


class MotionOutputParamWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("运动输出参数和产品质量参数设置")
        # self.setGeometry(100, 100, 400, 300)
        self.settings = QSettings("config.ini", QSettings.IniFormat)

        # self.setFixedSize(400,310)
        # 创建主布局
        self.main_layout = QVBoxLayout()
        param_label = QLabel("运动输出参数")
        param_label.setFixedHeight(50)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 16)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        param_label.setFont(param_font)
        param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.main_layout.addWidget(param_label)

        # 定义标签和编辑框的文本
        labels = [
            "主皮带速度：", "摆动速度：", "匀速摆动时间：", "边部停留时间：", "摆幅：", "同粒度磨头数："
        ]
        # 定义编辑框的名称
        line_edit_names = [
            "lineEdit_belt_speed", "lineEdit_beam_swing_speed", "lineEdit_beam_constant_time", "lineEdit_stay_time_output",
            "lineEdit_swing", "lineEdit_num_output"
        ]
        # 创建自定义的网格布局
        self.content_up_layout = JustifiedGridLayout(labels, line_edit_names,line_edit_names2 = line_edit_names)
        self.main_layout.addLayout(self.content_up_layout)

        param_label = QLabel("产品质量参数")
        param_label.setFixedHeight(50)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 16)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        param_label.setFont(param_font)
        param_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.main_layout.addWidget(param_label)

        # 定义标签和编辑框的文本
        labels = [
            "均匀系数："
        ]
        # 定义编辑框的名称
        line_edit_names = [
             "lineEdit_coefficient"
        ]
        # 创建自定义的网格布局
        self.content_down_layout = JustifiedGridLayout(labels, line_edit_names)
        self.main_layout.addLayout(self.content_down_layout)

        # 添加保存按钮
        self.save_button = ImageChangeButton("参数保存", ":SmallFrame", ":SmallFrameClicked", 114, 37,True)
        self.save_button.clicked.connect(self.saveParameters)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        self.main_layout.addStretch()
        self.main_layout.addLayout(button_layout)

        self.loadParameter()
        # 设置主布局
        self.setLayout(self.main_layout)

    def saveParameters(self):
        """保存各个LineEdit控件的数据到配置文件"""
        self.settings.setValue("motion_output_param_lineEdit_belt_speed", self.content_up_layout.get_line_edit_value("lineEdit_belt_speed"))
        self.settings.setValue("motion_output_param_lineEdit_beam_swing_speed", self.content_up_layout.get_line_edit_value("lineEdit_beam_swing_speed"))
        self.settings.setValue("motion_output_param_lineEdit_beam_constant_time", self.content_up_layout.get_line_edit_value("lineEdit_beam_constant_time"))
        self.settings.setValue("motion_output_param_lineEdit_stay_time_output", self.content_up_layout.get_line_edit_value("lineEdit_stay_time_output"))
        self.settings.setValue("motion_output_param_lineEdit_lineEdit_swing", self.content_up_layout.get_line_edit_value("lineEdit_swing"))
        self.settings.setValue("motion_output_param_lineEdit_lineEdit_num_output", self.content_up_layout.get_line_edit_value("lineEdit_num_output"))
        self.settings.setValue("motion_output_param_lineEdit_lineEdit_coefficient", self.content_down_layout.get_line_edit_value("lineEdit_coefficient"))

    def loadParameter(self):
        """加载配置文件中的数据到各个LineEdit控件"""
        self.content_up_layout.set_line_edit_value("lineEdit_belt_speed", self.settings.value("motion_output_param_lineEdit_belt_speed", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_beam_swing_speed", self.settings.value("motion_output_param_lineEdit_beam_swing_speed", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_beam_constant_time", self.settings.value("motion_output_param_lineEdit_beam_constant_time", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_stay_time_output", self.settings.value("motion_output_param_lineEdit_stay_time_output", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_swing", self.settings.value("motion_output_param_lineEdit_lineEdit_swing", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_num_output", self.settings.value("motion_output_param_lineEdit_lineEdit_num_output", ""))
        self.content_down_layout.set_line_edit_value("lineEdit_coefficient", self.settings.value("motion_output_param_lineEdit_lineEdit_coefficient", ""))