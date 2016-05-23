# -*- coding: utf-8 -*-
"""
Created on Fri May 20 11:26:23 2016

@author: zhiyiwu
"""

from info import Patch

import matplotlib.pyplot as plt


name_list = [
'15073106',
'15073109',
'15073111',
'15073100',
'15073002',
'15073112'
]
tres = [
25,
25,
20,
25,
25,
25
]
tcrit = [
100,
100,
70,
70,
70,
70

]

for index, name in enumerate(name_list):
    patch = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/10/{}.SCN'.format(name))
    patch.read_scn(tres=tres[index], tcrit=tcrit[index])
    plt.plot(patch.mean_open, patch.mean_shut,'o', alpha=0.5, label = name)



plt.legend()

maxopen = 0.46
maxshut = float('inf')
def rule(cluster, maxopen, maxshut): 
    if (cluster.mean_open > maxopen) or (cluster.mean_shut > maxshut): 
        return False
    else:
        return True

index = [0,3,4,5]
for i in index:
    patch = Patch('/Users/zhiyiwu/Documents/pharmfit/raw trace/10/{}.SCN'.format(name_list[i]))
    patch.read_scn(tres=tres[i], tcrit=tcrit[i])
    patch.filter_cluster(rule, maxopen, maxshut)
    patch.write_scn()


