"""
Display search options by plotting the search path.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from tqdm import tqdm


# Number of search and rescue vessels
number = 1  # number<R/(2*r)

t_sum = np.zeros(number)
n_min = 0

for n in tqdm(range(1, number + 1)):
    # search radius
    R = 500
    # sonar radius
    r = 10
    # Parameters that define the spiral
    a = 2 * r * n  # Coil spacing of spiral
    b = 10  # spiral radius growth rate
    # Define the extent of the spiral
    theta = np.linspace(0, (R - a) / b, 100000)
    distance = a + b * theta
    # Define arc length integral expression
    dr_dtheta = b  # Spiral derivative
    arc_length_expression = lambda theta: np.sqrt((a + b * theta) ** 2 + dr_dtheta ** 2)
    # Calculate arc length
    arc_length, _ = quad(arc_length_expression, 0, (R - a) / b)

    for i in range(1, n + 1):
        x = distance * np.cos(theta + 2 * i * np.pi / n)
        y = distance * np.sin(theta + 2 * i * np.pi / n)
        print(x, y)
        plt.plot(x, y)
    plt.show()
    plt.waitforbuttonpress(0)

    # Calculate scan time
    depth = np.linspace(3000, 50000, int(arc_length / (2 * a) + 1))  # Depth
    t_per = depth / 750. + 300  # The speed of sound propagates at every point
    v = 6
    t_sum[n - 1] = arc_length / v + np.sum(t_per)

N = np.arange(1, number + 1)
plt.plot(N, t_sum)
plt.savefig("search_plan.png")
plt.show()

# completed
