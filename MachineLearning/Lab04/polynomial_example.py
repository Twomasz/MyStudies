import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


path = os.getcwd() + '/ex2data1.txt'
data = pd.read_csv(path, header=None, names=['Exam 1', 'Exam 2', 'Admitted'])

X = data.values[:, :2].T
y = data.values[:, 2:].T

for i in range(X.shape[0]):
    X[i, :] = (X[i, :] - np.mean(X[i, :])) / (np.std(X[i, :]))

it = 100000
alpha = 0.01
no_of_degree = 3
assert no_of_degree > 0


for i in range(2, no_of_degree + 1):
    X = np.concatenate([X, X[0:1, :]**i])
X = np.concatenate([np.ones([1, X.shape[1]]), X])

theta = np.zeros((X.shape[0], 1))


def sig(t):
    return 1.0 / (1.0 + np.exp(-t))


def computeCost(X, y, theta, eps=10e-5):
    h = sig(theta.T @ X)
    y_1 = -y*np.log(h+eps)
    y_0 = (1-y)*np.log(1-h+eps)
    J = (y_1 - y_0).sum() / y.shape[1]
    return J


print(f'cost = {computeCost(X, y, theta)}')


def simple_gradient(X, y, theta, alpha, it):
    cost = []
    for i in range(it):
        h = sig(theta.T @ X)
        h_y = h - y
        h_yxX = h_y @ X.T
        theta = theta - alpha * h_yxX.T / X.shape[1]

        cost += [computeCost(X, y, theta)]

    return theta, cost


theta, cost = simple_gradient(X, y, theta, alpha, it)

print(f'cost after optimization: {cost[-1]}')
print(f'theta: {theta}')

# accuracy
preds = np.round(sig(theta.T @ X))
correct = (preds == y).astype(int).sum()
acc = correct / X.shape[1]
print(f'accuracy = {acc}')

# plot
fig, (ax1, ax2) = plt.subplots(1, 2)
# cost
ax1.plot(cost)

# decision boundary
step = 0.02
x1 = np.arange(X[1, :].min(), X[1, :].max()+step, step)
x2 = -theta[0, 0]/theta[2, 0] - (theta[1, 0]/theta[2, 0]*x1)
for i in range(2, no_of_degree + 1):
    x2 += -(theta[i+1, 0]/theta[2, 0]*x1**i)
ax2.plot(x1, x2)
X1_1 = X[1, y[0, :] == 1.0]
X2_1 = X[2, y[0, :] == 1.0]
X1_0 = X[1, y[0, :] == 0.0]
X2_0 = X[2, y[0, :] == 0.0]
ax2.plot(X1_1, X2_1, 'o')
ax2.plot(X1_0, X2_0, 'x')
ax2.axis(xmin=X[1, :].min()-step, xmax=X[1, :].max()+2*step)
ax2.axis(ymin=X[2, :].min()-step, ymax=X[2, :].max()+2*step)
plt.show()
pass
