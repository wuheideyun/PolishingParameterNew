'''

无边框对话框

'''

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QGraphicsDropShadowEffect, QWidget, QVBoxLayout


class FrameLessDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)  # 设置为无边框窗口

        self.setAttribute(Qt.WA_StyledBackground)  # 禁止父窗口样式影响子控件样式
        self.setStyleSheet('''
                            QDialog {
                                background-color: rgb(255, 254, 253);
                                border-radius: 10px;
                                border: 1px solid #cccccc;
                            }
                        ''')

        self.last_point_ = None  # 窗口左上角的位置
        self.last_position_ = None  # 窗口上一次的位置
        self._move_drag = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and (event.globalPos() - self.pos()).x() < self.width() and (
                event.globalPos() - self.pos()).y() < 32:
            self._move_drag = True
            self.last_point_ = self.pos()   # 窗口左上角的位置
            self.last_position_ = event.globalPos()

    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton) and self._move_drag:
            point_offset = event.globalPos() - self.last_position_
            self.move(point_offset + self.last_point_)

    def mouseReleaseEvent(self, event):
        self._move_drag = False