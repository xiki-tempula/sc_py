# -*- coding: utf-8 -*-
"""
Created on Fri May 20 11:26:23 2016

@author: zhiyiwu
"""

from info import Patch

import matplotlib.pyplot as plt


name_list = [
'15080404',
'15072411',
'15080408'
]
tres = [
20,
30,
20
]
tcrit = [
100,
70,
100
]
popen =[]
for index, name in enumerate(name_list):
    patch = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/3/{}.SCN'.format(name))
    patch.read_scn(tres=tres[index], tcrit=tcrit[index])

maxopen = 1
maxshut = float('inf')
def rule(cluster, maxopen, maxshut): 
    if (cluster.mean_open > maxopen) or (cluster.mean_shut > maxshut): 
        return False
    else:
        return True


for i in range(3):
    patch = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/3/{}.SCN'.format(name_list[i]))
    patch.read_scn(tres=tres[i], tcrit=tcrit[i])
    patch.filter_cluster(rule, maxopen, maxshut)
    patch.write_scn()