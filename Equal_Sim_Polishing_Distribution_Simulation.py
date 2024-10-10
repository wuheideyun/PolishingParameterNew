import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PySide6.QtCore import QThread, Signal
import time as te
import multiprocessing
# 多进程计算函数
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
# 抛磨量分布，子工作线程
class Polishing_distribution_Thread(QThread):
    result_ready= Signal(np.ndarray,str)
    def __init__(self, v1, v2, constant_time, stay_time, a, between, num, R, mo):
        super().__init__()
        # 变量赋值
        self.v1 = v1
        self.v2 = v2
        self.constant_time = constant_time
        self.stay_time = stay_time
        self.a = a
        self.between = between
        self.num = num
        self.R = R
        self.mo = mo
        self.n = 8
        self.w = 600  # 转速
        constant_t = constant_time
        motionless_t = stay_time
        accelerate_t = round(v2 / a, 2)
        self.t1 = accelerate_t
        self.t2 = constant_t
        self.t3 = accelerate_t
        self.t4 = motionless_t
        self.t5 = accelerate_t
        self.t6 = constant_t
        self.t7 = accelerate_t
        self.t8 = motionless_t
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

    def run(self):
        self.mod_rho, self.mod_theta = self.mod_information_calculate()
        matrix_results = self.start_multiprocessing()
        object_matrix, result = self.matrix_cal(matrix_results)
        self.result_ready.emit(object_matrix, result)

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

    def matrix_cal(self, H_all):
        sin_period = math.floor((2 * self.R + self.period * self.v1) / self.c_length_cell)  # 单个周期累加区域
        mid_period = math.floor((self.period * self.v1) / self.c_length_cell)  # 递增宽度
        H_period = H_all[:, 5:5 + sin_period]
        H_mid = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        for i in range(0, self.n):
            H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
                                                                   i * mid_period:i * mid_period + sin_period] + H_period
        # 多磨头叠加
        mul_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        mid_1 = math.floor(self.between / self.c_length_cell)
        for i in range(0, self.num):
            mul_H[:, mid_1 * i:self.c_length_mulcell - 1] = (
                    mul_H[:, mid_1 * i:self.c_length_mulcell - 1] +
                    H_mid[:, 0:self.c_length_mulcell - mid_1 * i - 1])
        # 计算 抛磨变异系数
        # 如果要计算此模块，周期数必须大于等于3
        cover_length = math.ceil(math.ceil(self.v1 * self.period + 2 * self.R) / 10)
        cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
        begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
        terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width
        begin_length = math.ceil((50 + self.v1 * 5 * self.period) / 10)
        terminate_length = begin_length + math.ceil((self.v1 * self.period + 2 * self.R) / 10)
        object_matrix = mul_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]
        equal_subsample = np.mean(object_matrix)  # 子样平均数
        middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
        variance_matrix = np.mean(middle_matrix)  # 子样方差
        result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
        return object_matrix, result

    def start_multiprocessing(self):
        value_list = [(0, self.t1, self.v1, self.v2, self.constant_time, self.stay_time, self.a, self.R, self.mod_rho,
                       self.mod_theta, self.mo,),
                      (self.t1, self.t1 + self.t2, self.v1, self.v2, self.constant_time, self.stay_time, self.a, self.R,
                       self.mod_rho, self.mod_theta, self.mo,),
                      (self.t1 + self.t2, self.t1 + self.t2 + self.t3, self.v1, self.v2, self.constant_time,
                       self.stay_time, self.a, self.R, self.mod_rho, self.mod_theta, self.mo,),
                      (self.t1 + self.t2 + self.t3, self.t1 + self.t2 + self.t3 + self.t4, self.v1, self.v2,
                       self.constant_time, self.stay_time, self.a, self.R, self.mod_rho, self.mod_theta, self.mo,),
                      (self.t1 + self.t2 + self.t3 + self.t4, self.t1 + self.t2 + self.t3 + self.t4 + self.t5, self.v1,
                       self.v2, self.constant_time, self.stay_time, self.a, self.R, self.mod_rho, self.mod_theta,
                       self.mo,),
                      (self.t1 + self.t2 + self.t3 + self.t4 + self.t5,
                       self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6, self.v1, self.v2, self.constant_time,
                       self.stay_time, self.a, self.R, self.mod_rho, self.mod_theta, self.mo,),
                      (self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6,
                       self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6 + self.t7, self.v1, self.v2,
                       self.constant_time, self.stay_time, self.a, self.R, self.mod_rho, self.mod_theta, self.mo,),
                      (self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6 + self.t7,
                       self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6 + self.t7 + self.t8, self.v1, self.v2,
                       self.constant_time, self.stay_time, self.a, self.R, self.mod_rho, self.mod_theta, self.mo,)]
        # 创建进程池 (4线程)
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