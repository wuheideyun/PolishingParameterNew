import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import animation
import time as te
from PySide6.QtCore import QThread, Signal
'''
class Animation_produce:
    def __init__(self,v1, v2, t1, t2, a, R, between,num):
        # 参数赋值
        self.v1=v1
        self.v2=v2
        self.t1=t1
        self.t2=t2
        self.a=a
        self.R=R
        self.between=between
        self.num=math.ceil(num)
        self.n=3
        self.msize=0.15
        period = round(4 * (v2 / a) + 2 * t1 + 2 * t2, 2)
        self.all_time_n = math.floor(period / self.msize) * self.n
        self.color_7 = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']  # 红橙黄绿青蓝紫
        # 计算矩阵
        self.single_X_location,self.single_Y_location=self.inner_cal_matrix()
        # 创建坐标绘图区
        self.fig = plt.figure(figsize=(10, 4))
        self.ax = self.fig.add_subplot(111)  # 默认111代表1*1的图的第一个子图
        # 设置坐标轴范围
        self.ax.set_xlim((-(30 + R), period * self.n * v1 + (num - 1) * between + 100))
        self.ax.set_ylim((-0.5 * (a * (v2 / a) ** 2 + v2 * t2) - R - 200,
                          0.5 * (a * (v2 / a) ** 2 + v2 * t1) + R + 800))
        self.ax.set_aspect('equal', adjustable='box')
        # 设置坐标轴名称
        self.ax.set_xlabel('Tile feed direction')
        self.ax.set_ylabel('Beam swing direction')
        # 绘制x、y、num的标识
        self.grinding_num = self.ax.text(period * (self.n - 0.5) * self.v1,
                                         0.5 * (a * (v2 / a) ** 2 + v2 * t1) + R + 600, '', fontsize=10)
        self.xtext_ani = self.ax.text(period*(self.n-0.5)*self.v1,0.5 * (a * (v2 / a) ** 2 + v2 * t1) + R + 400,'',fontsize=10)
        self.ytext_ani = self.ax.text(period*(self.n-0.5)*self.v1,0.5 * (a * (v2 / a) ** 2 + v2 * t1) + R + 200,'',fontsize=10)
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
        n=3
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
    def update(self,i):
        for j in range(0,self.num):
            circle = Circle(xy=(self.single_X_location[0,i]+j*self.between,
                   self.single_Y_location[0,i]-0.5*(self.v2**2/self.a+self.v2*self.t1)), radius=self.R, alpha=0.1, color=self.color_7[j])
            self.ax.add_patch(circle)
            # 设置标识符
            self.grinding_num.set_text('Same_grinding_num=%.0f' % self.num)
            self.xtext_ani.set_text('x_location=%.3f mm' % (self.single_X_location[0, i]))
            self.ytext_ani.set_text('y_location=%.3f mm' % (self.single_Y_location[0, i] - 0.5*(self.v2**2/self.a+self.v2*self.t1)))

    def animation_save(self):
        ani = animation.FuncAnimation(self.fig,self.update,frames=self.all_time_n,interval=50, repeat=False)
        ani.save('animation.gif', fps=30, writer='pillow')
'''
class Animation_produce(QThread):
    result_ready = Signal(str)
    def __init__(self,v1, v2, t1, t2, a, R, between,num):
        # 参数赋值
        super().__init__()
        self.v1=v1
        self.v2=v2
        self.t1=t1
        self.t2=t2
        self.a=a
        self.R=R
        self.between=between
        self.num=math.ceil(num)
        self.n=4
        self.msize=0.15
        period = round(4 * (v2 / a) + 2 * t1 + 2 * t2, 2)
        self.all_time_n = math.floor(period / self.msize) * self.n
        self.color_7 = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']  # 红橙黄绿青蓝紫
        # 计算矩阵
        self.single_X_location,self.single_Y_location=self.inner_cal_matrix()
        # 创建坐标绘图区
        self.fig = plt.figure('运行轨迹动画',figsize=(10, 4))
        self.ax = self.fig.add_subplot(111)  # 默认111代表1*1的图的第一个子图
        # 设置坐标轴范围
        self.x_range = [-(30 + R) - period * (self.n-1) * v1, (num - 1) * between + 200]
        self.ax.set_xlim(self.x_range)
        self.ax.set_ylim((-0.5 * (a * (v2 / a) ** 2 + v2 * t2) - R - 200,
                          0.5 * (a * (v2 / a) ** 2 + v2 * t1) + R + 800))
        self.ax.set_aspect('equal', adjustable='box')
        # 设置坐标轴名称
        self.ax.set_xlabel('Tile feed direction')
        self.ax.set_ylabel('Beam swing direction')
        self.x_range_numtext = 0
        self.one_size=self.msize * self.v1
        # 标识符位置设定
        self.grinding_num = self.ax.text(0.7,0.92,'',transform=self.ax.transAxes,fontsize=10,)
        self.xtext_ani = self.ax.text(0.7,0.82,'',transform=self.ax.transAxes,fontsize=10)
        self.ytext_ani = self.ax.text(0.7,0.72,'',transform=self.ax.transAxes,fontsize=10)
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
        n=4
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
    def update(self,i):
        # 设置坐标轴移动
        self.x_range[0] += self.one_size
        self.x_range[1] += self.one_size
        self.ax.set_xlim(self.x_range)
        # 绘制x、y、num的标识(坐标信息相对不移动)
        self.grinding_num.set_text('Same_grinding_num=%.0f' % self.num)
        self.xtext_ani.set_text('x_location=%.3f mm' % (self.single_X_location[0, i]))
        self.ytext_ani.set_text('y_location=%.3f mm' % (self.single_Y_location[0, i] - 0.5 * (self.v2 ** 2 / self.a + self.v2 * self.t1)))
        # 绘制抛光轨迹进行叠加
        for j in range(0,self.num):
            circle = Circle(xy=(self.single_X_location[0,i]+j*self.between,
                   self.single_Y_location[0,i]-0.5*(self.v2**2/self.a+self.v2*self.t1)), radius=self.R, alpha=0.1, color=self.color_7[j])
            self.ax.add_patch(circle)
    def run(self):
        ani = animation.FuncAnimation(self.fig,self.update,frames=self.all_time_n,interval=100, repeat=False)
        ani.save('animation.gif', fps=30, writer='pillow')
        self.result_ready.emit('动画保存成功')
        plt.close(self.fig)
