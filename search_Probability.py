import csv
import numpy as np
from scipy.spatial.distance import cdist


def read_csv(file_path):
    points = []
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            x, y = map(float, row[:2])
            points.append((x, y))
    return points


list = []


def density_analysis(points, R):
    max_len = len(points)
    while len(points) > 0:
        print("Points {}, {} left".format(len(points), max_len))
        # 计算每个点到所有其他点的距离矩阵
        distances = cdist(points, points)

        # 计算每个点在半径为R内的其他点的数量
        densities = np.sum(distances < R, axis=1)

        # 找到密度最高的点
        max_density_index = np.argmax(densities)
        max_density_point = points[max_density_index]
        max_density_value = densities[max_density_index]

        # 输出当前最高密度点的信息
        # print(f"Point: {max_density_point}, Density: {max_density_value / len(points)}")
        list.append(max_density_value / len(points))
        # print(list)

        # 在点集中删除半径为R内的所有点
        points = [point for i, point in enumerate(points) if distances[max_density_index, i] >= R]
    # 将list数据转换为numpy数组
    arr = np.array(list)
    # 将list中的数据csv文件，写入列
    np.savetxt("density.csv", arr, delimiter=',')
    # print(arr)


file_path = './source/position_history.csv'
data = read_csv(file_path)
R = 50
density_analysis(data, R)
