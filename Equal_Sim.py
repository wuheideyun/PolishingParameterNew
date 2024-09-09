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
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.between = QLineEdit(self.centralwidget)
        self.between.setObjectName(u"between")

        self.gridLayout.addWidget(self.between, 0, 2, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 3, 1, 1)

        self.grind_size = QLineEdit(self.centralwidget)
        self.grind_size.setObjectName(u"grind_size")

        self.gridLayout.addWidget(self.grind_size, 0, 4, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 5, 1, 1)

        self.radius = QLineEdit(self.centralwidget)
        self.radius.setObjectName(u"radius")

        self.gridLayout.addWidget(self.radius, 0, 6, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.a_speed = QLineEdit(self.centralwidget)
        self.a_speed.setObjectName(u"a_speed")

        self.gridLayout.addWidget(self.a_speed, 1, 1, 1, 2)

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 1, 3, 1, 1)

        self.num = QLineEdit(self.centralwidget)
        self.num.setObjectName(u"num")

        self.gridLayout.addWidget(self.num, 1, 4, 1, 1)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)

        self.belt_speed = QLineEdit(self.centralwidget)
        self.belt_speed.setObjectName(u"belt_speed")

        self.gridLayout.addWidget(self.belt_speed, 2, 1, 1, 2)

        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 2, 3, 1, 1)

        self.stay_time = QLineEdit(self.centralwidget)
        self.stay_time.setObjectName(u"stay_time")

        self.gridLayout.addWidget(self.stay_time, 2, 4, 1, 1)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)

        self.beam_speed = QLineEdit(self.centralwidget)
        self.beam_speed.setObjectName(u"beam_speed")

        self.gridLayout.addWidget(self.beam_speed, 3, 1, 1, 2)

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 3, 3, 1, 1)

        self.constant_time = QLineEdit(self.centralwidget)
        self.constant_time.setObjectName(u"constant_time")

        self.gridLayout.addWidget(self.constant_time, 3, 4, 1, 1)

        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 3, 5, 1, 1)

        self.equal_coefficient = QLineEdit(self.centralwidget)
        self.equal_coefficient.setObjectName(u"equal_coefficient")
        self.equal_coefficient.setEnabled(True)

        self.gridLayout.addWidget(self.equal_coefficient, 3, 6, 1, 1)

        self.animation_button = QPushButton(self.centralwidget)
        self.animation_button.setObjectName(u"animation_button")

        self.gridLayout.addWidget(self.animation_button, 4, 2, 1, 1)

        self.middle_line_button = QPushButton(self.centralwidget)
        self.middle_line_button.setObjectName(u"middle_line_button")

        self.gridLayout.addWidget(self.middle_line_button, 4, 3, 1, 1)

        self.simulation_button = QPushButton(self.centralwidget)
        self.simulation_button.setObjectName(u"simulation_button")

        self.gridLayout.addWidget(self.simulation_button, 4, 4, 1, 1)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"background-color: rgb(0, 170, 255);")

        self.gridLayout.addWidget(self.widget, 5, 0, 1, 7)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 940, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u78e8\u5934\u95f4\u8ddd\uff1a</p></body></html>", None))
        self.between.setText(QCoreApplication.translate("MainWindow", u"600", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u78e8\u5757\u5c3a\u5bf8\uff1a</p></body></html>", None))
        self.grind_size.setText(QCoreApplication.translate("MainWindow", u"170", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u78e8\u5934\u534a\u5f84\uff1a</p></body></html>", None))
        self.radius.setText(QCoreApplication.translate("MainWindow", u"270", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u52a0\u901f\u5ea6\u5927\u5c0f\uff1a</p></body></html>", None))
        self.a_speed.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u540c\u7c92\u5ea6\u78e8\u5934\u6570\u76ee", None))
        self.num.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u76ae\u5e26\u901f\u5ea6\uff1a</p></body></html>", None))
        self.belt_speed.setText(QCoreApplication.translate("MainWindow", u"300", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u8fb9\u90e8\u505c\u7559\u65f6\u95f4", None))
        self.stay_time.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6a2a\u6881\u6446\u52a8\u901f\u5ea6</p></body></html>", None))
        self.beam_speed.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u6a2a\u6881\u5300\u901f\u6446\u52a8\u65f6\u95f4", None))
        self.constant_time.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u5747\u5300\u7cfb\u6570\uff1a</p></body></html>", None))
        self.equal_coefficient.setText("")
        self.animation_button.setText(QCoreApplication.translate("MainWindow", u"\u52a8\u753b\u6309\u94ae", None))
        self.middle_line_button.setText(QCoreApplication.translate("MainWindow", u"\u8f68\u8ff9\u4e2d\u5fc3\u7ebf\u7ed8\u5236", None))
        self.simulation_button.setText(QCoreApplication.translate("MainWindow", u"\u629b\u78e8\u91cf\u5206\u5e03\u4eff\u771f", None))
    # retranslateUi

