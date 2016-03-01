# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:30:14 2016

@author: zhiyiwu
"""

import numpy as np
import matplotlib.pyplot as plt

wt = np.loadtxt('/Users/zhiyiwu/Downloads/a1WT.dat', skiprows = 3)
wt = wt.T

s270t = np.loadtxt('/Users/zhiyiwu/Downloads/a1S270T.dat', skiprows = 3)
s270t = s270t.T

fig = plt.figure(figsize=(10.78/776*328,6.12),dpi=300)
ax = fig.add_subplot(111)
ax.plot(wt[0,],wt[1,], label = 'wt')
ax.plot(s270t[0,],s270t[1,], label = 'S270T')
ax.plot([30,40],[-0.8,-0.8],linewidth=4, color = 'black')
ax.plot([9,11],[0.05,0.05],linewidth=2, color = 'red')
ax.annotate('10 ms', xy=(30, -0.88), size=15)
ax.legend(bbox_to_anchor = (0.8,0.5),bbox_transform=plt.gcf().transFigure)
ax.axis('off')
fig.savefig('/Users/zhiyiwu/Desktop/fig_jump.png', dpi = 500)

