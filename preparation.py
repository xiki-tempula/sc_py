# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 15:50:31 2015

@author: zhiyiwu
"""
from cost_function import add_separation
import numpy as np
from props import NORMAL, BROKEN

def filter_first_last(open_period, shut_period):
    '''
    Chop off the first or the last event if it is classifed as one stetch.
    '''
    separation_list, cost, mean_cost = add_separation(open_period, shut_period,
                                                      [0, len(open_period)])
    if separation_list[1] == 1:
        open_period = open_period[1:]
        shut_period = shut_period[1:]
    elif separation_list[1] == len(open_period)-2:
        open_period = open_period[:-2]
        shut_period = shut_period[:-2]
    else:
        return False
    return open_period, shut_period

def impose_resolution(start, end, 
                      open_period, shut_period,
                      open_amp, shut_amp,
                      open_flag, shut_flag,
                      resolution):
    '''
    Impose resolution.
    '''
    assert ((end - start) - (sum(open_period) + sum(shut_period))) < 0.00001
    assert len(open_period) == len(shut_period)
    assert len(open_amp) == len(shut_amp)
    assert len(open_flag) == len(shut_flag)
    
    # Prepare the data
    cluster_length = len(open_period)*2
    period = np.empty(cluster_length)
    period[::2] = open_period
    period[1::2] = shut_period
    amp = np.empty(cluster_length)
    amp[::2] = open_amp
    amp[1::2] = shut_amp
    flag = np.empty(cluster_length)
    flag[::2] = open_amp
    flag[1::2] = shut_flag
    state = np.empty(cluster_length, dtype=bool)
    state[::2] = True
    state[1::2] = False
    
    # Find out the periods which is unresolvable
    unresolvable = np.where(period < resolution)[0]

    # Cluster the unresolvable into consecutive compoents
    unresolvable = np.split(unresolvable, np.where(np.diff(unresolvable) != 1)[0]+1)
    
    for index in unresolvable:
        # If this index does not include the first period and the last period
        if index[0] != 0:
            # If the period before the first element of unresolvable list is
            # the same as the period after the last unresolvable list.
            # Merge all the periods in between
            if (state[index[0]-1] == state[index[-1]+1]) and (index[-1] != cluster_length-1):
                new_amp = (amp[index[0]-1] + amp[index[-1]+1])/2
                index = np.hstack((index, index[-1]+1, index[0]-1))
            # if not leave the next resolvable period untouched
            else:
                new_amp = amp[index[0]-1]
                index = np.hstack((index, index[0]-1))
                
            new_state = state[index[0]-1]
        else:
            new_state = False
            if state[index[-1]+1]:
                new_amp = np.nan
            else:
                new_amp = amp[index[-1]+1]
                index = np.hstack((index, index[-1]+1))
                
        new_period = sum(period[index])
        new_flag = BROKEN if any([flag[i] == BROKEN for i in index]) else NORMAL
        
        # Delete all the value in this range
        amp[index] = np.nan
        period[index] = np.nan
        flag[index] = np.nan
        state[index] = np.nan
        
        # Fill in new value
        amp[index[0]] = new_amp
        period[index[0]] = new_period
        flag[index[0]] = new_flag
        state[index[0]] = new_state
    
    # Filter out all the NaN   
    valid = np.isfinite(period)    
    amp = amp[valid]
    period = period[valid]
    flag = flag[valid]
    state = state[valid]
    
    # Check head and tail
    if not state[0]:
        start += period[0]
        head = 1
    else:
        head = 0
        
    if state[-1]:
        end -= period[-1]
        tail = -1
    else:
        tail = None
    
    # Chop off the head or tail if the head is shut or the tail is open
    if (head == 1) or (tail == -1):
        amp = amp[head:tail]
        period = period[head:tail]
        flag = flag[head:tail]
        state = state[head:tail]
    
    open_period = period[::2]
    shut_period = period[1::2]
    open_amp = period[::2]
    shut_amp = period[1::2]
    open_flag = period[::2]
    shut_flag = period[1::2]
    
    return start, end, open_period, shut_period, open_amp, shut_amp, open_flag, shut_flag
    