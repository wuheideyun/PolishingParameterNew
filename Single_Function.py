# 单头摆函数汇总
import os

import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import time as te
import multiprocessing
from matplotlib.patches import Rectangle  # 导入 Rectangle
from PySide6.QtCore import Qt, Signal, QThread
from matplotlib.patches import Circle
from matplotlib import animation
from PIL import Image, ImageSequence
# 四种模式合并

# 静态动画绘制
'''
class SingleWorkerThread(QThread):
    result_signal = Signal(object)  # 创建一个信号用于传递结果
    def __init__(self,**kwargs):
        super().__init__()
        # 选择绘图模式
        self.mode = kwargs.get('mode', None)
        # 抛磨量 + 轨迹中心线 画布
        self.fig_1 = kwargs.get('fig', None)
        self.fig_1.clf()

        # # 轨迹动画 画布（暂时屏蔽）
        # self.fig_2 = plt.figure('运行轨迹动画', figsize=(10, 7))
        # deep_blue = (31 / 255, 55 / 255, 96 / 255)
        # self.fig_2.patch.set_facecolor(deep_blue)

        # 新增轨迹动画图片画布
        self.fig_2 = kwargs.get('fig_2', None)
        self.fig_2.clf()
        deep_blue = (31 / 255, 55 / 255, 96 / 255)
        self.fig_2.patch.set_facecolor(deep_blue)

        # 输入参数
        self.v1 = kwargs.get('lineEdit_belt_speed', 0)
        self.v2 = kwargs.get('lineEdit_beam_swing_speed', 0)
        self.constant_time = kwargs.get('lineEdit_beam_constant_time', 0)

        self.a = kwargs.get('lineEdit_accelerate', 650)
        self.between = kwargs.get('lineEdit_between', 0)
        self.beam_between = kwargs.get('lineEdit_beam_between', 0)

        if self.mode == 'self_order':
            self.stay_time = kwargs.get('lineEdit_stay_time_input', 0)
            self.num = round(kwargs.get('lineEdit_num_input', 0))
        else:
            self.stay_time = kwargs.get('lineEdit_stay_time_output', 0)
            self.num = round(kwargs.get('lineEdit_num_output', 0))

        self.R = kwargs.get('R', 270)
        self.mo = kwargs.get('lineEdit_grind_length', 150)
        self.ceramic_width = kwargs.get('lineEdit_ceramic_width', 800)
        # 顺序摆参数
        self.delay_time = kwargs.get('lineEdit_delay_time', 0)
        # 自定义计算参数
        self.group = kwargs.get('lineEdit_group_count', 1)

        self.animation_name = kwargs.get('animation_name', 0)

    def check_animation_gif(self, animation_name):
        # 定义文件路径
        file_path = os.path.join(os.getcwd(), 'animation', animation_name + '.gif')

        # 判断文件是否存在
        return os.path.isfile(file_path)
    def run(self):
        # 抛磨量分布矩阵
        PDT = PolishingDistributionThread(mode=self.mode, v1=self.v1, v2=self.v2, constant_time=self.constant_time, stay_time=self.stay_time
                                          , a=self.a, between=self.between, beam_between=self.beam_between, mo=self.mo,delay_time=self.delay_time
                                          , num=self.num, R=self.R, group=self.group)
        object_matrix, result = PDT.emit()
        # 轨迹中心线坐标信息
        MLP = MiddleLinePlot(v1=self.v1, v2=self.v2, constant_time=self.constant_time, stay_time=self.stay_time
                             , a=self.a, between=self.between, beam_between=self.beam_between, delay_time=self.delay_time
                             , num=self.num, group=self.group)
        single_X_location, single_Y_location = MLP.inner_calculate()
        # 轨迹动画生成
        if self.mode == 'self_order':
            mode_an = 'order'
        else:
            mode_an = self.mode
        # 暂时屏蔽动画文件检索判断
        # if not self.check_animation_gif(self.animation_name):
        #     AP = AnimationProduce(mode=mode_an, fig=self.fig_2, v1=self.v1, v2=self.v2, constant_time=self.constant_time, stay_time=self.stay_time
        #                           ,delay_time=self.delay_time, a=self.a, between=self.between, beam_between=self.beam_between, num=self.num
        #                           , R=self.R, group=self.group, animation_name=self.animation_name)
        #     animation = AP.emit()
        #     print('单头动画不存在')
        # else:
        #     print('单头动画已经存在')
        #     plt.close('运行轨迹动画')

        # 新增静态图片绘制部分
        AP = AnimationProduce(mode=mode_an, fig=self.fig_2, v1=self.v1, v2=self.v2, constant_time=self.constant_time, stay_time=self.stay_time
                              ,delay_time=self.delay_time, a=self.a, between=self.between, beam_between=self.beam_between, num=self.num
                              , R=self.R, group=self.group, animation_name=self.animation_name)
        animation = AP.emit()

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置微软雅黑字体
        plt.rcParams['axes.unicode_minus'] = False             # 避免坐标轴不能正常地显示负号
        # 设置
        ax_1 = self.fig_1.add_subplot(211)
        ax_2 = self.fig_1.add_subplot(212)
        self.fig_1.subplots_adjust(hspace=0.5)
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
        # ----------------------抛磨量分布绘图------------------
        ax_1.set_aspect('equal', adjustable='box')
        # 设置权重操作
        max_set = np.max(object_matrix)
        # 计算第90百分位的阈值（前15%）
        percentile_85 = np.percentile(object_matrix, 85)
        # 对矩阵中大于等于该阈值的元素乘以0.85
        object_matrix[object_matrix >= percentile_85] *= 0.85

        im = ax_1.contourf(object_matrix, levels=15, alpha=1, cmap='jet', vmin=0, vmax=max_set)

        divider = make_axes_locatable(ax_1)
        cax = divider.append_axes("right", size="5%", pad=0.1)

        #colorbar = self.canvas.fig.colorbar(im, cax=cax)
        colorbar = self.fig_1.colorbar(im, cax=cax)

        colorbar.ax.tick_params(labelcolor='white')  # 设置刻度标签颜色
        colorbar.set_label('抛磨量大小', color='white')  # 设置 colorbar 标签的颜色
        # 绘制矩形线框
        ceramic_width_ = float(self.ceramic_width) * 0.1
        width, length = np.shape(object_matrix)
        x_begin = 0
        y_begin = (width - ceramic_width_) / 2
        rect = Rectangle((x_begin, y_begin), length - 1, ceramic_width_, edgecolor='red', linestyle='--', linewidth=2,
                         fill=False)
        ax_1.add_patch(rect)

        # ----------------------中心线绘图------------------
        accelerate_t = self.v2 / self.a
        period = 4 * accelerate_t + 2 * self.stay_time + 2 * self.constant_time
        # 设置图层属性
        ax_2.set_xlim((-200, period * 3 * self.v1 + self.between))
        ax_2.set_ylim((-200, self.a * (self.v2 / self.a) ** 2 + self.v2 * self.constant_time + 600))
        ax_2.set_aspect('equal', adjustable='box')
        # 设置图片文本
        ani_text = ax_2.text(0.7, 0.82, '', transform=ax_2.transAxes, fontsize=10, color='white')
        ani_text.set_text('Same_grinding_num=%.0f' % float(self.num))
        num_two = math.ceil(self.num / 2)
        color_7 = ['red', 'orange', 'green', 'cyan', 'blue', 'purple', 'yellow', 'lightgreen',
                   'slategrey', 'cornflowerblue', 'navy', 'indigo', 'violet', 'plum', 'oldlace', 'maroon',
                   'lightcyan', 'lightseagreen', 'seagreen', 'springgreen']  # 红橙黄绿青蓝紫
        all_time_n = math.floor(period / 0.01) * 3
        cross_size = round((self.v2/self.a + self.constant_time + self.stay_time + self.v2/self.a) / 0.01)

        if self.mode == 'equal':
            for i in range(0, self.num):
                ax_2.scatter(single_X_location + i * self.beam_between, single_Y_location,
                             color=color_7[i], s=1)
            # self.canvas.draw()
        elif self.mode == 'cross':
            for i in range(0, self.num):
                if (i + 2) % 2 == 0:
                    ax_2.scatter(single_X_location[0, 0:all_time_n - 1] + i * self.beam_between,
                                 single_Y_location[0, 0:all_time_n - 1],
                                 color=color_7[i], s=1)
                # 横梁数为偶数
                else:
                    ax_2.scatter(single_X_location[0, 0:all_time_n - cross_size] + i * self.beam_between,
                                 single_Y_location[0, cross_size - 1:all_time_n - 1],
                                 color=color_7[i], s=1)
            # self.canvas.draw()
        elif self.mode == 'order':
            for i in range(0, self.num):
                ax_2.scatter(single_X_location[0, 0:all_time_n - 1] + i * self.beam_between - i * self.delay_time * self.v1,
                             single_Y_location[0, 0:all_time_n - 1],
                             color=color_7[i], s=1)
            # self.canvas.draw()
        elif self.mode == 'self_order':
            self_delay_distance = self.between / self.group
            index = 0
            for i in range(0, self.group):
                for j in range(0, self.num):
                    ax_2.scatter(single_X_location[0,
                                 0:all_time_n - 1] + j * self.beam_between - j * self.delay_time * self.v1 + self_delay_distance * i,
                                 single_Y_location[0, 0:all_time_n - 1],
                                 color=color_7[index], s=1)
                    index += 1
            # self.canvas.draw()
        else:
            raise ValueError('mode must be equal or cross or order or self_order')
        # print(animation+'~~~~~~~~~~~')
        data = [result,self.animation_name]
        self.result_signal.emit(data)  # 发射信号将结果传回主线程
'''
# 动态动画绘制
class SingleWorkerThread(QThread):
    result_signal = Signal(object)  # 创建一个信号用于传递结果
    def __init__(self,**kwargs):
        super().__init__()
        # 选择绘图模式
        self.mode = kwargs.get('mode', None)
        # 抛磨量 + 轨迹中心线 画布
        self.fig_1 = kwargs.get('fig', None)
        self.fig_1.clf()

        # 轨迹动画 画布
        self.fig_2 = plt.figure('运行轨迹动画', figsize=(10, 7))
        deep_blue = (31 / 255, 55 / 255, 96 / 255)
        self.fig_2.patch.set_facecolor(deep_blue)

        # 输入参数
        self.v1 = kwargs.get('lineEdit_belt_speed', 0)
        self.v2 = kwargs.get('lineEdit_beam_swing_speed', 0)
        self.constant_time = kwargs.get('lineEdit_beam_constant_time', 0)

        self.a = kwargs.get('lineEdit_accelerate', 650)
        self.between = kwargs.get('lineEdit_between', 0)
        self.beam_between = kwargs.get('lineEdit_beam_between', 0)

        if self.mode == 'self_order':
            self.stay_time = kwargs.get('lineEdit_stay_time_input', 0)
            self.num = round(kwargs.get('lineEdit_num_input', 0))
        else:
            self.stay_time = kwargs.get('lineEdit_stay_time_output', 0)
            self.num = round(kwargs.get('lineEdit_num_output', 0))

        self.R = kwargs.get('R', 270)
        self.mo = kwargs.get('lineEdit_grind_length', 150)
        self.ceramic_width = kwargs.get('lineEdit_ceramic_width', 800)
        # 顺序摆参数
        self.delay_time = kwargs.get('lineEdit_delay_time', 0)
        # 自定义计算参数
        self.group = kwargs.get('lineEdit_group_count', 1)

        self.animation_name = kwargs.get('animation_name', 0)

    def check_animation_gif(self, animation_name):
        # 定义文件路径
        file_path = os.path.join(os.getcwd(), 'animation', animation_name + '.gif')

        # 判断文件是否存在
        return os.path.isfile(file_path)
    def run(self):
        # 抛磨量分布矩阵
        PDT = PolishingDistributionThread(mode=self.mode, v1=self.v1, v2=self.v2, constant_time=self.constant_time, stay_time=self.stay_time
                                          , a=self.a, between=self.between, beam_between=self.beam_between, mo=self.mo,delay_time=self.delay_time
                                          , num=self.num, R=self.R, group=self.group)
        object_matrix, result = PDT.emit()
        # 轨迹中心线坐标信息
        MLP = MiddleLinePlot(v1=self.v1, v2=self.v2, constant_time=self.constant_time, stay_time=self.stay_time
                             , a=self.a, between=self.between, beam_between=self.beam_between, delay_time=self.delay_time
                             , num=self.num, group=self.group)
        single_X_location, single_Y_location = MLP.inner_calculate()
        # 轨迹动画生成
        if self.mode == 'self_order':
            mode_an = 'order'
        else:
            mode_an = self.mode
        # 动画文件检索判断
        if not self.check_animation_gif(self.animation_name):
            AP = AnimationProduce(mode=mode_an, fig=self.fig_2, v1=self.v1, v2=self.v2, constant_time=self.constant_time, stay_time=self.stay_time
                                  ,delay_time=self.delay_time, a=self.a, between=self.between, beam_between=self.beam_between, num=self.num
                                  , R=self.R, group=self.group, animation_name=self.animation_name)
            animation = AP.emit()
            print('单头动画不存在')
        else:
            print('单头动画已经存在')
            plt.close('运行轨迹动画')

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置微软雅黑字体
        plt.rcParams['axes.unicode_minus'] = False             # 避免坐标轴不能正常地显示负号
        # 设置
        ax_1 = self.fig_1.add_subplot(211)
        ax_2 = self.fig_1.add_subplot(212)
        self.fig_1.subplots_adjust(hspace=0.5)
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
        # ----------------------抛磨量分布绘图------------------
        ax_1.set_aspect('equal', adjustable='box')
        # 设置权重操作
        max_set = np.max(object_matrix)
        # 计算第90百分位的阈值（前15%）
        percentile_85 = np.percentile(object_matrix, 85)
        # 对矩阵中大于等于该阈值的元素乘以0.85
        object_matrix[object_matrix >= percentile_85] *= 0.85

        im = ax_1.contourf(object_matrix, levels=15, alpha=1, cmap='jet', vmin=0, vmax=max_set)

        divider = make_axes_locatable(ax_1)
        cax = divider.append_axes("right", size="5%", pad=0.1)

        #colorbar = self.canvas.fig.colorbar(im, cax=cax)
        colorbar = self.fig_1.colorbar(im, cax=cax)

        colorbar.ax.tick_params(labelcolor='white')  # 设置刻度标签颜色
        colorbar.set_label('抛磨量大小', color='white')  # 设置 colorbar 标签的颜色
        # 绘制矩形线框
        ceramic_width_ = float(self.ceramic_width) * 0.1
        width, length = np.shape(object_matrix)
        x_begin = 0
        y_begin = (width - ceramic_width_) / 2
        rect = Rectangle((x_begin, y_begin), length - 1, ceramic_width_, edgecolor='red', linestyle='--', linewidth=2,
                         fill=False)
        ax_1.add_patch(rect)

        # ----------------------中心线绘图------------------
        accelerate_t = self.v2 / self.a
        period = 4 * accelerate_t + 2 * self.stay_time + 2 * self.constant_time
        # 设置图层属性
        ax_2.set_xlim((-200, period * 3 * self.v1 + self.between))
        ax_2.set_ylim((-200, self.a * (self.v2 / self.a) ** 2 + self.v2 * self.constant_time + 600))
        ax_2.set_aspect('equal', adjustable='box')
        # 设置图片文本
        ani_text = ax_2.text(0.7, 0.82, '', transform=ax_2.transAxes, fontsize=10, color='white')
        ani_text.set_text('Same_grinding_num=%.0f' % float(self.num))
        num_two = math.ceil(self.num / 2)
        color_7 = ['red', 'orange', 'green', 'cyan', 'blue', 'purple', 'yellow', 'lightgreen',
                   'slategrey', 'cornflowerblue', 'navy', 'indigo', 'violet', 'plum', 'oldlace', 'maroon',
                   'lightcyan', 'lightseagreen', 'seagreen', 'springgreen']  # 红橙黄绿青蓝紫
        all_time_n = math.floor(period / 0.01) * 3
        cross_size = round((self.v2/self.a + self.constant_time + self.stay_time + self.v2/self.a) / 0.01)

        if self.mode == 'equal':
            for i in range(0, self.num):
                ax_2.scatter(single_X_location + i * self.beam_between, single_Y_location,
                             color=color_7[i], s=1)
            # self.canvas.draw()
        elif self.mode == 'cross':
            for i in range(0, self.num):
                if (i + 2) % 2 == 0:
                    ax_2.scatter(single_X_location[0, 0:all_time_n - 1] + i * self.beam_between,
                                 single_Y_location[0, 0:all_time_n - 1],
                                 color=color_7[i], s=1)
                # 横梁数为偶数
                else:
                    ax_2.scatter(single_X_location[0, 0:all_time_n - cross_size] + i * self.beam_between,
                                 single_Y_location[0, cross_size - 1:all_time_n - 1],
                                 color=color_7[i], s=1)
            # self.canvas.draw()
        elif self.mode == 'order':
            for i in range(0, self.num):
                ax_2.scatter(single_X_location[0, 0:all_time_n - 1] + i * self.beam_between - i * self.delay_time * self.v1,
                             single_Y_location[0, 0:all_time_n - 1],
                             color=color_7[i], s=1)
            # self.canvas.draw()
        elif self.mode == 'self_order':
            self_delay_distance = self.between / self.group
            index = 0
            for i in range(0, self.group):
                for j in range(0, self.num):
                    ax_2.scatter(single_X_location[0,
                                 0:all_time_n - 1] + j * self.beam_between - j * self.delay_time * self.v1 + self_delay_distance * i,
                                 single_Y_location[0, 0:all_time_n - 1],
                                 color=color_7[index], s=1)
                    index += 1
            # self.canvas.draw()
        else:
            raise ValueError('mode must be equal or cross or order or self_order')
        # print(animation+'~~~~~~~~~~~')
        data = [result,self.animation_name]
        self.result_signal.emit(data)  # 发射信号将结果传回主线程


