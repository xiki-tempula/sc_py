# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 09:39:13 2015

@author: zhiyiwu
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('/Volumes/c-floor/William/S270T/ekdist.csv')
df['patchname'] = df['patchname'].astype(str)

#fig = plt.figure()
#ax1 = fig.add_subplot(211)
#ax2 = fig.add_subplot(212)
#for con in df['concentration'].unique():
#    area = np.array(df.loc[(df['concentration'] == con) & (df['state'] == 0), 'area'])
#    kinetic_constant = np.array(df.loc[(df['concentration'] == con) & (df['state'] == 0), 'kinetic_constant'])
#    kinetic_constant = np.repeat(kinetic_constant, 3)
#    y = np.zeros(len(kinetic_constant))
#    y[1::3] = area
#    ax1.plot(kinetic_constant,y, label = con, linewidth=1)
#    ax1.set_xlabel('kinetic constant')
#    ax1.set_ylabel('area')
#    ax1.set_xscale('log')
#    ax1.legend()
#    
#    area = np.array(df.loc[(df['concentration'] == con) & (df['state'] == 1), 'area'])
#    kinetic_constant = np.array(df.loc[(df['concentration'] == con) & (df['state'] == 1), 'kinetic_constant'])
#    kinetic_constant = np.repeat(kinetic_constant, 3)
#    y = np.zeros(len(kinetic_constant))
#    y[1::3] = area
#    ax2.set_xlabel('kinetic constant')
#    ax2.set_ylabel('area')
#    ax2.plot(kinetic_constant,y, label = con, linewidth=1)
#    ax2.set_xscale('log')
#    ax2.legend()
#
#fig.set_size_inches(22,17)
#fig.savefig('/Volumes/c-floor/William/S270T/ekdist.png', dpi=150)

con = []
name = []
cluster_no = []
for i in range(len(df)):
    if not df.iloc[i]['concentration'] in con:
        con.append(df.iloc[i]['concentration'])
        index = 0
    if not df.iloc[i]['patchname'] in name:
        name.append(df.iloc[i]['patchname'])
        index += 1
    cluster_no.append(index)
df['cluster_no']=cluster_no
#sns.factorplot(x='kinetic_constant',y='cluster_no',
#               row = 'concentration', col = 'state', data = df, kind = 'strip')
#plt.xscale('log')
g = sns.FacetGrid(df, row = 'concentration', col = 'state', 
                  xlim = [10e-4,10e3], sharey=False)
g.map(plt.scatter, "kinetic_constant","cluster_no")
g.set(xscale="log")
plt.savefig('/Volumes/c-floor/William/S270T/ekdistb.png', dpi=150)
