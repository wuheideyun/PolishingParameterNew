from MainWindow_New_Interface import MainWindow
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
import multiprocessing
from matplotlib.patches import Rectangle  # 导入 Rectangle
# 函数导入
from Double_enerage_project import Double_enerage_WorkerThread
from Double_efficient_project import double_num_calculate,polishing_cal,Polishing_distribution_Thread_order,middle_line_plot_order
class MainWindow_impl(MainWindow):
    def __init__(self):
        super().__init__()

        # -------------------------按钮逻辑部分---------------------
        self.button_energy_project.clicked.connect(self.enerage_project)
        self.button_efficient_project.clicked.connect(self.efficient_project)
        # self.button_selfdefine_project.clicked.connect(self.selfdefine_project)
        #
        # self.button_synchronization_mode.clicked.connect(self.syn_mode)
        # self.button_cross_mode.clicked.connect(self.cross_project)
        # self.button_order_mode.clicked.connect(self.order_project)
    # 按钮点击槽函数(计算)
    def enerage_project(self):
        if self.current_mode == 1:
            self.single_enerage_project()
        elif self.current_mode == 2:
            self.double_enerage_project(300, 900, 600, 1900, 270, 650, 170)
        elif self.current_mode == 3:
            # 待开发---
            return

    def efficient_project(self):
        if self.current_mode == 1:
            self.single_efficient_project()
        elif self.current_mode == 2:
            self.double_efficient_project()
        elif self.current_mode == 3:
            # 待开发---
            return

    def selfdefine_project(self):
        if self.current_mode == 1:
            self.single_self_project()
        elif self.current_mode == 2:
            self.double_self_project()
        elif self.current_mode == 3:
            # 待开发---
            return

    # # 按钮点击槽函数(仿真)
    # def syn_project(self):
    #     if self.current_mode == 1:
    #         self.single_synchronization_project()
    #     elif self.current_mode == 2:
    #         self.double_synchronization_project()
    #     elif self.current_mode == 3:
    #         # 待开发---
    #         return
    #
    # def cross_project(self):
    #     if self.current_mode == 1:
    #         self.single_cross_project()
    #     elif self.current_mode == 2:
    #         self.double_cross_project()
    #     elif self.current_mode == 3:
    #         # 待开发---
    #         return
    #
    # def order_project(self):
    #     if self.current_mode == 1:
    #         self.single_order_project()
    #     elif self.current_mode == 2:
    #         self.double_order_project()
    #     elif self.current_mode == 3:
    #         # 待开发---
    #         return

    # 单头摆-智能计算逻辑函数
    # def single_enerage_project(self):

    # def single_efficient_project(self):

    # def single_self_project(self):

    # 单头摆-人工寻优逻辑函数
    # def single_synchronization_project(self):
    #
    # def single_cross_project(self):
    #
    # def single_order_project(self):

    # 双头摆-智能计算逻辑函数
    '''
    def double_enerage_project(self, v1, ceramic_width, between, beam_between, R, a, mo):
        # 参数计算
        result = double_num_calculate(v1, ceramic_width, between, beam_between, R, a)
        v2 = result[0, 1]
        constant_time = result[0, 2]
        stay_time = result[0, 3]
        num = result[0, 4]
        delay_time = result[0, 5]
        # 抛磨量分布-计算
        r_P_d = Polishing_distribution_Thread_order(v1, v2, constant_time, stay_time, a, between, beam_between, num, R,
                                                    mo, delay_time)
        result_P_d_matrix, result_P_d_par = r_P_d.emit()
        # 轨迹中心线分布-计算
        m_l_p = middle_line_plot_order(v1, v2, constant_time, stay_time, a, num, between, beam_between, delay_time)
        single_X_location, single_Y_location = m_l_p.inner_calculate()


        # ---------绘制组合图-----------
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置微软雅黑字体
        plt.rcParams['axes.unicode_minus'] = False  # 避免坐标轴不能正常的显示负号
        # 清空画布
        self.canvas.fig.clear()
        ax_1 = self.canvas.fig.add_subplot(211)
        ax_2 = self.canvas.fig.add_subplot(212)
        # 设置画布背景、刻度、字体颜色
        deep_blue = (31/255, 55/255, 96/255)
        list = [ax_1, ax_2]
        for ax in list:
            # 设置 子图背景颜色
            ax.set_facecolor(deep_blue)
            # 设置坐标轴线的颜色为白色
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            # 设置坐标轴的刻度颜色为白色
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            # 设置坐标轴标签的颜色为白色
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            # 设置坐标轴标题字体颜色为白色
            ax.title.set_color('white')
            # 设置 子图 标签
            ax.set_xlabel('主皮带进给方向')
            ax.set_ylabel('横梁摆动方向')
        # 绘制抛磨量分布仿真
        ax_1.set_aspect('equal', adjustable='box')
        object_matrix = result_P_d_matrix
        # 设置权重操作
        max_set = np.max(object_matrix)
        # 计算第90百分位的阈值（前15%）
        percentile_85 = np.percentile(object_matrix, 85)
        # 对矩阵中大于等于该阈值的元素乘以0.85
        object_matrix[object_matrix >= percentile_85] *= 0.85

        im = ax_1.contourf(object_matrix, levels=15, alpha=1, cmap='jet', vmin=0, vmax=max_set)

        divider = make_axes_locatable(ax_1)
        cax = divider.append_axes("right", size="5%", pad=0.1)

        colorbar = plt.colorbar(im, cax=cax)

        colorbar.ax.tick_params(labelcolor='white')  # 设置刻度标签颜色
        colorbar.set_label('抛磨量大小', color='white')  # 设置 colorbar 标签的颜色
        # 绘制矩形线框
        ceramic_width_ = float(ceramic_width) * 0.1
        width, length = np.shape(object_matrix)

        x_begin = 0
        y_begin = (width - ceramic_width_) / 2

        rect = Rectangle((x_begin, y_begin), length - 1, ceramic_width_, edgecolor='red', linestyle='--', linewidth=2,
                         fill=False)
        ax_1.add_patch(rect)

        # 绘制轨迹中心线
        accelerate_t = v2 / a
        constant_t = constant_time
        motionless_t = stay_time
        period = 4 * accelerate_t + 2 * motionless_t + 2 * constant_t
        # 设置图层属性
        ax_2.set_xlim((-200, period * 3 * v1 + between))
        ax_2.set_ylim((-200, a * (v2 / a) ** 2 + v2 * constant_t + 600))
        ax_2.set_aspect('equal', adjustable='box')
        # 设置图片文本
        ani_text = ax_2.text(0.7, 0.82, '', transform=ax_2.transAxes, fontsize=10, color='white')
        ani_text.set_text('Same_grinding_num=%.0f' % float(num))
        num_two = math.ceil(num / 2)
        color_7 = ['red', 'orange', 'green', 'cyan', 'blue', 'purple', 'yellow', 'lightgreen',
                   'slategrey', 'cornflowerblue', 'navy', 'indigo', 'violet', 'plum', 'oldlace', 'maroon',
                   'lightcyan', 'lightseagreen', 'seagreen', 'springgreen']  # 红橙黄绿青蓝紫
        all_time_n = math.floor(period / 0.01) * 3
        for i in range(0, num_two):
            ax_2.scatter(single_X_location[0, 0:all_time_n - 1] + i * beam_between - i * delay_time * v1,
                         single_Y_location[0, 0:all_time_n - 1],
                         color=color_7[i], s=1)
            ax_2.scatter(single_X_location[0,
                         0:all_time_n - 1] + i * beam_between + between - i * delay_time * v1,
                         single_Y_location[0, 0:all_time_n - 1],
                         color=color_7[i], s=1)
        self.canvas.draw()
    '''
    def double_enerage_project(self, v1, ceramic_width, between, beam_between, R, a, mo):
        self.worker_thread = Double_enerage_WorkerThread(v1, ceramic_width, between, beam_between, R, a,mo)
        self.worker_thread.result_signal.connect(self.update_result_double_enerage_project)  # 连接子线程的信号
        self.worker_thread.start()  # 启动子线程

    def update_result_double_enerage_project(self, result):
        result_1 = result[0]
        result_2 = result[1]
        # 计算结果
        result_P_d_matrix, result_P_d_par, single_X_location, single_Y_location = result_1
        # 参数继承
        ceramic_width = float(result_2["ceramic_width"])
        between = float(result_2["between"])
        beam_between = float(result_2["beam_between"])
        num = float(result_2["num"])
        delay_time = float(result_2["delay_time"])
        v1 = float(result_2["v1"])
        v2 = float(result_2["v2"])
        a = float(result_2["a"])
        # ---------绘制组合图-----------
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置微软雅黑字体
        plt.rcParams['axes.unicode_minus'] = False  # 避免坐标轴不能正常的显示负号
        # 清空画布
        self.canvas.fig.clear()
        ax_1 = self.canvas.fig.add_subplot(211)
        ax_2 = self.canvas.fig.add_subplot(212)
        # 设置画布背景、刻度、字体颜色
        deep_blue = (31 / 255, 55 / 255, 96 / 255)
        list = [ax_1, ax_2]
        for ax in list:
            # 设置 子图背景颜色
            ax.set_facecolor(deep_blue)
            # 设置坐标轴线的颜色为白色
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            # 设置坐标轴的刻度颜色为白色
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            # 设置坐标轴标签的颜色为白色
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            # 设置坐标轴标题字体颜色为白色
            ax.title.set_color('white')
            # 设置 子图 标签
            ax.set_xlabel('主皮带进给方向')
            ax.set_ylabel('横梁摆动方向')
        # 绘制抛磨量分布仿真
        ax_1.set_aspect('equal', adjustable='box')
        object_matrix = result_P_d_matrix
        # 设置权重操作
        max_set = np.max(object_matrix)
        # 计算第90百分位的阈值（前15%）
        percentile_85 = np.percentile(object_matrix, 85)
        # 对矩阵中大于等于该阈值的元素乘以0.85
        object_matrix[object_matrix >= percentile_85] *= 0.85

        im = ax_1.contourf(object_matrix, levels=15, alpha=1, cmap='jet', vmin=0, vmax=max_set)

        divider = make_axes_locatable(ax_1)
        cax = divider.append_axes("right", size="5%", pad=0.1)

        colorbar = plt.colorbar(im, cax=cax)

        colorbar.ax.tick_params(labelcolor='white')  # 设置刻度标签颜色
        colorbar.set_label('抛磨量大小', color='white')  # 设置 colorbar 标签的颜色
        # 绘制矩形线框
        ceramic_width_ = float(ceramic_width) * 0.1
        width, length = np.shape(object_matrix)

        x_begin = 0
        y_begin = (width - ceramic_width_) / 2

        rect = Rectangle((x_begin, y_begin), length - 1, ceramic_width_, edgecolor='red', linestyle='--', linewidth=2,
                         fill=False)
        ax_1.add_patch(rect)
        # 绘制轨迹中心线
        accelerate_t = v2 / a
        constant_t = float(result_2["constant_time"])
        motionless_t = float(result_2["stay_time"])
        period = 4 * accelerate_t + 2 * motionless_t + 2 * constant_t
        # 设置图层属性
        ax_2.set_xlim((-200, period * 3 * v1 + between))
        ax_2.set_ylim((-200, a * (v2 / a) ** 2 + v2 * constant_t + 600))
        ax_2.set_aspect('equal', adjustable='box')
        # 设置图片文本
        ani_text = ax_2.text(0.7, 0.82, '', transform=ax_2.transAxes, fontsize=10, color='white')
        ani_text.set_text('Same_grinding_num=%.0f' % float(num))
        num_two = math.ceil(num / 2)
        color_7 = ['red', 'orange', 'green', 'cyan', 'blue', 'purple', 'yellow', 'lightgreen',
                   'slategrey', 'cornflowerblue', 'navy', 'indigo', 'violet', 'plum', 'oldlace', 'maroon',
                   'lightcyan', 'lightseagreen', 'seagreen', 'springgreen']  # 红橙黄绿青蓝紫
        all_time_n = math.floor(period / 0.01) * 3
        for i in range(0, num_two):
            ax_2.scatter(single_X_location[0, 0:all_time_n - 1] + i * beam_between - i * delay_time * v1,
                         single_Y_location[0, 0:all_time_n - 1],
                         color=color_7[i], s=1)
            ax_2.scatter(single_X_location[0,
                         0:all_time_n - 1] + i * beam_between + between - i * delay_time * v1,
                         single_Y_location[0, 0:all_time_n - 1],
                         color=color_7[i], s=1)
        self.canvas.draw()

    def double_efficient_project(self):
        # self.canvas.figure.add_subplot(211).clear()
        # self.canvas.figure.add_subplot(212).clear()
        self.canvas.figure.clear()
        self.canvas.draw()  # 更新显示新的绘图内容
    # def double_self_project(self):
    #
    # # 双头摆-人工寻优逻辑函数
    # def double_synchronization_project(self):
    #
    # def double_cross_project(self):
    #
    # def double_order_project(self):
