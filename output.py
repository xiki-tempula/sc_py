# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 21:50:22 2015

@author: xiki_tempula
"""
from batch_analysis import BatchAnalysis
from BatchQuery import BatchQuery
import os
from collections import OrderedDict
import numpy as np

class Output:
    '''
    Out put the cluster information which can be analysised outside the script.
    Such as csv file.
    '''
    
    def __init__(self, filepath = os.getcwd(), filename = 'Result.csv'):
        self._filepath = filepath
        self._filename = filename
        
        self._dtype = {'patchname': 'U20',
                       'cluster_no': 'u8'}
    
    def read_cluster_list(self, cluster_list):
        batch = BatchAnalysis(cluster_list)
        self._batch = batch
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
                    filename_list.append('~'.join(['{}'.format(i) for i in cluster_type_set[keys]]))
                    
            filename = '_'.join(['{}'.format(i) for i in filename_list])
            self._filename = filename
            self._cluster_type = cluster_type
        
    def select_element(self, **kwargs):
        '''
        Select the elements to export.
        Default: patchname, cluster_no, popen, amp, duration.
        '''
        self._selection = OrderedDict()
        self._selection['patchname'] = kwargs.get('patchname', True)
        self._selection['cluster_no'] = kwargs.get('cluster_no', True)
        self._selection['popen'] = kwargs.get('popen', True)
        self._selection['amp'] = kwargs.get('amp', True)
        self._selection['duration'] = kwargs.get('duration', True)
        

        dtype = OrderedDict([(key,self._dtype[key]) if key in self._dtype else (key,'f8')
                          for key in self._selection])

        structured_array = np.zeros((len(self._batch),), 
                                    dtype=[(key, dtype[key]) for key in dtype])
                                    
        cluster_data = self._batch.get_dict()
        for key in self._selection:
            structured_array[key] = cluster_data[key]
        self.structured_array = structured_array
    
    def save_data(self, filepath = None, filename = None, filetype = 'csv'):
        '''
        Save the cluster_data. By default save as csv to the current working dir.
        '''
        if not filepath:
            filepath = self._filepath
        if not filename:
            filename = self._filename
            
        dtype = {'patchname': '%s', 'cluster_no': '%i'}
                       
        np.savetxt(os.path.join(filepath,filename+'.'+filetype), 
                   self.structured_array, delimiter=',',
                   fmt=','.join([dtype[key] if key in self._dtype else '%f'
                          for key in self._selection]))
        
            
                    
        
            
            

#a = BatchQuery('/Users/zhiyiwu/Google Drive/data/')
#a.scan_folder()
#a.query(concentration = 100)
#query_list = a.query_list
#a.query(concentration = 10)
#query_list += a.query_list
#output = Output()
#output.read_cluster_list(query_list)
#output.select_element()
#output.save_data()