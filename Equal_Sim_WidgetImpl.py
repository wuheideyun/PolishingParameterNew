import math

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtWidgets import QWidget, QLabel
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import Equal_Sim
from Equal_Sim_Generate_Animation import Animation_produce
from Equal_Sim_Middle_Line_Plot import middle_line_plot
from Equal_Sim_Polishing_Distribution_Simulation import Polishing_distribution_Thread


class EqualSimWidgetImpl(QWidget, Equal_Sim.Ui_MainWindow):
    def __init__(self, w):
        super().__init__()
        self.setupUi(w)

        self.setAttribute(Qt.WA_StyledBackground)  # 禁止父窗口样式影响子控件样式

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

        # self.simulation_button.setText("开始翻译")
        # self.simulation_button.setFixedSize(100, 32)
        # self.simulation_button.clicked.connect(self.onStartTrans)

        # 运行逻辑
        # 按钮操作
        self.animation_button.clicked.connect(self.start_computation_trajectory_animation)  # 动画按钮
        self.simulation_button.clicked.connect(self.start_computation_Polishing_distribution)  # 抛磨量分布仿真按钮
        self.middle_line_button.clicked.connect(self.middle_line_figure_plot)  # 磨头中心线绘制按钮
        # 在程序中创建一个显示图框 播放gif动画
        self.gif_label = QLabel(self.widget)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 调整gif_label的大小以适应widget
        self.gif_label.resize(self.widget.size())
        # 确保gif_label随widget大小变化而变化
        self.widget.resizeEvent = self.resize_event

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

        self.animation_button.setStyleSheet(qss_Button)
        self.middle_line_button.setStyleSheet(qss_Button)
        self.simulation_button.setStyleSheet(qss_Button)

    # 抛磨量分布仿真子线程
    def start_computation_Polishing_distribution(self):      # 抛磨量分布仿真子线程
        # 创建子线程
        self.Polishing_distribution_thread = Polishing_distribution_Thread(float(self.belt_speed.text()),
                                                                           float(self.beam_speed.text()),
                                                                           float(self.constant_time.text()),
                                                                           float(self.stay_time.text()),
                                                                           float(self.a_speed.text()),
                                                                           float(self.between.text()),
                                                                           math.ceil(float(self.num.text())),
                                                                           float(self.radius.text()),
                                                                           float(self.grind_size.text()))
        self.Polishing_distribution_thread.result_ready.connect(self.Polishing_distribution_ready)
        self.simulation_button.setEnabled(False)
        # 运行子线程
        self.Polishing_distribution_thread.start()
    def Polishing_distribution_ready(self,object_matrix, result):     # 子线程回调函数
        # 在主线程中绘图
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置微软雅黑字体
        plt.rcParams['axes.unicode_minus'] = False  # 避免坐标轴不能正常的显示负号
        fig = plt.figure('抛磨强度分布仿真')
        ax = fig.add_subplot(111)
        ax.set_aspect('equal', adjustable='box')
        #plt.gca().set_aspect(1)  # x、y轴等刻度
        im = ax.contourf(object_matrix, 15, alpha=1, cmap='jet')
        plt.xlabel('Tile feed direction')
        plt.ylabel('Beam swing direction')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        plt.colorbar(im, cax=cax)
        plt.show()  # 显示函数图像
        self.equal_coefficient.setText(result)
        self.simulation_button.setEnabled(True)
    # 轨迹动画生成子线程
    def start_computation_trajectory_animation(self):
        self.trajectory_animation_thread = Animation_produce(float(self.belt_speed.text()),
                                                            float(self.beam_speed.text()),
                                                            float(self.constant_time.text()),
                                                            float(self.stay_time.text()),
                                                            float(self.a_speed.text()),
                                                            float(self.radius.text()),
                                                            float(self.between.text()),
                                                            math.ceil(float(self.num.text()))
                                                            )
        self.trajectory_animation_thread.result_ready.connect(self.trajectory_animation_ready)
        self.animation_button.setEnabled(False)
        # 运行子线程
        self.trajectory_animation_thread.start()
    def trajectory_animation_ready(self,str_222):
        # 加载GIF动画
        print(str_222)
        self.movie = QMovie("./animation.gif")
        #self.movie.setloopCount(1)  # 设置只播放一次
        self.gif_label.setMovie(self.movie)
        self.movie.start()
        self.animation_button.setEnabled(True)
    # 调整动画在界面图框中的位置
    def resize_event(self, event):
        self.gif_label.resize(event.size())
    # 绘制磨头中心轨迹线
    def middle_line_figure_plot(self):
        belt_speed=float(self.belt_speed.text())
        beam_speed=float(self.beam_speed.text())
        constant_time=float(self.constant_time.text())
        stay_time=float(self.stay_time.text())
        a_speed=float(self.a_speed.text())
        num=math.ceil(float(self.num.text()))
        between=float(self.between.text())
        mid_var=middle_line_plot(belt_speed,beam_speed,constant_time,stay_time,a_speed,num,between)
        mid_var.figure_plot()