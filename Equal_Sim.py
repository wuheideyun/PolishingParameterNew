# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Equal_Sim.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(940, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_num = QLabel(self.centralwidget)
        self.label_num.setObjectName(u"label_num")

        self.gridLayout.addWidget(self.label_num, 2, 3, 1, 1)

        self.lineEdit_num = QLineEdit(self.centralwidget)
        self.lineEdit_num.setObjectName(u"lineEdit_num")

        self.gridLayout.addWidget(self.lineEdit_num, 2, 4, 1, 1)

        self.label_grind_size = QLabel(self.centralwidget)
        self.label_grind_size.setObjectName(u"label_grind_size")

        self.gridLayout.addWidget(self.label_grind_size, 1, 3, 1, 1)

        self.lineEdit_coefficient = QLineEdit(self.centralwidget)
        self.lineEdit_coefficient.setObjectName(u"lineEdit_coefficient")
        self.lineEdit_coefficient.setEnabled(True)

        self.gridLayout.addWidget(self.lineEdit_coefficient, 4, 6, 1, 1)

        self.label_radius = QLabel(self.centralwidget)
        self.label_radius.setObjectName(u"label_radius")

        self.gridLayout.addWidget(self.label_radius, 1, 5, 1, 1)

        self.lineEdit_beam_swing_speed = QLineEdit(self.centralwidget)
        self.lineEdit_beam_swing_speed.setObjectName(u"lineEdit_beam_swing_speed")

        self.gridLayout.addWidget(self.lineEdit_beam_swing_speed, 4, 1, 1, 2)

        self.button_middle_line_equal = QPushButton(self.centralwidget)
        self.button_middle_line_equal.setObjectName(u"button_middle_line_equal")

        self.gridLayout.addWidget(self.button_middle_line_equal, 6, 3, 1, 1)

        self.label_top = QLabel(self.centralwidget)
        self.label_top.setObjectName(u"label_top")
        self.label_top.setMinimumSize(QSize(500, 0))
        self.label_top.setMaximumSize(QSize(16777215, 50))

        self.gridLayout.addWidget(self.label_top, 0, 0, 1, 7)

        self.label_middle = QLabel(self.centralwidget)
        self.label_middle.setObjectName(u"label_middle")
        self.label_middle.setMinimumSize(QSize(500, 0))
        self.label_middle.setMaximumSize(QSize(16777215, 25))

        self.gridLayout.addWidget(self.label_middle, 5, 0, 1, 7)

        self.label_beam_constant_time = QLabel(self.centralwidget)
        self.label_beam_constant_time.setObjectName(u"label_beam_constant_time")

        self.gridLayout.addWidget(self.label_beam_constant_time, 4, 3, 1, 1)

        self.lineEdit_beam_constant_time = QLineEdit(self.centralwidget)
        self.lineEdit_beam_constant_time.setObjectName(u"lineEdit_beam_constant_time")

        self.gridLayout.addWidget(self.lineEdit_beam_constant_time, 4, 4, 1, 1)

        self.lineEdit_grind_size = QLineEdit(self.centralwidget)
        self.lineEdit_grind_size.setObjectName(u"lineEdit_grind_size")

        self.gridLayout.addWidget(self.lineEdit_grind_size, 1, 4, 1, 1)

        self.label_stay_time = QLabel(self.centralwidget)
        self.label_stay_time.setObjectName(u"label_stay_time")

        self.gridLayout.addWidget(self.label_stay_time, 3, 3, 1, 1)

        self.lineEdit_belt_speed = QLineEdit(self.centralwidget)
        self.lineEdit_belt_speed.setObjectName(u"lineEdit_belt_speed")

        self.gridLayout.addWidget(self.lineEdit_belt_speed, 3, 1, 1, 2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"background-color: rgb(244, 244, 244);")

        self.gridLayout.addWidget(self.widget, 7, 0, 1, 7)

        self.label_belt_speed = QLabel(self.centralwidget)
        self.label_belt_speed.setObjectName(u"label_belt_speed")

        self.gridLayout.addWidget(self.label_belt_speed, 3, 0, 1, 1)

        self.label_beam_swing_speed = QLabel(self.centralwidget)
        self.label_beam_swing_speed.setObjectName(u"label_beam_swing_speed")

        self.gridLayout.addWidget(self.label_beam_swing_speed, 4, 0, 1, 1)

        self.lineEdit_stay_time = QLineEdit(self.centralwidget)
        self.lineEdit_stay_time.setObjectName(u"lineEdit_stay_time")

        self.gridLayout.addWidget(self.lineEdit_stay_time, 3, 4, 1, 1)

        self.lineEdit_accelerate = QLineEdit(self.centralwidget)
        self.lineEdit_accelerate.setObjectName(u"lineEdit_accelerate")

        self.gridLayout.addWidget(self.lineEdit_accelerate, 2, 1, 1, 2)

        self.button_animation_equal = QPushButton(self.centralwidget)
        self.button_animation_equal.setObjectName(u"button_animation_equal")

        self.gridLayout.addWidget(self.button_animation_equal, 6, 2, 1, 1)

        self.button_simulation_equal = QPushButton(self.centralwidget)
        self.button_simulation_equal.setObjectName(u"button_simulation_equal")

        self.gridLayout.addWidget(self.button_simulation_equal, 6, 4, 1, 1)

        self.label_accelerate = QLabel(self.centralwidget)
        self.label_accelerate.setObjectName(u"label_accelerate")

        self.gridLayout.addWidget(self.label_accelerate, 2, 0, 1, 1)

        self.label_between = QLabel(self.centralwidget)
        self.label_between.setObjectName(u"label_between")

        self.gridLayout.addWidget(self.label_between, 1, 0, 1, 1)

        self.lineEdit_radius = QLineEdit(self.centralwidget)
        self.lineEdit_radius.setObjectName(u"lineEdit_radius")

        self.gridLayout.addWidget(self.lineEdit_radius, 1, 6, 1, 1)

        self.label_coefficient = QLabel(self.centralwidget)
        self.label_coefficient.setObjectName(u"label_coefficient")

        self.gridLayout.addWidget(self.label_coefficient, 4, 5, 1, 1)

        self.label_bottom = QLabel(self.centralwidget)
        self.label_bottom.setObjectName(u"label_bottom")
        self.label_bottom.setMinimumSize(QSize(500, 0))
        self.label_bottom.setMaximumSize(QSize(16777215, 40))

        self.gridLayout.addWidget(self.label_bottom, 8, 0, 1, 7)

        self.lineEdit_between = QLineEdit(self.centralwidget)
        self.lineEdit_between.setObjectName(u"lineEdit_between")

        self.gridLayout.addWidget(self.lineEdit_between, 1, 1, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 940, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_num.setText(QCoreApplication.translate("MainWindow", u"\u540c\u7c92\u5ea6\u78e8\u5934\u6570\u76ee\uff1a", None))
        self.lineEdit_num.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.label_grind_size.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u78e8\u5757\u5c3a\u5bf8\uff1a</p></body></html>", None))
        self.lineEdit_coefficient.setText("")
        self.label_radius.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u78e8\u5934\u534a\u5f84\uff1a</p></body></html>", None))
        self.lineEdit_beam_swing_speed.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.button_middle_line_equal.setText(QCoreApplication.translate("MainWindow", u"\u540c\u6b65\u6446\u8f68\u8ff9\u4e2d\u5fc3\u7ebf\u7ed8\u5236", None))
        self.label_top.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_middle.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_beam_constant_time.setText(QCoreApplication.translate("MainWindow", u"\u6a2a\u6881\u5300\u901f\u6446\u52a8\u65f6\u95f4\uff1a", None))
        self.lineEdit_beam_constant_time.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.lineEdit_grind_size.setText(QCoreApplication.translate("MainWindow", u"170", None))
        self.label_stay_time.setText(QCoreApplication.translate("MainWindow", u"\u8fb9\u90e8\u505c\u7559\u65f6\u95f4\uff1a", None))
        self.lineEdit_belt_speed.setText(QCoreApplication.translate("MainWindow", u"300", None))
        self.label_belt_speed.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u76ae\u5e26\u901f\u5ea6\uff1a</p></body></html>", None))
        self.label_beam_swing_speed.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6a2a\u6881\u6446\u52a8\u901f\u5ea6\uff1a</p></body></html>", None))
        self.lineEdit_stay_time.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.lineEdit_accelerate.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.button_animation_equal.setText(QCoreApplication.translate("MainWindow", u"\u540c\u6b65\u6446\u52a8\u753b", None))
        self.button_simulation_equal.setText(QCoreApplication.translate("MainWindow", u"\u540c\u6b65\u6446\u629b\u78e8\u91cf\u5206\u5e03\u4eff\u771f", None))
        self.label_accelerate.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u52a0\u901f\u5ea6\u5927\u5c0f\uff1a</p></body></html>", None))
        self.label_between.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u78e8\u5934\u95f4\u8ddd\uff1a</p></body></html>", None))
        self.lineEdit_radius.setText(QCoreApplication.translate("MainWindow", u"270", None))
        self.label_coefficient.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u5747\u5300\u7cfb\u6570\uff1a</p></body></html>", None))
        self.label_bottom.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.lineEdit_between.setText(QCoreApplication.translate("MainWindow", u"600", None))
    # retranslateUi

