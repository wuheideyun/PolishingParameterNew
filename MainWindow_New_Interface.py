import ctypes
import os
import stat
import sys
import time

from PySide6.QtCore import QTranslator, QLocale, QEvent
from PySide6.QtGui import QPainter, QPixmap, QColor, QPalette, QBrush, QFont
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, \
    QLineEdit, QFrame, QSizePolicy, QSpacerItem, QStackedWidget, QScrollArea, QMessageBox, QStatusBar
from PySide6.QtCore import Qt, QSize, QSettings, QTimer

from DataModel import DataModel
from HostParamEqualWidget import HostParamEqualWidget
from JustifiedLabel import JustifiedLabel
from PySide6.QtGui import QMovie
from HostParamDoubleWidget import HostParamDoubleWidget
from HostParamSingleWidget import HostParamSingleWidget
from ImageButton import ImageButton
from ImageChangeButton import ImageChangeButton
from ImageChangeWithTextButton import ImageChangeWithTextButton
from LoggerHelper import LoggerHelper
from MotionInputOutputParamCombineWidget import MotionInputOutputParamCombineWidget
from MotionInputParamWidget import MotionInputParamWidget
from MotionOutputParamWidget import MotionOutputParamWidget
from OutputReportQWidget import OutputReportWidget
from TitleBar import TitleBar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtGui import QColor

# 设置框架样式表
frameStyleSheet = """
            QStackedWidget, QFrame {
                border: 5px solid #1a4a93;
                border-radius: 20px;
                margin: 8px;
            }
            QLabel {
                border : none;
            }
        """

# Matplotlib画布类
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height))
        deep_blue = (31 / 255, 55 / 255, 96 / 255)
        self.fig.patch.set_facecolor(deep_blue)
        super().__init__(self.fig)
        self.setParent(parent)

