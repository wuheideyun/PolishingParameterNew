# 动画分割函数封装
from PIL import Image, ImageSequence
def split_gif(input_gif, split_frame, output_gif_1, output_gif_2):
    # 打开输入的 GIF 文件
    with Image.open(input_gif) as img:
        # 提取所有帧
        frames = [frame.copy() for frame in ImageSequence.Iterator(img)]

    # 将帧按照指定的 split_frame 进行分割
    frames_1 = frames[:split_frame]  # 前半部分帧
    frames_2 = frames[split_frame:]  # 后半部分帧

    # 保存前半部分为一个新的 GIF
    frames_1[0].save(
        output_gif_1,
        save_all=True,
        append_images=frames_1[1:],  # 保存所有帧
        loop=1,  # 无限循环
        duration=img.info['duration']  # 使用原始的帧持续时间
    )
    # 保存后半部分为另一个新的 GIF
    frames_2[0].save(
        output_gif_2,
        save_all=True,
        append_images=frames_2[1:],  # 保存所有帧
        loop=0,  # 无限循环
        duration=img.info['duration']  # 使用原始的帧持续时间
    )
'''
# 示例调用
input_gif = 'animation.gif'  # 输入的 GIF 文件
split_frame = 328  # 在第 50 帧分割
output_gif_1 = 'part1_animation.gif'  # 输出的第一个 GIF 文件
output_gif_2 = 'part2_animation.gif'  # 输出的第二个 GIF 文件
# 调用函数进行 GIF 分割
split_gif(input_gif, split_frame, output_gif_1, output_gif_2)
'''