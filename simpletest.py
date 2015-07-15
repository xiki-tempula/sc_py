'''
Unit test
'''
import os
import random
import shutil

import numpy as np

from info import Patch
from PlotAnalysis import PlotMPL

class TestSuit:
    '''
    Unit test.
    '''

    def __init__(self, patch_num = 5, cluster_num = 5, stretch_num = 5, stretch_len = 1000, open_amp = 5, shut_amp = 0):
        '''
        Create testing data.
        '''
        random_float = str(random.random())[2:]
        self._dir = os.path.join(os.getcwd(),'Unit_test_temp'+random_float)
        try:
            os.makedirs(self._dir)
        except FileExistsError:
            print('File already exist.')

        self._patch_list = {}
        self._name_list = ['test_csv{}.csv'.format(i) for i in range(patch_num)]
        for i, name in enumerate(self._name_list):
            new_patch = {}

            csv_state = []
            csv_start = []
            csv_end = []
            csv_amp = []
            csv_dwell = []

            start_time = np.array(sorted(random.sample(range(10), cluster_num))) * 60000 + np.array(random.sample(range(1000), cluster_num))

            for j in range(cluster_num):
                new_cluster = {}
                new_cluster['start'] = start_time[j]
                if stretch_num >1:
                    new_cluster['stretch'] = np.random.randint(1, stretch_num)
                else:
                    new_cluster['stretch'] = 1
                new_cluster['mean_open'] = np.linspace(0.6, 1.4, new_cluster['stretch'])
                np.random.shuffle(new_cluster['mean_open'])
                new_cluster['mean_shut'] = np.linspace(0.6, 1.4, new_cluster['stretch'])
                np.random.shuffle(new_cluster['mean_shut'])

                new_cluster['open_amp'] = []
                new_cluster['shut_amp'] = []
                new_cluster['open_period'] = []
                new_cluster['shut_period'] = []

                temp_state = np.empty(new_cluster['stretch']*stretch_len*2)
                temp_amp = np.empty(new_cluster['stretch']*stretch_len*2)
                temp_dwell = np.empty(new_cluster['stretch']*stretch_len*2)

                for k in range(new_cluster['stretch']):
                    temp_state[k*stretch_len*2: (k+1)*stretch_len*2:2] = 1
                    temp_state[k*stretch_len*2+1: (k+1)*stretch_len*2:2] = 0

                    new_cluster[k] = {}

                    new_cluster[k]['open_amp'] = np.random.normal(loc = open_amp, scale = 0.5, size = stretch_len)
                    new_cluster['open_amp'].append(new_cluster[k]['open_amp'])

                    temp_amp[k*stretch_len*2: (k+1)*stretch_len*2:2] = new_cluster[k]['open_amp']

                    new_cluster[k]['shut_amp'] = np.random.normal(loc = shut_amp, scale = 0.5, size = stretch_len)
                    new_cluster['shut_amp'].append(new_cluster[k]['shut_amp'])

                    temp_amp[k*stretch_len*2+1: (k+1)*stretch_len*2:2] = new_cluster[k]['shut_amp']

                    new_cluster[k]['open_period'] = np.exp(np.random.normal(loc = np.log(new_cluster['mean_open'][k]), scale = 0.05, size = stretch_len))
                    new_cluster['open_period'].append(new_cluster[k]['open_period'])

                    temp_dwell[k*stretch_len*2: (k+1)*stretch_len*2:2] = new_cluster[k]['open_period']

                    new_cluster[k]['shut_period'] = np.exp(np.random.normal(loc = np.log(new_cluster['mean_shut'][k]), scale = 0.05, size = stretch_len))
                    new_cluster['shut_period'].append(new_cluster[k]['shut_period'])

                    temp_dwell[k*stretch_len*2+1: (k+1)*stretch_len*2:2] = new_cluster[k]['shut_period']

                dwell = np.cumsum(temp_dwell)
                temp_start = start_time[j] + np.hstack((0, dwell[:-1]))
                temp_end = start_time[j] + dwell

                csv_state.append(np.append(temp_state, np.nan))
                csv_start.append(np.append(temp_start, np.nan))
                csv_end.append(np.append(temp_end, np.nan))
                csv_amp.append(np.append(temp_amp, np.nan))
                csv_dwell.append(np.append(temp_dwell, np.nan))

                new_cluster['open_amp'] = np.hstack(new_cluster['open_amp'])
                new_cluster['shut_amp'] = np.hstack(new_cluster['shut_amp'])
                new_cluster['open_period'] = np.hstack(new_cluster['open_period'])
                new_cluster['shut_period'] = np.hstack(new_cluster['shut_period'])
                new_patch[j] = new_cluster

            csv_state = np.hstack(csv_state)
            csv_start = np.hstack(csv_start)
            csv_end = np.hstack(csv_end)
            csv_amp = np.hstack(csv_amp)
            csv_dwell = np.hstack(csv_dwell)

            empty_col = np.empty(len(csv_state))
            csv = np.vstack((empty_col, empty_col, csv_state, empty_col, csv_start, csv_end, csv_amp, empty_col, csv_dwell))
            csv = np.transpose(csv)
            np.savetxt(os.path.join(self._dir, self._name_list[i]), csv, delimiter=',')

            self._patch_list[name] = new_patch

    def test_info(self):
        '''
        Test the info module.
        '''

        for patch in self._name_list:
            test_patch = Patch(os.path.join(self._dir, patch))
            test_patch.scan()
            for index, cluster in enumerate(test_patch):
                # Testing basic information loading
                test_start = abs(cluster.start - self._patch_list[patch][index]['start'])
                if test_start > 0.0001:
                    print('Module Info "start" test failed')
                    print('Expected: {}, Obtained: {}'.format(self._patch_list[patch][index]['start'],
                    cluster.start))

                test_open_period = sum((cluster.open_period - self._patch_list[patch][index]['open_period'])**2)
                if test_open_period > 0.0001:
                    print('Module Info "open_period" test failed')
                    print('Total difference: {}'.format(test_open_period))

                test_shut_period = sum((cluster.shut_period - self._patch_list[patch][index]['shut_period'])**2)
                if test_shut_period > 0.0001:
                    print('Module Info "shut_period" test failed')
                    print('Total difference: {}'.format(test_shut_period))

                test_open_amp = sum((cluster.open_amp - self._patch_list[patch][index]['open_amp'])**2)
                if test_open_amp > 0.0001:
                    print('Module Info "open_amp" test failed')
                    print('Total difference: {}'.format(test_open_amp))

                test_shut_amp = sum((cluster.shut_amp - self._patch_list[patch][index]['shut_amp'])**2)
                if test_shut_amp > 0.0001:
                    print('Module Info "shut_amp" test failed')
                    print('Total difference: {}'.format(test_shut_amp))

    def test_PlotComputation_using_PlotMPL(self):
        '''
        Testing the PlotComputation using the PlotMPL module which uses Matplotlib as backend.
        '''
        for patch in self._name_list:
            test_patch = Patch(os.path.join(self._dir, patch))
            test_patch.scan()
            for index, cluster in enumerate(test_patch):
                cluster.compute_mode()
                cluster.compute_mode_detail()
                test_plot = PlotMPL(self._dir)
                test_plot.load_cluster(cluster)
                test_plot.plot_original()
                test_plot.plot_popen_on_original()
                test_plot.plot_open_close()
                test_plot.plot_cost_difference()


    def finish_test(self):
        '''
        Delete the test file generate during the test.
        '''
        shutil.rmtree(self._dir)



A = TestSuit()
A.test_info()
A.test_PlotComputation_using_PlotMPL()
#A.finish_test()
