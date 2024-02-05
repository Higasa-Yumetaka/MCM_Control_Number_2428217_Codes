import numpy as np
from scipy.stats import multivariate_normal, gaussian_kde
import matplotlib.pyplot as plt
import csv

from kde import get_max_density_coordinates

with open('./position_history.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    position_history = list(reader)
    position_history = np.array(position_history).astype(float)

position_history = position_history[:][:, 0:2]  # 取二维数据

centroid = np.mean(position_history, axis=0)  # 计算其质心
print(centroid)

max_density_coordinates = get_max_density_coordinates()
print(max_density_coordinates)

distances = np.linalg.norm(position_history - centroid, axis=1)  # 计算每个点到质心的距离

dist_mean = np.mean(distances)  # 计算平均距离
dist_std = np.std(distances)  # 计算标准差
dist_model = multivariate_normal(mean=dist_mean, cov=dist_std)  # 构建距离模型

plt.scatter(position_history[:, 0], position_history[:, 1], s=1)  # 绘制散点图
plt.scatter(centroid[0], centroid[1], c='r')  # 绘制质心
plt.show()

x = np.linspace(0, 100, 1000)
plt.plot(x, dist_model.pdf(x))  # 绘制距离模型
plt.show()

kde = gaussian_kde(position_history.T)  # 计算核密度估计

# 生成坐标网格
x, y = np.mgrid[-100:100:5, -100:100:5]
positions = np.vstack([x.ravel(), y.ravel()])

# 计算在每个坐标点上的核密度估计值
z = np.reshape(kde(positions).T, x.shape)
