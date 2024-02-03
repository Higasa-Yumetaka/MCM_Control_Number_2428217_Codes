import pandas
import numpy as np

import csv

with open('position_history.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    position_history = list(reader)
    position_history = np.array(position_history).astype(float)

print(position_history)
