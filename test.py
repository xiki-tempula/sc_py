# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 14:05:36 2016

@author: zhiyiwu
"""

from info import Cluster,Patch
from dcpyps import dataset
from PlotAnalysis import PlotSingle
from batch_analysis import BatchAnalysis
from myreport import html_report

import numpy as np

data = [
['B',	100,	30,	0.1],
['F',	1000,	30,	100],
['I',	3000,	20,	100],
['L',	10000,	25,	70],
['C',	300,	25,	0.12],
['H',	1000,	20,	300],
['K',	3000,	30,	30],
['M',	10000,	25,	70],
['D',	300,	30,	0.1],
['G',	1000,	20,	300],
['J',	3000,	20,	100],
['N',	10000,	25,	100]]
myreport=html_report("scn.html")
for patch in data:
    new_patch = Patch('./set/{}.SCN'.format(patch[0]))
    myreport.add_heading("Scan file {}, concentration: {}, res: {}, tcrit = {}".format(*patch))
    new_patch.read_scn(tres=patch[2], tcrit=patch[3])
    cluster_list = BatchAnalysis(new_patch.get_cluster_list())
    summary = cluster_list.compute_cluster_summary()
    myreport.add_subheading ("Popen distrubition")
    myreport.add_text("Mean: {}, std: {}".format(np.mean(summary['popen']), np.std(summary['popen'])))
    fig1 = myreport.init_figure()
    ax=fig1.add_subplot(1,1,1)
    ax.hist(summary['popen'])
    myreport.add_figure(fig1)
    myreport.add_subheading ("Popen duration correlation")
    fig1 = myreport.init_figure()
    ax=fig1.add_subplot(1,1,1)
    ax.plot(summary['duration'],summary['popen'],'o')
    myreport.add_figure(fig1)

myreport.write()
myreport.view()
    