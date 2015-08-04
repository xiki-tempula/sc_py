# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 18:18:25 2015

@author: zhiyiwu
"""
import numpy as np
import scipy as sc
import itertools
import time

def compute_cost(open_period, shut_period, separation, result_dict = None):
    '''
    Compute the cost based on the way of separation.
    '''
    if result_dict is None:
        result_dict = {}
    modes = len(separation) - 1
    cost = 0
    for i in range(modes):
        if not (separation[i], separation[i+1]) in result_dict:
            result_dict[(separation[i], separation[i+1])] = np.var(open_period[separation[i]: separation[i+1]])*(separation[i+1]-separation[i])
            result_dict[(separation[i], separation[i+1])] += np.var(shut_period[separation[i]: separation[i+1]])*(separation[i+1]-separation[i])
        cost += result_dict[(separation[i], separation[i+1])]
    return cost, result_dict

def add_separation(open_period, shut_period, separation, result_dict):
    '''
    Add one separation point which yeild the minium cost function to the data.
    '''
    cost = float('inf')
    mean_cost = 0
    cluster_length = len(open_period)
    for i in range(cluster_length):
        new_separation = np.append(separation, i)
        new_separation = np.unique(new_separation)
        new_cost, result_dict = compute_cost(open_period, shut_period, new_separation, result_dict)
        mean_cost += new_cost
        if new_cost < cost:
            cost = new_cost
            separation_list = new_separation
    mean_cost /= cluster_length
    return separation_list, cost, mean_cost, result_dict



def compute_separation_dict(open_period, shut_period, mode_number, output = False):
    '''
    Compute the way of separation the cluster given the maxium number of modes.
    '''
    if output:
        print('Computing for the separation for mode 1.')
    separation_dict = {}
    separation = [0, len(open_period)]
    separation_dict[1] = separation

    cost_dict = {}
    cost_dict[1], result_dict = compute_cost(open_period, shut_period, separation)

    mean_cost_dict = {}
    mean_cost_dict[1] = cost_dict[1]
    
    if mode_number > 1:
        for i in range(2, mode_number+1):
            if output:
                print('Computing for the separation for mode {}.'.format(i))
            separation, cost, mean_cost, result_dict = add_separation(open_period, shut_period,
                                           separation, result_dict)
            separation_dict[i] = separation
            cost_dict[i] = cost
            mean_cost_dict[i] = mean_cost
    return separation_dict, cost_dict, mean_cost_dict

def elbow_search(curve):
    '''
    Search the elbow point in the curve.
    '''
    n_points = len(curve)
    all_coor = np.vstack((np.arange(1, n_points+1), curve))
    all_coor = np.transpose(all_coor)
    first_point = all_coor[0, :]
    lin_vec = all_coor[-1, :] - first_point
    lin_vec_n = lin_vec/np.sqrt(sum(lin_vec**2))

    vec_from_first = all_coor - first_point

    scalar_product = np.dot(vec_from_first, lin_vec_n)

    vec_from_first_parallel = scalar_product[:,None] * lin_vec_n
    vec_to_line = vec_from_first - vec_from_first_parallel

    dist_to_line = np.sqrt(np.sum(vec_to_line ** 2, axis=1))
    return np.argmax(dist_to_line)

def compute_stretch_number(cost_dict, mean_cost_dict, threshold = 3, output = False):
    '''
    Compute the appropriate mode number.
    '''
    cost_list = [cost_dict[i] for i in cost_dict]
    mode_number = elbow_search(cost_list) + 1
    difference = [mean_cost_dict[i] - cost_dict[i] for i in cost_dict.keys()]

    quotient = np.mean(difference[1:mode_number])/np.mean(difference[mode_number:])
    if output:
        print('The threshold is {} and the quotient is {}'.format(threshold, quotient))
    if quotient < threshold:
        mode_number = 1
    if output:
        print('The number of stretches is {}'.format(mode_number))
    return mode_number

def compute_separation_dp(open_period, shut_period, max_mode_number):
    '''
    Wrapper of the computing the separation DP method.
    '''
    assert len(open_period) == len(shut_period)

    separation_dict = {}
    cost_dict = {}

    cluster_length = len(open_period)
    information_matrix = np.empty([cluster_length, cluster_length])
    information_matrix.fill(np.nan)

    for mode_number in range(1, max_mode_number+1):
        cost, separation_result, information_matrix = separation_mode_dp(open_period, shut_period, mode_number, cluster_length, information_matrix)
        separation_dict[mode_number] = separation_result
        cost_dict[mode_number] = cost

    return separation_dict, cost_dict

def test_dp(open_period, shut_period, max_mode_number):
    '''
    Estimate the time it might taken for computing the result.
    '''
    assert len(open_period) == len(shut_period)
    cluster_length = len(open_period)
    cost, separation_result, information_matrix = separation_mode_dp(
    open_period, shut_period, 3, cluster_length)
    
    start_time = time.time()
    separation_mode_dp(open_period, shut_period, 4, cluster_length, information_matrix)
    elapsed_time = time.time() - start_time
    
    amp = elapsed_time/sc.misc.comb(cluster_length, 3)
    
    time_dict = {}    
    for i in range(1,max_mode_number+1):
        time_dict[i] = sc.misc.comb(cluster_length, i-1)*amp
        
        print('It is estimated to take {} to compute {} modes'.format(
        time.strftime('%H:%M:%S', time.gmtime(time_dict[i])),
        i))
    return time_dict


def separation_mode_dp(open_period, shut_period, mode_number, cluster_length, information_matrix = None):
    '''
    Compute separation method for a certain mode number.
    '''
    if information_matrix is None:
        information_matrix = np.empty([cluster_length+1, cluster_length+1])
        information_matrix.fill(np.nan)

    cost = float('inf')
    separation_result = None
    for combinations in itertools.combinations(range(1,cluster_length), mode_number-1):
        separation = [0,]
        separation.extend(combinations)
        separation.append(cluster_length)
        new_cost = 0

        for stretch_number in range(len(separation)-1):
            start = separation[stretch_number]
            end = separation[stretch_number+1]
            
            # The -1 after end means that information_matrix[i,j]
            # signifies the cost from ith entry to the jth entry
            # Since when indexing [i:j] python only takes ith to j-1th
            # So this -1 offsets the -1 and makes the matrix size reasonble
            if np.isnan(information_matrix[start, end-1]):
                stretch_cost = (np.var(open_period[start:end]) + np.var(shut_period[start:end])) * (end - start)
                information_matrix[start, end-1] = stretch_cost

            new_cost += information_matrix[start, end-1]

        if new_cost < cost:
            cost = new_cost
            separation_result = separation
    return cost, separation_result, information_matrix