# ---------------抛磨量计算（多进程）-------------
# class PolishingDistributionThread():
#     def __init__(self,**kwargs):
#         # 当前模式
#         self.mode = kwargs.get('mode', None)
#         # 基本运动参数
#         self.v1 = kwargs.get('v1', 0)
#         self.v2 = kwargs.get('v2', 0)
#         self.constant_time = kwargs.get('constant_time', 0)
#         self.stay_time = kwargs.get('stay_time', 0)
#         self.a = kwargs.get('a', 650)
#         self.between = kwargs.get('between', 0)
#         self.beam_between = kwargs.get('beam_between', 0)
#         self.num = kwargs.get('num', 0)
#         self.R = kwargs.get('R', 270)
#         self.mo = kwargs.get('mo', 150)
#         # 顺序摆参数
#         self.delay_time = kwargs.get('delay_time', 0)
#         # 自定义计算参数
#         self.group = kwargs.get('group', 0)
# 
#         self.n = 6    # 周期数目
#         self.w = 600  # 转速
# 
#         accelerate_t = round(self.v2 / self.a, 2)
# 
#         self.t1 = accelerate_t
#         self.t2 = self.constant_time
#         self.t3 = accelerate_t
#         self.t4 = self.stay_time
#         self.t5 = accelerate_t
#         self.t6 = self.constant_time
#         self.t7 = accelerate_t
#         self.t8 = self.stay_time
#         self.period = self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6 + self.t7 + self.t8
# 
#         self.c_length_cell = 10  # 统计区域长度最小单位
#         self.c_width_cell = 10  # 统计区域宽度最小单位
# 
#         # 以10*10为最小单位 ，将瓷砖离散化，以每个格子的中心作为每个格子的坐标(0.5,0.5)
#         c_length = math.ceil(self.v1 * self.period * self.n + 2 * self.R + 50)  # 统计区域长度
#         c_width = math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R + 100)  # 统计区域宽度
# 
#         self.c_length_percell = round(
#             math.ceil(self.v1 * self.period + 2 * self.R + 100) / self.c_length_cell)  # 统计区域长度方向总单元格数目
#         self.c_length_mulcell = round(c_length / self.c_length_cell)  # 统计区域长度方向总单元格数目
#         self.c_width_mulcell = round(c_width / self.c_width_cell)  # 统计区域宽度方向总单元格数目
# 
#     # 输出端口
#     def emit(self):
#         self.mod_rho, self.mod_theta = self.mod_information_calculate()
#         matrix_results = self.start_multiprocessing()
# 
#         if self.mode == 'equal':
#             object_matrix, result = self.equal_matrix_cal(matrix_results)
#         elif self.mode == 'cross':
#             object_matrix, result = self.cross_matrix_cal(matrix_results)
#         elif self.mode == 'order':
#             object_matrix, result = self.order_matrix_cal(matrix_results)
#         elif self.mode == 'self_order':
#             object_matrix, result = self.self_order_matrix_cal(matrix_results)
#         else:
#             object_matrix = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
#             result = 0
# 
#         return object_matrix, result
# 
#     def mod_information_calculate(self):
#         size = 0.01  # 时间步长
#         # 磨块离散化计算   以磨块 长 64mm 宽 110mm 为例
#         # 仅仅计算单磨头，为了减少计算量，后续磨头直接进行叠加；
#         mod_length = 64  # 磨块长度
#         mod_width = self.mo  # 磨块宽度
# 
#         mod_width_cell = 5  # 磨块单元（宽度）
#         mod_length_cell = 4  # 磨块单元（长度）
# 
#         mod_width_mulcell = math.floor(mod_width / mod_width_cell)  # 磨块宽度方向单元格总数量
#         mod_length_mulcell = math.floor(mod_length / mod_length_cell)  # 磨块长度方向单元格总数量
# 
#         mod_x = np.zeros((mod_width_mulcell, mod_length_mulcell))
#         mod_y = np.zeros((mod_width_mulcell, mod_length_mulcell))
#         # 储存坐标(仅需要极径长度和角度,以坐标原点为磨头中心)
#         for i in range(0, mod_length_mulcell):
#             mod_x[:, i] = -mod_length / 2 + mod_length_cell / 2 + (i - 1) * mod_length_cell
#         for i in range(0, mod_width_mulcell):
#             mod_y[i, :] = mod_width - mod_width_cell / 2 - (i - 1) * mod_width_cell
#         mod_y = mod_y + self.R - self.mo  # 第一个磨块位置
#         # 计算单个磨块
#         mod_rho = np.zeros((mod_width_mulcell, mod_length_mulcell))  # 储存单个磨块极径
#         mod_theta = np.zeros((mod_width_mulcell, mod_length_mulcell))  # 储存单个磨粒角度
#         # 计算磨块各个点离磨头中心距离  角度
#         for i in range(0, mod_width_mulcell):
#             for j in range(0, mod_length_mulcell):
#                 mod_rho[i, j] = (mod_x[i, j] ** 2 + mod_y[i, j] ** 2) ** 0.5
#                 mod_theta[i, j] = math.atan(mod_y[i, j] / mod_x[i, j])
#                 if mod_theta[i, j] < 0:
#                     mod_theta[i, j] = math.pi + mod_theta[i, j]
#         return mod_rho, mod_theta
# 
#     # 同步摆模式计算
#     def equal_matrix_cal(self, H_all):
#         sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
#         mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
#         H_period = H_all[:, 5:5 + sin_period]
#         H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
#         for i in range(0, self.n):
#             H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
#                                                                    i * mid_period:i * mid_period + sin_period] + H_period
#         # 多磨头叠加
#         all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
#         beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
#         for i in range(0, self.num):
#             all_H[:, beam_between_cell * i:self.c_length_mulcell - 1] = (
#                     all_H[:, beam_between_cell * i:self.c_length_mulcell - 1] +
#                     H_mid[:, 0:self.c_length_mulcell - beam_between_cell * i - 1])
#         # 计算 抛磨变异系数
#         # 如果要计算此模块，周期数必须大于等于3
#         cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
#         begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
#         terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width
#         begin_length = math.ceil((50 + self.v1 * 3 * self.period) / 10)
#         terminate_length = begin_length + math.ceil((2 * self.v1 * self.period + 2 * self.R) / 10)
#         # object_matrix = np.zeros((terminate_width - begin_width, terminate_length - begin_length))
#         object_matrix = all_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]
#         equal_subsample = np.mean(object_matrix)  # 子样平均数
#         middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
#         variance_matrix = np.mean(middle_matrix)  # 子样方差
#         result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
#         return object_matrix, result
# 
#     # 交叉摆模式计算
#     def cross_matrix_cal(self, H_all):
#         sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
#         mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
#         H_period = H_all[:, 5:5 + sin_period]
#         H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
#         for i in range(0, self.n):
#             H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
#                                                                    i * mid_period:i * mid_period + sin_period] + H_period
#         # 多磨头叠加
#         all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
#         beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
#         cross_size = round((self.t1 + self.t2 + self.t3 + self.t4) * self.v1 / self.c_length_cell)
#         for i in range(0, self.num):
#             if (i + 2) % 2 == 0:  # 第 奇数 个横梁
#                 all_H[:, beam_between_cell * i:self.c_length_mulcell - 1 - mid_period] = (
#                         all_H[:, beam_between_cell * i:self.c_length_mulcell - 1 - mid_period] +
#                         H_mid[:, 0:self.c_length_mulcell - beam_between_cell * i - 1 - mid_period])
#             else:
#                 all_H[:, beam_between_cell * i:self.c_length_mulcell - 1 - mid_period] = (
#                         all_H[:, beam_between_cell * i: self.c_length_mulcell - 1 - mid_period] +
#                         H_mid[:,
#                         cross_size: self.c_length_mulcell - 1 - beam_between_cell * i + cross_size - mid_period])
#         # 计算 抛磨变异系数
#         # 如果要计算此模块，周期数必须大于等于3
#         cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
#         begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
#         terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width
#         begin_length = math.ceil((50 + self.v1 * (self.n - 3) * self.period) / 10)
#         terminate_length = begin_length + math.ceil((2 * self.v1 * self.period + 2 * self.R) / 10)
#         # object_matrix = np.zeros((terminate_width - begin_width, terminate_length - begin_length))
#         object_matrix = all_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]
#         equal_subsample = np.mean(object_matrix)  # 子样平均数
#         middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
#         variance_matrix = np.mean(middle_matrix)  # 子样方差
#         result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
#         return object_matrix, result
# 
#     # 顺序摆模式计算
#     def order_matrix_cal(self, H_all):
#         sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
#         mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
#         H_period = H_all[:, 5:5 + sin_period]
#         H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
#         for i in range(0, self.n):
#             H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
#                                                                    i * mid_period:i * mid_period + sin_period] + H_period
#         # 多磨头叠加
#         all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
#         beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
#         delay_cell = math.floor(self.delay_time * self.v1 / self.c_length_cell)
#         for i in range(0, self.num):
#             all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] = (
#                     all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] +
#                     H_mid[:, 0:self.c_length_mulcell - (beam_between_cell - delay_cell) * i - 1])
#         # 计算 抛磨变异系数
#         # 如果要计算此模块，周期数必须大于等于3
#         cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
#         begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
#         terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width
#         begin_length = math.ceil((50 + self.v1 * 3 * self.period) / 10)
#         terminate_length = begin_length + math.ceil((2 * self.v1 * self.period + 2 * self.R) / 10)
#         object_matrix = all_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]
#         equal_subsample = np.mean(object_matrix)  # 子样平均数
#         middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
#         variance_matrix = np.mean(middle_matrix)  # 子样方差
#         result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
#         return object_matrix, result
# 
#     # 自定义模式计算
#     def self_order_matrix_cal(self, H_all):
#         sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
#         mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
#         H_period = H_all[:, 5:5 + sin_period]
#         H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
#         for i in range(0, self.n):
#             H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
#                                                                    i * mid_period:i * mid_period + sin_period] + H_period
#         # 多磨头叠加
#         delay_cell = math.floor(self.delay_time * self.v1 / self.c_length_cell)
#         all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
#         beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
#         for i in range(0, self.num):
#             all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] = (
#                     all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] +
#                     H_mid[:, 0:self.c_length_mulcell - (beam_between_cell - delay_cell) * i - 1])
#         # 组数叠加
#         group = round(self.group)
#         group_size = math.floor(self.between / group / self.c_length_cell)
#         all_group_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
#         for i in range(0, group):
#             all_group_H[:, group_size * i:self.c_length_mulcell - 1] = (
#                     all_group_H[:, group_size * i:self.c_length_mulcell - 1] +
#                     all_H[:, 0:self.c_length_mulcell - group_size * i - 1])
#         # 计算 抛磨变异系数
#         # 如果要计算此模块，周期数必须大于等于3
#         cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
#         begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
#         terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width
#         begin_length = math.ceil((50 + self.v1 * (self.n - 3) * self.period) / 10)
#         terminate_length = begin_length + math.ceil((2 * self.v1 * self.period + 2 * self.R) / 10)
#         object_matrix = all_group_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]
#         equal_subsample = np.mean(object_matrix)  # 子样平均数
#         middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
#         variance_matrix = np.mean(middle_matrix)  # 子样方差
#         result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
#         return object_matrix, result
# 
# 
#     def start_multiprocessing(self):
#         value_list=[(0, self.t1,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
#                     (self.t1, self.t1 + self.t2,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
#                     (self.t1 + self.t2, self.t1 + self.t2 + self.t3,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
#                     (self.t1 + self.t2 + self.t3, self.t1 + self.t2 + self.t3 + self.t4,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
#                     (self.t1 + self.t2 + self.t3 + self.t4, self.t1 + self.t2 + self.t3 + self.t4 + self.t5,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
#                     (self.t1 + self.t2 + self.t3 + self.t4 + self.t5,self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
#                     (self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6,self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6 + self.t7,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
#                     (self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6 + self.t7,self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6 + self.t7 + self.t8,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,)]
#         # 创建进程池(4线程)
#         with multiprocessing.Pool(processes=4) as pool:
#             # 使用 apply_async 运行不同的函数
#             results = []
#             results.append(pool.apply_async(polishing_cal, args=(value_list[0])))
#             results.append(pool.apply_async(polishing_cal, args=(value_list[1])))
#             results.append(pool.apply_async(polishing_cal, args=(value_list[2])))
#             results.append(pool.apply_async(polishing_cal, args=(value_list[3])))
#             results.append(pool.apply_async(polishing_cal, args=(value_list[4])))
#             results.append(pool.apply_async(polishing_cal, args=(value_list[5])))
#             results.append(pool.apply_async(polishing_cal, args=(value_list[6])))
#             results.append(pool.apply_async(polishing_cal, args=(value_list[7])))
#             # 关闭进程池，等待所有任务完成
#             pool.close()
#             pool.join()
#         # 提取结果并进行相加
#         matrix_results = sum(result.get() for result in results)
#         return matrix_results
# def polishing_cal(begin,end,v1,v2,constant_t,stay_t,a,R,mod_rho,mod_theta,mo):
#     accelerate_t= round(v2 / a, 2)
#     t1 = accelerate_t
#     t2 = constant_t
#     t3 = accelerate_t
#     t4 = stay_t
#     t5 = accelerate_t
#     t6 = constant_t
#     t7 = accelerate_t
#     t8 = stay_t
#     period = 4 * accelerate_t + 2 * stay_t + 2 * constant_t
#     # 计算
#     w = 600  # 转速
#     size = 0.01  # 时间步长
#     n=6
# 
#     mod_width_cell = 5  # 磨块单元（宽度）
#     mod_length_cell = 4  # 磨块单元（长度）
# 
#     c_length_cell = 10  # 统计区域长度最小单位
#     c_width_cell = 10  # 统计区域宽度最小单位
# 
#     mod_length = 64  # 磨块长度
#     mod_width = mo  # 磨块宽度
# 
#     c_width = math.ceil(v2 * t2 + a * t1 ** 2 + 2 * R + 100)  # 统计区域宽度
# 
#     c_length_percell = round(math.ceil(v1 * period + 2 * R + 100) / c_length_cell)  # 统计区域长度方向（单周期）总单元格数目
#     c_width_mulcell = round(c_width / c_width_cell)  # 统计区域宽度方向总单元格数目
# 
#     mod_width_mulcell = math.floor(mod_width / mod_width_cell)  # 磨块宽度方向单元格总数量
#     mod_length_mulcell = math.floor(mod_length / mod_length_cell)  # 磨块长度方向单元格总数量
# 
#     H = np.zeros((c_width_mulcell, c_length_percell))  # 存放速度和
#     time = np.arange(0, period, size)  # 时间变量
#     begin_time = math.floor(begin / size)  # 单周期步长
#     end_time = math.floor(end / size)  # 单周期步长
#     # 计算单个周期磨头抛磨量分布
#     for k in range(begin_time, end_time):
#         t = time[k]  # 时间
#         # 第一段
#         if t >= 0 and t < t1:
#             x_0 = v1 * t + R + 50
#             y_0 = 0.5 * a * t ** 2 + R + 50
#         elif t >= t1 and t < t1 + t2:
#         # 第二段
#             x_0 = v1 * t + R + 50
#             y_0 = 0.5 * a * t1 ** 2 + v2 * (t - t1) + R + 50
#         # 第三段
#         elif t >= (t1 + t2) and t < (t1 + t2 + t3):
#             x_0 = v1 * t + R + 50
#             y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * (t - t1 - t2) - 0.5 * a * (t - t1 - t2) ** 2 + R + 50
#         # 第四段
#         elif t >= (t1 + t2 + t3) and t < (t1 + t2 + t3 + t4):
#             x_0 = v1 * t + R + 50
#             y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 + R + 50
#         # 第五段
#         elif t >= (t1 + t2 + t3 + t4) and t < (t1 + t2 + t3 + t4 + t5):
#             x_0 = v1 * t + R + 50
#             y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * (
#                         t - t1 - t2 - t3 - t4) ** 2 + R + 50
#         # 第六段
#         elif t >= (t1 + t2 + t3 + t4 + t5) and t < (t1 + t2 + t3 + t4 + t5 + t6):
#             x_0 = v1 * t + R + 50
#             y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * t5 ** 2 - v2 * (
#                         t - t1 - t2 - t3 - t4 - t5) + R + 50
#         # 第七段
#         elif t >= (t1 + t2 + t3 + t4 + t5 + t6) and t < (t1 + t2 + t3 + t4 + t5 + t6 + t7):
#             x_0 = v1 * t + R + 50
#             y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * t5 ** 2 - v2 * t6 - v2 * (
#                         t - t1 - t2 - t3 - t4 - t5 - t6) + 0.5 * a * (t - t1 - t2 - t3 - t4 - t5 - t6) ** 2 + R + 50
#         # 第八段
#         elif t >= (t1 + t2 + t3 + t4 + t5 + t6 + t7) and t <= (t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8):
#             x_0 = v1 * t + R + 50
#             y_0 = R + 50
#         # 磨头中心速度方程
#         v_x_0 = v1
#         # 第一段
#         if t >= 0 and t < t1:
#             v_y_0 = a * t
#         # 第二段
#         elif t >= t1 and t < t1 + t2:
#             v_y_0 = a * t1
#         # 第三段
#         elif t >= t1 + t2 and t < t1 + t2 + t3:
#             v_y_0 = a * t1 - a * (t - t1 - t2)
#         # 第四段
#         elif t >= (t1 + t2 + t3) and t < (t1 + t2 + t3 + t4):
#             v_y_0 = 0
#         # 第五段
#         elif t >= (t1 + t2 + t3 + t4) and t < (t1 + t2 + t3 + t4 + t5):
#             v_y_0 = -a * (t - t1 - t2 - t3 - t4)
#         # 第六段
#         elif t >= (t1 + t2 + t3 + t4 + t5) and t < (t1 + t2 + t3 + t4 + t5 + t6):
#             v_y_0 = -a * t5
#         # 第七段
#         elif t >= (t1 + t2 + t3 + t4 + t5 + t6) and t < (t1 + t2 + t3 + t4 + t5 + t6 + t7):
#             v_y_0 = -a * t5 + a * (t - t1 - t2 - t3 - t4 - t5 - t6)
#         # 第八段
#         elif t >= (t1 + t2 + t3 + t4 + t5 + t6 + t7) and t <= (t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8):
#             v_y_0 = 0
#         # 计算磨粒
#         for i_mod in range(0, 6):  # 磨块数为1-6
#             for i_width in range(0, mod_width_mulcell):
#                 for i_length in range(0, mod_length_mulcell):
#                     r = mod_rho[i_width, i_length]
#                     theta_1 = mod_theta[i_width, i_length] + i_mod * math.pi / 3
#                     # 磨粒运动轨迹方程
#                     theta = w * math.pi / 30 * t
#                     x = r * math.cos(theta) * math.cos(theta_1) + r * math.sin(theta) * math.sin(theta_1) + x_0
#                     y = -r * math.sin(theta) * math.cos(theta_1) + r * math.cos(theta) * math.sin(theta_1) + y_0
#                     # 磨粒速度方程
#                     v_x = -r * w * math.pi / 30 * math.sin(w * math.pi / 30 * t + theta_1) - v_x_0
#                     v_y = r * w * math.pi / 30 * math.cos(w * math.pi / 30 * t + theta_1) + v_y_0
#                     v_common = ((v_x ** 2 + v_y ** 2) ** 0.5)
#                     # 判断该点所在磨削区域的单元
#                     m_x = math.ceil(x / c_length_cell)
#                     m_y = math.ceil(y / c_width_cell)
#                     H[m_y, m_x] = H[m_y, m_x] + v_common  # 统计各个磨削区域速度和
#     return H



