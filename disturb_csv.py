"""
Simulate the abnormal data generated through Monte Carlo simulation
when predicting program exceptions:
Input:Normal Monte Carlo simulation produces results csv file: Output:Abnormal data csv file
"""

import csv
import numpy

# To run this code, you need to have a csv file in the source folder
file_name_1 = './source/position_history/单潜水器-2万点.csv'

with open(file_name_1, 'r') as csvfile:
    reader = csv.reader(csvfile)
    position_history = list(reader)
    position_history = numpy.array(position_history).astype(float)

"""
For each piece of data, there is a 10% probability of performing the following transformation:Change the data to 0; 
expand the data 10 times;
reduce the data 10 times;
add 100 to the data; 
subtract 100 from the data"""
p = 0.1  # The probability of an exception occurring

for i in range(len(position_history)):
    if numpy.random.random() < p:
        position_history[i] = 0
    elif numpy.random.random() < p:
        position_history[i] *= 10
    elif numpy.random.random() < p:
        position_history[i] *= -10
    elif numpy.random.random() < p:
        position_history[i] += 100
    elif numpy.random.random() < p:
        position_history[i] -= 100

# Write exception data to new csv file
with open('./source/position_history/disturb_单潜水器-2万点.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(position_history)

