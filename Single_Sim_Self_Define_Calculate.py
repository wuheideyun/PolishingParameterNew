import numpy as np
# 自定义抛光轨迹算法
def self_define_calculate(v1,beam_speed_up,ceramic_width,between_beam,R,a,num,stay_time):
    # 计算单周期时间
    B=ceramic_width+120-2*R
    t_a=round(beam_speed_up/a,2)
    if a*t_a**2>=B:
        t_a=round((B/a)**0.5,2)
        t_e=0
    else:
        t_e=round(((B-a*t_a**2)/beam_speed_up),2)
    t_period=4*t_a+2*t_e+2*stay_time
    # 计算磨头间距
    between=round(v1*t_period/num,2)
    # 计算延时时间
    delay_time=round((between_beam-between)/v1,2)
    result=np.zeros((1,8))
    result[0 , 0] = v1
    result[0 , 1] = round(t_a*a,2)
    result[0 , 2] = t_e
    result[0 , 3] = stay_time
    result[0 , 4] = num
    result[0 , 5] = delay_time
    result[0 , 6] = round(a*t_a**2+t_a*a*t_e,2)
    result[0,  7] = between
    return result