# -----------------轨迹中心线计算----------------------

# --------------抛磨量计算（单进程）-------------------
class PolishingDistributionThread():
    def __init__(self,**kwargs):
        # 当前模式
        self.mode = kwargs.get('mode', None)
        # 基本运动参数
        self.v1 = kwargs.get('v1', 0)
        self.v2 = kwargs.get('v2', 0)
        self.constant_time = kwargs.get('constant_time', 0)
        self.stay_time = kwargs.get('stay_time', 0)
        self.a = kwargs.get('a', 650)
        self.between = kwargs.get('between', 0)
        self.beam_between = kwargs.get('beam_between', 0)
        self.num = kwargs.get('num', 0)
        self.R = kwargs.get('R', 270)
        self.mo = kwargs.get('mo', 150)
        # 顺序摆参数
        self.delay_time = kwargs.get('delay_time', 0)
        # 自定义计算参数
        self.group = kwargs.get('group', 0)

        self.n = 6    # 周期数目
        self.w = 600  # 转速

        accelerate_t = round(self.v2 / self.a, 2)

        self.t1 = accelerate_t
        self.t2 = self.constant_time
        self.t3 = accelerate_t
        self.t4 = self.stay_time
        self.t5 = accelerate_t
        self.t6 = self.constant_time
        self.t7 = accelerate_t
        self.t8 = self.stay_time
        self.period = self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6 + self.t7 + self.t8

        self.c_length_cell = 10  # 统计区域长度最小单位
        self.c_width_cell = 10  # 统计区域宽度最小单位

        # 以10*10为最小单位 ，将瓷砖离散化，以每个格子的中心作为每个格子的坐标(0.5,0.5)
        c_length = math.ceil(self.v1 * self.period * self.n + 2 * self.R + 50)  # 统计区域长度
        c_width = math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R + 100)  # 统计区域宽度

        self.c_length_percell = round(
            math.ceil(self.v1 * self.period + 2 * self.R + 100) / self.c_length_cell)  # 统计区域长度方向总单元格数目
        self.c_length_mulcell = round(c_length / self.c_length_cell)  # 统计区域长度方向总单元格数目
        self.c_width_mulcell = round(c_width / self.c_width_cell)  # 统计区域宽度方向总单元格数目

    # 输出端口
    def emit(self):
        self.mod_rho, self.mod_theta = self.mod_information_calculate()
        matrix_results = self.polishing_cal()

        if self.mode == 'equal':
            object_matrix, result = self.equal_matrix_cal(matrix_results)
        elif self.mode == 'cross':
            object_matrix, result = self.cross_matrix_cal(matrix_results)
        elif self.mode == 'order':
            object_matrix, result = self.order_matrix_cal(matrix_results)
        elif self.mode == 'self_order':
            object_matrix, result = self.self_order_matrix_cal(matrix_results)
        else:
            object_matrix = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
            result = 0

        return object_matrix, result

    def mod_information_calculate(self):
        size = 0.01  # 时间步长
        # 磨块离散化计算   以磨块 长 64mm 宽 110mm 为例
        # 仅仅计算单磨头，为了减少计算量，后续磨头直接进行叠加；
        mod_length = 64  # 磨块长度
        mod_width = self.mo  # 磨块宽度

        mod_width_cell = 5  # 磨块单元（宽度）
        mod_length_cell = 4  # 磨块单元（长度）

        mod_width_mulcell = math.floor(mod_width / mod_width_cell)  # 磨块宽度方向单元格总数量
        mod_length_mulcell = math.floor(mod_length / mod_length_cell)  # 磨块长度方向单元格总数量

        mod_x = np.zeros((mod_width_mulcell, mod_length_mulcell))
        mod_y = np.zeros((mod_width_mulcell, mod_length_mulcell))
        # 储存坐标(仅需要极径长度和角度,以坐标原点为磨头中心)
        for i in range(0, mod_length_mulcell):
            mod_x[:, i] = -mod_length / 2 + mod_length_cell / 2 + (i - 1) * mod_length_cell
        for i in range(0, mod_width_mulcell):
            mod_y[i, :] = mod_width - mod_width_cell / 2 - (i - 1) * mod_width_cell
        mod_y = mod_y + self.R - self.mo  # 第一个磨块位置
        # 计算单个磨块
        mod_rho = np.zeros((mod_width_mulcell, mod_length_mulcell))  # 储存单个磨块极径
        mod_theta = np.zeros((mod_width_mulcell, mod_length_mulcell))  # 储存单个磨粒角度
        # 计算磨块各个点离磨头中心距离  角度
        for i in range(0, mod_width_mulcell):
            for j in range(0, mod_length_mulcell):
                mod_rho[i, j] = (mod_x[i, j] ** 2 + mod_y[i, j] ** 2) ** 0.5
                mod_theta[i, j] = math.atan(mod_y[i, j] / mod_x[i, j])
                if mod_theta[i, j] < 0:
                    mod_theta[i, j] = math.pi + mod_theta[i, j]
        return mod_rho, mod_theta

    # 同步摆模式计算
    def equal_matrix_cal(self, H_all):
        sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
        mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
        H_period = H_all[:, 5:5 + sin_period]
        H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, self.n):
            H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
                                                                   i * mid_period:i * mid_period + sin_period] + H_period
        # 多磨头叠加
        all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
        for i in range(0, self.num):
            all_H[:, beam_between_cell * i:self.c_length_mulcell - 1] = (
                    all_H[:, beam_between_cell * i:self.c_length_mulcell - 1] +
                    H_mid[:, 0:self.c_length_mulcell - beam_between_cell * i - 1])
        # 计算 抛磨变异系数
        # 如果要计算此模块，周期数必须大于等于3
        cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
        begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
        terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width
        begin_length = math.ceil((50 + self.v1 * 3 * self.period) / 10)
        terminate_length = begin_length + math.ceil((2 * self.v1 * self.period + 2 * self.R) / 10)
        # object_matrix = np.zeros((terminate_width - begin_width, terminate_length - begin_length))
        object_matrix = all_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]
        equal_subsample = np.mean(object_matrix)  # 子样平均数
        middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
        variance_matrix = np.mean(middle_matrix)  # 子样方差
        result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
        return object_matrix, result

    # 交叉摆模式计算
    def cross_matrix_cal(self, H_all):
        sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
        mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
        H_period = H_all[:, 5:5 + sin_period]
        H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, self.n):
            H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
                                                                   i * mid_period:i * mid_period + sin_period] + H_period
        # 多磨头叠加
        all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
        cross_size = round((self.t1 + self.t2 + self.t3 + self.t4) * self.v1 / self.c_length_cell)
        for i in range(0, self.num):
            if (i + 2) % 2 == 0:  # 第 奇数 个横梁
                all_H[:, beam_between_cell * i:self.c_length_mulcell - 1 - mid_period] = (
                        all_H[:, beam_between_cell * i:self.c_length_mulcell - 1 - mid_period] +
                        H_mid[:, 0:self.c_length_mulcell - beam_between_cell * i - 1 - mid_period])
            else:
                all_H[:, beam_between_cell * i:self.c_length_mulcell - 1 - mid_period] = (
                        all_H[:, beam_between_cell * i: self.c_length_mulcell - 1 - mid_period] +
                        H_mid[:,
                        cross_size: self.c_length_mulcell - 1 - beam_between_cell * i + cross_size - mid_period])
        # 计算 抛磨变异系数
        # 如果要计算此模块，周期数必须大于等于3
        cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
        begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
        terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width
        begin_length = math.ceil((50 + self.v1 * (self.n - 3) * self.period) / 10)
        terminate_length = begin_length + math.ceil((2 * self.v1 * self.period + 2 * self.R) / 10)
        # object_matrix = np.zeros((terminate_width - begin_width, terminate_length - begin_length))
        object_matrix = all_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]
        equal_subsample = np.mean(object_matrix)  # 子样平均数
        middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
        variance_matrix = np.mean(middle_matrix)  # 子样方差
        result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
        return object_matrix, result

    # 顺序摆模式计算
    def order_matrix_cal(self, H_all):
        sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
        mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
        H_period = H_all[:, 5:5 + sin_period]
        H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, self.n):
            H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
                                                                   i * mid_period:i * mid_period + sin_period] + H_period
        # 多磨头叠加
        all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
        delay_cell = math.floor(self.delay_time * self.v1 / self.c_length_cell)
        for i in range(0, self.num):
            all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] = (
                    all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] +
                    H_mid[:, 0:self.c_length_mulcell - (beam_between_cell - delay_cell) * i - 1])
        # 计算 抛磨变异系数
        # 如果要计算此模块，周期数必须大于等于3
        cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
        begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
        terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width
        begin_length = math.ceil((50 + self.v1 * 3 * self.period) / 10)
        terminate_length = begin_length + math.ceil((2 * self.v1 * self.period + 2 * self.R) / 10)
        object_matrix = all_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]
        equal_subsample = np.mean(object_matrix)  # 子样平均数
        middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
        variance_matrix = np.mean(middle_matrix)  # 子样方差
        result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
        return object_matrix, result

    # 自定义模式计算
    def self_order_matrix_cal(self, H_all):
        sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
        mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
        H_period = H_all[:, 5:5 + sin_period]
        H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, self.n):
            H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
                                                                   i * mid_period:i * mid_period + sin_period] + H_period
        # 多磨头叠加
        delay_cell = math.floor(self.delay_time * self.v1 / self.c_length_cell)
        all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
        for i in range(0, self.num):
            all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] = (
                    all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] +
                    H_mid[:, 0:self.c_length_mulcell - (beam_between_cell - delay_cell) * i - 1])
        # 组数叠加
        group = round(self.group)
        group_size = math.floor(self.between / group / self.c_length_cell)
        all_group_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, group):
            all_group_H[:, group_size * i:self.c_length_mulcell - 1] = (
                    all_group_H[:, group_size * i:self.c_length_mulcell - 1] +
                    all_H[:, 0:self.c_length_mulcell - group_size * i - 1])
        # 计算 抛磨变异系数
        # 如果要计算此模块，周期数必须大于等于3
        cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
        begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
        terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width
        begin_length = math.ceil((50 + self.v1 * (self.n - 3) * self.period) / 10)
        terminate_length = begin_length + math.ceil((2 * self.v1 * self.period + 2 * self.R) / 10)
        object_matrix = all_group_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]
        equal_subsample = np.mean(object_matrix)  # 子样平均数
        middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
        variance_matrix = np.mean(middle_matrix)  # 子样方差
        result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
        return object_matrix, result

    def polishing_cal(self):
        # 赋值操作
        v1 = self.v1
        v2 = self.v2
        constant_t = self.constant_time
        stay_t = self.stay_time
        a = self.a
        R = self.R
        mod_rho = self.mod_rho
        mod_theta = self.mod_theta
        mo = self.mo
        # 计算
        accelerate_t= round(v2 / a, 2)
        t1 = accelerate_t
        t2 = constant_t
        t3 = accelerate_t
        t4 = stay_t
        t5 = accelerate_t
        t6 = constant_t
        t7 = accelerate_t
        t8 = stay_t
        period = 4 * accelerate_t + 2 * stay_t + 2 * constant_t
        # 计算
        w = 600  # 转速
        size = 0.01  # 时间步长
        n=6
        mod_width_cell = 5  # 磨块单元（宽度）
        mod_length_cell = 4  # 磨块单元（长度）

        c_length_cell = 10  # 统计区域长度最小单位
        c_width_cell = 10  # 统计区域宽度最小单位

        mod_length = 64  # 磨块长度
        mod_width = mo  # 磨块宽度

        c_width = math.ceil(v2 * t2 + a * t1 ** 2 + 2 * R + 100)  # 统计区域宽度

        c_length_percell = round(math.ceil(v1 * period + 2 * R + 100) / c_length_cell)  # 统计区域长度方向（单周期）总单元格数目
        c_width_mulcell = round(c_width / c_width_cell)  # 统计区域宽度方向总单元格数目

        mod_width_mulcell = math.floor(mod_width / mod_width_cell)  # 磨块宽度方向单元格总数量
        mod_length_mulcell = math.floor(mod_length / mod_length_cell)  # 磨块长度方向单元格总数量

        H = np.zeros((c_width_mulcell, c_length_percell))  # 存放速度和
        time = np.arange(0, period, size)  # 时间变量
        end_time = math.floor(period / size)  # 单周期步长
        # 计算单个周期磨头抛磨量分布
        for k in range(0, end_time):
            t = time[k]  # 时间
            # 第一段
            if t >= 0 and t < t1:
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t ** 2 + R + 50
            elif t >= t1 and t < t1 + t2:
            # 第二段
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t1 ** 2 + v2 * (t - t1) + R + 50
            # 第三段
            elif t >= (t1 + t2) and t < (t1 + t2 + t3):
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * (t - t1 - t2) - 0.5 * a * (t - t1 - t2) ** 2 + R + 50
            # 第四段
            elif t >= (t1 + t2 + t3) and t < (t1 + t2 + t3 + t4):
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 + R + 50
            # 第五段
            elif t >= (t1 + t2 + t3 + t4) and t < (t1 + t2 + t3 + t4 + t5):
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * (
                            t - t1 - t2 - t3 - t4) ** 2 + R + 50
            # 第六段
            elif t >= (t1 + t2 + t3 + t4 + t5) and t < (t1 + t2 + t3 + t4 + t5 + t6):
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * t5 ** 2 - v2 * (
                            t - t1 - t2 - t3 - t4 - t5) + R + 50
            # 第七段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6) and t < (t1 + t2 + t3 + t4 + t5 + t6 + t7):
                x_0 = v1 * t + R + 50
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * t5 ** 2 - v2 * t6 - v2 * (
                            t - t1 - t2 - t3 - t4 - t5 - t6) + 0.5 * a * (t - t1 - t2 - t3 - t4 - t5 - t6) ** 2 + R + 50
            # 第八段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6 + t7) and t <= (t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8):
                x_0 = v1 * t + R + 50
                y_0 = R + 50
            # 磨头中心速度方程
            v_x_0 = v1
            # 第一段
            if t >= 0 and t < t1:
                v_y_0 = a * t
            # 第二段
            elif t >= t1 and t < t1 + t2:
                v_y_0 = a * t1
            # 第三段
            elif t >= t1 + t2 and t < t1 + t2 + t3:
                v_y_0 = a * t1 - a * (t - t1 - t2)
            # 第四段
            elif t >= (t1 + t2 + t3) and t < (t1 + t2 + t3 + t4):
                v_y_0 = 0
            # 第五段
            elif t >= (t1 + t2 + t3 + t4) and t < (t1 + t2 + t3 + t4 + t5):
                v_y_0 = -a * (t - t1 - t2 - t3 - t4)
            # 第六段
            elif t >= (t1 + t2 + t3 + t4 + t5) and t < (t1 + t2 + t3 + t4 + t5 + t6):
                v_y_0 = -a * t5
            # 第七段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6) and t < (t1 + t2 + t3 + t4 + t5 + t6 + t7):
                v_y_0 = -a * t5 + a * (t - t1 - t2 - t3 - t4 - t5 - t6)
            # 第八段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6 + t7) and t <= (t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8):
                v_y_0 = 0
            # 计算磨粒
            for i_mod in range(0, 6):  # 磨块数为1-6
                for i_width in range(0, mod_width_mulcell):
                    for i_length in range(0, mod_length_mulcell):
                        r = mod_rho[i_width, i_length]
                        theta_1 = mod_theta[i_width, i_length] + i_mod * math.pi / 3
                        # 磨粒运动轨迹方程
                        theta = w * math.pi / 30 * t
                        x = r * math.cos(theta) * math.cos(theta_1) + r * math.sin(theta) * math.sin(theta_1) + x_0
                        y = -r * math.sin(theta) * math.cos(theta_1) + r * math.cos(theta) * math.sin(theta_1) + y_0
                        # 磨粒速度方程
                        v_x = -r * w * math.pi / 30 * math.sin(w * math.pi / 30 * t + theta_1) - v_x_0
                        v_y = r * w * math.pi / 30 * math.cos(w * math.pi / 30 * t + theta_1) + v_y_0
                        v_common = ((v_x ** 2 + v_y ** 2) ** 0.5)
                        # 判断该点所在磨削区域的单元
                        m_x = math.ceil(x / c_length_cell)
                        m_y = math.ceil(y / c_width_cell)
                        H[m_y, m_x] = H[m_y, m_x] + v_common  # 统计各个磨削区域速度和
        return H
