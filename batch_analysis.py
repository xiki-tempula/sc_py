# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 21:27:37 2015

@author: xiki_tempula
"""

from collections import OrderedDict

import numpy as np

class BatchAnalysis:
    '''
    Perform analysis based on the input clusters.
    '''

    def __init__(self, cluster_list):
        self.cluster_list = cluster_list

    def __len__(self):
        return len(self.cluster_list)

    def get_summary_dict(self, *args):
        '''
        Return a dict consists of lists of queried data.
        By default return patchname, cluster_no, popen, amp, duration.
        Optional arguments patchname, cluster_no, popen, amp, duration,
        (to be added).
        '''

        option_list = ['patchname', 'cluster_no', 'popen', 'mean_amp', 'duration']
        if args:
            selection_list = args
        else:
            selection_list = option_list

        result_dict = OrderedDict([(key, []) for key in selection_list])
        for cluster in self.cluster_list:
            for key in result_dict:
                result_dict[key].append(getattr(cluster,key))
        return result_dict


    def get_length(self):
        '''
        Get a list of the number of shuttings and opening periods in cluster.
        Since cluster is prepared to have the same number of open and shut periods.
        The value is the number of open periods.
        '''
        len_list = []
        for cluster in self.cluster_list:
            len_list.append(len(cluster.open_period))
        return len_list

    def get_type(self):
        '''
        Get the type of clusters in the cluster list.
        '''
        type_list = ['receptor', 'mutation', 'composition', 'agonist', 'concentration']
        if not all([hasattr(cluster, 'concentration') for cluster in self.cluster_list]):
            return None

        cluster_type = OrderedDict()

        for key in type_list:
            cluster_type[key] = []
        for cluster in self.cluster_list:
            for key in type_list:
                cluster_type[key].append(getattr(cluster, key))
        return cluster_type

class StretchSummary(BatchAnalysis):
    '''
    Perform stretch specified operations.
    '''
    
    def compute_stretch_summary(self):
        '''
        Compute the summary of stretch information.
        '''
        stretch_summary = []
        
        for cluster in self.cluster_list :
            mode_dict = cluster.get_mode_detail()
            stretch_num = len(mode_dict['popen_list'])
            for index in range(stretch_num):
                new_stretch = {'stretch_num': stretch_num,
                               'popen': mode_dict['popen_list'][index],
                               'mean_open': mode_dict['mean_open'][index],
                               'mean_shut': mode_dict['mean_shut'][index],
                               'duration': mode_dict['duration'][index],
                               'event_num': mode_dict['event_num'][index]}
                stretch_summary.append(new_stretch)
        
        self.stretch_summary = np.zeros((len(stretch_summary), 6)
        , dtype=([('stretch_num','u4'), ('popen','f8'), ('mean_open','f8'),
                  ('mean_shut','f8'), ('duration','f8'), ('event_num','u8')]))
    
    

        