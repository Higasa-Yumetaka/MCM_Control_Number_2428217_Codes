import numpy as np
from SALib.analyze import sobol
from SALib.sample import saltelli
from SALib.plotting.bar import plot as barplot
from matplotlib import pyplot as plt
from tqdm import tqdm

from Submersible_motion_model import sensitivity

parameters = {
    'num_vars': 8,
    'names': ['speed_oc', 'temperature', 'salinity', 'pressure', 'latitude', 'sub_mass', 'sub_volume', 'water_onboard'],
    'bounds': [(0.0, 10.0),
               (0.0, 10.0),
               (37.0, 39.0),
               (9.7, 10.5),
               (36.0, 40.0),
               (21000.0, 23000.0),
               (20.0, 23.0),
               (2250.0, 3000.0)]
}

param_values = saltelli.sample(parameters, 1024)

# 运行模拟并获取输出
output_values = np.zeros([param_values.shape[0]])

for i in tqdm(range(param_values.shape[0])):
    output_values[i] = sensitivity(*param_values[i, :])

# 进行敏感度分析
sensitivity_results = sobol.analyze(parameters, output_values)

# 输出敏感度结果
print(sensitivity_results)

sf = sensitivity_results.to_df()
barplot(sf[0])
plt.ylabel('Sensitivity index')
plt.savefig('sensitivity_analysis.svg')
plt.show()


barplot(sf[1])
plt.ylabel('Total-order index')
plt.savefig('total_order_analysis.svg')
plt.show()

barplot(sf[2])
plt.ylabel('First-order index')
plt.savefig('first_order_analysis.svg')
plt.show()
