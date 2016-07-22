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




patch_G = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/1/15080500.SCN')
patch_G.read_scn(tres=20, tcrit=300)


patch_H = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/1/15080705.SCN')
patch_H.read_scn(tres=20, tcrit=300)

patch_G.filter_cluster(rule, maxopen, maxshut)
patch_G.write_scn()
patch_H.filter_cluster(rule, maxopen, maxshut)
patch_H.write_scn()