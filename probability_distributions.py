import numpy as np
from scipy.stats import multivariate_normal, gaussian_kde
import matplotlib.pyplot as plt
import csv

with open('./position_history.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    position_history = list(reader)
    position_history = np.array(position_history).astype(float)

position_history = position_history[:][:, 0:2]  # 取二维数据

centroid = np.mean(position_history, axis=0)  # 计算其质心

# kde = gaussian_kde(position_history.T)
#
# x, y = np.mgrid[-300:300:5, -300:300:5]
# position_history = np.vstack([x.ravel(), y.ravel()])
#
# # 计算在每个坐标点上的核密度估计值
# z = np.reshape(kde(position_history).T, x.shape)
#
# # 寻找密度最大的点
# max_density_point = np.unravel_index(np.argmax(z), z.shape)
# max_density_coordinates = (x[max_density_point], y[max_density_point])
# max_density_value = z[max_density_point]
#
# print(max_density_coordinates, max_density_value)

distances = np.linalg.norm(position_history - centroid, axis=1)  # 计算每个点到质心的距离

dist_mean = np.mean(distances)  # 计算平均距离
dist_std = np.std(distances)  # 计算标准差
dist_model = multivariate_normal(mean=dist_mean, cov=dist_std)  # 构建距离模型

plt.scatter(position_history[:, 0], position_history[:, 1], s=1)  # 绘制散点图
plt.scatter(centroid[0], centroid[1], c='r')  # 绘制质心
plt.show()

x = np.linspace(0, 100, 100)
plt.plot(x, dist_model.pdf(x))  # 绘制距离模型
plt.show()
