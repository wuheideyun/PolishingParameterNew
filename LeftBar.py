'''

左侧宽列表窗口

容纳列表

图片32 * 32

item 高 32 + 5 * 2，宽10 + 32 + 60 + 10

'''

from PySide6.QtCore import Qt, Signal, QTranslator, QCoreApplication
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QCheckBox, QListWidget, QListWidgetItem, \
    QPushButton, QHBoxLayout, QDialog, QMessageBox, QApplication

from AIBoxWidget import AIBoxWidget
from ConfirmDialog import ConfirmDialog
from CustomListItem import CustomListItem
from ImageTextButton import ImageTextButton
from LoginDialog import LoginDialog
from SwitchButton import SwitchButton


class LeftBar(QWidget):
    sig_ListIndex = Signal(int)
    sig_runse1 = Signal()

    sig_switch_language = Signal(bool)
    sig_login_action = Signal(bool)
    sig_login_administrator_action = Signal(bool)
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.loginDialog = LoginDialog()
        # 初始化翻译器
        self.translator = QTranslator()
        self.current_language = "zh"
        self.isLogin = False
        item_w = 141
        w = item_w + 40
        self.setFixedWidth(w)

        self.setAttribute(Qt.WA_StyledBackground)  # 禁止父窗口样式影响子控件样式

        self.setStyleSheet('''
            QWidget {
                background-color: rgb(50, 126, 188);
                border: none;
                border-top-left-radius:10px 10px 0 0 solid #cccccc;
                border-bottom-left-radius:10px 10px 0 0 solid #cccccc;
            }
        ''')

        mainVLay = QVBoxLayout()
        mainVLay.setContentsMargins(10, 10, 0, 0)

        hlay00 = QHBoxLayout()

        # hlay00.addSpacerItem(QSpacerItem(50, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))

        self.loginBtn = QPushButton("")
        self.loginBtn.setFixedSize(140, 50)
        self.loginBtn.setStyleSheet("""
            QPushButton {
                background-image: url(:kedalogo2);
                background-repeat: no-repeat;
                background-position: center;
                background-size: contain;
                border: none;
                outline: none;  /* 去掉按钮的虚线框 */
                font-color: white;
            }
        """)

        self.loginBtn.clicked.connect(self.OnShowLoginDlg)

        hlay00.addWidget(self.loginBtn)
        hlay00.setContentsMargins(10,40,10,10)
        hlay00.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        mainVLay.addLayout(hlay00)

        roundedButtonStyle = """
            QPushButton {
                color: white;
                background-color: rgb(50,126,188);
                border-style: solid;
                border-color: rgb(50,126,188);
                border-width: 0px;
                border-radius: 10px 10px 0 0;
                padding: 5px;
                font-size: 18px;
                outline: none;  /* 去掉按钮的虚线框 */
            }
    
            QPushButton:pressed {
                background-color: rgb(34,90,137);
            }
    
            QPushButton:hover {
                background-color: rgb(48,122,181);
            }
        """

        hlay01 = QHBoxLayout()
        self.h_spacer002 = QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)  # Minimum  Expanding
        self.h_spacer003 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  # Minimum  Expanding
        hlay01.addSpacerItem(self.h_spacer002)
        self.vipInfo = ImageTextButton(':homepage',self.tr("会员登录"),140,35)
        self.vipInfo.setStyleSheet(roundedButtonStyle)
        self.vipInfo.clicked.connect(self.OnShowLoginDlg)
        hlay01.addWidget(self.vipInfo)
        hlay01.addSpacerItem(self.h_spacer003)

        hlay01.setContentsMargins(10,0,10,10)
        mainVLay.addLayout(hlay01)

        self.spacer00 = QSpacerItem(40, 60, QSizePolicy.Minimum, QSizePolicy.Fixed)
        mainVLay.addSpacerItem(self.spacer00)

        # self.aiboxItem_widget = AIBoxWidget()
        # mainVLay.addWidget(self.aiboxItem_widget)
        # self.aiboxItem_widget.sig_runse0.connect(self.onRunse)

        # 创建QListWidget实例
        self.listWidget = QListWidget()
        self.listWidget.setFixedSize(w - 20, 42 * 7 + 150)

        # 连接点击事件
        self.listWidget.itemClicked.connect(self.item_clicked)

        self.firstPageItem_widget = CustomListItem(":single_click", self.tr("同步摆计算"))
        self.firstPageItem_widget.setContentsMargins(8,0,20,0)
        self.firstPage_item = QListWidgetItem(self.listWidget)
        self.firstPage_item.setSizeHint(self.firstPageItem_widget.sizeHint())
        self.listWidget.setItemWidget(self.firstPage_item, self.firstPageItem_widget)

        self.transItem_widget = CustomListItem(":quora", self.tr("同步摆仿真"))
        self.transItem_widget.setContentsMargins(8,0,20,0)
        self.trans_item = QListWidgetItem(self.listWidget)
        self.trans_item.setSizeHint(self.transItem_widget.sizeHint())
        self.listWidget.setItemWidget(self.trans_item, self.transItem_widget)

        self.writeItem_widget = CustomListItem(":single_click", self.tr("双头摆计算"))
        self.writeItem_widget.setContentsMargins(8,0,20,0)
        self.write_item = QListWidgetItem(self.listWidget)
        self.write_item.setSizeHint(self.writeItem_widget.sizeHint())
        self.listWidget.setItemWidget(self.write_item, self.writeItem_widget)

        self.soulunwenItem_widget = CustomListItem(":quora", self.tr("双头摆仿真"))
        self.soulunwenItem_widget.setContentsMargins(8,0,20,0)
        self.soulunwen_item = QListWidgetItem(self.listWidget)
        self.soulunwen_item.setSizeHint(self.soulunwenItem_widget.sizeHint())
        self.listWidget.setItemWidget(self.soulunwen_item, self.soulunwenItem_widget)

        self.dicbookItem_widget = CustomListItem(":single_click", self.tr("单头摆计算"))
        self.dicbookItem_widget.setContentsMargins(8,0,20,0)
        self.dicbook_item = QListWidgetItem(self.listWidget)
        self.dicbook_item.setSizeHint(self.dicbookItem_widget.sizeHint())
        self.listWidget.setItemWidget(self.dicbook_item, self.dicbookItem_widget)

        self.mytransItem_widget = CustomListItem(":quora", self.tr("单头摆仿真"))
        self.mytransItem_widget.setContentsMargins(8,0,20,0)
        self.mytrans_item = QListWidgetItem(self.listWidget)
        self.mytrans_item.setSizeHint(self.mytransItem_widget.sizeHint())
        self.listWidget.setItemWidget(self.mytrans_item, self.mytransItem_widget)

        mainVLay.addWidget(self.listWidget)

        self.spacer = QSpacerItem(40, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        mainVLay.addSpacerItem(self.spacer)
        mainVLay.setContentsMargins(10,10,10,10)

        layout = QVBoxLayout()
        self.language_switch = SwitchButton()
        # 添加按钮到布局，并设置水平居中
        layout.addWidget(self.language_switch, 0, Qt.AlignCenter)
        self.language_switch.sig_language_switch.connect(self.switch_language)

        mainVLay.addLayout(layout)
        # self.btnShotTrans = ImageTextButton(":shotimg", "工具")
        # self.btnShotTrans.setFixedSize(92, 32)
        #
        # hlay21 = QHBoxLayout()
        # self.h_spacer21 = QSpacerItem(12, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)  # Minimum  Expanding
        # hlay21.addSpacerItem(self.h_spacer21)
        # hlay21.addWidget(self.btnShotTrans)
        # self.h_spacer22 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  # Minimum  Expanding
        # hlay21.addSpacerItem(self.h_spacer22)
        #
        # mainVLay.addLayout(hlay21)

        # hlay3 = QHBoxLayout()
        # self.checkBox_1 = QCheckBox("取词")
        # self.checkBox_1.setFixedSize(80, 32)
        #
        # self.h_spacer1 = QSpacerItem(12, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)  # Minimum  Expanding
        # hlay3.addSpacerItem(self.h_spacer1)
        #
        # hlay3.addWidget(self.checkBox_1)
        #
        # self.h_spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  # Minimum  Expanding
        # hlay3.addSpacerItem(self.h_spacer2)
        #
        # mainVLay.addLayout(hlay3)

        # hlay4 = QHBoxLayout()
        # self.checkBox_2 = QCheckBox("划词")
        # self.checkBox_2.setFixedSize(80, 32)
        #
        # self.h_spacer3 = QSpacerItem(12, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)  # Minimum  Expanding
        # hlay4.addSpacerItem(self.h_spacer3)
        #
        # hlay4.addWidget(self.checkBox_2)
        #
        # self.h_spacer4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  # Minimum  Expanding
        # hlay4.addSpacerItem(self.h_spacer4)
        #
        # mainVLay.addLayout(hlay4)

        self.setLayout(mainVLay)

        style_sheet = """
            QListWidget::item:selected {
                background-color: #2E5C92;  /* 背景颜色 */
                color: white;               /* 文字颜色 */
                border-radius: 10px;
                border-right: 5px solid red;  /* 右侧的红色边框 */
            }
            QListWidget {
                background-color:rgb(50, 126, 188);
                border: none; /* 隐藏边框 */
                outline: none;  /* 去掉 QListWidget 选中项的虚线框 */
            }
            QListWidget::verticalScrollBar {
                width: 0px; /* 将滚动条宽度设置为0，实际上是隐藏它 */
            }
        """
        # 假设你有一个QListWidget实例叫做myListWidget
        self.listWidget.setStyleSheet(style_sheet)


        self.loginDialog.sig_login_success.connect(self.loginSuccess)
        self.loginDialog.sig_login_administrator_success.connect(self.loginAdministratorSuccess)
        self.loginDialog.sig_login_failure.connect(self.loginFailure)

    def onRunse(self):
        self.sig_runse1.emit()

    def OnShowLoginDlg(self):
        if self.current_language == "zh":
            QApplication.instance().removeTranslator(self.translator)
            # if self.vipInfo.text() == self.tr("退出登录"):
            #     self.vipInfo.setText(self.tr("退出登录"))
            # else:
            #     self.vipInfo.setText(self.tr("会员登录"))
        else:
            # 切换到英文
            # if self.translator.load("zh_CN.qm"):  # 加载语言文件
            QApplication.instance().installTranslator(self.translator)
                # if self.vipInfo.text() == self.tr("退出登录"):
                #     self.vipInfo.setText(self.tr("退出登录"))
                # else:
                #     self.vipInfo.setText(self.tr("会员登录"))

        if self.isLogin:
            """弹出确认对话框"""
            reply = QMessageBox.question(self, QCoreApplication.translate("MainWindow","确认",None), QCoreApplication.translate("MainWindow","你确定要退出登录吗？",None),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.isLogin = False
                self.sig_login_action.emit(False)
                self.vipInfo.setText(QCoreApplication.translate("MainWindow","会员登录",None))
        else:
            self.loginDialog.open_login(self.current_language)
    def item_clicked(self, item):
        # 重置所有项的自定义属性
        # for index in range(self.listWidget.count()):
        #     self.listWidget.item(index).setData(Qt.UserRole, False)

        index = self.listWidget.row(item)
        self.sig_ListIndex.emit(index)

        # 设置被点击项的自定义属性
        # item.setData(Qt.UserRole, True)

        # 更新样式
        # self.update_stylesheet()

    def loginSuccess(self):
        self.isLogin = True
        self.vipInfo.setText(QCoreApplication.translate("MainWindow","退出登录",None))
        self.sig_login_action.emit(True)

    def loginAdministratorSuccess(self):
        self.isLogin = True
        self.vipInfo.setText(QCoreApplication.translate("MainWindow","退出登录",None))
        self.sig_login_action.emit(True)
        self.sig_login_administrator_action.emit(True)

    def loginFailure(self):
        self.isLogin = False
        self.sig_login_action.emit(False)

    def switch_language(self,isChinese):
        self.sig_switch_language.emit(isChinese)
    def update_stylesheet(self):
        # 定义样式表
        stylesheet = """
            QListWidget {
                border: none; /* 隐藏边框 */
                # background-color:rgb(251, 245, 255)
            }
            QListWidget::item[data-user-role="true"] {
                /* 被点击项的样式 */
                border: 10px solid #ffffff;
                background-color: green;
            }
        """

    def retranslate_ui(self,MainWindow):
        self.firstPageItem_widget.setLabelName(QCoreApplication.translate("MainWindow","同步摆计算",None))
        self.transItem_widget.setLabelName(QCoreApplication.translate("MainWindow","同步摆仿真",None))
        self.writeItem_widget.setLabelName(QCoreApplication.translate("MainWindow","双头摆计算",None))
        self.soulunwenItem_widget.setLabelName(QCoreApplication.translate("MainWindow","双头摆仿真",None))
        self.dicbookItem_widget.setLabelName(QCoreApplication.translate("MainWindow","单头摆计算",None))
        self.mytransItem_widget.setLabelName(QCoreApplication.translate("MainWindow","单头摆仿真",None))

        if self.isLogin:
            self.vipInfo.updateTextName(QCoreApplication.translate("MainWindow","退出登录",None))
        else:
            self.vipInfo.updateTextName(QCoreApplication.translate("MainWindow","会员登录",None))


        # 应用样式表
        # self.listWidget.setStyleSheet(stylesheet.replace('data-user-role', str(Qt.UserRole)))

    # def update_stylesheet(self):
    #     # 定义样式表
    #     stylesheet = """
    #         QListWidget {
    #             border: none; /* 隐藏边框 */
    #             background-color:rgb(251, 245, 255)
    #         }
    #         QListWidget::item {
    #             /* 被点击项的样式 */
    #             /*border: 1px solid #5e97f6;*/
    #             background-color: #b0d4f1;
    #         }
    #     """
    #
    #     # 应用样式表
    #     # self.listWidget.setStyleSheet(stylesheet.replace('data-user-role', str(Qt.UserRole)))
    #     self.listWidget.setStyleSheet(stylesheet)
