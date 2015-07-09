# -*- coding: utf-8 -*-
"""
Read from Csv file and generate the cluster data from it.
"""
import numpy as np
import os
from cost_function import compute_stretch_number, compute_separation_dict, filter_first_last

class Patch:
    '''
    Patch class contains the patch information and the cluster detail.
    '''

    def __init__(self, path):
        if os.path.isfile(path):
            if path[-4:] == '.csv':
                self._filepath, self._patch_name = os.path.split(path)
            else:
                raise NameError('%s is not a csv file.' % path)
        else:
            raise NameError('%s does not exist.' % path)

    def get_path(self):
        '''
        return the complete path.
        '''

        return os.path.join(self._filepath, self._patch_name)

    def scan(self, filterone = True):
        '''
        Scan the csv file to determine clusters.
        '''

        self._cluster_dict = {}
        self._cluster_number = 0

        state, start, end, amp, dwell = np.genfromtxt(
        self.get_path(),
        delimiter=',', usecols=(2,4,5,6,8),unpack=True)

        # Remove all the empty rows
        nonempty = ~np.isnan(state)
        state = state[nonempty]
        state = state[nonempty]
        end = end[nonempty]
        amp = amp[nonempty]
        dwell = dwell[nonempty]

        # Detect number of clusters
        # If the end time is different from the next start time
        # A new cluster is defined
        sep_list = [0, ]
        for i in range(len(nonempty) - 1):
            if end[i] != start[i+1]:
                sep_list.append(i+1)
        sep_list.append(len(nonempty)-1)

        # Create a new cluster data if it is longer than 100ms
        for i in range(len(sep_list) - 1):
            if (end[sep_list[i+1]] - start[sep_list[i]]) > 100:
                # Get the indice for open and shut
                indice = np.array(range(sep_list[i], sep_list[i+1]))
                open_period_idx = np.intersect1d(indice, np.nonzero(state))
                shut_period_idx = np.intersect1d(indice, np.where(state == 0)[0])

                # Make sure that there is the smae number of open and shut period
                cluster_length = min(len(open_period_idx), len(shut_period_idx))
                open_period_idx = open_period_idx[:cluster_length]
                shut_period_idx = shut_period_idx[:cluster_length]



                # Filter out the clusters which is irrigiular
                open_period = dwell[open_period_idx]
                shut_period = dwell[shut_period_idx]

                while filter_first_last(open_period, shut_period):
                    open_period, shut_period = filter_first_last(open_period, shut_period)

                if (len(open_period) != cluster_length):
                    cluster_length = len(open_period)
                    first_idx = np.where(dwell[open_period_idx] == open_period[0])[0][0]
                    last_idx = np.where(dwell[open_period_idx] == open_period[-1])[0][-1]+1
                    open_period_idx = open_period_idx[first_idx: last_idx]
                    shut_period_idx = shut_period_idx[first_idx: last_idx]

                # Create new cluster
                self._cluster_number += 1
                new_cluster = Cluster(self.get_path())
                new_cluster.add_info(self._cluster_number,
                                     start[open_period_idx[0]], end[shut_period_idx[-1]],
                                    dwell[open_period_idx], dwell[shut_period_idx],
                                    amp[open_period_idx], amp[shut_period_idx])
                self._cluster_dict[self._cluster_number] = new_cluster
        self._cluster_list = list(self._cluster_dict.keys())

    def get_cluster(self, cluster_index, output = False):
        '''
        Return the requested cluster.
        '''
        if not hasattr(self, 'cluster_dict'):
            self.scan()

        if output:
            print(self._cluster_dict[cluster_index])
        return self._cluster_dict[cluster_index]

    def get_cluster_list(self, output = False):
        '''
        Return all clusters in this patch.
        '''

        if not hasattr(self, 'cluster_list'):
            self.scan()

        if output:
            print(self._cluster_list)
        return self._cluster_list

    __getitem__ = get_cluster

    def __str__(self):
        if not hasattr(self, 'cluster_number'):
            self.scan()
        str_filepath = 'Filepath: {} \n'.format(self.get_path())
        str_clusternumber = 'Number of clusters: {} \n'.format(int(self._cluster_number))
        return str_filepath+str_clusternumber



