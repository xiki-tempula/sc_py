from collections import defaultdict

import numpy as np

dtype = defaultdict(lambda: 'f8')
dtype['patchname'] = 'U20'
dtype['cluster_no'] = 'u8'
dtype['stretch_no'] = 'u8'
dtype['stretch_num'] = 'u4'
dtype['event_num'] = 'u8'
dtype['cluster_number'] = 'u8'
dtype['transition_number'] = np.uint16