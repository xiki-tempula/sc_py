# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 21:27:37 2015

@author: xiki_tempula
"""

from collections import OrderedDict

class BatchAnalysis:
    '''
    Perform analysis based on the input clusters.
    '''
    
    def __init__(self, cluster_list):
        self.cluster_list = cluster_list
    
    def __len__(self):
        return len(self.cluster_list)
    
    def get_dict(self, *args):
        '''
        Return a dict consists of lists of queried data.
        By default return patchname, cluster_no, popen, amp, duration.
        Optional arguments patchname, cluster_no, popen, amp, duration, 
        (to be added).
        '''
        
        option_list = ['patchname', 'cluster_no', 'popen', 'amp', 'duration']
        if args:
            selection_list = args
        else:
            selection_list = option_list
        
        result_dict = OrderedDict([(key, []) for key in selection_list])
        for cluster in self.cluster_list:
            for key in result_dict:
                result_dict[key].append(getattr(cluster,key))
        return result_dict

        
    
    def get_patchname(self):
        '''
        Get a list of all the patch name of the cluster list.
        '''
        patchname_list = []
        for cluster in self.cluster_list:
            patchname_list.append(cluster.patchname)
        return patchname_list
    
    def get_cluster_no(self):
        '''
        Get a list of cluster number in the Patch.
        '''
        cluster_no_list = []
        for cluster in self.cluster_list:
            cluster_no_list.append(cluster.cluster_no)
        return cluster_no_list
    
    def get_popen(self):
        '''
        Get a list of cluster Popen.
        '''
        popen_list = []
        for cluster in self.cluster_list:
            popen_list.append(cluster.popen)
        return popen_list
    
    def get_amp(self):
        '''
        Get a list of cluster amplitude.
        '''
        amp_list = []
        for cluster in self.cluster_list:
            amp_list.append(cluster.amp)
        return amp_list
    
    def get_duration(self):
        '''
        Get a list of cluster duration.
        '''
        amp_list = []
        for cluster in self.cluster_list:
            amp_list.append(cluster.duration)
        return amp_list
        
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