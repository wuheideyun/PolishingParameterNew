import sys

from PySide6.QtCore import Qt, QSettings, Signal, QEvent
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, \
    QGroupBox, QHBoxLayout, QSpacerItem, QSizePolicy

from ImageChangeButton import ImageChangeButton
from JustifiedGridLayout import JustifiedGridLayout


class MotionInputOutputParamCombineWidget(QWidget):
    sig_Saved = Signal()

    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle(self.tr("运动参数和输出参数设置"))
        self.setFixedSize(410, 820)
        self.settings = QSettings("config.ini", QSettings.IniFormat)
        # 创建主布局
        self.main_layout = QVBoxLayout()
        self.param_label = QLabel(self.tr("运动输入参数"))
        self.param_label.setFixedHeight(35)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 16)
        self.param_label.setFont(param_font)
        self.param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.main_layout.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.main_layout.addWidget(self.param_label)

        # 定义标签和编辑框的文本
        self.labels_up = [
            self.tr("产量大小(m²)："),
            self.tr("摆动速度(mm/s)："),
            self.tr("匀速摆动时间(s)："),
            self.tr("边部停留时间(s)："),
            self.tr("同粒度磨头数(个)："),
            self.tr("加速度大小(mm/s²)："),
            self.tr("进砖宽度(mm)："),
            self.tr("延时时间(s)：")
        ]
        # 定义编辑框的名称
        self.line_edit_names_up = [
            "lineEdit_production_volume", "lineEdit_beam_swing_speed", "lineEdit_beam_constant_time", "lineEdit_stay_time_input",
            "lineEdit_num_input", "lineEdit_accelerate", "lineEdit_ceramic_width", "lineEdit_delay_time"
        ]
        line_edit_names2 = self.line_edit_names_up
        # 创建自定义的网格布局
        self.content_up_layout = JustifiedGridLayout(self.labels_up, self.line_edit_names_up, 25, line_edit_names2, 6,
                                                    self.tr("以下参数仅在顺序摆动模式使用"), "yellow")
        self.main_layout.addLayout(self.content_up_layout)
        # 添加保存按钮
        self.save_button = ImageChangeButton(self.tr("参数保存"), ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        self.save_button.clicked.connect(self.saveParameters)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.save_button)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addStretch()
        self.main_layout.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.param_middle_label = QLabel(self.tr("运动输出参数"))
        self.param_middle_label.setFixedHeight(30)
        self.param_middle_label.setFont(param_font)
        self.param_middle_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.main_layout.addWidget(self.param_middle_label)

        # 定义标签和编辑框的文本
        self.labels_middle = [
            self.tr("主皮带速度(mm/s)："),
            self.tr("摆     幅(mm)：")
        ]
        # 定义编辑框的名称
        self.line_edit_names_middle = [
            "lineEdit_belt_speed", "lineEdit_swing"
        ]
        line_edit_names2 = self.line_edit_names_middle
        # 创建自定义的网格布局
        self.content_middle_layout = JustifiedGridLayout(self.labels_middle, self.line_edit_names_middle, 6, line_edit_names2)
        self.main_layout.addLayout(self.content_middle_layout)
        self.content_middle_layout.set_line_edit_editable(self.line_edit_names_middle, True)

        self.param_bottom_label = QLabel(self.tr("产品质量参数"))
        self.param_bottom_label.setFixedHeight(25)
        self.param_bottom_label.setFont(param_font)
        self.param_bottom_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.main_layout.addWidget(self.param_bottom_label)

        # 定义标签和编辑框的文本
        self.labels_bottom = [
            self.tr("均匀系数：")
        ]
        # 定义编辑框的名称
        self.line_edit_names_bottom = [
            "lineEdit_coefficient"
        ]
        # 创建自定义的网格布局
        self.content_bottom_layout = JustifiedGridLayout(self.labels_bottom, self.line_edit_names_bottom)
        self.main_layout.addLayout(self.content_bottom_layout)
        self.content_bottom_layout.set_line_edit_editable(self.line_edit_names_bottom, True)
        self.main_layout.addSpacerItem(QSpacerItem(0, 15, QSizePolicy.Expanding, QSizePolicy.Fixed))
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
        self.setWindowTitle(self.tr("运动参数和输出参数设置"))
        # 更新标签
        self.param_label.setText(self.tr("运动输入参数"))
        self.param_middle_label.setText(self.tr("运动输出参数"))
        self.param_bottom_label.setText(self.tr("产品质量参数"))
        # 更新网格布局中的标签
        updated_labels_up = [
            self.tr("产量大小(m²)："),
            self.tr("摆动速度(mm/s)："),
            self.tr("匀速摆动时间(s)："),
            self.tr("边部停留时间(s)："),
            self.tr("同粒度磨头数(个)："),
            self.tr("加速度大小(mm/s²)："),
            self.tr("进砖宽度(mm)："),
            self.tr("延时时间(s)：")
        ]
        self.content_up_layout.update_labels(updated_labels_up)
        updated_labels_middle = [
            self.tr("主皮带速度(mm/s)："),
            self.tr("摆     幅(mm)：")
        ]
        self.content_middle_layout.update_labels(updated_labels_middle)
        updated_labels_bottom = [
            self.tr("均匀系数：")
        ]
        self.content_bottom_layout.update_labels(updated_labels_bottom)
        # 更新保存按钮
        self.save_button.set_name(self.tr("参数保存"))

    def saveParameters(self):
        """保存各个LineEdit控件的数据到配置文件"""
        self.settings.setValue("motion_input_output_lineEdit_production_volume", self.content_up_layout.get_line_edit_value("lineEdit_production_volume"))
        self.settings.setValue("motion_input_output_lineEdit_beam_swing_speed", self.content_up_layout.get_line_edit_value("lineEdit_beam_swing_speed"))
        self.settings.setValue("motion_input_output_lineEdit_beam_constant_time", self.content_up_layout.get_line_edit_value("lineEdit_beam_constant_time"))
        self.settings.setValue("motion_input_output_lineEdit_stay_time_input", self.content_up_layout.get_line_edit_value("lineEdit_stay_time_input"))
        self.settings.setValue("motion_input_output_lineEdit_num_input", self.content_up_layout.get_line_edit_value("lineEdit_num_input"))
        self.settings.setValue("motion_input_output_lineEdit_accelerate", self.content_up_layout.get_line_edit_value("lineEdit_accelerate"))
        self.settings.setValue("motion_input_output_lineEdit_ceramic_width", self.content_up_layout.get_line_edit_value("lineEdit_ceramic_width"))
        self.settings.setValue("motion_input_output_lineEdit_delay_time", self.content_up_layout.get_line_edit_value("lineEdit_delay_time"))
        self.sig_Saved.emit()

    def loadParameter(self):
        """加载配置文件中的数据到各个LineEdit控件"""
        self.content_up_layout.set_line_edit_value("lineEdit_production_volume", self.settings.value("motion_input_output_lineEdit_production_volume", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_beam_swing_speed", self.settings.value("motion_input_output_lineEdit_beam_swing_speed", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_beam_constant_time", self.settings.value("motion_input_output_lineEdit_beam_constant_time", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_stay_time_input", self.settings.value("motion_input_output_lineEdit_stay_time_input", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_num_input", self.settings.value("motion_input_output_lineEdit_num_input", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_accelerate", self.settings.value("motion_input_output_lineEdit_accelerate", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_ceramic_width", self.settings.value("motion_input_output_lineEdit_ceramic_width", ""))
        self.content_up_layout.set_line_edit_value("lineEdit_delay_time", self.settings.value("motion_input_output_lineEdit_delay_time", ""))

    def output_report(self):
        pass