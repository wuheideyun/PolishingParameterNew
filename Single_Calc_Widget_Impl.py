from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget

import Single_Calc


class SingleCalcWidgetImpl(QWidget, Single_Calc.Ui_MainWindow):
    def __init__(self, w):
        super().__init__()
        self.setupUi(w)

        self.setAttribute(Qt.WA_StyledBackground)  # 禁止父窗口样式影响子控件样式

        # self.simulation_button.setText("开始翻译")
        # self.simulation_button.setFixedSize(100, 32)
        # self.simulation_button.clicked.connect(self.onStartTrans)

        # 界面分割图片元素
        self.label_top.setText('')
        pixmap = QPixmap(":equal")  # 替换为实际图片路径
        self.label_top.setPixmap(pixmap)
        # 如果需要，可以让图片自适应 QLabel 的大小
        self.label_top.setScaledContents(True)

        self.label_middle.setText('')
        pixmap = QPixmap(":middle")  # 替换为实际图片路径
        self.label_middle.setPixmap(pixmap)
        # 如果需要，可以让图片自适应 QLabel 的大小
        self.label_middle.setScaledContents(True)

        self.label_bottom.setText('')
        pixmap = QPixmap(":bottom")  # 替换为实际图片路径
        self.label_bottom.setPixmap(pixmap)
        # 如果需要，可以让图片自适应 QLabel 的大小
        self.label_bottom.setScaledContents(True)

        qss_TextEdit = """
            QTextEdit {
                border: 1px solid #CAD0EE; 
                border-radius: 2px; /* 轻微的圆角边框 */
            }
        """

        qss_Button = """
            QPushButton {
                background-color: rgb(0, 200, 0); /* 按钮的默认背景色为绿色 */
                color: white; /* 设置按钮文字颜色为白色 */
                border: none; /* 移除边框 */
                padding: 3px; /* 内边距 */
                font-size: 12px; /* 文字大小 */
                border-radius:5px;
            }

            QPushButton:hover {
                 background-color: #45A049; /* 鼠标悬停时按钮的背景色变深 */
            }

            QPushButton:pressed {
                background-color: #397d3c; /* 鼠标按下时按钮的背景色更深 */
            }
        """

        self.button_energy_calculate.setStyleSheet(qss_Button)
        self.button_middle_line_order.setStyleSheet(qss_Button)
        self.button_animation_order.setStyleSheet(qss_Button)
        self.button_simulation_order.setStyleSheet(qss_Button)
        self.button_animation_order_define.setStyleSheet(qss_Button)
        self.button_middle_line_order_define.setStyleSheet(qss_Button)
        self.button_efficient_calculate.setStyleSheet(qss_Button)
        self.button_selfdefine_calculate.setStyleSheet(qss_Button)
        self.button_simulation_order_define.setStyleSheet(qss_Button)


