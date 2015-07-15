# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 11:11:09 2015

@author: xiki_tempula
"""

import os
from info import Patch, BatchCluster

def list_folder(current_path):
    '''
    Return a list of all the folders in this directory.
    '''
    return [i_dir for i_dir in os.listdir(current_path)
    if (os.path.isdir(os.path.join(current_path,i_dir)) and i_dir[0] != '.')]

class Batch:
    '''
    Save the information of many clusters into one file.
    '''
    
    def __init__(self, folder_list = None, cluster_list = []):
        '''
        Define the location and name of the final generated report.
        '''
        if type(folder_list) != list:
            if folder_list is None:
                folder_list = [os.getcwd(), ]
            else:
                folder_list = [folder_list, ]
        self._folder_list = folder_list
        self._cluster_list = cluster_list
        
        
    def _add_cluster(self, cluster, **kwargs):
        '''
        Add cluster to cluster list.
        '''
        
        self._cluster_list.append(BatchCluster(cluster,
                                              receptor = kwargs['receptor'],
                                              mutation = kwargs['mutation'],
                                              composition = kwargs['composition'],
                                              agonist = kwargs['agonist'],
                                              concentration = kwargs['concentration']))
    def scan_folder(self, clear = True):
        '''
        Scan and collect all the clusters in the folder.
        '''
        if clear:
            self._cluster_list = []
        for folder in self._folder_list:
            patch_list = [csv for csv in os.listdir(folder) if csv[-4:] == '.csv']
            for patch in patch_list:
                current_path = os.path.join(folder, patch)
                current_patch = Patch(current_path)
                current_patch.scan()
                for cluster in current_patch:
                    self._cluster_list.append(cluster)
        return self._cluster_list
                
            
    
    def scan_orded_folder(self, func = _add_cluster, clear = True):
        '''
        Scan the folder and apply the func to every clusters in the folder.
        If func is not provided, a whole list of the clusters in the folder
        will be generated.
        '''
        if clear:
            self._cluster_list = []
        for folder in self._folder_list:
            current_path = folder
            current_folder_list = list_folder(current_path)
                
            for receptor in current_folder_list:
                current_path_R = os.path.join(current_path, receptor)
                current_folder_list_R = list_folder(current_path_R)
                    
                for mutation in current_folder_list_R:
                    current_path_M = os.path.join(current_path_R, mutation)
                    current_folder_list_M = list_folder(current_path_M)
                    
                    for composition in current_folder_list_M:
                        current_path_C = os.path.join(current_path_M, composition)
                        current_folder_list_C = list_folder(current_path_C)
                        
                        for agonist in current_folder_list_C:
                            current_path_A = os.path.join(current_path_C, agonist)
                            current_folder_list_A = list_folder(current_path_A)
                            
                            for concentration in current_folder_list_A:
                                path = os.path.join(current_path_A, concentration)
                                patch_list = [csv for csv in os.listdir(path)
                                              if csv[-4:] == '.csv']
                                
                                for patch in patch_list:
                                    filepath = os.path.join(path, patch)
                                    current_patch = Patch(filepath)
                                    current_patch.scan()
                                    
                                    for cluster in current_patch:
                                        func(self, cluster,
                                             receptor = receptor,
                                             mutation = mutation,
                                             composition = composition,
                                             agonist = agonist,
                                             concentration = concentration)
        
    def query(self, **kwargs):
        '''
        Output a list of clusters which satisfies the condition.
        '''
        keys = ['receptor', 'mutation', 'composition', 'agonist', 'concentration']
        for key in kwargs:
            if not key in keys:
                raise KeyError("{} is not a recognised key from 'receptor', 'mutation', 'composition', 'agonist', 'concentration'".format(key))
        query_list = []
        for cluster in self._cluster_list:
            condition = True
            for key in kwargs:
                if getattr(cluster,key) != str(kwargs[key]):
                    condition = False
            if condition:
                query_list.append(cluster)
        return query_list
    
    def filter_by(self, amplitude = [-float('inf'), float('inf')],
                        popen = [0,1],
                        duration = [0, float('inf')],
                        event_num = [0, float('inf')]):
        '''
        filter the cluster list by the ablove conditions.
        '''
        query_list = []
        for cluster in self._cluster_list:
            if ((cluster.mean_amp > amplitude[0]) and (cluster.mean_amp < amplitude[1])
                and
                (cluster.popen > popen[0]) and (cluster.popen < popen[1])
                and
                (cluster.duration > duration[0]) and (cluster.duration < duration[1])
                and
                (cluster.event_num > event_num[0]) and (cluster.event_num < event_num[1])):
                    
                query_list.append(cluster)
        return query_list


#a = BatchQuery('/Users/xiki_tempula/Documents/data/')
#a.scan_folder()
#a.query(concentration = 100)
        