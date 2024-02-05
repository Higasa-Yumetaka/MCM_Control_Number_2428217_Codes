import numpy as np


def is_positive_reciprocal_matrix(A):
    n = len(A)
    for i in range(n):
        for j in range(n):
            a = A[i, j]
            b = A[j, i]
            if a * b != 1:
                return False
    return True


def arithmetic_mean_method(A):
    print("算术平均法=========================================================================================")
    print("判断矩阵A为:")
    print(A)
    if is_positive_reciprocal_matrix(A):
        print("A是正互反矩阵!!!")
        n = A.shape[0]
        sumA = np.sum(A, axis=0)
        sumA2 = np.tile(sumA, (n, 1))
        standardA = A / sumA2
        sumStandardA = np.sum(standardA, axis=1) / A.shape[1]
        print("算术平均法求得的权重向量为:")
        print(sumStandardA)
    else:
        print("A不是正互反矩阵！！！请重新运行！！！")


def geometric_mean_method(A):
    print("几何平均法=======================================================================================")
    print("判断矩阵A为:")
    print(A)
    if is_positive_reciprocal_matrix(A):
        print("A是正互反矩阵!!!")
        prodA = np.prod(A, axis=1)
        n = A.shape[0]
        prodA_n = np.power(prodA, 1 / n)
        prodA_n_e = prodA_n / np.sum(prodA_n, axis=0)
        print("几何平均法求得的权重向量为:")
        print(prodA_n_e)
    else:
        print("A不是正互反矩阵！！！请重新运行！！！")


def eigenvalue_method(A):
    print("特征值法==========================================================================================")
    print("判断矩阵A为:")
    print(A)
    if is_positive_reciprocal_matrix(A):
        print("A是正互反矩阵!!!")
        maxValue = max(np.linalg.eig(A)[0])
        _, V = np.linalg.eig(A)
        D = np.where(np.linalg.eig(A)[0] == maxValue, 1, 0)
        print(np.nonzero(D))
        r, c = np.nonzero(D)
        ans = V[:, c]
        result = ans / np.sum(ans, axis=0)
        print("特征值法求得的权重向量为:")
        print(result)
    else:
        print("A不是正互反矩阵！！！请重新运行！！！")


def consistency_ratio_method(A):
    print("一致性比例法=====================================================================================")
    print("判断矩阵A为:")
    print(A)
    print("判断一致性结果为：")
    maxValue = max(np.linalg.eig(A)[0])
    n = A.shape[0]
    CI = (maxValue - n) / (n - 1)
    RI = [0, 0, 0.52, 0.89, 1.12, 1.26, 1.36, 1.41, 1.46, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59]
    CR = CI / RI[n]
    if CR < 0.1:
        print("CR={:.2f}<0.1,所以,该判断矩阵A的一致性可以接受！！！".format(CR))
    else:
        print("CR={:.2f}>=0.1,所以,该判断矩阵A的一致性不能接受！！！".format(CR))


# 主程序
A = np.array([[1, 2, 5], [1 / 2, 1, 2], [1 / 5, 1 / 2, 1]])

arithmetic_mean_method(A)
geometric_mean_method(A)
eigenvalue_method(A)
consistency_ratio_method(A)
