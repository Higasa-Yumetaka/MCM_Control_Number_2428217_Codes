import csv

import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt


with open('单潜水器.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    position_history = list(reader)
    position_history = np.array(position_history).astype(float)

position = position_history[:][:, 0:2]  # 取二维数据

# 分别寻找x和y的最大最小值
max_values = np.max(position, axis=0)
min_values = np.min(position, axis=0)
# print(max_values)
# print(min_values)

# print(position)

# 计算核密度估计
kde = gaussian_kde(position.T)

scale = 0.7

# 生成坐标网格
x, y = np.mgrid[0: 1000:1, 300: 1200:1]
positions = np.vstack([x.ravel(), y.ravel()])

# 计算在每个坐标点上的核密度估计值
z = np.reshape(kde(positions).T, x.shape)

# 寻找密度最大的点
max_density_point = np.unravel_index(np.argmax(z), z.shape)
max_density_coordinates = (x[max_density_point], y[max_density_point])
max_density_value = z[max_density_point]

print(max_density_point)


def get_max_density_coordinates():
    """
    使用核密度估计寻找最大密度点，即最可能的潜水器位置
    :return: 最大密度点的坐标
    """
    return max_density_coordinates


def main():
    # 绘制等高线图
    plt.contourf(x, y, z, cmap="viridis", levels=20)  # 调整levels以改变等高线数量
    plt.colorbar(label='Density')  # 添加颜色条

    # 绘制散点图
    # plt.scatter(position[:, 0], position[:, 1], s=5, color="white", alpha=0.5)

    # 绘制最大密度点
    plt.scatter(*max_density_coordinates, color="red", marker="o", label="Max Density Point")

    plt.legend()
    # plt.title('2D Kernel Density Estimation')
    fileName = '单潜水器.svg'
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.savefig(fileName)
    plt.show()


if __name__ == '__main__':
    main()
