# 用于方案对比
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

import sys
import time
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QProgressBar)
from PySide6.QtCore import QThread, Signal

class ComparisonWorkerThread(QThread):
    result_signal = Signal(object)  # 创建一个信号用于传递结果
    def __init__(self,fig,*args):
        super().__init__()
        self.args = args
        self.dict_list = list(self.args)
        self.count_figure = len(self.dict_list)
        self.fig = fig

    def run(self):
        self.dict_list = list(self.args)
        self.count_figure = len(self.dict_list)
        # 储存抛磨量数值矩阵
        polishing_object_matrix_list = []
        # 储存抛磨变异系数
        polishing_result_list = []
        # 储存轨迹中心坐标
        middle_line_parameter_list = []
        # 遍历输入的所有字典
        for i in self.dict_list:
            # 当前字典
            current_dict = i['full_motion_param']
            # 抛磨量分布矩阵
            PDT = PolishingDistributionThread(**current_dict)
            object_matrix, result = PDT.emit()
            # 抛磨量分布仿真结果收集
            polishing_object_matrix_list.append(object_matrix)
            polishing_result_list.append(result)

            # 轨迹中心线坐标信息
            MLP = MiddleLinePlot(**current_dict)
            single_X_location, single_Y_location = MLP.inner_calculate()
            polishing_result = [[single_X_location], [single_Y_location]]
            middle_line_parameter_list.append(polishing_result)

        # 绘图
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置微软雅黑字体
        plt.rcParams['axes.unicode_minus'] = False  # 避免坐标轴不能正常地显示负号
        # 创建绘图图层
        ax_list = []
        for i in range(1,self.count_figure*2+1):
            ax = self.fig.add_subplot(self.count_figure,2,i)
            # 设置 子图 标签
            ax.set_xlabel('主皮带进给方向')
            ax.set_ylabel('横梁摆动方向')
            ax.set_title("Subplot Title")
            ax_list.append(ax)
        # 绘制轨迹中心线--(位置：1 3 5 7 )    绘制仿真图--(位置：2 4 6 8 )
        j = 1
        for i in range(1, self.count_figure * 2, 2):
            parameter = self.dict_list[j-1]   # 储存参数集的字典
            # 轨迹中心线绘图
            middle_plot(middle_line_parameter_list[j-1][0], middle_line_parameter_list[j-1][1],ax_list[i-1], **parameter)
            # 抛磨量分布绘图
            polishing_plot(polishing_object_matrix_list[j-1],ax_list[i],self.fig,**parameter)
            j += 1
        self.fig.subplots_adjust(hspace=0.5)

        self.result_signal.emit(polishing_result_list)  # 发射信号将结果传回主线程

