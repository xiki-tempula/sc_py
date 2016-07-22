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


from batch_query import Batch
from batch_analysis import BatchAnalysis, PatchExamination


#sns.set(color_codes=True)

batch = Batch('/Users/zhiyiwu/Desktop/data/')
batch.scan_orded_folder()
concentation_list = ['10',]
total = ''
amp = []
popen = []
errorbar = []
total_summary = pd.DataFrame()
for concentration in concentation_list:
    cluster_list = batch.query(mutation = 'wt', concentration = concentration)
    batch_analysis = BatchAnalysis(cluster_list)
    summary = batch_analysis.compute_cluster_summary()
    summary['start'] /= 1000
    summary['end'] /= 1000

    np.savetxt('test.csv', summary, delimiter=',', fmt = '%s,%.18e,%.18e,%.18e,%.18e,%.18e,%.18e,%.18e,%.18e,%.18e,%.18e,%.18e')

