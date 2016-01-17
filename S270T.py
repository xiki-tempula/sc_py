# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:11:05 2015

@author: zhiyiwu
"""

import os
import codecs

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


from batch_query import Batch
from batch_analysis import BatchAnalysis, PatchExamination


sns.set(color_codes=True)

batch = Batch('./data/')
batch.scan_orded_folder()
concentation_list = ['0.3', '1', '3', '10', '100']
total = ''
amp = []
popen = []
errorbar = []
total_summary = pd.DataFrame()
for concentration in concentation_list:
    cluster_list = batch.query(mutation = 'S270T', concentration = concentration)
    
    patch_list = batch.query(mutation = 'S270T', concentration = concentration, 
                             output = 'patch')
    patch_summary = PatchExamination(patch_list)  
    summary = patch_summary.compute_summary_table()
    summary = pd.DataFrame(summary)
    
    length = len(summary)
    summary.loc[:,'concentration'] = float(concentration)
    total_summary = total_summary.append(summary, ignore_index=True)

    if cluster_list:
        cluster_summary = BatchAnalysis(cluster_list)
        result = cluster_summary.compute_cluster_summary()

        plot = sns.jointplot(result['popen'],result['mean_amp'], stat_func= None)
        plot.set_axis_labels('Popen', 'Amp (pA)')
        plot.savefig(os.path.join('/Volumes/c-floor/William/data','{}_scatter.png'.format(concentration)),dpi=300)
        plt.close()
        
        plot = sns.distplot(result['popen'], bins = np.arange(0,1.05,0.05), kde=False, rug=True);
        plt.title('Popen distribution ({}mM glycine)'.format(concentration))
        plt.savefig(os.path.join('/Volumes/c-floor/William/data','{}_Popen_original.png'.format(concentration)),dpi=300)
        plt.close()
        
        amp.append(result['mean_amp'])
        result = cluster_summary.compute_cluster_summary(patchname = '2015_07_24_0011.csv')


                
        result = cluster_summary.compute_cluster_summary(mean_amp = [3.1,5.1])
        result = cluster_summary.get_summary(output = 'dict')
        popen.append(result['popen']['value'])
        errorbar.append(result['popen']['se'])
        string = cluster_summary.get_summary(output = 'string')
        string = '{}mM: \n'.format(concentration) + string
        total += string + '\n'
        print(string)

file = codecs.open('/Volumes/c-floor/William/data/summary.txt', 'w', "utf-8")
file.write(total)
file.close()

amp = np.hstack(amp)
sns.distplot(amp, kde= False, rug=True);
plt.xlabel('Amplitude (pA)')
plt.savefig(os.path.join('/Volumes/c-floor/William/data','AMP_dist.png'.format(concentration)),dpi=300)

df = pd.DataFrame({'popen':popen,'concentration (mM)': [float(con) for con in concentation_list]},index = concentation_list)
g = sns.FacetGrid(df)
g.map(plt.errorbar, 'concentration (mM)', "popen",yerr=errorbar, fmt='o')
plt.xscale('log')
plt.xlim([0.1, 1000])
plt.title('Popen curve')
plt.savefig(os.path.join('/Volumes/c-floor/William/data','Popen_curve.png'),dpi=300)
plt.close()
total_summary.to_csv('out.csv', index=False)