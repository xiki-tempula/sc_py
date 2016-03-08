# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 10:49:17 2016

@author: zhiyiwu
"""
import matplotlib.pyplot as plt
import numpy as np
from dcpyps import dataset
from scipy.optimize import leastsq

def funcexp(params, x):
    y = np.zeros(len(x))
    for i in range(int(len(params)/2)):
        y += x*params[i]**(-1)*np.exp(x/-params[i])*params[i+1]
    return y
        
        
        
        
    


def plot(ax, filename, tres, exp, os):
    tres /= 1e6
    screcord = dataset.SCRecord([filename,], tres=tres)
    if os == 'open':
        x = np.array(screcord.opint)[np.array(screcord.oppro) != 8]
        xlim = 100
    else:
        x = np.array(screcord.shint)[np.array(screcord.shpro) != 8]
        xlim = 1000
    x*=1000
    n=len(x)
    if n <= 300:
        nbdec = 5.0
    elif n <= 1000:
        nbdec = 8.0
    elif n <= 3000:
        nbdec = 10.0
    else:
        nbdec = 12.0
    bins = np.arange(np.log10(tres*1000), np.log10(xlim) + np.log10(10)/nbdec, np.log10(10)/nbdec)
    bins = 10**bins
    hist, bin_edges = np.histogram(x, bins = bins)
    
    plothist = np.hstack((0, np.repeat(hist, 2), 0)).astype(float)
    plotbin_edges = np.repeat(bin_edges, 2)    
    
    params = np.zeros(len(exp['value'])*2)
    params[::2]=exp['value']
    params[1::2]=np.array(exp['area'])*2.30259*np.log10(10)/nbdec/100*n
    ErrorFunc=lambda tpl,x,y: funcexp(tpl,x)-y
    tplFinal1,success= leastsq(ErrorFunc, params, args=(plotbin_edges[1:], plothist[1:]))
    exp1 = {}    
    exp1['value'] = tplFinal1[::2]
    exp1['area'] = tplFinal1[1::2]
    plothist = np.sqrt(plothist)
    ax.plot(plotbin_edges, plothist, 'k')
    
    x = 10**np.linspace(np.log10(0.01), np.log10(xlim), 1000)
    sum_y=np.zeros(1000)
    for i in range(len(exp['value'])):
        y = x*exp1['value'][i]**(-1)*np.exp(x/-exp1['value'][i])*exp1['area'][i]
        ax.plot(x,np.sqrt(y), 'k--')
        sum_y+=y
        
    ax.plot(x, np.sqrt(sum_y), 'k')

    
    
    
    ax.set_yticklabels([str(i**2) for i in ax.get_yticks()])
    ax.set_xscale('log', basex=10)
    ax.set_xlim([0.01, xlim])
    if os == 'open':
        ax.set_xticks([0.01,0.1,1,10,100])
        ax.set_xticklabels(['0.01','0.1','1','10','100'], fontsize=11, ha = 'left')
    else:
        ax.set_xticks([0.01,0.1,1,10,100, 1000])
        ax.set_xticklabels(['0.01','0.1','1','10','100', '1000'], fontsize=11, ha = 'left')

    
    

fig = plt.figure(figsize=(16,8))
ax1 = fig.add_subplot(2,4,1)
ax2 = fig.add_subplot(2,4,5)
ax3 = fig.add_subplot(2,4,2)
ax4 = fig.add_subplot(2,4,6)
ax5 = fig.add_subplot(2,4,3)
ax6 = fig.add_subplot(2,4,7)
ax7 = fig.add_subplot(2,4,4)
ax8 = fig.add_subplot(2,4,8)
plot(ax1, '/Users/zhiyiwu/D.SCN', 30, {'value': [0.046, 0.235, 2.27], 'area': [49.3, 45.8, 4.9]}, 'open')
plot(ax2, '/Users/zhiyiwu/D.SCN', 30, {'value': [0.0128, 0.706, 11.6, 97.4], 'area': [24.5, 7.6, 35.9,32]}, 'close')
plot(ax3, '/Users/zhiyiwu/F.SCN', 30, {'value': [0.106, 0.410, 3.49], 'area': [42, 51.9, 6.1]}, 'open')
plot(ax4, '/Users/zhiyiwu/F.SCN', 30, {'value': [0.0206, 1.96, 9.11,159.8], 'area': [24.5, 36.5, 37.4, 1.5]}, 'close')
plot(ax5, '/Users/zhiyiwu/I.SCN', 20, {'value': [0.0889, 0.3, 3.01], 'area': [43.4, 53.5, 3.1]}, 'open')
plot(ax6, '/Users/zhiyiwu/I.SCN', 20, {'value': [0.0227, 2.21, 10.3, 111.9], 'area': [11.3, 49.2, 38, 1.5]}, 'close')
plot(ax7, '/Users/zhiyiwu/M.SCN', 20, {'value': [0.0302, 0.208, 2.52], 'area': [17.8, 77, 5.1]}, 'open')
plot(ax8, '/Users/zhiyiwu/M.SCN', 20, {'value': [0.0141, 1.87, 10.1], 'area': [7.6, 78, 14.1]}, 'close')