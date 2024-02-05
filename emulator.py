"""
多潜水器的蒙特卡洛模拟仿真
运行本程序以生成epoch次数的潜水器运动的最终位置
由epochs指定每搜潜水器的仿真次数
由submersible_number指定仿真的潜水器数量
由min_distance指定潜水器之间的最小距离
"""
import numpy as np

import Submersible_motion_model
from tqdm import tqdm
import csv

# 仿真次数
epochs = 20000

# 潜水器的数量
submersible_number = 3

# 每个潜水器之间的最小距离
min_distance = 200

# 初始化随机位置
start_position = np.array([0.0, 1000.0])

# 可能的开始时的深度
depth_start = np.array([0.0, 2000.0])


# 随机生成初始位置
def random_start_position():
    """
    为潜水器仿真的蒙特卡洛模拟进行随机位置的初始化
    """
    # 返回一个随机生成的初始位置，其[0][1]分别为x和y坐标，由start_position指定范围内的随机数生成，[2]为深度，由depth_start指定范围内的随机数生成
    return np.array([np.random.uniform(-start_position[0], start_position[1]),
                     np.random.uniform(-start_position[0], start_position[1]),
                     np.random.uniform(depth_start[0], depth_start[1])])


# 指定下降的目标深度
target_ = 5000.0

position_history = []
for _ in range(submersible_number):
    print("Epoch: ", _ + 1, " of ", submersible_number)
    start_ = random_start_position()
    print("start position: ", start_)
    for epoch in tqdm(range(epochs)):
        # 由Submersible_motion_model.emulate()方法仿真潜水器的运动
        position = Submersible_motion_model.emulate(start_,
                                                    target_)
        position_history.append(position)
    print('\n')

# 将所有仿真的潜水器最终位置保存至csv文件中
with open('position_history.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(position_history)
    print('./position_history.csv saved')