# ---------------轨迹中心线---------------------
class MiddleLinePlot():
    def __init__(self,**kwargs):
        # 基本运动参数
        self.v1 = kwargs.get('v1', 0)
        self.v2 = kwargs.get('v2', 0)
        self.constant_time = kwargs.get('constant_time', 0)
        self.stay_time = kwargs.get('stay_time', 0)
        self.a = kwargs.get('a', 650)
        self.num = kwargs.get('num', 0)
        self.between = kwargs.get('between', 0)
        self.beam_between=kwargs.get('beam_between', 0)
        # 顺序摆参数
        self.delay_time = kwargs.get('delay_time', 0)
        # 自定义计算参数
        self.group = kwargs.get('group', 0)

        self.n=4
    def inner_calculate(self):
        # 参数赋值
        v1 = self.v1
        v2 = self.v2
        accelerate_t = self.v2 / self.a
        constant_t = self.constant_time
        a=self.a
        motionless_t = self.stay_time

        t1 = accelerate_t
        t2 = constant_t
        t3 = accelerate_t
        t4 = motionless_t
        t5 = accelerate_t
        t6 = constant_t
        t7 = accelerate_t
        t8 = motionless_t
        period = 4 * accelerate_t + 2 * motionless_t + 2 * constant_t
        # 正式计算
        n = self.n
        msize = 0.01
        time = np.arange(0, period, msize)  # 时间变量
        T_size = math.floor(period / msize)  # 单周期步长
        # 磨头中心坐标
        X_location = np.zeros((1, T_size))
        Y_location = np.zeros((1, T_size))
        for k in range(0, T_size):
            t = time[k]
            # 第一段
            if t >= 0 and t <= t1:
                x_0 = v1 * t
                y_0 = 0.5 * a * t ** 2
            elif t >= t1 and t <= t1 + t2:
                # 第二段
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * (t - t1)
            # 第三段
            elif t >= (t1 + t2) and t <= (t1 + t2 + t3):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * (t - t1 - t2) - 0.5 * a * (t - t1 - t2) ** 2
            # 第四段
            elif t >= (t1 + t2 + t3) and t <= (t1 + t2 + t3 + t4):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2
            # 第五段
            elif t >= (t1 + t2 + t3 + t4) and t <= (t1 + t2 + t3 + t4 + t5):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * (
                        t - t1 - t2 - t3 - t4) ** 2
            # 第六段
            elif t >= (t1 + t2 + t3 + t4 + t5) and t <= (t1 + t2 + t3 + t4 + t5 + t6):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * t5 ** 2 - v2 * (
                        t - t1 - t2 - t3 - t4 - t5)
            # 第七段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6) and t <= (t1 + t2 + t3 + t4 + t5 + t6 + t7):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * t5 ** 2 - v2 * t6 - v2 * (
                        t - t1 - t2 - t3 - t4 - t5 - t6) + 0.5 * a * (t - t1 - t2 - t3 - t4 - t5 - t6) ** 2
            # 第八段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6 + t7) and t <= (t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8):
                x_0 = v1 * t
                y_0 = 0
            X_location[0, k] = x_0
            Y_location[0, k] = y_0
        all_time_n = T_size * n
        single_X_location = np.zeros((1, all_time_n))
        single_Y_location = np.zeros((1, all_time_n))
        for i in range(0, n):
            single_X_location[0, i * T_size:(i + 1) * T_size] = X_location + period * v1 * i
            single_Y_location[0, i * T_size:(i + 1) * T_size] = Y_location
        return single_X_location,single_Y_location
    ''''
    def figure_plot(self):
        msize = 0.01
        n=self.n
        accelerate_t=self.v2/self.a
        constant_t=self.constant_t
        motionless_t=self.motionless_t
        period = 4 * accelerate_t + 2 * motionless_t + 2 * constant_t
        T_size = math.floor(period / msize)  # 单周期步长
        single_X_location, single_Y_location=self.inner_calculate()
        all_time_n = T_size * n
        # 设置图层属性
        fig=plt.figure('磨头中心轨迹曲线',figsize=(10,4))
        #fig.suptitle('磨头中心轨迹曲线')
        ax=fig.add_subplot(111)
        ax.set_xlim((-200,period * 3 * self.v1+self.between))
        ax.set_ylim((-200, self.a * (self.v2 / self.a) ** 2 + self.v2 * self.constant_t + 600))
        ax.set_aspect('equal', adjustable='box')
        # 设置图片文本
        ani_text = ax.text(0.7, 0.82, '', transform=ax.transAxes, fontsize=10)
        ani_text.set_text('Same_grinding_num=%.0f' % self.num)
        # 设置坐标轴名称
        plt.xlabel('Tile feed direction')
        plt.ylabel('Beam swing direction')
        between_cell = math.floor(self.between / self.v1 / msize)  # 间距步长
        beam_between_cell = math.floor(self.beam_between / self.v1 / msize)  # 间距步长
        num_two=math.ceil(self.num/2)
        color_7 = ['red', 'orange', 'green', 'cyan', 'blue', 'purple', 'yellow', 'lightgreen',
                        'slategrey', 'cornflowerblue', 'navy', 'indigo', 'violet', 'plum', 'oldlace', 'maroon',
                        'lightcyan', 'lightseagreen', 'seagreen', 'springgreen']  # 红橙黄绿青蓝紫
        for i in range(0, num_two):
            plt.scatter(single_X_location+ i * self.beam_between,single_Y_location,color=color_7[i],s=1)
            plt.scatter(single_X_location + i * self.beam_between + self.between,single_Y_location,color=color_7[i],s=1)
        plt.show()  # 显示函数图像
    '''
