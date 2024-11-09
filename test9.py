from PySide6.QtWidgets import (QApplication, QWidget, QGridLayout, QVBoxLayout,
                               QLabel, QPushButton, QLineEdit, QHBoxLayout, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置主窗口
        self.setWindowTitle("抛光参数计算系统")
        # self.setStyleSheet("background-color: #0d1b3d; color: white; font-size: 14px;")
        # self.setStyleSheet("background-image: url('./Resources/NewUI/Base/background.png'); background-repeat: no-repeat; background-size: cover;")

        # 设置主布局，左中右按1:5:1比例布局
        main_layout = QGridLayout(self)
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 5)
        main_layout.setColumnStretch(2, 1)

        # 区域1 - 左侧按钮
        self.setup_area1(main_layout)
        # 区域2 - 机型图
        self.setup_area2(main_layout)
        # 区域3 - 主机参数
        self.setup_area3(main_layout)
        # 区域4 - 轨迹分布
        self.setup_area4(main_layout)
        # 区域5 - 轨迹动画
        self.setup_area5(main_layout)
        # 区域6 - 模式选择和方案选择
        self.setup_area6(main_layout)
        # 区域7 - 运动输入参数
        self.setup_area7(main_layout)
        # 区域8 - 运动输出参数
        self.setup_area8(main_layout)
        # 区域9 - 输出报告按钮
        self.setup_area9(main_layout)

    def setup_area1(self, layout):
        area1 = QGroupBox()
        area1_layout = QVBoxLayout()
        buttons = ["单头摆", "双头摆", "同步摆"]
        for text in buttons:
            button = QPushButton(text)
            button.setStyleSheet("background-color: #1f3b5c;")
            area1_layout.addWidget(button)
        area1.setLayout(area1_layout)
        layout.addWidget(area1, 0, 0, 3, 1)

    def setup_area2(self, layout):
        area2 = QLabel("机型图")
        area2.setAlignment(Qt.AlignCenter)
        area2.setStyleSheet("border: 1px solid #1f3b5c;")
        layout.addWidget(area2, 1, 1)

    def setup_area3(self, layout):
        area3 = QGroupBox("主机参数")
        area3_layout = QVBoxLayout()
        labels = ["磨头间距", "横梁间距", "磨头直径", "磨块长度"]
        for label_text in labels:
            row_layout = QHBoxLayout()
            label = QLabel(label_text)
            edit = QLineEdit()
            row_layout.addWidget(label)
            row_layout.addWidget(edit)
            area3_layout.addLayout(row_layout)
        save_button = QPushButton("参数保存")
        area3_layout.addWidget(save_button)
        area3.setLayout(area3_layout)
        layout.addWidget(area3, 2, 1)

    def setup_area4(self, layout):
        area4 = QLabel("轨迹分布")
        area4.setAlignment(Qt.AlignCenter)
        area4.setStyleSheet("border: 1px solid #1f3b5c;")
        layout.addWidget(area4, 0, 1)

    def setup_area5(self, layout):
        area5 = QLabel("轨迹动画")
        area5.setAlignment(Qt.AlignCenter)
        area5.setStyleSheet("border: 1px solid #1f3b5c;")
        layout.addWidget(area5, 1, 2)

    def setup_area6(self, layout):
        area6 = QGroupBox()
        area6_layout = QVBoxLayout()
        labels = ["模式选择", "方案选择"]
        for label_text in labels:
            label = QLabel(label_text)
            area6_layout.addWidget(label)
        buttons = ["智能寻优模式", "人工寻优模式", "节能方案", "高品质方案", "自定义修正方案"]
        button_layout = QHBoxLayout()
        for text in buttons:
            button = QPushButton(text)
            button.setStyleSheet("background-color: #1f3b5c;")
            button_layout.addWidget(button)
        area6_layout.addLayout(button_layout)
        area6.setLayout(area6_layout)
        layout.addWidget(area6, 2, 1)

    def setup_area7(self, layout):
        area7 = QGroupBox("运动输入参数")
        area7_layout = QVBoxLayout()
        labels = ["产量大小", "进砖宽度", "加速度大小", "轨迹重量",
                  "<font color='red'>以下参数仅在自定义修正方案使用</font>",
                  "单组覆盖磨头数", "叠加组数", "边部停留时间"]
        for label_text in labels:
            row_layout = QHBoxLayout()
            label = QLabel(label_text)
            edit = QLineEdit()
            row_layout.addWidget(label)
            row_layout.addWidget(edit)
            area7_layout.addLayout(row_layout)
        save_button = QPushButton("参数保存")
        area7_layout.addWidget(save_button)
        area7.setLayout(area7_layout)
        layout.addWidget(area7, 1, 2)

    def setup_area8(self, layout):
        area8 = QGroupBox("运动输出参数")
        area8_layout = QVBoxLayout()
        labels = ["主皮带速度", "摆动速度", "加速摆动时间", "边部停留时间", "摆幅", "同粒度磨头数"]
        for label_text in labels:
            row_layout = QHBoxLayout()
            label = QLabel(label_text)
            edit = QLineEdit()
            row_layout.addWidget(label)
            row_layout.addWidget(edit)
            area8_layout.addLayout(row_layout)
        save_button = QPushButton("参数保存")
        area8_layout.addWidget(save_button)
        area8.setLayout(area8_layout)
        layout.addWidget(area8, 2, 2)

    def setup_area9(self, layout):
        area9 = QPushButton("输出报告")
        area9.setStyleSheet("background-color: #ff4b4b; color: white;")
        layout.addWidget(area9, 3, 2)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
