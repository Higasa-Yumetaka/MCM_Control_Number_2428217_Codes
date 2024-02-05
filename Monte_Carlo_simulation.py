"""
Monte Carlo Simulation for Multiple Submersibles

Run this program to generate the final positions of submersible movements for a given number of epochs.

The simulation is run for each submersible specified by the epochs parameter.
The number of submersibles to be simulated is determined by the submersible_number parameter.
The minimum distance between submersibles is specified by the min_distance parameter.
"""
import numpy as np

import Submersible_motion_model
from tqdm import tqdm
import csv

# Number of simulations
epochs = 20000

# Number Of Submersibles
submersible_number = 1

# minimum Distance Between Each Submersible
min_distance = 200

# initialize A Random Location
start_position = np.array([0.0, 1000.0])

# possible Depth At The Beginning
depth_start = np.array([0.0, 2000.0])


# generate The Initial PositionRandomly
def random_start_position():
    """
    initialization Of Random Positions For Monte Carlo Simulation Of Submersible Simulation
    :return: A Randomly Generated Initial Position, Whose [0][1] Are The X And Y Coordinates Respectively,
    """
    return np.array([np.random.uniform(-start_position[0], start_position[1]),
                     np.random.uniform(-start_position[0], start_position[1]),
                     np.random.uniform(depth_start[0], depth_start[1])])


# specify A Target Depth For Descent
target_ = 5000.0
start_positions = []

position_history = []
for _ in range(submersible_number):
    print("Epoch: ", _ + 1, " of ", submersible_number)
    start_ = random_start_position()
    """
    the Initial Position Is Continuously Generated Randomly 
    Until The Distance Between All Submersibles Is Greater Than MinDistance
    """
    while len(start_positions) > 1 and np.min(np.linalg.norm(np.array(start_positions) - start_, axis=1)) < min_distance:
        start_ = random_start_position()
    print("start position: ", start_)
    start_positions.append(start_)
    for epoch in tqdm(range(epochs)):
        # with Submersible_motion_model.emulate() to simulateTheMovementOfTheSubmersible
        position = Submersible_motion_model.emulate(start_,
                                                    target_)
        position_history.append(position)
    print('\n')

# Save the final positions of all simulated submersibles to a csv file
with open('Monte_Carlo_simulation.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(position_history)
    print('emulator result csv file saved')

# completed
