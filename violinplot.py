# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 09:39:13 2015

@author: zhiyiwu
"""

import numpy as np
from dcpyps.dataset import SCRecord

# 0.1mM glycine
scnfiles = [['/Volumes/c-floor/William/S270T/0.1/15071503.SCN'],
            ['/Volumes/c-floor/William/S270T/0.1/15071504.SCN']]
tres = [0.000025, 0.000025]
conc = [0.0001, 0.0001]
recs = []
bursts = []
for i in range(len(scnfiles)):
    rec = SCRecord(scnfiles[i], conc[i], tres[i])
    rec.record_type = 'recorded'
    recs.append(rec)