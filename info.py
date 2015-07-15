# -*- coding: utf-8 -*-
"""
Read from Csv file and generate the cluster data from it.
"""
import numpy as np
import os
from cost_function import compute_stretch_number, compute_separation_dict
from preparation import filter_first_last, impose_resolution


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

    def scan(self, filterone = False):
        '''
        Scan the csv file to determine clusters.
        '''

        self._cluster_dict = {}
        self._cluster_number = 0

        state, start, end, amp, dwell = np.genfromtxt(
        self.get_path(),
        delimiter=',', usecols=(2,4,5,6,8),unpack=True)

        # Remove all the empty rows
        nonempty = np.isfinite(state)
        state = state[nonempty]
        start = start[nonempty]
        end = end[nonempty]
        amp = amp[nonempty]
        dwell = dwell[nonempty]

        # Detect number of clusters
        # If the end time is different from the next start time
        # A new cluster is defined
        sep_list = [0, ]
        for i in range(len(state) - 1):
            if end[i] != start[i+1]:
                sep_list.append(i+1)
        sep_list.append(len(state))

        # Create a new cluster data if it is longer than 100ms
        for i in range(len(sep_list) - 1):
            if (end[sep_list[i+1]-1] - start[sep_list[i]]) > 100:
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
                if filterone:
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
                new_cluster = Cluster(self._patch_name, i+1)
                new_cluster.add_info(self._cluster_number,
                                     start[open_period_idx[0]], end[shut_period_idx[-1]],
                                    dwell[open_period_idx], dwell[shut_period_idx],
                                    amp[open_period_idx], amp[shut_period_idx],
                                    np.zeros(len(open_period_idx)),
                                    np.zeros(len(shut_period_idx)))
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

    def __iter__(self):
        cluster_list = self._cluster_list.copy()
        while cluster_list:
            yield self._cluster_dict[cluster_list.pop(0)]

    def __repr__(self):
        return 'Patch({})'.format(self._patch_name)

    def __str__(self):
        if not hasattr(self, 'cluster_number'):
            self.scan()
        str_filepath = 'Filepath: {} \n'.format(self.get_path())
        str_clusternumber = 'Number of clusters: {} \n'.format(int(self._cluster_number))
        return str_filepath+str_clusternumber



