# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 16:14:24 2015

@author: zhiyiwu
"""

from BatchQuery import Batch
from PlotAnalysis import PlotAnalysis
a = Batch(['/Users/zhiyiwu/GitHub/sc_py/HeteroData/'])
cluster_list = a.scan_folder()
for cluster in cluster_list:
    cluster.compute_mode()
    cluster.compute_mode_detail(True)
    c = PlotAnalysis()
    c.load_cluster(cluster)
    c.plot_original()
    c.plot_popen_on_original()
    c.plot_open_close()
    c.plot_cost_difference()
    

