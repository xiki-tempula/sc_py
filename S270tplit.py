# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 15:18:53 2015

@author: zhiyiwu
"""
from info import Cluster
from dcpyps import dataset
from PlotAnalysis import PlotSingle
scnfiles = ['/Volumes/c-floor/William/S270T/0.1/15071503.SCN']
rec = dataset.SCRecord(scnfiles, 0.1, 25e-6)
cluster = Cluster()
cluster.load_SCRecord(rec)
cluster.compute_mode()
cluster.compute_mode_detail(True)
c = PlotSingle('/Users/zhiyiwu/GitHub/sc_py/temp/')
c.load_cluster(cluster)
c.plot_multitrace()