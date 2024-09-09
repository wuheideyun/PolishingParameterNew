'''

登录窗口

'''

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QGridLayout, \
    QSpacerItem, QSizePolicy, QMessageBox

from FrameLessDialog import FrameLessDialog
from ImageButton import ImageButton
from LoginEdit import LoginEdit
from PopupMessageBox import PopupMessageBox


class LoginDialog(FrameLessDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("登录")

        self.setFixedSize(1224, 590)
        # self.setWindowFlag(Qt.FramelessWindowHint)

        outHLay = QHBoxLayout()

        kedaLabel = QLabel()
        kedaLabel.setFixedSize(1000, 666)
        keda_pixmap = QPixmap(":keda")  # 替换为实际图片路径
        kedaLabel.setPixmap(keda_pixmap)
        outHLay.addWidget(kedaLabel)

        mainVLay = QVBoxLayout()

        hlay1 = QHBoxLayout()

        self.btnClose = ImageButton(":close16", 16, 16)
        self.btnClose.clicked.connect(self.close)

        hlay1.addStretch()
        hlay1.addWidget(self.btnClose)

        mainVLay.addLayout(hlay1)
        # self.btnClose.move(500, 10)

        mainVLay.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        logoLabel = QLabel("")
        logoLabel.setFixedSize(302, 48)

        pixmap = QPixmap(":login_logo2")  # 替换为实际图片路径
        logoLabel.setPixmap(pixmap)

        # 如果需要，可以让图片自适应 QLabel 的大小
        logoLabel.setScaledContents(True)

        hlay2 = QHBoxLayout()
        hlay2.addWidget(logoLabel)
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
        mainVLay.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        mainVLay.addLayout(hlay3)

        mainVLay.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        gridLayout = QGridLayout()

        self.userNameEdit = LoginEdit(":login_user")
        self.userNameEdit.setPlaceholderText("用户名/手机号/邮箱")

        gridLayout.addWidget(self.userNameEdit, 0, 0, 1, 2)  # 第0行，第0列，占1行，占2列

        self.passwordEdit = LoginEdit(":login_pwd")
        self.passwordEdit.setPlaceholderText("密码")
        self.passwordEdit.setEchoMode(LoginEdit.Password)

        gridLayout.addWidget(self.passwordEdit, 1, 0, 1, 2)  # 第1行，第0列，占1行，占2列

        self.checkBoxAutoLogin = QCheckBox("自动登录")
        self.checkBoxAutoLogin.setFixedSize(80, 18)

        gridLayout.addWidget(self.checkBoxAutoLogin, 2, 0)

        self.checkBoxRemember = QCheckBox("记住密码")
        self.checkBoxRemember.setFixedSize(80, 18)

        gridLayout.addWidget(self.checkBoxRemember, 2, 1, alignment=Qt.AlignRight)

        hlay4 = QHBoxLayout()
        hlay4.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hlay4.addLayout(gridLayout)
        hlay4.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        mainVLay.addLayout(hlay4)

        mainVLay.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))

        hlay5 = QHBoxLayout()
        self.btnLogin = QPushButton("登 录")
        self.btnLogin.setFixedSize(328, 48)

        self.sig_Login = Signal()
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
        mainVLay.setContentsMargins(30, 30, 30, 30)
        outHLay.addLayout(mainVLay)

        self.setLayout(outHLay)

    def OnLogin(self):
        username = self.userNameEdit.text()
        password = self.passwordEdit.text()

        # 实际项目里登录使用http post

        if username == "" or password == "":
            msgbox = PopupMessageBox("提示", "用户名或密码为空")
            msgbox.exec()
            return

        if username == "admin" and password == "123456":
            QMessageBox.information(self, "提示", "登录成功")
            self.accept()
