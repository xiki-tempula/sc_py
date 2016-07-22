# -*- coding: utf-8 -*-
"""
Created on Fri May 20 11:26:23 2016

@author: zhiyiwu
"""

from info import Patch

import matplotlib.pyplot as plt


name_list = [
'06111411',
'15060420',
'15072908'
]
tres = [
20,
20,
20
]
tcrit = [
70,
70,
70

]


maxopen = 1
maxshut = float('inf')
def rule(cluster, maxopen, maxshut): 
    if (cluster.mean_open > maxopen) or (cluster.mean_shut > maxshut): 
        return False
    else:
        return True

for index, name in enumerate(name_list):
    patch = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/100/{}.SCN'.format(name))
    patch.read_scn(tres=tres[index], tcrit=tcrit[index])
    patch.filter_cluster(rule, maxopen, maxshut)
    patch.write_scn()