# -------------------抛磨量计算--------------------
class PolishingDistributionThread():
    def __init__(self,**kwargs):
        # 机型选择： 单头摆-single 双头摆-double 同步摆-equal
        self.current_device = kwargs.get('device', None)
        # 摆动模式：  同-equal 交叉摆-ceoss 顺序摆-order 自定义方案-self_order
        self.mode = kwargs.get('mode', None)
        # 基本运动参数
        self.v1 = kwargs.get('lineEdit_belt_speed', 0)
        self.v2 = kwargs.get('lineEdit_beam_swing_speed', 0)
        self.constant_time = kwargs.get('lineEdit_beam_constant_time', 0)
        self.a = kwargs.get('lineEdit_accelerate', 650)
        self.between = kwargs.get('lineEdit_between', 0)
        self.beam_between = kwargs.get('lineEdit_beam_between', 0)
        self.R = kwargs.get('R', 270)
        self.mo = kwargs.get('lineEdit_grind_length', 150)
        self.ceramic_width = kwargs.get('lineEdit_ceramic_width', 800)
        if self.mode == 'self_order':
            self.stay_time = kwargs.get('lineEdit_stay_time_input', 0)
            self.num = round(kwargs.get('lineEdit_num_input', 0))
        else:
            self.stay_time = kwargs.get('lineEdit_stay_time_output', 0)
            self.num = round(kwargs.get('lineEdit_num_output', 0))
        # 顺序摆参数
        self.delay_time = kwargs.get('lineEdit_delay_time', 0)
        # 自定义计算参数
        self.group = kwargs.get('lineEdit_group_count', 1)

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
        matrix_results = self.start_multiprocessing()

        fun_str = self.current_device+'_'+self.mode+'_matrix_cal'
        fun_matrix_cal = getattr(self,fun_str,None)

        object_matrix, result = fun_matrix_cal(matrix_results)

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

    # 单头摆-同步摆模式计算
    def single_equal_matrix_cal(self, H_all):
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

    # 单头摆-交叉摆模式计算
    def single_cross_matrix_cal(self, H_all):
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

    # 单头摆-顺序摆模式计算
    def single_order_matrix_cal(self, H_all):
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

    # 单头摆-自定义模式计算
    def single_self_order_matrix_cal(self, H_all):
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

    # 双头摆-同步摆模式计算
    def double_equal_matrix_cal(self, H_all):
        sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
        mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
        H_period = H_all[:, 5:5 + sin_period]
        H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, self.n):
            H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
                                                                   i * mid_period:i * mid_period + sin_period] + H_period
        # 多磨头叠加
        mul_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        between_cell = math.floor(self.between / self.c_length_cell)
        for i in range(0, 2):
            mul_H[:, between_cell * i:self.c_length_mulcell - 1] = (
                    mul_H[:, between_cell * i:self.c_length_mulcell - 1] +
                    H_mid[:, 0:self.c_length_mulcell - between_cell * i - 1])
        num_two = math.floor(self.num / 2)
        all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
        for i in range(0, num_two):
            all_H[:, beam_between_cell * i:self.c_length_mulcell - 1] = (
                    all_H[:, beam_between_cell * i:self.c_length_mulcell - 1] +
                    mul_H[:, 0:self.c_length_mulcell - beam_between_cell * i - 1])
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

    # 双头摆-交叉摆模式计算
    def double_cross_matrix_cal(self, H_all):
        sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
        mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
        H_period = H_all[:, 5:5 + sin_period]
        H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, self.n):
            H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
                                                                   i * mid_period:i * mid_period + sin_period] + H_period
        # 多磨头叠加
        mul_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        between_cell = math.floor(self.between / self.c_length_cell)
        for i in range(0, 2):
            mul_H[:, between_cell * i:self.c_length_mulcell - 1] = (
                    mul_H[:, between_cell * i:self.c_length_mulcell - 1] +
                    H_mid[:, 0:self.c_length_mulcell - between_cell * i - 1])
        num_two = math.floor(self.num / 2)
        all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
        cross_size = round((self.t1 + self.t2 + self.t3 + self.t4) * self.v1 / self.c_length_cell)
        # 末尾减去50 防止切片溢出
        for i in range(0, num_two):
            if (i + 2) % 2 == 0:  # 第 奇数 个横梁
                all_H[:, beam_between_cell * i:self.c_length_mulcell - 1 - 50] = (
                        all_H[:, beam_between_cell * i:self.c_length_mulcell - 1 - 50] +
                        mul_H[:, 0:self.c_length_mulcell - beam_between_cell * i - 1 - 50])
            else:
                all_H[:, beam_between_cell * i:self.c_length_mulcell - 1 - 50] = (
                        all_H[:, beam_between_cell * i: self.c_length_mulcell - 1 - 50] +
                        mul_H[:, cross_size: self.c_length_mulcell - 1 - beam_between_cell * i + cross_size - 50])
        # 计算 抛磨变异系数
        # 如果要计算此模块，周期数必须大于等于3
        cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
        begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
        terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width
        begin_length = math.ceil((50 + self.v1 * (self.n - 5) * self.period) / 10)
        terminate_length = begin_length + math.ceil((2 * self.v1 * self.period + 2 * self.R) / 10)
        object_matrix = all_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]
        equal_subsample = np.mean(object_matrix)  # 子样平均数
        middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
        variance_matrix = np.mean(middle_matrix)  # 子样方差
        result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
        return object_matrix, result

    # 双头摆-顺序摆模式计算
    def double_order_matrix_cal(self, H_all):
        sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
        mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
        H_period = H_all[:, 5:5 + sin_period]
        H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, self.n):
            H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
                                                                   i * mid_period:i * mid_period + sin_period] + H_period
        # 多磨头叠加
        mul_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        between_cell = math.floor(self.between / self.c_length_cell)
        delay_cell = math.floor(self.delay_time * self.v1 / self.c_length_cell)
        for i in range(0, 2):
            mul_H[:, between_cell * i:self.c_length_mulcell - 1] = (
                    mul_H[:, between_cell * i:self.c_length_mulcell - 1] +
                    H_mid[:, 0:self.c_length_mulcell - between_cell * i - 1])
        num_two = math.floor(self.num / 2)
        all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
        for i in range(0, num_two):
            all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] = (
                    all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] +
                    mul_H[:, 0:self.c_length_mulcell - (beam_between_cell - delay_cell) * i - 1])
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

    # 双头摆-自定义模式计算
    def double_self_order_matrix_cal(self, H_all):
        sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
        mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
        H_period = H_all[:, 5:5 + sin_period]
        H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, self.n):
            H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
                                                                   i * mid_period:i * mid_period + sin_period] + H_period
        # 多磨头叠加
        mul_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        between_cell = math.floor(self.between / self.c_length_cell)
        delay_cell = math.floor(self.delay_time * self.v1 / self.c_length_cell)
        for i in range(0, 2):
            mul_H[:, between_cell * i:self.c_length_mulcell - 1] = (
                    mul_H[:, between_cell * i:self.c_length_mulcell - 1] +
                    H_mid[:, 0:self.c_length_mulcell - between_cell * i - 1])
        num_two = math.floor(self.num / 2)
        all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
        for i in range(0, num_two):
            all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] = (
                    all_H[:, (beam_between_cell - delay_cell) * i:self.c_length_mulcell - 1] +
                    mul_H[:, 0:self.c_length_mulcell - (beam_between_cell - delay_cell) * i - 1])
        # 组数叠加
        group = round(self.group)
        group_size = math.floor(self.between / self.group / self.c_length_cell)
        all_group_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, group):
            all_group_H[:, group_size * i:self.c_length_mulcell - 1] = (
                    all_group_H[:, group_size * i:self.c_length_mulcell - 1] +
                    all_H[:, 0:self.c_length_mulcell - group_size * i - 1])
        # 计算 抛磨变异系数
        # 如果要计算此模块，周期数必须大于等于3
        # cover_length = math.ceil(math.ceil(v1 * period + 2 * R) / 10)
        cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
        begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
        terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width
        begin_length = math.ceil((50 + self.v1 * 3 * self.period) / 10)
        terminate_length = begin_length + math.ceil((2 * self.v1 * self.period + 2 * self.R) / 10)
        # object_matrix = np.zeros((terminate_width - begin_width, terminate_length - begin_length))
        object_matrix = all_group_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]
        equal_subsample = np.mean(object_matrix)  # 子样平均数
        middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
        variance_matrix = np.mean(middle_matrix)  # 子样方差
        result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
        return object_matrix, result

    # 同步摆-同步摆模式计算
    def equal_equal_matrix_cal(self, H_all):
        sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
        mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
        H_period = H_all[:, 5:5 + sin_period]
        H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, self.n):
            H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
                                                                   i * mid_period:i * mid_period + sin_period] + H_period
        # 多磨头叠加
        all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        between_cell = math.floor(self.between / self.c_length_cell)
        for i in range(0, self.num):
            all_H[:, between_cell * i:self.c_length_mulcell - 1] = (
                    all_H[:, between_cell * i:self.c_length_mulcell - 1] +
                    H_mid[:, 0:self.c_length_mulcell - between_cell * i - 1])
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

    def start_multiprocessing(self):
        value_list=[(0, self.t1,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
                    (self.t1, self.t1 + self.t2,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
                    (self.t1 + self.t2, self.t1 + self.t2 + self.t3,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
                    (self.t1 + self.t2 + self.t3, self.t1 + self.t2 + self.t3 + self.t4,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
                    (self.t1 + self.t2 + self.t3 + self.t4, self.t1 + self.t2 + self.t3 + self.t4 + self.t5,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
                    (self.t1 + self.t2 + self.t3 + self.t4 + self.t5,self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
                    (self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6,self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6 + self.t7,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,),
                    (self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6 + self.t7,self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6 + self.t7 + self.t8,self.v1,self.v2,self.constant_time,self.stay_time,self.a,self.R,self.mod_rho,self.mod_theta,self.mo,)]
        # 创建进程池(4线程)
        with multiprocessing.Pool(processes=4) as pool:
            # 使用 apply_async 运行不同的函数
            results = []
            results.append(pool.apply_async(polishing_cal, args=(value_list[0])))
            results.append(pool.apply_async(polishing_cal, args=(value_list[1])))
            results.append(pool.apply_async(polishing_cal, args=(value_list[2])))
            results.append(pool.apply_async(polishing_cal, args=(value_list[3])))
            results.append(pool.apply_async(polishing_cal, args=(value_list[4])))
            results.append(pool.apply_async(polishing_cal, args=(value_list[5])))
            results.append(pool.apply_async(polishing_cal, args=(value_list[6])))
            results.append(pool.apply_async(polishing_cal, args=(value_list[7])))
            # 关闭进程池，等待所有任务完成
            pool.close()
            pool.join()
        # 提取结果并进行相加
        matrix_results = sum(result.get() for result in results)
        return matrix_results
def polishing_cal(begin,end,v1,v2,constant_t,stay_t,a,R,mod_rho,mod_theta,mo):
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
    begin_time = math.floor(begin / size)  # 单周期步长
    end_time = math.floor(end / size)  # 单周期步长
    # 计算单个周期磨头抛磨量分布
    for k in range(begin_time, end_time):
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
# -----------------轨迹中心线计算----------------------
class MiddleLinePlot():
    def __init__(self,**kwargs):
        # 基本运动参数
        self.v1 = kwargs.get('lineEdit_belt_speed', 0)
        self.v2 = kwargs.get('lineEdit_beam_swing_speed', 0)
        self.constant_time = kwargs.get('lineEdit_beam_constant_time', 0)
        self.a = kwargs.get('lineEdit_accelerate', 650)
        self.between = kwargs.get('lineEdit_between', 0)
        self.beam_between = kwargs.get('lineEdit_beam_between', 0)
        self.mode = kwargs.get('mode', 0)
        if self.mode == 'self_order':
            self.stay_time = kwargs.get('lineEdit_stay_time_input', 0)
            self.num = round(kwargs.get('lineEdit_num_input', 0))
        else:
            self.stay_time = kwargs.get('lineEdit_stay_time_output', 0)
            self.num = round(kwargs.get('lineEdit_num_output', 0))

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
# -----------------轨迹中心线绘图----------------------
def middle_plot(single_X_location,single_Y_location,ax,**kwargs):
    single_X_location = single_X_location[0]
    single_Y_location = single_Y_location[0]
    # 赋值
    current_device = kwargs.get('device', None)
    # 摆动模式：  同-equal 交叉摆-ceoss 顺序摆-order 自定义方案-self_order
    mode = kwargs.get('mode', 0)
    v1 = kwargs.get('lineEdit_belt_speed', 0)
    v2 = kwargs.get('lineEdit_beam_swing_speed', 0)
    constant_time = kwargs.get('lineEdit_beam_constant_time', 0)
    a = kwargs.get('lineEdit_accelerate', 650)
    between = kwargs.get('lineEdit_between', 0)
    beam_between = kwargs.get('lineEdit_beam_between', 0)
    group = round(kwargs.get('lineEdit_group_count', 1))
    delay_time = kwargs.get('lineEdit_delay_time', 0)
    if mode == 'self_order':
        stay_time = kwargs.get('lineEdit_stay_time_input', 0)
        num = round(kwargs.get('lineEdit_num_input', 0))
    else:
        stay_time = kwargs.get('lineEdit_stay_time_output', 0)
        num = round(kwargs.get('lineEdit_num_output', 0))

    # ----------------------中心线绘图------------------
    accelerate_t = v2 / a
    period = 4 * accelerate_t + 2 * stay_time + 2 * constant_time
    # 设置图层属性
    ax.set_xlim((-200, period * 3 * v1 + between))
    ax.set_ylim((-200, a * (v2 / a) ** 2 + v2 * constant_time + 600))
    ax.set_aspect('equal', adjustable='box')
    # 设置图片文本
    ani_text = ax.text(0.7, 0.82, '', transform=ax.transAxes, fontsize=10)
    ani_text.set_text('Same_grinding_num=%.0f' % float(num))
    num_two = math.ceil(num / 2)
    color_7 = ['red', 'orange', 'green', 'cyan', 'blue', 'purple', 'yellow', 'lightgreen',
               'slategrey', 'cornflowerblue', 'navy', 'indigo', 'violet', 'plum', 'oldlace', 'maroon',
               'lightcyan', 'lightseagreen', 'seagreen', 'springgreen']  # 红橙黄绿青蓝紫
    all_time_n = math.floor(period / 0.01) * 3
    cross_size = round((v2 / a + constant_time + stay_time + v2 / a) / 0.01)

    if current_device == 'equal':
        if mode == 'equal' or mode == 'self_order':
            for i in range(0, num):
                ax.scatter(single_X_location + i * between, single_Y_location,
                             color=color_7[i], s=1)
    elif current_device == 'double':
        if mode == 'equal':
            for i in range(0, num_two):
                ax.scatter(single_X_location + i * beam_between, single_Y_location, color=color_7[i], s=1)
                ax.scatter(single_X_location + i * beam_between + between, single_Y_location,
                             color=color_7[i], s=1)
        elif mode == 'cross':
            for i in range(0, num_two):
                if (i + 2) % 2 == 0:
                    ax.scatter(single_X_location[0, 0:all_time_n - 1] + i * beam_between,
                                 single_Y_location[0, 0:all_time_n - 1],
                                 color=color_7[i], s=1)
                    ax.scatter(single_X_location[0, 0:all_time_n - 1] + i * beam_between + between,
                                 single_Y_location[0, 0:all_time_n - 1],
                                 color=color_7[i], s=1)
                # 横梁数为偶数
                else:
                    ax.scatter(single_X_location[0, 0:all_time_n - cross_size] + i * beam_between,
                                 single_Y_location[0, cross_size - 1:all_time_n - 1],
                                 color=color_7[i], s=1)
                    ax.scatter(
                        single_X_location[0, 0:all_time_n - cross_size] + i * beam_between + between,
                        single_Y_location[0, cross_size - 1:all_time_n - 1],
                        color=color_7[i], s=1)
        elif mode == 'order':
            for i in range(0, num_two):
                ax.scatter(
                    single_X_location[0, 0:all_time_n - 1] + i * beam_between - i * delay_time * v1,
                    single_Y_location[0, 0:all_time_n - 1],
                    color=color_7[i], s=1)
                ax.scatter(single_X_location[0,
                             0:all_time_n - 1] + i * beam_between + between - i * delay_time * v1,
                             single_Y_location[0, 0:all_time_n - 1],
                             color=color_7[i], s=1)
        elif mode == 'self_order':
            self_delay_distance = between / group
            idex = 0
            for i in range(0, group):
                for j in range(0, num_two):
                    ax.scatter(single_X_location[0,
                                 0:all_time_n - 1] + j * beam_between - j * delay_time * v1 + self_delay_distance * i,
                                 single_Y_location[0, 0:all_time_n - 1],
                                 color=color_7[idex], s=1)
                    ax.scatter(single_X_location[0,
                                 0:all_time_n - 1] + j * beam_between + between - j * delay_time * v1 + self_delay_distance * i,
                                 single_Y_location[0, 0:all_time_n - 1],
                                 color=color_7[idex], s=1)
                    idex = idex + 1
        else:
            raise ValueError('mode must be equal or cross or order or self_order')
    elif current_device == 'single':
        if mode == 'equal':
            for i in range(0, num):
                ax.scatter(single_X_location + i * beam_between, single_Y_location,
                             color=color_7[i], s=1)
        elif mode == 'cross':
            for i in range(0, num):
                if (i + 2) % 2 == 0:
                    ax.scatter(single_X_location[0, 0:all_time_n - 1] + i * beam_between,
                                 single_Y_location[0, 0:all_time_n - 1],
                                 color=color_7[i], s=1)
                # 横梁数为偶数
                else:
                    ax.scatter(single_X_location[0, 0:all_time_n - cross_size] + i * beam_between,
                                 single_Y_location[0, cross_size - 1:all_time_n - 1],
                                 color=color_7[i], s=1)
        elif mode == 'order':
            for i in range(0, num):
                ax.scatter(
                    single_X_location[0, 0:all_time_n - 1] + i * beam_between - i * delay_time * v1,
                    single_Y_location[0, 0:all_time_n - 1],
                    color=color_7[i], s=1)
        elif mode == 'self_order':
            self_delay_distance = between / group
            index = 0
            for i in range(0, group):
                for j in range(0, num):
                    ax.scatter(single_X_location[0,
                                 0:all_time_n - 1] + j * beam_between - j * delay_time * v1 + self_delay_distance * i,
                                 single_Y_location[0, 0:all_time_n - 1],
                                 color=color_7[index], s=1)
                    index += 1
        else:
            raise ValueError('mode must be equal or cross or order or self_order')
# -----------------抛磨量仿真绘图----------------------
def polishing_plot(object_matrix,ax,fig,**kwargs):
    ceramic_width = kwargs.get('lineEdit_ceramic_width',0)

    ax.set_aspect('equal', adjustable='box')
    # 设置权重操作
    max_set = np.max(object_matrix)
    # 计算第90百分位的阈值（前15%）
    percentile_85 = np.percentile(object_matrix, 85)
    # 对矩阵中大于等于该阈值的元素乘以0.85
    object_matrix[object_matrix >= percentile_85] *= 0.85

    im = ax.contourf(object_matrix, levels=15, alpha=1, cmap='jet', vmin=0, vmax=max_set)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)

    # colorbar = self.canvas.fig.colorbar(im, cax=cax)
    colorbar = fig.colorbar(im, cax=cax)

    # colorbar.ax.tick_params(labelcolor='white')  # 设置刻度标签颜色
    colorbar.set_label('抛磨量大小')  # 设置 colorbar 标签的颜色
    # 绘制矩形线框
    ceramic_width_ = float(ceramic_width) * 0.1
    width, length = np.shape(object_matrix)
    x_begin = 0
    y_begin = (width - ceramic_width_) / 2
    rect = Rectangle((x_begin, y_begin), length - 1, ceramic_width_, edgecolor='red', linestyle='--', linewidth=2,
                     fill=False)
    ax.add_patch(rect)

# 将字典中所有的值转换为数值类型
def dict_value_to_float(my_dict):
    dict_keys = my_dict.keys()
    for key in dict_keys:
        if my_dict[key] != '' and my_dict[key] is not None and not isinstance(my_dict[key], list):
            my_dict[key] = float(my_dict[key])
    return my_dict

def double_efficient_project(data):
    print(data)




# 功能测试
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 QThread Example")

        # 主界面布局
        self.layout = QVBoxLayout()
        self.progress_bar = QProgressBar()  # 进度条
        self.start_button = QPushButton("Start Task")  # 启动按钮

        # 添加组件到布局
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.start_button)

        # 中央小部件
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # 按钮点击事件
        self.start_button.clicked.connect(self.start_thread)

        # 输入量（字典类型）
        a = {'lineEdit_beam_between': '650.0', 'lineEdit_diameter': '540.0', 'lineEdit_grind_length': '160.0',
             'lineEdit_work_time': '22.0', 'lineEdit_production_volume': '30000.0', 'lineEdit_ceramic_width': '900.0',
             'lineEdit_accelerate': '650.0', 'lineEdit_overlap': '10.0', 'lineEdit_num_input': '4.0',
             'lineEdit_group_count': '1.0', 'lineEdit_stay_time_input': '0.8', 'lineEdit_belt_speed': '420.88',
             'lineEdit_beam_swing_speed': '289.2', 'lineEdit_beam_constant_time': '1.21',
             'lineEdit_stay_time_output': '1.4',
             'lineEdit_swing': '478.6', 'lineEdit_num_output': '5', 'lineEdit_coefficient': '0.3864',
             'lineEdit_delay_time': '0.14', 'lineEdit_delay_time_list': [0.0, 0.14, 0.28, 0.42, 0.56],
             'lineEdit_between': '590.5492918897945', 'R': '270.0'}
        b = {'lineEdit_beam_between': '600.0', 'lineEdit_diameter': '540.0', 'lineEdit_grind_length': '160.0',
             'lineEdit_work_time': '22.0', 'lineEdit_production_volume': '25000.0', 'lineEdit_ceramic_width': '900.0',
             'lineEdit_accelerate': '650.0', 'lineEdit_overlap': '10.0', 'lineEdit_num_input': '4',
             'lineEdit_group_count': '1', 'lineEdit_stay_time_input': '0.8', 'lineEdit_belt_speed': '350.73',
             'lineEdit_beam_swing_speed': '559.0', 'lineEdit_beam_constant_time': '0',
             'lineEdit_stay_time_output': '0.8',
             'lineEdit_swing': '480.74', 'lineEdit_num_output': '4', 'lineEdit_coefficient': '0.3874',
             'lineEdit_delay_time': '0.45',
             'lineEdit_delay_time_list': [1.26, 0.45, 0.9, 1.35], 'lineEdit_between': '441.92', 'R': '270.0',
             'self_delay_time': '1.26'}
        c = {'lineEdit_between': '600.0', 'lineEdit_beam_between': '1906.0', 'lineEdit_diameter': '540.0',
         'lineEdit_grind_length': '150.0', 'lineEdit_work_time': '22.0', 'lineEdit_production_volume': '25000.0',
         'lineEdit_ceramic_width': '900.0', 'lineEdit_accelerate': '650.0', 'lineEdit_overlap': '10.0',
         'lineEdit_num_input': '4.0', 'lineEdit_group_count': '1.0', 'lineEdit_stay_time_input': '0.8',
         'lineEdit_belt_speed': '350.73', 'lineEdit_beam_swing_speed': '250.62', 'lineEdit_beam_constant_time': '1.85',
         'lineEdit_stay_time_output': '0.8', 'lineEdit_swing': '560.28', 'lineEdit_num_output': '4.0',
         'lineEdit_coefficient': '', 'lineEdit_delay_time': '2.01', 'lineEdit_delay_time_list': [0.0, 2.01],
         'R': '270.0', 'self_delay_time': '1.71'}
        a = dict_value_to_float(a)
        b = dict_value_to_float(b)
        c = dict_value_to_float(c)
        a['device'] = 'single'
        a['mode'] = 'order'
        b['device'] = 'single'
        b['mode'] = 'self_order'
        c['device'] = 'double'
        c['mode'] = 'self_order'
        fig = plt.figure(figsize=(16, 8), dpi=100)
        fig.suptitle("方案对比")

        # 获取当前图形窗口（针对Qt后端）
        canvas = plt.gcf().canvas
        # 获取Qt窗口并设置标题
        if hasattr(canvas.manager, 'window'):
            canvas.manager.window.setWindowTitle("My Matplotlib Figure Window")

        self.worker_thread = ComparisonWorkerThread(fig,a,b,c)
        self.worker_thread.result_signal.connect(self.update_progress)

    def start_thread(self):
        # self.start_button.setEnabled(False)  # 禁用按钮，防止重复点击
        self.worker_thread.start()

    def update_progress(self, value):
        print(value)
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

