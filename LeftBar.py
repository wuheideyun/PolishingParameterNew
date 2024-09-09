'''

左侧宽列表窗口

容纳列表

图片32 * 32

item 高 32 + 5 * 2，宽10 + 32 + 60 + 10

'''

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QCheckBox, QListWidget, QListWidgetItem, \
    QPushButton, QHBoxLayout

from AIBoxWidget import AIBoxWidget
from CustomListItem import CustomListItem
from ImageTextButton import ImageTextButton
from LoginDialog import LoginDialog


class LeftBar(QWidget):
    sig_ListIndex = Signal(int)
    sig_runse1 = Signal()

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        item_w = 111
        w = item_w + 40
        self.setFixedWidth(w)

        self.setAttribute(Qt.WA_StyledBackground)  # 禁止父窗口样式影响子控件样式

        self.setStyleSheet('''
                    QWidget {
                        background-color: rgb(251, 245, 255);
                        border: none;
                        border-top-left-radius:10px solid #cccccc;
                        border-bottom-left-radius:10px solid #cccccc;
                    }
                ''')

        mainVLay = QVBoxLayout()
        mainVLay.setContentsMargins(0, 10, 0, 0)

        hlay00 = QHBoxLayout()

        hlay00.addSpacerItem(QSpacerItem(50, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))

        self.loginBtn = QPushButton("")
        self.loginBtn.setFixedSize(32, 32)
        self.loginBtn.setStyleSheet("""
            QPushButton {
                border: none;
                background-image: url(:user);
                background-position: center center;
                background-repeat: no-repeat;
                background-size: cover; /* 或者使用 contain */
            }
        """)

        self.loginBtn.clicked.connect(self.OnShowLoginDlg)

        hlay00.addWidget(self.loginBtn)
        hlay00.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        mainVLay.addLayout(hlay00)

        roundedButtonStyle = """
            QPushButton {
                background-color: rgb(255,216,188);
                border-style: solid;
                border-color: rgb(255,216,188);
                border-width: 0px;
                border-radius: 10px;
                color: rgb(44,33,65);
                padding: 5px;
                font-size: 14px;
            }
    
            QPushButton:pressed {
                background-color: rgb(105,216,188);
            }
    
            QPushButton:hover {
                background-color: rgb(205,216,188);
            }
        """

        hlay01 = QHBoxLayout()
        self.h_spacer002 = QSpacerItem(15, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)  # Minimum  Expanding
        self.h_spacer003 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  # Minimum  Expanding
        hlay01.addSpacerItem(self.h_spacer002)
        self.vipInfo = QPushButton('会员登录')
        self.vipInfo.setFixedSize(100, 32)
        self.vipInfo.setStyleSheet(roundedButtonStyle)
        hlay01.addWidget(self.vipInfo)
        hlay01.addSpacerItem(self.h_spacer003)

        mainVLay.addLayout(hlay01)

        self.spacer00 = QSpacerItem(40, 60, QSizePolicy.Minimum, QSizePolicy.Fixed)
        mainVLay.addSpacerItem(self.spacer00)

        # self.aiboxItem_widget = AIBoxWidget()
        # mainVLay.addWidget(self.aiboxItem_widget)
        # self.aiboxItem_widget.sig_runse0.connect(self.onRunse)

        # 创建QListWidget实例
        self.listWidget = QListWidget()
        self.listWidget.setFixedSize(w - 30, 42 * 7 + 250)

        # 连接点击事件
        self.listWidget.itemClicked.connect(self.item_clicked)

        self.firstPageItem_widget = CustomListItem(":firstpagered", "同步摆计算")
        self.firstPage_item = QListWidgetItem(self.listWidget)
        self.firstPage_item.setSizeHint(self.firstPageItem_widget.sizeHint())
        self.listWidget.setItemWidget(self.firstPage_item, self.firstPageItem_widget)

        self.transItem_widget = CustomListItem(":transred", "同步摆仿真")
        self.trans_item = QListWidgetItem(self.listWidget)
        self.trans_item.setSizeHint(self.transItem_widget.sizeHint())
        self.listWidget.setItemWidget(self.trans_item, self.transItem_widget)

        self.writeItem_widget = CustomListItem(":writered", "双头摆计算")
        self.write_item = QListWidgetItem(self.listWidget)
        self.write_item.setSizeHint(self.writeItem_widget.sizeHint())
        self.listWidget.setItemWidget(self.write_item, self.writeItem_widget)

        self.soulunwenItem_widget = CustomListItem(":soulunwenred", "双头摆仿真")
        self.soulunwen_item = QListWidgetItem(self.listWidget)
        self.soulunwen_item.setSizeHint(self.soulunwenItem_widget.sizeHint())
        self.listWidget.setItemWidget(self.soulunwen_item, self.soulunwenItem_widget)

        self.dicbookItem_widget = CustomListItem(":dickbookred", "单头摆计算")
        self.dicbook_item = QListWidgetItem(self.listWidget)
        self.dicbook_item.setSizeHint(self.dicbookItem_widget.sizeHint())
        self.listWidget.setItemWidget(self.dicbook_item, self.dicbookItem_widget)

        self.mytransItem_widget = CustomListItem(":mytransred", "单头摆仿真")
        self.mytrans_item = QListWidgetItem(self.listWidget)
        self.mytrans_item.setSizeHint(self.mytransItem_widget.sizeHint())
        self.listWidget.setItemWidget(self.mytrans_item, self.mytransItem_widget)

        mainVLay.addWidget(self.listWidget)

        self.spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        mainVLay.addSpacerItem(self.spacer)

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
            QListWidget {
                background-color:rgb(251, 245, 255);
                border: none; /* 隐藏边框 */
            }
    
            QListWidget::verticalScrollBar {
                width: 0px; /* 将滚动条宽度设置为0，实际上是隐藏它 */
            }
        """

        # 假设你有一个QListWidget实例叫做myListWidget
        self.listWidget.setStyleSheet(style_sheet)

    def onRunse(self):
        self.sig_runse1.emit()

    def OnShowLoginDlg(self):
        loginDialog = LoginDialog()
        loginDialog.exec()

    def item_clicked(self, item):
        # 重置所有项的自定义属性
        for index in range(self.listWidget.count()):
            self.listWidget.item(index).setData(Qt.UserRole, False)

        index = self.listWidget.row(item)
        self.sig_ListIndex.emit(index)

        # 设置被点击项的自定义属性
        item.setData(Qt.UserRole, True)

        # 更新样式
        self.update_stylesheet()

    def update_stylesheet(self):
        # 定义样式表
        stylesheet = """
            QListWidget {
                border: none; /* 隐藏边框 */
                background-color:rgb(251, 245, 255)
            }
            QListWidget::item[data-user-role="true"] {
                /* 被点击项的样式 */
                /*border: 1px solid #5e97f6;*/
                background-color: #b0d4f1;
            }
        """

        # 应用样式表
        self.listWidget.setStyleSheet(stylesheet.replace('data-user-role', str(Qt.UserRole)))

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
