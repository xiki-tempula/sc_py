from collections import defaultdict

dtype = defaultdict(lambda: 'f8')
dtype['patchname'] = 'U20'
dtype['cluster_no'] = 'u8'
dtype['stretch_no'] = 'u8'
dtype['stretch_num'] = 'u4'
dtype['event_num'] = 'u8'
