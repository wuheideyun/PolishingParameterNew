import math

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtWidgets import QWidget, QLabel
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import Single_Calc
import Single_Calc_Parameter_Calculate
from Single_Calc_Generate_Animation import Animation_produce_order
from Single_Calc_Middle_Line_Plot import middle_line_plot_order, middle_line_plot_self_define_order
from Single_Calc_Polishing_Distribution_Simulation import Polishing_distribution_Thread_order, \
    Polishing_distribution_Thread_order_unequal
from Single_Calc_Self_Define_Calculate import self_define_calculate


class SingleCalcWidgetImpl(QWidget, Single_Calc.Ui_MainWindow):
    def __init__(self, w):
        super().__init__()
        self.setupUi(w)

        self.setAttribute(Qt.WA_StyledBackground)  # 禁止父窗口样式影响子控件样式

        # 运行逻辑
        # 按钮操作
        self.button_energy_calculate.clicked.connect(self.energy_calculate)  # 节能计算
        self.button_efficient_calculate.clicked.connect(self.efficient_calculate)  # 高效计算
        self.button_selfdefine_calculate.clicked.connect(self.define_calculate)  # 自定义计算计算
        # 动画按钮(顺序摆动画)
        self.button_animation_order.clicked.connect(self.start_computation_trajectory_animation_order)
        # 动画按钮(顺序摆动画自定义模式)
        self.button_animation_order_define.clicked.connect(self.start_computation_trajectory_animation_order_define)

        self.button_simulation_order.clicked.connect(
            self.start_computation_Polishing_distribution_order)  # 顺序摆抛磨量分布仿真按钮
        self.button_simulation_order_define.clicked.connect(
            self.start_computation_Polishing_distribution_order_define)  # 顺序摆(自定义)摆抛磨量分布按钮

        self.button_middle_line_order.clicked.connect(self.middle_line_figure_plot_order)  # 顺序摆轨迹中心线绘制按钮
        self.button_middle_line_order_define.clicked.connect(
            self.middle_line_figure_plot_order_selfdefine)  # 顺序摆(自定义)中心线绘制按钮
        # 在程序中创建一个显示图框 播放gif动画
        self.gif_label = QLabel(self.widget)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 调整gif_label的大小以适应widget
        self.gif_label.resize(self.widget.size())
        # 确保gif_label随widget大小变化而变化
        self.widget.resizeEvent = self.resize_event

        # 界面分割图片元素
        self.label_top.setText('')
        pixmap = QPixmap(":single")  # 替换为实际图片路径
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

    # 轨迹参数计算（节能计算）
    def energy_calculate(self):
        v1=float(self.lineEdit_belt_speed.text())
        ceramic_width=float(self.lineEdit_ceramic_width.text())
        beam_between=float(self.lineEdit_beam_between.text())
        R=float(self.lineEdit_radius.text())
        overlap=float(self.lineEdit_overlap.text())
        a=float(self.lineEdit_accelerate.text())
        beam_speed_up=float(self.lineEdit_beam_speed_up.text())
        result=Single_Calc_Parameter_Calculate.single_num_calculate(v1,ceramic_width,beam_between,R,overlap,a,beam_speed_up)
        self.lineEdit_beam_swing_speed.setText(str(result[0, 1]))
        self.lineEdit_beam_constant_time.setText(str(result[0, 2]))
        self.lineEdit_stay_time.setText(str(result[0, 3]))
        self.lineEdit_num.setText(str(result[0, 4]))
        self.lineEdit_delay_time.setText(str(result[0,5]))
        self.lineEdit_swing.setText(str(result[0, 6]))
        self.lineEdit_between.setText(str(result[0, 7]))
    # 轨迹参数计算（高效计算）
    def efficient_calculate(self):       # 高效计算
        v1 = float(self.lineEdit_belt_speed.text())
        ceramic_width = float(self.lineEdit_ceramic_width.text())
        beam_between = float(self.lineEdit_beam_between.text())
        R = float(self.lineEdit_radius.text())
        overlap = float(self.lineEdit_overlap.text())
        a = float(self.lineEdit_accelerate.text())
        beam_speed_up = float(self.lineEdit_beam_speed_up.text())
        result = Single_Calc_Parameter_Calculate.single_num_calculate(v1, ceramic_width, beam_between, R, overlap, a,
                                                                 beam_speed_up)
        self.lineEdit_beam_swing_speed.setText(str(result[1, 1]))
        self.lineEdit_beam_constant_time.setText(str(result[1, 2]))
        self.lineEdit_stay_time.setText(str(result[1, 3]))
        self.lineEdit_num.setText(str(result[1, 4]))
        self.lineEdit_delay_time.setText(str(result[1, 5]))
        self.lineEdit_swing.setText(str(result[1, 6]))
        self.lineEdit_between.setText(str(result[0, 7]))
    # 轨迹参数计算（自定义计算）
    def define_calculate(self):
        v1 = float(self.lineEdit_belt_speed.text())
        ceramic_width = float(self.lineEdit_ceramic_width.text())
        beam_between = float(self.lineEdit_beam_between.text())
        R = float(self.lineEdit_radius.text())
        a = float(self.lineEdit_accelerate.text())
        num=float(self.lineEdit_num_set.text())
        group=float(self.lineEdit_group_count.text())
        stay_time=float(self.lineEdit_stay_time.text())
        beam_speed_up=float(self.lineEdit_beam_speed_up.text())
        result = self_define_calculate(v1,beam_speed_up,ceramic_width,beam_between,R,a,num,stay_time)
        self.lineEdit_beam_swing_speed.setText(str(result[0, 1]))
        self.lineEdit_beam_constant_time.setText(str(result[0, 2]))
        self.lineEdit_stay_time.setText(str(result[0, 3]))
        self.lineEdit_num.setText(str(result[0, 4]*group))
        self.lineEdit_delay_time.setText(str(result[0, 5]))
        self.lineEdit_swing.setText(str(result[0, 6]))
        self.lineEdit_between.setText(str(result[0, 7]))
    # 抛磨量分布仿真子线程
    # 顺序摆抛磨量分布仿真子线程
    def start_computation_Polishing_distribution_order(self):      # 抛磨量分布仿真子线程
        # 创建子线程
        self.Polishing_distribution_thread = Polishing_distribution_Thread_order(float(self.lineEdit_belt_speed.text()),
                                                                           float(self.lineEdit_beam_swing_speed.text()),
                                                                           float(self.lineEdit_beam_constant_time.text()),
                                                                           float(self.lineEdit_stay_time.text()),
                                                                           float(self.lineEdit_accelerate.text()),
                                                                           float(self.lineEdit_between.text()),
                                                                           float(self.lineEdit_beam_between.text()),
                                                                           math.ceil(float(self.lineEdit_num.text())),
                                                                           float(self.lineEdit_radius.text()),
                                                                           float(self.lineEdit_grind_size.text()),
                                                                           float(self.lineEdit_delay_time.text()))
        self.Polishing_distribution_thread.result_ready.connect(self.Polishing_distribution_ready)
        self.button_simulation_order.setEnabled(False)
        self.button_simulation_order_define.setEnabled(False)
        # 运行子线程
        self.Polishing_distribution_thread.start()
    # 顺序摆（自定义）抛磨量分布仿真子线程
    def start_computation_Polishing_distribution_order_define(self):      # 抛磨量分布仿真子线程
        # 创建子线程
        self.Polishing_distribution_thread = Polishing_distribution_Thread_order_unequal(float(self.lineEdit_belt_speed.text()),
                                                                           float(self.lineEdit_beam_swing_speed.text()),
                                                                           float(self.lineEdit_beam_constant_time.text()),
                                                                           float(self.lineEdit_stay_time.text()),
                                                                           float(self.lineEdit_accelerate.text()),
                                                                           float(self.lineEdit_between.text()),
                                                                           float(self.lineEdit_beam_between.text()),
                                                                           math.ceil(float(self.lineEdit_num_set.text())),
                                                                           float(self.lineEdit_radius.text()),
                                                                           float(self.lineEdit_grind_size.text()),
                                                                           float(self.lineEdit_delay_time.text()),
                                                                           float(self.lineEdit_group_count.text()))
        self.Polishing_distribution_thread.result_ready.connect(self.Polishing_distribution_ready)
        self.button_simulation_order.setEnabled(False)
        self.button_simulation_order_define.setEnabled(False)
        # 运行子线程
        self.Polishing_distribution_thread.start()
    def Polishing_distribution_ready(self,object_matrix, result):     # 子线程回调函数
        # 在主线程中绘图
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置微软雅黑字体
        plt.rcParams['axes.unicode_minus'] = False  # 避免坐标轴不能正常的显示负号
        fig = plt.figure('抛磨强度分布仿真')
        ax = fig.add_subplot(111)
        ax.set_aspect('equal', adjustable='box')
        im = ax.contourf(object_matrix, 15, alpha=1, cmap='jet')
        plt.xlabel('Tile feed direction')
        plt.ylabel('Beam swing direction')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        plt.colorbar(im, cax=cax)
        plt.show()  # 显示函数图像
        #equal_coefficient
        self.button_simulation_order.setEnabled(True)
        self.button_simulation_order_define.setEnabled(True)
        self.lineEdit_coefficient.setText(result)
    # 轨迹动画生成子线程
    # 顺序摆动画
    def start_computation_trajectory_animation_order(self):
        self.trajectory_animation_thread = Animation_produce_order(float(self.lineEdit_belt_speed.text()),
                                                            float(self.lineEdit_beam_swing_speed.text()),
                                                            float(self.lineEdit_beam_constant_time.text()),
                                                            float(self.lineEdit_stay_time.text()),
                                                            float(self.lineEdit_accelerate.text()),
                                                            float(self.lineEdit_radius.text()),
                                                            float(self.lineEdit_between.text()),
                                                            float(self.lineEdit_beam_between.text()),
                                                            math.ceil(float(self.lineEdit_num.text())),
                                                            float(self.lineEdit_delay_time.text())
                                                            )
        self.trajectory_animation_thread.result_ready.connect(self.trajectory_animation_ready)
        self.button_animation_order.setEnabled(False)
        self.button_animation_order_define.setEnabled(False)
        # 运行子线程
        self.trajectory_animation_thread.start()
    # 顺序摆动画（自定义模式）
    def start_computation_trajectory_animation_order_define(self):
        self.trajectory_animation_thread = Animation_produce_order(float(self.lineEdit_belt_speed.text()),
                                                            float(self.lineEdit_beam_swing_speed.text()),
                                                            float(self.lineEdit_beam_constant_time.text()),
                                                            float(self.lineEdit_stay_time.text()),
                                                            float(self.lineEdit_accelerate.text()),
                                                            float(self.lineEdit_radius.text()),
                                                            float(self.lineEdit_between.text()),
                                                            float(self.lineEdit_beam_between.text()),
                                                            math.ceil(float(self.lineEdit_num_set.text())),
                                                            float(self.lineEdit_delay_time.text())
                                                            )
        self.trajectory_animation_thread.result_ready.connect(self.trajectory_animation_ready)
        self.button_animation_order.setEnabled(False)
        self.button_animation_order_define.setEnabled(False)
        # 运行子线程
        self.trajectory_animation_thread.start()
    def trajectory_animation_ready(self,str_22):
        # 加载GIF动画
        print(str_22)
        self.movie = QMovie("animation.gif")
        #self.movie.setloopCount(1)  # 设置只播放一次
        self.gif_label.setMovie(self.movie)
        self.movie.start()
        self.button_animation_order.setEnabled(True)
        self.button_animation_order_define.setEnabled(True)
    # 调整动画在界面图框中的位置
    def resize_event(self, event):
        self.gif_label.resize(event.size())
    # 绘制磨头中心轨迹线
    # 顺序摆模式轨迹中心线
    def middle_line_figure_plot_order(self):
        belt_speed=float(self.lineEdit_belt_speed.text())
        beam_speed=float(self.lineEdit_beam_swing_speed.text())
        constant_time=float(self.lineEdit_beam_constant_time.text())
        stay_time=float(self.lineEdit_stay_time.text())
        a_speed=float(self.lineEdit_accelerate.text())
        num=math.ceil(float(self.lineEdit_num.text()))
        between=float(self.lineEdit_between.text())
        between_beam = float(self.lineEdit_beam_between.text())
        delay_tome = float(self.lineEdit_delay_time.text())
        mid_var=middle_line_plot_order(belt_speed,beam_speed,constant_time,stay_time,a_speed,num,between,between_beam,delay_tome)
        mid_var.figure_plot()
    # 顺序摆（自定义）模式轨迹中心线
    def middle_line_figure_plot_order_selfdefine(self):
        belt_speed=float(self.lineEdit_belt_speed.text())
        beam_speed=float(self.lineEdit_beam_swing_speed.text())
        constant_time=float(self.lineEdit_beam_constant_time.text())
        stay_time=float(self.lineEdit_stay_time.text())
        a_speed=float(self.lineEdit_accelerate.text())
        num=math.ceil(float(self.lineEdit_num_set.text()))
        between=float(self.lineEdit_between.text())
        between_beam = float(self.lineEdit_beam_between.text())
        delay_time = float(self.lineEdit_delay_time.text())
        group = float(self.lineEdit_group_count.text())
        mid_var=middle_line_plot_self_define_order(belt_speed,beam_speed,constant_time,stay_time,a_speed,num,between,between_beam,delay_time,group)
        mid_var.figure_plot()

