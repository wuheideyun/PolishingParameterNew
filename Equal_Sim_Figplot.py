import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
def equal_plot(v1, v2, t1, t2, a, R, between, num):
        # 放置参数信息
        '''
        self.num = num
        self.v1 = v1
        self.v2 = v2
        self.a = a
        self.R = R
        self.between = between
        self.n = 3
        self.accelerate_t = self.v2 / self.a
        self.constant_t = t1  # 匀速时间
        self.motionless_t = t2  # 边布停留时间
        '''
        period = round(4 * v2/a + 2 * t1 + 2 * t2,2)
        n=3
        msize=0.15
        plot_figure(v1,v2,t1,t2,a,R,period,n,num,between,msize)
def cal_matrix(v1,v2,constant_t,motionless_t,a,between,msize):
        '''
        num=self.num
        v1=self.v1
        v2=self.v2
        constant_t=self.constant_t
        motionless_t=self.motionless_t
        a=self.a
        R=self.R
        # -----------正式计算--------------
        # ----------磨头间距计算------------
        between=self.between
        #---------------------------------
        # 参数赋值
        accelerate_t=self.accelerate_t
        '''
        accelerate_t=round(v2/a,2)
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
        #msize=0.15
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
        return single_X_location,single_Y_location
def plot_figure(v1,v2,t1,t2,a,R,period,n,num,between,msize):
        # 绘图模块
        fig = plt.figure(figsize=(10, 4))
        ax = fig.add_subplot(111) # 默认111代表1*1的图的第一个子图
        #设置坐标轴范围
        ax.set_xlim((-(30+R), period*n*v1+(num-1)*between+100))
        #设置坐标轴名称
        ax.set_xlabel('Tile feed direction')
        ax.set_ylabel('Beam swing direction')
        color_7 = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple'] # 红橙黄绿青蓝紫
        ax.axis('equal')
        #绘制x、y的坐标标识
        #xtext_ani = plt.text(period*(n-1)*v1+600,a*t1**2+v2*t2+540,'',fontsize=10)
        #ytext_ani = plt.text(period*(n-1)*v1+600,a*t1**2+v2*t2+240,'',fontsize=10)
        single_X_location,single_Y_location=cal_matrix(v1,v2,t1,t2,a,between,msize)
        T_size = math.floor(period / msize)
        all_time_n = T_size*n
        for i in range(0,all_time_n):
            for j in range(0,num):
                circle = Circle(xy=(single_X_location[0,i]+j*between,
                       single_Y_location[0,i]-0.5*(a*t1**2+v2*t2)), radius=R, alpha=0.1, color=color_7[j])
                ax.add_patch(circle)
            plt.pause(0.05)
        plt.show()  #  保存显示函数图像