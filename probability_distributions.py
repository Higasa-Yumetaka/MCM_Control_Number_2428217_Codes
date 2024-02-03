import csv

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from scipy.stats import multivariate_normal
from scipy.stats import norm

with open('position_history.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    position_history = list(reader)
    position_history = np.array(position_history).astype(float)

position = position_history[:][:, 0:2]  # 取二维数据

centroid = np.mean(position, axis=0)  # 计算其质心
cov = np.cov(position, rowvar=False)  # 计算其协方差矩阵

# distances = np.linalg.norm(position_history - centroid, axis=1)  # 计算每个点到质心的距离

kde = gaussian_kde(position.T)  # 构建核密度估计模型

plt.scatter(position[:, 0], position[:, 1], s=1)  # 绘制散点图
plt.scatter(centroid[0], centroid[1], c='r')  # 绘制质心
plt.show()

x = np.linspace(0, 200, 100)
plt.plot(x, kde(x))  # 绘制核密度估计模型
plt.show()
