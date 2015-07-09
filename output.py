# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 21:50:22 2015

@author: xiki_tempula
"""
from batch_analysis import BatchAnalysis
from BatchQuery import BatchQuery
import os
from collections import OrderedDict

class Output:
    '''
    Out put the cluster information which can be analysised outside the script.
    Such as csv file.
    '''
    
    def __init(self, filepath = os.getcwd(), filename = 'Result.csv'):
        self._filepath = filepath
        self._filename = filename
    
    def save_cluster_list(self, cluster_list):
        batch = BatchAnalysis(cluster_list)
        cluster_type = batch.get_type()
        if cluster_type:
            cluster_type_set = OrderedDict()
            for key in cluster_type:
                cluster_type_set[key] = set(cluster_type[key])

            filename_list = []
            for keys in cluster_type_set:
                if len(cluster_type_set[keys]) == 1:
                    filename_list.append(str(cluster_type_set[keys].pop()))
                else:
                    filename_list.append('/'.join(['{}'.format(i) for i in cluster_type_set[keys]]))
                    
            filename = '_'.join(['{}'.format(i) for i in filename_list])
            filename += '.csv'
            self._filename = filename
            
            

a = BatchQuery('/Users/xiki_tempula/Documents/data/')
a.scan_folder()
a.query(concentration = 100)
query_list = a.query_list
a.query(concentration = 10)
query_list += a.query_list
output = Output()
output.save_cluster_list(query_list)