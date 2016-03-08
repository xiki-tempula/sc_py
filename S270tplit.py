# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 15:18:53 2015

@author: zhiyiwu
"""
from info import Cluster,Patch
from dcpyps import dataset
from PlotAnalysis import PlotSingle
from batch_analysis import BatchAnalysis

<<<<<<< HEAD
scnfiles1 = '/Users/xiki_tempula/Google Drive/scn/L.SCN'
rec1 = Patch(scnfiles1)
rec1.read_scn(tres=25e-3, tcrit=600)

scnfiles2 = '/Users/xiki_tempula/Google Drive/scn/E.SCN'
rec2 = Patch(scnfiles1)
rec2.read_scn(tres=30e-3, tcrit=65)
c_list = []
c_list.extend(rec1.get_cluster_list())
c_list.extend(rec2.get_cluster_list())
cluster_list = BatchAnalysis(c_list)
=======
scnfiles = '/Users/zhiyiwu/Google Drive/scn/G.SCN'
rec = Patch(scnfiles)
rec.read_scn(tres=15e-3, tcrit=600)
cluster_list = BatchAnalysis(rec.get_cluster_list())
>>>>>>> origin/master
cluster_list.hierarchical_clustering(data = 'open_shut')
cluster_list[0].show_origianl()

