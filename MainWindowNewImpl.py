from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

import MainWindowNew_back
from LeftBar import LeftBar


class MainWindowNewImpl(QMainWindow,MainWindowNew.Ui_MainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(main_window)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)  # 设置为无边框窗口

        # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.leftbar_widget = LeftBar()
        self.leftbar_widget.show()

        # 按钮操作

