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

def impose_resolution(start, end, period, amp, flag, resolution):
    '''
    Impose resolution.
    '''
    assert ((end - start) - sum(period)) < 0.1
    assert all([len(element) == len(period) for element in [amp, flag]])

    # Prepare the data
    cluster_length = len(period)
    state = np.empty(cluster_length, dtype=bool)
    state[::2] = True
    state[1::2] = False

    # Find out the periods which is unresolvable
    unresolvable = np.where(period < resolution)[0]
    if len(unresolvable):
    
        # Cluster the unresolvable into consecutive compoents
        unresolvable = np.split(unresolvable, np.where(np.diff(unresolvable) != 1)[0]+1)
    
        for index in unresolvable:
            # If this index does not include the first period
            # Merge all the periods in the index with the previous one
            if index[0] != 0:
                new_amp = amp[index[0]-1]
                new_state = state[index[0]-1]
                index = np.hstack((index[0]-1, index))
            # Since there is no previous one
            # Merge all the periods in the index
            else:
                new_state = False
                new_amp = np.nan
    
            # Merge all the periods
            new_period = sum(period[index])
            # Detect bad flag
            new_flag = BROKEN if any([flag[i] == BROKEN for i in index]) else NORMAL
    
            # Flag the unresolvble in the period
            amp[index] = np.nan
    
            # Fill in the merged value
            amp[index[0]] = new_amp
            period[index[0]] = new_period
            flag[index[0]] = new_flag
            state[index[0]] = new_state
    
        # Filter out all the flags
        valid = np.isfinite(amp)
    
        # Find the first open and last shut
        first = None
        last = None
        for index in range(cluster_length):
            if valid[index] and state[index]:
                first = index
                break
        for index in reversed(range(cluster_length)):
            if valid[index] and not state[index]:
                last = index + 1
                break
            
        if first is not None and last is not None:
            # Update the valid range
            valid[:first] =False
    
            valid[last:] = False
            
        
            # Update all the value
            start += np.nansum(period[:first])
            end -= np.nansum(period[last:])
            amp = amp[valid]
            period = period[valid]
            flag = flag[valid]
            state = state[valid]
        
            # Check for the consecutive open and shut
            open_index  = np.where(state == True)[0]
            shut_index  = np.where(state == False)[0]
            # Find out all the adjacent shut/open.
            consecutive = []
            
            consecutive_open = np.where(np.diff(open_index) == 1)[0]
            if consecutive_open.size != 0:
                consecutive_open = np.unique(np.append(open_index[consecutive_open], open_index[consecutive_open+1]))
                consecutive_open = np.split(consecutive_open, np.where(np.diff(consecutive_open) != 1)[0]+1)
                consecutive += consecutive_open
            
            consecutive_shut = np.where(np.diff(shut_index) == 1)[0]
            if consecutive_shut.size != 0:
                consecutive_shut = np.unique(np.append(shut_index[consecutive_shut], shut_index[consecutive_shut+1]))
                consecutive_shut = np.split(consecutive_shut, np.where(np.diff(consecutive_shut) != 1)[0]+1)
                consecutive += consecutive_shut
        
            if len(consecutive) > 0:
                # Merge all the consecutive open and shut
                for index in consecutive:
                    new_amp = np.mean(amp[index])
                    new_period = np.sum(period[index])
                    try:
                        new_state = state[index][0]
                    except IndexError:
                        pass
                    new_flag = BROKEN if any([flag[i] == BROKEN for i in index]) else NORMAL
        
                    # Delete all the value in this range
                    amp[index] = np.nan
                    period[index] = np.nan
                    flag[index] = np.nan
                    state[index] = np.nan
        
                    # Fill in the merged value
                    amp[index[0]] = new_amp
                    period[index[0]] = new_period
                    flag[index[0]] = new_flag
                    state[index[0]] = new_state
        
                # Get rid of the NaN
                valid = np.isfinite(period)
                amp = amp[valid]
                period = period[valid]
                flag = flag[valid]
                state = state[valid]
        
    
        return start, end, period, amp, flag
    else:
        return None