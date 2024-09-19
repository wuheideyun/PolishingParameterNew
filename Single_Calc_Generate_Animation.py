import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import animation
import time as te
from PySide6.QtCore import QThread, Signal
from Public_Animation_Split import split_gif
class Animation_produce_order(QThread):
    result_ready = Signal(str)
    def __init__(self,v1,v2,t1,t2,a,R,between,beam_between,num,delay_time,animation_name):
        # 参数赋值
        super().__init__()
        self.animation_name = animation_name
        self.v1=v1
        self.v2=v2
        self.t1=t1
        self.t2=t2
        self.a=a
        self.R=R
        self.between=between
        self.num=math.ceil(num)
        self.beam_between=beam_between
        self.n=6
        self.msize=0.15
        self.delay_time=delay_time
        self.delay_time_size=round(delay_time / self.msize)
        self.beam_between_cell = math.floor(beam_between / v1 / self.msize)  # 横梁步长
        self.cross_size=round((2 * round(v2/a,2) + t1 + t2)/self.msize)
        self.num_two = math.floor(num / 2)
        period = round(4 * (v2 / a) + 2 * t1 + 2 * t2, 2)
        self.all_time_n = math.floor(period / self.msize) * self.n
        self.color_7 = ['red', 'orange', 'green', 'cyan', 'blue', 'purple', 'yellow','lightgreen','slategrey','cornflowerblue','navy','indigo','violet','plum','oldlace','maroon','lightcyan','lightseagreen','seagreen','springgreen']  # 红橙黄绿青蓝紫  # 红橙黄绿青蓝紫
        # 计算矩阵
        self.single_X_location,self.single_Y_location=self.inner_cal_matrix()
        # 创建坐标绘图区
        self.fig = plt.figure('运行轨迹动画',figsize=(10, 4))
        self.ax = self.fig.add_subplot(111)  # 默认111代表1*1的图的第一个子图
        # 设置坐标轴范围
        self.x_range = [-(self.num*between+(self.num-1)*(beam_between-between)+200),period * (self.n-2) * v1]
        self.ax.set_xlim(self.x_range)
        self.ax.set_ylim((-0.5 * 1.4 * ((a * (v2 / a) ** 2 + v2 * t2) + R),
                          0.5 * 2.3 * ((a * (v2 / a) ** 2 + v2 * t1) + R)))
        self.ax.set_aspect('equal', adjustable='box')
        # 设置坐标轴名称
        self.ax.set_xlabel('Tile feed direction')
        self.ax.set_ylabel('Beam swing direction')
        # 单独隐藏刻度和标签
        self.ax.set_xticks([])         # 隐藏刻度
        self.ax.set_xticklabels([])  # 隐藏刻度标签
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
    def update(self,j):
        # 设置坐标轴移动
        self.x_range[0] -= self.one_size
        self.x_range[1] -= self.one_size
        self.ax.set_xlim(self.x_range)
        # 绘制x、y、num的标识(坐标信息相对不移动)
        self.grinding_num.set_text('Same_grinding_num=%.0f' % self.num)
        self.xtext_ani.set_text('x_location=%.3f mm' % (self.single_X_location[0, j]))
        self.ytext_ani.set_text('y_location=%.3f mm' % (self.single_Y_location[0, j] - 0.5 * (self.v2 ** 2 / self.a + self.v2 * self.t1)))
        # 绘制抛光轨迹进行叠加
        patches = []
        for i in range(0, self.num):
            # 延时绘制效果
            if j>=self.delay_time_size*i:
                circle_1 = Circle(xy=(-(self.single_X_location[0, j] + (self.num-i-1)*self.beam_between),
                                          self.single_Y_location[0, j-self.delay_time_size*i] - 0.5 * (self.v2 ** 2 / self.a + self.v2 * self.t1)),
                                      radius=self.R, alpha=0.05,
                                      color=self.color_7[i])
                self.ax.add_patch(circle_1)
                patches.append(circle_1)
        return [self.grinding_num, self.xtext_ani, self.ytext_ani] + patches
    def run(self):
        ani = animation.FuncAnimation(self.fig,self.update,frames=self.all_time_n,interval=100, repeat=False)
        ani.save('animation/' + self.animation_name + '.gif', fps=30, writer='pillow')
        # 动画分割
        input_gif = 'animation/' + self.animation_name + '.gif'
        split_frames = int(self.all_time_n / self.n * 4)
        output_gif_1 = 'animation/' + self.animation_name + '_1' + '.gif'
        output_gif_2 = 'animation/' + self.animation_name + '_2' + '.gif'
        split_gif(input_gif, split_frames, output_gif_1, output_gif_2)

        self.result_ready.emit(self.animation_name)
        plt.close(self.fig)