class Cluster(Patch):
    '''
    Detail information about a cluster.
    '''

    def add_info(self, cluster_no, start, end,
                 open_period, shut_period,
                 open_amp, shut_amp):
        '''
        Add information about the cluster.
        '''

        self._cluster_no = cluster_no
        self._start = start
        self._end = end
        self._open_period = open_period
        self._shut_period = shut_period
        self._open_amp = open_amp
        self._shut_amp = shut_amp


        # Calculate mean amplitude
        # Only takes into account of the periods longer than 0.3ms
        # If all the periods are less than 0.3ms take the median instead
        open_val = self._open_amp[self._open_period > 0.3]
        shut_val = self._shut_amp[self._open_period > 0.3]
        if len(open_val) > 0:
            mean_amp = np.mean(open_val)
        else:
            mean_amp = np.median(self._open_amp)

        if len(shut_val) > 0:
            mean_amp -= np.mean(shut_val)
        else:
            mean_amp -= np.median(shut_val)
        self._mean_amp = mean_amp

        # Calculate the mean Popen
        self._mean_popen = np.sum(self._open_period)/(np.sum(self._open_period) +
        np.sum(self._shut_period))

        # Calculate the duration
        self._duration = self._end - self._start

    def get_cluster_detail(self):
        '''
        Get the detail info of the start, end, open_period, shut_period,
        open_amp and shut_amp as a dictionary.
        '''
        cluster_dict = {}
        cluster_dict['start'] = self._start
        cluster_dict['end'] = self._end
        cluster_dict['open_period'] = self._open_period
        cluster_dict['shut_period'] = self._shut_period
        cluster_dict['open_amp'] = self._open_amp
        cluster_dict['shut_amp'] = self._shut_amp
        return cluster_dict

    def compute_mode(self, mode_number = 10, threshold = 3):
        '''
        Compute the ways of separating the mode.
        '''

        separation_dict, cost_dict, mean_cost_dict = compute_separation_dict(
        np.log(self._open_period), np.log(self._shut_period), mode_number)
        mode_number = compute_stretch_number(cost_dict, mean_cost_dict, threshold)
        self._mode_number = mode_number
        self._separation_dict = separation_dict
        self._cost_dict = cost_dict
        self._mean_cost_dict = mean_cost_dict

    def compute_mode_detail(self, output = False):
        '''
        Compute the Popen, mean open time, mean shut time.
        '''
        mode_separation = self._separation_dict[self._mode_number]
        mode_start = []
        mode_stop = []
        popen_list = []
        mean_open = []
        mean_shut = []

        for i in range(len(mode_separation)-1):
            open_period = self._open_period[mode_separation[i]:mode_separation[i+1]]
            shut_period = self._shut_period[mode_separation[i]:mode_separation[i+1]]
            popen_list.append(sum(open_period)/(sum(open_period) + sum(shut_period)))
            mean_open.append(np.exp(np.mean(np.log(open_period))))
            mean_shut.append(np.exp(np.mean(np.log(shut_period))))
            if i == 0:
                mode_start.append(0)
            else:
                mode_start.append(sum(self._open_period[:mode_separation[i]])
                + sum(self._shut_period[:mode_separation[i]]))
            mode_stop.append(sum(self._open_period[:mode_separation[i+1]])
                + sum(self._shut_period[:mode_separation[i+1]]))

        self._mode_start = mode_start
        self._mode_stop = mode_stop
        self._popen_list = popen_list
        self._mean_open = mean_open
        self._mean_shut = mean_shut

        if output:
            for i in range(len(mode_stop)):
                print('Mode {}: Start: {:.2f}, End: {:.2f}, Popen {:.2f}, Mean open: {:.2f}, Mean shut: {:.2f}'.format(
                i+1, mode_start[i], mode_stop[i], popen_list[i], mean_open[i],
                mean_shut[i]))

    def get_mode_detail(self):
        '''
        Get the detail info of mode_start, mode_stop, popen_list, mean_open,
        mean_shut as a dictionary.
        '''
        if hasattr(self, '_mode_start'):
            mode_dict = {}
            mode_dict['mode_start'] = self._mode_start
            mode_dict['mode_stop'] = self._mode_stop
            mode_dict['popen_list'] = self._popen_list
            mode_dict['mean_open'] = self._mean_open
            mode_dict['mean_shut'] = self._mean_shut
            mode_dict['separation'] = self._separation_dict[self._mode_number]
            mode_dict['cost_dict'] = self._cost_dict
            mode_dict['mean_cost_dict'] = self._mean_cost_dict
            return mode_dict
        else:
            return None


    def __str__(self):
        str_filepath = 'Filepath: {} \n'.format(self.get_path())
        str_cluster_no = 'Cluster number: {} \n'.format(int(self._cluster_no))
        str_start_end = 'From {:.2f} s to {:.2f} s. \n'.format(self._start/1000, self._end/1000)
        str_duration = 'Cluster duration: {:.2f} ms \n'.format(self._duration)
        str_amp = 'Mean amplitude: {:.2f} pA. \n'.format(self._mean_amp)
        str_popen = 'Popen is {:.2f}'.format(self._mean_popen)
        return str_filepath+str_cluster_no+str_start_end+str_duration+str_amp+str_popen




# a = Patch('/Users/zhiyiwu/GitHub/sc_py/070710c1_0005_5.csv')
# a.scan()
# b = a[1]
# b.compute_mode()
# b.compute_mode_detail(True)
