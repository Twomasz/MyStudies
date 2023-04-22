import numpy as np


m = 10  # number of examples
n = 2  # number of features

X = np.ones((n+1, m))  # X.shape == [n+1, m]
y = np.zeros((1, m))  # y.shape == [1, m]
theta = np.zeros((n+1, 1))  # theta.shape == [n+1, m]


def computeCost(X, y, theta):
    h = theta.T @ X
    J = ((h - y)**2).sum() / (2*X.shape[1])
    return J


print(f'cost = {computeCost(X, y, theta)}')


def simple_gradient(X, y, theta, alpha, it):
    cost = []
    for i in range(it):
        h = theta.T @ X
        h_y = h - y
        h_yxX = h_y @ X.T
        theta = theta - alpha * h_yxX.T / X.shape[1]

        cost += [computeCost(X, y, theta)]

    return theta, cost


theta, cost = simple_gradient(X, y, theta, 0.01, 1000)

print(f'cost after optimization: {cost[-1]}')
print(f'theta: {theta}')
