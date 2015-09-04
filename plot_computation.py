'''
Compute the necessary information for ploting.
Such as x axis, y axis.
'''
import numpy as np
import matplotlib.pyplot as plt
from batch_analysis import BatchAnalysis

class PlotSingleCluster:
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

        return np.array(time), popen

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
        cost_diff = {'mode_num': self.cluster.mode_number,
                'cost': self.cluster.normalised_cost,
                'mean_cost': self.cluster.normalised_mean_cost,
                'difference': self.cluster.difference}

        mean_difference = np.hstack((np.ones(self.cluster.mode_number-1)*np.mean(self.cluster.difference[:self.cluster.mode_number-1]),
                np.ones(len(self.cluster.normalised_cost)-self.cluster.mode_number)*np.mean(self.cluster.difference[self.cluster.mode_number-1:])))
        cost_diff['mean_difference'] = mean_difference
        return cost_diff
    
def separate_multiply_line(x, y, tracelength = 5e6):
     
     '''
     Create a list of x and y which is chopped into length of tracelength.
     '''
     new_x = []
     new_y = []
     offset = x[0]
     x = x - offset
     totallength = x[-1]
     fulllength_trace = int(totallength//tracelength)
     if fulllength_trace == 0:
         # If trace doesn't reach full length, don't change
         new_x.append(x)
         new_y.append(y)
     else:
        
         # Create first trace
         final_index = np.where(x > tracelength)[0][0]
         new_x.append(np.append(x[:final_index], tracelength))
         new_y.append(y[:final_index+1])
        
         for i in range(1,fulllength_trace):
             # made up te middle part
             first_index = np.where(x <= tracelength*i)[0][-1]
             final_index = np.where(x > tracelength*(i+1))[0][0]
             check = True
             if x[final_index-1] == tracelength*(i+1):
                 new_x.append(np.hstack((tracelength*i,x[first_index+1:final_index])))
                 new_y.append(y[first_index:final_index])
                 check = False
             if x[first_index] == tracelength*(i):
                 new_x.append(np.hstack((x[first_index+1:final_index], tracelength*(i+1))))
                 new_y.append(y[first_index+1:final_index+1])
                 check = False
             if check:
                 new_x.append(np.hstack((tracelength*i,x[first_index+1:final_index], tracelength*(i+1))))
                 new_y.append(y[first_index:final_index+1])
        
         # Make the final trace
         first_index = np.where(x <= tracelength*fulllength_trace)[0][-1]
         new_x.append(np.append(tracelength*fulllength_trace, 
                       x[first_index+1:]))
         new_y.append(y[first_index:])
    
     for i in range(len(new_x)):
         new_x[i] = new_x[i]+offset
     return new_x, new_y



class PlotMultiCluster:
    '''
    Compute the information for multiply clusters.
    '''
    def __init__(self, summary):
        self.summary = summary

    def compute_hist(self, element, bins = None):
        '''
        Provide Popen list for ploting histogram.
        '''
        if element in self.summary.dtype.names:
            data = self.summary[element]
            if bins:
                return np.histogram(data, bins=bins)
            else:
                return np.histogram(data)
                
        else:
            raise KeyError('{} is not in the summary array.'.format(element))
            
