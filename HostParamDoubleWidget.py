import sys

from PySide6.QtCore import Qt, QSettings, Signal, QEvent
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, \
    QHBoxLayout

from ImageChangeButton import ImageChangeButton
from JustifiedGridLayout import JustifiedGridLayout


class HostParamDoubleWidget(QWidget):
    sig_Saved = Signal()

    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle(self.tr("主机参数(双头摆)设置"))

        self.settings = QSettings("config.ini", QSettings.IniFormat)
        # 创建布局
        self.layout = QVBoxLayout()
        self.param_label = QLabel(self.tr("主机参数"))
        self.param_label.setFixedHeight(50)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 18)
        self.param_label.setFont(param_font)
        self.param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layout.addWidget(self.param_label)

        # 添加一个负的上边距，使标签向上移动10个像素
        self.param_label.setContentsMargins(0, -20, 0, 0)
        # 定义标签和编辑框的文本
        self.labels_text = [
            self.tr("磨头间距(mm)："),
            self.tr("横梁间距(mm)："),
            self.tr("磨头直径(mm)："),
            self.tr("磨块长度(mm)："),
            self.tr("工作时长(h)：")
        ]
        # 定义编辑框的名称
        self.line_edit_names = [
            "lineEdit_between", "lineEdit_beam_between", "lineEdit_diameter", "lineEdit_grind_length", "lineEdit_work_time"
        ]
        # 创建自定义的网格布局(对所有参数增加监听)
        self.content_layout = JustifiedGridLayout(self.labels_text, self.line_edit_names, 6, self.line_edit_names, -1, '', '')

        # 添加保存按钮
        self.save_button = ImageChangeButton(self.tr("参数保存"), ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        self.save_button.clicked.connect(self.saveParameters)
        self.layout.addLayout(self.content_layout)
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.save_button)
        self.layout.addStretch()
        self.layout.addLayout(self.button_layout)
        self.loadParameter()
        # 设置主布局
        self.setLayout(self.layout)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    def retranslate_ui(self):
        """更新界面元素的翻译文本"""
        # 更新窗口标题
        self.setWindowTitle(self.tr("主机参数(双头摆)设置"))
        # 更新参数标签
        self.param_label.setText(self.tr("主机参数"))
        # 更新网格布局中的标签
        updated_labels = [
            self.tr("磨头间距(mm)："),
            self.tr("横梁间距(mm)："),
            self.tr("磨头直径(mm)："),
            self.tr("磨块长度(mm)："),
            self.tr("工作时长(h)：")
        ]
        self.content_layout.update_labels(updated_labels)
        # 更新保存按钮文本
        self.save_button.set_name(self.tr("参数保存"))

    def saveParameters(self):
        """保存各个LineEdit控件的数据到配置文件"""
        self.settings.setValue("host_param_double_lineEdit_between", self.content_layout.get_line_edit_value("lineEdit_between"))
        self.settings.setValue("host_param_double_lineEdit_beam_between", self.content_layout.get_line_edit_value("lineEdit_beam_between"))
        self.settings.setValue("host_param_double_lineEdit_diameter", self.content_layout.get_line_edit_value("lineEdit_diameter"))
        self.settings.setValue("host_param_double_lineEdit_grind_length", self.content_layout.get_line_edit_value("lineEdit_grind_length"))
        self.settings.setValue("host_param_double_lineEdit_work_time", self.content_layout.get_line_edit_value("lineEdit_work_time"))
        self.sig_Saved.emit()

    def loadParameter(self):
        """加载配置文件中的数据到各个LineEdit控件"""
        self.content_layout.set_line_edit_value("lineEdit_between", self.settings.value("host_param_double_lineEdit_between", ""))
        self.content_layout.set_line_edit_value("lineEdit_beam_between", self.settings.value("host_param_double_lineEdit_beam_between", ""))
        self.content_layout.set_line_edit_value("lineEdit_diameter", self.settings.value("host_param_double_lineEdit_diameter", ""))
        self.content_layout.set_line_edit_value("lineEdit_grind_length", self.settings.value("host_param_double_lineEdit_grind_length", ""))
        self.content_layout.set_line_edit_value("lineEdit_work_time", self.settings.value("host_param_double_lineEdit_work_time", ""))