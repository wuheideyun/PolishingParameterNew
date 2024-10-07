import numpy as np
# 自定义抛光轨迹算法
def self_define_calculate(v1,ceramic_width,between,between_beam,R,a,num,group):
    B=ceramic_width+120-2*R
    distance_period=between*num
    t_all=round(distance_period/v1,2)
    # 边部停留时间设定
    if ceramic_width >= 1200:
        #t2 = 0.8
        t2=1.51
    else:
        t2 = 0.6
    t_a_in=(t_all-2*t2)/2
    # t_a 加速时间
    # t_e 匀速时间
    # H 摆幅
    # t_总=2*t_a+t_e
    # f=a*t_a^2-a*t_a*t_总+H
    par_a=a
    par_b=-a*t_a_in
    par_c=B
    if par_b**2-4*par_a*par_c>=0:
        t_a=(-par_b-(par_b**2-4*par_a*par_c)**0.5)/(2*a)
    else:
        t_a=t_a_in/2
        st='警告：摆幅不够'
    #t1 = t_a  # 加速时间
    t1 = round(t_a_in - 2*t_a,2)
    v2 = round(a * t_a, 2)
    delay_time=round((between_beam-2*between)/v1,2)
    self_delay_time=round(between/group/v1,2)
    result=np.zeros((1,8))
    result[0 , 0] = v1
    result[0 , 1] = v2
    result[0 , 2] = t1
    result[0 , 3] = t2
    result[0 , 4] = num*group
    result[0 , 5] = delay_time
    result[0 , 6] = self_delay_time
    result[0 , 7] = round(a*t_a**2+v2*t1,2)
    return result