# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 21:27:37 2015

@author: xiki_tempula
"""

from collections import OrderedDict

import numpy as np
from dtype import dtype

NOFILTER = [-float('inf'), float('inf')]

class BatchAnalysis:
    '''
    Perform analysis based on the input clusters.
    '''

    def __init__(self, cluster_list):
        self.cluster_list = cluster_list

    def __len__(self):
        return len(self.cluster_list)

    def compute_cluster_summary(self, patchname = True, cluster_no = True,
    popen = True, mean_amp = True, duration = True, event_num = True):
        '''
        Return a dict consists of lists of queried data.
        By default return patchname, cluster_no, popen, amp, duration.
        Optional arguments patchname, cluster_no, popen, amp, duration,
        (to be added).
        '''
        option_list = OrderedDict()

        if patchname:
            if patchname == True:
                option_list['patchname'] = True
            elif type(patchname) == str:
                option_list['patchname'] = [patchname, ]
            else:
                option_list['patchname'] = patchname

        if cluster_no:
            if type(cluster_no) == bool:
                if cluster_no == True:
                    option_list['cluster_no'] = NOFILTER

            else:
                try:
                    cluster_no = int(cluster_no)
                    option_list['cluster_no'] = [cluster_no, cluster_no+1]
                except TypeError:
                    option_list['cluster_no'] = cluster_no


        if popen:
            if popen == True:
                option_list['popen'] = NOFILTER
            else:
                option_list['popen'] = popen

        if mean_amp:
            if mean_amp == True:
                option_list['mean_amp'] = NOFILTER
            else:
                option_list['mean_amp'] = mean_amp

        if duration:
            if duration == True:
                option_list['duration'] = NOFILTER
            else:
                option_list['duration'] = duration

        if event_num:
            if event_num == True:
                option_list['event_num'] = NOFILTER
            else:
                option_list['event_num'] = event_num

        count = 0
        self.summary = np.zeros((len(self.cluster_list), )
                , dtype=[(key, dtype[key]) for key in option_list])

        for cluster in self.cluster_list:
            select = True
            for key in option_list:
                if key == 'patchname':
                    if option_list['patchname'] != True:
                        if not cluster.patchname in option_list['patchname']:
                            select = False
                            break

                else:
                    if ((getattr(cluster,key) < option_list[key][0])
                       or
                       (getattr(cluster,key) >= option_list[key][1])):
                       select = False
                       break
            if select:
                for key in option_list:
                    self.summary[count][key] = getattr(cluster,key)
                count += 1
        self.summary = self.summary[:count]
        return self.summary



    def compute_stretch_summary(self, patchname = True, cluster_no = True,
                                stretch_num = True, popen = True,
                                mean_open = True, mean_shut = True,
                                duration = True, event_num = True):
        '''
        Compute the summary of stretch information.
        '''

        option_list = OrderedDict()

        if patchname:
            if patchname == True:
                option_list['patchname'] = True
            elif type(patchname) == str:
                option_list['patchname'] = [patchname, ]
            else:
                option_list['patchname'] = patchname

        if cluster_no:
            if type(cluster_no) == bool:
                if cluster_no == True:
                    option_list['cluster_no'] = NOFILTER

            else:
                try:
                    cluster_no = int(cluster_no)
                    option_list['cluster_no'] = [cluster_no, cluster_no+1]
                except TypeError:
                    option_list['cluster_no'] = cluster_no

        if stretch_num:
            option_list['stretch_no'] = NOFILTER
            if type(stretch_num) == bool:
                option_list['stretch_num'] = NOFILTER

            else:
                try:
                    stretch_num = int(stretch_num)
                    option_list['stretch_num'] = [stretch_num, stretch_num+1]

                except TypeError:
                    option_list['stretch_num'] = cluster_no


        if popen:
            if popen == True:
                option_list['popen'] = NOFILTER
            else:
                option_list['popen'] = popen

        if mean_open:
            if mean_open == True:
                option_list['mean_open'] = NOFILTER
            else:
                option_list['mean_open'] = mean_open

        if mean_shut:
            if mean_shut == True:
                option_list['mean_shut'] = NOFILTER
            else:
                option_list['mean_shut'] = mean_shut

        if duration:
            if duration == True:
                option_list['duration'] = NOFILTER
            else:
                option_list['duration'] = duration

        if event_num:
            if event_num == True:
                option_list['event_num'] = NOFILTER
            else:
                option_list['event_num'] = event_num

        count = 0
        self.summary = np.zeros((len(self.cluster_list), )
                , dtype=[(key, dtype[key]) for key in option_list])

        for cluster in self.cluster_list :
            mode_dict = cluster.get_mode_detail()
            for index in range(cluster.mode_number):
                select = True
                new_stretch = {'patchname': cluster.patchname,
                               'cluster_no': cluster.cluster_no,
                               'stretch_num': stretch_num,
                               'stretch_no': index+1,
                               'popen': mode_dict['popen_list'][index],
                               'mean_open': mode_dict['mean_open'][index],
                               'mean_shut': mode_dict['mean_shut'][index],
                               'duration': mode_dict['duration'][index],
                               'event_num': mode_dict['event_num'][index]}

                for key in option_list:
                    if key == 'patchname':
                        if option_list['patchname'] != True:
                            if not new_stretch['patchname'] in option_list['patchname']:
                                select = False
                                break

                    else:
                        if ((new_stretch.get(key) < option_list[key][0])
                           or
                           (new_stretch.get(key) >= option_list[key][1])):
                            select = False
                            break
                if select:
                    for key in option_list:
                        self.summary[count][key] = new_stretch[key]
                    count += 1
                    if count >= len(self.summary):
                        self.summary = np.hstack((self.summary,
                                                  np.zeros((len(self.cluster_list), )
                                                  , dtype=[(key, dtype[key]) for key in option_list])))

        self.summary = self.summary[:count]

        return self.summary

    



    def get_length(self):
        '''
        Get a list of the number of shuttings and opening periods in cluster.
        Since cluster is prepared to have the same number of open and shut periods.
        The value is the number of open periods.
        '''
        len_list = []
        for cluster in self.cluster_list:
            len_list.append(len(cluster.open_period))
        return len_list