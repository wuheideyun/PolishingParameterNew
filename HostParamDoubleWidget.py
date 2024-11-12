import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, \
    QHBoxLayout

from ImageChangeButton import ImageChangeButton
from JustifiedGridLayout import JustifiedGridLayout


class HostParamDoubleWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("主机参数(双头摆)设置")
        # self.setGeometry(100, 100, 300, 200)

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
            "磨头间距：", "横梁间距：", "磨头直径：", "磨块长度："
        ]
        # 定义编辑框的名称
        line_edit_names = [
            "lineEdit_between", "lineEdit_beam_between", "lineEdit_diameter", "lineEdit_grind_length"
        ]
        # 创建自定义的网格布局
        self.content_layout = JustifiedGridLayout(labels, line_edit_names,-1,'','')

        # 添加保存按钮
        self.save_button = ImageChangeButton("参数保存", ":SmallFrame", ":SmallFrameClicked", 114, 37,True)
        self.save_button.clicked.connect(self.save_parameters)
        layout.addLayout(self.content_layout)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        layout.addStretch()
        layout.addLayout(button_layout)

        # 设置主布局
        self.setLayout(layout)

    def save_parameters(self):
        # 获取输入的参数
        between = self.content_layout.get_line_edit_value('lineEdit_between')
        beam_between = self.content_layout.get_line_edit_value('lineEdit_beam_between')
        diameter = self.content_layout.get_line_edit_value('lineEdit_diameter')
        grind_size = self.content_layout.get_line_edit_value('lineEdit_grind_size')

        # 打印参数（实际应用中可以保存到文件或数据库）
        print("磨头间距:", between)
        print("横梁间距:", beam_between)
        print("磨头直径:", diameter)
        print("磨块长度:", grind_size)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = HostParamDoubleWidget()
    window.show()

    sys.exit(app.exec())