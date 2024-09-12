import math
import os

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtWidgets import QWidget, QLabel
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import Single_Sim
from Single_Sim_Middle_Line_Plot import middle_line_plot_order,middle_line_plot_equal,middle_line_plot_cross
from Single_Sim_Generate_Animation import Animation_produce_cross, Animation_produce_order, Animation_produce_equal
from Single_Sim_Polishing_Distribution_Simulation import Polishing_distribution_Thread_equal, \
    Polishing_distribution_Thread_order, Polishing_distribution_Thread_cross


class SingleSimWidgetImpl(QWidget, Single_Sim.Ui_MainWindow):
    def __init__(self, w):
        super().__init__()
        self.setupUi(w)

        self.setAttribute(Qt.WA_StyledBackground)  # 禁止父窗口样式影响子控件样式

        self.settings = QSettings("config.ini", QSettings.IniFormat)  # 使用配置文件
        self.loadParameter()  # 在初始化时加载设置
        # 运行逻辑
        # 按钮操作
        # 动画按钮(同步摆动画)
        self.button_animation_equal.clicked.connect(self.start_computation_trajectory_animation_equal)
        # 动画按钮(交叉摆动画)
        self.button_animation_cross.clicked.connect(self.start_computation_trajectory_animation_cross)
        # 动画按钮(顺序摆动画)
        self.button_animation_order.clicked.connect(self.start_computation_trajectory_animation_order)

        self.button_simulation_equal.clicked.connect(
            self.start_computation_Polishing_distribution_equal)  # 同步摆抛磨量分布仿真按钮
        self.button_simulation_order.clicked.connect(
            self.start_computation_Polishing_distribution_order)  # 顺序摆抛磨量分布仿真按钮
        self.button_simulation_cross.clicked.connect(self.start_computation_Polishing_distribution_cross)  # 交叉抛磨量分布仿真按钮

        self.button_middle_line_equal.clicked.connect(self.middle_line_figure_plot_equal)  # 同步摆轨迹中心线绘制按钮
        self.button_middle_line_cross.clicked.connect(self.middle_line_figure_plot_cross)  # 交叉摆轨迹中心线绘制按钮
        self.button_middle_line_order.clicked.connect(self.middle_line_figure_plot_order)  # 顺序摆轨迹中心线绘制按钮
        self.button_save_parameter.clicked.connect(self.saveParameter)
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

        self.line_edits = [self.lineEdit_beam_between, self.lineEdit_grind_size, self.lineEdit_belt_speed,
                           self.lineEdit_beam_constant_time,
                           self.lineEdit_radius, self.lineEdit_ceramic_width, self.lineEdit_beam_swing_speed,
                           self.lineEdit_stay_time,
                           self.lineEdit_accelerate,
                           self.lineEdit_delay_time,
                           self.lineEdit_num]

    # 抛磨量分布仿真子线程
    # 同步摆抛磨量分布仿真子线程
    def start_computation_Polishing_distribution_equal(self):
        # 创建子线程
        self.Polishing_distribution_thread = Polishing_distribution_Thread_equal(float(self.lineEdit_belt_speed.text()),
                                                                           float(self.lineEdit_beam_swing_speed.text()),
                                                                           float(self.lineEdit_beam_constant_time.text()),
                                                                           float(self.lineEdit_stay_time.text()),
                                                                           float(self.lineEdit_accelerate.text()),
                                                                           float(self.lineEdit_beam_between.text()),
                                                                           math.ceil(float(self.lineEdit_num.text())),
                                                                           float(self.lineEdit_radius.text()),
                                                                           float(self.lineEdit_grind_size.text()))
        self.Polishing_distribution_thread.result_ready.connect(self.polishing_distribution_ready)
        self.button_simulation_equal.setEnabled(False)
        self.button_simulation_cross.setEnabled(False)
        self.button_simulation_order.setEnabled(False)
        # 运行子线程
        self.Polishing_distribution_thread.start()
    # 顺序摆抛磨量分布仿真子线程
    def start_computation_Polishing_distribution_order(self):
        # 创建子线程
        self.Polishing_distribution_thread = Polishing_distribution_Thread_order(float(self.lineEdit_belt_speed.text()),
                                                                           float(self.lineEdit_beam_swing_speed.text()),
                                                                           float(self.lineEdit_beam_constant_time.text()),
                                                                           float(self.lineEdit_stay_time.text()),
                                                                           float(self.lineEdit_accelerate.text()),
                                                                           float(self.lineEdit_beam_between.text()),
                                                                           math.ceil(float(self.lineEdit_num.text())),
                                                                           float(self.lineEdit_radius.text()),
                                                                           float(self.lineEdit_grind_size.text()),
                                                                           float(self.lineEdit_delay_time.text()))
        self.Polishing_distribution_thread.result_ready.connect(self.polishing_distribution_ready)
        self.button_simulation_equal.setEnabled(False)
        self.button_simulation_cross.setEnabled(False)
        self.button_simulation_order.setEnabled(False)
        # 运行子线程
        self.Polishing_distribution_thread.start()
    # 交叉摆抛磨量分布仿真子线程
    def start_computation_Polishing_distribution_cross(self):
        # 创建子线程
        self.Polishing_distribution_thread = Polishing_distribution_Thread_cross(float(self.lineEdit_belt_speed.text()),
                                                                           float(self.lineEdit_beam_swing_speed.text()),
                                                                           float(self.lineEdit_beam_constant_time.text()),
                                                                           float(self.lineEdit_stay_time.text()),
                                                                           float(self.lineEdit_accelerate.text()),
                                                                           float(self.lineEdit_beam_between.text()),
                                                                           math.ceil(float(self.lineEdit_num.text())),
                                                                           float(self.lineEdit_radius.text()),
                                                                           float(self.lineEdit_grind_size.text()))
        self.Polishing_distribution_thread.result_ready.connect(self.polishing_distribution_ready)
        self.button_simulation_equal.setEnabled(False)
        self.button_simulation_order.setEnabled(False)
        self.button_simulation_cross.setEnabled(False)
        # 运行子线程
        self.Polishing_distribution_thread.start()
    # 抛磨量分布仿真子线程回调函数
    def polishing_distribution_ready(self,object_matrix, result):
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
        self.button_simulation_equal.setEnabled(True)
        self.button_simulation_order.setEnabled(True)
        self.button_simulation_cross.setEnabled(True)
        self.lineEdit_coefficient.setText(result)

    def on_button_clicked(self):
        for line_edit in self.line_edits:
            if not line_edit.text().strip():  # 如果任何一个LineEdit为空
                textname = self.on_Find_Label_Name(line_edit.objectName())
                QMessageBox.warning(self, "警告", f"{textname}输入框必须填写数据！")
                return False
        return True
    # 轨迹动画生成子线程
    def start_computation_trajectory_animation_cross(self):
        if not self.on_button_clicked():
            return
        animation_name = ('SingleSimCrossAnimation-' +
                          self.lineEdit_belt_speed.text() + '_' + self.lineEdit_beam_swing_speed.text() + '_' + self.lineEdit_beam_constant_time.text() + '_' +
                          self.lineEdit_stay_time.text() + '_' +
                          self.lineEdit_accelerate.text() + '_' +
                          self.lineEdit_radius.text() + '_' +
                          self.lineEdit_beam_between.text() + '_' +
                          self.lineEdit_num.text())

        if not self.check_animation_gif(animation_name):
            self.trajectory_animation_thread = Animation_produce_cross(float(self.lineEdit_belt_speed.text()),
                                                                float(self.lineEdit_beam_swing_speed.text()),
                                                                float(self.lineEdit_beam_constant_time.text()),
                                                                float(self.lineEdit_stay_time.text()),
                                                                float(self.lineEdit_accelerate.text()),
                                                                float(self.lineEdit_radius.text()),
                                                                float(self.lineEdit_beam_between.text()),
                                                                math.ceil(float(self.lineEdit_num.text())),
                                                                animation_name
                                                                )
            self.trajectory_animation_thread.result_ready.connect(self.trajectory_animation_ready)
            self.button_animation_equal.setEnabled(False)
            self.button_animation_order.setEnabled(False)
            self.button_animation_cross.setEnabled(False)
            # 运行子线程
            self.trajectory_animation_thread.start()
        else:
            self.trajectory_animation_ready(animation_name)
    def start_computation_trajectory_animation_order(self):
        if not self.on_button_clicked():
            return
        animation_name = ('SingleSimOrderAnimation-' +
                          self.lineEdit_belt_speed.text() + '_' + self.lineEdit_beam_swing_speed.text() + '_' + self.lineEdit_beam_constant_time.text() + '_' +
                          self.lineEdit_stay_time.text() + '_' +
                          self.lineEdit_accelerate.text() + '_' +
                          self.lineEdit_radius.text() + '_' +
                          self.lineEdit_beam_between.text() + '_' +
                          self.lineEdit_num.text() + '_' + self.lineEdit_delay_time.text())

        if not self.check_animation_gif(animation_name):
            self.trajectory_animation_thread = Animation_produce_order(float(self.lineEdit_belt_speed.text()),
                                                                float(self.lineEdit_beam_swing_speed.text()),
                                                                float(self.lineEdit_beam_constant_time.text()),
                                                                float(self.lineEdit_stay_time.text()),
                                                                float(self.lineEdit_accelerate.text()),
                                                                float(self.lineEdit_radius.text()),
                                                                float(self.lineEdit_beam_between.text()),
                                                                math.ceil(float(self.lineEdit_num.text())),
                                                                float(self.lineEdit_delay_time.text()),
                                                                animation_name
                                                                )
            self.trajectory_animation_thread.result_ready.connect(self.trajectory_animation_ready)
            self.button_animation_equal.setEnabled(False)
            self.button_animation_order.setEnabled(False)
            self.button_animation_cross.setEnabled(False)
            # 运行子线程
            self.trajectory_animation_thread.start()
        else:
            self.trajectory_animation_ready(animation_name)
    def start_computation_trajectory_animation_equal(self):
        if not self.on_button_clicked():
            return
        animation_name = ('SingleSimEqualAnimation-' +
                          self.lineEdit_belt_speed.text() + '_' + self.lineEdit_beam_swing_speed.text() + '_' + self.lineEdit_beam_constant_time.text() + '_' +
                          self.lineEdit_stay_time.text() + '_' +
                          self.lineEdit_accelerate.text() + '_' +
                          self.lineEdit_radius.text() + '_' +
                          self.lineEdit_beam_between.text() + '_' + self.lineEdit_num.text())

        if not self.check_animation_gif(animation_name):
            self.trajectory_animation_thread = Animation_produce_equal(float(self.lineEdit_belt_speed.text()),
                                                                       float(self.lineEdit_beam_swing_speed.text()),
                                                                       float(self.lineEdit_beam_constant_time.text()),
                                                                       float(self.lineEdit_stay_time.text()),
                                                                       float(self.lineEdit_accelerate.text()),
                                                                       float(self.lineEdit_radius.text()),
                                                                       float(self.lineEdit_beam_between.text()),
                                                                       math.ceil(float(self.lineEdit_num.text())),
                                                                       animation_name
                                                                       )
            self.trajectory_animation_thread.result_ready.connect(self.trajectory_animation_ready)
            self.button_animation_equal.setEnabled(False)
            self.button_animation_order.setEnabled(False)
            self.button_animation_cross.setEnabled(False)
            # 运行子线程
            self.trajectory_animation_thread.start()
        else:
            self.trajectory_animation_ready(animation_name)
    def trajectory_animation_ready(self,animation_name):
        # 加载GIF动画
        print(animation_name)
        self.movie = QMovie('./animation/' + animation_name + '.gif')
        #self.movie.setloopCount(1)  # 设置只播放一次
        self.gif_label.setMovie(self.movie)
        self.movie.start()
        self.button_animation_equal.setEnabled(True)
        self.button_animation_order.setEnabled(True)
        self.button_animation_cross.setEnabled(True)
    # 调整动画在界面图框中的位置
    def resize_event(self, event):
        self.gif_label.resize(event.size())
    # 绘制磨头中心轨迹线
    # 同步摆模式轨迹中心线
    def middle_line_figure_plot_equal(self):
        belt_speed=float(self.lineEdit_belt_speed.text())
        beam_speed=float(self.lineEdit_beam_swing_speed.text())
        constant_time=float(self.lineEdit_beam_constant_time.text())
        stay_time=float(self.lineEdit_stay_time.text())
        a_speed=float(self.lineEdit_accelerate.text())
        num=math.ceil(float(self.lineEdit_num.text()))
        beam_between=float(self.lineEdit_beam_between.text())
        mid_var=middle_line_plot_equal(belt_speed,beam_speed,constant_time,stay_time,a_speed,num,beam_between)
        mid_var.figure_plot()
    # 交叉摆模式轨迹中心线
    def middle_line_figure_plot_cross(self):
        belt_speed=float(self.lineEdit_belt_speed.text())
        beam_speed=float(self.lineEdit_beam_swing_speed.text())
        constant_time=float(self.lineEdit_beam_constant_time.text())
        stay_time=float(self.lineEdit_stay_time.text())
        a_speed=float(self.lineEdit_accelerate.text())
        num=math.ceil(float(self.lineEdit_num.text()))
        beam_between = float(self.lineEdit_beam_between.text())
        mid_var=middle_line_plot_cross(belt_speed,beam_speed,constant_time,stay_time,a_speed,num,beam_between)
        mid_var.figure_plot()
    # 顺序摆模式轨迹中心线
    def middle_line_figure_plot_order(self):
        belt_speed=float(self.lineEdit_belt_speed.text())
        beam_speed=float(self.lineEdit_beam_swing_speed.text())
        constant_time=float(self.lineEdit_beam_constant_time.text())
        stay_time=float(self.lineEdit_stay_time.text())
        a_speed=float(self.lineEdit_accelerate.text())
        num=math.ceil(float(self.lineEdit_num.text()))
        between_beam = float(self.lineEdit_beam_between.text())
        delay_time = float(self.lineEdit_delay_time.text())
        mid_var=middle_line_plot_order(belt_speed,beam_speed,constant_time,stay_time,a_speed,num,between_beam,delay_time)
        mid_var.figure_plot()

    def saveParameter(self):
        """保存各个LineEdit控件的数据到配置文件"""
        self.settings.setValue("lineEdit_beam_between6", self.lineEdit_beam_between.text())
        self.settings.setValue("lineEdit_grind_size6", self.lineEdit_grind_size.text())
        self.settings.setValue("lineEdit_belt_speed6", self.lineEdit_belt_speed.text())
        self.settings.setValue("lineEdit_beam_constant_time6", self.lineEdit_beam_constant_time.text())
        self.settings.setValue("lineEdit_radius6", self.lineEdit_radius.text())
        self.settings.setValue("lineEdit_ceramic_width6", self.lineEdit_ceramic_width.text())
        self.settings.setValue("lineEdit_beam_swing_speed6", self.lineEdit_beam_swing_speed.text())
        self.settings.setValue("lineEdit_stay_time6", self.lineEdit_stay_time.text())
        self.settings.setValue("lineEdit_delay_time6", self.lineEdit_delay_time.text())
        self.settings.setValue("lineEdit_accelerate6", self.lineEdit_accelerate.text())
        self.settings.setValue("lineEdit_num6", self.lineEdit_num.text())
        self.settings.setValue("lineEdit_coefficient6", self.lineEdit_coefficient.text())

    def loadParameter(self):
        """加载配置文件中的数据到各个LineEdit控件"""
        self.lineEdit_beam_between.setText(self.settings.value("lineEdit_beam_between6", ""))
        self.lineEdit_grind_size.setText(self.settings.value("lineEdit_grind_size6", ""))
        self.lineEdit_belt_speed.setText(self.settings.value("lineEdit_belt_speed6", ""))
        self.lineEdit_beam_constant_time.setText(self.settings.value("lineEdit_beam_constant_time6", ""))
        self.lineEdit_radius.setText(self.settings.value("lineEdit_radius6", ""))
        self.lineEdit_ceramic_width.setText(self.settings.value("lineEdit_ceramic_width6", ""))
        self.lineEdit_beam_swing_speed.setText(self.settings.value("lineEdit_beam_swing_speed6", ""))
        self.lineEdit_stay_time.setText(self.settings.value("lineEdit_stay_time6", ""))
        self.lineEdit_delay_time.setText(self.settings.value("lineEdit_delay_time6", ""))
        self.lineEdit_accelerate.setText(self.settings.value("lineEdit_accelerate6", ""))
        self.lineEdit_num.setText(self.settings.value("lineEdit_num6", ""))
        self.lineEdit_coefficient.setText(self.settings.value("lineEdit_coefficient6", ""))

    def check_animation_gif(self, animation_name):
        # 定义文件路径
        file_path = os.path.join(os.getcwd(), 'animation', animation_name + '.gif')

        # 判断文件是否存在
        return os.path.isfile(file_path)