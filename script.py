# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 16:14:24 2015

@author: zhiyiwu
"""

from batch_query import Batch
from PlotAnalysis import PlotSingle

a = Batch(['/Users/zhiyiwu/GitHub/Single_channel/HeteroData/',])
cluster_list = a.scan_folder()


for cluster in cluster_list:
    cluster.compute_mode()
    cluster.compute_mode_detail(True)
    c = PlotSingle('/Users/zhiyiwu/GitHub/sc_py/temp/')
    c.load_cluster(cluster)
    c.plot_original()
    c.plot_popen_on_original()
    c.plot_open_close()
    c.plot_cost_difference()
    
    

