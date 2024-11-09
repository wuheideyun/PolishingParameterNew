from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QStackedWidget, QWidget, QLabel, \
    QHBoxLayout
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 区域1的按钮
        self.button1 = QPushButton("单头摆")
        self.button2 = QPushButton("双头摆")
        self.button3 = QPushButton("同步摆")

        # 连接按钮点击信号
        self.button1.clicked.connect(lambda: self.update_content(0))
        self.button2.clicked.connect(lambda: self.update_content(1))
        self.button3.clicked.connect(lambda: self.update_content(2))

        # 区域2
        self.label_area2 = QLabel("区域2 内容")

        # 区域3和区域4的 QStackedWidget
        self.stacked_widget_area3_4 = QStackedWidget()

        # 初始化单头摆的布局（区域3和区域4分开）
        page_single = QWidget()
        layout_single = QVBoxLayout(page_single)
        self.label_area3 = QLabel("区域3 内容 - 单头摆")
        self.label_area4 = QLabel("区域4 内容 - 单头摆")
        layout_single.addWidget(self.label_area3)
        layout_single.addWidget(self.label_area4)
        self.stacked_widget_area3_4.addWidget(page_single)

        # 初始化双头摆的布局（区域3和区域4合并成一个）
        page_double = QWidget()
        layout_double = QVBoxLayout(page_double)
        self.label_area3_4_combined = QLabel("区域3+4 合并内容 - 双头摆")
        layout_double.addWidget(self.label_area3_4_combined)
        self.stacked_widget_area3_4.addWidget(page_double)

        # 初始化同步摆的布局（区域3和区域4分开）
        page_sync = QWidget()
        layout_sync = QVBoxLayout(page_sync)
        self.label_area3_sync = QLabel("区域3 内容 - 同步摆")
        self.label_area4_sync = QLabel("区域4 内容 - 同步摆")
        layout_sync.addWidget(self.label_area3_sync)
        layout_sync.addWidget(self.label_area4_sync)
        self.stacked_widget_area3_4.addWidget(page_sync)

        # 主布局设置
        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.label_area2)
        layout.addWidget(self.stacked_widget_area3_4)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_content(self, index):
        # 根据选择的按钮索引切换区域3和区域4的内容布局
        self.stacked_widget_area3_4.setCurrentIndex(index)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
