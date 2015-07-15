# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 18:18:25 2015

@author: zhiyiwu
"""
import numpy as np

def compute_cost(open_period, shut_period, separation):
    '''
    Compute the cost based on the way of separation.
    '''
    modes = len(separation) - 1
    cost = 0
    for i in range(modes):
        temp_open_period = open_period[separation[i]: separation[i+1]]
        cost += np.sum((temp_open_period - np.mean(temp_open_period))**2)
        temp_shut_period = shut_period[separation[i]: separation[i+1]]
        cost += np.sum((temp_shut_period - np.mean(temp_shut_period))**2)
    return cost

def add_separation(open_period, shut_period, separation):
    '''
    Add one separation point which yeild the minium cost function to the data.
    '''
    cost = float('inf')
    mean_cost = 0
    cluster_length = len(open_period)
    for i in range(cluster_length):
        new_separation = np.append(separation, i)
        new_separation = np.unique(new_separation)
        new_cost = compute_cost(open_period, shut_period, new_separation)
        mean_cost += new_cost
        if new_cost < cost:
            cost = new_cost
            separation_list = new_separation
    mean_cost /= cluster_length
    return separation_list, cost, mean_cost



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
    cost_dict[1] = compute_cost(open_period, shut_period, separation)

    mean_cost_dict = {}
    mean_cost_dict[1] = cost_dict[1]

    if mode_number > 1:
        for i in range(2, mode_number+1):
            if output:
                print('Computing for the separation for mode {}.'.format(i))
            separation, cost, mean_cost = add_separation(open_period, shut_period,
                                           separation)
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
