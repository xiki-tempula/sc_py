# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 09:21:42 2015

@author: zhiyiwu
"""
import os

import matplotlib.pyplot as plt
import numpy as np

from batch_query import Batch
from batch_analysis import BatchAnalysis

batch = Batch('/Users/zhiyiwu/GitHub/sc_py/data')
batch.scan_orded_folder()
list_100 = batch.query(mutation = 'wt', agonist = 'taurine', concentration = '100')
list_30 = batch.query(mutation = 'wt', agonist = 'taurine', concentration = '30')

combined_list = list_100 + list_30
for cluster in combined_list:
    cluster.compute_mode()
    cluster.compute_mode_detail(output = True)

batch_100 = BatchAnalysis(list_100)
cluster_100 = batch_100.compute_cluster_summary()
stretch_100 = batch_100.compute_stretch_summary()

popen_100 = plt.figure()
ax = popen_100.add_subplot(111)
ax.hist(stretch_100['popen'], bins = np.arange(0,1.05,0.05), color = 'blue')
ax.hist(cluster_100['popen'], bins = np.arange(0,1.05,0.05), color = 'red')
ax.set_title('Popen distribution for 100mM taurine')
popen_100.savefig(os.path.join('/Users/zhiyiwu/GitHub/sc_py/data','taurine_100_Popen.png'),dpi=300)
plt.close(popen_100)

open_shut_100 = plt.figure()
ax = open_shut_100.add_subplot(111)
ax.scatter(stretch_100['mean_open'], stretch_100['mean_shut'], s=1, color = 'blue')
ax.scatter(cluster_100['mean_open'], cluster_100['mean_shut'], s=1, color = 'red')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_title('Mean open vs mean shut for 100mM taurine')
open_shut_100.savefig(os.path.join('/Users/zhiyiwu/GitHub/sc_py/data','taurine_100_cluster_open_close.png'),dpi=300)
plt.close(open_shut_100)

batch_30 = BatchAnalysis(list_30)
cluster_30 = batch_30.compute_cluster_summary()
stretch_30 = batch_30.compute_stretch_summary()

popen_30 = plt.figure()
ax = popen_30.add_subplot(111)
ax.hist(stretch_30['popen'], bins = np.arange(0,1.05,0.05),color = 'blue')
#ax.hist(cluster_30['popen'], bins = np.arange(0,1.05,0.05), color = 'red')
ax.set_title('Popen distribution for 30mM taurine')
popen_30.savefig(os.path.join('/Users/zhiyiwu/GitHub/sc_py/data','taurine_30_stretch_Popen.png'),dpi=300)
plt.close(popen_30)

open_shut_30 = plt.figure()
ax = open_shut_30.add_subplot(111)
#ax.scatter(stretch_30['mean_open'], stretch_30['mean_shut'], s=1,  color = 'blue')
ax.scatter(cluster_30['mean_open'], cluster_30['mean_shut'], s=1,  color = 'red')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_title('Mean open vs mean shut for 30mM taurine')
open_shut_30.savefig(os.path.join('/Users/zhiyiwu/GitHub/sc_py/data','taurine_30_stretch_open_close.png'),dpi=300)
plt.close(open_shut_30)

plt.hist(stretch_100['duration'], bins = range(0,20)) 
plt.xlim = [0,100]