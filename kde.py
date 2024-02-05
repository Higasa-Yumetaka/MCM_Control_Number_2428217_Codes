"""Performs a 2D kernel density estimation (KDE) on the position history data of a single submersible obtained from a
CSV file.
It aims to find the point with the maximum density, representing the most probable location of the
submersible.
:Input: A CSV file containing the position data of monte carlo simulation; Output: A 2D kernel density
estimation plot with the maximum density point marked"""
import csv

import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt


with open('./source/position_history/disturb_单潜水器-2万点.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    position_history = list(reader)
    position_history = np.array(position_history).astype(float)

# delete the row that is all 0, because it is error data
position_history = position_history[~np.all(position_history == 0, axis=1)]
position = position_history[:][:, 0:2]  # 取二维数据

# Find the maximum and minimum values of x and y
max_values = np.max(position, axis=0)
min_values = np.min(position, axis=0)

# Compute Kernel Density Estimate
kde = gaussian_kde(position.T)
print("Have done kde")

scale = 0.7

# Generate coordinate grid
x, y = np.mgrid[-550:1260:1, -560: 1255:1]
positions = np.vstack([x.ravel(), y.ravel()])

# Calculate the kernel density estimate at each coordinate point
z = np.reshape(kde(positions).T, x.shape)

# Find the point with the highest density
max_density_point = np.unravel_index(np.argmax(z), z.shape)
max_density_coordinates = (x[max_density_point], y[max_density_point])

max_density_value = z[max_density_point]
print(max_density_coordinates)


def get_max_density_coordinates():
    """
    Use kernel density estimation to find the maximum density point, i.e., the most likely submersible location
    :return: The coordinates of the maximum density point
    """
    return max_density_coordinates


def main():
    # Draw a contour map
    plt.contourf(x, y, z, cmap="viridis", levels=20)
    plt.colorbar(label='Density')

    # Drawing a scatter plot
    # It will obscure the density plot
    # plt.scatter(position[:, 0], position[:, 1], s=5, color="white", alpha=0.5)

    # Plot maximum density point
    plt.scatter(*max_density_coordinates, color="red", marker="o", label="Max Density Point")

    plt.legend()
    fileName = 'd_KDE.svg'
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.savefig(fileName)
    plt.show()


if __name__ == '__main__':
    main()
