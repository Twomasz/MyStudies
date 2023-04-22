import numpy as np
import pickle
import matplotlib
import matplotlib.pyplot as plt
import string
import random


def compare_plot(x1: np.ndarray, y1: np.ndarray, x2: np.ndarray, y2: np.ndarray, xlabel: str, ylabel: str,
                 title: str, label1: str, label2: str):
    if x1.shape != y1.shape or min(x1.shape) == 0 or x2.shape != y2.shape or min(x2.shape) == 0:
        return None

    fig, ax = plt.subplots()
    ax.plot(x1, y1, 'b', label=label1, linewidth=4)
    ax.plot(x2, y2, 'r', label=label2, linewidth=2)
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    plt.legend()
    return fig


def parallel_plot(x1: np.ndarray, y1: np.ndarray, x2: np.ndarray, y2: np.ndarray,
                  x1label: str, y1label: str, x2label: str, y2label: str, title: str, orientation: str):

    if x1.shape != y1.shape or min(x1.shape) == 0 or x2.shape != y2.shape or min(x2.shape) == 0:
        return None

    if orientation == 'h':
        n = 2
        m = 1
    elif orientation == 'v':
        n = 1
        m = 2
    else:
        return None

    fig = plt.figure()
    fig.suptitle(t=title)
    plt.subplot(n, m, 1)
    plt.plot(x1, y1, 'b')
    plt.xlabel(xlabel=x1label)
    plt.ylabel(ylabel=y1label)

    plt.subplot(n, m, 2)
    plt.plot(x2, y2, 'r')
    plt.xlabel(xlabel=x2label)
    plt.ylabel(ylabel=y2label)

    return fig


def log_plot(x: np.ndarray, y: np.ndarray, xlabel: str, ylabel: str, title: str, log_axis: str):

    if x.shape != y.shape or min(x.shape) == 0:
        return None

    fig = plt.figure()
    plt.plot(x, y, 'g')
    plt.xlabel(xlabel=xlabel)
    plt.ylabel(ylabel=ylabel)
    plt.title(label=title)
    if log_axis == 'x':
        plt.semilogx()
    elif log_axis == 'y':
        plt.semilogy()
    elif log_axis == 'xy':
        plt.loglog()
    else:
        return None
    return fig
