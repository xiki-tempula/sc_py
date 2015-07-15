'''
Compute the necessary information for ploting.
Such as x axis, y axis.
'''
import numpy as np
class PlotComputation:
    '''
    Generate the data for ploting.
    '''

    def __init__(self, cluster):
        self.cluster = cluster


    def compute_original(self):
        '''
        Generate the x and y axis for ploting the original trace.
        '''
        # Generate the time which is the x axis
        time = np.zeros(len(self.cluster.open_period) + len(self.cluster.shut_period))
        time[0::2] = self.cluster.open_period
        time[1::2] = self.cluster.shut_period
        time = np.cumsum(time)
        time = np.repeat(time,2)
        time = np.hstack((0, time[:-1]))
        if hasattr(self.cluster, 'start'):
            time += self.cluster.start

        # Generate the amplitude which is the y axis
        amp = np.zeros(len(self.cluster.open_amp) + len(self.cluster.shut_amp))
        amp[0::2] = self.cluster.open_amp
        amp[1::2] = self.cluster.shut_amp
        amp = np.repeat(amp,2)

        return time, amp

    def compute_popen(self):
        '''
        Generate the x and y axis for ploting the Popen of different stretch on their time axis.
        '''
        time = []
        popen = []
        for i in range(self.cluster.mode_number):
            time.append(self.cluster.mode_start[i])
            time.append(self.cluster.mode_stop[i])
            popen.append(self.cluster.popen_list[i])
        popen = np.repeat(popen,2)

        return time, popen

    def compute_open_close(self):
        '''
        Generate a list which contains dictinaries which corresponding to different stretchs including information about open period, shut period,  mean open time, mean shut time.
        '''

        stretch_list = []

        for i in range(self.cluster.mode_number):
            open_period = self.cluster.open_period[self.cluster.separation[i]:self.cluster.separation[i+1]]
            shut_period = self.cluster.shut_period[self.cluster.separation[i]:self.cluster.separation[i+1]]
            stretch_list.append({'open_period': open_period,
                                 'shut_period': shut_period,
                                 'mean_open': self.cluster.mean_open,
                                 'mean_shut': self.cluster.mean_shut})

        return stretch_list

    def compute_cost_diff(self):
        '''
        Return a dict of cost, mean cost and difference.
        '''
        return {'mode_num': self.cluster.mode_number,
                'cost': self.cluster.normalised_cost,
                'mean_cost': self.cluster.normalised_mean_cost,
                'difference': self.cluster.difference,
                'mean_difference':
                np.hstack((np.ones(self.cluster.mode_number-1)*np.mean(self.cluster.difference[1:self.cluster.mode_number]),
                np.ones(len(self.cluster.normalised_cost)-self.cluster.mode_number)*np.mean(self.cluster.difference[self.cluster.mode_number:])))}
