import sys

from PyQt5.QtCore import pyqtSignal
from PySide6 import QtWidgets
from PySide6.QtCore import QRect, Signal
from PySide6.QtGui import QPen, QColor, QBrush, Qt, QFont, QPainter
from PySide6.QtWidgets import QWidget, QApplication


class SwitchButton(QWidget):
    sig_language_switch = Signal(bool)

    def __init__(self, ):
        super(SwitchButton, self).__init__()
        self.setFixedSize(100,40)

        # 开关状态，默认关闭
        self.state = True

    def mousePressEvent(self, event):
        super(SwitchButton, self).mousePressEvent(event)

        self.state = False if self.state else True
        self.update()
        self.sig_language_switch.emit(self.state)

    def paintEvent(self, event):
        super(SwitchButton, self).paintEvent(event)

        # 创建绘制器并设置抗锯齿和图片流畅转换
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        # 定义字体样式
        font = QFont('SimHei')
        font.setPixelSize(15)
        painter.setFont(font)

        # 开关为开的状态
        if self.state:

            ##todo 绘制外框方形
            painter.setPen(Qt.NoPen)
            brush_color = QColor('#1da4e7')
            painter.setBrush(QBrush(brush_color))
            corner_radius = 10
            painter.drawRoundedRect(0, 0, self.width(), self.height(), corner_radius, corner_radius)  # 设置矩形圆角

            # todo 绘制内框方形
            slider_size = self.height() - 6
            slider_position = self.width() - slider_size - 3
            painter.setBrush(QBrush(QColor('#ffffff')))
            painter.drawRoundedRect(slider_position + 3, 9, slider_size - 10, slider_size - 10,
                                    corner_radius - 5, corner_radius - 5)
            # 绘制文本
            painter.setPen(QPen(QColor('#ffffff')))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QRect(10, 13, 60, 30), Qt.AlignHCenter, '中文')
        # 开关为关的状态
        else:

            ##todo 绘制外框方形
            painter.setPen(Qt.NoPen)
            # brush_color = QColor('#fa6a07')
            brush_color = QColor('#c8c8c8')
            painter.setBrush(QBrush(brush_color))
            corner_radius = 10  # Adjust the radius as needed
            painter.drawRoundedRect(0, 0, self.width(), self.height(), corner_radius, corner_radius)

            # todo 绘制内框方形
            slider_size = self.height() - 6
            slider_position = 3
            painter.setBrush(QBrush(QColor('#747474')))
            painter.drawRoundedRect(slider_position + 5, 9, slider_size - 10, slider_size - 10,
                                    corner_radius - 5, corner_radius - 5)
            # 绘制文本
            painter.setPen(QPen(QColor('#000000')))
            painter.setBrush(Qt.NoBrush)

            painter.drawText(QRect(35, 13, 60, 30), Qt.AlignHCenter, 'English')



