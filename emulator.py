"""
潜水器运动模型仿真
运行本程序以生成epoch次数的潜水器运动的最终位置
"""
import numpy as np

import Submersible_motion_model
from tqdm import tqdm
import csv

# 仿真次数
epochs = 20000

# 可能的开始时的深度
depth_start = np.array([0.0, 4000.0])

# 可能的目标深度
target_depth_ = np.array([2000.0, 4000.0])

position_history = []
for epoch in tqdm(range(epochs)):

    position = Submersible_motion_model.emulate(np.random.uniform(depth_start[0], depth_start[1]), np.random.uniform(target_depth_[0], target_depth_[1]))
    position_history.append(position)

# 导出到csv文件
with open('position_history.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(position_history)
