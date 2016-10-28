# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 22:46:15 2015

@author: Joel
"""

import math
import matplotlib as mpl
from matplotlib.colors import colorConverter
#from matplotlib import pylab
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import glob #For extracting filenames from directory


"""
Bresenham
"""
def bresenham(x,y,x2,y2):
    """Brensenham line algorithm"""
    steep = 0
    coords = []
    dx = abs(x2 - x)
    if (x2 - x) > 0: sx = 1
    else: sx = -1
    dy = abs(y2 - y)
    if (y2 - y) > 0: sy = 1
    else: sy = -1
    if dy > dx:
        steep = 1
        x,y = y,x
        dx,dy = dy,dx
        sx,sy = sy,sx
    d = (2 * dy) - dx
    for i in range(0,dx):
        if steep: coords.append((y,x))
        else: coords.append((x,y))
        while d >= 0:
            y = y + sy
            d = d - (2 * dx)
        x = x + sx
        d = d + (2 * dy)
    return coords


def linearColormap(mapName, mapSize, color1, color2, clim, cmin, alphaLim):
    color11 = colorConverter.to_rgba(color1)
    color22 = colorConverter.to_rgba(color2)
    
    cmap = mpl.colors.LinearSegmentedColormap.from_list(mapName,[color11,color22],mapSize)
    cmap._init()
    alpha = np.zeros(mapSize+3)
    first = int(mapSize*((-abs(cmin)-clim[0])/(clim[1]-clim[0])))
    last = int((mapSize+3)*((abs(cmin)-clim[0])/(clim[1]-clim[0])))
    if first > 0:
        alpha[:first:] = np.linspace(alphaLim[1],alphaLim[0],first)
    alpha[last+1::] = np.linspace(alphaLim[0],alphaLim[1],mapSize+3-last-1)
    cmap._lut[:,-1] = alpha
    return cmap


def make_colormap(mapName, mapSize, seq, clim, cmin, alphaLim):
    seq = [colorConverter.to_rgb(element) if isinstance(element,str) else element for element in seq]
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    cmap = mpl.colors.LinearSegmentedColormap(mapName, cdict, mapSize)
    cmap._init()
    alpha = np.zeros(mapSize+3)
    first = int(mapSize*((-abs(cmin)-clim[0])/(clim[1]-clim[0])))
    last = int((mapSize+3)*((abs(cmin)-clim[0])/(clim[1]-clim[0])))
    if first > 0:
        alpha[:first:] = np.linspace(alphaLim[1],alphaLim[0],first)
    alpha[last+1::] = np.linspace(alphaLim[0],alphaLim[1],mapSize+3-last-1)
    cmap._lut[:,-1] = alpha
    return cmap

def makeCmap(mapName, mapSize, seq, clim, cmin, alphaLim):
    seq = [colorConverter.to_rgb(element) if isinstance(element,str) else element for element in seq]
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    cmap = mpl.colors.LinearSegmentedColormap(mapName, cdict, mapSize)
    cmap._init()
    alpha = np.ones(mapSize+3)*alphaLim[1]
    idx = int(mapSize*alphaLim[2])
    
    alpha[0:idx:] = np.linspace(alphaLim[0],alphaLim[1],idx)
    alpha[-3] = alphaLim[0]
    alpha[-2] = alphaLim[1]
    alpha[-1] = alphaLim[1]
    cmap._lut[:,-1] = alpha
    return cmap

def show_plot(figure_id=None):    
    if figure_id is not None:
        fig = plt.figure(num=figure_id)
    else:
        fig = plt.gcf()
    fig.show()
    fig.canvas.draw()

grid = {}
pData = {}
trackData = {}
norm = {}
cmaps = {}
cmaps_Size = {}
clim = {}
cmin = {}
alim = {}
imax = {}

X_Min=-0.0015000000000000000312250225675825276994
Y_Min=-0.0030486282601243420466163858151276144781
Z_Min=-0.0000007442940088194194449747035681463903
X_Max=0.0045972565202486836283268800684709276538
Y_Max=0.0030486282601243420466163858151276144781
Z_Max=0.0000007442940088194194449747035681463903

MeV=0.0000016021765700000000157555805901932189

dirDiv = '/'
dataFolders = ['Ex2D','Ey2D','Electron2D','Proton2D']
pNames = ['Ex2D','Electron2D','Proton2D','tracks']
cbar = False
tracksFadeFactor = math.sqrt(math.sqrt(0.5))
tracksCutoff = 0.1*MeV
trackSkip = 100


cmaps_Size['Electron2D'] = 256
cmaps_Size['Proton2D'] = 256
cmaps_Size['Ex2D'] = 256
cmaps_Size['tracks'] = 256

clim['Electron2D'] = (0,5e6)
clim['Proton2D'] = (0,1e5)
clim['Ex2D'] = (0,5e8)
clim['tracks'] = (0,10*MeV)

cmin['Electron2D'] = 0
cmin['Proton2D'] = 0
cmin['Ex2D'] = 0
cmin['tracks'] = 0

alim['Electron2D'] = 0, 1, 0.75
alim['Proton2D'] = 0, 1, 1
alim['Ex2D'] = 0, 1, 0.75
alim['tracks'] = 1, 1, 1


cmaps['Electron2D'] = makeCmap('my_cmap1', cmaps_Size['Electron2D'], ['g',0.75,'g','k'], clim['Electron2D'], cmin['Electron2D'], alim['Electron2D'])
cmaps['Proton2D'] = makeCmap('my_cmap2', cmaps_Size['Proton2D'], ['m'], clim['Proton2D'], cmin['Proton2D'], alim['Proton2D'])
cmaps['Ex2D'] = makeCmap('my_cmap3', cmaps_Size['Ex2D'], ['w','r',alim['Ex2D'][2],'r','k'], clim['Ex2D'], cmin['Ex2D'], alim['Ex2D'])
cmaps['tracks'] = makeCmap('my_cmap4', cmaps_Size['tracks'], ['yellow', 'red'], clim['tracks'], cmin['tracks'], alim['tracks'])


files = sorted([os.path.basename(x) for x in glob.glob('Ey2D/*.bin')])

trackFiles = [os.path.basename(x) for x in glob.glob('ParticleTracking/*.txt')]
trackDataMatrix = np.zeros((1024,1024))
trackAlpha = np.zeros((1024,1024))


plt.rc('text', usetex=True)
plt.rc('font', family='serif')
fig, ax = plt.subplots(nrows=1)
plotExtent = [X_Min/1e-4,X_Max/1e-4,Y_Min/1e-4,Y_Max/1e-4]

for i in range(len(files)):
    
    for folder in dataFolders:
        Current_filename = files[i]
        size = 1024
        grid[folder] = (np.fromfile(folder+dirDiv+Current_filename, dtype='f')).reshape((size, size))
        
    if i == 0:
        for pName in pNames:
            if pName == 'tracks':
                for track in trackFiles[::trackSkip]:
                    trackData[track] = np.loadtxt('ParticleTracking'+dirDiv+track)
                    if (trackData[track].shape[0] > i) and (trackData[track][i,6] > tracksCutoff):
                        currentBin = (int(1024*(trackData[track][i,1]-Y_Min)/(Y_Max-Y_Min)),int(1024*(trackData[track][i,0]-X_Min)/(X_Max-X_Min)))
                        trackDataMatrix[currentBin] = trackData[track][i,6]
                        trackAlpha[currentBin] = 1
                norm[pName] = mpl.colors.Normalize(clim[pName][0], clim[pName][1])
                img_array = plt.get_cmap(cmaps[pName])(norm[pName](trackDataMatrix))
                img_array[..., 3] = trackAlpha
                imax[pName] = ax.imshow(img_array, extent=plotExtent, aspect=1, origin='lower')
                imax[pName].set_cmap(cmaps[pName])
                imax[pName].set_clim(clim[pName])
            
            else:
                pData[pName] = grid[pName]
            
                norm[pName] = mpl.colors.Normalize(clim[pName][0], clim[pName][1])
                img_array = plt.get_cmap(cmaps[pName])(norm[pName](pData[pName]))
                
                imax[pName] = ax.imshow(img_array, extent=plotExtent, aspect=1, origin='lower')
                imax[pName].set_cmap(cmaps[pName])
                imax[pName].set_clim(clim[pName])
            
            if cbar:
                plt.colorbar(imax[pName],shrink=0.5)

            ax.set_xlabel(r'$x$ ($\mu$m)')
            ax.set_ylabel(r'$y$ ($\mu$m)')

            fig.set_tight_layout(True)

    else:
        for pName in pNames:
            if pName == 'tracks':
                trackAlpha *= tracksFadeFactor
                for track in trackFiles[::trackSkip]:
                    if (trackData[track].shape[0] > i) and (trackData[track][i,6] > tracksCutoff):
                        previousBin = (int(1024*(trackData[track][i-1,1]-Y_Min)/(Y_Max-Y_Min)),int(1024*(trackData[track][i-1,0]-X_Min)/(X_Max-X_Min)))
                        currentBin = (int(1024*(trackData[track][i,1]-Y_Min)/(Y_Max-Y_Min)),int(1024*(trackData[track][i,0]-X_Min)/(X_Max-X_Min)))

                        Bins = bresenham(previousBin[0],previousBin[1],currentBin[0],currentBin[1])
                        for bin in Bins:
                            trackDataMatrix[bin] = trackData[track][i,6]
                            trackAlpha[bin] = 1
                        trackDataMatrix[currentBin] = trackData[track][i,6]
                        trackAlpha[currentBin] = 1

                img_array = plt.get_cmap(cmaps[pName])(norm[pName](trackDataMatrix))
                img_array[..., 3] = trackAlpha
                imax[pName].set_data(img_array)
            else:
                pData[pName] = grid[pName]
                imax[pName].set_data(pData[pName])

    show_plot()
    fig.savefig(os.path.splitext(Current_filename)[0]+'.png', format='png', dpi=300)
