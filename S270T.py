# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:11:05 2015

@author: zhiyiwu
"""

import os
import codecs

import matplotlib.pyplot as plt
import numpy as np

from batch_query import Batch
from batch_analysis import BatchAnalysis



batch = Batch('/Volumes/c-floor/William/data/')
batch.scan_orded_folder()
concentation_list = ['0.3', '1', '3', '10', '100']
total = ''
for concentration in concentation_list:
    cluster_list = batch.query(mutation = 'S270T', concentration = concentration)
    if cluster_list:
        cluster_summary = BatchAnalysis(cluster_list)
        result = cluster_summary.compute_cluster_summary()
        
        popen_hist = plt.figure()
        ax = popen_hist.add_subplot(111)
        ax.hist(result['popen'], bins = np.arange(0,1.05,0.05), color = 'blue')
        ax.set_title('Popen distribution ({}mM glycine)'.format(concentration))
        popen_hist.savefig(os.path.join('/Volumes/c-floor/William/data','{}_Popen.png'.format(concentration)),dpi=300)
        plt.close(popen_hist)
        string = cluster_summary.get_summary(output = 'string')
        string = '{}mM: \n'.format(concentration) + string
        total += string + '\n'
        print(string)

file = codecs.open('/Volumes/c-floor/William/data/summary.txt', 'w', "utf-8")
file.write(total)
file.close()