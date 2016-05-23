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


patch_F = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/1/15071710.SCN')
patch_F.read_scn(tres=30, tcrit=100)
plt.plot(patch_F.mean_open, patch_F.mean_shut,'o', alpha=0.5, label = 'F')

patch_G = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/1/15080500.SCN')
patch_G.read_scn(tres=20, tcrit=300)
plt.plot(patch_G.mean_open, patch_G.mean_shut,'o', alpha=0.5, label = 'G')

patch_H = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/1/15080705.SCN')
patch_H.read_scn(tres=20, tcrit=300)
plt.plot(patch_H.mean_open, patch_H.mean_shut,'o', alpha=0.5, label = 'H')

plt.legend()