import sys

from PySide6.QtCore import Qt, QSettings, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, \
    QGridLayout, QHBoxLayout

from ImageChangeButton import ImageChangeButton
from JustifiedGridLayout import JustifiedGridLayout


class HostParamSingleWidget(QWidget):
    sig_Saved = Signal()
    def __init__(self):
        super().__init__()


        # 设置窗口标题和大小
        self.setWindowTitle("主机参数(单头摆)设置")
        # self.setGeometry(100, 100, 300, 200)

        self.settings = QSettings("config.ini", QSettings.IniFormat)

        # 创建布局
        layout = QVBoxLayout()
        param_label = QLabel("主机参数")
        param_label.setFixedHeight(50)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 18)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        param_label.setFont(param_font)
        param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(param_label)


        # 定义标签和编辑框的文本
        labels = [
            "横梁间距：", "磨头直径：", "磨块长度：", "工作时长："
        ]

        # 定义编辑框的名称
        line_edit_names = [
            "lineEdit_beam_between", "lineEdit_diameter", "lineEdit_grind_length", "lineEdit_work_time"
        ]
        # 创建自定义的网格布局（增加监听）
        self.content_layout = JustifiedGridLayout(labels, line_edit_names,line_edit_names2=line_edit_names)

        # 添加保存按钮
        self.save_button = ImageChangeButton("参数保存",":SmallFrame",":SmallFrameClicked",114,37,True)
        self.save_button.clicked.connect(self.saveParameters)
        layout.addLayout(self.content_layout)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.loadParameter()
        # 设置主布局
        self.setLayout(layout)

    def saveParameters(self):
        """保存各个LineEdit控件的数据到配置文件"""
        self.settings.setValue("host_param_single_lineEdit_beam_between", self.content_layout.get_line_edit_value("lineEdit_beam_between"))
        self.settings.setValue("host_param_single_lineEdit_diameter", self.content_layout.get_line_edit_value("lineEdit_diameter"))
        self.settings.setValue("host_param_single_lineEdit_grind_length", self.content_layout.get_line_edit_value("lineEdit_grind_length"))
        self.settings.setValue("host_param_single_lineEdit_work_time", self.content_layout.get_line_edit_value("lineEdit_work_time"))
        self.sig_Saved.emit()
    def loadParameter(self):
        """加载配置文件中的数据到各个LineEdit控件"""
        self.content_layout.set_line_edit_value("lineEdit_beam_between",self.settings.value("host_param_single_lineEdit_beam_between", ""))
        self.content_layout.set_line_edit_value("lineEdit_diameter",self.settings.value("host_param_single_lineEdit_diameter", ""))
        self.content_layout.set_line_edit_value("lineEdit_grind_length",self.settings.value("host_param_single_lineEdit_grind_length", ""))
        self.content_layout.set_line_edit_value("lineEdit_work_time",self.settings.value("host_param_single_lineEdit_work_time", ""))
