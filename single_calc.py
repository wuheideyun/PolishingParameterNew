# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'single_calc.ui'
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
        MainWindow.resize(1017, 686)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_beam_between = QLabel(self.centralwidget)
        self.label_beam_between.setObjectName(u"label_beam_between")

        self.gridLayout.addWidget(self.label_beam_between, 0, 0, 1, 1)

        self.lineEdit_beam_between = QLineEdit(self.centralwidget)
        self.lineEdit_beam_between.setObjectName(u"lineEdit_beam_between")

        self.gridLayout.addWidget(self.lineEdit_beam_between, 0, 1, 1, 2)

        self.label_grind_size = QLabel(self.centralwidget)
        self.label_grind_size.setObjectName(u"label_grind_size")

        self.gridLayout.addWidget(self.label_grind_size, 0, 3, 1, 1)

        self.lineEdit_grind_size = QLineEdit(self.centralwidget)
        self.lineEdit_grind_size.setObjectName(u"lineEdit_grind_size")

        self.gridLayout.addWidget(self.lineEdit_grind_size, 0, 4, 1, 2)

        self.label_belt_speed = QLabel(self.centralwidget)
        self.label_belt_speed.setObjectName(u"label_belt_speed")

        self.gridLayout.addWidget(self.label_belt_speed, 0, 7, 1, 1)

        self.lineEdit_belt_speed = QLineEdit(self.centralwidget)
        self.lineEdit_belt_speed.setObjectName(u"lineEdit_belt_speed")

        self.gridLayout.addWidget(self.lineEdit_belt_speed, 0, 8, 1, 2)

        self.label_accelerate = QLabel(self.centralwidget)
        self.label_accelerate.setObjectName(u"label_accelerate")

        self.gridLayout.addWidget(self.label_accelerate, 0, 10, 1, 2)

        self.lineEdit_accelerate = QLineEdit(self.centralwidget)
        self.lineEdit_accelerate.setObjectName(u"lineEdit_accelerate")

        self.gridLayout.addWidget(self.lineEdit_accelerate, 0, 12, 1, 2)

        self.label_num_set = QLabel(self.centralwidget)
        self.label_num_set.setObjectName(u"label_num_set")

        self.gridLayout.addWidget(self.label_num_set, 0, 14, 1, 2)

        self.lineEdit_num_set = QLineEdit(self.centralwidget)
        self.lineEdit_num_set.setObjectName(u"lineEdit_num_set")

        self.gridLayout.addWidget(self.lineEdit_num_set, 0, 16, 1, 1)

        self.label_radius = QLabel(self.centralwidget)
        self.label_radius.setObjectName(u"label_radius")

        self.gridLayout.addWidget(self.label_radius, 1, 0, 1, 1)

        self.lineEdit_radius = QLineEdit(self.centralwidget)
        self.lineEdit_radius.setObjectName(u"lineEdit_radius")

        self.gridLayout.addWidget(self.lineEdit_radius, 1, 1, 1, 2)

        self.label_cerimatic_width = QLabel(self.centralwidget)
        self.label_cerimatic_width.setObjectName(u"label_cerimatic_width")

        self.gridLayout.addWidget(self.label_cerimatic_width, 1, 3, 1, 1)

        self.lineEdit_ceramic_width = QLineEdit(self.centralwidget)
        self.lineEdit_ceramic_width.setObjectName(u"lineEdit_ceramic_width")

        self.gridLayout.addWidget(self.lineEdit_ceramic_width, 1, 4, 1, 2)

        self.label_beam_speed_up = QLabel(self.centralwidget)
        self.label_beam_speed_up.setObjectName(u"label_beam_speed_up")

        self.gridLayout.addWidget(self.label_beam_speed_up, 1, 6, 1, 2)

        self.lineEdit_beam_speed_up = QLineEdit(self.centralwidget)
        self.lineEdit_beam_speed_up.setObjectName(u"lineEdit_beam_speed_up")

        self.gridLayout.addWidget(self.lineEdit_beam_speed_up, 1, 8, 1, 2)

        self.label_overlap = QLabel(self.centralwidget)
        self.label_overlap.setObjectName(u"label_overlap")

        self.gridLayout.addWidget(self.label_overlap, 1, 10, 1, 2)

        self.lineEdit_overlap = QLineEdit(self.centralwidget)
        self.lineEdit_overlap.setObjectName(u"lineEdit_overlap")

        self.gridLayout.addWidget(self.lineEdit_overlap, 1, 12, 1, 2)

        self.label_group_count = QLabel(self.centralwidget)
        self.label_group_count.setObjectName(u"label_group_count")

        self.gridLayout.addWidget(self.label_group_count, 1, 14, 1, 1)

        self.lineEdit_group_count = QLineEdit(self.centralwidget)
        self.lineEdit_group_count.setObjectName(u"lineEdit_group_count")

        self.gridLayout.addWidget(self.lineEdit_group_count, 1, 16, 1, 1)

        self.button_energy_calculate = QPushButton(self.centralwidget)
        self.button_energy_calculate.setObjectName(u"button_energy_calculate")

        self.gridLayout.addWidget(self.button_energy_calculate, 2, 0, 1, 2)

        self.button_animation_order = QPushButton(self.centralwidget)
        self.button_animation_order.setObjectName(u"button_animation_order")

        self.gridLayout.addWidget(self.button_animation_order, 2, 5, 1, 4)

        self.button_middle_line_order = QPushButton(self.centralwidget)
        self.button_middle_line_order.setObjectName(u"button_middle_line_order")

        self.gridLayout.addWidget(self.button_middle_line_order, 2, 13, 1, 2)

        self.label_tips = QLabel(self.centralwidget)
        self.label_tips.setObjectName(u"label_tips")

        self.gridLayout.addWidget(self.label_tips, 2, 15, 1, 2)

        self.button_animation_order_define = QPushButton(self.centralwidget)
        self.button_animation_order_define.setObjectName(u"button_animation_order_define")

        self.gridLayout.addWidget(self.button_animation_order_define, 3, 5, 1, 4)

        self.button_simulation_order_define = QPushButton(self.centralwidget)
        self.button_simulation_order_define.setObjectName(u"button_simulation_order_define")

        self.gridLayout.addWidget(self.button_simulation_order_define, 3, 9, 1, 4)

        self.button_middle_line_order_define = QPushButton(self.centralwidget)
        self.button_middle_line_order_define.setObjectName(u"button_middle_line_order_define")

        self.gridLayout.addWidget(self.button_middle_line_order_define, 3, 13, 1, 2)

        self.label_beam_constant_time = QLabel(self.centralwidget)
        self.label_beam_constant_time.setObjectName(u"label_beam_constant_time")

        self.gridLayout.addWidget(self.label_beam_constant_time, 4, 0, 1, 2)

        self.lineEdit_beam_constant_time = QLineEdit(self.centralwidget)
        self.lineEdit_beam_constant_time.setObjectName(u"lineEdit_beam_constant_time")

        self.gridLayout.addWidget(self.lineEdit_beam_constant_time, 4, 2, 1, 3)

        self.label_beam_swing_speed = QLabel(self.centralwidget)
        self.label_beam_swing_speed.setObjectName(u"label_beam_swing_speed")

        self.gridLayout.addWidget(self.label_beam_swing_speed, 4, 5, 1, 2)

        self.lineEdit_beam_swing_speed = QLineEdit(self.centralwidget)
        self.lineEdit_beam_swing_speed.setObjectName(u"lineEdit_beam_swing_speed")

        self.gridLayout.addWidget(self.lineEdit_beam_swing_speed, 4, 7, 1, 2)

        self.label_num = QLabel(self.centralwidget)
        self.label_num.setObjectName(u"label_num")

        self.gridLayout.addWidget(self.label_num, 4, 10, 1, 1)

        self.lineEdit_num = QLineEdit(self.centralwidget)
        self.lineEdit_num.setObjectName(u"lineEdit_num")

        self.gridLayout.addWidget(self.lineEdit_num, 4, 11, 1, 3)

        self.label_between = QLabel(self.centralwidget)
        self.label_between.setObjectName(u"label_between")

        self.gridLayout.addWidget(self.label_between, 4, 14, 1, 1)

        self.lineEdit_between = QLineEdit(self.centralwidget)
        self.lineEdit_between.setObjectName(u"lineEdit_between")

        self.gridLayout.addWidget(self.lineEdit_between, 4, 15, 1, 2)

        self.label_stay_time = QLabel(self.centralwidget)
        self.label_stay_time.setObjectName(u"label_stay_time")

        self.gridLayout.addWidget(self.label_stay_time, 5, 0, 1, 2)

        self.lineEdit_stay_time = QLineEdit(self.centralwidget)
        self.lineEdit_stay_time.setObjectName(u"lineEdit_stay_time")

        self.gridLayout.addWidget(self.lineEdit_stay_time, 5, 2, 1, 3)

        self.label_swing = QLabel(self.centralwidget)
        self.label_swing.setObjectName(u"label_swing")

        self.gridLayout.addWidget(self.label_swing, 5, 5, 1, 2)

        self.lineEdit_swing = QLineEdit(self.centralwidget)
        self.lineEdit_swing.setObjectName(u"lineEdit_swing")

        self.gridLayout.addWidget(self.lineEdit_swing, 5, 7, 1, 2)

        self.label_delay_time = QLabel(self.centralwidget)
        self.label_delay_time.setObjectName(u"label_delay_time")

        self.gridLayout.addWidget(self.label_delay_time, 5, 10, 1, 1)

        self.lineEdit_delay_time = QLineEdit(self.centralwidget)
        self.lineEdit_delay_time.setObjectName(u"lineEdit_delay_time")

        self.gridLayout.addWidget(self.lineEdit_delay_time, 5, 11, 1, 3)

        self.label_coefficient = QLabel(self.centralwidget)
        self.label_coefficient.setObjectName(u"label_coefficient")

        self.gridLayout.addWidget(self.label_coefficient, 5, 14, 1, 1)

        self.lineEdit_coefficient = QLineEdit(self.centralwidget)
        self.lineEdit_coefficient.setObjectName(u"lineEdit_coefficient")

        self.gridLayout.addWidget(self.lineEdit_coefficient, 5, 15, 1, 2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"background-color: rgb(0, 170, 255);")

        self.gridLayout.addWidget(self.widget, 6, 0, 1, 17)

        self.button_simulation_order = QPushButton(self.centralwidget)
        self.button_simulation_order.setObjectName(u"button_simulation_order")

        self.gridLayout.addWidget(self.button_simulation_order, 2, 9, 1, 4)

        self.button_selfdefine_calculate = QPushButton(self.centralwidget)
        self.button_selfdefine_calculate.setObjectName(u"button_selfdefine_calculate")

        self.gridLayout.addWidget(self.button_selfdefine_calculate, 3, 0, 1, 2)

        self.button_efficient_calculate = QPushButton(self.centralwidget)
        self.button_efficient_calculate.setObjectName(u"button_efficient_calculate")

        self.gridLayout.addWidget(self.button_efficient_calculate, 2, 2, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1017, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_beam_between.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u6a2a\u6881\u95f4\u8ddd\uff1a</p></body></html>", None))
        self.lineEdit_beam_between.setText(QCoreApplication.translate("MainWindow", u"800", None))
        self.label_grind_size.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u78e8\u5757\u5c3a\u5bf8\uff1a</p></body></html>", None))
        self.lineEdit_grind_size.setText(QCoreApplication.translate("MainWindow", u"150", None))
        self.label_belt_speed.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u76ae\u5e26\u901f\u5ea6\uff1a</p></body></html>", None))
        self.lineEdit_belt_speed.setText(QCoreApplication.translate("MainWindow", u"240.37", None))
        self.label_accelerate.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u52a0\u901f\u5ea6\u5927\u5c0f\uff1a</p></body></html>", None))
        self.lineEdit_accelerate.setText(QCoreApplication.translate("MainWindow", u"650", None))
        self.label_num_set.setText(QCoreApplication.translate("MainWindow", u"\u5355\u7ec4\u78e8\u5934\u6570\u8bbe\u5b9a", None))
        self.lineEdit_num_set.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.label_radius.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u78e8\u5934\u534a\u5f84\uff1a</p></body></html>", None))
        self.lineEdit_radius.setText(QCoreApplication.translate("MainWindow", u"260", None))
        self.label_cerimatic_width.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u8fdb\u7816\u5bbd\u5ea6\uff1a</p></body></html>", None))
        self.lineEdit_ceramic_width.setText(QCoreApplication.translate("MainWindow", u"1800", None))
        self.label_beam_speed_up.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u6a2a\u6881\u6446\u52a8\u901f\u5ea6\u4e0a\u9650\uff1a</p></body></html>", None))
        self.lineEdit_beam_speed_up.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.label_overlap.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u8f68\u8ff9\u91cd\u53e0\u91cf\uff1a</p></body></html>", None))
        self.lineEdit_overlap.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.label_group_count.setText(QCoreApplication.translate("MainWindow", u"\u7ec4\u6570\uff1a", None))
        self.lineEdit_group_count.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.button_energy_calculate.setText(QCoreApplication.translate("MainWindow", u"\u8282\u80fd\u8ba1\u7b97", None))
        self.button_animation_order.setText(QCoreApplication.translate("MainWindow", u"\u987a\u5e8f\u6446\u52a8\u753b", None))
        self.button_middle_line_order.setText(QCoreApplication.translate("MainWindow", u"\u987a\u5e8f\u6446\u8f68\u8ff9\u4e2d\u5fc3\u7ebf\u7ed8\u5236", None))
        self.label_tips.setText(QCoreApplication.translate("MainWindow", u"\u6b64\u9879\u4ec5\u5728\u81ea\u5b9a\u4e49\u8ba1\u7b97\u6a21\u5f0f\u4f7f\u7528", None))
        self.button_animation_order_define.setText(QCoreApplication.translate("MainWindow", u"\u987a\u5e8f\u6446\u52a8\u753b\uff08\u81ea\u5b9a\u4e49\u6a21\u5f0f\uff09", None))
        self.button_simulation_order_define.setText(QCoreApplication.translate("MainWindow", u"\u987a\u5e8f\u6446(\u81ea\u5b9a\u4e49)\u6446\u629b\u78e8\u91cf\u5206\u5e03", None))
        self.button_middle_line_order_define.setText(QCoreApplication.translate("MainWindow", u"\u987a\u5e8f\u6446(\u81ea\u5b9a\u4e49)\u4e2d\u5fc3\u7ebf\u7ed8\u5236", None))
        self.label_beam_constant_time.setText(QCoreApplication.translate("MainWindow", u"\u6a2a\u6881\u5300\u901f\u6446\u52a8\u65f6\u95f4", None))
        self.lineEdit_beam_constant_time.setText("")
        self.label_beam_swing_speed.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6a2a\u6881\u6446\u52a8\u901f\u5ea6</p></body></html>", None))
        self.lineEdit_beam_swing_speed.setText("")
        self.label_num.setText(QCoreApplication.translate("MainWindow", u"\u540c\u7c92\u5ea6\u78e8\u5934\u6570\u76ee", None))
        self.lineEdit_num.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.label_between.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u78e8\u5934\u95f4\u8ddd\uff1a</p></body></html>", None))
        self.lineEdit_between.setText("")
        self.label_stay_time.setText(QCoreApplication.translate("MainWindow", u"\u8fb9\u90e8\u505c\u7559\u65f6\u95f4", None))
        self.lineEdit_stay_time.setText("")
        self.label_swing.setText(QCoreApplication.translate("MainWindow", u"\u6446\u5e45", None))
        self.label_delay_time.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u5ef6\u65f6\u65f6\u95f4\uff1a</p></body></html>", None))
        self.lineEdit_delay_time.setText("")
        self.label_coefficient.setText(QCoreApplication.translate("MainWindow", u"\u5747\u5300\u7cfb\u6570", None))
        self.button_simulation_order.setText(QCoreApplication.translate("MainWindow", u"\u987a\u5e8f\u6446\u629b\u78e8\u91cf\u5206\u5e03\u4eff\u771f", None))
        self.button_selfdefine_calculate.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u5b9a\u4e49\u8ba1\u7b97", None))
        self.button_efficient_calculate.setText(QCoreApplication.translate("MainWindow", u"\u9ad8\u6548\u8ba1\u7b97", None))
    # retranslateUi

