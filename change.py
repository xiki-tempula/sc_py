# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 11:48:18 2016

@author: zhiyiwu
"""
from info import Cluster,Patch
from dcpyps import dataset
from PlotAnalysis import PlotSingle
from batch_analysis import BatchAnalysis
from myreport import html_report

import numpy as np
minPopen = 0
maxPopen = 1.1
def rule(cluster, minPopen, maxPopen): 
    if (cluster.popen < minPopen) or (cluster.popen > maxPopen): 
        return False
    else:
        return True

def change(name, tres, tcrit, minPopen = 0, maxPopen = 1.1):
    new_patch = Patch('./set/{}.SCN'.format(name))
    new_patch.read_scn(tres=tres, tcrit=tcrit)
    new_patch.filter_cluster(rule, minPopen, maxPopen)
    new_patch.write_scn()

change('F', 30, 100, maxPopen = 0.6)
change('I', 30, 100, maxPopen = 0.08)
change('L', 20, 70, minPopen = 0.1)

change('H', 20, 300, maxPopen = 0.025)
change('K', 30, 70, minPopen = 0.075, maxPopen = 0.25)
change('M', 25, 70, minPopen = 0.15)

change('G', 20, 300, maxPopen = 0.02)
change('J', 20, 70, maxPopen = 0.035)
change('N', 25, 70, minPopen = 0.06)

