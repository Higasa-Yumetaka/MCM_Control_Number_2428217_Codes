"""
Use the best search method to simulate the search time and the probability relationship searched
"""
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
        # Calculate the distance matrix from each point to all other points
        distances = cdist(points, points)

        # Count the number of other points within radius R for each point
        densities = np.sum(distances < R, axis=1)

        # Find the point with the highest density
        max_density_index = np.argmax(densities)
        max_density_point = points[max_density_index]
        max_density_value = densities[max_density_index]

        # Output the information of the current highest density point
        # print(f"Point: {max_density_point}, Density: {max_density_value / len(points)}")
        list.append(max_density_value / len(points))
        # print(list)

        # Delete all points within radius R from the point set
        points = [point for i, point in enumerate(points) if distances[max_density_index, i] >= R]
    arr = np.array(list)

    np.savetxt("density.csv", arr, delimiter=',')


file_path = 'Monte_Carlo_simulation.csv'
data = read_csv(file_path)
R = 50
density_analysis(data, R)

# completed
