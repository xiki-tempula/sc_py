# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 14:48:32 2015

@author: xiki_tempula
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

for concentration in concentation_list:
    cluster_list = batch.query(mutation = 'S270T', concentration = concentration)
    cluster_summary = BatchAnalysis(cluster_list)  
    summary = cluster_summary.compute_cluster_summary()
    np.savetxt(concentration+'.csv', summary, 
               fmt= ['%s', '%i', '%.2f', '%.2f','%.2f','%i','%.2f','%.2f'],
               delimiter = ',')
    