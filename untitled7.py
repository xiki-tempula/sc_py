# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 14:03:19 2016

@author: zhiyiwu
"""

import numpy as np
from dcpyps import dataset, dcio

intervals = np.arange(10)/10
amplitudes = np.ones(10)
amplitudes[::2] = 0
amplitudes = amplitudes.astype('int')
flags = np.zeros(10)
flags = flags.astype('int')

dcio.scn_write(intervals, amplitudes, flags, filename='./test.SCN')

screcord = dataset.SCRecord(['./test.SCN',])
print(screcord.pint)