# -----------------轨迹动画计算----------------------
# 轨迹动画绘制
class AnimationProduce():
    def __init__(self,**kwargs):
        # 动画名字
        self.animation_name = kwargs.get('animation_name','donghua')
        # 子线程不支持绘图，将绘图的figure创建在主线程
        self.fig = kwargs.get('fig',None)
        # 摆动模式
        self.mode = kwargs.get('mode', None)
        # 基本运动参数
        self.v1=kwargs.get('v1', 0)
        self.v2=kwargs.get('v2', 0)
        self.t1=kwargs.get('constant_time', 0)
        self.t2=kwargs.get('stay_time', 0)
        self.a=kwargs.get('a', 650)
        self.R=kwargs.get('R', 270)
        self.between=kwargs.get('between', 650)
        self.num=kwargs.get('num', 0)
        self.beam_between=kwargs.get('beam_between', 0)
        # 顺序摆参数
        self.delay_time = kwargs.get('delay_time', 0)


        self.n=6
        self.msize=0.15
        self.delay_time_size = round(self.delay_time / self.msize)
        self.beam_between_cell = math.floor(self.beam_between / self.v1 / self.msize)  # 横梁步长
        self.cross_size=round((2 * round(self.v2/self.a,2) + self.t1 + self.t2)/self.msize)
        self.num_two = math.floor(self.num / 2)
        period = round(4 * (self.v2 / self.a) + 2 * self.t1 + 2 * self.t2, 2)
        self.all_time_n = math.floor(period / self.msize) * self.n
        self.all_time_n_1 = math.floor(period / self.msize) * (self.n-1)
        self.color_7 = ['red','orange','green','cyan','blue','purple','yellow',
                        'lightgreen','slategrey','cornflowerblue','navy','indigo','violet',
                        'plum','oldlace','maroon','lightcyan','lightseagreen','seagreen','springgreen']  # 红橙黄绿青蓝紫
        # 计算矩阵
        self.single_X_location,self.single_Y_location=self.inner_cal_matrix()
        # 创建坐标绘图区
        #self.fig = figure
        self.ax = self.fig.add_subplot(111)  # 默认111代表1*1的图的第一个子图
        # 设置坐标轴范围
        self.x_range = [-(self.num*self.between+(self.num-1)*(self.beam_between-self.between)+200),period * (self.n-4) * self.v1]
        self.ax.set_xlim(self.x_range)
        self.ax.set_ylim((-0.5 * 1.2 * ((self.a * (self.v2 / self.a) ** 2 + self.v2 * self.t1) + 2 * self.R),
                          0.5 * 1.5 * ((self.a * (self.v2 / self.a) ** 2 + self.v2 * self.t1) + 2 * self.R)))
        self.ax.set_aspect('equal', adjustable='box')
        # 设置坐标轴名称
        self.ax.set_xlabel('Tile feed direction')
        self.ax.set_ylabel('Beam swing direction')
        # 单独隐藏刻度和标签
        # self.ax.set_xticks([])         # 隐藏刻度
        self.ax.set_xticklabels([])  # 隐藏刻度标签
        #self.x_range_numtext = 0
        self.one_size=self.msize * self.v1
        # 标识符位置设定
        self.grinding_num = self.ax.text(0.7,0.90,'',transform=self.ax.transAxes,fontsize=8,color='white')
        # self.ytext_ani = self.ax.text(0.7,0.78,'',transform=self.ax.transAxes,fontsize=8,color='white')

        # 设置子图颜色
        deep_blue = (31 / 255, 55 / 255, 96 / 255)
        self.ax.set_facecolor(deep_blue)
        # 设置坐标轴线的颜色为白色
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        # 设置坐标轴的刻度颜色为白色
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        # 设置坐标轴标签的颜色为白色
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        # 设置坐标轴标题字体颜色为白色
        self.ax.title.set_color('white')

    def inner_cal_matrix(self):
        v1=self.v1
        v2=self.v2
        constant_t=self.t1
        motionless_t=self.t2
        a=self.a
        between=self.between
        msize=self.msize
        accelerate_t = round(v2 / a, 2)
        t1=accelerate_t
        t2=constant_t
        t3=accelerate_t
        t4=motionless_t
        t5=accelerate_t
        t6=constant_t
        t7=accelerate_t
        t8=motionless_t
        period=4*accelerate_t+2*motionless_t+2*constant_t
        # 正式计算
        n=self.n
        between_cell=math.floor(between/v1/msize)    # 间距步长
        time=np.arange(0,period,msize)               # 时间变量
        T_size=math.floor(period/msize)              # 单周期步长
        # 磨头中心坐标
        X_location=np.zeros((1,T_size))
        Y_location=np.zeros((1,T_size))
        for k in range(0,T_size):
            t=time[k]
            # 第一段
            if t >= 0 and t < t1:
                x_0 = v1 * t
                y_0 = 0.5 * a * t ** 2
            elif t >= t1 and t < t1 + t2:
                # 第二段
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * (t - t1)
            # 第三段
            elif t >= (t1 + t2) and t < (t1 + t2 + t3):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * (t - t1 - t2) - 0.5 * a * (t - t1 - t2) ** 2
            # 第四段
            elif t >= (t1 + t2 + t3) and t < (t1 + t2 + t3 + t4):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2
            # 第五段
            elif t >= (t1 + t2 + t3 + t4) and t < (t1 + t2 + t3 + t4 + t5):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * (
                            t - t1 - t2 - t3 - t4) ** 2
            # 第六段
            elif t >= (t1 + t2 + t3 + t4 + t5) and t < (t1 + t2 + t3 + t4 + t5 + t6):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * t5 ** 2 - v2 * (
                            t - t1 - t2 - t3 - t4 - t5)
            # 第七段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6) and t < (t1 + t2 + t3 + t4 + t5 + t6 + t7):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * t5 ** 2 - v2 * t6 - v2 * (
                            t - t1 - t2 - t3 - t4 - t5 - t6) + 0.5 * a * (t - t1 - t2 - t3 - t4 - t5 - t6) ** 2
            # 第八段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6 + t7) and t <= (t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8):
                x_0 = v1 * t
                y_0 = 0
            X_location[0,k] = x_0
            Y_location[0,k] = y_0
        all_time_n=T_size*n
        single_X_location=np.zeros((1,all_time_n))
        single_Y_location=np.zeros((1,all_time_n))
        for i in range(0,n):
            single_X_location[0,i*T_size:(i+1)*T_size] = X_location+period*v1*i
            single_Y_location[0,i*T_size:(i+1)*T_size] = Y_location
        return single_X_location, single_Y_location
    # 同步摆动动画更新函数
    def equal_update(self,j):
        self.x_range[0] -= self.one_size
        self.x_range[1] -= self.one_size
        self.ax.set_xlim(self.x_range)
        # 绘制x、y、num的标识(坐标信息相对不移动)
        self.grinding_num.set_text('Same_grinding_num=%.0f' % self.num)
        # self.xtext_ani.set_text('x_location=%.3f mm' % (self.single_X_location[0, j]))
        # self.ytext_ani.set_text(
        #     'y_location=%.3f mm' % (self.single_Y_location[0, j] - 0.5 * (self.v2 ** 2 / self.a + self.v2 * self.t1)))
        # 绘制抛光轨迹进行叠加
        patches = []
        for i in range(0, self.num):
            circle_1 = Circle(xy=(-(self.single_X_location[0, j] + i * self.beam_between),
                                  self.single_Y_location[0, j] - 0.5 * (self.v2 ** 2 / self.a + self.v2 * self.t1)),
                              radius=self.R, alpha=0.05,
                              color=self.color_7[i])
            self.ax.add_patch(circle_1)
            patches.append(circle_1)
        # return [self.grinding_num, self.xtext_ani, self.ytext_ani] + patches
        return [self.grinding_num] + patches # 去掉y轴坐标变化

    # 交叉摆动动画更新函数
    def cross_update(self, j):
        # 设置坐标轴移动
        self.x_range[0] -= self.one_size
        self.x_range[1] -= self.one_size
        self.ax.set_xlim(self.x_range)
        # 绘制x、y、num的标识(坐标信息相对不移动)
        self.grinding_num.set_text('Same_grinding_num=%.0f' % self.num)
        # self.xtext_ani.set_text('x_location=%.3f mm' % (self.single_X_location[0, j]))
        # self.ytext_ani.set_text(
        #     'y_location=%.3f mm' % (self.single_Y_location[0, j] - 0.5 * (self.v2 ** 2 / self.a + self.v2 * self.t1)))
        # 绘制抛光轨迹进行叠加
        patches = []
        for i in range(0, self.num):
            # 横梁数为奇数
            if (i + 2) % 2 == 0:
                circle_1 = Circle(xy=(-(self.single_X_location[0, j] + i * self.beam_between),
                                      self.single_Y_location[0, j] - 0.5 * (self.v2 ** 2 / self.a + self.v2 * self.t1)),
                                  radius=self.R, alpha=0.05,
                                  color=self.color_7[i])
            # 横梁数为偶数
            else:
                circle_1 = Circle(xy=(-(self.single_X_location[0, j] + i * self.beam_between),
                                      self.single_Y_location[0, j + self.cross_size] - 0.5 * (
                                                  self.v2 ** 2 / self.a + self.v2 * self.t1)), radius=self.R,
                                  alpha=0.05,
                                  color=self.color_7[i])
            self.ax.add_patch(circle_1)
            patches.append(circle_1)
        # return [self.grinding_num, self.xtext_ani, self.ytext_ani] + patches
        return [self.grinding_num] + patches # 去掉 y 轴坐标变化

    # 顺序摆动动画更新函数
    def order_update(self, j):
        # 设置坐标轴移动
        self.x_range[0] -= self.one_size
        self.x_range[1] -= self.one_size
        self.ax.set_xlim(self.x_range)
        # 绘制x、y、num的标识(坐标信息相对不移动)
        self.grinding_num.set_text('Same_grinding_num=%.0f' % self.num)
        # self.xtext_ani.set_text('x_location=%.3f mm' % (self.single_X_location[0, j]))
        # self.ytext_ani.set_text(
        #     'y_location=%.3f mm' % (self.single_Y_location[0, j] - 0.5 * (self.v2 ** 2 / self.a + self.v2 * self.t1)))
        # 绘制抛光轨迹进行叠加
        patches = []
        for i in range(0, self.num):
            # 延时绘制效果
            if j >= self.delay_time_size * i:
                circle_1 = Circle(xy=(-(self.single_X_location[0, j] + (self.num - i - 1) * self.beam_between),
                                      self.single_Y_location[0, j - self.delay_time_size * i] - 0.5 * (
                                                  self.v2 ** 2 / self.a + self.v2 * self.t1)),
                                  radius=self.R, alpha=0.05,
                                  color=self.color_7[i])
                self.ax.add_patch(circle_1)
                patches.append(circle_1)
        # return [self.grinding_num, self.xtext_ani, self.ytext_ani] + patches
        return [self.grinding_num] + patches # 去掉 y 轴坐标变化


    def emit(self):
        if self.mode == 'equal':
            An_fun = self.equal_update
        elif self.mode == 'cross':
            An_fun = self.cross_update
        elif self.mode == 'order':
            An_fun = self.order_update
        else:
            raise ValueError('mode must be equal or cross or order')
        ani = animation.FuncAnimation(self.fig, An_fun, frames=self.all_time_n_1, interval=100, repeat=False)

        ani.save('animation/' + self.animation_name + '.gif', fps=30, writer='pillow')
        # 动画分割
        input_gif = 'animation/' + self.animation_name + '.gif'
        split_frames = int(self.all_time_n / self.n * 3)
        output_gif_1 = 'animation/' + self.animation_name + '_1' + '.gif'
        output_gif_2 = 'animation/' + self.animation_name + '_2' + '.gif'
        split_gif(input_gif, split_frames, output_gif_1, output_gif_2)
        plt.close(self.fig)
        return (self.animation_name)

