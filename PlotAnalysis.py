# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 16:41:03 2015

@author: zhiyiwu
"""
import numpy as np
import matplotlib.pyplot as plt
from info import Patch
import os

class PlotAnalysis:
    '''
    Plotting for the single channel analysis.
    '''
    
    def __init__(self, open_period = np.random.exponential(1,100), 
                 shut_period = np.random.exponential(1,100)):
        self._open_period = open_period
        self._shut_period = shut_period
        self._open_amp = np.ones(len(open_period))
        self._shut_amp = np.zeros(len(shut_period))
        self._start = 0
        self._end = sum(open_period) + sum(shut_period)
    
    def define_amp(self, open_amp, shut_amp):
        '''
        Change the default one for open amp and zero for shut amplitude.
        '''
        
        self._open_amp = open_amp
        self._shut_amp = shut_amp
    
    def define_start_end(self, start, end):
        '''
        Change the default 0 for start and cluster length for end.
        '''
        
        self._start = start
        self._end = end
    
    def load_cluster(self, cluster):
        '''
        Load necessary information from cluster object.
        '''
        
        self._cluster = cluster
        cluster_dict = cluster.get_cluster_detail()
        self._start = cluster_dict['start']
        self._end = cluster_dict['end']
        self._open_period = cluster_dict['open_period']
        self._shut_period = cluster_dict['shut_period']
        self._open_amp = cluster_dict['open_amp']
        self._shut_amp = cluster_dict['shut_amp']
        
        if cluster.get_mode_detail():
            mode_dict = cluster.get_mode_detail()
            self._separation = mode_dict['separation']
            self._mode_start = mode_dict['mode_start']
            self._mode_stop = mode_dict['mode_stop']
            self._popen_list = mode_dict['popen_list']
            self._mean_open = mode_dict['mean_open']
            self._mean_shut = mode_dict['mean_shut']
            self._cost_dict = mode_dict['cost_dict']
            self._mean_cost_dict = mode_dict['mean_cost_dict']

            
    
    def plot_original(self, fig = plt.figure()):
        '''
        Plot the original trace.
        '''
        
        # Build X axis
        time = np.zeros(2*len(self._open_period))
        time[0::2] = self._open_period
        time[1::2] = self._shut_period
        time = np.cumsum(time)
        time = np.repeat(time,2)
        time = np.hstack((self._start, time[:-1]))
        
        # Build Y axis
        amp = np.zeros(2*len(self._open_period))
        amp[0::2] = self._open_amp
        amp[1::2] = self._shut_amp
        amp = np.repeat(amp,2)
        ax1 = fig.add_subplot(111)
        ax1.plot(time, amp, color = 'black', lw=1, 
                                label = 'Original trace')
        ax1.set_xlim([time[0], time[-1]])
        ax1.set_xlabel('Time (ms)')
        ax1.set_ylabel('Amplitude (pA)')
        self._original_plot = fig
    
    def plot_popen_on_original(self):
        '''
        Plot the Popen of different modes on the original trace.
        '''
        
        if ~hasattr(self, '_original_plot'):
            self.plot_original()
            
        if len(self._original_plot.get_axes()) == 1:
            ax2 = self._original_plot.get_axes()[0].twinx()
        else:
            raise IndexError('More than one axis in the figure')
        mode_number = len(self._mode_start)
        x = []
        y = []
        for i in range(mode_number):
            x.append(self._mode_start[i])
            x.append(self._mode_stop[i])
            y.append(self._popen_list[i])
        y = np.repeat(y,2)
        ax2.plot(x, y, color = 'blue', label = 'Popen')
        ax2.set_ylabel('Popen')
        ax2.yaxis.label.set_color('blue')
        ax2.set_ylim([0, 1])
        ax2.set_xlim([x[0], x[-1]])
        for tl in ax2.get_yticklabels():
            tl.set_color('blue')
    
    def plot_open_close(self, fig = plt.figure()):
        '''
        Plot the open period versus shut periods.
        '''
        
        if not hasattr(self, '_separation'):
            raise ReferenceError('The mode analysis of this cluster is not performed')
        
        ax = fig.add_subplot(111)
        mode_number = len(self._mode_start)
        cmap = np.linspace(0,1,mode_number)
        for i in range(mode_number):
            open_period = self._open_period[self._separation[i]:self._separation[i+1]]
            shut_period = self._shut_period[self._separation[i]:self._separation[i+1]]
            ax.scatter(open_period, shut_period, facecolors='none', 
                       edgecolors=plt.cm.spectral(cmap[i]),
                        s=1)
        for i in range(mode_number):
            ax.scatter(self._mean_open[i], self._mean_shut[i],  
                       color=plt.cm.spectral(cmap[i]),
                        s=100)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_ylim([np.exp(-4), np.exp(7)])
        ax.set_xlim([np.exp(-4), np.exp(5)])
        ax.set_xlabel('Open period (ms in log scale)')
        ax.set_ylabel('Shut period (ms in log scale)')
        
    def plot_cost_difference(self, fig = plt.figure()):
        '''
        Plot the cost function, and the difference between the cost and 
        normalised cost function, which are all normalised by dividing by the 
        cluster length.
        '''
        
        if not hasattr(self, '_cost_dict'):
            raise ReferenceError('The mode analysis of this cluster is not performed')
        
        # Normalise the cost and 
        cost = np.array([self._cost_dict[i] for i in self._cost_dict])
        mean_cost = np.array([self._mean_cost_dict[i] for i in self._mean_cost_dict])
        cluster_length = len(self._open_period)
        normalised_cost = cost/cluster_length
        normalised_mean_cost = mean_cost/cluster_length
        mode_number = len(self._separation) - 1
        x = range(1, len(cost) + 1)        
        
        # Plot cost and mean cost function
        ax1 = fig.add_subplot(211)
        ax1.plot(x, normalised_cost, color = 'blue', label = 'cost')
        ax1.plot(x, normalised_mean_cost, color = 'red', label = 'mean cost')
        ax1.plot(mode_number, normalised_cost[mode_number - 1], 'o')
        ax1.plot(mode_number, normalised_mean_cost[mode_number - 1], 'o')
        ax1.set_xlabel('Mode number')
        ax1.set_ylabel('Normalised cost')
        ax1.legend()
        # ax1.set_ylim(bottom=0)
        
        # Calculate the difference between cost and mean cost funcion.
        difference  = normalised_mean_cost - normalised_cost
        heterogeneity_mean = np.mean(difference[1:mode_number])
        baseline_mean = np.mean(difference[mode_number:])
        
        # Plot the difference between two cost
        ax2 = fig.add_subplot(212)
        ax2.plot(x, difference, 'o')
        ax2.plot(range(2,mode_number+1), np.ones(mode_number-1)*heterogeneity_mean)
        ax2.plot(range(mode_number+1, len(cost)+1), np.ones(len(cost)-mode_number)*baseline_mean)
        ax1.set_xlabel('Mode number')
        ax1.set_ylabel('Normalised cost difference')
        
        
a = Patch(os.path.join(os.getcwd(),'070710c1_0005_5.csv'))
a.scan()
b = a[1]
b.compute_mode()
b.compute_mode_detail(True)
c = PlotAnalysis()
c.load_cluster(b)
c.plot_original()
c.plot_popen_on_original()
c.plot_open_close()
c.plot_cost_difference()
plt.show()