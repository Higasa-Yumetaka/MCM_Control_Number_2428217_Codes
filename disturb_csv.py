import csv
import numpy

fileName = './source/position_history/单潜水器-2万点.csv'

with open(fileName, 'r') as csvfile:
    reader = csv.reader(csvfile)
    position_history = list(reader)
    position_history = numpy.array(position_history).astype(float)

# 对其中的每一条数据，有10%的概率进行如下变换：
# 将数据变为0;数据扩大10倍;数据缩小10倍;数据加上100;数据减去100
p = 0.2  # 概率

for i in range(len(position_history)):
    if numpy.random.random() < p:
        position_history[i] = 0
    elif numpy.random.random() < p:
        position_history[i] *= 10
    elif numpy.random.random() < p:
        position_history[i] /= 10
    elif numpy.random.random() < p:
        position_history[i] += 100
    elif numpy.random.random() < p:
        position_history[i] -= 100

# 将数据写入新的csv文件
with open('./source/position_history/disturb_单潜水器-2万点.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(position_history)

