import numpy as np


def is_positive_reciprocal_matrix(A):
    """
    Determine whether the matrix A is a direct and inverse matrix
    :param A: importance relationship matrix
    :return: True or False
    """
    n = len(A)
    for i in range(n):
        for j in range(n):
            a = A[i, j]
            b = A[j, i]
            if a * b != 1:
                return False
    return True


def arithmetic_mean_method(A):
    print("Rrithmetic mean=========================================================================================")
    print(A)
    if is_positive_reciprocal_matrix(A):
        n = A.shape[0]
        sumA = np.sum(A, axis=0)
        sumA2 = np.tile(sumA, (n, 1))
        standardA = A / sumA2
        sumStandardA = np.sum(standardA, axis=1) / A.shape[1]
        print("The weight vector is:")
        print(sumStandardA)
    else:
        print("Matrix A is not a direct and inverse matrix! ! ! Please modify the matrix and run again! ! !")


def geometric_mean_method(A):
    print("Geometric mean=======================================================================================")
    print(A)
    if is_positive_reciprocal_matrix(A):
        prodA = np.prod(A, axis=1)
        n = A.shape[0]
        prodA_n = np.power(prodA, 1 / n)
        prodA_n_e = prodA_n / np.sum(prodA_n, axis=0)
        print("The weight vector is:")
        print(prodA_n_e)
    else:
        print("Matrix A is not a direct and inverse matrix! ! ! Please modify the matrix and run again! ! !")


def eigenvalue_method(A):
    print("Eigenvalue==========================================================================================")
    print(A)
    if is_positive_reciprocal_matrix(A):
        maxValue = max(np.linalg.eig(A)[0])
        _, V = np.linalg.eig(A)
        D = np.where(np.linalg.eig(A)[0] == maxValue, 1, 0)
        print(np.nonzero(D))
        r, c = np.nonzero(D)
        ans = V[:, c]
        result = ans / np.sum(ans, axis=0)
        print("The weight vector is:")
        print(result)
    else:
        print("Matrix A is not a direct and inverse matrix! ! ! Please modify the matrix and run again! ! !")


def consistency_ratio_method(A):
    print("Consistency check=====================================================================================")
    print("The importance relationship matrix is:")
    print(A)
    print("The result of judging its consistency is:")
    maxValue = max(np.linalg.eig(A)[0])
    n = A.shape[0]
    CI = (maxValue - n) / (n - 1)
    RI = [0, 0, 0.52, 0.89, 1.12, 1.26, 1.36, 1.41, 1.46, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59]
    CR = CI / RI[n]
    if CR < 0.1:
        print("CR={:.2f}<0.1,The consistency of this judgment matrix A is acceptable!".format(CR))
    else:
        print("CR={:.2f}>=0.1,The consistency of this judgment matrix A is unacceptable!".format(CR))


# importance relationship matrix
A = np.array([[1, 2, 5], [1 / 2, 1, 2], [1 / 5, 1 / 2, 1]])

arithmetic_mean_method(A)
geometric_mean_method(A)
eigenvalue_method(A)
consistency_ratio_method(A)
