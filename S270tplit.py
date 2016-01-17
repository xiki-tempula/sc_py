# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 15:18:53 2015

@author: zhiyiwu
"""
from info import Cluster,Patch
from dcpyps import dataset
from PlotAnalysis import PlotSingle
from batch_analysis import BatchAnalysis

scnfiles = '/Users/xiki_tempula/Google Drive/scn/G.SCN'
rec = Patch(scnfiles)
rec.read_scn(tres=15e-3, tcrit=600)
cluster_list = BatchAnalysis(rec.get_cluster_list())
cluster_list.hierarchical_clustering(data = 'popen')
cluster_list[0].show_origianl()

