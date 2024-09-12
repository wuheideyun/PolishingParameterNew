# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindowNew.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(929, 671)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.leftbar_widget = QWidget(self.centralwidget)
        self.leftbar_widget.setObjectName(u"leftbar_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftbar_widget.sizePolicy().hasHeightForWidth())
        self.leftbar_widget.setSizePolicy(sizePolicy)
        self.leftbar_widget.setMinimumSize(QSize(120, 0))
        self.leftbar_widget.setMaximumSize(QSize(120, 16777215))
        self.leftbar_widget.setStyleSheet(u"background-color:rgb(244,244,244)")

        self.horizontalLayout.addWidget(self.leftbar_widget)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titlebar_widget = QWidget(self.centralwidget)
        self.titlebar_widget.setObjectName(u"titlebar_widget")
        self.titlebar_widget.setMinimumSize(QSize(0, 20))
        self.titlebar_widget.setMaximumSize(QSize(16777215, 20))
        self.titlebar_widget.setStyleSheet(u"background-color:rgb(144,244,244)")

        self.verticalLayout.addWidget(self.titlebar_widget)

        self.content_widget = QWidget(self.centralwidget)
        self.content_widget.setObjectName(u"content_widget")
        self.content_widget.setStyleSheet(u"background-color:rgb(244,144,244)")

        self.verticalLayout.addWidget(self.content_widget)

        self.statusbar_widget = QWidget(self.centralwidget)
        self.statusbar_widget.setObjectName(u"statusbar_widget")
        self.statusbar_widget.setMinimumSize(QSize(0, 20))
        self.statusbar_widget.setMaximumSize(QSize(16777215, 20))
        self.statusbar_widget.setStyleSheet(u"background-color:rgb(244,244,144)")

        self.verticalLayout.addWidget(self.statusbar_widget)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 929, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi

