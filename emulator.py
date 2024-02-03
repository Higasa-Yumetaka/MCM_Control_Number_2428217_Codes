import Submersible_motion_model
from tqdm import tqdm
import csv

epochs = 20000

position_history = []
for epoch in tqdm(range(epochs)):
    position = Submersible_motion_model.emulate()
    position_history.append(position)

# 导出到csv文件
with open('position_history.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(position_history)
