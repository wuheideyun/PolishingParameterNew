from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("同步摆抛光参数计算系统")
        self.setFixedSize(1500, 700)

        # 主布局
        main_layout = QHBoxLayout(self)

        # 左侧面板布局
        left_panel = QVBoxLayout()
        # 标题
        title_label = QLabel("KEDA")
        title_label.setStyleSheet("font-size: 30px; color: white;")

        # 按钮
        button1 = QPushButton("1 单头摆")
        button2 = QPushButton("2 双头摆")
        buttonN = QPushButton("N 同步摆")

        # 设置按钮样式
        button_style = """
            QPushButton {
                font-size: 18px;
                color: white;
                background-color: #1e90ff;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #6495ed;
            }
        """
        button1.setStyleSheet(button_style)
        button2.setStyleSheet(button_style)
        buttonN.setStyleSheet(button_style)

        left_panel.addWidget(title_label)
        left_panel.addWidget(button1)
        left_panel.addWidget(button2)
        left_panel.addWidget(buttonN)

        # 图片区域
        img_label = QLabel(self)
        img_pixmap = QPixmap("your_image_path.png").scaled(400, 400, Qt.KeepAspectRatio)
        img_label.setPixmap(img_pixmap)
        left_panel.addWidget(img_label)

        # 中间图表区域
        middle_panel = QVBoxLayout()
        chart1 = QLabel("图表1")
        chart1.setStyleSheet("background-color: white; border: 2px solid #1e90ff;")
        chart1.setFixedSize(600, 200)
        chart2 = QLabel("图表2")
        chart2.setStyleSheet("background-color: white; border: 2px solid #1e90ff;")
        chart2.setFixedSize(600, 200)

        middle_panel.addWidget(chart1)
        middle_panel.addWidget(chart2)

        # 右侧参数区域
        right_panel = QVBoxLayout()
        param_label = QLabel("运动参数")
        param_label.setStyleSheet("font-size: 24px; color: white;")

        param_info = QLabel("122333\n32111213123\n...")
        param_info.setStyleSheet("font-size: 18px; color: white;")

        calc_button = QPushButton("高效计算")
        calc_button.setStyleSheet(button_style)
        output_button = QPushButton("输出报告")
        output_button.setStyleSheet(button_style)

        right_panel.addWidget(param_label)
        right_panel.addWidget(param_info)
        right_panel.addWidget(calc_button)
        right_panel.addWidget(output_button)

        # 布局整合
        main_layout.addLayout(left_panel)
        main_layout.addLayout(middle_panel)
        main_layout.addLayout(right_panel)

        # 设置背景色
        self.setStyleSheet("background-color: #001f3f;")


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
