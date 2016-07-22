# -*- coding: utf-8 -*-
"""
Created on Fri May 20 11:26:23 2016

@author: zhiyiwu
"""

from info import Cluster,Patch
from dcpyps import dataset
from PlotAnalysis import PlotSingle
from batch_analysis import BatchAnalysis
import matplotlib.pyplot as plt
import numpy as np


maxopen = 1
maxshut = float('inf')
def rule(cluster, maxopen, maxshut): 
    if (cluster.mean_open > maxopen) or (cluster.mean_shut > maxshut): 
        return False
    else:
        return True

fig = plt.figure()
patch_E = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/0.3/15071611.SCN')
patch_E.read_scn(tres=30, tcrit=100)


#plt.plot(patch_E.mean_open, patch_E.mean_shut,'o', label = '15071611')

patch_F = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/1/15071710.SCN')
patch_F.read_scn(tres=30, tcrit=100)
#plt.plot(patch_F.mean_open, patch_F.mean_shut,'o', alpha=0.5, label = '15071710')

patch_G = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/1/15080500.SCN')
patch_G.read_scn(tres=20, tcrit=300)
ax = fig.add_subplot(2,1,1)
#ax.hist(patch_G.transition_distribution, bins = range(100))
#ax.set_xlim([0,20])
ax.hist(patch_G.popen_distribution)
#plt.plot(patch_G.mean_open, patch_G.mean_shut,'o', alpha=0.5, label = '15080500')



patch_H = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/1/15080705.SCN')
patch_H.read_scn(tres=20, tcrit=300)
ax = fig.add_subplot(2,1,2)
#ax.hist(patch_H.transition_distribution, bins = range(100))
#ax.set_xlim([0,20])
ax.hist(patch_H.popen_distribution)
#plt.plot(patch_H.mean_open, patch_H.mean_shut,'o', alpha=0.5, label = '15080705')


plt.legend()

print(np.mean(patch_G.popen_distribution.extend(patch_H.popen_distribution)))

#patch_G.filter_cluster(rule, maxopen, maxshut)
#patch_G.write_scn()
#patch_H.filter_cluster(rule, maxopen, maxshut)
#patch_H.write_scn()