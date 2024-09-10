from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtWidgets import QWidget, QLabel
import math

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import Equal_Calc
import Equal_Calc_Parameter_Calculate
from Equal_Calc_Polishing_Distribution_Simulation import Polishing_distribution_Thread
from Equal_Calc_Generate_Animation import Animation_produce
from Equal_Calc_Middle_Line_Plot import middle_line_plot


class EqualWidgetImpl(QWidget, Equal_Calc.Ui_MainWindow):
    def __init__(self, w):
        super().__init__()
        self.setupUi(w)

        self.reCalcFlag = True

        self.setAttribute(Qt.WA_StyledBackground)  # 禁止父窗口样式影响子控件样式

        # 运行逻辑
        # 按钮操作
        self.button_energy_calculate.clicked.connect(self.energy_calculate)  # 节能计算按钮
        self.button_efficient_calculate.clicked.connect(self.efficient_calculate)  # 高效计算按钮
        self.button_animation_equal.clicked.connect(self.start_computation_trajectory_animation)  # 动画按钮
        self.button_simulation_equal.clicked.connect(self.start_computation_Polishing_distribution)  # 抛磨量分布仿真按钮
        self.button_middle_line_equal.clicked.connect(self.middle_line_figure_plot)  # 磨头中心线绘制按钮
        # 在程序中创建一个显示图框 播放gif动画
        self.gif_label = QLabel(self.widget)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 调整gif_label的大小以适应widget
        self.gif_label.resize(self.widget.size())
        # 确保gif_label随widget大小变化而变化
        self.widget.resizeEvent = self.resize_event

        self.lineEdit_between.setText('600')
        self.lineEdit_radius.setText('270')
        self.lineEdit_grind_size.setText('170')
        self.lineEdit_ceramic_width.setText('1200')
        self.lineEdit_belt_speed.setText('300')
        self.lineEdit_beam_speed_up.setText('500')
        self.lineEdit_accelerate.setText('600')
        self.lineEdit_overlap.setText('50')

        self.add_text_change_monitor(self.lineEdit_between)
        self.add_text_change_monitor(self.lineEdit_grind_size)
        self.add_text_change_monitor(self.lineEdit_belt_speed)
        self.add_text_change_monitor(self.lineEdit_accelerate)
        self.add_text_change_monitor(self.lineEdit_radius)
        self.add_text_change_monitor(self.lineEdit_beam_speed_up)
        self.add_text_change_monitor(self.lineEdit_ceramic_width)
        self.add_text_change_monitor(self.lineEdit_overlap)

        self.line_edits = [self.lineEdit_between, self.lineEdit_grind_size, self.lineEdit_belt_speed, self.lineEdit_accelerate,
                           self.lineEdit_radius, self.lineEdit_beam_speed_up, self.lineEdit_ceramic_width, self.lineEdit_overlap]

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
        self.button_animation_equal.setStyleSheet(qss_Button)
        self.button_efficient_calculate.setStyleSheet(qss_Button)
        self.button_middle_line_equal.setStyleSheet(qss_Button)
        self.button_simulation_equal.setStyleSheet(qss_Button)

    def add_text_change_monitor(self, line_edit):
        """为QLineEdit控件添加内容变化监控"""
        line_edit.textChanged.connect(self.on_text_changed)

    def on_text_changed(self, text):
        """当LineEdit内容发生变化时触发的回调函数"""
        # print(f"内容发生变化: {text}")
        self.reCalcFlag = True

    # 轨迹参数计算（节能计算）
    def energy_calculate(self):
        v1=float(self.lineEdit_belt_speed.text())
        ceramic_width=float(self.lineEdit_ceramic_width.text())
        between=float(self.lineEdit_between.text())
        R=float(self.lineEdit_radius.text())
        overlap=float(self.lineEdit_overlap.text())
        a=float(self.lineEdit_accelerate.text())
        beam_speed_up=float(self.lineEdit_beam_speed_up.text())
        result=Equal_Calc_Parameter_Calculate.equal_num_calculate(v1,ceramic_width,between,R,overlap,a,beam_speed_up)
        self.lineEdit_beam_swing_speed.setText(str(result[0, 1]))
        self.lineEdit_num.setText(str(result[0, 4]))
        self.lineEdit_stay_time.setText(str(result[0, 3]))
        self.lineEdit_beam_constant_time.setText(str(result[0, 2]))
        self.lineEdit_swing.setText(str(result[0, 5]))
    # 轨迹参数计算（高效计算）
    def efficient_calculate(self):       # 高效计算
        v1=float(self.lineEdit_belt_speed.text())
        ceramic_width=float(self.lineEdit_ceramic_width.text())
        between=float(self.lineEdit_between.text())
        R=float(self.lineEdit_radius.text())
        overlap=float(self.lineEdit_overlap.text())
        a=float(self.lineEdit_accelerate.text())
        beam_speed_up=float(self.lineEdit_beam_speed_up.text())
        result=Equal_Calc_Parameter_Calculate.equal_num_calculate(v1,ceramic_width,between,R,overlap,a,beam_speed_up)
        self.lineEdit_beam_swing_speed.setText(str(result[1, 1]))
        self.lineEdit_num.setText(str(result[1, 4]))
        self.lineEdit_stay_time.setText(str(result[1, 3]))
        self.lineEdit_beam_constant_time.setText(str(result[1, 2]))
        self.lineEdit_swing.setText(str(result[1, 5]))
    # 抛磨量分布仿真子线程
    def start_computation_Polishing_distribution(self):      # 抛磨量分布仿真子线程
        # 创建子线程
        self.Polishing_distribution_thread = Polishing_distribution_Thread(float(self.lineEdit_belt_speed.text()),
                                                                           float(self.lineEdit_beam_swing_speed.text()),
                                                                           float(self.lineEdit_beam_constant_time.text()),
                                                                           float(self.lineEdit_stay_time.text()),
                                                                           float(self.lineEdit_accelerate.text()),
                                                                           float(self.lineEdit_between.text()),
                                                                           math.ceil(float(self.lineEdit_num.text())),
                                                                           float(self.lineEdit_radius.text()),
                                                                           float(self.lineEdit_grind_size.text()))
        self.Polishing_distribution_thread.result_ready.connect(self.Polishing_distribution_ready)
        self.button_simulation_equal.setEnabled(False)
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
        self.lineEdit_coefficient.setText(result)
        self.button_simulation_equal.setEnabled(True)
    # 轨迹动画生成子线程
    def start_computation_trajectory_animation(self):
        self.trajectory_animation_thread = Animation_produce(float(self.lineEdit_belt_speed.text()),
                                                            float(self.lineEdit_beam_swing_speed.text()),
                                                            float(self.lineEdit_beam_constant_time.text()),
                                                            float(self.lineEdit_stay_time.text()),
                                                            float(self.lineEdit_accelerate.text()),
                                                            float(self.lineEdit_radius.text()),
                                                            float(self.lineEdit_between.text()),
                                                            math.ceil(float(self.lineEdit_num.text()))
                                                            )
        self.trajectory_animation_thread.result_ready.connect(self.trajectory_animation_ready)
        self.button_animation_equal.setEnabled(False)
        # 运行子线程
        self.trajectory_animation_thread.start()
    def trajectory_animation_ready(self,str_22):
        # 加载GIF动画
        print(str_22)
        self.movie = QMovie('./animation.gif')
        #self.movie.setloopCount(1)  # 设置只播放一次
        self.gif_label.setMovie(self.movie)
        self.movie.start()
        self.button_animation_equal.setEnabled(True)
    # 调整动画在界面图框中的位置
    def resize_event(self, event):
        self.gif_label.resize(event.size())
    # 绘制磨头中心轨迹线
    def middle_line_figure_plot(self):
        belt_speed=float(self.lineEdit_belt_speed.text())
        beam_speed=float(self.lineEdit_beam_swing_speed.text())
        constant_time=float(self.lineEdit_beam_constant_time.text())
        stay_time=float(self.lineEdit_stay_time.text())
        a_speed=float(self.lineEdit_accelerate.text())
        num=math.ceil(float(self.lineEdit_num.text()))
        between=float(self.lineEdit_between.text())
        mid_var=middle_line_plot(belt_speed,beam_speed,constant_time,stay_time,a_speed,num,between)
        mid_var.figure_plot()