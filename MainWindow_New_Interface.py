from PySide6.QtGui import QPainter, QPixmap, QColor, QPalette, QBrush, QFont
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, \
    QLineEdit, QFrame, QSizePolicy, QSpacerItem, QStackedWidget, QScrollArea
from PySide6.QtCore import Qt, QSize

from HostParamDoubleWidget import HostParamDoubleWidget
from HostParamSingleWidget import HostParamSingleWidget
from ImageButton import ImageButton
from ImageChangeButton import ImageChangeButton
from ImageChangeWithTextButton import ImageChangeWithTextButton
from MotionInputOutputParamCombineWidget import MotionInputOutputParamCombineWidget
from MotionInputParamWidget import MotionInputParamWidget
from MotionOutputParamWidget import MotionOutputParamWidget
from TitleBar import TitleBar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtGui import QColor

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=12, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.margin_value = 15
        self.flag = False

        self.selectedFunction = 1

        self.left_frame_width = 410
        self.right_frame_width = 410
        self.setWindowTitle("抛光参数计算系统")
        self.setStyleSheet("color: white;")
        # 模式切换标签    1：单头摆  2：双头摆  3：同步摆
        self.current_mode = 1
        # self.setAttribute(Qt.WA_TranslucentBackground)# 设置窗口背景透明

        # 创建 QStackedWidget
        self.host_param_stacked_widget = QStackedWidget()
        self.host_param_stacked_widget.setFixedSize(self.left_frame_width,310)

        # 创建 QStackedWidget
        self.motion_param_stacked_widget = QStackedWidget()
        self.motion_param_stacked_widget.setFixedWidth(420)

        # 初始窗口大小
        self.resize(1560, 540)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(0)

        global_layout = QVBoxLayout()
        global_layout.addSpacerItem(QSpacerItem(500,100,QSizePolicy.Expanding, QSizePolicy.Fixed))
        # 内容区域布局
        content_layout = QHBoxLayout()
        global_layout.addLayout(content_layout)
        main_layout.addLayout(global_layout)

        # 左侧布局
        left_layout = QVBoxLayout()
        # 区域1 - 三个按钮

        # 机型选择按钮区域
        self.button_frame = QFrame()
        self.button_frame.setFixedWidth(self.left_frame_width)
        self.button_frame.setContentsMargins(self.margin_value,self.margin_value,self.margin_value,self.margin_value)
        button_layout = QVBoxLayout(self.button_frame)
        self.single_button = ImageChangeButton("",":Single",":SingleClicked",315,74)
        # 单头摆模式切换
        self.single_button.clicked.connect(self.switch_motion_param_single_frame)
        self.double_button = ImageChangeButton("",":Double",":DoubleClicked",315,74)
        # 双头摆模式切换
        self.double_button.clicked.connect(self.switch_motion_param_double_frame)

        self.equal_button = ImageChangeButton("",":Equal",":EqualClicked",315,74)

        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.single_button)
        button_layout.addSpacerItem(QSpacerItem(315,10,QSizePolicy.Fixed,QSizePolicy.Fixed))
        button_layout.addWidget(self.double_button)
        button_layout.addSpacerItem(QSpacerItem(315,10,QSizePolicy.Fixed,QSizePolicy.Fixed))
        button_layout.addWidget(self.equal_button)

        left_layout.addWidget(self.button_frame)

        # 区域2 - 图片位置
        self.image_frame = QFrame()
        self.image_frame.setFixedWidth(self.left_frame_width)
        self.image_frame.setContentsMargins(self.margin_value,5,self.margin_value,self.margin_value)
        image_layout = QVBoxLayout(self.image_frame)
        image_label = QLabel("机型图")
        # 设置字体大小和字体类型
        image_font = QFont("Microsoft YaHei", 18)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        image_label.setFont(image_font)
        image_layout.addWidget(image_label)
        image_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        left_layout.addWidget(self.image_frame)


        # 区域3 - 主机参数(双头摆)
        self.host_param_double_frame = HostParamDoubleWidget()
        # self.main_param_frame.setFrameShape(QFrame.Box)
        self.host_param_double_frame.setFixedSize(self.left_frame_width,310)
        self.host_param_double_frame.setContentsMargins(self.margin_value, 5, self.margin_value, self.margin_value)
        # main_param_layout = QVBoxLayout(self.main_param_frame)

        # param_label = QLabel("主机参数")
        # # 设置字体大小和字体类型
        # param_font = QFont("Microsoft YaHei", 18)  # "Microsoft YaHei" 为字体类型，18 为字体大小
        # param_label.setFont(param_font)
        # main_param_layout.addWidget(param_label)
        # param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # for i in range(4):
        #     param_label = QLabel(f"主机参数{i + 1}")
        #     param_edit = QLineEdit()
        #     param_layout = QHBoxLayout()
        #     param_layout.addWidget(param_label)
        #     param_layout.addWidget(param_edit)
        #     main_param_layout.addLayout(param_layout)

        # 区域3 - 主机参数(单头摆)
        self.host_param_single_frame = HostParamSingleWidget()
        # self.main_param_frame.setFrameShape(QFrame.Box)
        self.host_param_single_frame.setFixedSize(self.left_frame_width,310)
        self.host_param_single_frame.setContentsMargins(self.margin_value, 5, self.margin_value, self.margin_value)


        self.host_param_stacked_widget.addWidget(self.host_param_single_frame)
        self.host_param_stacked_widget.addWidget(self.host_param_double_frame)
        left_layout.addWidget(self.host_param_stacked_widget)

        content_layout.addLayout(left_layout)

        # 中间布局
        center_layout = QVBoxLayout()

        # 区域6 - 轨迹分布
        self.chart_frame1 = QFrame()
        chart1_layout = QVBoxLayout(self.chart_frame1)
        self.chart_frame1.setContentsMargins(self.margin_value,5,self.margin_value,self.margin_value)

        chart_label1 = QLabel("轨迹分布")
        chart1_font = QFont("Microsoft YaHei",18)
        chart_label1.setFont(chart1_font)
        chart1_layout.addWidget(chart_label1)
        chart_label1.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.chart_frame1.setFixedHeight(300)
        center_layout.addWidget(self.chart_frame1)

        # 创建一个QWidget作为图框--轨迹分布
        self.central_widget = QWidget()
        #self.central_widget.setStyleSheet("border: 2px solid skyblue;border-radius: 10px")  # 设置边框为红色，宽度为3px
        self.central_widget.setStyleSheet("""
                                    QWidget {
                                        border: 2px solid white;
                                        border-radius: 10px;
                                    }
                                """)
        layout_widget = QVBoxLayout(self.central_widget)
        self.canvas = MplCanvas(self, width=8, height=4, dpi=100)

        deep_blue = (31/255, 55/255, 96/255)
        self.canvas.figure.set_facecolor(deep_blue)  # 设置画布背景颜色为底色

        # 创建拖动条
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(False)  # 强制显示拖动条

        # 自定义滚动条样式
        scroll_area.verticalScrollBar().setStyleSheet("""
                    QScrollBar:vertical {
                        border: 1px solid #999999;
                        border-radius: 10px;
                        background: #f0f0f0;
                        width: 16px;
                        margin: 16px 0 16px 0;
                    }
                    QScrollBar::handle:vertical {
                        background: #5d99c6;
                        min-height: 20px;
                        border-radius: 8px;
                    }
                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                        background: none;
                        height: 0px;
                    }
                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                        background: #e0e0e0;
                    }
                """)

        scroll_area.horizontalScrollBar().setStyleSheet("""
                    QScrollBar:horizontal {
                        border: 1px solid #999999;
                        border-radius: 10px;
                        background: #f0f0f0;
                        height: 16px;
                        margin: 0px 16px 0px 16px;
                    }
                    QScrollBar::handle:horizontal {
                        background: #5d99c6;
                        min-width: 20px;
                        border-radius: 8px;
                    }
                    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                        background: none;
                        width: 0px;
                    }
                    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                        background: #e0e0e0;
                    }
                """)

        scroll_area.setWidget(self.canvas)
        # 将拖动条加入widget中
        layout_widget.addWidget(scroll_area)
        # 将widget加入QFrame中
        chart1_layout.addWidget(self.central_widget)

        # 区域7 - 轨迹动画
        self.chart_frame2 = QFrame()
        self.chart_frame2.setContentsMargins(self.margin_value,5,self.margin_value,self.margin_value)
        chart_label2 = QLabel("轨迹动画")
        chart2_font = QFont("Microsoft YaHei",18)
        chart_label2.setFont(chart2_font)
        chart_label2.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        chart2_layout = QVBoxLayout(self.chart_frame2)
        chart2_layout.addWidget(chart_label2)
        self.chart_frame2.setFixedHeight(300)
        center_layout.addWidget(self.chart_frame2)

        # 区域8 - 计算模式按钮
        self.calc_button_frame = QFrame()
        self.calc_button_frame.setContentsMargins(self.margin_value,self.margin_value,self.margin_value,self.margin_value)
        calc_button_layout = QVBoxLayout(self.calc_button_frame)

        self.first_widget = QWidget()
        first_layout = QHBoxLayout(self.first_widget)
        self.intelligent_search_mode = ImageChangeButton("智能寻优模式",":MiddleFrame",":MiddleFrameCliecked",236,56)
        self.intelligent_search_mode.clicked.connect(self.switch_search_motion_param_intelligence_frame)
        self.artificial_search_mode = ImageChangeButton("人工寻优模式",":MiddleFrame",":MiddleFrameCliecked",236,56)
        self.artificial_search_mode.clicked.connect(self.switch_search_motion_param_manual_frame)
        self.save_button = ImageChangeButton("参数保存",":SmallFrame",":SmallFrameCliecked",114,37)
        first_layout.addWidget(self.intelligent_search_mode)
        first_layout.addWidget(self.artificial_search_mode)
        first_layout.addWidget(self.save_button)

        self.second_widget = QWidget()
        second_layout = QHBoxLayout(self.second_widget)
        self.button_energy_project = ImageChangeButton("节能方案", ":GreenFrame", ":GreenFrameCliecked",
                                    236,56)
        self.button_efficient_project = ImageChangeButton("高品质方案", ":GreenFrame", ":GreenFrameCliecked",
                                    236,56)
        self.button_selfdefine_project = ImageChangeButton("自定义修正方案", ":GreenFrame", ":GreenFrameCliecked",236,56)
        second_layout.addWidget(self.button_energy_project)
        second_layout.addWidget(self.button_efficient_project)
        second_layout.addWidget(self.button_selfdefine_project)

        self.third_widget = QWidget()
        third_layout = QHBoxLayout(self.third_widget)
        self.button_synchronization_mode = ImageChangeButton("同步摆动模式", ":GreenFrame", ":GreenFrameCliecked",
                                                       236, 56)
        self.button_cross_mode = ImageChangeButton("交叉摆动模式", ":GreenFrame", ":GreenFrameCliecked",
                                                          236, 56)
        self.button_order_mode = ImageChangeButton("顺序摆动模式", ":GreenFrame", ":GreenFrameCliecked", 236,
                                                           56)
        third_layout.addWidget(self.button_synchronization_mode)
        third_layout.addWidget(self.button_cross_mode)
        third_layout.addWidget(self.button_order_mode)



        calc_button_layout.addWidget(self.first_widget)
        calc_button_layout.addWidget(self.second_widget)
        calc_button_layout.addWidget(self.third_widget)
        # for i in range(3):
        #     calc_button = QPushButton("高效计算")
        #     calc_button_layout.addWidget(calc_button)

        center_layout.addWidget(self.calc_button_frame)

        content_layout.addLayout(center_layout)




        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0,0,0,0)
        # 右侧布局(智能寻优模式)
        self.right_intelligent_search_mode_layout = QVBoxLayout()
        # 区域4 - 运动输入参数
        self.motion_in_param_frame = MotionInputParamWidget()
        motion_in_param_layout = QVBoxLayout(self.motion_in_param_frame)
        # motion_in_param_label = QLabel("运动输入参数")
        # motion_in_param_layout.addWidget(motion_in_param_label)
        # motion_in_font = QFont("Microsoft YaHei",18)
        # motion_in_param_label.setFont(motion_in_font)
        # motion_in_param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.motion_in_param_frame.setFixedWidth(self.right_frame_width)
        self.motion_in_param_frame.setContentsMargins(self.margin_value,5,self.margin_value,self.margin_value)

        # for i in range(4):
        #     param_label = QLabel(f"运动参数{i + 1}")
        #     param_edit = QLineEdit()
        #     param_layout = QHBoxLayout()
        #     param_layout.addWidget(param_label)
        #     param_layout.addWidget(param_edit)
        #     motion_in_param_layout.addLayout(param_layout)

        # right_layout.addWidget(self.motion_in_param_frame)

        # 区域5 - 运动输出参数
        self.motion_out_param_frame = MotionOutputParamWidget()
        self.motion_out_param_frame.setFixedWidth(self.right_frame_width)
        self.motion_out_param_frame.setContentsMargins(self.margin_value,5,self.margin_value,self.margin_value)
        # motion_out_param_layout = QVBoxLayout(self.motion_out_param_frame)
        # motion_out_param_label = QLabel("运动输出参数")
        # motion_out_param_layout.addWidget(motion_out_param_label)
        # motion_out_font = QFont("Microsoft YaHei",18)
        # motion_out_param_label.setFont(motion_out_font)
        # motion_out_param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # product_quality_param_label = QLabel("产品质量参数")
        # motion_out_param_layout.addWidget(product_quality_param_label)
        # product_quality_font = QFont("Microsoft YaHei", 18)
        # product_quality_param_label.setFont(product_quality_font)
        # product_quality_param_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)


        # for i in range(4):
        #     param_label = QLabel(f"计算参数{i + 1}")
        #     param_edit = QLineEdit()
        #     param_layout = QHBoxLayout()
        #     param_layout.addWidget(param_label)
        #     param_layout.addWidget(param_edit)
        #     motion_out_param_layout.addLayout(param_layout)

        # right_layout.addWidget(self.motion_out_param_frame)

        self.right_intelligent_search_mode_layout.addWidget(self.motion_in_param_frame)
        self.right_intelligent_search_mode_layout.addWidget(self.motion_out_param_frame)

        self.combine_frame = QFrame()
        self.combine_frame.setLayout(self.right_intelligent_search_mode_layout)



        # 运动参数-人工寻优模式
        self.motion_input_out_param_manual_frame = MotionInputOutputParamCombineWidget()

        self.motion_input_out_param_manual_frame.setFixedSize(self.right_frame_width,830)

        # 右侧切换部分
        self.motion_param_stacked_widget.addWidget(self.combine_frame)
        self.motion_param_stacked_widget.addWidget(self.motion_input_out_param_manual_frame)
        right_layout.addWidget(self.motion_param_stacked_widget)

        content_layout.addLayout(right_layout)

        # 底部按钮区域布局
        bottom_layout = QHBoxLayout()

        # 底部 - 输出报告按钮
        report_button = ImageChangeWithTextButton("输出报告",":SmallFrame",":SmallFrameCliecked",73,64)

        # report_button = QPushButton("输出报告")
        report_button.setFixedHeight(50)
        bottom_layout.addWidget(report_button, alignment=Qt.AlignRight)
        bottom_layout.addSpacerItem(QSpacerItem(100,60,QSizePolicy.Fixed, QSizePolicy.Fixed))

        main_layout.addLayout(bottom_layout)

        # 设置各个组件的背景图片
        self.update_background_image()

        # 设置主窗口布局
        self.setLayout(main_layout)

        self.third_widget.setVisible(False)
        self.showMaximized()

    def set_frame_image(self, image_path):
        # 加载图片
        self.frame_image = QPixmap(image_path)
        # 设置背景
        self.update_frame_image()

    def update_frame_image(self):
        # 获取窗口大小
        window_size = self.chart_frame2.size()
        # 将图片缩放至窗口大小
        scaled_image = self.frame_image.scaled(window_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # 设置为窗口背景
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scaled_image))
        self.chart_frame2.setPalette(palette)
        self.chart_frame2.setAutoFillBackground(True)


    def set_background_image(self):
        # 主窗口背景AAAAAAAAAAAAA
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
        # self.setAutoFillBackground(True)  # 确保背景填充


        # 单头摆/双头摆/同步摆设备选择AAAAAAAAAAAAAAAAAA
        # 设置背景图片路径
        self.button_frame_image_path = ":SwingAndHostParameter"
        self.button_frame_image = QPixmap(self.button_frame_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        button_frame_size = self.button_frame.size()
        scaled_image = self.button_frame_image.scaled(button_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # 设置为窗口背景
        palette1 = QPalette()
        palette1.setBrush(QPalette.Window, QBrush(scaled_image))
        self.button_frame.setPalette(palette1)
        self.button_frame.setAutoFillBackground(True)

        # 机型图AAAAAAAAAAAAAAAAAA
        # 设置背景图片路径
        self.image_frame_image_path = ":Machine"
        self.image_frame_image = QPixmap(self.image_frame_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        image_frame_size = self.image_frame.size()
        scaled_image = self.image_frame_image.scaled(image_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # 设置为窗口背景
        palette2 = QPalette()
        palette2.setBrush(QPalette.Window, QBrush(scaled_image))
        self.image_frame.setPalette(palette2)
        self.image_frame.setAutoFillBackground(True)

        # 主机参数-双头摆AAAAAAAAAAAAAAAAAAAAA
        # 设置背景图片路径
        self.main_param_frame_image_path = ":SwingAndHostParameter"
        self.main_param_frame_image = QPixmap(self.main_param_frame_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        main_param_frame_size = self.host_param_double_frame.size()
        scaled_image = self.main_param_frame_image.scaled(main_param_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # 设置为窗口背景
        palette3 = QPalette()
        palette3.setBrush(QPalette.Window, QBrush(scaled_image))
        self.host_param_double_frame.setPalette(palette3)
        self.host_param_double_frame.setAutoFillBackground(True)

        # 主机参数-单头摆AAAAAAAAAAAAAAAAAAAAA
        # 设置背景图片路径
        self.main_param_frame_image_path = ":SwingAndHostParameter"
        self.main_param_frame_image = QPixmap(self.main_param_frame_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        main_param_frame_size = self.host_param_single_frame.size()
        scaled_image = self.main_param_frame_image.scaled(main_param_frame_size, Qt.IgnoreAspectRatio,
                                                          Qt.SmoothTransformation)
        # 设置为窗口背景
        palette3 = QPalette()
        palette3.setBrush(QPalette.Window, QBrush(scaled_image))
        self.host_param_single_frame.setPalette(palette3)
        self.host_param_single_frame.setAutoFillBackground(True)

        # 轨迹分布AAAAAAAAAAAAAA
        # 设置背景图片路径
        self.sim_image_path = ":Line"
        self.sim_image = QPixmap(self.sim_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        sim_frame_size = self.chart_frame1.size()
        scaled_image = self.sim_image.scaled(sim_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # 设置为窗口背景
        palette4 = QPalette()
        palette4.setBrush(QPalette.Window, QBrush(scaled_image))
        self.chart_frame1.setPalette(palette4)
        self.chart_frame1.setAutoFillBackground(True)

        # 轨迹动画AAAAAAAAAAAAAA
        # 设置背景图片路径
        self.animation_image_path = ":Line"
        self.animation_image = QPixmap(self.animation_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        animation_frame_size = self.chart_frame2.size()
        scaled_image = self.animation_image.scaled(animation_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # 设置为窗口背景
        palette5 = QPalette()
        palette5.setBrush(QPalette.Window, QBrush(scaled_image))
        self.chart_frame2.setPalette(palette5)
        self.chart_frame2.setAutoFillBackground(True)

        # 模式选择AAAAAAAAAAAAAA
        # 设置背景图片路径
        self.animation_image_path = ":Select"
        self.animation_image = QPixmap(self.animation_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        animation_frame_size = self.calc_button_frame.size()
        scaled_image = self.animation_image.scaled(animation_frame_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # 设置为窗口背景
        palette6 = QPalette()
        palette6.setBrush(QPalette.Window, QBrush(scaled_image))
        self.calc_button_frame.setPalette(palette6)
        self.calc_button_frame.setAutoFillBackground(True)


        # 运动输入参数AAAAAAAAAAAAAA
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



        # 运动输出参数AAAAAAAAAAAAAA
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

        # 运动参数-合并AAAAAAAAAAAAA

        self.motion_input_out_param_manual_image_path = ":SimInputOutput"
        self.motion_input_out_param_manual_image = QPixmap(self.motion_input_out_param_manual_image_path)
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        calc_param_frame_size = self.motion_input_out_param_manual_frame.size()
        scaled_image = self.motion_input_out_param_manual_image.scaled(calc_param_frame_size, Qt.IgnoreAspectRatio,
                                                          Qt.SmoothTransformation)
        # 设置为窗口背景
        palette9 = QPalette()
        palette9.setBrush(QPalette.Window, QBrush(scaled_image))
        self.motion_input_out_param_manual_frame.setPalette(palette9)
        self.motion_input_out_param_manual_frame.setAutoFillBackground(True)

    def update_background_image(self):
        # 更新背景图片的显示效果
        self.set_background_image()

    def resizeEvent(self, event):
        # 窗口大小改变时更新背景图片
        self.update_background_image()

        # 继承父类的 resizeEvent
        super(MainWindow, self).resizeEvent(event)

    def switch_motion_param_single_frame(self):
        self.host_param_stacked_widget.setCurrentIndex(0);
        self.current_mode = 1

    def switch_motion_param_double_frame(self):
        self.host_param_stacked_widget.setCurrentIndex(1);
        self.current_mode = 2

    def switch_search_motion_param_intelligence_frame(self):
        self.second_widget.setVisible(True)
        self.third_widget.setVisible(False)
        self.motion_param_stacked_widget.setCurrentIndex(0);

    def switch_search_motion_param_manual_frame(self):
        self.second_widget.setVisible(False)
        self.third_widget.setVisible(True)
        self.motion_param_stacked_widget.setCurrentIndex(1);

    def set_main_param_frame_visible(self, visible):
        if visible:
            # 重新设置背景
            # 运动输入参数AAAAAAAAAAAAAA
            # 设置背景图片路径
            self.motion_param_image_path = ":InputOutput"
            self.motion_param_image = QPixmap(self.motion_param_image_path)
            # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
            motion_in_param_frame_size = self.motion_in_param_frame.size()
            scaled_image = self.motion_param_image.scaled(motion_in_param_frame_size, Qt.IgnoreAspectRatio,
                                                          Qt.SmoothTransformation)
            # 设置为窗口背景
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


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    window.show()
    app.exec()