# 静态动画绘制
'''
class AnimationProduce():
    def __init__(self,**kwargs):
        # 动画名字
        self.animation_name = kwargs.get('animation_name','donghua')
        # 子线程不支持绘图，将绘图的figure创建在主线程
        self.fig = kwargs.get('fig',None)
        # 摆动模式
        self.mode = kwargs.get('mode', None)
        # 基本运动参数
        self.v1=kwargs.get('v1', 0)
        self.v2=kwargs.get('v2', 0)
        self.t1=kwargs.get('constant_time', 0)
        self.t2=kwargs.get('stay_time', 0)
        self.a=kwargs.get('a', 650)
        self.R=kwargs.get('R', 270)
        self.between=kwargs.get('between', 650)
        self.num=kwargs.get('num', 0)
        self.beam_between=kwargs.get('beam_between', 0)
        # 顺序摆参数
        self.delay_time = kwargs.get('delay_time', 0)


        self.n=6
        self.msize=0.15
        self.delay_time_size = round(self.delay_time / self.msize)
        self.beam_between_cell = math.floor(self.beam_between / self.v1 / self.msize)  # 横梁步长
        self.cross_size=round((2 * round(self.v2/self.a,2) + self.t1 + self.t2)/self.msize)
        self.num_two = math.floor(self.num / 2)
        period = round(4 * (self.v2 / self.a) + 2 * self.t1 + 2 * self.t2, 2)
        self.all_time_n = math.floor(period / self.msize) * self.n
        self.all_time_n_1 = math.floor(period / self.msize) * (self.n-1)
        self.color_7 = ['red','orange','green','cyan','blue','purple','yellow',
                        'lightgreen','slategrey','cornflowerblue','navy','indigo','violet',
                        'plum','oldlace','maroon','lightcyan','lightseagreen','seagreen','springgreen']  # 红橙黄绿青蓝紫
        # 计算矩阵
        self.single_X_location,self.single_Y_location=self.inner_cal_matrix()
        # 创建坐标绘图区
        #self.fig = figure
        self.ax = self.fig.add_subplot(111)  # 默认111代表1*1的图的第一个子图
        # 设置坐标轴范围
        # self.x_range = [-(self.num*self.between+(self.num-1)*(self.beam_between-self.between)+200),period * (self.n-4) * self.v1]  （轨迹动画，暂时屏蔽）
        # self.ax.set_xlim(self.x_range)

        self.ax.set_xlim([-540,self.v1*period*3.5])
        self.ax.set_ylim((-0.5 * 1.3 * ((self.a * (self.v2 / self.a) ** 2 + self.v2 * self.t1) + 2 * self.R),
                          0.5 * 1.5 * ((self.a * (self.v2 / self.a) ** 2 + self.v2 * self.t1) + 2 * self.R)))
        self.ax.set_aspect('equal', adjustable='box')
        # 设置坐标轴名称
        self.ax.set_xlabel('Tile feed direction')
        self.ax.set_ylabel('Beam swing direction')
        # 单独隐藏刻度和标签
        # self.ax.set_xticks([])         # 隐藏刻度
        self.ax.set_xticklabels([])  # 隐藏刻度标签
        #self.x_range_numtext = 0
        self.one_size=self.msize * self.v1
        # 标识符位置设定
        self.grinding_num = self.ax.text(0.7,0.90,'',transform=self.ax.transAxes,fontsize=8,color='white')
        self.ytext_ani = self.ax.text(0.7,0.78,'',transform=self.ax.transAxes,fontsize=8,color='white')

        # 设置子图颜色
        deep_blue = (31 / 255, 55 / 255, 96 / 255)
        self.ax.set_facecolor(deep_blue)
        # 设置坐标轴线的颜色为白色
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        # 设置坐标轴的刻度颜色为白色
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        # 设置坐标轴标签的颜色为白色
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        # 设置坐标轴标题字体颜色为白色
        self.ax.title.set_color('white')

    def inner_cal_matrix(self):
        v1=self.v1
        v2=self.v2
        constant_t=self.t1
        motionless_t=self.t2
        a=self.a
        between=self.between
        msize=self.msize
        accelerate_t = round(v2 / a, 2)
        t1=accelerate_t
        t2=constant_t
        t3=accelerate_t
        t4=motionless_t
        t5=accelerate_t
        t6=constant_t
        t7=accelerate_t
        t8=motionless_t
        period=4*accelerate_t+2*motionless_t+2*constant_t
        # 正式计算
        n=self.n
        between_cell=math.floor(between/v1/msize)    # 间距步长
        time=np.arange(0,period,msize)               # 时间变量
        T_size=math.floor(period/msize)              # 单周期步长
        # 磨头中心坐标
        X_location=np.zeros((1,T_size))
        Y_location=np.zeros((1,T_size))
        for k in range(0,T_size):
            t=time[k]
            # 第一段
            if t >= 0 and t < t1:
                x_0 = v1 * t
                y_0 = 0.5 * a * t ** 2
            elif t >= t1 and t < t1 + t2:
                # 第二段
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * (t - t1)
            # 第三段
            elif t >= (t1 + t2) and t < (t1 + t2 + t3):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * (t - t1 - t2) - 0.5 * a * (t - t1 - t2) ** 2
            # 第四段
            elif t >= (t1 + t2 + t3) and t < (t1 + t2 + t3 + t4):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2
            # 第五段
            elif t >= (t1 + t2 + t3 + t4) and t < (t1 + t2 + t3 + t4 + t5):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * (
                            t - t1 - t2 - t3 - t4) ** 2
            # 第六段
            elif t >= (t1 + t2 + t3 + t4 + t5) and t < (t1 + t2 + t3 + t4 + t5 + t6):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * t5 ** 2 - v2 * (
                            t - t1 - t2 - t3 - t4 - t5)
            # 第七段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6) and t < (t1 + t2 + t3 + t4 + t5 + t6 + t7):
                x_0 = v1 * t
                y_0 = 0.5 * a * t1 ** 2 + v2 * t2 + v2 * t3 - 0.5 * a * t3 ** 2 - 0.5 * a * t5 ** 2 - v2 * t6 - v2 * (
                            t - t1 - t2 - t3 - t4 - t5 - t6) + 0.5 * a * (t - t1 - t2 - t3 - t4 - t5 - t6) ** 2
            # 第八段
            elif t >= (t1 + t2 + t3 + t4 + t5 + t6 + t7) and t <= (t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8):
                x_0 = v1 * t
                y_0 = 0
            X_location[0,k] = x_0
            Y_location[0,k] = y_0
        all_time_n=T_size*n
        single_X_location=np.zeros((1,all_time_n))
        single_Y_location=np.zeros((1,all_time_n))
        for i in range(0,n):
            single_X_location[0,i*T_size:(i+1)*T_size] = X_location+period*v1*i
            single_Y_location[0,i*T_size:(i+1)*T_size] = Y_location
        return single_X_location, single_Y_location

    def emit(self):
        period = math.floor(self.all_time_n / self.n * 3.5)

        if self.mode == 'equal':
            # 绘制x、y、num的标识(坐标信息相对不移动)
            self.grinding_num.set_text('Same_grinding_num=%.0f' % self.num)
            # self.xtext_ani.set_text('x_location=%.3f mm' % (self.single_X_location[0, j]))
            # 绘制抛光轨迹进行叠加
            for i in range(0, self.num):
                for j in range(0,period):
                    circle_1 = Circle(xy=((self.single_X_location[0, j] + i * self.beam_between),
                                          self.single_Y_location[0, j] - 0.5 * (
                                                      self.v2 ** 2 / self.a + self.v2 * self.t1)),
                                      radius=self.R, alpha=0.05,
                                      color=self.color_7[i])
                    self.ax.add_patch(circle_1)

        elif self.mode == 'cross':
            # 绘制x、y、num的标识(坐标信息相对不移动)
            self.grinding_num.set_text('Same_grinding_num=%.0f' % self.num)
            # self.xtext_ani.set_text('x_location=%.3f mm' % (self.single_X_location[0, j]))
            # 绘制抛光轨迹进行叠加
            for i in range(0, self.num):
                for j in range(0,period):
                    # 横梁数为奇数
                    if (i + 2) % 2 == 0:
                        circle_1 = Circle(xy=((self.single_X_location[0, j] + i * self.beam_between),
                                              self.single_Y_location[0, j] - 0.5 * (
                                                      self.v2 ** 2 / self.a + self.v2 * self.t1)),
                                          radius=self.R, alpha=0.05,
                                          color=self.color_7[i])
                    # 横梁数为偶数
                    else:
                        circle_1 = Circle(xy=((self.single_X_location[0, j] + i * self.beam_between),
                                              self.single_Y_location[0, j + self.cross_size] - 0.5 * (
                                                      self.v2 ** 2 / self.a + self.v2 * self.t1)), radius=self.R,
                                          alpha=0.05,
                                          color=self.color_7[i])
                    self.ax.add_patch(circle_1)

        elif self.mode == 'order':
            # 绘制x、y、num的标识(坐标信息相对不移动)
            self.grinding_num.set_text('Same_grinding_num=%.0f' % self.num)
            # self.xtext_ani.set_text('x_location=%.3f mm' % (self.single_X_location[0, j]))
            # 绘制抛光轨迹进行叠加
            for i in range(0, self.num):
                for j in range(0,period):
                    # 延时绘制效果
                    circle_1 = Circle(xy=((self.single_X_location[0, j] + i * (self.beam_between-self.delay_time*self.v1)),
                                          self.single_Y_location[0, j] - 0.5 * (
                                                  self.v2 ** 2 / self.a + self.v2 * self.t1)),
                                      radius=self.R, alpha=0.05,
                                      color=self.color_7[i])
                    self.ax.add_patch(circle_1)
        else:
            raise ValueError('mode must be equal or cross or order')
        return (self.animation_name)
'''
# -----------------智能计算------------------
def single_num_calculate(v1,ceramic_width,beam_between,R,a,mo,**kwargs):
    # mode = enerage or efficient
    mode = kwargs.get('mode', None)
    # 计算相叠overlap  mm 斜率（已知磨头间距为between）
    # 轨迹重叠量，可调整算法优化性能，范围：（0~200）
    overlap = 25
    # 横梁摆动速度最大值，可调整算法优化性能，范围：（300~800）
    beam_speed_up = 750
    v2 = beam_speed_up
    theta = math.atan(v2 / v1)
    between = round((2 * R - overlap) / math.sin(theta),2)
    # 中间计算(边部停留时长为单倍磨头间距)
    B = (ceramic_width + 200) - 2 * R  # 摆幅（要求两极限位置各伸出80mm）
    t_a = v2 / a  # 加速时间
    t_e = (B - a * t_a ** 2) / v2  # 匀速时间
    t_between = between / v1 * 1  # 边部停留时长
    period_1 = 4 * t_a + 2 * t_e + 2 * t_between  # 单周期时间
    num_1 = math.ceil(v1 * period_1 / between)  # 同粒度磨头数目
    t_beam = (num_1 * between - 2 * between) / (2 * v1)  # 2 * t_a + t_e
    #
    # f_1 = a * t_a ^ 2 - t_beam * a * t_a + B;
    #
    if (t_beam * a) ** 2 - 4 * a * B >= 0:
        t_a = (-((t_beam * a) ** 2 - 4 * a * B) ** 0.5 + a * t_beam) / (2 * a)
        # t1 = (((t_beam * a) ^ 2 - 4 * a * B) ^ 0.5 + a * t_beam) / (2 * a)
    else:
        t_a = t_beam / 2
        ValueError('The swing cannot reach the set value')
    v2 = round(t_a * a, 2)
    t_e = round(t_beam - 2 * t_a, 2)
    # 延时时间计算
    t_delay = round((beam_between - between) / v1, 2)
    t_delay_list_enerage = []
    t_delay_list_efficient = []
    for i in range(0,num_1):
        t_delay_list_enerage.append(round(i * t_delay,2))
    for i in range(0,num_1+2):
        t_delay_list_efficient.append(round(i * t_delay,2))
    # 结果输出
    params = {}
    if mode == 'enerage':
        params.update(
            {'lineEdit_belt_speed': round(v1, 2), 'lineEdit_beam_swing_speed': round(v2, 2), 'lineEdit_beam_constant_time': round(t_e, 2)
                , 'lineEdit_stay_time_output': round(t_between, 2), 'lineEdit_num_output': round(num_1),'lineEdit_delay_time': t_delay
                ,'lineEdit_delay_time_list': t_delay_list_enerage, 'lineEdit_swing': round(a * t_a ** 2 + v2 * t_e, 2), 'lineEdit_ceramic_width': ceramic_width
                , 'lineEdit_between': between, 'lineEdit_beam_between': beam_between, 'R': R, 'lineEdit_accelerate': a
                ,'lineEdit_grind_length': mo})
    elif mode == 'efficient':
        params.update(
            {'lineEdit_belt_speed': round(v1, 2), 'lineEdit_beam_swing_speed': round(v2, 2), 'lineEdit_beam_constant_time': round(t_e, 2)
            ,'lineEdit_stay_time_output': round(t_between * 2, 2), 'lineEdit_num_output': round(num_1 + 2),'lineEdit_delay_time': t_delay
            ,'lineEdit_delay_time_list': t_delay_list_efficient,'lineEdit_swing': round(a * t_a ** 2 + v2 * t_e, 2), 'lineEdit_ceramic_width': ceramic_width
            , 'lineEdit_between': between, 'lineEdit_beam_between': beam_between, 'R': R, 'lineEdit_accelerate': a,'lineEdit_grind_length': mo})
    else:
        ValueError('mode must be enerage or efficient')
    '''
    result = np.zeros((2, 8))
    # 方案一 节能方案
    result[0, 0] = round(v1, 2)
    result[0, 1] = round(v2, 2)
    result[0, 2] = round(t_e, 2)
    result[0, 3] = round(t_between, 2)
    result[0, 4] = round(num_1)
    result[0, 5] = t_delay
    result[0, 6] = round(a * t_a ** 2 + t_e * a * t_a, 2)
    result[0, 7] = round(between, 2)
    # 方案二 高光泽度方案
    result[1, 0] = round(v1, 2)
    result[1, 1] = round(v2, 2)
    result[1, 2] = round(t_e, 2)
    result[1, 3] = round(t_between * 2, 2)
    result[1, 4] = round(num_1 + 2)
    result[1, 5] = t_delay
    result[1, 6] = round(a * t_a ** 2 + t_e * a * t_a, 2)
    result[1, 7] = round(between, 2)
    '''
    return params
