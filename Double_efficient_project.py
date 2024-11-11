# 双头摆界面-----节能方案按钮功能逻辑
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import time as te
import multiprocessing
from matplotlib.patches import Rectangle  # 导入 Rectangle
# ——————————————出图程序（主程序）———————————————
def data_figure_plot(v1,ceramic_width,between,beam_between,R,a,mo):
    # 抛磨量分布子程序
    result = double_num_calculate(v1,ceramic_width,between,beam_between,R,a)
    v2 = result[1,1]
    constant_time =result[1,2]
    stay_time =result[1,3]
    num = result[1,4]
    delay_time = result[1,5]
    r_P_d = Polishing_distribution_Thread_order(v1, v2, constant_time, stay_time, a, between, beam_between, num, R, mo,delay_time)
    result_P_d_matrix,result_P_d_par = r_P_d.emit()
    # 轨迹中心线分布
    m_l_p = middle_line_plot_order(v1, v2, constant_time, stay_time, a, num, between, beam_between,delay_time)
    result_middle_line_x,result_middle_line_y = m_l_p.inner_calculate()
    # ---------绘制组合图-----------
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置微软雅黑字体
    plt.rcParams['axes.unicode_minus'] = False  # 避免坐标轴不能正常的显示负号
    fig = plt.figure('抛磨强度分布仿真')

    # 绘制抛磨量分布仿真
    ax_1 = fig.add_subplot(211)
    ax_1.set_aspect('equal', adjustable='box')
    object_matrix = result_P_d_matrix
    # 设置权重操作
    max_set = np.max(object_matrix)
    # 计算第90百分位的阈值（前15%）
    percentile_85 = np.percentile(object_matrix, 85)
    # 对矩阵中大于等于该阈值的元素乘以0.85
    object_matrix[object_matrix >= percentile_85] *= 0.85
    im = ax_1.contourf(object_matrix, levels=15, alpha=1, cmap='jet', vmin=0, vmax=max_set)
    ax_1.set_xlabel('Tile feed direction')
    ax_1.set_ylabel('Beam swing direction')
    divider = make_axes_locatable(ax_1)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    plt.colorbar(im, cax=cax)
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
    single_X_location, single_Y_location = m_l_p.inner_calculate()
    # 设置图层属性
    ax_2 = fig.add_subplot(212)
    ax_2.set_xlim((-200, period * 3 * v1 + between))
    ax_2.set_ylim((-200, a * (v2 / a) ** 2 + v2 * constant_t + 600))
    ax_2.set_aspect('equal', adjustable='box')
    # 设置图片文本
    ani_text = ax_2.text(0.7, 0.82, '', transform=ax_2.transAxes, fontsize=10)
    ani_text.set_text('Same_grinding_num=%.0f' % float(num))
    # 设置坐标轴名称
    ax_2.set_xlabel('Tile feed direction')
    ax_2.set_ylabel('Beam swing direction')
    num_two = math.ceil(num / 2)
    color_7 = ['red', 'orange', 'green', 'cyan', 'blue', 'purple', 'yellow', 'lightgreen',
               'slategrey', 'cornflowerblue', 'navy', 'indigo', 'violet', 'plum', 'oldlace', 'maroon',
               'lightcyan', 'lightseagreen', 'seagreen', 'springgreen']  # 红橙黄绿青蓝紫
    all_time_n = math.floor(period / 0.01) * 3
    # all_time_n = math.floor(period / msize) * n
    for i in range(0, num_two):
        ax_2.scatter(single_X_location[0, 0:all_time_n - 1] + i * beam_between - i * delay_time * v1,
                   single_Y_location[0, 0:all_time_n - 1],
                   color=color_7[i], s=1)
        ax_2.scatter(single_X_location[0,
                   0:all_time_n - 1] + i * beam_between + between - i * delay_time * v1,
                   single_Y_location[0, 0:all_time_n - 1],
                   color=color_7[i], s=1)
    plt.show()
# --------------参数计算函数---------------
def double_num_calculate(v1,ceramic_width,between,beam_between,R,a):
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
    B = (ceramic_width + 120) - 2 * R           # 摆幅（要求两极限位置各伸出60mm）
    t_a_ = v2_ / a                    # 加速时间
    t_e = (B - a * t_a_ ** 2) / v2_   # 匀速时间
    t_between = between / v1 * coef_1          # 边部停留时长
    period_1 = 4 * t_a_ + 2 * t_e + 2 * t_between     # 单周期时间
    num_1 = math.ceil(v1 * period_1 / between)       # 同粒度磨头数目
    if num_1 % 2 != 0:
        num_1 = num_1 + 1
    t_beam = (num_1 * between - 2 * t_between*v1) / (2 * v1)   # 2 * t_a + t_e
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
    result[0,0] = round(v1,2)
    result[0,1] = round(v2,2)
    result[0,2] = round(t_e,2)
    result[0,3] = round(t_between,2)
    result[0,4] = round(num_1)
    result[0,5] = round((beam_between-2*between)/v1,2)
    result[0,6] = round(a*t_a**2+v2*t_e,2)
    # 方案二 高光泽度方案
    result[1,0] = round(v1,2)
    result[1,1] = round(v2,2)
    result[1,2] = round(t_e,2)
    result[1,3] = round(t_between * 2,2)
    result[1,4] = round(num_1 + 2,2)
    result[1,5] = round((beam_between-2*between)/v1,2)
    result[1,6] = round(a*t_a**2+v2*t_e,2)
    return result
# ------------抛磨量分布仿真函数-------------
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
class middle_line_plot_order():
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

if __name__ == '__main__':
    data_figure_plot(300,900,600,1900,270,650,140)