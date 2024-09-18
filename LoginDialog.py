'''

登录窗口

'''
import sqlite3

from PySide6.QtCore import Qt, Signal, QSettings
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QGridLayout, \
    QSpacerItem, QSizePolicy, QMessageBox

from DatabaseHelper import DatabaseHelper
from FrameLessDialog import FrameLessDialog
from ImageButton import ImageButton
from LoginEdit import LoginEdit
from PopupMessageBox import PopupMessageBox


class LoginDialog(FrameLessDialog):
    sig_login_success = Signal()
    sig_login_administrator_success = Signal()
    sig_login_failure = Signal()
    def __init__(self):
        super().__init__()
        self.db = DatabaseHelper('database.db')
        self.setWindowTitle("登录")
        self.setFixedSize(1100, 450)

        self.settings = QSettings("config.ini", QSettings.IniFormat)  # 使用配置文件



        self.setWindowFlag(Qt.FramelessWindowHint)
        self.saved_username = ""
        outHLay = QHBoxLayout()
        outHLay.setContentsMargins(0, 0, 20, 0)
        kedaLabel = QLabel()
        keda_pixmap = QPixmap(":keda")  # 替换为实际图片路径
        kedaLabel.setScaledContents(True)
        kedaLabel.setPixmap(keda_pixmap)
        outHLay.addWidget(kedaLabel)

        mainVLay = QVBoxLayout()

        hlay1 = QHBoxLayout()

        self.btnClose = ImageButton(":close16", 16, 16)
        self.btnClose.clicked.connect(self.btn_close)

        hlay1.addStretch()
        hlay1.addWidget(self.btnClose)
        hlay1.setContentsMargins(0, 0, 0, 0)
        mainVLay.addLayout(hlay1)
        # self.btnClose.move(500, 10)

        mainVLay.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed))

        logoLabel = QLabel("")
        logoLabel.setFixedSize(302, 48)

        pixmap = QPixmap(":login_logo2")  # 替换为实际图片路径
        logoLabel.setPixmap(pixmap)

        # 如果需要，可以让图片自适应 QLabel 的大小
        logoLabel.setScaledContents(True)

        hlay2 = QHBoxLayout()
        hlay2.addWidget(logoLabel)
        hlay2.setContentsMargins(0, 0, 0, 0)
        mainVLay.addLayout(hlay2)

        textLabel = QLabel("欢迎登录")
        textLabel.setAlignment(Qt.AlignCenter)  # 将文本居中对齐
        textLabel.setFixedSize(100, 30)  # 不设置大小，在水平布局时不会自动居中
        textLabel.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #000000;
            }
        """)

        hlay3 = QHBoxLayout()
        hlay3.addWidget(textLabel)
        mainVLay.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed))
        mainVLay.addLayout(hlay3)
        mainVLay.setContentsMargins(0, 0, 0, 0)
        mainVLay.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed))
        gridLayout = QGridLayout()

        self.userNameEdit = LoginEdit(":login_user")
        self.userNameEdit.setPlaceholderText("用户名/手机号/邮箱")

        gridLayout.addWidget(self.userNameEdit, 0, 0, 1, 2)  # 第0行，第0列，占1行，占2列

        self.passwordEdit = LoginEdit(":login_pwd")
        self.passwordEdit.setPlaceholderText("密码")
        self.passwordEdit.setEchoMode(LoginEdit.Password)

        gridLayout.addWidget(self.passwordEdit, 1, 0, 1, 2)  # 第1行，第0列，占1行，占2列

        # self.checkBoxAutoLogin = QCheckBox("自动登录")
        # self.checkBoxAutoLogin.setFixedSize(80, 18)
        #
        # gridLayout.addWidget(self.checkBoxAutoLogin, 2, 0)

        self.checkBoxRemember = QCheckBox("记住账号")
        self.checkBoxRemember.setFixedSize(80, 18)

        gridLayout.addWidget(self.checkBoxRemember, 2, 1, alignment=Qt.AlignRight)

        hlay4 = QHBoxLayout()
        hlay4.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hlay4.addLayout(gridLayout)
        hlay4.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        mainVLay.addLayout(hlay4)

        mainVLay.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed))

        hlay5 = QHBoxLayout()
        self.btnLogin = QPushButton("登 录")
        self.btnLogin.setFixedSize(328, 48)

        self.btnLogin.clicked.connect(self.OnLogin)

        self.btnLogin.setStyleSheet("""
                   QPushButton {
                       background-color: #30438c; /* 按钮的默认背景色为绿色 */
                       color: white; /* 设置按钮文字颜色为白色 */
                       border: none; /* 移除边框 */
                       padding: 10px; /* 内边距 */
                       font-size: 18px; /* 文字大小 */
                   }
                   QPushButton:hover {
                       background-color: #40539c; /* 鼠标悬停时按钮的背景色变深 */
                   }
                   QPushButton:pressed {
                       background-color: #7986b5; /* 鼠标按下时按钮的背景色更深 */
                   }
               """)

        hlay5.addWidget(self.btnLogin)
        mainVLay.addLayout(hlay5)

        # self.btnPhoneLogin = QPushButton("手机号验证码登录")
        # self.btnPhoneLogin.setFixedSize(328, 48)
        # self.btnPhoneLogin.setStyleSheet("""
        #                font-size: 18px; /* 文字大小 */
        #             """)
        #
        # hlay6 = QHBoxLayout()
        # hlay6.addWidget(self.btnPhoneLogin)
        # mainVLay.addLayout(hlay6)

        mainVLay.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # hlay7 = QHBoxLayout()
        # otherLabel = QLabel("其它登录方式")
        # otherLabel.setAlignment(Qt.AlignCenter)  # 将文本居中对齐
        # otherLabel.setFixedSize(200, 24)
        #
        # hlay7.addWidget(otherLabel)
        # mainVLay.addLayout(hlay7)

        # self.btnWeiChatLogin = QPushButton("")
        # self.btnWeiChatLogin.setFixedSize(48, 48)
        # self.btnWeiChatLogin.setStyleSheet("""
        #     QPushButton {
        #         border: none;
        #         background-image: url(:weichat);
        #         background-position: center center;
        #         background-repeat: no-repeat;
        #         background-size: cover; /* 或者使用 contain */
        #     }
        # """)
        #
        # self.btnWeiboLogin = QPushButton("")
        # self.btnWeiboLogin.setFixedSize(48, 48)
        # self.btnWeiboLogin.setStyleSheet("""
        #     QPushButton {
        #         border: none;
        #         background-image: url(:weibo);
        #         background-position: center center;
        #         background-repeat: no-repeat;
        #         background-size: cover; /* 或者使用 contain */
        #     }
        # """)
        #
        # self.btnQQLogin = QPushButton("")
        # self.btnQQLogin.setFixedSize(48, 48)
        # self.btnQQLogin.setStyleSheet("""
        #     QPushButton {
        #         border: none;
        #         background-image: url(:QQ);
        #         background-position: center center;
        #         background-repeat: no-repeat;
        #         background-size: cover; /* 或者使用 contain */
        #     }
        # """)

        # hlay8 = QHBoxLayout()
        # hlay8.addWidget(self.btnWeiChatLogin)
        # hlay8.addWidget(self.btnWeiboLogin)
        # hlay8.addWidget(self.btnQQLogin)
        #
        # mainVLay.addLayout(hlay8)
        mainVLay.setContentsMargins(0, 0, 0, 0)
        outHLay.addLayout(mainVLay)

        self.setLayout(outHLay)
        self.checkBoxRemember.checkStateChanged.connect(self.changecheckBoxRemember)
        self.load_saved_credentials()

    def btn_close(self):
        self.changecheckBoxRemember()
        self.close()

    def changecheckBoxRemember(self):
        """checkbox状态改变时，记录状态"""
        if self.checkBoxRemember.isChecked():
            self.settings.setValue("Remember", "True")
            self.settings.setValue("userName", self.userNameEdit.text())
        else:
            self.settings.setValue("Remember", "False")

    def load_saved_credentials(self):
        if self.settings.value("Remember", "") == 'True':
            """加载保存的账号信息"""
            self.userNameEdit.setText(self.settings.value("userName", ""))


    def OnLogin(self):
        username = self.userNameEdit.text()
        password = self.passwordEdit.text()
        self.save_username()
        # 实际项目里登录使用http post

        if username == "" or password == "":
            msgbox = PopupMessageBox("提示", "用户名或密码为空")
            msgbox.setFixedSize(200,100)
            msgbox.exec()

            self.sig_login_failure.emit()
            return

        if self.db.verify_login('users', username, password):
            msgbox = PopupMessageBox("提示", "登录成功!")
            msgbox.setFixedSize(200, 100)
            msgbox.exec()
            if username == "administrator":
                self.sig_login_administrator_success.emit()
            else:
                self.sig_login_success.emit()
            self.accept()
        else:
            QMessageBox.information(self, "提示", "用户名或密码错误")
            self.sig_login_failure.emit()

    def open_login(self):
        self.passwordEdit.setText('')
        flag = self.settings.value("Remember", "")
        if flag == 'True':
            self.checkBoxRemember.setChecked(True)
        else:
            self.checkBoxRemember.setChecked(False)
        """打开登录界面时的逻辑"""
        if not self.checkBoxRemember.isChecked():
            # 如果没有勾选保存账号，清除账号输入框
            self.userNameEdit.clear()
        self.exec()

    def save_username(self):
        """保存账号信息到配置文件"""
        if self.checkBoxRemember.isChecked():
            self.settings.setValue("Remember", 'True')
        else:
            self.settings.setValue("Remember", 'False')
        """保存账号的逻辑"""
        if self.checkBoxRemember.isChecked():
            # 如果checkbox为true，保存当前输入的账号
            self.settings.setValue("userName", self.userNameEdit.text())
            self.saved_username = self.userNameEdit.text()
        else:
            # 如果checkbox为false，不保存账号
            self.saved_username = ""
            self.settings.setValue("userName", '')
        self.close()
