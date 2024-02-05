"""
Distance-submersible distribution model
Replaced by kernel density estimation model
"""
import numpy as np
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt
import csv

with open('Monte_Carlo_simulation.csv.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    position_history = list(reader)
    position_history = np.array(position_history).astype(float)

# Extract the first two columns of the data (2D data)
position_history = position_history[:, 0:2]

# Calculate the centroid (mean) of the positions
centroid = np.mean(position_history, axis=0)
print(centroid)

# Calculate distances of each point to the centroid
distances = np.linalg.norm(position_history - centroid, axis=1)

# Calculate mean and standard deviation of distances
dist_mean = np.mean(distances)
dist_std = np.std(distances)

# Build a distance model using a multivariate normal distribution
dist_model = multivariate_normal(mean=dist_mean, cov=dist_std)

# Plot scatter plot of positions and centroid
plt.scatter(position_history[:, 0], position_history[:, 1], s=1)
plt.scatter(centroid[0], centroid[1], c='r')
plt.show()

# Plot the distance model
x = np.linspace(0, 100, 1000)
plt.plot(x, dist_model.pdf(x))
plt.show()

# completed
