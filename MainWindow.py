'''

主界面

'''

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QEnterEvent
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox, QToolBar, QSizePolicy


from ContentWidget import ContentWidget
from LeftBar import LeftBar
from TitleBar import TitleBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # 不要加self
        self.setMouseTracking(True)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)  # 设置为无边框窗口

        # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置主窗口的标题
        self.setWindowTitle("科达系统")

        # self.setStyleSheet('''
        #     background-color:white;
        #     border-radius:10px;
        # ''')

        mainHLay = QHBoxLayout()
        mainHLay.setSpacing(0)
        mainHLay.setContentsMargins(0, 0, 0, 0)

        self.leftBar = LeftBar()
        mainHLay.addWidget(self.leftBar)
        self.leftBar.sig_login_action.connect(self.showStackWidget)
        self.leftBar.sig_runse1.connect(self.onRunse)

        vLay = QVBoxLayout()
        vLay.setContentsMargins(0,0,0,0)
        vLay.setSpacing(0)
        self.titleBar = TitleBar()
        vLay.addWidget(self.titleBar)

        self.titleBar.sig_Min.connect(self.onMin)
        self.titleBar.sig_Normal.connect(self.onNormal)
        self.titleBar.sig_Max.connect(self.onMax)
        self.titleBar.sig_Close.connect(self.onClose)

        self.contentWidget = ContentWidget()
        vLay.addWidget(self.contentWidget)
        mainHLay.addLayout(vLay)

        # 创建一个QWidget作为中央部件
        self.centralWidget = QWidget()
        self.centralWidget.setMouseTracking(True)  # 给QMainWindow中间控件设置鼠标跟踪，不然无法监控拉伸时鼠标的样式
        self.centralWidget.setContentsMargins(0, 0, 0, 0)
        # 将布局设置给中央部件
        self.centralWidget.setLayout(mainHLay)

        # 最后，设置窗口的中央部件
        self.setCentralWidget(self.centralWidget)

        self.leftBar.sig_ListIndex.connect(self.changeContentPage)

        # self.statusBar = BottomStatusBar()
        # self.setStatusBar(self.statusBar)
        # self.statusBar.setStyleSheet('''
        #     background-color: rgb(255, 255, 255);
        #     color: rgb(0, 0, 0);
        #     radius: 15px;
        # ''')
        # self.statusBar.setContentsMargins(150,0,0,0)
        # self.statusBar.contentsMargins()
        # self.statusBar.showMessage('Status')

        ####################################################
        # 这里5距离是指窗口setContentsMargins的大小
        self.kMouseRegionLeft = 5
        self.kMouseRegionTop = 5
        self.kMouseRegionButtom = 5
        self.kMouseRegionRight = 5

        self.kMouseDrag = 0
        self.kMousePositionLeftTop = 11
        self.kMousePositionTop = 12  # 拖拽移动的区域
        self.kMousePositionRightTop = 13
        self.kMousePositionLeft = 21
        self.kMousePositionMid = 22
        self.kMousePositionRight = 23
        self.kMousePositionLeftButtom = 31
        self.kMousePositionButtom = 32
        self.kMousePositionRightButtom = 33

        self.TITLEBAR_HEIGHT = 32
        self.TITLEBAR_MARGIN = 5

        self.last_point_ = None
        self.last_position_ = None  # 窗口上一次的位置

        self.left_button_pressed_ = False
        self.mouse_press_region_ = self.kMousePositionMid  # 鼠标点击的区域

        self.installEventFilter(self)  # 初始化事件过滤器

        # 设置窗口的尺寸
        self.setGeometry(0, 0, 1000, 600)

        self.center_on_screen()

    def center_on_screen(self):
        # 获取显示器分辨率
        screen_geometry = self.screen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # 计算窗口的左上角点位置
        x_position = (screen_width - self.width()) / 2
        y_position = (screen_height - self.height()) / 2 - 60 # 向上偏移60像素

        # 移动窗口到上述位置
        self.move(int(x_position), int(y_position))

    def onRunse(self):
        QMessageBox.information(None, '提示', '智能润色')

    def showStackWidget(self,flag):
        if flag:
            self.contentWidget.setStackedWidgetVisible(True)
        else:
            self.contentWidget.setStackedWidgetVisible(False)

    def eventFilter(self, obj, event):
        # 事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super().eventFilter(obj, event)

    def onMin(self):
        self.showMinimized()

    def onNormal(self):
        TitleBar.isMax = False
        self.titleBar.setMaxIcon(False)
        self.showNormal()

    def onMax(self):
        TitleBar.isMax = True
        self.titleBar.setMaxIcon(True)
        self.showMaximized()

    def onClose(self):
        self.close()

    def changeContentPage(self, index):
        self.contentWidget.gotoPage(index)

    def mousePressEvent(self, event):
        tempPos = event.pos()

        if event.buttons() == Qt.LeftButton:
            self.left_button_pressed_ = True
            self.last_point_ = self.pos()
            self.last_position_ = event.globalPos()
            self.mouse_press_region_ = self.getMouseRegion(tempPos.x(), tempPos.y())

    def mouseMoveEvent(self, event):
        self.setMouseCursor(event.pos().x(), event.pos().y())

        if (event.buttons() == Qt.LeftButton) and self.left_button_pressed_:
            point_offset = event.globalPos() - self.last_position_

            if self.mouse_press_region_ == self.kMouseDrag:
                self.setCursor(Qt.ArrowCursor)
                self.move(point_offset + self.last_point_)
            else:
                rect = self.geometry()

                if self.mouse_press_region_ == self.kMousePositionLeftTop:  # 左上角
                    rect.setTopLeft(rect.topLeft() + point_offset)
                elif self.mouse_press_region_ == self.kMousePositionTop: # 上面
                    rect.setTop(rect.top() + point_offset.y())
                elif self.mouse_press_region_ == self.kMousePositionRightTop: # 右上角
                    rect.setTopRight(rect.topRight() + point_offset)
                elif self.mouse_press_region_ == self.kMousePositionRight: # 右边
                    rect.setRight(rect.right() + point_offset.x())
                elif self.mouse_press_region_ == self.kMousePositionRightButtom: # 右下角
                    rect.setBottomRight(rect.bottomRight() + point_offset)
                elif self.mouse_press_region_ == self.kMousePositionButtom: # 下面
                    rect.setBottom(rect.bottom() + point_offset.y())
                elif self.mouse_press_region_ == self.kMousePositionLeftButtom: # 左下角
                    rect.setBottomLeft(rect.bottomLeft() + point_offset)
                elif self.mouse_press_region_ == self.kMousePositionLeft: # 左边
                    rect.setLeft(rect.left() + point_offset.x())

                self.setGeometry(rect)
                self.last_position_ = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.left_button_pressed_ = False

    def setMouseCursor(self, x, y):
        cursor = Qt.ArrowCursor
        region = self.getMouseRegion(x, y)

        if region == self.kMousePositionLeftTop or region == self.kMousePositionRightButtom:
            cursor = Qt.SizeFDiagCursor
        elif region == self.kMousePositionRightTop or region == self.kMousePositionLeftButtom:
            cursor = Qt.SizeBDiagCursor
        elif region == self.kMousePositionLeft or region == self.kMousePositionRight:
            cursor = Qt.SizeHorCursor
        elif region == self.kMousePositionTop or region == self.kMousePositionButtom:
            cursor = Qt.SizeVerCursor
        elif region == self.kMousePositionMid:
            cursor = Qt.ArrowCursor

        self.setCursor(cursor)

    def getMouseRegion(self, x, y):
        w = self.width()
        region_x = 0
        region_y = 0

        if x < self.kMouseRegionLeft:
            region_x = 1
        elif x > w - self.kMouseRegionRight:
            region_x = 3
        else:
            region_x = 2

        if y < self.kMouseRegionTop:
            region_y = 1
        elif y > self.height() - self.kMouseRegionButtom:
            region_y = 3
        elif x > self.TITLEBAR_MARGIN and x < w - self.TITLEBAR_MARGIN and y > self.TITLEBAR_MARGIN and y < self.TITLEBAR_HEIGHT - self.TITLEBAR_MARGIN:
            # 拖拽区域
            return 0
        else:
            region_y = 2

        return region_y * 10 + region_x

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255, 255))
        rect = self.rect()
        painter.drawRoundedRect(rect, 10, 10)  # 绘制圆角矩形
