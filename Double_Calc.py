# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Double_Calc.ui'
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
    QMainWindow, QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1088, 633)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_between_beam = QLineEdit(self.centralwidget)
        self.lineEdit_between_beam.setObjectName(u"lineEdit_between_beam")

        self.gridLayout.addWidget(self.lineEdit_between_beam, 2, 1, 1, 2)

        self.button_middle_line_order_define = QPushButton(self.centralwidget)
        self.button_middle_line_order_define.setObjectName(u"button_middle_line_order_define")

        self.gridLayout.addWidget(self.button_middle_line_order_define, 6, 8, 1, 1)

        self.button_simulation_order_define = QPushButton(self.centralwidget)
        self.button_simulation_order_define.setObjectName(u"button_simulation_order_define")

        self.gridLayout.addWidget(self.button_simulation_order_define, 6, 10, 1, 1)

        self.label_ceramic_width = QLabel(self.centralwidget)
        self.label_ceramic_width.setObjectName(u"label_ceramic_width")

        self.gridLayout.addWidget(self.label_ceramic_width, 2, 6, 1, 1)

        self.lineEdit_belt_speed = QLineEdit(self.centralwidget)
        self.lineEdit_belt_speed.setObjectName(u"lineEdit_belt_speed")

        self.gridLayout.addWidget(self.lineEdit_belt_speed, 1, 7, 1, 1)

        self.label_stay_time = QLabel(self.centralwidget)
        self.label_stay_time.setObjectName(u"label_stay_time")

        self.gridLayout.addWidget(self.label_stay_time, 14, 0, 1, 2)

        self.label_beam_constant_time = QLabel(self.centralwidget)
        self.label_beam_constant_time.setObjectName(u"label_beam_constant_time")

        self.gridLayout.addWidget(self.label_beam_constant_time, 13, 0, 1, 2)

        self.label_delay_time = QLabel(self.centralwidget)
        self.label_delay_time.setObjectName(u"label_delay_time")

        self.gridLayout.addWidget(self.label_delay_time, 14, 7, 1, 1)

        self.lineEdit_accelerate = QLineEdit(self.centralwidget)
        self.lineEdit_accelerate.setObjectName(u"lineEdit_accelerate")

        self.gridLayout.addWidget(self.lineEdit_accelerate, 1, 10, 1, 1)

        self.lineEdit_beam_constant_time = QLineEdit(self.centralwidget)
        self.lineEdit_beam_constant_time.setObjectName(u"lineEdit_beam_constant_time")

        self.gridLayout.addWidget(self.lineEdit_beam_constant_time, 13, 2, 1, 1)

        self.lineEdit_radius = QLineEdit(self.centralwidget)
        self.lineEdit_radius.setObjectName(u"lineEdit_radius")

        self.gridLayout.addWidget(self.lineEdit_radius, 2, 4, 1, 2)

        self.label_accelerate = QLabel(self.centralwidget)
        self.label_accelerate.setObjectName(u"label_accelerate")

        self.gridLayout.addWidget(self.label_accelerate, 1, 8, 1, 1)

        self.lineEdit_beam_swing_speed = QLineEdit(self.centralwidget)
        self.lineEdit_beam_swing_speed.setObjectName(u"lineEdit_beam_swing_speed")

        self.gridLayout.addWidget(self.lineEdit_beam_swing_speed, 13, 5, 1, 1)

        self.button_middle_line_order = QPushButton(self.centralwidget)
        self.button_middle_line_order.setObjectName(u"button_middle_line_order")

        self.gridLayout.addWidget(self.button_middle_line_order, 6, 3, 1, 1)

        self.label_num = QLabel(self.centralwidget)
        self.label_num.setObjectName(u"label_num")

        self.gridLayout.addWidget(self.label_num, 13, 7, 1, 1)

        self.label_bottom = QLabel(self.centralwidget)
        self.label_bottom.setObjectName(u"label_bottom")
        self.label_bottom.setMinimumSize(QSize(500, 0))
        self.label_bottom.setMaximumSize(QSize(16777215, 40))

        self.gridLayout.addWidget(self.label_bottom, 15, 0, 1, 11)

        self.lineEdit_delay_time = QLineEdit(self.centralwidget)
        self.lineEdit_delay_time.setObjectName(u"lineEdit_delay_time")

        self.gridLayout.addWidget(self.lineEdit_delay_time, 14, 8, 1, 1)

        self.label_middle = QLabel(self.centralwidget)
        self.label_middle.setObjectName(u"label_middle")
        self.label_middle.setMinimumSize(QSize(500, 0))
        self.label_middle.setMaximumSize(QSize(16777215, 25))

        self.gridLayout.addWidget(self.label_middle, 7, 0, 1, 11)

        self.lineEdit_grind_size = QLineEdit(self.centralwidget)
        self.lineEdit_grind_size.setObjectName(u"lineEdit_grind_size")

        self.gridLayout.addWidget(self.lineEdit_grind_size, 1, 4, 1, 2)

        self.label_beam_swing_speed = QLabel(self.centralwidget)
        self.label_beam_swing_speed.setObjectName(u"label_beam_swing_speed")

        self.gridLayout.addWidget(self.label_beam_swing_speed, 13, 3, 1, 2)

        self.lineEdit_ceramic_width = QLineEdit(self.centralwidget)
        self.lineEdit_ceramic_width.setObjectName(u"lineEdit_ceramic_width")

        self.gridLayout.addWidget(self.lineEdit_ceramic_width, 2, 7, 1, 1)

        self.label_grind_size = QLabel(self.centralwidget)
        self.label_grind_size.setObjectName(u"label_grind_size")

        self.gridLayout.addWidget(self.label_grind_size, 1, 3, 1, 1)

        self.label_beam_between = QLabel(self.centralwidget)
        self.label_beam_between.setObjectName(u"label_beam_between")

        self.gridLayout.addWidget(self.label_beam_between, 2, 0, 1, 1)

        self.label_swing = QLabel(self.centralwidget)
        self.label_swing.setObjectName(u"label_swing")

        self.gridLayout.addWidget(self.label_swing, 14, 3, 1, 2)

        self.label_between = QLabel(self.centralwidget)
        self.label_between.setObjectName(u"label_between")

        self.gridLayout.addWidget(self.label_between, 1, 0, 1, 1)

        self.lineEdit_stay_time = QLineEdit(self.centralwidget)
        self.lineEdit_stay_time.setObjectName(u"lineEdit_stay_time")

        self.gridLayout.addWidget(self.lineEdit_stay_time, 14, 2, 1, 1)

        self.lineEdit_num = QLineEdit(self.centralwidget)
        self.lineEdit_num.setObjectName(u"lineEdit_num")

        self.gridLayout.addWidget(self.lineEdit_num, 13, 8, 1, 1)

        self.label_belt_speed = QLabel(self.centralwidget)
        self.label_belt_speed.setObjectName(u"label_belt_speed")

        self.gridLayout.addWidget(self.label_belt_speed, 1, 6, 1, 1)

        self.lineEdit_self_delay_time = QLineEdit(self.centralwidget)
        self.lineEdit_self_delay_time.setObjectName(u"lineEdit_self_delay_time")

        self.gridLayout.addWidget(self.lineEdit_self_delay_time, 14, 10, 1, 1)

        self.lineEdit_between = QLineEdit(self.centralwidget)
        self.lineEdit_between.setObjectName(u"lineEdit_between")

        self.gridLayout.addWidget(self.lineEdit_between, 1, 1, 1, 2)

        self.button_simulation_order = QPushButton(self.centralwidget)
        self.button_simulation_order.setObjectName(u"button_simulation_order")

        self.gridLayout.addWidget(self.button_simulation_order, 6, 2, 1, 1)

        self.label_radius = QLabel(self.centralwidget)
        self.label_radius.setObjectName(u"label_radius")

        self.gridLayout.addWidget(self.label_radius, 2, 3, 1, 1)

        self.lineEdit_swing = QLineEdit(self.centralwidget)
        self.lineEdit_swing.setObjectName(u"lineEdit_swing")

        self.gridLayout.addWidget(self.lineEdit_swing, 14, 5, 1, 1)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"background-color: rgb(244, 244, 244);")

        self.gridLayout.addWidget(self.widget, 10, 0, 1, 11)

        self.label_self_define_num = QLabel(self.centralwidget)
        self.label_self_define_num.setObjectName(u"label_self_define_num")

        self.gridLayout.addWidget(self.label_self_define_num, 3, 6, 1, 1)

        self.lineEdit_self_define_num = QLineEdit(self.centralwidget)
        self.lineEdit_self_define_num.setObjectName(u"lineEdit_self_define_num")

        self.gridLayout.addWidget(self.lineEdit_self_define_num, 3, 7, 1, 1)

        self.label_group_count = QLabel(self.centralwidget)
        self.label_group_count.setObjectName(u"label_group_count")

        self.gridLayout.addWidget(self.label_group_count, 4, 6, 1, 1)

        self.lineEdit_group_count = QLineEdit(self.centralwidget)
        self.lineEdit_group_count.setObjectName(u"lineEdit_group_count")

        self.gridLayout.addWidget(self.lineEdit_group_count, 4, 7, 1, 1)

        self.label_overlap = QLabel(self.centralwidget)
        self.label_overlap.setObjectName(u"label_overlap")

        self.gridLayout.addWidget(self.label_overlap, 2, 8, 1, 1)

        self.lineEdit_overlap = QLineEdit(self.centralwidget)
        self.lineEdit_overlap.setObjectName(u"lineEdit_overlap")

        self.gridLayout.addWidget(self.lineEdit_overlap, 2, 10, 1, 1)

        self.label_beam_speed_up = QLabel(self.centralwidget)
        self.label_beam_speed_up.setObjectName(u"label_beam_speed_up")

        self.gridLayout.addWidget(self.label_beam_speed_up, 3, 0, 1, 1)

        self.lineEdit_beam_speed_up = QLineEdit(self.centralwidget)
        self.lineEdit_beam_speed_up.setObjectName(u"lineEdit_beam_speed_up")

        self.gridLayout.addWidget(self.lineEdit_beam_speed_up, 3, 2, 1, 1)

        self.button_save_parameter = QPushButton(self.centralwidget)
        self.button_save_parameter.setObjectName(u"button_save_parameter")

        self.gridLayout.addWidget(self.button_save_parameter, 4, 0, 1, 1)

        self.button_energy_calculate = QPushButton(self.centralwidget)
        self.button_energy_calculate.setObjectName(u"button_energy_calculate")

        self.gridLayout.addWidget(self.button_energy_calculate, 4, 2, 1, 1)

        self.button_efficient_calculate = QPushButton(self.centralwidget)
        self.button_efficient_calculate.setObjectName(u"button_efficient_calculate")

        self.gridLayout.addWidget(self.button_efficient_calculate, 4, 3, 1, 1)

        self.button_selfdefine_calculate = QPushButton(self.centralwidget)
        self.button_selfdefine_calculate.setObjectName(u"button_selfdefine_calculate")

        self.gridLayout.addWidget(self.button_selfdefine_calculate, 4, 8, 1, 1)

        self.button_animation_order = QPushButton(self.centralwidget)
        self.button_animation_order.setObjectName(u"button_animation_order")

        self.gridLayout.addWidget(self.button_animation_order, 6, 5, 1, 1)

        self.label_coefficient = QLabel(self.centralwidget)
        self.label_coefficient.setObjectName(u"label_coefficient")

        self.gridLayout.addWidget(self.label_coefficient, 3, 8, 1, 1)

        self.lineEdit_coefficient = QLineEdit(self.centralwidget)
        self.lineEdit_coefficient.setObjectName(u"lineEdit_coefficient")

        self.gridLayout.addWidget(self.lineEdit_coefficient, 3, 10, 1, 1)

        self.label_top = QLabel(self.centralwidget)
        self.label_top.setObjectName(u"label_top")
        self.label_top.setMinimumSize(QSize(500, 0))
        self.label_top.setMaximumSize(QSize(16777215, 50))

        self.gridLayout.addWidget(self.label_top, 0, 0, 1, 11)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lineEdit_between_beam.setText(QCoreApplication.translate("MainWindow", u"1906", None))
        self.button_middle_line_order_define.setText(QCoreApplication.translate("MainWindow", u"\u987a\u5e8f\u6446(\u81ea\u5b9a\u4e49)\u4e2d\u5fc3\u7ebf\u7ed8\u5236", None))
        self.button_simulation_order_define.setText(QCoreApplication.translate("MainWindow", u"\u987a\u5e8f\u6446(\u81ea\u5b9a\u4e49)\u6446\u629b\u78e8\u91cf\u5206\u5e03", None))
        self.label_ceramic_width.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u8fdb\u7816\u5bbd\u5ea6\uff1a</p></body></html>", None))
        self.lineEdit_belt_speed.setText(QCoreApplication.translate("MainWindow", u"240.37", None))
        self.label_stay_time.setText(QCoreApplication.translate("MainWindow", u"\u8fb9\u90e8\u505c\u7559\u65f6\u95f4", None))
        self.label_beam_constant_time.setText(QCoreApplication.translate("MainWindow", u"\u6a2a\u6881\u5300\u901f\u6446\u52a8\u65f6\u95f4", None))
        self.label_delay_time.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u5ef6\u65f6\u65f6\u95f4\uff1a</p></body></html>", None))
        self.lineEdit_accelerate.setText(QCoreApplication.translate("MainWindow", u"650", None))
        self.lineEdit_beam_constant_time.setText("")
        self.lineEdit_radius.setText(QCoreApplication.translate("MainWindow", u"260", None))
        self.label_accelerate.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u52a0\u901f\u5ea6\u5927\u5c0f\uff1a</p></body></html>", None))
        self.lineEdit_beam_swing_speed.setText("")
        self.button_middle_line_order.setText(QCoreApplication.translate("MainWindow", u"\u987a\u5e8f\u6446\u8f68\u8ff9\u4e2d\u5fc3\u7ebf\u7ed8\u5236", None))
        self.label_num.setText(QCoreApplication.translate("MainWindow", u"\u540c\u7c92\u5ea6\u78e8\u5934\u6570\u76ee", None))
        self.label_bottom.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.lineEdit_delay_time.setText("")
        self.label_middle.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.lineEdit_grind_size.setText(QCoreApplication.translate("MainWindow", u"150", None))
        self.label_beam_swing_speed.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6a2a\u6881\u6446\u52a8\u901f\u5ea6</p></body></html>", None))
        self.lineEdit_ceramic_width.setText(QCoreApplication.translate("MainWindow", u"1800", None))
        self.label_grind_size.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u78e8\u5757\u5c3a\u5bf8\uff1a</p></body></html>", None))
        self.label_beam_between.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u6a2a\u6881\u95f4\u8ddd\uff1a</p></body></html>", None))
        self.label_swing.setText(QCoreApplication.translate("MainWindow", u"\u6446\u5e45", None))
        self.label_between.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u78e8\u5934\u95f4\u8ddd\uff1a</p></body></html>", None))
        self.lineEdit_stay_time.setText("")
        self.lineEdit_num.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.label_belt_speed.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u76ae\u5e26\u901f\u5ea6\uff1a</p></body></html>", None))
        self.lineEdit_self_delay_time.setText("")
        self.lineEdit_between.setText(QCoreApplication.translate("MainWindow", u"580", None))
        self.button_simulation_order.setText(QCoreApplication.translate("MainWindow", u"\u987a\u5e8f\u6446\u629b\u78e8\u91cf\u5206\u5e03\u4eff\u771f", None))
        self.label_radius.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u78e8\u5934\u534a\u5f84\uff1a</p></body></html>", None))
        self.label_self_define_num.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u5b9a\u5168\u8986\u76d6\u78e8\u5934\u6570\uff1a", None))
        self.label_group_count.setText(QCoreApplication.translate("MainWindow", u"\u7ec4\u6570\uff1a", None))
        self.lineEdit_group_count.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.label_overlap.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u8f68\u8ff9\u91cd\u53e0\u91cf\uff1a</p></body></html>", None))
        self.lineEdit_overlap.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.label_beam_speed_up.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6a2a\u6881\u6446\u52a8\u901f\u5ea6\u4e0a\u9650\uff1a</p></body></html>", None))
        self.lineEdit_beam_speed_up.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.button_save_parameter.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u53c2\u6570", None))
        self.button_energy_calculate.setText(QCoreApplication.translate("MainWindow", u"\u8282\u80fd\u8ba1\u7b97", None))
        self.button_efficient_calculate.setText(QCoreApplication.translate("MainWindow", u"\u9ad8\u6548\u8ba1\u7b97", None))
        self.button_selfdefine_calculate.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u5b9a\u4e49\u8ba1\u7b97", None))
        self.button_animation_order.setText(QCoreApplication.translate("MainWindow", u"\u987a\u5e8f\u6446\u52a8\u753b", None))
        self.label_coefficient.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u5747\u5300\u7cfb\u6570\uff1a</p></body></html>", None))
        self.label_top.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

