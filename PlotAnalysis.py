# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 16:41:03 2015

@author: zhiyiwu
"""
import os

import numpy as np
import matplotlib.pyplot as plt

from info import Patch
from plot_computation import PlotComputation

class PlotMPL:
    '''
    Plotting for the single channel analysis.
    '''

    def __init__(self, filepath = os.getcwd()):
        self.filepath = filepath
        self._plot_dict = {}

    def load_cluster(self, cluster):
        '''
        Load necessary information from cluster object.
        '''

        self.cluster_data = PlotComputation(cluster)
        self.name = cluster.identity()
        '''
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
        '''


    def plot_original(self, fig = plt.figure(), savefig = True):
        '''
        Plot the original trace.
        '''
        fig.clf()
        # Build X axis
        time, amp = self.cluster_data.compute_original()

        ax1 = fig.add_subplot(111)
        ax1.plot(time, amp, color = 'black', lw=1,
                                label = 'Original trace')
        ax1.set_xlim([time[0], time[-1]])
        ax1.set_xlabel('Time (ms)')
        ax1.set_ylabel('Amplitude (pA)')
        ax1.set_title('Original trace')
        self._plot_dict['original'] = fig
        if savefig:
            fig.savefig(os.path.join(self.filepath,self.name+'_Original.png'),dpi=300)


    def plot_popen_on_original(self, savefig = True):
        '''
        Plot the Popen of different modes on the original trace.
        '''

        if 'original' in self._plot_dict:
            self.plot_original()
        fig = self._plot_dict['original']
        if len(fig.get_axes()) == 1:
            ax2 = fig.get_axes()[0].twinx()
        else:
            raise IndexError('More than one axis in the figure')

        time, popen = self.cluster_data.compute_popen()

        ax2.plot(time, popen, color = 'blue', label = 'Popen')
        ax2.set_ylabel('Popen')
        ax2.yaxis.label.set_color('blue')
        ax2.set_ylim([0, 1])
        ax2.set_xlim([time[0], time[-1]])
        for tl in ax2.get_yticklabels():
            tl.set_color('blue')
        if savefig:
            fig.savefig(os.path.join(self.filepath,self.name+'Popen.png'),dpi=300)

    def plot_open_close(self, fig = plt.figure(), savefig = True):
        '''
        Plot the open period versus shut periods.
        '''

        stretch_list = self.cluster_data.compute_open_close()
        mode_num = len(stretch_list)

        fig.clf()
        ax = fig.add_subplot(111)
        cmap = np.linspace(0,1,mode_num)

        for index, stretch in enumerate(stretch_list):
            ax.scatter(stretch['open_period'], stretch['shut_period'],
                       facecolors='none',
                       edgecolors=plt.cm.spectral(cmap[index]),
                       s=1)
            ax.scatter(stretch['mean_open'], stretch['mean_shut'],
                       color=plt.cm.spectral(cmap[index]),
                       s=100)

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_ylim([np.exp(0.3), np.exp(7)])
        ax.set_xlim([np.exp(0.3), np.exp(5)])
        ax.set_xlabel('Open period (ms in log scale)')
        ax.set_ylabel('Shut period (ms in log scale)')
        ax.set_title('Open/Shut')
        if savefig:
            fig.savefig(os.path.join(self.filepath,self.name+'Open_Shut.png'),dpi=300)

    def plot_cost_difference(self, fig = plt.figure(), savefig = True):
        '''
        Plot the cost function, and the difference between the cost and
        normalised cost function, which are all normalised by dividing by the
        cluster length.
        '''
        fig.clf()

        # get the data
        dataset = self.cluster_data.compute_cost_diff()
        mode_num = dataset['mode_num']
        cost = dataset['cost']
        mean_cost = dataset['mean_cost']
        difference = dataset['difference']
        mean_difference = dataset['mean_difference']
        x = range(1, len(cost)+1)

        # Plot cost and mean cost function
        ax1 = fig.add_subplot(211)
        ax1.plot(x, cost, color = 'blue', label = 'cost')
        ax1.plot(x, mean_cost, color = 'red', label = 'mean cost')
        ax1.plot(mode_num, cost[mode_num - 1], 'o')
        ax1.plot(mode_num, mean_cost[mode_num - 1], 'o')
        ax1.set_xlabel('Mode number')
        ax1.set_ylabel('Normalised cost')
        ax1.legend()
        # ax1.set_ylim(bottom=0)

        # Plot the difference between two cost
        x = range(2, len(cost)+1)
        ax2 = fig.add_subplot(212)
        ax2.plot(x, difference, 'o')
        ax2.plot(x, mean_difference)
        ax1.set_xlabel('Mode number')
        ax1.set_ylabel('Normalised cost difference')
        ax1.set_title('Cost/Difference')

        if savefig:
            fig.savefig(os.path.join(self.filepath,self.name+'Cost_Difference.png'),dpi=300)

#
#a = Patch(os.path.join(os.getcwd(),'290610c1_0000.csv'))
#a.scan()
#b = a[1]
#b.compute_mode()
#b.compute_mode_detail(True)
#c = PlotAnalysis()
#c.load_cluster(b)
#c.plot_original()
#c.plot_popen_on_original()
#c.plot_open_close()
#c.plot_cost_difference()
#plt.show()
