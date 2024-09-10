import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PySide6.QtCore import QThread, Signal
import time as te
# 抛磨量分布，子工作线程
class Polishing_distribution_Thread(QThread):
    result_ready= Signal(np.ndarray,str)
    def __init__(self,v1, v2, t1, t2, a, between, num, R, mo):
        super().__init__()
        # 变量赋值
        self.v1=v1
        self.v2=v2
        self.t1=t1
        self.t2=t2
        self.a=a
        self.between=between
        self.num=num
        self.R=R
        self.mo=mo
    def run(self):
        # 各项参数
        object_matrix, result = self.inner_calculate()
        # 绘图（改放到主线程）
        '''
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.gca().set_aspect(1)  # x、y轴等刻度
        im = ax.contourf(object_matrix, 15, alpha=1, cmap='jet')
        plt.xlabel('Tile feed direction')
        plt.ylabel('Beam swing direction')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        plt.colorbar(im, cax=cax)
        '''
        #plt.show()  # 显示函数图像
        self.result_ready.emit(object_matrix, result)
    def inner_calculate(self):
        v1=self.v1
        v2=self.v2
        a=self.a
        between=self.between
        num=self.num
        R=self.R
        mo=self.mo
        constant_t=self.t1
        motionless_t=self.t2
        R_small = R - mo  # 磨头小径
        accelerate_t = round(v2 / a,2)
        t1 = accelerate_t
        t2 = constant_t
        t3 = accelerate_t
        t4 = motionless_t
        t5 = accelerate_t
        t6 = constant_t
        t7 = accelerate_t
        t8 = motionless_t
        between_inner = between
        period = 4 * accelerate_t + 2 * motionless_t + 2 * constant_t
        # 计算
        w = 600  # 转速
        n = 6  # 周期数目（必须）
        size = 0.01  # 时间步长
        time = np.arange(0, period, size)  # 时间变量
        T_size = math.floor(period / size)  # 单周期步长
        # 磨块离散化计算   以磨块 长 64mm 宽 110mm 为例
        # 仅仅计算单磨头，为了减少计算量，后续磨头直接进行叠加；
        mod_length = 64  # 磨块长度
        mod_width = mo  # 磨块宽度

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
        mod_y = mod_y + R_small  # 第一个磨块位置
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
        # 拓展为六个磨块
        # 以10*10为最小单位 ，将瓷砖离散化，以每个格子的中心作为每个格子的坐标(0.5,0.5)
        c_length = math.ceil(v1 * period * n + 2 * R + 50)  # 统计区域长度
        c_width = math.ceil(v2 * t2 + a * t1 ** 2 + 2 * R + 100)  # 统计区域宽度

        c_length_cell = 10  # 统计区域长度最小单位
        c_width_cell = 10  # 统计区域宽度最小单位

        c_length_percell = round(math.ceil(v1 * period + 2 * R + 100) / c_length_cell)  # 统计区域长度方向总单元格数目
        c_length_mulcell = round(c_length / c_length_cell)  # 统计区域长度方向总单元格数目
        c_width_mulcell = round(c_width / c_width_cell)  # 统计区域宽度方向总单元格数目

        H = np.zeros((c_width_mulcell, c_length_percell))  # 存放速度和
        H_mid = np.zeros((c_width_mulcell, c_length_mulcell))
        # 计算单个周期磨头抛磨量分布
        for k in range(0, T_size):
            # k=math.floor(k)
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
                        # frequency(m_y,m_x)=frequency(m_y,m_x)+1; # 统计各个磨削区域磨削频数
        sin_period = math.floor((2 * R + period * v1) / c_length_cell)  # 单个周期累加区域
        mid_period = math.floor((period * v1) / c_length_cell)  # 递增宽度
        H_period = H[:, 5:5 + sin_period]
        for i in range(0, n):
            H_mid[:, i * mid_period:i * mid_period + sin_period] = H_mid[:,
                                                                   i * mid_period:i * mid_period + sin_period] + H_period
        # 多磨头叠加
        mul_H = np.zeros((c_width_mulcell, c_length_mulcell))
        mid_1 = math.floor(between / c_length_cell)
        for i in range(0, num):
            mul_H[:, mid_1 * i:c_length_mulcell - 1] = (
                    mul_H[:, mid_1 * i:c_length_mulcell - 1] +
                    H_mid[:, 0:c_length_mulcell - mid_1 * i - 1])
        # 计算 抛磨变异系数
        # 如果要计算此模块，周期数必须大于等于3
        cover_length = math.ceil(math.ceil(v1 * period + 2 * R) / 10)
        cover_width = math.ceil(math.ceil(v2 * t2 + a * t1 ** 2 + 2 * R) / 10)
        begin_width = math.ceil(math.ceil(c_width_mulcell - cover_width) / 2)
        terminate_width = math.ceil(math.ceil(c_width_mulcell - cover_width) / 2) + cover_width
        begin_length = math.ceil((50 + v1 * 3 * period) / 10)
        terminate_length = begin_length + math.ceil((1 * v1 * period + 2 * R) / 10)
        #object_matrix = np.zeros((terminate_width - begin_width, terminate_length - begin_length))
        object_matrix = mul_H[begin_width + 1:terminate_width, begin_length + 1:terminate_length]
        equal_subsample = np.mean(object_matrix)  # 子样平均数
        middle_matrix = np.power(object_matrix, 2) - np.power(equal_subsample, 2)
        variance_matrix = np.mean(middle_matrix)  # 子样方差
        result = format(variance_matrix ** 0.5 / equal_subsample, '.4f')  # 抛磨变异系数
        #print(result)
        return object_matrix, result