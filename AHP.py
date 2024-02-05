"""
For a given importance relationship matrix,
use the analytic hierarchy process to calculate its weight vector
"""

import numpy as np

# Build comparison matrix
matrix = np.array([[1, 1/5, 1/3],
                   [5, 1, 2],
                   [3, 1/2, 1]])

# Normalized comparison matrix
n = matrix.shape[0]

# Calculate the weight of each criterion
eig_val, eig_vec = np.linalg.eig(matrix)
max_eig_val = max(eig_val)
max_eig_vec = eig_vec[:, list(eig_val).index(max_eig_val)]
weights = max_eig_vec / sum(max_eig_vec)

# Output results
for i in range(n):
    print("The weight of dimension {} 's weight: {}".format(i+1, round(weights[i].real, 3)))

# calculate consistency ratio
eigenvalues, eigenvectors = np.linalg.eig(matrix)
max_eigenvalue = max(eigenvalues)
n = len(matrix)
ci = (max_eigenvalue - n) / (n - 1)
RI = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
cr = ci.real / RI[n - 1]

if cr < 0.1:
    print("Consistency check passed, CR =", round(cr, 2))
else:
    print("Consistency check failed, CR =", round(cr, 2))
