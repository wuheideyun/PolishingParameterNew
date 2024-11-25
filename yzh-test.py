import matplotlib.pyplot as plt
import numpy as np

rows, cols = 10, 10  # 创建 10x10 的子图
fig, axes = plt.subplots(rows, cols, figsize=(20, 20))

for i in range(rows):
    for j in range(cols):
        axes[i, j].plot(np.random.rand(10))
        axes[i, j].set_title(f"Subplot ({i+1},{j+1})", fontsize=6)

plt.tight_layout()
plt.show()

