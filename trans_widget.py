# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'trans_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(732, 499)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBox_src = QComboBox(Form)
        self.comboBox_src.setObjectName(u"comboBox_src")

        self.horizontalLayout.addWidget(self.comboBox_src)

        self.horizontalSpacer = QSpacerItem(85, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.comboBox_target = QComboBox(Form)
        self.comboBox_target.setObjectName(u"comboBox_target")

        self.horizontalLayout.addWidget(self.comboBox_target)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.btnStartTrans = QPushButton(Form)
        self.btnStartTrans.setObjectName(u"btnStartTrans")

        self.horizontalLayout.addWidget(self.btnStartTrans)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.textEdit_src = QTextEdit(Form)
        self.textEdit_src.setObjectName(u"textEdit_src")

        self.horizontalLayout_2.addWidget(self.textEdit_src)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.textEdit_target = QTextEdit(Form)
        self.textEdit_target.setObjectName(u"textEdit_target")

        self.horizontalLayout_2.addWidget(self.textEdit_target)

        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u6e90\u8bed\u79cd", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u76ee\u6807\u8bed\u79cd", None))
        self.btnStartTrans.setText(QCoreApplication.translate("Form", u"PushButton", None))
    # retranslateUi

