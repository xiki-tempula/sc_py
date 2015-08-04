# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 21:50:22 2015

@author: xiki_tempula
"""

import os

import numpy as np

from dtype import dtype

class Output:
    '''
    Out put the cluster information which can be analysised outside the script.
    Such as csv file.
    '''

    def __init__(self, filepath = os.getcwd(), filename = 'Result'):
        self._filepath = filepath
        self._filename = filename
        self._dtype = dtype

    def load_result(self, summary):
        '''
        load the data from the the processed array.
        '''
        self._summary = summary
        self._selection = summary.dtype.fields
    
    def save_data(self, filetype = 'csv', selection = None):
        '''
        Save the cluster_data. By default save as csv to the current working dir.
        '''
        if selection:
            self._selection = selection


        dtype = {}
        for key in self._selection:
            if self._selection[key][0] == 'u':
                dtype[key] = '%i'
            elif self._selection[key][0] == 'f':
                dtype[key] = '%f'
            else:
                dtype[key] = '%s'


        np.savetxt(os.path.join(filepath,filename+'.'+filetype),
                   self.structured_array, delimiter=',',
                   fmt=','.join([dtype[key] for key in self._selection]))


