# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 12:09:24 2016

@author: zhiyiwu
"""
import matplotlib.pyplot as plt
import numpy as np

concentration = [0.3, 1, 3, 10, 100]
popen = [0.032, 0.08966, 0.12257, 0.14855, 0.11373]
error = [0.00593, 0.01155, 0.01469, 0.01267, 0.00968]

def Hill_equation(con, EC50, maxPopen, nH):
    return maxPopen*(1-1/(1+(con/EC50)**nH))
con = 10**np.linspace(-2,2.5,1000)
fig = plt.figure(figsize=(8.45/18*8.43,7.42/18*8.43),dpi=300)
#fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(con, Hill_equation(con, 0.106,0.98,1.8), 'k-', linewidth = 1, 
        label = 'wild type')
#ax.annotate('WT\nEC50: 0.106\nMaximum Popen: 0.98\nHill slope:1.8', 
#            va='top',xy=(5,0.95), size=15)
#ax.axhline(y=0.98, color = 'black', linestyle = ':')
#ax.annotate('0.98', xy=(0.011, 0.99), size = 15)
#ax.axvline(x=0.106, ymax = 0.45 ,
#           color = 'black', linestyle = ':')
#ax.annotate('0.106', xy=(0.11, 0.45), size = 15)
ax.plot(con, Hill_equation(con, 0.65,0.133,2.0), 'k--', linewidth = 1,
        label = 'S270T')
#ax.annotate('S270T\nEC50: 0.65\nMaximum Popen: 0.133\nHill slope: 2.0', xy=(1,0.2), size=15)
#ax.axhline(y=0.133, color = 'black', linestyle = ':')
#ax.annotate('0.13', xy=(0.011, 0.145), size = 15)
#ax.axvline(x=0.65, ymax = 0.06 ,
#           color = 'black', linestyle = ':')
#ax.annotate('0.65', xy=(0.7,0.02), size=15)





ax.errorbar(concentration, popen, yerr=error, barsabove = True,markerfacecolor='white',fmt='o',color = 'black', markersize = 8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.set_xscale('log')
ax.set_xlabel('[Glycine], mM', size =11)
ax.set_ylim([0,1])
ax.set_xlim([0.01,130])
ax.set_ylabel('Popen', size = 11)
[tick.label.set_fontsize(11) for tick in ax.yaxis.get_major_ticks()]
ax.set_xticks([0.01,0.1,1,10,100])
ax.set_xticklabels(['0.01','0.1','1','10','100'], fontsize=11, ha = 'left')
fig.savefig('/Users/zhiyiwu/Google Drive/fig_popen.png',dpi=500)
plt.show()