class Cluster:
    '''
    Detail information about a cluster.
    '''

    def __init__(self, patchname, cluster_no):
        self.patchname = patchname
        self.cluster_no = cluster_no

    def add_info(self, cluster_no, start, end,
                 open_period, shut_period,
                 open_amp, shut_amp,
                 open_flag, shut_flag):
        '''
        Add information about the cluster.
        '''

        self.cluster_no = cluster_no
        self.start = start
        self.end = end
        self.open_period = open_period
        self.shut_period = shut_period
        self.open_amp = open_amp
        self.shut_amp = shut_amp
        self._open_flag = open_flag
        self._shut_flag = shut_flag

        # Calculate the mean Popen
        self.popen = np.sum(self.open_period)/(np.sum(self.open_period) +
        np.sum(self.shut_period))

        # Impose resolution
        self.impose_resolution()

        # Calculate mean amplitude
        # Only takes into account of the periods longer than 0.3ms
        # If all the periods are less than 0.3ms take the median instead
        self.mean_amp = np.mean(self.open_amp-self.shut_amp)

        # Calculate the duration
        self.duration = sum(self.open_period) + sum(self.shut_period)

        # Number of events in th cluster
        self.event_num = len(self.open_period) + len(self.shut_period)

    def _get_period(self):
        cluster_length = len(self.open_period)*2
        period = np.empty(cluster_length)
        period[::2] = self.open_period
        period[1::2] = self.shut_period
        return period

    def _set_period(self, period):
        self.open_period = period[::2]
        self.shut_period = period[1::2]

    period = property(_get_period, _set_period)

    def _get_amp(self):
        cluster_length = len(self.open_amp)*2
        amp = np.empty(cluster_length)
        amp[::2] = self.open_amp
        amp[1::2] = self.shut_amp
        return amp

    def _set_amp(self, amp):
        self.open_amp = amp[::2]
        self.shut_amp = amp[1::2]

    amp = property(_get_amp, _set_amp)

    def _get_flag(self):
        cluster_length = len(self._open_flag)*2
        flag = np.empty(cluster_length)
        flag[::2] = self._open_flag
        flag[1::2] = self._shut_flag
        return flag

    def _set_flag(self, flag):
        self._open_flag = flag[::2]
        self._shut_flag = flag[1::2]

    flag = property(_get_flag, _set_flag)

    def impose_resolution(self, resolution = 0.3):
        '''
        Impose resolution. By default: 0.3ms
        '''
        (self.start,
         self.end,
         self.period,
         self.amp,
         self.flag) = impose_resolution(self.start,
                                             self.end,
                                             self.period,
                                             self.amp,
                                             self.flag,
                                             resolution)


    def get_cluster_detail(self):
        '''
        Get the detail info of the start, end, open_period, shut_period,
        open_amp and shut_amp as a dictionary.
        '''
        cluster_dict = {}
        cluster_dict['start'] = self.start
        cluster_dict['end'] = self.end
        cluster_dict['open_period'] = self.open_period
        cluster_dict['shut_period'] = self.shut_period
        cluster_dict['open_amp'] = self.open_amp
        cluster_dict['shut_amp'] = self.shut_amp
        return cluster_dict

    def compute_mode(self, mode_number = 10, threshold = 3):
        '''
        Compute the ways of separating the mode.
        '''
        self.impose_resolution()
        separation_dict, cost_dict, mean_cost_dict = compute_separation_dict(
        np.log(self.open_period), np.log(self.shut_period), mode_number)
        mode_number = compute_stretch_number(cost_dict, mean_cost_dict, threshold)
        self.mode_number = mode_number
        self._separation_dict = separation_dict
        self._cost_dict = cost_dict
        self._mean_cost_dict = mean_cost_dict

    def compute_mode_detail(self, output = False):
        '''
        Compute the Popen, mean open time, mean shut time.
        '''
        mode_separation = self._separation_dict[self.mode_number]
        mode_start = []
        mode_stop = []
        popen_list = []
        mean_open = []
        mean_shut = []

        for i in range(len(mode_separation)-1):
            open_period = self.open_period[mode_separation[i]:mode_separation[i+1]]
            shut_period = self.shut_period[mode_separation[i]:mode_separation[i+1]]
            popen_list.append(sum(open_period)/(sum(open_period) + sum(shut_period)))
            mean_open.append(np.exp(np.mean(np.log(open_period))))
            mean_shut.append(np.exp(np.mean(np.log(shut_period))))

            mode_start.append(sum(self.open_period[:mode_separation[i]])
                + sum(self.shut_period[:mode_separation[i]]))
            mode_stop.append(sum(self.open_period[:mode_separation[i+1]])
                + sum(self.shut_period[:mode_separation[i+1]]))

        self.mode_start = self.start + np.array(mode_start)
        self.mode_stop = self.start + np.array(mode_stop)
        self.popen_list = popen_list
        self.mean_open = mean_open
        self.mean_shut = mean_shut

        if output:
            for i in range(len(mode_stop)):
                print('Mode {}: Start: {:.2f}, End: {:.2f}, Popen {:.2f}, Mean open: {:.2f}, Mean shut: {:.2f}'.format(
                i+1, mode_start[i], mode_stop[i], popen_list[i], mean_open[i],
                mean_shut[i]))

    def _get_separation(self):
        return self._separation_dict[self.mode_number]
    separation = property(_get_separation)

    def _get_normalised_cost(self):
        return np.array([self._cost_dict[i] for i in self._cost_dict])/self.event_num
    normalised_cost = property(_get_normalised_cost)

    def _get_normalised_mean_cost(self):
        return np.array([self._mean_cost_dict[i] for i in self._mean_cost_dict])/self.event_num
    normalised_mean_cost = property(_get_normalised_mean_cost)

    def _get_difference(self):
        difference = self.normalised_mean_cost - self.normalised_cost
        return difference[1:]
    difference = property(_get_difference)

    def get_mode_detail(self):
        '''
        Get the detail info of mode_start, mode_stop, popen_list, mean_open,
        mean_shut as a dictionary.
        '''
        if hasattr(self, 'mode_start'):
            mode_dict = {}
            mode_dict['mode_start'] = self.mode_start
            mode_dict['mode_stop'] = self.mode_stop
            mode_dict['popen_list'] = self.popen_list
            mode_dict['mean_open'] = self.mean_open
            mode_dict['mean_shut'] = self.mean_shut
            mode_dict['separation'] = self._separation_dict[self.mode_number]
            mode_dict['cost_dict'] = self._cost_dict
            mode_dict['mean_cost_dict'] = self._mean_cost_dict
            return mode_dict
        else:
            return None

    def identity(self):
        return '({}:{})'.format(self.patchname,self.cluster_no)

    def __repr__(self):
        return 'Cluster({}/{})'.format(self.patchname,self.cluster_no)


    def __str__(self):
        str_filepath = 'Patch Name: {} \n'.format(self.patchname)
        str_cluster_no = 'Cluster number: {} \n'.format(int(self.cluster_no))
        str_start_end = 'From {:.2f} s to {:.2f} s. \n'.format(self.start/1000, self.end/1000)
        str_duration = 'Cluster duration: {:.2f} ms \n'.format(self.duration)
        str_amp = 'Mean amplitude: {:.2f} pA. \n'.format(self.amp)
        str_popen = 'Popen is {:.2f}'.format(self.popen)
        return str_filepath+str_cluster_no+str_start_end+str_duration+str_amp+str_popen


class BatchCluster(Cluster):
    '''
    Cluster class with detailed information for batch analysis.
    Initialize with kwargs for receptor, mutation, composition, agonist, concentration
    Default: 'GlyR', 'wt', 'alpha1', 'glycine', None
    '''
    def __init__(self, cluster, **kwargs):
        self.__dict__ = cluster.__dict__.copy()

        self.receptor = kwargs.get('receptor', 'GlyR')
        self.mutation = kwargs.get('mutation', 'wt')
        self.composition = kwargs.get('composition', 'alpha1')
        self.agonist = kwargs.get('agonist', 'glycine')
        self.concentration = kwargs.get('concentration', None)

    def __repr__(self):
        return 'BatchCluster({}/{})'.format(self.patchname,self.cluster_no)



#
#a = Patch(os.path.join(os.getcwd(),'290610c1_0000.csv'))
#a.scan()
#b = a[1]
#amp = b.amp
#b.impose_resolution()
#b.compute_mode()
#b.compute_mode_detail(True)
