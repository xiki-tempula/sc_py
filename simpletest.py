'''
Unit test
'''
import os
import random
import shutil
from collections import OrderedDict
import copy

import numpy as np

from info import Patch
from PlotAnalysis import PlotSingle
from batch_analysis import BatchAnalysis
from batch_query import Batch

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

        self.patch_num = patch_num
        self.cluster_num = cluster_num
        self.stretch_num = stretch_num
        self.stretch_len = stretch_len
        self.open_amp = open_amp
        self.shut_amp = shut_amp


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
                test_plot = PlotSingle(self._dir)
                test_plot.load_cluster(cluster)
                test_plot.plot_original()
                test_plot.plot_popen_on_original()
                test_plot.plot_open_close()
                test_plot.plot_cost_difference()

    def test_batch_analysis(self):
        '''
        test the batch analysis.
        '''
        cluster_list = []
        for patch in self._name_list:
            test_patch = Patch(os.path.join(self._dir, patch))
            test_patch.scan()
            for cluster in test_patch:
                cluster.compute_mode()
                cluster.compute_mode_detail()
                cluster_list.append(cluster)

        # Test BatchAnalysis class
        batch_analysis = BatchAnalysis(list(cluster_list))
        test_dict = batch_analysis.compute_cluster_summary()



        for patchname in self._name_list:
            for cluster_no in range(1, self.cluster_num+1):
                test_dict = batch_analysis.compute_cluster_summary(
                patchname = patchname, cluster_no = cluster_no)

                temp_amp = np.mean(self._patch_list[patchname][cluster_no-1]['open_amp']
                                   -
                                   self._patch_list[patchname][cluster_no-1]['shut_amp'])
                if abs(test_dict['mean_amp'] - temp_amp) > 0.0001:
                    print('Amplitude error')

                temp_duration = (sum(self._patch_list[patchname][cluster_no-1]['open_period'])
                                 +
                                 sum(self._patch_list[patchname][cluster_no-1]['shut_period']))

                if abs(test_dict['duration'] - temp_duration) > 0.0001:
                    print('Duration error')

                temp_popen = sum(self._patch_list[patchname][cluster_no-1]['open_period']) / temp_duration
                if abs(test_dict['popen'] - temp_popen) > 0.0001:
                    print('Popen error')

        # Test StretchSummary class

        batch_analysis.compute_stretch_summary()

    def test_batch_query(self):
        '''
        test the batch_query module.
        '''
        cluster_list = []
        for patch in self._name_list:
            test_patch = Patch(os.path.join(self._dir, patch))
            test_patch.scan()
            for cluster in test_patch:
                cluster_list.append(cluster)
        # Test search orded folder scan
        choice_dict = OrderedDict([('receptor', ['NMDA', 'AMPA']),
                       ('mutation', ['S219P', 'S200T']),
                       ('composition', ['a1','ab']),
                       ('agonist', ['glycine', 'taurine']),
                       ('concentration', ['100', '0.1'])])

        organisation = {keys:{key: [] for key in choice_dict[keys]} for keys in choice_dict}

        for index in range(len(self._name_list)):
            temp_filepath = self._dir
            for key in choice_dict:
                choice = random.choice(choice_dict[key])
                temp_filepath = os.path.join(temp_filepath, choice)
                organisation[key][choice].extend([index]*self.cluster_num)
            try:
                os.makedirs(temp_filepath)
            except FileExistsError:
                pass
            shutil.copy2(os.path.join(self._dir, self._name_list[index]),
                      os.path.join(temp_filepath, self._name_list[index]))

        test_batch = Batch(folder_list = self._dir)
        if len(test_batch.scan_folder()) != len(cluster_list):
            print('scan_folder error')
        test_cluster_list = test_batch.scan_orded_folder(clear = True,export = True)
        copy_organisation = copy.deepcopy(organisation)
        for cluster in test_cluster_list:
            index = self._name_list.index(cluster.patchname)
            for key in organisation:
                if not index in organisation[key][getattr(cluster, key)]:
                    print('scan_orded_folder error')
                else:
                    copy_organisation[key][getattr(cluster, key)].remove(index)
        for i in copy_organisation:
            for j in copy_organisation[i]:
                if copy_organisation[i][j]:
                    print('scan_orded_folder error')

        # Test query
        copy_organisation = copy.deepcopy(organisation)
        for i in organisation:
            for j in organisation[i]:
                if organisation[i][j]:
                    query_list = test_batch.query(**{i: j})
                    for cluster in query_list:
                        index = self._name_list.index(cluster.patchname)
                        try:
                            copy_organisation[i][j].remove(index)
                        except ValueError:
                            print('query error')
        for i in copy_organisation:
            for j in copy_organisation[i]:
                if copy_organisation[i][j]:
                    print('query error')

        # Test filter




    def finish_test(self):
        '''
        Delete the test file generate during the test.
        '''
        shutil.rmtree(self._dir)



A = TestSuit()
A.test_info()
#A.test_PlotComputation_using_PlotMPL()
A.test_batch_analysis()
A.test_batch_query()
A.finish_test()
