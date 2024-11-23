import sys

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QGroupBox, QHBoxLayout

from ImageChangeButton import ImageChangeButton
from JustifiedGridLayout import JustifiedGridLayout


class MotionInputParamWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("config.ini", QSettings.IniFormat)  # 使用配置文件
        # 设置窗口标题和大小
        self.setWindowTitle("运动输入参数设置")
        # self.setGeometry(100, 100, 400, 300)
        # self.setFixedSize(400,310)

        # 创建主布局
        main_layout = QVBoxLayout()
        param_label = QLabel("运动输入参数")
        param_label.setFixedHeight(50)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 16)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        param_label.setFont(param_font)
        param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        main_layout.addWidget(param_label)

        # 定义标签和编辑框的文本
        labels = [
            "产量大小：", "进砖宽度：", "加速度大小：", "轨迹重叠量：", "单组覆盖磨头数：", "叠加组数：", "边部停留时间："
        ]

        # 定义编辑框的名称
        line_edit_names = [
            "lineEdit_production_volume", "lineEdit_ceramic_width", "lineEdit_accelerate", "lineEdit_overlap", "lineEdit_num_input","lineEdit_group_count", "lineEdit_stay_time_input"
        ]

        # 定义编辑框的名称
        line_edit_names2 = [
            "lineEdit_production_volume"
        ]
        # 创建自定义的网格布局
        self.content_layout = JustifiedGridLayout(labels, line_edit_names,6,line_edit_names2,3,'以下参数仅在自定义修正方案使用','yellow')

        # 添加保存按钮
        self.save_button = ImageChangeButton("参数保存", ":SmallFrame", ":SmallFrameClicked", 114, 37,True)
        self.save_button.clicked.connect(self.save_parameters)
        main_layout.addLayout(self.content_layout)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.content_layout.textChanged.connect(self.on_text_changed)

        self.loadParameter()  # 在初始化时加载设置
        # 设置主布局
        self.setLayout(main_layout)

    # 连接信号到槽函数
    def on_text_changed(name, text):
        print(f"Text changed in {name}: {text}")
    def save_parameters(self):
        # 获取输入的参数
        """保存各个LineEdit控件的数据到配置文件"""
        self.settings.setValue("motion_input_lineEdit_production_volume", self.content_layout.get_line_edit_value("lineEdit_production_volume"))
        self.settings.setValue("motion_input_lineEdit_ceramic_width", self.content_layout.get_line_edit_value("lineEdit_ceramic_width"))
        self.settings.setValue("motion_input_lineEdit_accelerate", self.content_layout.get_line_edit_value("lineEdit_accelerate"))
        self.settings.setValue("motion_input_lineEdit_overlap", self.content_layout.get_line_edit_value("lineEdit_overlap"))
        self.settings.setValue("motion_input_lineEdit_num_input", self.content_layout.get_line_edit_value("lineEdit_num_input"))
        self.settings.setValue("motion_input_lineEdit_group_count", self.content_layout.get_line_edit_value("lineEdit_group_count"))
        self.settings.setValue("motion_input_lineEdit_stay_time_input", self.content_layout.get_line_edit_value("lineEdit_stay_time_input"))
    def loadParameter(self):
        """加载配置文件中的数据到各个LineEdit控件"""
        self.content_layout.set_line_edit_value("lineEdit_production_volume",self.settings.value("motion_input_lineEdit_production_volume", ""))
        self.content_layout.set_line_edit_value("lineEdit_ceramic_width",self.settings.value("motion_input_lineEdit_ceramic_width", ""))
        self.content_layout.set_line_edit_value("lineEdit_accelerate",self.settings.value("motion_input_lineEdit_accelerate", ""))
        self.content_layout.set_line_edit_value("lineEdit_overlap",self.settings.value("motion_input_lineEdit_overlap", ""))
        self.content_layout.set_line_edit_value("lineEdit_num_input",self.settings.value("motion_input_lineEdit_num_input", ""))
        self.content_layout.set_line_edit_value("lineEdit_group_count",self.settings.value("motion_input_lineEdit_group_count", ""))
        self.content_layout.set_line_edit_value("lineEdit_stay_time_input",self.settings.value("motion_input_lineEdit_stay_time_input", ""))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())