class Animation_produce_order_define(QThread):
    result_ready = Signal(str)
    def __init__(self,v1,v2,t1,t2,a,R,between,beam_between,num,delay_time,animation_name):
        # 参数赋值
        super().__init__()
        self.animation_name = animation_name
        self.v1=v1
        self.v2=v2
        self.t1=t1
        self.t2=t2
        self.a=a
        self.R=R
        #self.group=group
        self.between=between
        self.num=math.ceil(num)
        self.beam_between=beam_between
        self.n=6
        self.msize=0.15
        #delay_time=[0,3.1,7,10.1,14.01,17.11,18.6,21.7]
        self.delay_time=delay_time
        #delay_time_define=round(between/group/v1,2)
        self.delay_time_size=round(delay_time / self.msize)
        self.beam_between_cell = math.floor(beam_between / v1 / self.msize)  # 横梁步长
        self.cross_size=round((2 * round(v2/a,2) + t1 + t2)/self.msize)
        #self.num_two = math.floor(num / 2)
        period = round(4 * (v2 / a) + 2 * t1 + 2 * t2, 2)
        self.all_time_n = math.floor(period / self.msize) * self.n
        #self.all_time_n_1 = math.floor(period / self.msize) * (self.n-1)
        self.color_7 = ['red', 'orange', 'green', 'cyan', 'blue', 'purple', 'yellow','lightgreen','slategrey','cornflowerblue','navy','indigo','violet','plum','oldlace','maroon','lightcyan','lightseagreen','seagreen','springgreen']  # 红橙黄绿青蓝紫
        # 计算矩阵
        self.single_X_location,self.single_Y_location=self.inner_cal_matrix()
        # 创建坐标绘图区
        self.fig = plt.figure('运行轨迹动画',figsize=(10, 4))
        self.ax = self.fig.add_subplot(111)  # 默认111代表1*1的图的第一个子图
        # 设置坐标轴范围
        #self.x_range = [-(self.num_two*between+(self.num_two-1)*(beam_between-between)+200),period * (self.n-2) * v1]
        self.x_range = [-(self.num * between + (self.num - 1) * (beam_between - between) + 200),
                        period * (self.n - 2) * v1]
        self.ax.set_xlim(self.x_range)
        self.ax.set_ylim((-0.5 * 1.3 * ((a * (v2 / a) ** 2 + v2 * t2) + R),
                          0.5 * 2.5 * ((a * (v2 / a) ** 2 + v2 * t1) + R)))
        self.ax.set_aspect('equal', adjustable='box')
        # 设置坐标轴名称
        self.ax.set_xlabel('Tile feed direction')
        self.ax.set_ylabel('Beam swing direction')
        # 单独隐藏刻度和标签
        # self.ax.set_xticks([])         # 隐藏刻度
        self.ax.set_xticklabels([])  # 隐藏刻度标签
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
        n=self.n
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
    def update(self,j):
        # 设置坐标轴移动
        self.x_range[0] -= self.one_size
        self.x_range[1] -= self.one_size
        self.ax.set_xlim(self.x_range)
        # 绘制x、y、num的标识(坐标信息相对不移动)
        self.grinding_num.set_text('Same_grinding_num=%.0f' % self.num)
        self.xtext_ani.set_text('x_location=%.3f mm' % (self.single_X_location[0, j]))
        self.ytext_ani.set_text('y_location=%.3f mm' % (self.single_Y_location[0, j] - 0.5 * (self.v2 ** 2 / self.a + self.v2 * self.t1)))
        # 绘制抛光轨迹进行叠加
        patches = []
        for i in range(0, self.num):
            # 延时绘制效果
            if j>=self.delay_time_size*i:
                circle_1 = Circle(xy=(-(self.single_X_location[0, j] + (self.num-i-1)*self.beam_between),
                                          self.single_Y_location[0, j-self.delay_time_size*i] - 0.5 * (self.v2 ** 2 / self.a + self.v2 * self.t1)),
                                      radius=self.R, alpha=0.05,
                                      color=self.color_7[i])
                self.ax.add_patch(circle_1)
                patches.append(circle_1)
        return [self.grinding_num, self.xtext_ani, self.ytext_ani] + patches
    def run(self):
        ani = animation.FuncAnimation(self.fig,self.update,frames=self.all_time_n,interval=100, repeat=False)
        ani.save('animation/' + self.animation_name + '.gif', fps=30, writer='pillow')
        # 动画分割
        input_gif = 'animation/' + self.animation_name + '.gif'
        split_frames = int(self.all_time_n / self.n * 4)
        output_gif_1 = 'animation/' + self.animation_name + '_1' + '.gif'
        output_gif_2 = 'animation/' + self.animation_name + '_2' + '.gif'
        split_gif(input_gif, split_frames, output_gif_1, output_gif_2)

        self.result_ready.emit(self.animation_name)
        plt.close(self.fig)