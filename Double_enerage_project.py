# 双头摆界面-----节能方案按钮功能逻辑
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import time as te
import multiprocessing
from matplotlib.patches import Rectangle  # 导入 Rectangle
from PySide6.QtCore import Qt, Signal, QThread
from Public_Animation_Split import split_gif
from matplotlib.patches import Circle
from matplotlib import animation
# ——————————————出图程序———————————————
# 子线程执行多进程计算任务
class Double_enerage_WorkerThread(QThread):
    result_signal = Signal(object)  # 创建一个信号用于传递结果
    def __init__(self,v1, ceramic_width, between, beam_between, R, a,mo,animation_name):
        super().__init__()
        self.v1 = v1
        self.ceramic_width = ceramic_width
        self.between = between
        self.beam_between = beam_between
        self.R = R
        self.a = a
        self.mo = mo
        self.animation_name_input = animation_name
        self.fig = plt.figure('运行轨迹动画', figsize=(10, 4))
        deep_blue = (31 / 255, 55 / 255, 96 / 255)
        self.fig.patch.set_facecolor(deep_blue)
    def run(self):
        # 参数计算
        result = self.double_num_calculate(self.v1, self.ceramic_width, self.between, self.beam_between, self.R, self.a)
        v2 = result[0, 1]
        constant_time = result[0, 2]
        stay_time = result[0, 3]
        num = result[0, 4]
        delay_time = result[0, 5]
        # 抛磨量分布--计算
        PD_order = Polishing_distribution_Thread_order(self.v1, v2, constant_time, stay_time, self.a, self.between, self.beam_between, num,
                                                       self.R,self.mo, delay_time)
        self.result_P_d_matrix, self.result_P_d_par = PD_order.emit()
        # 中心轨迹曲线--计算
        Mlp_order = Middle_line_plot_order(self.v1, v2, constant_time, stay_time, self.a, num, self.between, self.beam_between, delay_time)
        self.single_X_location, self.single_Y_location = Mlp_order.inner_calculate()
        # 动画生成
        Apo = Animation_produce_order(self.v1,v2,constant_time,stay_time,self.a,self.R,num,delay_time,self.between,self.beam_between,self.animation_name_input,self.fig)
        animation_name_output = Apo.emit()
        # 参数传递
        self.result = result
        # 结果输出
        list_1 = [self.result_P_d_matrix, self.result_P_d_par, self.single_X_location, self.single_Y_location]
        par_dict = {"v1":self.result[0,0] ,"v2":self.result[0,1] ,"constant_time":self.result[0,2],"stay_time":self.result[0,3],
                    "num":self.result[0,4],"delay_time":self.result[0,5],"swing":self.result[0,6],"ceramic_width":self.ceramic_width,
                    "between":self.between,"beam_between":self.beam_between,"R":self.R,"a":self.a}
        list= [list_1, par_dict,animation_name_output]
        data = list
        self.result_signal.emit(data)  # 发射信号将结果传回主线程
    # 参数计算函数
    def double_num_calculate(self,v1, ceramic_width, between, beam_between, R, a):
        # 轨迹重叠量（0~200），可调整轨迹优化性能
        overlap = 10
        # 摆动速度上限值（防止摆动速度过载）
        beam_speed_up = 800
        # coef_1-边部停留时间系数，参数范围（0.5~1.0）可调整轨迹优化性能
        coef_1 = 0.9
        theta = math.asin((2 * R - overlap) / between)
        k = math.tan(theta)
        # 判断皮带速度是否过快
        v2_mid = k * v1
        if v2_mid <= beam_speed_up:
            v2_ = v2_mid
        else:
            v2_ = beam_speed_up
        # 中间计算(边部停留时长为单倍磨头间距)
        B = (ceramic_width + 120) - 2 * R  # 摆幅（要求两极限位置各伸出60mm）
        t_a_ = v2_ / a  # 加速时间
        t_e = (B - a * t_a_ ** 2) / v2_  # 匀速时间
        t_between = between / v1 * coef_1  # 边部停留时长
        period_1 = 4 * t_a_ + 2 * t_e + 2 * t_between  # 单周期时间
        num_1 = math.ceil(v1 * period_1 / between)  # 同粒度磨头数目
        if num_1 % 2 != 0:
            num_1 = num_1 + 1
        t_beam = (num_1 * between - 2 * t_between * v1) / (2 * v1)  # 2 * t_a + t_e
        #
        # f_1 = a * t_a ^ 2 - t_beam * a * t_a + B;
        #
        if (t_beam * a) ** 2 - 4 * a * B >= 0:
            t_a = (-((t_beam * a) ** 2 - 4 * a * B) ** 0.5 + a * t_beam) / (2 * a)
            # t1 = (((t_beam * a) ^ 2 - 4 * a * B) ^ 0.5 + a * t_beam) / (2 * a)
        else:
            t_a = t_beam / 2
        v2 = round(t_a * a, 2)
        t_e = round(t_beam - 2 * t_a, 2)
        # 结果输出
        result = np.zeros((2, 7))
        # 方案一 节能方案
        result[0, 0] = round(v1, 2)
        result[0, 1] = round(v2, 2)
        result[0, 2] = round(t_e, 2)
        result[0, 3] = round(t_between, 2)
        result[0, 4] = round(num_1)
        result[0, 5] = round((beam_between - 2 * between) / v1, 2)
        result[0, 6] = round(a * t_a ** 2 + v2 * t_e, 2)
        # 方案二 高光泽度方案
        result[1, 0] = round(v1, 2)
        result[1, 1] = round(v2, 2)
        result[1, 2] = round(t_e, 2)
        result[1, 3] = round(t_between * 2, 2)
        result[1, 4] = round(num_1 + 2, 2)
        result[1, 5] = round((beam_between - 2 * between) / v1, 2)
        result[1, 6] = round(a * t_a ** 2 + v2 * t_e, 2)
        return result
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
# -------------抛磨量分布仿真计算函数-------------
class Polishing_distribution_Thread_order():
    def __init__(self,v1, v2, constant_time, stay_time, a, between, beam_between, num, R, mo,delay_time):
        # 变量赋值
        self.v1 = v1
        self.v2 = v2
        self.constant_time = constant_time
        self.stay_time = stay_time
        self.delay_time=delay_time
        self.a = a
        self.between = between
        self.beam_between=beam_between
        self.num = num
        self.R = R
        self.mo = mo
        self.n = 6
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

    def emit(self):
        self.mod_rho, self.mod_theta = self.mod_information_calculate()
        matrix_results = self.start_multiprocessing()
        object_matrix, result = self.matrix_cal(matrix_results)
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
        between_cell = math.floor(self.between / self.c_length_cell)
        delay_cell=math.floor(self.delay_time*self.v1/ self.c_length_cell)
        for i in range(0, 2):
            mul_H[:, between_cell * i:self.c_length_mulcell - 1] = (
                    mul_H[:, between_cell * i:self.c_length_mulcell - 1] +
                    H_mid[:, 0:self.c_length_mulcell - between_cell * i - 1])
        num_two = math.floor(self.num / 2)
        all_H = np.zeros((self.c_width_mulcell, self.c_length_mulcell))
        beam_between_cell = math.floor(self.beam_between / self.c_length_cell)
        for i in range(0, num_two):
            all_H[:, (beam_between_cell-delay_cell) * i:self.c_length_mulcell - 1] = (
                    all_H[:,(beam_between_cell-delay_cell) * i:self.c_length_mulcell-1] +
                    mul_H[:,0:self.c_length_mulcell-(beam_between_cell-delay_cell)*i-1])
        # 计算 抛磨变异系数
        # 如果要计算此模块，周期数必须大于等于3
        cover_width = math.ceil(math.ceil(self.v2 * self.t2 + self.a * self.t1 ** 2 + 2 * self.R) / 10)
        begin_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2)
        terminate_width = math.ceil(math.ceil(self.c_width_mulcell - cover_width) / 2) + cover_width
        begin_length = math.ceil((50 + self.v1 * 3 * self.period) / 10)
        terminate_length = begin_length + math.ceil((1 * self.v1 * self.period + 2 * self.R) / 10)

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
# ------------- 轨迹中心线分布---------------
class Middle_line_plot_order():
    def __init__(self, v1, v2, t1, t2, a, num, between, beam_between,delay_time):
        # 变量输入
        self.v1 = v1
        self.v2 = v2
        self.constant_t = t1
        self.motionless_t = t2
        self.a = a
        self.num = num
        self.between = between
        self.beam_between = beam_between
        self.delay_time = delay_time
        self.n=3
    def inner_calculate(self):
        # 参数赋值
        v1 = self.v1
        v2 = self.v2
        accelerate_t = self.v2 / self.a
        constant_t = self.constant_t
        a = self.a
        motionless_t = self.motionless_t
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
        self.msize = 0.01
        msize = self.msize
        time = np.arange(0, period, msize)  # 时间变量
        T_size = math.floor(period / msize)  # 单周期步长
        self.cross_size = round((2 * round(v2 / a, 2) + t1 + t2) / self.msize)
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
        self.all_time_n = T_size * n
        single_X_location = np.zeros((1, self.all_time_n))
        single_Y_location = np.zeros((1, self.all_time_n))
        for i in range(0, n):
            single_X_location[0, i * T_size:(i + 1) * T_size] = X_location + period * v1 * i
            single_Y_location[0, i * T_size:(i + 1) * T_size] = Y_location
        return single_X_location, single_Y_location
