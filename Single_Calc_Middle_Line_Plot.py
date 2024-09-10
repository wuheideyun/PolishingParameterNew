import numpy as np
import math
import matplotlib.pyplot as plt
class middle_line_plot_order():
    def __init__(self, v1, v2, t1, t2, a, num, between, between_beam,delay_time):
        # 变量输入
        self.v1 = v1
        self.v2 = v2
        self.constant_t = t1
        self.motionless_t = t2
        self.a = a
        self.num = num
        self.between = between
        self.between_beam = between_beam
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
    def figure_plot(self):
        msize = 0.01
        n = self.n
        accelerate_t = self.v2 / self.a
        constant_t = self.constant_t
        motionless_t = self.motionless_t
        period = 4 * accelerate_t + 2 * motionless_t + 2 * constant_t
        single_X_location, single_Y_location = self.inner_calculate()
        # 设置图层属性
        fig = plt.figure('磨头中心轨迹曲线', figsize=(10, 4))
        ax = fig.add_subplot(111)
        ax.set_xlim((-200, period * 3 * self.v1 + self.between))
        ax.set_ylim((-200, self.a * (self.v2 / self.a) ** 2 + self.v2 * self.constant_t + 600))
        ax.set_aspect('equal', adjustable='box')
        # 设置图片文本
        ani_text = ax.text(0.7, 0.82, '', transform=ax.transAxes, fontsize=10)
        ani_text.set_text('Same_grinding_num=%.0f' % self.num)
        # 设置坐标轴名称
        plt.xlabel('Tile feed direction')
        plt.ylabel('Beam swing direction')
        color_7 = ['red', 'orange', 'green', 'cyan', 'blue', 'purple', 'yellow','lightgreen',
                   'slategrey','cornflowerblue','navy','indigo','violet','plum','oldlace','maroon',
                   'lightcyan','lightseagreen','seagreen','springgreen']  # 红橙黄绿青蓝紫
        for i in range(0, self.num):
                ax.scatter(single_X_location[0, 0:self.all_time_n-1] + i * self.between_beam - i*self.delay_time*self.v1,
                           single_Y_location[0, 0:self.all_time_n-1],
                           color=color_7[i],s=1)
        plt.show()  # 显示函数图像
class middle_line_plot_self_define_order():
    def __init__(self, v1, v2, t1, t2, a, num, between, between_beam,delay_time,group):
        # 变量输入
        self.v1 = v1
        self.v2 = v2
        self.constant_t = t1
        self.motionless_t = t2
        self.a = a
        self.num = num
        self.between = between
        self.between_beam = between_beam
        self.delay_time = delay_time
        self.group=math.floor(group)
        self.n=3
    def inner_calculate(self):
        # 参数赋值
        v1 = self.v1
        v2 = self.v2
        accelerate_t = self.v2 / self.a
        constant_t = self.constant_t
        a = self.a
        motionless_t = self.motionless_t
        between = self.between
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
    def figure_plot(self):
        msize = 0.01
        n = self.n
        accelerate_t = self.v2 / self.a
        constant_t = self.constant_t
        motionless_t = self.motionless_t
        period = 4 * accelerate_t + 2 * motionless_t + 2 * constant_t
        T_size = math.floor(period / msize)  # 单周期步长
        single_X_location, single_Y_location = self.inner_calculate()
        # 设置图层属性
        fig = plt.figure('磨头中心轨迹曲线', figsize=(10, 4))
        # fig.suptitle('磨头中心轨迹曲线')
        ax = fig.add_subplot(111)
        ax.set_xlim((-200, period * 3 * self.v1 + self.between))
        ax.set_ylim((-200, self.a * (self.v2 / self.a) ** 2 + self.v2 * self.constant_t + 600))
        ax.set_aspect('equal', adjustable='box')
        # 设置图片文本
        ani_text = ax.text(0.7, 0.82, '', transform=ax.transAxes, fontsize=10)
        ani_text.set_text('Same_grinding_num=%.0f' % (self.num*self.group))
        # 设置坐标轴名称
        plt.xlabel('Tile feed direction')
        plt.ylabel('Beam swing direction')
        color_7 = ['red', 'orange', 'green', 'cyan', 'blue', 'purple', 'yellow','lightgreen','slategrey','cornflowerblue','navy','indigo','violet','plum','oldlace','maroon','lightcyan','lightseagreen','seagreen','springgreen']  # 红橙黄绿青蓝紫
        self_delay_distance=self.between/self.group
        for i in range(0,self.group):
            for j in range(0, self.num):
                ax.scatter(single_X_location[0, 0:self.all_time_n-1] + j * self.between_beam - j*self.delay_time*self.v1 + self_delay_distance*i,
                           single_Y_location[0, 0:self.all_time_n-1],
                           color=color_7[i+j],s=1)
        plt.show()  # 显示函数图像