"""
Read from Csv file and generate the cluster data from it.
"""
import os

import numpy as np
import pandas as pd

from dcpyps import dataset

from cost_function import compute_stretch_number, compute_separation_dict, compute_separation_dp, test_dp
from preparation import filter_first_last, impose_resolution
from PlotAnalysis import PlotSingle


class Patch:
    '''
    Patch class contains the patch information and the cluster detail.
    '''

    def __init__(self, path):
        self._filepath, self._patch_name = os.path.split(path)
    
    def read_scn(self, tres=0.0, tcrit=None, event_num = 10, duration = 100):
        '''
        read from scn file and divide the record based on the tcrit.
        '''
        
        self._cluster_dict = {}
        self._cluster_number = 0        
        screcord = dataset.SCRecord([os.path.join(self._filepath, self._patch_name),], 
                               tres=tres/1000, tcrit=tcrit/1000)
                               
        patchname = []
        for patch in screcord.filenames:
            head, tail = os.path.split(patch)
            root, ext = os.path.splitext(tail)
            patchname.append(root)
        patchname = ','.join(patchname)
        self._patch_name = patchname

        start = 0
        end = sum(screcord.pint)
        
        open_period = np.array(screcord.opint)*1000
        shut_period = np.array(screcord.shint)*1000
        open_amp = np.array(screcord.opamp)*-1
        shut_amp = np.array(screcord.shamp)
        open_flag = np.array(screcord.oppro)
        shut_flag = np.array(screcord.shpro)
        
        shut_tcrit = np.where(shut_period < tcrit)[0]
        split_index = np.split(shut_tcrit,
                                   np.where(np.diff(shut_tcrit) != 1)[0]+1)
                                   
                            
        for cluster in split_index:
            if (len(cluster) > event_num) or ((sum(open_period[cluster]) + sum(shut_period[cluster]))> duration):
                self._cluster_number += 1
                new_cluster = Cluster(self._patch_name, self._cluster_number, patch = self)
                new_cluster.add_info(self._cluster_number,
                                         sum(screcord.pint[:cluster[0]]), sum(screcord.pint[:cluster[-1]+1]),
                                        open_period[cluster], shut_period[cluster],
                                        open_amp[cluster], shut_amp[cluster],
                                        open_flag[cluster], shut_flag[cluster],
                                        impose_resolution = False)
                self._cluster_dict[self._cluster_number] = new_cluster
        self._cluster_list = list(self._cluster_dict.keys())

        

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
                new_cluster = Cluster(self._patch_name, i+1, patch = self)

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
        if not hasattr(self, '_cluster_dict'):
            self.scan()

        if output:
            print(self._cluster_dict[cluster_index])
        return self._cluster_dict[cluster_index]

    def get_cluster_list(self, output = False):
        '''
        Return all clusters in this patch.
        '''

        if not hasattr(self, '_cluster_dict'):
            self.scan()

        if output:
            print(self._cluster_list)
        return list(self._cluster_dict.values())



    __getitem__ = get_cluster

    def _get_open_period(self):
        open_period = []
        for cluster in self._cluster_dict.values():
            open_period.append(cluster.open_period)
        open_period = np.hstack(open_period)
        return open_period
    open_period = property(_get_open_period)

    def _get_shut_period(self):
        shut_period = []
        for cluster in self._cluster_dict.values():
            shut_period.append(cluster.shut_period)
        shut_period = np.hstack(shut_period)
        return shut_period
    shut_period = property(_get_shut_period)


    def _get_amp_distribution(self):
        amp_distribution = []
        for cluster in self._cluster_dict.values():
            amp_distribution.append(cluster.mean_amp)
        return amp_distribution
    amp_distribution = property(_get_amp_distribution)

    def _get_popen_distribution(self):
        popen_distribution = []
        for cluster in self._cluster_dict.values():
            popen_distribution.append(cluster.popen)
        return popen_distribution
    popen_distribution = property(_get_popen_distribution)

    def _get_cluster_number(self): return self._cluster_number
    cluster_number  = property(_get_cluster_number)

    def _get_transition_number(self): return len(self.open_period) + len(self.shut_period)
    transition_number = property(_get_transition_number)

    def _get_patchname(self): return self._patch_name
    patchname = property(_get_patchname)

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

    def __init__(self, patchname = None, cluster_no = None, patch = None):
        self.patchname = patchname
        self.cluster_no = cluster_no
        self.patch = patch

    def add_info(self, cluster_no, start, end,
                 open_period, shut_period,
                 open_amp, shut_amp,
                 open_flag, shut_flag,
                 impose_resolution = True):
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
        self.event_num = len(self.open_period) + len(self.shut_period)


        # Impose resolution
        if impose_resolution:
            self.impose_resolution()

        self._expolatory_analysis()

    def load_SCRecord(self, screcord):
        '''
        Load data from SCRecord.
        '''

        patchname = []
        for patch in screcord.filenames:
            head, tail = os.path.split(patch)
            root, ext = os.path.splitext(tail)
            patchname.append(root)
        patchname = ','.join(patchname)
        self.patchname = patchname

        self.start = 0
        self.end = sum(screcord.periods)


        self.open_period = np.array(screcord.opint)*1000
        self.shut_period = np.array(screcord.shint)*1000
        self.open_amp = np.array(screcord.opamp)*-1/1000
        self.shut_amp = np.array(screcord.shamp)
        self._open_flag = np.array(screcord.oppro)
        self._shut_flag = np.array(screcord.shpro)

        self._expolatory_analysis()

    def _expolatory_analysis(self):
        '''
        Calculate the popen, mean amplitude, duration and event_sum.
        '''
        # Calculate the mean Popen
        self.popen = np.sum(self.open_period)/(np.sum(self.open_period) +
        np.sum(self.shut_period))
        # Calculate mean amplitude
        # Only takes into account of the periods longer than 0.3ms
        # If all the periods are less than 0.3ms take the median instead
        self.mean_amp = np.mean(self.open_amp-self.shut_amp)

        # Calculate the duration
        self.duration = sum(self.open_period) + sum(self.shut_period)

        # Number of events in th cluster
        self.event_num = len(self.open_period) + len(self.shut_period)

    def _get_dataframe(self, output_list = ['patchname', 'cluster_no', 'period', 'amp', 'flag']):
        '''
        Generate dataframe for plotting (currently).
        '''
        tempdict = {name: getattr(self, name) for name in output_list}
        df = pd.DataFrame(tempdict)
        df = df[output_list]
        # Check if the even periods are shut and the odd periods are open.
        assert np.mean(df['amp'][::2]) > 10 * np.mean(df['amp'][1::2])

        df['state'] = np.ones(self.event_num, dtype=bool)
        df['state'][1::2] = False
        return df

    dataframe = property(_get_dataframe)

    def _get_period(self):
        period = np.empty(self.event_num)
        period[::2] = self.open_period
        period[1::2] = self.shut_period
        return period

    def _set_period(self, period):
        self.open_period = period[::2]
        self.shut_period = period[1::2]

    period = property(_get_period, _set_period)

    def _get_amp(self):
        amp = np.empty(self.event_num)
        amp[::2] = self.open_amp
        amp[1::2] = self.shut_amp
        return amp

    def _set_amp(self, amp):
        self.open_amp = amp[::2]
        self.shut_amp = amp[1::2]

    amp = property(_get_amp, _set_amp)

    def _get_flag(self):
        flag = np.empty(self.event_num)
        flag[::2] = self._open_flag
        flag[1::2] = self._shut_flag
        return flag

    def _set_flag(self, flag):
        self._open_flag = flag[::2]
        self._shut_flag = flag[1::2]

    flag = property(_get_flag, _set_flag)

    def _get_mean_open(self):
        return np.mean(self.shut_period)
    mean_open = property(_get_mean_open)

    def _get_mean_shut(self):
        return np.mean(self.open_period)
    mean_shut = property(_get_mean_shut)

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
        separation_dict, cost_dict, mean_cost_dict = compute_separation_dict(
        np.log(self.open_period), np.log(self.shut_period), mode_number)
        #test_dp(np.log(self.open_period), np.log(self.shut_period), 10)
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
        self.mode_mean_open = mean_open
        self.mode_mean_shut = mean_shut

        if output:
            for i in range(len(mode_stop)):
                print('Mode {}: Start: {:.2f}, End: {:.2f}, Popen {:.2f}, Mean open: {:.2f}, Mean shut: {:.2f}'.format(
                i+1, self.mode_start[i], self.mode_stop[i], popen_list[i], mean_open[i],
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
            mode_dict['duration'] = self.mode_stop - self.mode_start
            mode_dict['mean_open'] = self.mode_mean_open
            mode_dict['mean_shut'] = self.mode_mean_shut
            mode_dict['separation'] = self._separation_dict[self.mode_number]
            mode_dict['event_num'] = np.diff(mode_dict['separation'])
            mode_dict['cost_dict'] = self._cost_dict
            mode_dict['mean_cost_dict'] = self._mean_cost_dict
            return mode_dict
        else:
            return None

    def identity(self):
        return '({}:{})'.format(self.patchname,self.cluster_no)


    def __eq__(self, other):
        if (self.patchname == other.patchname) and (self.cluster_no == other.cluster_no):
            return True
        else:
            return False

    def __repr__(self):
        return 'Cluster({}/{})'.format(self.patchname,self.cluster_no)


    def __str__(self):
        str_filepath = 'Patch Name: {} \n'.format(self.patchname)
        str_cluster_no = 'Cluster number: {} \n'.format(int(self.cluster_no))
        str_start_end = 'From {:.2f} s to {:.2f} s. \n'.format(self.start/1000, self.end/1000)
        str_duration = 'Cluster duration: {:.2f} ms \n'.format(self.duration)
        str_amp = 'Mean amplitude: {:.2f} pA. \n'.format(self.mean_amp)
        str_popen = 'Popen is {:.2f}'.format(self.popen)
        return str_filepath+str_cluster_no+str_start_end+str_duration+str_amp+str_popen
    
    def show_origianl(self):
        plot = PlotSingle()
        plot.load_cluster(self)
        plot.plot_original(savefig = False, display = True)
        


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
