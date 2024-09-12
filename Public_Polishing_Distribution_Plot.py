import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
def polishing_distribution_Plot(object_matrix):
    # 设置权重操作
    max_set=np.max(object_matrix)
    # 计算第90百分位的阈值（前10%）
    percentile_85 = np.percentile(object_matrix, 85)
    # 对矩阵中大于等于该阈值的元素乘以0.95
    object_matrix[object_matrix >= percentile_85] *= 0.85
    # 在主线程中绘图
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置微软雅黑字体
    plt.rcParams['axes.unicode_minus'] = False  # 避免坐标轴不能正常的显示负号
    fig = plt.figure('抛磨强度分布仿真')
    ax = fig.add_subplot(111)
    ax.set_aspect('equal', adjustable='box')
    im=ax.contourf(object_matrix,levels=15,alpha=1,cmap='jet',vmin=0,vmax=max_set)
    plt.xlabel('Tile feed direction')
    plt.ylabel('Beam swing direction')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    plt.colorbar(im, cax=cax)
    plt.show()  # 显示函数图像