# -----------------自定义计算-----------------
def single_self_define_calculate(v1,ceramic_width,beam_between,R,a,num_input,group,stay_time,mo,**kwargs):
    # 考虑到机型限制，num_input最小为3 ，gruop最小为1，最大为4
    mode = kwargs.get('mode', None)
    num_input = round(num_input)
    group = round(group)
    # 计算单周期时间
    beam_speed_up = 850
    B=ceramic_width+200-2*R
    t_a=round(beam_speed_up/a,2)
    if a*t_a**2>=B:
        t_a=round((B/a)**0.5,2)
        t_e=0
    else:
        t_e=round(((B-a*t_a**2)/beam_speed_up),2)
    t_period=4*t_a+2*t_e+2*stay_time
    # 计算磨头间距
    between=round(v1*t_period/num_input,2)
    # 计算延时时间
    delay_time=round((beam_between-between)/v1,2)
    self_delay_time=round(between/group/v1,2)
    # 延时时间计算
    delay_time_self_list = []
    # 多组磨头叠加延时时间计算
    for i in range(0,num_input*group):
        current_delay_time = round(i*delay_time, 2)
        if (i / num_input) >=1:
            current_delay_time += math.floor(i / num_input)*self_delay_time
        delay_time_self_list.append(round(current_delay_time, 2))

    params = {}
    params.update(
            {'lineEdit_belt_speed': v1, 'lineEdit_beam_swing_speed': round(t_a*a,2), 'lineEdit_beam_constant_time': t_e
                , 'lineEdit_stay_time_output': stay_time, 'lineEdit_num_output': num_input*group, 'lineEdit_num_input':num_input
                ,'lineEdit_group_count':group,'lineEdit_delay_time': delay_time,'lineEdit_delay_time_list': delay_time_self_list
                , 'lineEdit_swing': round(a*t_a**2+t_a*a*t_e,2)
                , 'lineEdit_ceramic_width': ceramic_width, 'lineEdit_between': between, 'lineEdit_beam_between': beam_between, 'R': R
                , 'lineEdit_accelerate': a,'lineEdit_grind_length': mo
                #,'self_delay_time': self_delay_time
                ,'lineEdit_stay_time_input': stay_time}
    )
    return params
