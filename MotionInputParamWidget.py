import sys

from PySide6.QtCore import Qt, QSettings, Signal, QEvent
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QGroupBox, QHBoxLayout

from ImageChangeButton import ImageChangeButton
from JustifiedGridLayout import JustifiedGridLayout


class MotionInputParamWidget(QWidget):
    sig_Saved = Signal()

    def __init__(self):
        super().__init__()
        self.settings = QSettings("config.ini", QSettings.IniFormat)
        # 设置窗口标题
        self.setWindowTitle(self.tr("运动输入参数设置"))
        self.setFixedSize(400, 410)

        # 创建主布局
        self.main_layout = QVBoxLayout()
        self.param_label = QLabel(self.tr("运动输入参数"))
        self.param_label.setFixedHeight(50)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 16)
        self.param_label.setFont(param_font)
        self.param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.main_layout.addWidget(self.param_label)

        # 定义标签和编辑框的文本
        self.labels = [
            self.tr("产量大小(m²)："),
            self.tr("进砖宽度(mm)："),
            self.tr("加速度大小(mm/s²)："),
            self.tr("轨迹重叠量(mm)："),
            self.tr("单组覆盖磨头数(个)："),
            self.tr("叠加组数(个)："),
            self.tr("边部停留时间(s)：")
        ]
        # 定义编辑框的名称
        self.line_edit_names = [
            "lineEdit_production_volume", "lineEdit_ceramic_width", "lineEdit_accelerate", "lineEdit_overlap",
            "lineEdit_num_input", "lineEdit_group_count", "lineEdit_stay_time_input"
        ]
        line_edit_names2 = ["lineEdit_production_volume"]
        # 创建自定义的网格布局
        self.content_layout = JustifiedGridLayout(self.labels, self.line_edit_names, 6, line_edit_names2, 3,
                                                 self.tr("以下参数仅在自定义修正方案使用"), "yellow")

        # 添加保存按钮
        self.save_button = ImageChangeButton(self.tr("参数保存"), ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        self.save_button.clicked.connect(self.saveParameters)
        self.main_layout.addLayout(self.content_layout)
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.save_button)
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
        self.setWindowTitle(self.tr("运动输入参数设置"))
        # 更新标签
        self.param_label.setText(self.tr("运动输入参数"))
        # 更新网格布局中的标签
        updated_labels = [
            self.tr("产量大小(m²)："),
            self.tr("进砖宽度(mm)："),
            self.tr("加速度大小(mm/s²)："),
            self.tr("轨迹重叠量(mm)："),
            self.tr("单组覆盖磨头数(个)："),
            self.tr("叠加组数(个)："),
            self.tr("边部停留时间(s)：")
        ]
        self.content_layout.update_labels(updated_labels)
        # 更新保存按钮
        self.save_button.set_name(self.tr("参数保存"))

    def saveParameters(self):
        """保存各个LineEdit控件的数据到配置文件"""
        self.settings.setValue("motion_input_lineEdit_production_volume", self.content_layout.get_line_edit_value("lineEdit_production_volume"))
        self.settings.setValue("motion_input_lineEdit_ceramic_width", self.content_layout.get_line_edit_value("lineEdit_ceramic_width"))
        self.settings.setValue("motion_input_lineEdit_accelerate", self.content_layout.get_line_edit_value("lineEdit_accelerate"))
        self.settings.setValue("motion_input_lineEdit_overlap", self.content_layout.get_line_edit_value("lineEdit_overlap"))
        self.settings.setValue("motion_input_lineEdit_num_input", self.content_layout.get_line_edit_value("lineEdit_num_input"))
        self.settings.setValue("motion_input_lineEdit_group_count", self.content_layout.get_line_edit_value("lineEdit_group_count"))
        self.settings.setValue("motion_input_lineEdit_stay_time_input", self.content_layout.get_line_edit_value("lineEdit_stay_time_input"))
        self.sig_Saved.emit()

    def loadParameter(self):
        """加载配置文件中的数据到各个LineEdit控件"""
        self.content_layout.set_line_edit_value("lineEdit_production_volume", self.settings.value("motion_input_lineEdit_production_volume", ""))
        self.content_layout.set_line_edit_value("lineEdit_ceramic_width", self.settings.value("motion_input_lineEdit_ceramic_width", ""))
        self.content_layout.set_line_edit_value("lineEdit_accelerate", self.settings.value("motion_input_lineEdit_accelerate", ""))
        self.content_layout.set_line_edit_value("lineEdit_overlap", self.settings.value("motion_input_lineEdit_overlap", ""))
        self.content_layout.set_line_edit_value("lineEdit_num_input", self.settings.value("motion_input_lineEdit_num_input", ""))
        self.content_layout.set_line_edit_value("lineEdit_group_count", self.settings.value("motion_input_lineEdit_group_count", ""))
        self.content_layout.set_line_edit_value("lineEdit_stay_time_input", self.settings.value("motion_input_lineEdit_stay_time_input", ""))