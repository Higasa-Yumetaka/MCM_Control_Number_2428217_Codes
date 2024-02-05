import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from tqdm import tqdm
import csv

with open('./position_history.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    position_history = list(reader)
    position_history = np.array(position_history).astype(float)


# 确定搜救船只数量，绘制轨迹图
number = 1  # number<R/(2*r)

t_sum = np.zeros(number)
n_min = 0

for n in tqdm(range(1, number + 1)):
    # 搜索半径
    R = 500
    # 确定声纳半径
    r = 0.1
    # 定义螺旋线的参数
    a = 2 * r * n  # 螺旋线的线圈间距参数
    b = 0.5  # 螺旋线半径增长率feedingRateLamprey
    # 定义螺旋线的范围
    theta = np.linspace(0, (R - a) / b, 100000)  # 满足半径200，100000个点
    distance = a + b * theta
    # 定义弧长积分表达式
    dr_dtheta = b  # 螺线导数
    arc_length_expression = lambda theta: np.sqrt((a + b * theta) ** 2 + dr_dtheta ** 2)
    # 计算弧长
    arc_length, _ = quad(arc_length_expression, 0, (R - a) / b)

    for i in range(1, n + 1):
        x = distance * np.cos(theta + 2 * i * np.pi / n)
        y = distance * np.sin(theta + 2 * i * np.pi / n)
        print(x, y)
        plt.plot(x, y)
    plt.show()
    plt.waitforbuttonpress(0)

    # 计算扫描时间
    depth = np.linspace(3000, 50000, int(arc_length / (2 * a) + 1))  # 深度!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    t_per = depth / 750. + 300  # 每个点声速传播
    v = 6
    t_sum[n - 1] = arc_length / v + np.sum(t_per)

N = np.arange(1, number + 1)
plt.plot(N, t_sum)
plt.show()