# -------------轨迹动画-------------
class Animation_produce_order():
    def __init__(self,v1,v2,t1,t2,a,R,num,delay_time,between,beam_between,animation_name,figure):
        # 参数赋值
        self.animation_name = animation_name

        self.v1 = v1
        self.v2 = v2
        self.t1 = t1
        self.t2 = t2
        self.a = a
        self.R = R
        self.between = between
        self.num = num
        self.delay_time = delay_time
        self.beam_between = beam_between
        self.n = 6
        self.msize = 0.15

        self.delay_time_size = round(self.delay_time / self.msize)
        self.beam_between_cell = math.floor(beam_between / v1 / self.msize)  # 横梁步长
        self.cross_size = round((2 * round(v2 / a, 2) + t1 + t2) / self.msize)
        self.num_two = math.floor(num / 2)
        period = round(4 * (v2 / a) + 2 * t1 + 2 * t2, 2)
        self.all_time_n = math.floor(period / self.msize) * self.n
        self.color_7 = ['red', 'orange', 'green', 'cyan', 'blue', 'purple', 'yellow',
                        'lightgreen', 'slategrey', 'cornflowerblue', 'navy', 'indigo', 'violet',
                        'plum', 'oldlace', 'maroon', 'lightcyan', 'lightseagreen', 'seagreen', 'springgreen']  # 红橙黄绿青蓝紫
        # 计算矩阵
        self.single_X_location, self.single_Y_location = self.inner_cal_matrix()
        # 创建坐标绘图区
        #self.fig = plt.figure('运行轨迹动画', figsize=(10, 4))
        self.fig = figure
        self.ax = self.fig.add_subplot(111)  # 默认111代表1*1的图的第一个子图
        # 设置坐标轴范围
        self.x_range = [-(self.num_two * between + (self.num_two - 1) * (beam_between - delay_time * v1) + 540),
                        period * 3 * v1]
        self.ax.set_xlim(self.x_range)
        # 使用系数设定范围
        self.ax.set_ylim((-0.5 * 1.3 * ((a * (v2 / a) ** 2 + v2 * t1) + R),
                          0.5 * 2.5 * ((a * (v2 / a) ** 2 + v2 * t1) + R)))
        self.ax.set_aspect('equal', adjustable='box')
        # 设置坐标轴名称
        self.ax.set_xlabel('Tile feed direction')
        self.ax.set_ylabel('Beam swing direction')
        # 单独隐藏刻度和标签
        self.ax.set_xticks([])  # 隐藏刻度
        self.ax.set_xticklabels([])  # 隐藏刻度标签
        # self.x_range_numtext = 0
        self.one_size = self.msize * self.v1
        # 标识符位置设定
        self.grinding_num = self.ax.text(0.7, 0.90, '', transform=self.ax.transAxes, fontsize=10,color='white')
        # self.xtext_ani = self.ax.text(0.7,0.80,'',transform=self.ax.transAxes,fontsize=10)
        self.ytext_ani = self.ax.text(0.7, 0.78, '', transform=self.ax.transAxes, fontsize=10,color = 'white')
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
        v1 = self.v1
        v2 = self.v2
        constant_t = self.t1
        motionless_t = self.t2
        a = self.a
        between = self.between
        msize = self.msize
        accelerate_t = round(v2 / a, 2)
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
        between_cell = math.floor(between / v1 / msize)  # 间距步长
        time = np.arange(0, period, msize)  # 时间变量
        T_size = math.floor(period / msize)  # 单周期步长
        # 磨头中心坐标
        X_location = np.zeros((1, T_size))
        Y_location = np.zeros((1, T_size))
        for k in range(0, T_size):
            t = time[k]
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
            X_location[0, k] = x_0
            Y_location[0, k] = y_0
        all_time_n = T_size * n
        single_X_location = np.zeros((1, all_time_n))
        single_Y_location = np.zeros((1, all_time_n))
        for i in range(0, n):
            single_X_location[0, i * T_size:(i + 1) * T_size] = X_location + period * v1 * i
            single_Y_location[0, i * T_size:(i + 1) * T_size] = Y_location
        return single_X_location, single_Y_location

    def update(self, j):
        # 设置坐标轴移动
        self.x_range[0] -= self.one_size
        self.x_range[1] -= self.one_size
        self.ax.set_xlim(self.x_range)
        # 绘制x、y、num的标识(坐标信息相对不移动)
        self.grinding_num.set_text('Same_grinding_num=%.0f' % float(self.num))
        # self.xtext_ani.set_text('x_location=%.3f mm' % (self.single_X_location[0, j]))
        self.ytext_ani.set_text(
            'y_location=%.3f mm' % (self.single_Y_location[0, j] - 0.5 * (self.v2 ** 2 / self.a + self.v2 * self.t1)))
        # 绘制抛光轨迹进行叠加
        patches_1 = []
        patches_2 = []
        for i in range(0, self.num_two):
            # 延时绘制效果
            if j >= self.delay_time_size * i:
                circle_1 = Circle(xy=(-(self.single_X_location[0, j] + (self.num_two - i - 1) * self.beam_between),
                                      self.single_Y_location[0, j - self.delay_time_size * i] - 0.5 * (
                                                  self.v2 ** 2 / self.a + self.v2 * self.t1)),
                                  radius=self.R, alpha=0.05,
                                  color=self.color_7[i])
                circle_2 = Circle(
                    xy=(-(self.single_X_location[0, j] + (self.num_two - i - 1) * self.beam_between - self.between),
                        self.single_Y_location[0, j - self.delay_time_size * i] - 0.5 * (
                                    self.v2 ** 2 / self.a + self.v2 * self.t1)), radius=self.R, alpha=0.05,
                    color=self.color_7[i])
                self.ax.add_patch(circle_1)
                self.ax.add_patch(circle_2)
                patches_1.append(circle_1)
                patches_2.append(circle_2)
        return [self.grinding_num, self.ytext_ani] + patches_1 + patches_2

    def emit(self):
        ani = animation.FuncAnimation(self.fig, self.update, frames=self.all_time_n, interval=100, repeat=False)
        # ani.save('animation/' + self.animation_name + '.gif', fps=30, writer='pillow')
        # ani.save(self.animation_name + '.gif', fps=30, writer='pillow')
        ani.save('donghua.gif', fps=30, writer='pillow')
        plt.close(self.fig)
        # 动画分割
        # input_gif = 'animation/' + self.animation_name + '.gif'
        # split_frames = int(self.all_time_n / self.n * 4)
        # output_gif_1 = 'animation/' + self.animation_name + '_1' + '.gif'
        # output_gif_2 = 'animation/' + self.animation_name + '_2' + '.gif'
        # split_gif(input_gif, split_frames, output_gif_1, output_gif_2)
        print('test')
        return 'donghua.gif'


