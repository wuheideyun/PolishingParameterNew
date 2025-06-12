import sys

from PySide6.QtCore import Qt, QSettings, Signal, QEvent
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QGroupBox, QHBoxLayout

from ImageChangeButton import ImageChangeButton
from JustifiedGridLayout import JustifiedGridLayout


class MotionOutputParamWidget(QWidget):
    sig_Saved = Signal()

    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle(self.tr("运动输出参数和产品质量参数设置"))
        self.settings = QSettings("config.ini", QSettings.IniFormat)
        self.setFixedSize(410, 410)
        # 创建主布局
        self.main_layout = QVBoxLayout()
        self.param_label_up = QLabel(self.tr("运动输出参数"))
        self.param_label_up.setFixedHeight(50)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 16)
        self.param_label_up.setFont(param_font)
        self.param_label_up.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.main_layout.addWidget(self.param_label_up)

        # 定义标签和编辑框的文本
        self.labels_up = [
            self.tr("主皮带速度(mm/s)："),
            self.tr("摆动速度(mm/s)："),
            self.tr("匀速摆动时间(s)："),
            self.tr("边部停留时间(s)："),
            self.tr("摆     幅(mm)："),
            self.tr("同粒度磨头数(个)：")
        ]
        # 定义编辑框的名称
        self.line_edit_names_up = [
            "lineEdit_belt_speed", "lineEdit_beam_swing_speed", "lineEdit_beam_constant_time", "lineEdit_stay_time_output",
            "lineEdit_swing", "lineEdit_num_output"
        ]
        # 创建自定义的网格布局
        self.content_up_layout = JustifiedGridLayout(self.labels_up, self.line_edit_names_up, line_edit_names2=self.line_edit_names_up)
        self.main_layout.addLayout(self.content_up_layout)
        self.content_up_layout.set_line_edit_editable(self.line_edit_names_up, True)

        self.param_label_down = QLabel(self.tr("产品质量参数"))
        self.param_label_down.setFixedHeight(50)
        self.param_label_down.setFont(param_font)
        self.param_label_down.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.main_layout.addWidget(self.param_label_down)

        # 定义标签和编辑框的文本
        self.labels_down = [
            self.tr("均匀系数："),
            self.tr("频次：")
        ]
        # 定义编辑框的名称
        self.line_edit_names_down = [
            "lineEdit_coefficient", "lineEdit_frequency"
        ]
        # 创建自定义的网格布局
        self.content_down_layout = JustifiedGridLayout(self.labels_down, self.line_edit_names_down)
        self.main_layout.addLayout(self.content_down_layout)
        self.content_down_layout.set_line_edit_editable(self.line_edit_names_down, True)


        # self.save_button = ImageChangeButton(self.tr("参数保存"), ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        # self.save_button.clicked.connect(self.saveParameters)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        # self.button_layout.addWidget(self.save_button)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.button_layout)

        self.loadParameter()
        # 设置主布局
        self.setLayout(self.main_layout)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    def retranslate_ui(self):
        """更新界面元素的翻译文本"""
        # 更新窗口标题
        self.setWindowTitle(self.tr("运动输出参数和产品质量参数设置"))
        # 更新标签
        self.param_label_up.setText(self.tr("运动输出参数"))
        self.param_label_down.setText(self.tr("产品质量参数"))
        # 更新网格布局中的标签
        updated_labels_up = [
            self.tr("主皮带速度(mm/s)："),
            self.tr("摆动速度(mm/s)："),
            self.tr("匀速摆动时间(s)："),
            self.tr("边部停留时间(s)："),
            self.tr("摆     幅(mm)："),
            self.tr("同粒度磨头数(个)：")
        ]
        self.content_up_layout.update_labels(updated_labels_up)
        updated_labels_down = [
            self.tr("均匀系数："),
            self.tr("频次：")
        ]
        self.content_down_layout.update_labels(updated_labels_down)
        # 更新保存按钮
        # self.save_button.set_name(self.tr("参数保存"))

    def saveParameters(self):
        """保存各个LineEdit控件的数据到配置文件"""
        self.settings.setValue("motion_output_param_lineEdit_belt_speed", self.content_up_layout.get_line_edit_value("lineEdit_belt_speed"))
        self.settings.setValue("motion_output_param_lineEdit_beam_swing_speed", self.content_up_layout.get_line_edit_value("lineEdit_beam_swing_speed"))
        self.settings.setValue("motion_output_param_lineEdit_beam_constant_time", self.content_up_layout.get_line_edit_value("lineEdit_beam_constant_time"))
        self.settings.setValue("motion_output_param_lineEdit_stay_time_output", self.content_up_layout.get_line_edit_value("lineEdit_stay_time_output"))
        self.settings.setValue("motion_output_param_lineEdit_swing", self.content_up_layout.get_line_edit_value("lineEdit_swing"))
        self.settings.setValue("motion_output_param_lineEdit_num_output", self.content_up_layout.get_line_edit_value("lineEdit_num_output"))
        self.settings.setValue("motion_output_param_lineEdit_coefficient", self.content_down_layout.get_line_edit_value("lineEdit_coefficient"))
        self.settings.setValue("motion_output_param_lineEdit_frequency", self.content_down_layout.get_line_edit_value("lineEdit_frequency"))
        self.sig_Saved.emit()

    def loadParameter(self):
        """加载配置文件中的数据到各个LineEdit控件"""
        self.content_up_layout.set_line_edit_value("lineEdit_belt_speed", self.settings.value("motion_output_param_lineEdit_belt_speed", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_beam_swing_speed", self.settings.value("motion_output_param_lineEdit_beam_swing_speed", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_beam_constant_time", self.settings.value("motion_output_param_lineEdit_beam_constant_time", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_stay_time_output", self.settings.value("motion_output_param_lineEdit_stay_time_output", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_swing", self.settings.value("motion_output_param_lineEdit_swing", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_num_output", self.settings.value("motion_output_param_lineEdit_num_output", ""))
        self.content_down_layout.set_line_edit_value("lineEdit_coefficient", self.settings.value("motion_output_param_lineEdit_coefficient", ""))
        self.content_down_layout.set_line_edit_value("lineEdit_frequency", self.settings.value("motion_output_param_lineEdit_frequency", ""))