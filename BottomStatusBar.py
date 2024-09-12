from PySide6.QtGui import QAction
from PySide6.QtWidgets import QStatusBar, QMainWindow


class BottomStatusBar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)