# -----------------动画分割-------------------
def split_gif(input_gif, split_frame, output_gif_1, output_gif_2):
    # 打开输入的 GIF 文件
    with Image.open(input_gif) as img:
        # 提取所有帧
        frames = [frame.copy() for frame in ImageSequence.Iterator(img)]

    # 将帧按照指定的 split_frame 进行分割
    frames_1 = frames[:split_frame]  # 前半部分帧
    frames_2 = frames[split_frame:]  # 后半部分帧

    # 保存前半部分为一个新的 GIF
    frames_1[0].save(
        output_gif_1,
        save_all=True,
        append_images=frames_1[1:],  # 保存所有帧
        loop=1,  # 无限循环
        duration=img.info['duration']  # 使用原始的帧持续时间
    )
    # 保存后半部分为另一个新的 GIF
    frames_2[0].save(
        output_gif_2,
        save_all=True,
        append_images=frames_2[1:],  # 保存所有帧
        loop=0,  # 无限循环
        duration=img.info['duration']  # 使用原始的帧持续时间
    )

def double_plot(**kwargs):
    # 选择绘图模式
    mode = kwargs.get('mode', None)
    # 输入参数
    v1 = kwargs.get('v1', 0)
    v2 = kwargs.get('v2', 0)
    constant_time = kwargs.get('constant_time', 0)
    stay_time = kwargs.get('stay_time', 0)
    a = kwargs.get('a', 650)
    between = kwargs.get('between', 0)
    beam_between = kwargs.get('beam_between', 0)
    num = kwargs.get('num', 0)
    R = kwargs.get('R', 270)
    mo = kwargs.get('mo', 150)
    # 顺序摆参数
    delay_time = kwargs.get('delay_time', 0)
    # 自定义计算参数
    group = kwargs.get('group', 1)

    # 抛磨量 + 轨迹中心线 画布
    fig_1 = kwargs.get('fig_1', None)
    # 轨迹动画 画布
    fig_2 = kwargs.get('fig_2', None)
    animation_name = kwargs.get('Animation_name', 0)

    # 抛磨量分布矩阵
    PDT = PolishingDistributionThread(mode = mode, v1 = v1, v2 = v2, constant_time = constant_time, stay_time = stay_time
                                                ,a = a, between= between, beam_between=beam_between, mo = mo, delay_time = delay_time
                                                ,num = num, R = R, group = group)
    object_matrix,result = PDT.emit()
    # 轨迹中心线坐标信息
    MLP = MiddleLinePlot(v1 = v1, v2 = v2, constant_time = constant_time, stay_time = stay_time
                                                ,a = a, between= between, beam_between=beam_between, delay_time = delay_time
                                                ,num = num, group = group)
    single_X_location, single_Y_location = MLP.inner_calculate()
    # 轨迹动画生成
    if mode == 'self_order':
        mode_an = 'order'
    else:
        mode_an = mode
    AP = AnimationProduce(mode=mode_an, fig=fig_2, v1 = v1, v2 = v2, constant_time = constant_time, stay_time = stay_time
                                ,a = a, between= between, beam_between=beam_between,num = num
                                 , R = R, group = group, animation_name= animation_name)
    animation = AP.emit()
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置微软雅黑字体
    plt.rcParams['axes.unicode_minus'] = False  # 避免坐标轴不能正常的显示负号
    # 设置
    ax_1 = fig_1.add_subplot(211)
    ax_2 = fig_1.add_subplot(212)
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
    # ----------------------抛磨量分布绘图------------------
    ax_1.set_aspect('equal', adjustable='box')
    # 设置权重操作
    max_set = np.max(object_matrix)
    # 计算第90百分位的阈值（前15%）
    percentile_85 = np.percentile(object_matrix, 85)
    # 对矩阵中大于等于该阈值的元素乘以0.85
    object_matrix[object_matrix >= percentile_85] *= 0.85

    im = ax_1.contourf(object_matrix, levels=15, alpha=1, cmap='jet', vmin=0, vmax=max_set)

    divider = make_axes_locatable(ax_1)
    cax = divider.append_axes("right", size="5%", pad=0.1)

    colorbar = self.canvas.fig.colorbar(im, cax=cax)

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
    # ----------------------中心线绘图------------------
    accelerate_t = v2 / a
    period = 4 * accelerate_t + 2 * stay_time + 2 * constant_time
    # 设置图层属性
    ax_2.set_xlim((-200, period * 3 * v1 + between))
    ax_2.set_ylim((-200, a * (v2 / a) ** 2 + v2 * constant_time + 600))
    ax_2.set_aspect('equal', adjustable='box')
    # 设置图片文本
    ani_text = ax_2.text(0.7, 0.82, '', transform=ax_2.transAxes, fontsize=10, color='white')
    ani_text.set_text('Same_grinding_num=%.0f' % (num*group))
    num_two = math.ceil(num / 2)
    color_7 = ['red', 'orange', 'green', 'cyan', 'blue', 'purple', 'yellow', 'lightgreen',
               'slategrey', 'cornflowerblue', 'navy', 'indigo', 'violet', 'plum', 'oldlace', 'maroon',
               'lightcyan', 'lightseagreen', 'seagreen', 'springgreen']  # 红橙黄绿青蓝紫
    if mode == 'equal':
        for i in range(0, num_two):
            ax_2.scatter(single_X_location + i * beam_between, single_Y_location, color=color_7[i], s=1)
            ax_2.scatter(single_X_location + i * beam_between + between, single_Y_location, color=color_7[i], s=1)
    elif mode == 'cross':
        for i in range(0, num_two):
            ax_2.scatter(single_X_location + i * beam_between, single_Y_location, color=color_7[i], s=1)
            ax_2.scatter(single_X_location + i * beam_between + between, single_Y_location, color=color_7[i], s=1)
    elif mode == 'order':
        for i in range(0, num_two):
            ax_2.scatter(single_X_location[0, 0:all_time_n - 1] + i * beam_between - i * delay_time * v1,
                         single_Y_location[0, 0:all_time_n - 1],
                         color=color_7[i], s=1)
            ax_2.scatter(single_X_location[0,
                         0:all_time_n - 1] + i * beam_between + between - i * delay_time * v1,
                         single_Y_location[0, 0:all_time_n - 1],
                         color=color_7[i], s=1)
    elif mode == 'self_oeder':
        self_delay_distance = between / group
        idex = 0
        for i in range(0, group):
            for j in range(0, num_two):
                ax_2.scatter(single_X_location[0,
                             0:all_time_n - 1] + j * beam_between - j * delay_time * v1 + self_delay_distance * i,
                             single_Y_location[0, 0:all_time_n - 1],
                             color=color_7[idex], s=1)
                ax_2.scatter(single_X_location[0,
                             0:all_time_n - 1] + j * beam_between + between - j * delay_time * v1 + self_delay_distance * i,
                             single_Y_location[0, 0:all_time_n - 1],
                             color=color_7[idex], s=1)
                idex = idex + 1
    else:
        raise ValueError('mode must be equal or cross or order')