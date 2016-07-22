# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:11:05 2015

@author: zhiyiwu
"""

import os
import codecs

import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns
import pandas as pd

from info import Patch
from batch_query import Batch
from batch_analysis import BatchAnalysis, PatchExamination


#sns.set(color_codes=True)


name_list = [
'06111410',
'06111411',
'15060420',
'15072908']
tres = [
20,
20,
20,
20]
tcrit = [
70,
70,
70,
70]
cluster_list = []

data = np.loadtxt('./ekdist_paramteters.csv', 
                  delimiter=',', dtype={
                  'names': ('filename', 'concentration', 'res', 'tcrit'),
                  'formats': ('S8', 'S3', 'f4', 'f4')})

concentrations = [1,3,10,100]
for concentration in concentrations:
    for patch in data:
        if float(patch['concentration']) == concentration:
            filename = "./ekdist_traces/{}.scn".format(patch['filename'].decode('utf8'))
#
#            filename = "./raw trace/{}/{}.scn".format(patch['concentration'].decode('utf8'), 
#    patch['filename'].decode('utf8'))
            patch = Patch(filename)
            patch.read_scn(tres=patch['res']*1e-6, tcrit=patch['tcrit']*1e-6)
            cluster_list.extend(patch.get_cluster_list())
            
    
    
    batch_analysis = BatchAnalysis(cluster_list)
    summary = batch_analysis.compute_cluster_summary()
    summary['start'] /= 1000
    summary['end'] /= 1000
    
    np.savetxt('temp.csv', summary, delimiter=',', fmt = '%s,%.18e,%.18e,%.18e,%.18e,%.18e,%.18e,%.18e,%.18e,%.18e,%.18e,%.18e')
    col_name = str(summary.dtype.names)
    col_name = col_name[1:-1] + '\n'
    f = open('temp.csv','r')
    string = f.read()
    string = col_name + string
    f.close()
    f = open('scan_summary_{}.csv'.format(concentration),'w')
    f.write(string)
    f.close()

#concentration = 10
#total = ''
#amp = []
#popen = []
#total_summary = pd.DataFrame()
#
#patch_summary = PatchExamination(patch_list)
#summary = patch_summary.compute_summary_table()
#summary = pd.DataFrame(summary)
#
#length = len(summary)
#
#total_summary = total_summary.append(summary, ignore_index=True)
#
#if cluster_list:
#    cluster_summary = BatchAnalysis(cluster_list)
#    result = cluster_summary.compute_cluster_summary()
#
#    result = cluster_summary.get_summary(output = 'dict')
#    popen.append(result['popen']['value'])
#    errorbar.append(result['popen']['se'])
#    string = cluster_summary.get_summary(output = 'string')
#    string = '{}mM: \n'.format(concentration) + string
#    total += string + '\n'
#    print(string)
#
#df = pd.DataFrame({'popen':popen,'concentration (mM)': [float(con) for con in concentation_list]},index = concentation_list)
#
#total_summary.to_csv('out.csv', index=False)
