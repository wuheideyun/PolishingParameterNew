'''

标题栏

图片大小16 * 16
高度16 + 5 * 5

'''


from PySide6.QtCore import Signal, Qt, QPoint
from PySide6.QtGui import QPainter, QColor, QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QVBoxLayout, QMenu, QLabel

from CheckCodeDialog import CheckCodeDialog
from ImageButton import ImageButton
from ImageTextButton import ImageTextButton


class TitleBar(QWidget):
    sig_Min = Signal()
    sig_Max = Signal()
    sig_Normal = Signal()
    sig_Close = Signal()
    sig_logout = Signal()
    isMax = False

    def __init__(self):
        super().__init__()
        self.setFixedHeight(32)

        self.setMouseTracking(True)
        self.checkcodeDialog = CheckCodeDialog()

        self.setAttribute(Qt.WA_StyledBackground)  # 禁止父窗口样式影响子控件样式
        self.setStyleSheet('''
                    QWidget {
                        background-color: rgb(251, 245, 255);
                        border: none;
                        border-top-right-radius:10px solid #f00;
                    }
                ''')

        self.btnMenu = QPushButton("")
        self.btnMenu.setFixedSize(16, 16)

        self.btnMenu.setContextMenuPolicy(Qt.CustomContextMenu)
        self.btnMenu.customContextMenuRequested.connect(self.show_menu)

        # 创建菜单
        self.menu = QMenu()
        self.menu.addAction("激活码验证", self.action1_triggered)
        # self.menu.addAction("会员中心", self.action2_triggered)
        self.menu.addSeparator()
        # self.menu.addAction("意见反馈")
        # self.menu.addAction("关于")
        self.menu.addAction("退出登录", self.action2_triggered)

        self.btnMenu.setMenu(self.menu)

        qss = """
            QMenu {
                font: 15px; /* 设置菜单字体大小 */
                color: black; /* 设置菜单字体颜色 */
                background-color: #f2f2f2; /* 菜单背景色 */
            }
    
            QMenu::item {
                /* 设置菜单项的字体颜色和背景颜色 */
                color: blue; /* 菜单项字体颜色 */
                background-color: transparent; /* 菜单项背景色 */
                padding: 5px 20px; /* 菜单项内边距 (上下左右) */
                border: 1px solid transparent; /* 菜单项边框 */
            }
    
            QMenu::item:selected { /* 当菜单项被选中时 */
                background-color: #3875d7; /* 选中项背景色 */
                color: white; /* 选中项字体颜色 */
            }
    
            QMenu::icon {
                /* 调整图标和文本的间距 */
                margin-right: 5px;
            }
    
            /* 设置分隔符的样式 */
            QMenu::separator {
                height: 2px; /* 分隔符高度 */
                background-color: lightgray; /* 分隔符颜色 */
                margin-left: 10px;
                margin-right: 10px;
            }
        """

        self.menu.setStyleSheet(qss)

        qss001 = '''
            QPushButton {
                border: none;
                background-image: url(:menu16);
                background-position: center center;
                background-repeat: no-repeat;
                background-color: rgb(251, 245, 255)
            }
            
            QPushButton:hover {
                background-color: #f00; /* 鼠标悬停时的背景色 */
            }
            
            QPushButton::menu-indicator { 
                image: none; 
                width: 0px; 
            }
        '''

        self.btnMenu.setStyleSheet(qss001)

        btnMin = ImageButton(":min16", 16, 16)
        btnMin.clicked.connect(self.onMin)

        self.btnMax = QPushButton("")
        self.btnMax.setFixedSize(16, 16)
        self.btnMax.clicked.connect(self.onMax)
        self.btnMax.setIcon(QIcon(":max16"))  # 设置按钮图标

        # 让图标自适应按钮大小
        self.btnMax.setIconSize(self.btnMax.size())  # 和按钮的尺寸一致

        self.btnMax.setStyleSheet("""
            QPushButton {
                border: none; /* 无边框 */
            }

            QPushButton:hover {
                background-color: #f00; /* 鼠标悬停时的背景色 */
            }

            QPushButton:pressed {
                background-color: #aaaaaa; /* 鼠标按下时的背景色 */
            }
        """)

        btnClose = ImageButton(":close16", 16, 16)
        btnClose.clicked.connect(self.onClose)

        hlay = QHBoxLayout()
        hlay.setContentsMargins(0, 0, 0, 0)

        label = QLabel()
        label.setText("Copyright © 2024 科达制造股份有限公司")
        hlay.addWidget(label)
        hlay.addStretch()

        hlay.addWidget(self.btnMenu)
        hlay.addSpacerItem(QSpacerItem(15, 5, QSizePolicy.Fixed, QSizePolicy.Minimum))
        hlay.addWidget(btnMin)
        hlay.addSpacerItem(QSpacerItem(15, 5, QSizePolicy.Fixed, QSizePolicy.Minimum))
        hlay.addWidget(self.btnMax)
        hlay.addSpacerItem(QSpacerItem(15, 5, QSizePolicy.Fixed, QSizePolicy.Minimum))
        hlay.addWidget(btnClose)
        hlay.addSpacerItem(QSpacerItem(15, 5, QSizePolicy.Fixed, QSizePolicy.Minimum))

        self.setLayout(hlay)

    def onMin(self):
        self.sig_Min.emit()

    def onClose(self):
        self.sig_Close.emit()

    def onMax(self):
        if self.isMax:   # 用于判断当前窗口是否为最大化, 在主窗口可以设置True或False
            self.sig_Normal.emit()
        else:
            self.sig_Max.emit()

    def setMaxIcon(self, isMax):
        if isMax:
            self.btnMax.setIcon(QIcon(":normal16"))
        else:
            self.btnMax.setIcon(QIcon(":max16"))

    def show_menu(self, pos):
        # 在按钮下方显示菜单
        self.menu.exec(self.button.mapToGlobal(pos))

    def action1_triggered(self):
        self.checkcodeDialog.open_checkcode()

    def action2_triggered(self):
        print("Action 2 triggered")

    def exit_triggered(self):
        self.close()

    def mouseDoubleClickEvent(self, event):
        self.onMax()