# 主窗口类
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化翻译器和语言状态
        self.translator = QTranslator(self)
        self.is_english = False  # 默认为中文
        # 检查是否在 PyCharm 中运行
        if self.is_running_in_pycharm():
            print("程序在 PyCharm 中运行，跳过管理员权限检查。")
        else:
            # 检查是否以管理员权限运行
            if not self.is_admin():
                print("程序需要以管理员权限运行，正在重新启动...")
                self.run_as_admin()
                time.sleep(3)
                sys.exit(0)  # 退出当前进程
            else:
                print("程序已以管理员权限运行。")

        # 继续执行程序的逻辑
        print("程序正在运行...")
        # 检查动画文件夹是否存在
        self.check_and_create_folder()
        # 是否计算标识
        self.ifcalcflag = False
        self.data_model = DataModel('database.db')
        self.margin_value = 5
        self.flag = False
        self.logger = LoggerHelper('param_change')
        self.selectedFunction = 1
        # 输出报告界面
        self.output_report = OutputReportWidget(self.data_model)
        # 创建定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)

        self.host_param_single_changed_flag = False
        self.host_param_double_changed_flag = False
        self.motion_input_intelligence_changed_flag = False
        self.motion_input_manual_changed_flag = False

        self.left_frame_width = 395
        self.middle_frame_width = 1050
        self.right_frame_width = 410
        self.setWindowTitle(self.tr("抛光仿真系统"))
        self.setStyleSheet("color: white;")
        # 设备切换标签    1：单头摆  2：双头摆  3：同步摆
        self.current_device = 1
        self.device_mapping = {
            1: self.tr("单头摆"),
            2: self.tr("双头摆"),
            3: self.tr("同步摆")
        }
        # 设备图片路径映射
        self.device_image_mapping = {
            1: ":DeviceSingle",
            2: ":DeviceDouble",
            3: ":DeviceEqual"
        }
        # 模式切换标签    1：智能寻优模式  2：方案验证模式
        self.current_mode = 1
        self.mode_mapping = {
            1: self.tr("智能寻优模式"),
            2: self.tr("方案验证模式")
        }
        # 方案选择 1：节能方案  2：高品质方案  3: 自定义修正方案  4：同步摆动模式  5：交叉摆动模式  6：顺序摆动模式
        self.solution_selection = 1
        self.selection_mapping = {
            1: self.tr("节能方案"),
            2: self.tr("高品质方案"),
            3: self.tr("自定义修正方案"),
            4: self.tr("同步摆动模式"),
            5: self.tr("交叉摆动模式"),
            6: self.tr("顺序摆动模式")
        }
        self.swing_mode_mapping = {
            1: self.tr("顺序摆"),
            2: self.tr("顺序摆"),
            3: self.tr("顺序摆"),
            4: self.tr("同步摆"),
            5: self.tr("交叉摆"),
            6: self.tr("顺序摆")
        }
        # self.setAttribute(Qt.WA_TranslucentBackground)# 设置窗口背景透明
        self.settings = QSettings("config.ini", QSettings.IniFormat)  # 使用配置文件

        # 创建 QStackedWidget
        self.host_param_stacked_widget = QStackedWidget()
        self.host_param_stacked_widget.setFixedSize(self.left_frame_width, 320)
        self.host_param_stacked_widget.setStyleSheet(frameStyleSheet)

        # 创建 QStackedWidget
        self.motion_param_stacked_widget = QStackedWidget()
        self.motion_param_stacked_widget.setFixedSize(400, 910)

        # 初始窗口大小
        self.resize(1560, 540)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(0)

        global_layout = QVBoxLayout()
        # global_layout.addSpacerItem(QSpacerItem(500,100,QSizePolicy.Expanding, QSizePolicy.Fixed))

        top_layout = QHBoxLayout()

        version_label = JustifiedLabel(self.tr("版本号: KDUI-2401"))
        version_label.setFixedSize(250, 100)
        # 设置字体大小和字体类型
        param_font = QFont("Microsoft YaHei", 18)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        version_label.setFont(param_font)
        version_label.setAlignment(Qt.AlignRight)
        top_layout.addWidget(version_label, 0, Qt.AlignRight)
        top_layout.addSpacerItem(QSpacerItem(60, 100, QSizePolicy.Fixed, QSizePolicy.Minimum))

        global_layout.addLayout(top_layout)
        # 内容区域布局
        content_layout = QHBoxLayout()
        global_layout.addLayout(content_layout)
        main_layout.addLayout(global_layout)

        # 左侧布局
        left_layout = QVBoxLayout()
        # 区域1 - 三个按钮
        self.button_frame = QFrame()
        self.button_frame.setFixedWidth(self.left_frame_width)
        self.button_frame.setContentsMargins(self.margin_value, 0, self.margin_value, 0)
        self.button_frame.setStyleSheet(frameStyleSheet)

        button_layout = QVBoxLayout(self.button_frame)
        self.single_button = ImageChangeButton("", ":Single", ":SingleClicked", 315, 74)
        self.single_button.clicked.connect(self.switch_motion_param_single_clicked)
        self.double_button = ImageChangeButton("", ":Double", ":DoubleClicked", 315, 74)
        self.double_button.clicked.connect(self.switch_motion_param_double_clicked)
        self.equal_button = ImageChangeButton("", ":Equal", ":EqualClicked", 315, 74)
        self.equal_button.clicked.connect(self.switch_motion_param_equal_clicked)

        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.single_button)
        button_layout.addSpacerItem(QSpacerItem(315, 10, QSizePolicy.Fixed, QSizePolicy.Fixed))
        button_layout.addWidget(self.double_button)
        button_layout.addSpacerItem(QSpacerItem(315, 10, QSizePolicy.Fixed, QSizePolicy.Fixed))
        button_layout.addWidget(self.equal_button)

        left_layout.addWidget(self.button_frame)

        # 区域2 - 图片位置
        self.image_frame = QFrame()
        self.image_frame.setFixedWidth(self.left_frame_width)
        image_layout = QHBoxLayout(self.image_frame)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setSpacing(0)

        # 创建一个容器来放置image_label，以便控制其位置
        image_label_container = QWidget()
        image_label_container.setFixedHeight(150)  # 设置容器高度
        image_label_layout = QVBoxLayout(image_label_container)
        image_label_layout.setContentsMargins(0, 0, 0, 0)  # 设置布局边距为0

        self.image_label = QLabel(self.tr("机\n型\n图"))
        self.image_label.setStyleSheet("border : none;")
        self.image_label.setFixedWidth(90)
        # 设置字体大小和字体类型
        image_font = QFont("Microsoft YaHei", 18)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        self.image_label.setFont(image_font)
        self.image_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        image_label_layout.addWidget(self.image_label)

        # 添加一个负的上边距，使标签向上移动10个像素
        self.image_label.setContentsMargins(40, 0, 0, 0)

        image_layout.addWidget(image_label_container)

        # 添加图片显示区域
        self.device_image_label = QLabel()
        self.device_image_label.setAlignment(Qt.AlignCenter)
        self.device_image_label.setStyleSheet("border: none;")
        # 设置图片标签的固定大小，限制图片区域
        self.device_image_label.setFixedSize(self.left_frame_width - 70, 185)  # 减去边距，设置合适的高度
        image_layout.addWidget(self.device_image_label)

        self.image_frame.setStyleSheet(frameStyleSheet)
        left_layout.addWidget(self.image_frame)
        # 移除这行，因为我们已经添加了图片标签
        # image_layout.addStretch()

        # 区域3 - 主机参数(单头摆)
        self.host_param_single_frame = HostParamSingleWidget()
        self.host_param_single_frame.setFixedSize(self.left_frame_width, 280)
        self.host_param_single_frame.setContentsMargins(50, 0, 50, self.margin_value)
        self.host_param_single_frame.setStyleSheet("border : none")

        # 区域3 - 主机参数(双头摆)
        self.host_param_double_frame = HostParamDoubleWidget()
        self.host_param_double_frame.setFixedSize(self.left_frame_width, 300)
        self.host_param_double_frame.setContentsMargins(50, 0, 50, self.margin_value)
        self.host_param_double_frame.setStyleSheet("border : none")

        # 区域3 - 主机参数(同步摆)
        self.host_param_equal_frame = HostParamEqualWidget()
        self.host_param_equal_frame.setFixedSize(self.left_frame_width, 300)
        self.host_param_equal_frame.setContentsMargins(50, 0, 50, self.margin_value)
        self.host_param_equal_frame.setStyleSheet("border : none")

        self.host_param_stacked_widget.addWidget(self.host_param_single_frame)
        self.host_param_stacked_widget.addWidget(self.host_param_double_frame)
        self.host_param_stacked_widget.addWidget(self.host_param_equal_frame)

        left_layout.addWidget(self.host_param_stacked_widget)

        content_layout.addLayout(left_layout)

        # 中间布局
        center_layout = QVBoxLayout()

        # 区域6 - 轨迹分布
        self.chart_frame1 = QFrame()
        chart1_layout = QHBoxLayout(self.chart_frame1)
        self.chart_frame1.setContentsMargins(0, 0, 0, 0)

        chart_label1 = QLabel(self.tr("轨\n迹\n分\n布"))
        chart1_font = QFont("Microsoft YaHei", 18)
        chart_label1.setFont(chart1_font)

        chart_label1.setFixedWidth(80)
        # chart_label1.setStyleSheet("QLabel { writing-mode: vertical-rl; }")
        # chart1_layout.addSpacing(10)
        chart1_layout.addWidget(chart_label1)
        chart_label1.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.chart_frame1.setFixedSize(self.middle_frame_width, 420)
        self.chart_frame1.setStyleSheet(frameStyleSheet)
        center_layout.addWidget(self.chart_frame1)

        # 创建一个QWidget作为图框--轨迹分布
        self.central_widget = QWidget()
        # 设置 QWidget 尺寸大小
        self.central_widget.setFixedSize(830, 400)  # 最大尺寸为 500x400
        # 设置 QWidget 边框、样式
        self.central_widget.setStyleSheet("""
            QWidget {
                border: 0px solid white;
                border-radius: 10px;
                background-color: transparent;
            }
        """)
        layout_widget = QVBoxLayout(self.central_widget)

        # 创建画布
        self.canvas = MplCanvas(self, width=10, height=4, dpi=100)
        self.canvas.setStyleSheet("""
            border - radius: 10px;
            background - color: white;
        """)
        # 设置画布颜色
        deep_blue = (31 / 255, 55 / 255, 96 / 255)
        # self.canvas.figure.set_facecolor(deep_blue)  # 设置画布背景颜色为底色

        # self.canvas.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明

        chart1_layout.addStretch()
        # 创建拖动条
        scroll_area = QScrollArea(self)
        # 轨迹分布动画框尺寸调整***
        scroll_area.setFixedSize(900, 380)
        scroll_area.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明

        scroll_area.setWidgetResizable(True)  # 强制显示拖动条
        # 给画布设置拖动条
        scroll_area.setWidget(self.canvas)
        # # 自定义滚动条样式
        # scroll_area.verticalScrollBar().setStyleSheet("""
        #             QScrollBar:vertical {
        #                 border: 1px solid #999999;
        #                 border-radius: 20px;
        #                 background: #f0f0f0;
        #                 width: 16px;
        #                 margin: 0px 0 0px 0;
        #             }
        #             QScrollBar::handle:vertical {
        #                 background: #5d99c6;
        #                 min-height: 20px;
        #                 border-radius: 18px;
        #             }
        #             QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        #                 background: none;
        #                 height: 0px;
        #             }
        #             QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        #                 background: #e0e0e0;
        #             }
        #         """)
        #
        # scroll_area.horizontalScrollBar().setStyleSheet("""
        #             QScrollBar:horizontal {
        #                 border: 1px solid #999999;
        #                 border-radius: 10px;
        #                 background: #f0f0f0;
        #                 height: 16px;
        #                 margin: 0px 16px 0px 16px;
        #             }
        #             QScrollBar::handle:horizontal {
        #                 background: #5d99c6;
        #                 min-width: 20px;
        #                 border-radius: 18px;
        #             }
        #             QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        #                 background: none;
        #                 width: 0px;
        #             }
        #             QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        #                 background: #e0e0e0;
        #             }
        #         """)
        # scroll_area.setStyleSheet("QScrollArea { border-radius: 10px; background-color: white; }")

        # 将拖动条加入widget中,并设为居中
        layout_widget.addWidget(scroll_area, alignment=Qt.AlignmentFlag.AlignCenter)
        # 将widget加入QFrame中,并设为居中
        chart1_layout.addWidget(self.central_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        chart1_layout.addStretch()

        # 区域7 - 轨迹动画
        self.chart_frame2 = QFrame()
        # self.chart_frame2.setContentsMargins(self.margin_value,5,self.margin_value,self.margin_value)
        chart_label2 = QLabel("轨\n迹\n动\n画")
        chart2_font = QFont("Microsoft YaHei", 18)
        chart_label2.setFont(chart2_font)
        chart_label2.setAlignment(Qt.AlignVCenter)
        chart_label2.setFixedWidth(50)
        chart2_layout = QHBoxLayout(self.chart_frame2)
        chart2_layout.addSpacing(10)
        chart2_layout.addWidget(chart_label2)
        self.chart_frame2.setFixedSize(self.middle_frame_width, 260)

        self.chart_frame2.setStyleSheet(frameStyleSheet)
        center_layout.addWidget(self.chart_frame2)

        # 创建一个 QLabel ，用来播放轨迹动画
        self.animation_QLabel = QLabel()
        # 轨迹动画尺寸调整***
        self.animation_QLabel.setFixedSize(920, 228)
        # 设置 QLabel 背景颜色
        self.animation_QLabel.setStyleSheet("background-color: white;")  # 设置背景色为 lightgray
        self.animation_QLabel.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明
        chart2_layout.addWidget(self.animation_QLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        chart2_layout.addStretch()

        # 创建一个QWidget()，用来显示 轨迹动画静态绘图（暂时屏蔽）
        '''
        self.animation_QWidget = QWidget()
        # 轨迹动画尺寸调整***
        self.animation_QWidget.setFixedSize(920, 228)
        # 设置 QWidget 背景颜色
        self.animation_QWidget.setStyleSheet("background-color: white;")  # 设置背景色为 lightgray
        self.animation_QWidget.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明
        # 创建MatplotlibWidget
        self.canvas_animation = MplCanvas(width=6, height=4)
        # 将绘图内容添加到QWidget中
        animation_QWidget_layout = QVBoxLayout(self.animation_QWidget)
        animation_QWidget_layout.addWidget(self.canvas_animation)
        chart2_layout.addWidget(self.animation_QWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        chart2_layout.addStretch()
        '''

        # self.animation_QLabel.setAlignment(Qt.AlignCenter)

        # # 初始加载第一个 GIF
        # self.movie = QMovie('donghua.gif')  # 替换为实际 GIF 文件路径
        # self.animation_QLabel.setMovie(self.movie)

        # 区域8 - 模式选择和方案选择
        self.calc_button_frame = QFrame()
        self.calc_button_frame.setContentsMargins(0, 0, 0, 0)
        calc_button_layout = QVBoxLayout(self.calc_button_frame)
        self.calc_button_frame.setFixedSize(self.middle_frame_width, 160)

        self.first_widget = QWidget()
        first_layout = QHBoxLayout(self.first_widget)
        self.first_widget.setFixedHeight(75)
        self.intelligent_search_mode = ImageChangeButton(self.tr("智能寻优模式"), ":MiddleFrame", ":MiddleFrameClicked", 200, 45)
        self.intelligent_search_mode.clicked.connect(self.switch_search_motion_param_intelligence_clicked)
        self.artificial_search_mode = ImageChangeButton(self.tr("方案验证模式"), ":MiddleFrame", ":MiddleFrameClicked", 200, 45)
        self.artificial_search_mode.clicked.connect(self.switch_search_motion_param_manual_clicked)
        self.save_button = ImageChangeButton(self.tr("参数保存"), ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        first_layout.addSpacerItem(QSpacerItem(136, 50, QSizePolicy.Expanding, QSizePolicy.Expanding))
        # first_layout.addWidget(QLabel(self.tr("模式\n选择"), styleSheet="font-size: 17px;width:10px"))
        self.mode_label = QLabel(self.tr("模式\n选择"))
        self.mode_label.setStyleSheet("font-size: 17px;")
        self.mode_label.setFixedWidth(59)  # 固定宽度为 100 像素
        self.mode_label.setAlignment(Qt.AlignCenter)  # 居中对齐
        first_layout.addWidget(self.mode_label)
        first_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Fixed, QSizePolicy.Expanding))
        first_layout.addWidget(self.intelligent_search_mode)
        first_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Fixed, QSizePolicy.Expanding))
        first_layout.addWidget(self.artificial_search_mode)
        first_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Fixed, QSizePolicy.Expanding))
        first_layout.addSpacerItem(QSpacerItem(50, 50, QSizePolicy.Fixed, QSizePolicy.Expanding))
        first_layout.addWidget(self.save_button)
        first_layout.addSpacerItem(QSpacerItem(61, 50, QSizePolicy.Fixed, QSizePolicy.Expanding))
        first_layout.addSpacerItem(QSpacerItem(61, 50, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.second_widget = QWidget()
        self.second_widget.setFixedHeight(75)
        second_layout = QHBoxLayout(self.second_widget)
        self.button_energy_project = ImageChangeButton(self.tr("节能方案"), ":GreenFrame", ":GreenFrameClicked", 200, 45, True)
        self.button_efficient_project = ImageChangeButton(self.tr("高品质方案"), ":GreenFrame", ":GreenFrameClicked", 200, 45, True)
        self.button_selfdefine_project = ImageChangeButton(self.tr("自定义修正方案"), ":GreenFrame", ":GreenFrameClicked", 200, 45, True)
        second_layout.addSpacerItem(QSpacerItem(136, 50, QSizePolicy.Expanding, QSizePolicy.Expanding))
        # second_layout.addWidget(QLabel(self.tr("方案\n选择"), styleSheet="font-size: 17px;"))
        self.scheme_label1 = QLabel(self.tr("方案\n选择"))
        self.scheme_label1.setStyleSheet("font-size: 17px;")
        self.scheme_label1.setFixedWidth(59)  # 固定宽度为 100 像素
        self.scheme_label1.setAlignment(Qt.AlignCenter)  # 居中对齐
        second_layout.addWidget(self.scheme_label1)
        second_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Fixed, QSizePolicy.Expanding))
        second_layout.addWidget(self.button_energy_project)
        second_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Fixed, QSizePolicy.Expanding))
        second_layout.addWidget(self.button_efficient_project)
        second_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Fixed, QSizePolicy.Expanding))
        second_layout.addWidget(self.button_selfdefine_project)
        second_layout.addSpacerItem(QSpacerItem(55, 50, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.third_widget = QWidget()
        self.third_widget.setFixedHeight(75)
        third_layout = QHBoxLayout(self.third_widget)
        self.button_synchronization_mode = ImageChangeButton(self.tr("同步摆动模式"), ":GreenFrame", ":GreenFrameClicked", 200, 45, True)
        self.button_cross_mode = ImageChangeButton(self.tr("交叉摆动模式"), ":GreenFrame", ":GreenFrameClicked", 200, 45, True)
        self.placeholder1 = QWidget()
        self.placeholder1.setFixedSize(206, 50)
        self.button_order_mode = ImageChangeButton(self.tr("顺序摆动模式"), ":GreenFrame", ":GreenFrameClicked", 200, 45, True)
        self.placeholder2 = QWidget()
        self.placeholder2.setFixedSize(206, 50)
        third_layout.addSpacerItem(QSpacerItem(136, 50, QSizePolicy.Expanding, QSizePolicy.Expanding))
        # third_layout.addWidget(QLabel(self.tr("方案\n选择"), styleSheet="font-size: 17px;"), alignment=Qt.AlignmentFlag.AlignLeft)
        self.scheme_label2 = QLabel(self.tr("方案\n选择"))
        self.scheme_label2.setStyleSheet("font-size: 17px;")
        self.scheme_label2.setFixedWidth(59)  # 固定宽度为 100 像素
        self.scheme_label2.setAlignment(Qt.AlignLeft)  # 左对齐
        third_layout.addWidget(self.scheme_label2, alignment=Qt.AlignmentFlag.AlignLeft)
        third_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Fixed, QSizePolicy.Expanding))
        third_layout.addWidget(self.button_synchronization_mode, alignment=Qt.AlignmentFlag.AlignLeft)
        third_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Fixed, QSizePolicy.Expanding))
        third_layout.addWidget(self.button_cross_mode)
        third_layout.addWidget(self.placeholder1)
        self.placeholder1.setVisible(False)
        third_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Fixed, QSizePolicy.Expanding))
        third_layout.addWidget(self.button_order_mode)
        third_layout.addWidget(self.placeholder2)
        self.placeholder2.setVisible(False)
        third_layout.addSpacerItem(QSpacerItem(55, 50, QSizePolicy.Expanding, QSizePolicy.Expanding))

        calc_button_layout.addWidget(self.first_widget)
        calc_button_layout.addWidget(self.second_widget)
        calc_button_layout.addWidget(self.third_widget)
        calc_button_layout.setContentsMargins(0, 0, 0, 0)
        self.calc_button_frame.setStyleSheet(frameStyleSheet)
        center_layout.addWidget(self.calc_button_frame)
        content_layout.addLayout(center_layout)

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        # 右侧布局(智能寻优模式)
        self.right_intelligent_search_mode_layout = QVBoxLayout()
        # 区域4 - 运动输入参数
        self.motion_in_param_frame = MotionInputParamWidget()
        # motion_in_param_layout = QVBoxLayout(self.motion_in_param_frame)
        self.motion_in_param_frame.setFixedWidth(self.right_frame_width - 5)
        self.motion_in_param_frame.setContentsMargins(30, 5, 30, self.margin_value)

        # 区域5 - 运动输出参数
        self.motion_out_param_frame = MotionOutputParamWidget()
        self.motion_out_param_frame.setFixedWidth(self.right_frame_width - 5)
        self.motion_out_param_frame.setContentsMargins(30, 5, 30, self.margin_value)

        self.right_intelligent_search_mode_layout.addWidget(self.motion_in_param_frame)
        self.right_intelligent_search_mode_layout.addWidget(self.motion_out_param_frame)
        self.right_intelligent_search_mode_layout.setContentsMargins(0, 0, 0, 0)

        self.combine_frame = QFrame()
        self.combine_frame.setFixedSize(410, 830)
        self.combine_frame.setContentsMargins(0, 0, 0, 0)
        self.combine_frame.setLayout(self.right_intelligent_search_mode_layout)

        # 运动参数-方案验证界面
        self.motion_input_out_param_manual_frame = MotionInputOutputParamCombineWidget()
        self.motion_input_out_param_manual_frame.setFixedSize(self.right_frame_width - 5, 825)
        self.motion_input_out_param_manual_frame.setContentsMargins(30, 0, 30, 0)

        # 右侧切换部分stacked_widget
        self.motion_param_stacked_widget.addWidget(self.combine_frame)
        self.motion_param_stacked_widget.addWidget(self.motion_input_out_param_manual_frame)
        right_layout.addWidget(self.motion_param_stacked_widget)
        content_layout.addLayout(right_layout)

        # 底部按钮区域布局
        bottom_layout = QHBoxLayout()
        # 添加中英文切换按钮
        self.translate_button = ImageChangeButton(self.tr("中文"), ":SmallFrame", ":SmallFrameClicked", 114, 37, True)
        bottom_layout.addWidget(self.translate_button, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.translate_button.clicked.connect(self.toggle_language)
        # 创建状态栏标签
        self.status_label = QLabel("")
        self.status_label.setFixedSize(699, 30)
        self.status_label.setStyleSheet("QLabel { text - align: center; }")
        # self.status_label.setStyleSheet("background: transparent;")
        self.status_label.setAttribute(Qt.WA_TranslucentBackground)
        self.status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        status_font = QFont("Microsoft YaHei", 16)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        self.status_label.setFont(status_font)

        # 在标签前添加拉伸
        bottom_layout.addSpacerItem(QSpacerItem(284, 60, QSizePolicy.Fixed, QSizePolicy.Fixed))
        bottom_layout.addSpacerItem(QSpacerItem(1, 60, QSizePolicy.Expanding, QSizePolicy.Fixed))

        # 添加status_label，但不指定对齐方式
        bottom_layout.addWidget(self.status_label, alignment=Qt.AlignRight | Qt.AlignBottom)

        # 在标签后添加拉伸使其居中
        # bottom_layout.addStretch()
        # 在标签前添加拉伸
        bottom_layout.addSpacerItem(QSpacerItem(50, 60, QSizePolicy.Expanding, QSizePolicy.Fixed))

        # 底部 - 输出报告按钮
        self.report_button = ImageChangeButton(self.tr("输出报告"), ":SmallFrame", ":SmallFrameClicked", 166, 37, True)
        # 新增“整线配置”按钮
        self.line_config_button = ImageChangeButton(self.tr("整线配置"), ":SmallFrame", ":SmallFrameClicked", 166, 37,
                                                    True)
        # 添加向右对齐的report_按钮
        bottom_layout.addWidget(self.report_button, alignment=Qt.AlignRight | Qt.AlignBottom)
        self.report_button.clicked.connect(self.open_new_window)

        # 新增：在两个按钮之间添加一个小的间隔
        bottom_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 新增：添加“整线配置”按钮
        bottom_layout.addWidget(self.line_config_button, alignment=Qt.AlignRight | Qt.AlignBottom)

        # 如果需要，在按钮后添加一个间隔符
        bottom_layout.addSpacerItem(QSpacerItem(170, 60, QSizePolicy.Fixed, QSizePolicy.Fixed))

        main_layout.addLayout(bottom_layout)

        # 设置各个组件的背景图片
        self.update_background_image()

        # 初始化界面值
        # self.setInitValues()

        # 定义状态文本列表
        self.current_text_index = 0

        self.button_energy_project.clicked.connect(self.start_calculation)
        self.button_efficient_project.clicked.connect(self.start_calculation)
        self.button_selfdefine_project.clicked.connect(self.start_calculation)
        # -------------------------按钮逻辑部分-------------------------

        self.button_synchronization_mode.clicked.connect(self.start_calculation)
        self.button_cross_mode.clicked.connect(self.start_calculation)
        self.button_order_mode.clicked.connect(self.start_calculation)

        self.setInitButtonClicked()

        # 界面输入框数据变动监控
        self.host_param_single_frame.content_layout.sig_textChanged.connect(self.on_host_param_single_changed)
        self.host_param_double_frame.content_layout.sig_textChanged.connect(self.on_host_param_double_changed)
        self.motion_in_param_frame.content_layout.sig_textChanged.connect(self.on_motion_input_intelligence_changed)
        self.motion_input_out_param_manual_frame.content_up_layout.sig_textChanged.connect(self.on_motion_input_manual_changed)

        # 绑定参数保存信号槽
        self.host_param_single_frame.sig_Saved.connect(self.on_host_param_single_saved)
        self.host_param_double_frame.sig_Saved.connect(self.on_host_param_double_saved)
        self.motion_in_param_frame.sig_Saved.connect(self.on_motion_param_intelligence_saved)
        self.motion_input_out_param_manual_frame.sig_Saved.connect(self.on_motion_param_manual_saved)
        # 设置主窗口布局
        self.setLayout(main_layout)
        self.third_widget.setVisible(False)
        self.showMaximized()
        print('Software loading succeeded!')

    # 切换中英文
    def toggle_language(self):
        if not self.is_english:
            # 切换到英文
            if self.translator.load("en_US.qm", ":/translations") or self.translator.load("en_US.qm", "./translations"):
                QApplication.instance().installTranslator(self.translator)
                self.is_english = True
                self.translate_button.setText(self.tr("English"))
            else:
                print("Failed to load en_US.qm")
        else:
            # 恢复中文
            QApplication.instance().removeTranslator(self.translator)
            self.is_english = False
            self.translate_button.setText(self.tr("中文"))

        # 触发语言变更事件，更新界面
        self.retranslate_ui()
        lang_change_event = QEvent(QEvent.LanguageChange)
        QApplication.instance().sendEvent(self, lang_change_event)

    # 动态更新界面文本 翻译 中英文切换
    def retranslate_ui(self):
        self.setWindowTitle(self.tr("抛光仿真系统"))
        self.device_mapping = {
            1: self.tr("单头摆"),
            2: self.tr("双头摆"),
            3: self.tr("同步摆")
        }
        self.mode_mapping = {
            1: self.tr("智能寻优模式"),
            2: self.tr("方案验证模式")
        }
        self.selection_mapping = {
            1: self.tr("节能方案"),
            2: self.tr("高品质方案"),
            3: self.tr("自定义修正方案"),
            4: self.tr("同步摆动模式"),
            5: self.tr("交叉摆动模式"),
            6: self.tr("顺序摆动模式")
        }
        self.swing_mode_mapping = {
            1: self.tr("顺序摆"),
            2: self.tr("顺序摆"),
            3: self.tr("顺序摆"),
            4: self.tr("同步摆"),
            5: self.tr("交叉摆"),
            6: self.tr("顺序摆")
        }
        # 更新版本号
        self.findChild(JustifiedLabel).setText(self.tr("版本号: KDUI-2401"))
        self.format_vertical_label(self.image_label, "机\n型\n图")
        # 更新轨迹分布
        self.format_vertical_label(self.chart_frame1.findChild(QLabel), "轨\n迹\n分\n布")

        # 更新轨迹动画
        self.format_vertical_label(self.chart_frame2.findChild(QLabel), "轨\n迹\n动\n画")

        # 更新模式选择
        # self.first_widget.findChild(QLabel).setText(self.tr("模式\n选择"))
        self.format_vertical_label(self.first_widget.findChild(QLabel), "模式\n选择")
        self.intelligent_search_mode.set_name(self.tr("智能寻优模式"))
        self.artificial_search_mode.set_name(self.tr("方案验证模式"))
        self.save_button.set_name(self.tr("参数保存"))
        # 更新方案选择
        self.format_vertical_label(self.second_widget.findChild(QLabel), "方案\n选择")
        self.button_energy_project.set_name(self.tr("节能方案"))
        self.button_efficient_project.set_name(self.tr("高品质方案"))
        self.button_selfdefine_project.set_name(self.tr("自定义修正方案"))
        # 更新第三区域方案选择
        self.format_vertical_label(self.third_widget.findChild(QLabel), "方案\n选择")
        self.button_synchronization_mode.set_name(self.tr("同步摆动模式"))
        self.button_cross_mode.set_name(self.tr("交叉摆动模式"))
        self.button_order_mode.set_name(self.tr("顺序摆动模式"))
        # 更新报告按钮
        self.report_button.set_name(self.tr("输出报告"))
        self.translate_button.set_name(self.tr("中文"))
        # 更新状态文本
        self.status_texts = self.get_current_device_mode_solution()
        self.showNormal()
        self.move(0, 0)
        self.showMaximized()

    def format_vertical_label(self, label, name):
        """
        为 QLabel 设置竖向排列文本，根据当前语言动态处理中英文。
        :param label: QLabel 对象，如 self.image_label
        """
        if not label:
            return
        # 获取标签当前文本作为翻译键
        current_text = label.text()
        if not current_text:
            return
        # 获取翻译文本
        text = self.tr(current_text)

        if self.is_english:
            # 按字符拆分英文
            # char_array = list(text)
            # text = "\n".join(char_array)  # 每个字符一行
            char_array = text.split()
            text = "\n".join(char_array)
        else:
            # 中文：使用映射中的带换行文本，fallback 到翻译文本
            text = self.tr(name)
        # 设置标签文本
        label.setText(text)

    # 获取当前设备、模式和方案的状态文本
    def get_current_device_mode_solution(self):
        return [
            self.tr("正在进行【{device}-{mode}-{solution}】计算，请稍后").format(
                device=self.device_mapping.get(self.current_device),
                mode=self.mode_mapping.get(self.current_mode),
                solution=self.selection_mapping.get(self.solution_selection)),
            self.tr("正在进行【{device}-{mode}-{solution}】计算，请稍后。").format(
                device=self.device_mapping.get(self.current_device),
                mode=self.mode_mapping.get(self.current_mode),
                solution=self.selection_mapping.get(self.solution_selection)),
            self.tr("正在进行【{device}-{mode}-{solution}】计算，请稍后。。").format(
                device=self.device_mapping.get(self.current_device),
                mode=self.mode_mapping.get(self.current_mode),
                solution=self.selection_mapping.get(self.solution_selection)),
            self.tr("正在进行【{device}-{mode}-{solution}】计算，请稍后。。。").format(
                device=self.device_mapping.get(self.current_device),
                mode=self.mode_mapping.get(self.current_mode),
                solution=self.selection_mapping.get(self.solution_selection))
        ]

    # 单头摆参数变化处理
    def on_host_param_single_changed(self, text):
        self.host_param_single_changed_flag = True

    # 双头摆参数变化处理
    def on_host_param_double_changed(self, text):
        self.host_param_double_changed_flag = True

    # 智能寻优模式输入参数变化处理
    def on_motion_input_intelligence_changed(self, text):
        self.motion_input_intelligence_changed_flag = True

    # 方案验证模式输入参数变化处理
    def on_motion_input_manual_changed(self, text):
        self.motion_input_manual_changed_flag = True

    # 单头摆参数保存处理
    def on_host_param_single_saved(self):
        self.host_param_single_changed_flag = False

    # 双头摆参数保存处理
    def on_host_param_double_saved(self):
        self.host_param_double_changed_flag = False

    # 智能寻优模式参数保存处理
    def on_motion_param_intelligence_saved(self):
        self.motion_input_intelligence_changed_flag = False

    # 方案验证模式参数保存处理
    def on_motion_param_manual_saved(self):
        self.motion_input_manual_changed_flag = False

    # 打开新窗口（输出报告）
    def open_new_window(self):
        # 动态传入过滤条件
        filter_condition = self.device_mapping.get(self.current_device)  # 这里可以根据需要动态获取过滤条件
        self.output_report.set_filter_condition(filter_condition)
        self.output_report.show()

    # 设置初始值
    def setInitValues(self):
        self.motion_in_param_frame.content_layout.set_line_edit_value('lineEdit_accelerate', '650')
        self.motion_in_param_frame.content_layout.set_line_edit_value('lineEdit_overlap', '10')

    # 设置初始按钮状态
    def setInitButtonClicked(self):
        self.intelligent_search_mode.init_clicked_background()
        self.intelligent_search_mode.is_clicked = True
        self.single_button.init_clicked_background()
        self.single_button.is_clicked = True
        # 初始化显示单头摆图片
        self.update_device_image()

    def set_frame_image(self, image_path):
        # 加载图片
        self.frame_image = QPixmap(image_path)
        # 设置背景
        self.update_frame_image()

    # 更新框架图片
    def update_frame_image(self):
        # 获取窗口大小
        window_size = self.chart_frame2.size()
        # 将图片缩放至窗口大小
        scaled_image = self.frame_image.scaled(window_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # 设置为窗口背景
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scaled_image))
        # self.chart_frame2.setPalette(palette)
        # self.chart_frame2.setAutoFillBackground(True)

    # 设置背景图片
    def set_background_image(self):

        # 主窗口背景
        # 设置背景图片路径
        self.background_image_path = ":background"
        self.background_image = QPixmap(self.background_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        window_size = self.size()
        scaled_image = self.background_image.scaled(window_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # 设置为窗口背景
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scaled_image))
        self.setPalette(palette)
        self.setAutoFillBackground(True)  # 确保背景填充

        # 单头摆/双头摆/同步摆设备选择
        # 设置背景图片路径
        # self.button_frame_image_path = ":SwingAndHostParameter"
        # self.button_frame_image = QPixmap(self.button_frame_image_path)
        # # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        # button_frame_size = self.button_frame.size()
        # scaled_image = self.button_frame_image.scaled(button_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # # 设置为窗口背景
        # palette1 = QPalette()
        # palette1.setBrush(QPalette.Window, QBrush(scaled_image))
        # self.button_frame.setPalette(palette1)
        # self.button_frame.setAutoFillBackground(True)

        # 机型图
        # 设置背景图片路径
        # self.image_frame_image_path = ":Machine"
        # self.image_frame_image = QPixmap(self.image_frame_image_path)
        # # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        # image_frame_size = self.image_frame.size()
        # scaled_image = self.image_frame_image.scaled(image_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # # 设置为窗口背景
        # palette2 = QPalette()
        # palette2.setBrush(QPalette.Window, QBrush(scaled_image))
        # self.image_frame.setPalette(palette2)
        # self.image_frame.setAutoFillBackground(True)

        # 主机参数-双头摆
        # 设置背景图片路径
        # self.host_param_frame_image = QPixmap(":SwingAndHostParameter")
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        # scaled_image = self.host_param_frame_image.scaled(self.host_param_double_frame.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # # 设置为窗口背景
        # host_palette = QPalette()
        # host_palette.setBrush(QPalette.Window, QBrush(scaled_image))

        # self.host_param_double_frame.setPalette(host_palette)
        # self.host_param_double_frame.setAutoFillBackground(True)

        # 主机参数-单头摆
        # 设置为窗口背景
        # self.host_param_single_frame.setPalette(host_palette)
        # self.host_param_single_frame.setAutoFillBackground(True)

        # 主机参数-同步摆
        # 设置为窗口背景
        # self.host_param_equal_frame.setPalette(host_palette)
        # self.host_param_equal_frame.setAutoFillBackground(True)

        # 轨迹分布
        # 设置背景图片路径
        # self.sim_image_path = ":Line"
        # self.sim_image = QPixmap(self.sim_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        # sim_frame_size = self.chart_frame1.size()
        # scaled_image = self.sim_image.scaled(sim_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # 设置为窗口背景
        # palette4 = QPalette()
        # palette4.setBrush(QPalette.Window, QBrush(scaled_image))
        # self.chart_frame1.setPalette(palette4)
        # self.chart_frame1.setAutoFillBackground(True)
        # self.chart_frame1.setStyleSheet(frameStyleSheet)
        # 轨迹动画
        # 设置背景图片路径
        # self.animation_image_path = ":Line"
        # self.animation_image = QPixmap(self.animation_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        # animation_frame_size = self.chart_frame2.size()
        # scaled_image = self.animation_image.scaled(animation_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # 设置为窗口背景
        # palette5 = QPalette()
        # palette5.setBrush(QPalette.Window, QBrush(scaled_image))
        # self.chart_frame2.setPalette(palette5)
        # self.chart_frame2.setAutoFillBackground(True)

        # 模式选择
        # 设置背景图片路径
        # self.animation_image_path = ":Select"
        # self.animation_image = QPixmap(self.animation_image_path)
        # # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        # animation_frame_size = self.calc_button_frame.size()
        # scaled_image = self.animation_image.scaled(animation_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # # 设置为窗口背景
        # palette6 = QPalette()
        # palette6.setBrush(QPalette.Window, QBrush(scaled_image))
        # self.calc_button_frame.setPalette(palette6)
        # self.calc_button_frame.setAutoFillBackground(True)

        # 运动输入参数
        # 设置背景图片路径
        self.motion_param_image_path = ":InputOutput"
        self.motion_param_image = QPixmap(self.motion_param_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        motion_in_param_frame_size = self.motion_in_param_frame.size()
        scaled_image = self.motion_param_image.scaled(motion_in_param_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # 设置为窗口背景
        palette7 = QPalette()
        palette7.setBrush(QPalette.Window, QBrush(scaled_image))
        self.motion_in_param_frame.setPalette(palette7)
        self.motion_in_param_frame.setAutoFillBackground(True)

        # 运动输出参数
        # 设置背景图片路径
        self.motion_out_param_image_path = ":InputOutput"
        self.motion_out_param_image = QPixmap(self.motion_out_param_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        calc_param_frame_size = self.motion_out_param_frame.size()
        scaled_image = self.motion_out_param_image.scaled(calc_param_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # 设置为窗口背景
        palette8 = QPalette()
        palette8.setBrush(QPalette.Window, QBrush(scaled_image))
        self.motion_out_param_frame.setPalette(palette8)
        self.motion_out_param_frame.setAutoFillBackground(True)

        # 运动参数-合并
        self.motion_input_out_param_manual_image_path = ":SimInputOutput"
        self.motion_input_out_param_manual_image = QPixmap(self.motion_input_out_param_manual_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        calc_param_frame_size = self.motion_input_out_param_manual_frame.size()
        scaled_image = self.motion_input_out_param_manual_image.scaled(calc_param_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # 设置为窗口背景
        palette9 = QPalette()
        palette9.setBrush(QPalette.Window, QBrush(scaled_image))
        self.motion_input_out_param_manual_frame.setPalette(palette9)
        self.motion_input_out_param_manual_frame.setAutoFillBackground(True)

    # 更新背景图片
    def update_background_image(self):
        # 更新背景图片的显示效果
        self.set_background_image()

    # 窗口大小调整事件
    def resizeEvent(self, event):
        # 窗口大小改变时更新背景图片
        self.update_background_image()

        # 继承父类的 resizeEvent
        super(MainWindow, self).resizeEvent(event)

    # 切换到单头摆
    def switch_motion_param_single_clicked(self):
        self.placeholder1.setVisible(False)
        self.placeholder2.setVisible(False)
        self.button_cross_mode.setVisible(True)
        self.button_order_mode.setVisible(True)
        self.double_button.reset_background()
        self.equal_button.reset_background()
        self.host_param_stacked_widget.setCurrentIndex(0)
        self.current_device = 1
        self.logger.log_multiple_params('info', ('current_mode', self.current_device))
        # 更新设备图片
        self.update_device_image()

    # 切换到双头摆
    def switch_motion_param_double_clicked(self):
        self.placeholder1.setVisible(False)
        self.placeholder2.setVisible(False)
        self.button_cross_mode.setVisible(True)
        self.button_order_mode.setVisible(True)
        self.single_button.reset_background()
        self.equal_button.reset_background()
        self.host_param_stacked_widget.setCurrentIndex(1)
        self.current_device = 2
        # 更新设备图片
        self.update_device_image()

    # 切换到同步摆
    def switch_motion_param_equal_clicked(self):
        self.button_cross_mode.setVisible(False)
        self.button_order_mode.setVisible(False)
        self.placeholder1.setVisible(True)
        self.placeholder2.setVisible(True)
        self.single_button.reset_background()
        self.double_button.reset_background()
        self.host_param_stacked_widget.setCurrentIndex(2)
        self.current_device = 3
        # 更新设备图片
        self.update_device_image()

    # 切换到智能寻优模式
    def switch_search_motion_param_intelligence_clicked(self):
        self.current_mode = 1
        self.artificial_search_mode.reset_background()
        self.third_widget.setVisible(False)
        self.second_widget.setVisible(True)
        self.motion_param_stacked_widget.setCurrentIndex(0)

    # 切换到方案验证模式
    def switch_search_motion_param_manual_clicked(self):
        self.current_mode = 2
        self.intelligent_search_mode.reset_background()
        self.second_widget.setVisible(False)
        self.third_widget.setVisible(True)
        self.motion_param_stacked_widget.setCurrentIndex(1)

    # 设置主参数框架可见性
    def set_main_param_frame_visible(self, visible):
        if visible:
            # 重新设置背景
            # 运动输入参数
            # 设置背景图片路径
            self.motion_param_image_path = ":InputOutput"
            self.motion_param_image = QPixmap(self.motion_param_image_path)
            # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
            motion_in_param_frame_size = self.motion_in_param_frame.size()
            scaled_image = self.motion_param_image.scaled(motion_in_param_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            palette5 = QPalette()
            palette5.setBrush(QPalette.Window, QBrush(scaled_image))
            self.motion_in_param_frame.setPalette(palette5)
            self.motion_in_param_frame.setAutoFillBackground(True)
        else:
            # 移除背景

            self.motion_in_param_frame.setPalette(QPalette())
            self.motion_in_param_frame.setAutoFillBackground(False)

        # 设置可见性
        self.motion_in_param_frame.setVisible(visible)

    # 更新状态栏
    def update_status(self):
        # self.status_texts = ["正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。", "正在进行【"+self.device_mapping.get(self.current_device)+"-"+self.mode_mapping.get(self.current_mode)+"-"+self.selection_mapping.get(self.solution_selection)+"】计算，请稍后。。。"]

        self.status_label.setText(self.status_texts[self.current_text_index])
        self.current_text_index = (self.current_text_index + 1) % len(self.status_texts)

    # 开始计算
    def start_calculation(self):
        self.timer.start(500)  # 每秒触发一次

    # 显示消息框
    def show_message(self, text):
        # 创建消息框
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(self.tr("提示"))
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.button(QMessageBox.Ok).setText(self.tr("确认"))
        msg_box.exec()

    # 检查并创建动画文件夹
    def check_and_create_folder(self):
        # 获取程序所在的根目录路径
        # base_path = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.dirname(sys.executable)
        print(base_path)
        exe_dir = self.get_exe_directory()
        print(f"当前程序所在的目录是: {exe_dir}")
        base_path = exe_dir
        # 定义文件夹路径
        folder_path = os.path.join(base_path, "animation")

        # 判断文件夹是否存在
        if not os.path.exists(folder_path):
            try:
                # 创建文件夹
                os.makedirs(folder_path)
                print(f"文件夹 '{folder_path}' 已创建。")
            except Exception as e:
                print(f"无法创建文件夹 '{folder_path}'，错误信息：{e}")
        # else:

        # print(f"文件夹'{folder_path}' 已存在。")

    # 获取可执行文件目录
    def get_exe_directory(self):
        if 'PYCHARM_HOSTED' in os.environ:
            # 如果是 PyCharm 中运行
            return os.path.dirname(os.path.abspath(__file__))
        else:
            # 其他情况（如命令行运行）
            return os.path.dirname(sys.executable)

    # 检查是否以管理员权限运行
    def is_admin(self):
        """
        检查当前程序是否以管理员权限运行
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    # 检查是否在 PyCharm 中运行
    def is_running_in_pycharm(self):
        """
        检查当前程序是否在 PyCharm 中运行
        """
        # 检查是否存在 PyCharm 相关的环境变量或命令行参数
        if "PYCHARM_HOSTED" in os.environ:  # PyCharm 的环境变量
            return True
        if "pycharm" in sys.executable.lower():  # 检查 Python 解释器路径
            return True
        return False

    # 以管理员权限重新运行
    def run_as_admin(self):
        """
        以管理员权限重新运行程序
        """
        script = sys.argv[0]
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)

    # 添加更新设备图片的方法
    def update_device_image(self):
        # 获取当前设备的图片路径
        image_path = self.device_image_mapping.get(self.current_device)
        # if image_path and os.path.exists(image_path):
        # 加载图片
        pixmap = QPixmap(image_path)
        # 获取图片标签的固定大小
        label_size = self.device_image_label.size()
        # 缩放图片以适应标签大小，保持纵横比
        scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # 设置图片
        self.device_image_label.setPixmap(scaled_pixmap)
        # else:
        #     print(f"图片路径不存在: {image_path}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    window.show()
    app.exec()
