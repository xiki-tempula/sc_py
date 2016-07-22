# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 09:32:25 2016

@author: zhiyiwu
"""


import numpy as np
import matplotlib.pyplot as plt

from info import Patch
from binary_search import BFS

patch = Patch('/Users/zhiyiwu/Documents/pharmfit/12061415.csv')
patch.scan()
cluster = patch[1]
opening = cluster.open_period
log_opening = np.log10(opening)
plt.hist(log_opening)
sep_open = sorted(BFS(log_opening[:, np.newaxis]))
print(sep_open)

shutting = cluster.shut_period
plt.hist(np.log10(shutting))
log_shutting = np.log10(shutting)
plt.hist(log_shutting)
sep_shut = sorted(BFS(log_shutting[:, np.newaxis]))
print(sep_shut)

period = cluster.period

fig = plt.fig()
for i in range(10):
    ax = fig.add_subplot(10,1,i+1)
    plt