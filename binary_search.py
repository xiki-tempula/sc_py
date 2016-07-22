# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 09:27:38 2016

@author: zhiyiwu
"""

import numpy as np
from scipy.stats import ttest_ind
from scipy.cluster.hierarchy import dendrogram, linkage
import queue

def std(data, sep, length = None):
    if length:
        pass
    else:
        length = len(data)
    result = np.std(data[:sep,:]) ** 2 * sep
    result += np.std(data[sep:,:]) ** 2 * (length - sep)
    return result
    
def binary_search(data, func):
    '''
    Search the best point using the binary method.
    Each data point is a role
    '''
    start = 0
    length = end = len(data)
    while (end - start) > 3:
        region = (end - start) // 3
        first_part = func(data, start + region, length)
        second_part = func(data, end - region, length)
        if first_part < second_part:
            end -= region
        else:
            start += region
    return (start + end) // 2

def linear_search(data, func):
    length = len(data)
    i = 1

    min_std = float('inf')
    sep = 0
    while i < length-1:
        result = func(data, i, length)
        if result < min_std:
            min_std = result
            sep = i
        i += 1
    return sep            

def t_test(data, sep, length, threshold = 0.05):
    t, prob = ttest_ind(data[:sep],data[sep:], equal_var = False)
    if prob < threshold:
        return True
    else:
        return False

def min_number(data, sep, length, minimum = 10):
    if sep < minimum or sep > (length - minimum):
        return False
    else:
        return True
 
    

def BFS(data, max_cluster = 100, func_min = std, func_crict = t_test):
    sep_list = []
    start = 0
    end = len(data)
    index = (start, end)
    Queue = queue.Queue()
    Queue.put(index)
    while Queue.empty() is False:
        start, end = Queue.get()
        sep = binary_search(data[start: end], func_min)
#        sep = linear_search(data[start: end], func_min)
        if func_crict(data[start: end], sep, end-start) is False:
            pass
        else:
            sep_list.append(start + sep)
            if (sep < max_cluster):
                Queue.put((start + sep, end))
            elif (sep > ((end - start) - max_cluster)):
                Queue.put((start, start + sep))
            else:
                Queue.put((start + sep, end))
                Queue.put((start, start + sep))
    return sep_list

def mean(data):
    return (np.mean(data),)

def prepare_data(data, sep_list, func = mean):
    data_list = []
    sep_list.extend([0, len(data)])
    sep_list = sorted(sep_list)
    for index in range(len(sep_list)-1):
        data_list.append(func(data[sep_list[index]: sep_list[index+1]]))
    return data_list, sep_list
    
    

def hierarchical_clustering(data, sep_list, maximum_cluster = 10):
    data_list, sep_list = prepare_data(data, sep_list)
    Z = linkage(data_list, 'ward')
    dendrogram(Z)
    
    
    

        
    
    
##np.random.seed(100)
#a = np.random.normal(loc=1.0, scale=0.5, size=(2000,1))
#b = np.random.normal(loc=2.0, scale=0.5, size=(4000,1))
#c = np.random.normal(loc=1.0, scale=0.5, size=(2000,1))
#d = np.random.normal(loc=2.0, scale=0.5, size=(2000,1))
#data = np.vstack((a,b,c,d))
#
#
##count = 0
##for i in range(100):
##    if binary_search(data, std) < 210 or binary_search(data, std) > 190:
##        count += 1
##print(count)
#sep_list = BFS(data)
#print(sep_list)
#hierarchical_clustering(data, sep_list)
